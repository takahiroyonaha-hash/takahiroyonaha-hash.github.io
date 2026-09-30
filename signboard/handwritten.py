"""ブーゲンビリア版 × 手書き風文字 × 白背景。signs_handwritten.html と png/hw_*.png を書き出す。"""
import asyncio
import pathlib

from build import BRAND, H, SUB, W, bougainvillea, fit, mark, page, vtext

HERE = pathlib.Path(__file__).parent
LOCAL_FONTS = pathlib.Path("/tmp/claude-0/fonts/hw")  # プレビュー描画専用
NAME = "暮しと供養のステーション"
FONTS = ("https://fonts.googleapis.com/css2?family=Klee+One:wght@600&family=Zen+Kurenaido"
         "&family=Yuji+Syuku&family=Yomogi&display=swap")

# (キー, ラベル, 書体, 字間)
HANDS = [
    ("klee", "教科書体ペン（Klee One）", "600 {fs}px 'Klee One',serif", .10),
    ("kurenaido", "筆ペン（Zen Kurenaido）", "400 {fs}px 'Zen Kurenaido',sans-serif", .10),
    ("syuku", "毛筆（Yuji Syuku）", "400 {fs}px 'Yuji Syuku',serif", .08),
    ("yomogi", "ゆるい手書き（Yomogi）", "400 {fs}px 'Yomogi',sans-serif", .08),
]
INK = "#3A2C33"


def flowers_h():
    return bougainvillea(760, H, [
        (((-20, 40), (220, 10), (420, 120), (560, 60)), 6, 46),
        (((-20, 60), (120, 200), (160, 380), (120, 560)), 6, 44),
        (((60, 120), (260, 180), (330, 330), (300, 470)), 4, 38),
    ])


def hw(font, ls):
    fs = fit(NAME, 1480, ls, 160)
    return f'''<div style="position:absolute;inset:0;background:#FFFFFF"></div>
<div style="position:absolute;left:0;top:0">{flowers_h()}</div>
<div style="position:absolute;left:780px;top:0;bottom:0;width:1560px;display:flex;flex-direction:column;justify-content:center">
  <div style="font:{font.format(fs=fs)};letter-spacing:{ls}em;color:{INK};line-height:1.2;white-space:nowrap">{NAME}</div>
  <div style="margin-top:36px;display:flex;align-items:center;gap:28px">
    {mark(BRAND, 84)}
    <span style="font:{font.format(fs=46)};letter-spacing:.16em;color:#7A5F6C">{SUB}</span>
  </div>
</div>'''


def hw_v(font):
    flowers = bougainvillea(H, 560, [
        (((-20, 30), (200, 0), (420, 90), (620, 40)), 7, 42),
        (((-20, 50), (100, 180), (140, 330), (90, 520)), 5, 40),
        (((620, 60), (500, 180), (470, 330), (520, 480)), 5, 40),
    ], seed=3)
    return f'''<div style="position:absolute;inset:0;background:#FFFFFF"></div>
<div style="position:absolute;left:0;top:0">{flowers}</div>
<div style="position:absolute;left:0;right:0;top:600px;height:1580px;display:flex;justify-content:center">
  {vtext(NAME, int(1500/len(NAME)/1.08), font, INK)}
</div>
<div style="position:absolute;left:215px;bottom:40px">{mark(BRAND, 170)}</div>'''


PAGES = ([(f"hw_{k}", f"手書き・白｜{lbl}", hw(f, ls), W, H) for k, lbl, f, ls in HANDS]
         + [(f"hwv_{k}", f"袖看板 手書き・白｜{lbl}", hw_v(f), H, W) for k, lbl, f, ls in HANDS[:2]])


async def render():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = await b.new_page()
        for key, lbl, body, w, h in PAGES:
            await pg.set_viewport_size({"width": w, "height": h})
            # ChromiumはプロキシのCAを信頼しないため、curlで落としたフォント（LOCAL_FONTS）を使う
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
    doc = (f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>看板 手書き・白</title>'
           f'<link rel="stylesheet" href="{FONTS}"><style>body{{margin:0;background:#888}}</style></head><body>'
           + "".join(page(lbl, body, w, h) for _, lbl, body, w, h in PAGES) + "</body></html>")
    (HERE / "signs_handwritten.html").write_text(doc, encoding="utf-8")
    asyncio.run(render())
