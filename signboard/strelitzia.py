"""ストレチア（極楽鳥花）版。ブーゲンビリア版と同じ構成（白地・蓮マーク・店名）。

signs_strelitzia.html … Canva取り込み用
png/st_*.png          … フォント込みの完成画像（Canva不要で使える）
"""
import asyncio
import math
import pathlib

from build import BRAND, H, SUB, W, fit, mark, page, vtext

HERE = pathlib.Path(__file__).parent
LOCAL_FONTS = pathlib.Path("/tmp/claude-0/fonts/st")  # プレビュー描画専用
NAME = "暮しと供養のステーション"
FONTS = ("https://fonts.googleapis.com/css2?family=Zen+Old+Mincho:wght@700&family=Yuji+Syuku"
         "&family=Zen+Kaku+Gothic+New:wght@500&display=swap")
INK = "#33302B"

ORANGE = ["#F07F12", "#F7A21B", "#E96A10"]
BLUE = "#3556A6"
GREEN = "#4F7A45"
GREEN_D = "#3C6238"


def petal(L, w, ang, fill, ox=0, oy=0):
    """先の尖った花びら。根元を(ox,oy)に置き、angで回す。"""
    d = (f"M0 0 C{L*.25:.0f} {-w:.0f} {L*.72:.0f} {-w*.75:.0f} {L:.0f} 0 "
         f"C{L*.72:.0f} {w*.75:.0f} {L*.25:.0f} {w:.0f} 0 0 Z")
    return f'<path transform="translate({ox} {oy}) rotate({ang})" d="{d}" fill="{fill}"/>'


def flower(x, y, s, rot):
    """ストレチアの花。舟形の苞から橙の萼片3枚と青い花弁が伸びる。(x,y)は茎の先端。"""
    g = []
    # 橙の萼片（扇状に3枚）
    for i, a in enumerate((-78, -52, -26)):
        g.append(petal(150, 22, a, ORANGE[i], 0, 0))
    # 青い花弁（手前に1枚、細く長く）
    g.append(petal(170, 20, -2, BLUE, 6, 8))
    # 舟形の苞（緑、縁は赤茶）
    g.append('<path d="M-70 36 C-52 -12 44 -34 110 -8 C72 26 -6 52 -70 36 Z" fill="#5C8A4C" '
             'stroke="#8C3B22" stroke-width="3" stroke-linejoin="round"/>')
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">{"".join(g)}</g>')


def leaf(x, y, L, wd, rot, fill=GREEN):
    """櫂（かい）形の大きな葉。中央に葉脈。"""
    d = (f"M0 0 C{wd*.7:.0f} {-L*.18:.0f} {wd:.0f} {-L*.6:.0f} 0 {-L:.0f} "
         f"C{-wd:.0f} {-L*.6:.0f} {-wd*.7:.0f} {-L*.18:.0f} 0 0 Z")
    return (f'<g transform="translate({x} {y}) rotate({rot})"><path d="{d}" fill="{fill}"/>'
            f'<path d="M0 -6 L0 {-L*.94:.0f}" stroke="#2F5030" stroke-width="3" opacity=".55"/></g>')


def stem(x0, y0, x1, y1, bend):
    return (f'<path d="M{x0} {y0} C{x0} {y0-(y0-y1)*.5:.0f} {x1-bend} {y1+(y0-y1)*.3:.0f} {x1} {y1}" '
            f'fill="none" stroke="{GREEN_D}" stroke-width="7" stroke-linecap="round"/>')


def cluster_h(w, h):
    """左下から立ち上がる群れ。奥に葉、手前に花。"""
    parts = [
        leaf(70, h + 10, 470, 70, -18, GREEN_D), leaf(250, h + 10, 430, 66, 14, GREEN),
        leaf(160, h + 10, 520, 74, -2, GREEN), leaf(20, h + 10, 300, 56, -38, GREEN),
        stem(150, h + 10, 330, 190, 60), stem(90, h + 10, 210, 275, -30), stem(200, h + 10, 470, 330, 40),
        flower(330, 190, 0.95, -6), flower(210, 275, 0.8, -20), flower(470, 330, 0.7, 8),
    ]
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">{"".join(parts)}</svg>'


def cluster_v(w, h):
    """袖看板用：下端から立ち上がる。"""
    parts = [
        leaf(150, h + 10, 400, 72, -14, GREEN_D), leaf(470, h + 10, 380, 70, 16, GREEN_D),
        leaf(300, h + 10, 470, 78, 0, GREEN), leaf(60, h + 10, 300, 56, -36, GREEN),
        leaf(560, h + 10, 300, 56, 34, GREEN),
        stem(190, h + 10, 190, 200, 20), stem(410, h + 10, 430, 300, -20),
        flower(190, 200, 0.85, -10), flower(430, 300, 0.75, 8),
    ]
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">{"".join(parts)}</svg>'


def hz(font, ls, ink=INK):
    fs = fit(NAME, 1480, ls, 160)
    return f'''<div style="position:absolute;inset:0;background:#FFFFFF"></div>
<div style="position:absolute;left:0;top:0">{cluster_h(760, H)}</div>
<div style="position:absolute;left:780px;top:0;bottom:0;width:1560px;display:flex;flex-direction:column;justify-content:center">
  <div style="font:{font.format(fs=fs)};letter-spacing:{ls}em;color:{ink};line-height:1.2;white-space:nowrap">{NAME}</div>
  <div style="margin-top:36px;display:flex;align-items:center;gap:28px">
    {mark(BRAND, 84)}
    <span style="font:500 46px 'Zen Kaku Gothic New',sans-serif;letter-spacing:.16em;color:#6E665C">{SUB}</span>
  </div>
</div>'''


def vt(font, ink=INK):
    return f'''<div style="position:absolute;inset:0;background:#FFFFFF"></div>
<div style="position:absolute;left:215px;top:40px">{mark(BRAND, 170)}</div>
<div style="position:absolute;left:0;right:0;top:260px;height:1420px;display:flex;justify-content:center">
  {vtext(NAME, int(1340/len(NAME)/1.08), font, ink)}
</div>
<div style="position:absolute;left:0;bottom:0">{cluster_v(H, 600)}</div>'''


MINCHO = "700 {fs}px 'Zen Old Mincho',serif"
BRUSH = "400 {fs}px 'Yuji Syuku',serif"
PAGES = [
    ("st_h_mincho", "ストレチア・明朝", hz(MINCHO, .12), W, H),
    ("st_h_brush", "ストレチア・毛筆", hz(BRUSH, .08), W, H),
    ("st_v_mincho", "袖看板 ストレチア・明朝", vt(MINCHO), H, W),
    ("st_v_brush", "袖看板 ストレチア・毛筆", vt(BRUSH), H, W),
]


async def render():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = await b.new_page()
        for key, lbl, body, w, h in PAGES:
            await pg.set_viewport_size({"width": w, "height": h})
            tmp = LOCAL_FONTS / "page.html"
            tmp.write_text(f'<html><head><meta charset="utf-8"><link rel="stylesheet" href="local.css">'
                           f'<style>body{{margin:0}}</style></head><body>{page(lbl, body, w, h, False)}</body></html>',
                           encoding="utf-8")
            await pg.goto(tmp.as_uri())
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(800)
            await pg.screenshot(path=str(HERE / "png" / f"{key}.png"))
        await b.close()


if __name__ == "__main__":
    doc = (f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>看板 ストレチア版</title>'
           f'<link rel="stylesheet" href="{FONTS}"><style>body{{margin:0;background:#888}}</style></head><body>'
           + "".join(page(lbl, body, w, h) for _, lbl, body, w, h in PAGES) + "</body></html>")
    (HERE / "signs_strelitzia.html").write_text(doc, encoding="utf-8")
    asyncio.run(render())
