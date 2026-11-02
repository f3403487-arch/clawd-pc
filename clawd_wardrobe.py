"""Гардероб Clawd: шапки, очки, шеи, вещи в лапе, спина, узоры на теле и ауры.

Всё нарисовано строками-картинками: каждая буква — цвет из палитры вещи, «.» — пусто.
Общие буквы: B — цвет тела, D — тело темнее, L — тело светлее, E — цвет глаз.
Тот же рисунок рисует окно настроек (clawd_ui.html), поэтому данные отдаются ему как есть.

Как вещь встаёт на Клодика (left/right/top — края тела, mx — его середина):
  head    — низ картинки на строке над головой (dy сдвигает вниз), по центру + dx
  face    — две половинки по 5 клеток, у каждой глаз в 3-м столбце; bridge — чем заполнить
            промежуток между ними, edge — чем дотянуть до края тела (когда тело сплющено)
  neck    — верх картинки на 6-й строке тела, по центру + dx
  hand    — в правой лапе: 1-й столбец над кончиком лапы, низ картинки на уровне лапы
  back    — рисуется ДО тела, верх на строке top + dy: видно только то, что торчит по бокам
  pattern — плитка, которой заливается тело (поверх цвета, под глазами)
  aura    — не рисуется на теле, а сыплет частицами: {"shape", "colors", "every", "fall"}
need: None — открыто сразу, "id" — нужна эта ачивка, число — сколько ачивок всего.
"""

SLOTS = [
    ("head", "Голова", "🎩"), ("face", "Лицо", "🕶"), ("neck", "Шея", "🎀"), ("hand", "В лапе", "🗡"),
    ("back", "Спина", "🦋"), ("pattern", "Узор", "🦓"), ("aura", "Аура", "✨"),
]
SLOT_KEYS = [s for s, _, _ in SLOTS]
# сезонные вещи — во вкладке «Сезонное», сгруппированы по праздникам (носятся в своём слоте)
SEASONS = [
    ("halloween", "Хэллоуин", "🎃"), ("newyear", "Новый год", "🎄"), ("valentine", "День святого Валентина", "💘"),
    ("spring", "Весна", "🌸"), ("summer", "Лето", "☀️"),
]

ITEMS = {}


def _add(key, slot, name, need=None, rows=(), pal=None, dx=0, dy=0, left=(), right=(), bridge=(), edge=(),
         aura=None, auto=False, season=None):
    ITEMS[key] = {"key": key, "slot": slot, "name": name, "need": need, "rows": list(rows), "pal": pal or {},
                  "dx": dx, "dy": dy, "left": list(left), "right": list(right), "bridge": [list(b) for b in bridge],
                  "edge": [list(e) for e in edge], "aura": aura, "auto": auto, "season": season}


# ---------- голова ----------
_add("bow", "head", "Бантик", "pet10", ["m..m", "mxxm"], {"m": "#ff6fa8", "x": "#d94c88"}, dx=3)
_add("party", "head", "Колпак", "ask10", [".ww.", ".yy.", "bbbb"], {"w": "#ffffff", "y": "#ffc94d", "b": "#6fb8ff"})
_add("crown", "head", "Корона", "pet100", ["g.gg.g", "ggrrgg"], {"g": "#ffc94d", "r": "#ff5c7a"})
_add("flower", "head", "Цветок", "days7", [".m.", "mxm", ".m."], {"m": "#ff6fa8", "x": "#ffc94d"}, dx=4, dy=1)
_add("halo", "head", "Нимб", "days30", [".mmmmmm.", "x......x", "........"], {"m": "#ffe08a", "x": "#ffc94d"})
_add("phones", "head", "Наушники", "file10",
     ["..mmmmmmmmmm..", "..............", "xx..........xx", "xx..........xx", "xx..........xx"],
     {"m": "#3a3a3a", "x": "#5e6670"}, dy=4)
_add("tophat", "head", "Цилиндр", None, ["..kkkkkk..", "..kkkkkk..", "..kkkkkk..", "..rrrrrr..", "kkkkkkkkkk"],
     {"k": "#1f1f24", "r": "#c94a3f"})
_add("cowboy", "head", "Ковбойская шляпа", None, ["....bbbb....", "...bbbbbb...", "b..dddddd..b", ".bbbbbbbbbb."],
     {"b": "#8b5a2b", "d": "#5a3a1a"})
_add("cap", "head", "Кепка", None, ["......w.......", "...rrrrrr.....", "..rrrrrrrr....", "..rrrrrrrrvvvv"],
     {"r": "#3b7dd8", "w": "#ffffff", "v": "#2a5aa0"})
_add("beanie", "head", "Шапка-бини", None, [".....pp.....", "...yyyyyy...", "..yyyyyyyy..", "dddddddddddd"],
     {"y": "#e5534b", "d": "#b8322b", "p": "#ffffff"}, dy=1)
_add("chef", "head", "Поварской колпак", 1, ["..wwwwww..", ".wwwwwwww.", ".wwwwwwww.", "..wwwwww..", "..gggggg.."],
     {"w": "#ffffff", "g": "#dfe3ea"})
_add("viking", "head", "Шлем викинга", 2, ["w............w", "ww..........ww", ".wwssssssssww.", "..ssssssssss.."],
     {"w": "#f2e6c8", "s": "#8a8f99"}, dy=1)
_add("wizard", "head", "Шляпа волшебника", 3,
     ["........p.....", ".......pp.....", "......ppp.....", ".....ppypp....", "....pppppp....", "...ppyppppp...",
      "pppppppppppppp"], {"p": "#6a4fc9", "y": "#ffd34d"})
_add("witch", "head", "Шляпа ведьмы", 2,
     ["........k.....", ".......kk.....", "......kkk.....", ".....kkkk.....", "....kooook....", "kkkkkkkkkkkkkk"],
     {"k": "#241a2e", "o": "#f08a24"})
_add("pirate", "head", "Треуголка", "throw20", [".....kkkk.....", "...kkkwwkkk...", ".kkkkkkkkkkkk.", "kkyyyyyyyyyykk"],
     {"k": "#1f1f24", "w": "#ffffff", "y": "#e8b84a"})
_add("headband", "head", "Повязка ниндзя", None, ["rr..............", ".rrrrrrrrrrrrr.."], {"r": "#e5534b"}, dy=1)
_add("tiara", "head", "Диадема", 4, ["...y....", "..yby...", ".y.y.y.y", "yyyyyyyy"], {"y": "#ffd34d", "b": "#6fb8ff"}, dy=1)
_add("antenna", "head", "Антенки", None, ["g........g", ".s......s.", "..s....s.."], {"g": "#8fff6a", "s": "#3a3a3a"})
_add("catears", "head", "Кошачьи ушки", None, ["B..........B", "BB........BB", "BpB......BpB"], {"p": "#ff9fc0"})
_add("bunny", "head", "Ушки зайки", 1, ["..ww....ww..", "..wp....pw..", "..wp....pw..", "..wp....pw..", "..ww....ww.."],
     {"w": "#ffffff", "p": "#ffb3cf"})
_add("horns", "head", "Рожки чертёнка", 3, ["r..........r", "rr........rr"], {"r": "#d6332b"})
_add("propeller", "head", "Кепка с пропеллером", 2,
     ["...yyyyyy...", ".....kk.....", "...rrggbb...", "..rrrggbbb.."],
     {"y": "#ffd34d", "k": "#333333", "r": "#e5534b", "g": "#4fbf98", "b": "#4fa8e8"})
_add("mushroom", "head", "Мухомор", 5, ["...rrrrrr...", ".rrwrrrrwrr.", "rrrrrrwrrrrr"], {"r": "#e5534b", "w": "#ffffff"})
_add("frog", "head", "Шапка-лягушка", 4, ["..gg....gg..", ".gwkg..gwkg.", "gggggggggggg"],
     {"g": "#5cb85c", "w": "#ffffff", "k": "#111111"}, dy=1)
_add("grad", "head", "Шапочка выпускника", "ask50", ["kkkkkkkkkkkkkk", "...kkkkkkkk.y.", "...kkkkkkkk.y."],
     {"k": "#1f1f24", "y": "#ffd34d"})
_add("wreath", "head", "Венок", "days7", [".p..y..b..p.", "gpggyggbggpg"],
     {"p": "#ff6fa8", "y": "#ffd34d", "b": "#6fb8ff", "g": "#4f8a2e"}, dy=1)
_add("crest", "head", "Гребень дракона", 6, [".g...g...g..", "ggg.ggg.ggg."], {"g": "#6bd16b"})
_add("straw", "head", "Соломенная шляпа", None, [".....yyyyyy.....", ".....rrrrrr.....", "yyyyyyyyyyyyyyyy"],
     {"y": "#e8c66a", "r": "#e5534b"})
_add("sprout", "head", "Росток", None, ["gg.gg", ".ggg.", "..s.."], {"g": "#6bd16b", "s": "#3f8a2e"})
_add("bucket", "head", "Панамка", None, ["...bbbbbb...", "..bbbbbbbb..", "bbbbbbbbbbbb"], {"b": "#5aa0d8"}, dy=1)
_add("crown2", "head", "Королевская корона", 10,
     ["y...y...y", "y.y.y.y.y", "yyyyyyyyy", "yrybyryby", "yyyyyyyyy"],
     {"y": "#ffc94d", "r": "#e5534b", "b": "#4fa8e8"})
_add("astro", "head", "Шлем космонавта", 8,
     ["...wwwwww...", "..wccccccw..", ".wcc.ccccw..", ".wccccccccw."], {"w": "#e9ecf2", "c": "#6fb8ff"}, dy=1)
# сами надеваются по погоде и ночью — в шкафу их не видно
_add("nightcap", "head", "Ночной колпак", rows=["......bbw", "..bbbbb..", "wbbbbbbb."],
     pal={"b": "#4a6fd0", "w": "#ffffff"}, auto=True)
_add("umbrella", "head", "Зонтик", rows=["...rrrrrrrr...", "rrrrwrrrrwrrrr", ".......k......"],
     pal={"r": "#e5534b", "w": "#ffffff", "k": "#3a3a3a"}, auto=True)
_add("santa", "head", "Шапка Санты", rows=["..rrrrrrww", "wwwwwwwwww"], pal={"r": "#e53935", "w": "#ffffff"},
     season="newyear")

# ---------- лицо ----------
_add("glasses", "face", "Очки", "ride10", left=["", "mxmmm", ".mmm."], right=["", "mxmmm", ".mmm."],
     pal={"m": "#1a1a1a", "x": "#5e6670"}, bridge=[(1, "m")], edge=[(1, "m")])
_add("eyepatch", "face", "Пиратская повязка", "throw20", left=["mmmmm"], right=["mmmmm", ".mmm.", ".mmm."],
     pal={"m": "#141414"}, bridge=[(0, "m")], edge=[(0, "m")])
_add("round", "face", "Круглые очки", None, left=[".mmm.", "m...m", "m...m", ".mmm."],
     right=[".mmm.", "m...m", "m...m", ".mmm."], pal={"m": "#c9a14a"}, bridge=[(1, "m")])
_add("hearts", "face", "Очки-сердечки", None, left=[".m.m.", "mmmmm", ".mmm.", "..m.."],
     right=[".m.m.", "mmmmm", ".mmm.", "..m.."], pal={"m": "#ff4f8a"}, bridge=[(1, "m")])
_add("stars", "face", "Очки-звёзды", 2, left=["..y..", "yyyyy", ".yyy.", ".y.y."],
     right=["..y..", "yyyyy", ".yyy.", ".y.y."], pal={"y": "#ffd34d"}, bridge=[(1, "y")])
_add("3d", "face", "3D-очки", 1, left=["kkkkk", "krrrk", "krrrk"], right=["kkkkk", "kbbbk", "kbbbk"],
     pal={"k": "#f2f2f2", "r": "#e5534b", "b": "#4fa8e8"}, bridge=[(0, "k"), (1, "k")], edge=[(0, "k")])
_add("visor", "face", "Кибер-визор", 6, left=["", "ccccc", "CCCCC"], right=["", "ccccc", "CCCCC"],
     pal={"c": "#39e6ff", "C": "#1aa6c8"}, bridge=[(1, "c"), (2, "C")], edge=[(1, "c"), (2, "C")])
_add("monocle", "face", "Монокль", 4, right=[".yyy.", "y...y", "y...y", ".yyy.", "....y"], pal={"y": "#e8b84a"})
_add("mustache", "face", "Усы", None, left=["", "", "", ".kkkk", "kk..."], right=["", "", "", "kkkk.", "...kk"],
     pal={"k": "#3a2414"}, bridge=[(3, "k")])
_add("blush", "face", "Румянец", None, left=["", "", "", "rr..."], right=["", "", "", "...rr"], pal={"r": "#ff7aa0"})
_add("clown", "face", "Нос клоуна", 1, left=["", "", "....r", "....r"], right=["", "", "r....", "r...."],
     pal={"r": "#ff3030"}, bridge=[(2, "r"), (3, "r")])
_add("sleepmask", "face", "Маска для сна", 3, left=["", "ppppp", "pkkkp", "ppppp"], right=["", "ppppp", "pkkkp", "ppppp"],
     pal={"p": "#ffb3cf", "k": "#b85a80"}, bridge=[(1, "p"), (2, "p"), (3, "p")], edge=[(1, "p"), (2, "p"), (3, "p")])
_add("scar", "face", "Шрам", 5, left=[".r...", "..r..", "...r."], pal={"r": "#b8322b"})
_add("freckles", "face", "Веснушки", None, left=["", "", "", ".D.D."], right=["", "", "", ".D.D."])
_add("lasers", "face", "Лазерные глаза", 9, left=["", "..R..", "..r..", ".r...", "r...."], right=["", "..R..", "..r..", "...r.", "....r"],
     pal={"r": "#ff2a2a", "R": "#ffb0b0"})

# ---------- шея ----------
_add("scarf", "neck", "Шарф", None, ["mxmmxmmxmmxm", ".........mx.", ".........m.."], {"m": "#e5534b", "x": "#ffc94d"})
_add("bowtie", "neck", "Бабочка", None, ["r...r", "rrRrr", "r...r"], {"r": "#e5534b", "R": "#a52f28"})
_add("tie", "neck", "Галстук", 1, [".r.", ".r.", "rrr", "rrr", ".r."], {"r": "#3b5bd8"})
_add("chain", "neck", "Золотая цепь", 6, ["y........y", ".yy....yy.", "...yyyy...", "....YY...."],
     {"y": "#e8b84a", "Y": "#fff1a0"})
_add("medal", "neck", "Медаль", 5, ["b...b", ".b.b.", "..y..", ".yyy.", "..y.."], {"b": "#3b5bd8", "y": "#ffc94d"})
_add("bell", "neck", "Ошейник с бубенчиком", None, ["rrrrrrrrrrrr", ".....yy.....", ".....yy....."],
     {"r": "#e5534b", "y": "#ffd34d"})
_add("bandana", "neck", "Бандана", 2, ["rwrrrwrrrwrr", "..rrrrrrrr..", "....rrrr....", ".....rr....."],
     {"r": "#d6332b", "w": "#ffffff"})
_add("pearls", "neck", "Жемчуг", 4, ["wWwWwWwWwWwW"], {"w": "#ffffff", "W": "#d9dde6"})
_add("lei", "neck", "Гавайские бусы", 3, ["pypbpypbpypb", "..ppyybbpp.."], {"p": "#ff6fa8", "y": "#ffd34d", "b": "#6fb8ff"})
_add("neckphones", "neck", "Наушники на шее", None, ["kk........kk", ".kkkkkkkkkk."], {"k": "#3a3a3a"})
_add("clover", "neck", "Клевер на удачу", 7, ["..gg..", ".gggg.", "..gg..", "...s.."], {"g": "#4fbf6a", "s": "#2f7a3a"}, dx=2)

# ---------- в лапе ----------
_add("sword", "hand", "Меч", 3, [".s.", ".s.", ".s.", ".s.", "ggg", ".b."],
     {"s": "#dfe6f2", "g": "#e8b84a", "b": "#7a4a26"}, dx=-1)
_add("wand", "hand", "Волшебная палочка", 4, [".y.", "yyy", ".y.", ".k.", ".k.", ".k."], {"y": "#ffd34d", "k": "#3a2414"},
     dx=-1)
_add("balloon", "hand", "Воздушный шарик", None, [".rr.", "rWrr", "rrrr", ".rr.", "..k.", ".k..", "..k.", ".k.."],
     {"r": "#ff4f6a", "W": "#ffb3c0", "k": "#cfcfcf"}, dx=-1)
_add("icecream", "hand", "Мороженое", None, [".p.", "ppp", "yyy", ".y."], {"p": "#ff9fc0", "y": "#e0a050"}, dx=-1)
_add("fish", "hand", "Рыбка", None, ["b.bbb.", ".bbbkb", "b.bbb."], {"b": "#6fb8ff", "k": "#111111"})
_add("flag", "hand", "Флажок", 1, ["krrr", "krrr", "k...", "k...", "k..."], {"k": "#3a2414", "r": "#e5534b"})
_add("lollipop", "hand", "Леденец", None, ["ppp", "pwp", "ppp", ".k.", ".k."], {"p": "#ff6fa8", "w": "#ffffff", "k": "#dddddd"},
     dx=-1)
_add("coffee", "hand", "Кофе", 2, [".g.g.", "wwww.", "wbbww", "wwww."], {"g": "#cfcfcf", "w": "#ffffff", "b": "#6b3e1f"})
_add("phone", "hand", "Телефончик", None, ["kk", "cc", "cc", "kk"], {"k": "#222222", "c": "#6fb8ff"})
_add("bouquet", "hand", "Букет", 3, ["p.y", "rbp", ".g.", ".g."],
     {"p": "#ff6fa8", "y": "#ffd34d", "r": "#e5534b", "b": "#6fb8ff", "g": "#4f8a2e"}, dx=-1)
_add("pizza", "hand", "Пицца", 2, ["bbbb", "yryy", ".yr.", ".y.."], {"b": "#c98a3a", "y": "#ffd34d", "r": "#e5534b"}, dx=-1)
_add("saber", "hand", "Световой меч", 8, ["c", "c", "c", "c", "c", "s", "s"], {"c": "#39e6ff", "s": "#9aa0a8"})
_add("magnifier", "hand", "Лупа", 5, ["..kk.", ".k..k", ".k..k", "..kk.", ".k...", "k...."], {"k": "#3a3a3a"})
_add("trophy", "hand", "Кубок", 12, ["y...y", "yyyyy", ".yyy.", "..y..", ".yyy."], {"y": "#ffc94d"}, dx=-1)

# ---------- спина ----------
_add("angel", "back", "Крылья ангела", "days30",
     ["ww................ww", "www..............www", ".www............www.", "..ww............ww.."], {"w": "#ffffff"}, dy=-1)
_add("bat", "back", "Крылья летучей мыши", 4,
     ["k..................k", "kk................kk", "kkk..............kkk", "k.k..............k.k"], {"k": "#3a2a44"}, dy=-1)
_add("butterfly", "back", "Крылья бабочки", 3,
     ["pp................pp", "pyp..............pyp", ".pp..............pp.", "..bb............bb.."],
     {"p": "#ff6fa8", "y": "#ffd34d", "b": "#6fb8ff"}, dy=-1)
_add("dragon", "back", "Крылья дракона", 10,
     ["g..................g", "gg................gg", "gGg..............gGg", "g.g..............g.g"],
     {"g": "#4f9a4f", "G": "#8fd46a"}, dy=-1)
_add("cape", "back", "Плащ героя", 2,
     ["r............r", "r............r", "rr...........r", "rr...........r", ".rr..........r", ".rrr........rr",
      "..rrrrrrrrrrr."], {"r": "#d6332b"}, dy=1)
_add("jetpack", "back", "Реактивный ранец", 7, ["ss..............", "sss.............", "sss.............",
                                                ".o..............", ".y.............."],
     {"s": "#9aa0a8", "o": "#ff7a1a", "y": "#ffd34d"}, dy=1)
_add("backpack", "back", "Рюкзак", None, ["bbb.", "bbbb", "bybb", "bbbb"], {"b": "#4f8a2e", "y": "#ffd34d"}, dx=-7, dy=1)
_add("foxtail", "back", "Лисий хвост", 1, ["....o", "...oo", "..ooo", ".ooow", "oow.."], {"o": "#f08a24", "w": "#ffffff"},
     dx=-8, dy=3)
_add("deviltail", "back", "Хвостик чертёнка", 3, ["rr...", "rrr..", ".r...", "..rr.", "....r"], {"r": "#d6332b"},
     dx=-8, dy=3)

# ---------- узоры (плитка по телу) ----------
_add("stripes", "pattern", "Полоски", None, ["D", "."])
_add("tiger", "pattern", "Тигр", 2, ["D...D.", ".D...D", "D...D.", "......"])
_add("giraffe", "pattern", "Жираф", 3, ["DD....", "DD..D.", "....DD", ".D..DD"])
_add("dots", "pattern", "Горошек", None, ["L...", "....", "..L.", "...."])
_add("belly", "pattern", "Пузико", None, ["............", "............", "............", "....LLLL....",
                                           "...LLLLLL...", "...LLLLLL...", "....LLLL...."])
_add("checker", "pattern", "Шахматка", 1, ["D.", ".D"])
_add("camo", "pattern", "Камуфляж", 4, ["DD..LL..", "D..LLL.D", "..DD...D", "LL.DD.LL"])
_add("heartsp", "pattern", "Принт с сердечками", 2, [".p.p...", "ppppp..", ".ppp...", "..p....", "......."], {"p": "#ff6fa8"})
_add("shadow", "pattern", "Закат", None, ["L", "L", ".", ".", "D", "D", "D"])
_add("rainbow", "pattern", "Радуга", 6, ["r", "o", "y", "g", "b", "i", "v"],
     {"r": "#ef5350", "o": "#ff9f43", "y": "#ffd34d", "g": "#66d17a", "b": "#4fa8e8", "i": "#5c6bd6", "v": "#a66be0"})
_add("galaxy", "pattern", "Галактика", 9, ["pppppPpppppp", "ppwppppppPpp", "pppppppwpppp", "pPpppppppppw",
                                          "ppppwppPpppp", "pppppppppwpp", "wppPpppppppp"],
     {"p": "#2a1f5c", "P": "#5a3fb0", "w": "#ffffff"})
_add("zombie", "pattern", "Зомби", 7, ["............", ".gg.......k.", ".ggg.....kkk", "..g.......k.",
                                      "......ss....", "...gg.......", "..ggg......."], {"g": "#7fbf5a", "s": "#3a2a2a", "k": "#3a2a2a"})
_add("robot", "pattern", "Робот", 8, ["y..........y", "............", "............", "............",
                                     ".DDDDDDDDDD.", ".D.y.DD.y.D.", ".DDDDDDDDDD."], {"y": "#ffd34d"})
_add("lava", "pattern", "Лава", 11, ["kokkkkokkkkk", "kkookkkkookk", "okkkoookkkko", "kkkkkkkokkkk",
                                    "kookkkkkkook", "kkkookkookkk", "okkkkookkkko"], {"k": "#3a1a12", "o": "#ff7a1a"})

# ---------- ауры ----------
_add("a_sparkle", "aura", "Блёстки", None, aura={"shape": "rect", "colors": ["#ffd34d", "#ffffff", "#fff1a0"], "every": 0.35})
_add("a_hearts", "aura", "Сердечки", "pet10", aura={"shape": "heart", "colors": [], "every": 0.6})
_add("a_fire", "aura", "Огонь", 5, aura={"shape": "rect", "colors": ["#ff4a1a", "#ff9f43", "#ffd34d"], "every": 0.12})
_add("a_bubbles", "aura", "Пузырьки", None, aura={"shape": "ring", "colors": ["#9bd3ff", "#d6f0ff"], "every": 0.4})
_add("a_notes", "aura", "Ноты", 1, aura={"shape": "text", "text": "♪♫", "colors": ["#7ab8ff", "#b28cff", "#6be3a2"],
                                        "every": 0.6})
_add("a_snow", "aura", "Снегопад", 3, aura={"shape": "rect", "colors": ["#ffffff"], "every": 0.15, "fall": True})
_add("a_rainbow", "aura", "Радужный след", 8, aura={"shape": "rect", "colors": ["#ef5350", "#ff9f43", "#ffd34d", "#66d17a",
                                                                               "#4fa8e8", "#a66be0"], "every": 0.1})
_add("a_stars", "aura", "Звёздочки", 2, aura={"shape": "text", "text": "✦★", "colors": ["#ffd34d", "#fff1a0", "#9bd3ff"],
                                             "every": 0.45})
_add("a_money", "aura", "Денежки", 10, aura={"shape": "text", "text": "$", "colors": ["#66d17a", "#3fae5a"], "every": 0.4})
_add("a_leaves", "aura", "Листопад", 4, aura={"shape": "rect", "colors": ["#e8a33a", "#d9622b", "#9bd45a"], "every": 0.25,
                                             "fall": True})
_add("a_ghost", "aura", "Призрачная дымка", "ghost5", aura={"shape": "oval", "colors": ["#c9ccd6", "#9aa0b0"], "every": 0.2})
_add("a_zap", "aura", "Молнии", 12, aura={"shape": "text", "text": "ϟ", "colors": ["#ffe14a", "#9bd3ff"], "every": 0.3})


# ---------- сезонное (открыто всегда — праздник можно устроить в любой день) ----------
_add("pumpkinhat", "head", "Тыква на голову", rows=["....gg....", ".oooOoooo.", "ooyOooOyoo", "oOooyyoOoo", ".oooOoooo."],
     pal={"o": "#f08a24", "O": "#c96a12", "y": "#ffd34d", "g": "#4f8a2e"}, dy=1, season="halloween")
_add("ghostsuit", "pattern", "Костюм привидения", rows=["w"], pal={"w": "#eef0f6"}, season="halloween")
_add("candybucket", "hand", "Ведёрко для сладостей", rows=[".kkk.", "k...k", "ooooo", "oyoyo", "ooooo"],
     pal={"o": "#f08a24", "y": "#ffd34d", "k": "#3a2414"}, dx=-1, season="halloween")
_add("a_pumpkin", "aura", "Тыквенная аура", aura={"shape": "rect", "colors": ["#8a4fd8", "#f08a24", "#ffb347"], "every": 0.25},
     season="halloween")
_add("antlers", "head", "Оленьи рога", rows=["b.b......b.b", ".bb......bb.", "..b......b.."], pal={"b": "#8b5a2b"},
     season="newyear")
_add("elf", "head", "Колпак эльфа", rows=["......ggy", "..ggggg..", "rrrrrrrr."], pal={"g": "#3fae5a", "y": "#ffd34d", "r": "#e5534b"},
     season="newyear")
_add("garland", "neck", "Гирлянда", rows=["kkkkkkkkkkkk", "r..y..b..g.."],
     pal={"k": "#2f5f2a", "r": "#ff5a7a", "y": "#ffd34d", "b": "#6fb8ff", "g": "#8fcf6a"}, season="newyear")
_add("gift", "hand", "Подарок", rows=["y...y", ".y.y.", "rryrr", "yyyyy", "rryrr"], pal={"r": "#e5534b", "y": "#ffd34d"},
     dx=-1, season="newyear")
_add("a_festive", "aura", "Праздничные огоньки", aura={"shape": "text", "text": "✦", "colors": ["#ff5a7a", "#ffd34d", "#6fb8ff",
                                                                                         "#8fcf6a"], "every": 0.3},
     season="newyear")
_add("heartballoon", "hand", "Шарик-сердце", rows=["rr.rr", "rrrrr", ".rrr.", "..r..", "..k..", ".k...", "..k..", ".k..."],
     pal={"r": "#ff4f6a", "k": "#cfcfcf"}, dx=-1, season="valentine")
_add("cupid", "back", "Крылья купидона", rows=["pp................pp", "ppp..............ppp", ".ppp............ppp.",
                                               "..pp............pp.."], pal={"p": "#ffb3cf"}, dy=-1, season="valentine")
_add("easteregg", "hand", "Пасхальное яйцо", rows=[".ppp.", "pyyyp", "pbbbp", "pyyyp", ".ppp."],
     pal={"p": "#ff9fc0", "y": "#ffd34d", "b": "#6fb8ff"}, dx=-1, season="spring")
_add("a_petals", "aura", "Лепестки сакуры", aura={"shape": "rect", "colors": ["#ffb3cf", "#ff9fc0", "#ffffff"], "every": 0.25,
                                                  "fall": True}, season="spring")
_add("watermelon", "hand", "Арбуз", rows=["ggggg", "wwwww", "rkrkr", ".rrr.", "..r.."],
     pal={"g": "#3fae5a", "w": "#e8f5d0", "r": "#ff5a6a", "k": "#1a1a1a"}, dx=-1, season="summer")
_add("a_sun", "aura", "Солнечные зайчики", aura={"shape": "text", "text": "✦", "colors": ["#ffd34d", "#fff1a0", "#ffb347"],
                                                 "every": 0.35}, season="summer")
# подходящее из обычного гардероба тоже показываем в сезонном
for _k, _s in {"witch": "halloween", "horns": "halloween", "bat": "halloween", "deviltail": "halloween",
               "a_ghost": "halloween", "scarf": "newyear", "a_snow": "newyear", "hearts": "valentine",
               "heartsp": "valentine", "a_hearts": "valentine", "bow": "valentine", "bunny": "spring", "wreath": "spring",
               "flower": "spring", "butterfly": "spring", "sprout": "spring", "straw": "summer", "lei": "summer",
               "icecream": "summer", "bucket": "summer"}.items():
    ITEMS[_k]["season"] = _s


# праздничные украшения рядом с Клодиком (пиксель-арт, буквы — цвета, «*» — мигающие огоньки)
DECOR = {
    "halloween": (["....gg......", "...gg.......", "..oOooOooO..", ".ooOooOooOo.", "oOyyOooOyyOo", "oOooOooOooOo",
                   "oOoyyyyyyoOo", "oOooyOOyooOo", ".ooOooOooOo.", "..oOooOooO.."],
                  {"g": "#4f8a2e", "o": "#f08a24", "O": "#c96a12", "y": "*"}),
    "newyear": (["......S......", ".....SSS.....", "......G......", ".....GGG.....", "....G*GGG....", "...GGGG*GG...",
                 "....GGGGG....", "...G*GGGGG...", "..GGGGG*GGG..", "...GGGGGGG...", "..GG*GGGG*G..", ".GGGGGG*GGGG.",
                 "GGG*GGGGGG*GG", ".....TTT.....", ".....TTT....."],
                {"S": "#ffd34d", "G": "#2f8f3a", "T": "#7a4a26"}),
    "valentine": ([".RRR...RRR.", "RRWRR.RRRRR", "RWRRRRR*RRR", "RRRRRRRRRRR", "RRRR*RRRRRR", ".RRRRRRR*R.", "..RRRRRRR..",
                   "...RRRRR...", "....RRR....", ".....R....."],
                  {"R": "#ff4f6a", "W": "#ffb3c0"}),
    "spring": (["..p...y..", ".ppp.yyy.", "..p*..y*.", "...g..g..", "....gg...", "..g.g.g..", "...ggg...", ".BBBBBBB.",
                "..BBBBB..", "..BBBBB..", "...BBB..."],
               {"p": "#ff6fa8", "y": "#ffd34d", "g": "#4f9a4f", "B": "#c96a3a"}),
    "summer": (["....y....", ".y..y..y.", "..yyyyy..", ".yYYYYYy.", "yyY*YY*Yy", ".yYYYYYy.", "..yyyyy..", ".y..y..y.",
                "....y...."],
               {"y": "#ffd34d", "Y": "#ffb347"}),
}
DECOR_LIGHTS = {"halloween": ("#ffd34d", "#ff9a2e", "#ffe680"), "newyear": ("#ff5a7a", "#ffd34d", "#6fb8ff", "#8fcf6a"),
                "valentine": ("#ffffff", "#ffd1dc", "#ff9fc0"), "spring": ("#fff1a0", "#ffffff", "#ffd34d"),
                "summer": ("#ffffff", "#fff1a0", "#ff9f43")}
# что можно поставить рядом с Клодиком (вкладка «Сезонное» на ПК и телефоне): auto — по календарю, none — ничего
DECOR_NAMES = {"halloween": "Тыква", "newyear": "Ёлка", "valentine": "Сердце", "spring": "Цветок в горшке", "summer": "Солнце"}


def shade(color, t):
    """t < 0 — темнее, t > 0 — светлее."""
    r, g, b = (int(color[i:i + 2], 16) for i in (1, 3, 5))
    if t < 0:
        r, g, b = (round(c * (1 + t)) for c in (r, g, b))
    else:
        r, g, b = (round(c + (255 - c) * t) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


def _resolve(ch, pal, body, eye):
    if ch == "B":
        return body
    if ch == "D":
        return shade(body, -0.28)
    if ch == "L":
        return shade(body, 0.32)
    if ch == "E":
        return eye
    return pal.get(ch)


def _stamp(px, rows, pal, x0, y0, body, eye):
    """Строки-картинку — клетками; одинаковые соседние клетки в строке ставятся одним куском."""
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            ch = row[c]
            if ch == ".":
                c += 1
                continue
            end = c + 1
            while end < len(row) and row[end] == ch:
                end += 1
            color = _resolve(ch, pal, body, eye)
            if color:
                px(x0 + c, y0 + r, x0 + end, y0 + r + 1, color)
            c = end


def _row_fill(px, x_from, x_to, y, ch, pal, body, eye):
    if x_to > x_from:
        color = _resolve(ch, pal, body, eye)
        if color:
            px(x_from, y, x_to, y + 1, color)


def draw(px, items, phase, left, right, top, bottom, ey, look, body, eye, hands_free=True):
    """phase: back — до тела, pattern — по телу, front — поверх глаз и рта."""
    mx = (left + right) // 2
    worn = [ITEMS[k] for k in items if k in ITEMS]
    if phase == "back":
        for it in worn:
            if it["slot"] == "back":
                w = len(it["rows"][0])
                _stamp(px, it["rows"], it["pal"], mx - w // 2 + it["dx"], top + it["dy"], body, eye)
        return
    if phase == "pattern":
        for it in worn:
            if it["slot"] != "pattern":
                continue
            rows = it["rows"]
            h, w = len(rows), len(rows[0])
            for y in range(top, bottom):
                _stamp(px, ["".join(rows[(y - top) % h][(x - left) % w] for x in range(left, right))], it["pal"],
                       left, y, body, eye)
        return
    order = {"face": 0, "neck": 1, "head": 2, "hand": 3}
    for it in sorted((i for i in worn if i["slot"] in order), key=lambda i: order[i["slot"]]):
        slot, pal = it["slot"], it["pal"]
        if slot == "face":
            lcx, rcx, y0 = left + 3 + look, right - 4 + look, ey - 1 + it["dy"]
            _stamp(px, it["left"], pal, lcx - 2, y0, body, eye)
            _stamp(px, it["right"], pal, rcx - 2, y0, body, eye)
            for row, ch in it["bridge"]:
                _row_fill(px, lcx + 3, rcx - 2, y0 + row, ch, pal, body, eye)
            for row, ch in it["edge"]:
                _row_fill(px, left, lcx - 2, y0 + row, ch, pal, body, eye)
                _row_fill(px, rcx + 3, right, y0 + row, ch, pal, body, eye)
        elif slot == "neck":
            w = len(it["rows"][0])
            _stamp(px, it["rows"], pal, mx - w // 2 + it["dx"], top + 5 + it["dy"], body, eye)
        elif slot == "head":
            w, h = len(it["rows"][0]), len(it["rows"])
            _stamp(px, it["rows"], pal, mx - w // 2 + it["dx"], top - h + it["dy"], body, eye)
        elif slot == "hand" and hands_free:
            h = len(it["rows"])
            _stamp(px, it["rows"], pal, right + 1 + it["dx"], top + 5 - h + it["dy"], body, eye)


GLOW = 3  # на сколько клеток свечение ауры выходит за силуэт


def aura_of(keys):
    """Аура среди надетого (или None)."""
    return next((ITEMS[k]["aura"] for k in keys if k in ITEMS and ITEMS[k]["aura"]), None)


def glow(px, cells, keys, phase, bounds):
    """Свечение ауры вокруг силуэта (cells — занятые клетки): три кольца, внутреннее сплошное,
    среднее — «рябью», внешнее — редкими искрами. phase 0..3 двигает рябь и искры, у многоцветных аур
    ещё и цвета бегут по кольцам. bounds = (x0, y0, x1, y1) — куда можно рисовать."""
    aura = aura_of(keys)
    if aura is None or not cells:
        return
    cols = aura["colors"] or ["#ff6fa8", "#ff9fc0"]
    n = len(cols)
    x0, y0, x1, y1 = bounds
    # щели в одну клетку (между ножками, под рукой) — часть силуэта: иначе свечение заливает их и Клодик
    # превращается в светящийся комок
    gaps = set()
    xs = [x for x, _ in cells]
    ys = [y for _, y in cells]
    for x in range(min(xs), max(xs) + 1):
        for y in range(min(ys), max(ys) + 1):
            if (x, y) not in cells and (((x - 1, y) in cells and (x + 1, y) in cells) or
                                        ((x, y - 1) in cells and (x, y + 1) in cells)):
                gaps.add((x, y))
    taken = set(cells) | gaps
    ring = set(taken)
    for k in range(GLOW):
        ring = {(x + dx, y + dy) for x, y in ring for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))} - taken
        taken |= ring
        # мало цветов — внутри светлый (последний), снаружи насыщенный; много — радуга бежит по кругу
        color = cols[(k + phase) % n] if n >= 4 else cols[max(0, n - 1 - k)]
        for x, y in sorted(ring):
            if not (x0 <= x < x1 and y0 <= y < y1):
                continue
            if k == 1 and (x + y + phase) % 2:
                continue
            if k == 2 and (x + 2 * y + phase) % 4:
                continue
            px(x, y, x + 1, y + 1, color)


def for_ui():
    """Всё для окна настроек (без вещей, которые надеваются сами)."""
    return {"slots": [{"key": k, "name": n, "icon": i} for k, n, i in SLOTS],
            "seasons": [{"key": k, "name": n, "icon": i} for k, n, i in SEASONS],
            "items": [it for it in ITEMS.values() if not it["auto"]]}


def _check():
    for it in ITEMS.values():
        for part in ("rows", "left", "right"):
            rows = [r for r in it[part] if r]
            widths = {len(r) for r in rows}
            assert len(widths) <= 1, (it["key"], part, widths)
            if part != "rows":
                assert widths <= {5}, (it["key"], part, widths)
            for r in rows:
                for ch in r:
                    assert ch in ".BDLE" or ch in it["pal"], (it["key"], ch)
        assert it["slot"] in SLOT_KEYS, it["key"]
        assert (it["aura"] is not None) == (it["slot"] == "aura"), it["key"]
        assert it["season"] in (None, *[s for s, _, _ in SEASONS]), it["key"]


_check()
