"""Мелкие «органы чувств» Clawd на компе: погода, микрофон, буфер обмена, непрочитанные в Telegram,
связь с Clawd на телефоне и приём файлов, брошенных на Clawd мышкой."""

import ctypes
import ctypes.wintypes as wt
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import clawd_agent

user32 = ctypes.windll.user32
HERE = Path(__file__).resolve().parent

# ---------- погода (Open-Meteo, без ключа) ----------


def weather(city):
    """{'kind': rain|snow|heat|cold|clear, 'temp': 12, 'text': 'дождь, +12°'} или None."""
    if not city:
        return None
    q = urllib.parse.urlencode({"name": city, "count": 1, "language": "ru"})
    with urllib.request.urlopen(f"https://geocoding-api.open-meteo.com/v1/search?{q}", timeout=10) as r:
        geo = json.loads(r.read().decode("utf-8")).get("results") or []
    if not geo:
        return None
    lat, lon = geo[0]["latitude"], geo[0]["longitude"]
    q = urllib.parse.urlencode({"latitude": lat, "longitude": lon, "wind_speed_unit": "ms",
                                "current": "temperature_2m,weather_code,precipitation,wind_speed_10m,is_day"})
    with urllib.request.urlopen(f"https://api.open-meteo.com/v1/forecast?{q}", timeout=10) as r:
        cur = json.loads(r.read().decode("utf-8"))["current"]
    t, code = float(cur["temperature_2m"]), int(cur["weather_code"])
    wind, day = float(cur.get("wind_speed_10m") or 0), bool(cur.get("is_day", 1))
    if code in (71, 73, 75, 77, 85, 86):
        kind, word = "snow", "снег"
    elif code in (95, 96, 99):
        kind, word = "storm", "гроза"
    elif code in (51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82):
        kind, word = "rain", "дождь"
    elif t >= 27:
        kind, word = "heat", "жара"
    elif t <= -5:
        kind, word = "cold", "мороз"
    else:
        kind, word = "clear", "ясно" if code <= 1 else "облачно"
    windy = f", ветер {round(wind)} м/с" if wind >= 8 else ""
    return {"kind": kind, "temp": round(t), "wind": wind, "day": day, "sunny": code <= 1,
            "text": f"{word}, {'+' if t > 0 else ''}{round(t)}°{windy}", "city": geo[0].get("name", city)}


# ---------- скорость интернета (серверы Cloudflare, без ключа) ----------


def speedtest():
    """{'ping': мс, 'down': Мбит/с, 'up': Мбит/с}. Качает ~25 МБ и отправляет ~8 МБ."""
    import socket
    pings = []
    for _ in range(4):
        t0 = time.perf_counter()
        try:
            socket.create_connection(("speed.cloudflare.com", 443), timeout=3).close()
            pings.append((time.perf_counter() - t0) * 1000)
        except OSError:
            pass
    ua = {"User-Agent": "Mozilla/5.0 Clawd"}
    t0, got = time.perf_counter(), 0
    with urllib.request.urlopen(urllib.request.Request("https://speed.cloudflare.com/__down?bytes=25000000", headers=ua),
                                timeout=30) as r:
        while time.perf_counter() - t0 < 12:
            chunk = r.read(256 * 1024)
            if not chunk:
                break
            got += len(chunk)
    down = got * 8 / (time.perf_counter() - t0) / 1e6
    data = os.urandom(8_000_000)
    t0 = time.perf_counter()
    try:
        urllib.request.urlopen(urllib.request.Request("https://speed.cloudflare.com/__up", data=data, method="POST",
                                                      headers=ua), timeout=30).read()
        up = len(data) * 8 / (time.perf_counter() - t0) / 1e6
    except Exception:
        up = None
    return {"ping": round(min(pings)) if pings else None, "down": round(down, 1), "up": round(up, 1) if up else None}


# ---------- микрофон: запись через winmm (без библиотек) и расшифровка Gemini ----------

_mci = ctypes.windll.winmm.mciSendStringW
REC_FILE = os.path.join(tempfile.gettempdir(), "clawd_voice.wav")


def _mcic(cmd):
    return _mci(cmd, None, 0, None)


def rec_start():
    _mcic("close clawdrec")
    if _mcic("open new type waveaudio alias clawdrec") != 0:
        return False
    # MCI принимает формат только целиком и в таком порядке — иначе молча пишет 8 бит / 11 кГц
    _mcic("set clawdrec time format ms bitspersample 16 channels 1 samplespersec 16000 bytespersec 32000 alignment 2")
    return _mcic("record clawdrec") == 0


def rec_stop():
    """Останавливает запись и возвращает байты WAV (или None)."""
    _mcic("stop clawdrec")
    try:
        if os.path.exists(REC_FILE):
            os.remove(REC_FILE)
    except OSError:
        pass
    _mcic(f'save clawdrec "{REC_FILE}"')
    _mcic("close clawdrec")
    try:
        with open(REC_FILE, "rb") as f:
            data = f.read()
        return data if len(data) > 8000 else None  # меньше ~0.25 с — ничего не сказали
    except OSError:
        return None


def transcribe(wav, cfg=None):
    """Речь → текст. Умеет только Gemini (он принимает звук)."""
    import base64
    cfg = cfg or clawd_agent.load_config()
    if cfg.get("ai_provider") != "gemini" or not str(cfg.get("ai_key", "")).strip():
        raise ValueError("голос работает с ключом Gemini")
    model = str(cfg.get("ai_model", "")).strip() or clawd_agent.DEFAULT_MODELS["gemini"]
    data = clawd_agent._post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        {"contents": [{"role": "user", "parts": [
            {"inline_data": {"mime_type": "audio/wav", "data": base64.b64encode(wav).decode("ascii")}},
            {"text": "Запиши дословно, что сказано (по-русски, без кавычек и пояснений). Если речи нет — верни пустую строку."},
        ]}]},
        {"x-goog-api-key": cfg["ai_key"].strip()},
    )
    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    text = "".join(p.get("text", "") for p in parts if not p.get("thought")).strip().strip('"«»')
    # на тишину модель иногда выдумывает «00:00» или «...» — без букв это не речь
    return text if sum(c.isalpha() for c in text) >= 2 else ""


# ---------- буфер обмена ----------


def clip_seq():
    return user32.GetClipboardSequenceNumber()


def clip_text():
    if not user32.OpenClipboard(None):
        return None
    try:
        user32.GetClipboardData.restype = ctypes.c_void_p
        h = user32.GetClipboardData(13)  # CF_UNICODETEXT
        if not h:
            return None
        k = ctypes.windll.kernel32
        k.GlobalLock.restype = ctypes.c_void_p
        k.GlobalLock.argtypes = [ctypes.c_void_p]
        k.GlobalUnlock.argtypes = [ctypes.c_void_p]
        p = k.GlobalLock(h)
        try:
            return ctypes.wstring_at(p)
        finally:
            k.GlobalUnlock(h)
    finally:
        user32.CloseClipboard()


def page_text(url, limit=6000):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 Clawd"})
    with urllib.request.urlopen(req, timeout=15) as r:
        html = r.read(800_000).decode(r.headers.get_content_charset() or "utf-8", "ignore")
    html = re.sub(r"(?is)<(script|style|noscript|svg|nav|footer|header)\b.*?</\1>", " ", html)
    title = re.search(r"(?is)<title[^>]*>(.*?)</title>", html)
    text = re.sub(r"(?s)<[^>]+>", " ", html)
    text = re.sub(r"&nbsp;|&#160;", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return ((title.group(1).strip() + "\n") if title else "") + text[:limit]


# ---------- Telegram: непрочитанные из заголовка окна («Telegram (12)») ----------


def tg_unread():
    for _, _, exe, title in clawd_agent.windows():
        if exe in clawd_agent.TG_EXES:
            m = re.search(r"\((\d+)\)", title)
            return int(m.group(1)) if m else 0
    return None


# ---------- связь с Clawd на телефоне (по Wi-Fi, код — тот же 6-значный «Код синхронизации») ----------

PHONE_PORT = 8768  # слушает приложение Clawd на телефоне
PC_PORT = 8769  # слушает этот комп


def phone_host():
    cfg = clawd_agent.load_config()
    if cfg.get("phone_ip"):
        return cfg["phone_ip"]
    try:
        return json.loads((HERE / "sender_config.json").read_text(encoding="utf-8")).get("host")
    except Exception:
        return None


def phone_send(event, **data):
    """Событие на телефон: arrive/leave/pc_active. Возвращает ответ телефона (его статистику) или None."""
    cfg = clawd_agent.load_config()
    code, host = str(cfg.get("phone_code", "")).strip(), phone_host()
    if not code or not host:
        return None
    body = json.dumps({"event": event, "port": PC_PORT, **data}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(f"http://{host}:{PHONE_PORT}/pc", data=body, method="POST",
                                 headers={"Content-Type": "application/json", "X-Clawd-Code": code})
    try:
        with urllib.request.urlopen(req, timeout=3) as r:
            raw = r.read().decode("utf-8", "ignore")
            try:
                return json.loads(raw) if raw.startswith("{") else {}
            except ValueError:
                return {}
    except Exception:
        return None


# ---------- созвоны: кто держит микрофон и кто сейчас звучит ----------

CALL_APPS = ("discord.exe", "telegram.exe", "ayugram.exe", "zoom.exe", "teams.exe", "ms-teams.exe", "skype.exe",
             "whatsapp.exe", "slack.exe")


def mic_users():
    """exe, которые прямо сейчас слушают микрофон (Windows сам это записывает для значка микрофона)."""
    import winreg
    users = set()
    base = r"Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone\NonPackaged"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, base) as k:
            i = 0
            while True:
                try:
                    name = winreg.EnumKey(k, i)
                except OSError:
                    break
                i += 1
                try:
                    with winreg.OpenKey(k, name) as sub:
                        stop, _ = winreg.QueryValueEx(sub, "LastUsedTimeStop")
                        if stop == 0:
                            users.add(name.rsplit("#", 1)[-1].lower())
                except OSError:
                    continue
    except OSError:
        pass
    return users


def app_peak(exe):
    """Насколько громко сейчас звучит программа (0..1) — слышно ли собеседника."""
    try:
        from pycaw.pycaw import AudioUtilities, IAudioMeterInformation
        peak = 0.0
        for s in AudioUtilities.GetAllSessions():
            if s.Process and s.Process.name().lower() == exe:
                meter = s._ctl.QueryInterface(IAudioMeterInformation)
                peak = max(peak, meter.GetPeakValue())
        return peak
    except Exception:
        return 0.0


# ---------- праздники ----------


def season():
    """halloween / newyear / valentine / None — по сегодняшней дате."""
    t = time.localtime()
    m, d = t.tm_mon, t.tm_mday
    if (m == 10 and d >= 20) or (m == 11 and d <= 3):
        return "halloween"
    if (m == 12 and d >= 15) or (m == 1 and d <= 15):
        return "newyear"
    if m == 2 and 10 <= d <= 14:
        return "valentine"
    return None


def start_phone_listener(on_event):
    """Принимает события от телефона (уведомления, «Клодик убежал в телефон»). Нужен тот же код."""

    class H(BaseHTTPRequestHandler):
        def do_POST(self):
            code = str(clawd_agent.load_config().get("phone_code", "")).strip()
            if not code or self.headers.get("X-Clawd-Code") != code or self.path != "/phone":
                self.send_response(403)
                self.end_headers()
                return
            try:
                size = min(int(self.headers.get("Content-Length", 0)), 8192)
                data = json.loads(self.rfile.read(size).decode("utf-8") or "{}")
            except Exception:
                data = {}
            # телефон сменил адрес — запоминаем, откуда пришёл
            cfg = clawd_agent.load_config()
            if cfg.get("phone_ip") != self.client_address[0]:
                cfg["phone_ip"] = self.client_address[0]
                clawd_agent.save_config(cfg)
            on_event(data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")

        def log_message(self, *args):
            pass

    try:
        server = ThreadingHTTPServer(("0.0.0.0", PC_PORT), H)
    except OSError:
        return None
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


# ---------- файлы, брошенные мышкой на Clawd → на телефон через PhotoSync ----------

WM_DROPFILES = 0x0233
GWLP_WNDPROC = -4
_WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_ssize_t, wt.HWND, ctypes.c_uint, wt.WPARAM, wt.LPARAM)
_keep = []


def accept_drops(hwnd, on_files):
    """Разрешает бросать файлы на окно Clawd (WM_DROPFILES) и вызывает on_files(list_of_paths)."""
    shell32 = ctypes.windll.shell32
    shell32.DragAcceptFiles(hwnd, True)
    user32.SetWindowLongPtrW.restype = ctypes.c_void_p
    user32.SetWindowLongPtrW.argtypes = [wt.HWND, ctypes.c_int, ctypes.c_void_p]
    user32.CallWindowProcW.restype = ctypes.c_ssize_t
    user32.CallWindowProcW.argtypes = [ctypes.c_void_p, wt.HWND, ctypes.c_uint, wt.WPARAM, wt.LPARAM]
    shell32.DragQueryFileW.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_wchar_p, ctypes.c_uint]
    shell32.DragFinish.argtypes = [ctypes.c_void_p]
    # окно не принимает перетаскивание от программ «выше» по правам — разрешаем сообщения
    for msg in (WM_DROPFILES, 0x0049, 0x004A):
        try:
            user32.ChangeWindowMessageFilterEx(hwnd, msg, 1, None)
        except Exception:
            pass
    old = None

    def proc(h, msg, wp, lp):
        if msg == WM_DROPFILES:
            n = shell32.DragQueryFileW(wp, 0xFFFFFFFF, None, 0)
            files = []
            for i in range(n):
                buf = ctypes.create_unicode_buffer(1024)
                shell32.DragQueryFileW(wp, i, buf, 1024)
                files.append(buf.value)
            shell32.DragFinish(wp)
            on_files(files)
            return 0
        return user32.CallWindowProcW(old, h, msg, wp, lp)

    cb = _WNDPROC(proc)
    _keep.append(cb)
    old = user32.SetWindowLongPtrW(hwnd, GWLP_WNDPROC, ctypes.cast(cb, ctypes.c_void_p))


def can_send_to_phone():
    """PhotoSync лежит рядом — без него файлы на телефон носить нечем."""
    return (HERE / "photo_sender.py").is_file()


def send_to_phone(paths):
    """Отправка через PhotoSync (photo_sender.py сам найдёт телефон и сообщит Clawd о полёте файла)."""
    files = [p for p in paths if os.path.isfile(p)]
    if not files or not can_send_to_phone():
        return False
    py = os.path.join(os.path.dirname(sys.executable), "python.exe")
    p = subprocess.Popen([py, str(HERE / "photo_sender.py"), *files], cwd=str(HERE), stdin=subprocess.PIPE,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x08000000)
    try:
        p.stdin.write(b"\n")
        p.stdin.close()
    except OSError:
        pass
    return True
