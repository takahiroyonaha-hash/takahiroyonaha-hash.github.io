"""Affinity向けベクター版の看板（名称：暮しと供養のステーション）。

出力: signboard/affinity/*.svg  … 文字は全てアウトライン化済み（フォント不要）。Affinity Designerで開ける。
      signboard/affinity/*.pdf  … 同じ内容のベクターPDF
      signboard/affinity/png/*.png … 確認用プレビュー

SVGの寸法は実寸（横長 3600×900mm / 袖看板 900×3600mm）。レイヤー相当のグループに id を付けてある。
"""
import asyncio
import pathlib
import re

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

from build import BRAND, _MARK, bougainvillea

HERE = pathlib.Path(__file__).parent
OUT = HERE / "affinity"
TTF = pathlib.Path("/tmp/claude-0/ttf")  # Google Fonts（OFL）から取得した TTF

NAME = "暮しと供養のステーション"
SUB = "法事・法要・納骨・ご供養のご相談"
W, H = 2400, 600
MM = 1.5  # 1単位 = 1.5mm

INK = "#2E2630"
SOFT = "#6B5F6E"
CREAM = "#F2ECDF"

_fonts = {}


def font(name):
    if name not in _fonts:
        f = TTFont(TTF / name)
        _fonts[name] = (f, f.getGlyphSet(), f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm)
    return _fonts[name]


MINCHO = "ZenOldMincho-Bold.ttf"
GOTHIC = "ZenKakuGothicNew-Medium.ttf"
GOTHIC_B = "ZenKakuGothicNew-Bold.ttf"


def _glyph(fname, ch):
    f, gs, cmap, hmtx, upm = font(fname)
    g = cmap[ord(ch)]
    return gs, g, hmtx[g][0], upm


def text_width(text, fname, size, ls=0.0):
    w = 0
    for ch in text:
        _, _, aw, upm = _glyph(fname, ch)
        w += aw * size / upm + ls * size
    return w - ls * size


def fit_size(text, fname, avail, ls, cap):
    """avail幅に収まる最大のフォントサイズ。"""
    return min(cap, avail / text_width(text, fname, 1.0, ls))


def text_path(text, fname, size, x, y, fill, ls=0.0, anchor="start", pid=None):
    """横書き。(x,y)は基準線の左端（anchor=middleなら中央）。アウトライン化した1本のパス。"""
    if anchor == "middle":
        x -= text_width(text, fname, size, ls) / 2
    d = []
    cx = x
    for ch in text:
        gs, g, aw, upm = _glyph(fname, ch)
        s = size / upm
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, cx, y)))
        d.append(pen.getCommands())
        cx += aw * s + ls * size
    i = f' id="{pid}"' if pid else ""
    return f'<path{i} d="{"".join(d)}" fill="{fill}"/>'


def vtext_path(text, fname, size, cx, y0, fill, adv=1.1, pid=None):
    """縦書き（上から下）。ーは90°回転、小さい仮名は右上へ寄せる。"""
    small = "ァィゥェォッャュョ"
    d = []
    for i, ch in enumerate(text):
        gs, g, aw, upm = _glyph(fname, ch)
        s = size / upm
        cy = y0 + size * adv * (i + .5)
        tx, ty = cx - aw * s / 2, cy + .38 * size
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
        if ch == "ー":
            m = (0, s, s, 0, cx - ty + cy, cy + tx - cx)
        else:
            if ch in small:
                tx += .12 * size
                ty -= .12 * size
            m = (s, 0, 0, -s, tx, ty)
        gs[g].draw(TransformPen(pen, m))
        d.append(pen.getCommands())
    i = f' id="{pid}"' if pid else ""
    return f'<path{i} d="{"".join(d)}" fill="{fill}"/>'


def lotus(x, y, w, fill=BRAND, pid="lotus-mark"):
    """TAKUSHO GROUPロゴの蓮マーク（トレース）。左上(x,y)、幅w。"""
    s = w / 1656
    return f'<g id="{pid}" transform="translate({x} {y}) scale({s:.5f})" fill="{fill}">{_MARK}</g>'


def lotus_h(w):
    return w * 1184 / 1656


def kasuri_band(y, h, color, pid):
    """琉球絣の十字柄の帯（図形のみ）。"""
    r = []
    for i in range(W // 96 + 1):
        x = i * 96
        cy = y + h / 2
        r.append(f"M{x+44} {cy-18}h8v36h-8zM{x+30} {cy-4}h36v8h-36z")
        r.append(f"M{x+4} {cy-3}h10v6h-10zM{x+82} {cy-3}h10v6h-10z")
    return f'<path id="{pid}" d="{"".join(r)}" fill="{color}" opacity=".95"/>'


def bougain(w, h, branches, seed):
    svg = bougainvillea(w, h, branches, seed)
    return re.sub(r"^<svg[^>]*>|</svg>$", "", svg)


def doc(title, w, h, layers):
    body = "".join(f'<g id="{n}">{c}</g>' for n, c in layers)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w*MM:g}mm" height="{h*MM:g}mm" '
            f'viewBox="0 0 {w} {h}"><title>{title}</title>{body}</svg>')


def rect(x, y, w, h, fill, rx=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>'


# ---- 横長 -----------------------------------------------------------------

def h1():  # 蓮マークを大きく（ロゴ主役）
    fs = fit_size(NAME, MINCHO, W - 760 - 130, .1, 140)
    bg = rect(0, 0, W, H, "#FFFFFF") + rect(0, H - 14, W, 14, BRAND)
    mk = lotus(150, (H - 14 - lotus_h(440)) / 2, 440)
    nx = 760
    tx = (text_path(NAME, MINCHO, fs, nx, 322, INK, .1, pid="shop-name")
          + rect(nx, 392, 90, 3, BRAND)
          + text_path(SUB, GOTHIC, 46, nx + 120, 408, SOFT, .16, pid="sub-copy"))
    return doc("看板 H1 蓮マーク", W, H, [("background", bg), ("logo", mk), ("text", tx)])


def h2():  # 路線図（ステーション）
    bg = rect(0, 0, W, H, "#FFFFFF")
    mk = lotus(140, (H - lotus_h(330)) / 2, 330)
    nx = 560
    name = text_path(NAME, MINCHO, fit_size(NAME, MINCHO, W - nx - 130, .1, 128), nx, 232, INK, .1, pid="shop-name")
    xs = [610 + i * 400 for i in range(5)]
    labels = ["法事", "法要", "納骨", "ご供養", "ご相談"]
    route = f'<path d="M{xs[0]} 372H{xs[-1]}" stroke="{BRAND}" stroke-width="8" stroke-linecap="round" fill="none"/>'
    nodes = ""
    for i, x in enumerate(xs):
        if i == len(xs) - 1:
            nodes += (f'<circle cx="{x}" cy="372" r="30" fill="#FFFFFF" stroke="{BRAND}" stroke-width="7"/>'
                      f'<circle cx="{x}" cy="372" r="14" fill="{BRAND}"/>')
        else:
            nodes += f'<circle cx="{x}" cy="372" r="19" fill="#FFFFFF" stroke="{BRAND}" stroke-width="8"/>'
    lab = "".join(text_path(t, GOTHIC_B, 44, x, 470, INK, .1, "middle", pid=f"station-{i+1}")
                  for i, (t, x) in enumerate(zip(labels, xs)))
    return doc("看板 H2 路線図", W, H, [("background", bg), ("logo", mk), ("route", route + nodes),
                                       ("text", name + lab)])


def h3():  # 琉球絣（藍）
    bg = rect(0, 0, W, H, "#1F3550")
    bands = kasuri_band(0, 64, CREAM, "kasuri-top") + kasuri_band(H - 64, 64, CREAM, "kasuri-bottom")
    mk = lotus(150, (H - lotus_h(380)) / 2, 380, CREAM)
    nx = 700
    tx = (text_path(NAME, MINCHO, fit_size(NAME, MINCHO, W - nx - 150, .1, 128), nx, 310, CREAM, .1, pid="shop-name")
          + text_path(SUB, GOTHIC, 44, nx, 410, "#C9D2DC", .2, pid="sub-copy"))
    return doc("看板 H3 琉球絣", W, H, [("background", bg), ("pattern", bands), ("logo", mk), ("text", tx)])


def h4():  # ブーゲンビリア（再構築）
    bg = rect(0, 0, W, H, "#FFFFFF")
    fl = bougain(760, H, [
        (((-20, 40), (220, 10), (420, 120), (560, 60)), 7, 46),
        (((-20, 60), (120, 200), (160, 380), (120, 560)), 7, 44),
        (((60, 120), (260, 180), (330, 330), (300, 470)), 5, 38),
    ], 1)
    nx = 820
    tx = (text_path(NAME, MINCHO, fit_size(NAME, MINCHO, W - nx - 130, .1, 134), nx, 318, INK, .1, pid="shop-name")
          + text_path(SUB, GOTHIC, 46, nx + 130, 408, SOFT, .16, pid="sub-copy"))
    mk = lotus(nx, 370, 100)
    return doc("看板 H4 ブーゲンビリア", W, H, [("background", bg), ("flowers", fl), ("logo", mk), ("text", tx)])


# ---- 袖看板（縦） ---------------------------------------------------------

def v1():  # 蓮マーク
    bg = rect(0, 0, H, W, "#FFFFFF") + rect(0, W - 14, H, 14, BRAND)
    mk = lotus(120, 150, 360)
    tx = vtext_path(NAME, MINCHO, 118, 300, 560, INK, pid="shop-name")
    return doc("袖看板 V1 蓮マーク", H, W, [("background", bg), ("logo", mk), ("text", tx)])


def v4():  # ブーゲンビリア
    bg = rect(0, 0, H, W, "#FFFFFF")
    fl = bougain(H, 560, [
        (((-20, 30), (200, 0), (420, 90), (620, 40)), 7, 42),
        (((-20, 50), (100, 180), (140, 330), (90, 520)), 5, 40),
        (((620, 60), (500, 180), (470, 330), (520, 480)), 5, 40),
    ], 3)
    tx = vtext_path(NAME, MINCHO, 114, 300, 640, INK, pid="shop-name")
    mk = lotus(200, 2210, 200)
    return doc("袖看板 V4 ブーゲンビリア", H, W, [("background", bg), ("flowers", fl), ("logo", mk), ("text", tx)])


DESIGNS = [
    ("h1_lotus", h1, W, H), ("h2_route", h2, W, H), ("h3_kasuri", h3, W, H), ("h4_bougainvillea", h4, W, H),
    ("v1_lotus", v1, H, W), ("v4_bougainvillea", v4, H, W),
]


async def render(files):
    from playwright.async_api import async_playwright
    (OUT / "png").mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = await b.new_page()
        for key, svg, w, h in files:
            await pg.set_viewport_size({"width": w, "height": h})
            px_svg = svg.replace('width="%gmm" height="%gmm"' % (w * MM, h * MM), 'width="%d" height="%d"' % (w, h))
            await pg.set_content('<html><body style="margin:0">' + px_svg + '</body></html>')
            await pg.screenshot(path=str(OUT / "png" / f"{key}.png"))
            await pg.set_content(f'<html><head><style>@page{{size:{w*MM:g}mm {h*MM:g}mm;margin:0}}'
                                 f'body{{margin:0}}svg{{display:block}}</style></head><body>{svg}</body></html>')
            await pg.pdf(path=str(OUT / f"{key}.pdf"), width=f"{w*MM:g}mm", height=f"{h*MM:g}mm",
                         print_background=True, page_ranges="1")
        await b.close()


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    files = []
    for key, fn, w, h in DESIGNS:
        svg = fn()
        (OUT / f"{key}.svg").write_text(svg, encoding="utf-8")
        files.append((key, svg, w, h))
    asyncio.run(render(files))
