"""Иконка Clawd для ПК: clawd.ico (16…256 px) и clawd_icon.png (256 px, для окна настроек).

Клодик нарисован по клеткам, как на экране; на больших размерах — на пиксельной плашке с углами «лесенкой»,
на 16–24 px — без плашки, чтобы не превратиться в кашу. Нужен pillow:  py make_icon.py
"""

from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
BODY, EYE = "#d97757", "#1a1a1a"
TILE, BORDER, SHADOW = "#211b17", "#e0855f", "#0a0807"


def sprite():
    """Клетки Клодика 18×13 в позе «машет» — {(x, y): цвет}."""
    cells = {}

    def px(x0, y0, x1, y1, color):
        for x in range(x0, x1):
            for y in range(y0, y1):
                cells[(x, y)] = color

    left, right, top, bottom = 3, 15, 3, 10
    for c in (left + 1, left + 3, right - 4, right - 2):
        px(c, bottom, c + 1, bottom + 2, BODY)
    px(left - 2, top + 3, left, top + 5, BODY)  # левая рука
    px(right + 1, top - 1, right + 2, top + 3, BODY)  # правая машет
    px(right, top + 2, right + 1, top + 3, BODY)
    px(left, top, right, bottom, BODY)
    for cx in (left + 3, right - 4):
        px(cx, top + 2, cx + 1, top + 4, EYE)
    return cells


def stepped(d, x0, y0, x1, y1, s, fill):
    """Прямоугольник с углами «лесенкой» (ступенька s px)."""
    d.rectangle((x0 + 2 * s, y0, x1 - 2 * s, y1), fill=fill)
    d.rectangle((x0, y0 + 2 * s, x1, y1 - 2 * s), fill=fill)
    d.rectangle((x0 + s, y0 + s, x1 - s, y1 - s), fill=fill)


def render(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cells = sprite()
    xs = [x for x, _ in cells]
    ys = [y for _, y in cells]
    gw, gh = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
    if size >= 32:
        s = max(1, size // 32)  # ступенька и тень
        stepped(d, 2 * s, 2 * s, size - 1, size - 1, s, SHADOW)
        stepped(d, 0, 0, size - 1 - 2 * s, size - 1 - 2 * s, s, BORDER)
        b = max(1, size // 24)
        stepped(d, b, b, size - 1 - 2 * s - b, size - 1 - 2 * s - b, s, TILE)
        inner = size - 2 * s - 2 * b
        cell = max(1, int(inner * 0.78) // gw)
        ox = b + (inner - gw * cell) // 2
        oy = b + (inner - gh * cell) // 2
    else:
        cell = max(1, size // gw)
        ox = (size - gw * cell) // 2
        oy = (size - gh * cell) // 2
    for (x, y), color in cells.items():
        X, Y = ox + (x - min(xs)) * cell, oy + (y - min(ys)) * cell
        d.rectangle((X, Y, X + cell - 1, Y + cell - 1), fill=color)
    return img


def main():
    sizes = [16, 24, 32, 48, 64, 128, 256]
    imgs = [render(s) for s in sizes]
    imgs[-1].save(HERE / "clawd.ico", format="ICO", sizes=[(s, s) for s in sizes], append_images=imgs[:-1])
    imgs[-1].save(HERE / "clawd_icon.png")
    print("clawd.ico, clawd_icon.png")


if __name__ == "__main__":
    main()
