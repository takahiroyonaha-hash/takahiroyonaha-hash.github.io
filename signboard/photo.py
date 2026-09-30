"""写真入り看板（名称：暮しと供養のステーション）。signs_photo.html を書き出す。

写真は Pexels（無料・クレジット表記不要）。Canva取り込み時に Canva 側が直接読み込む。
"""
import pathlib

from build import BRAND, FONTS, SUB, W, H, fit, mark, page, vtext

HERE = pathlib.Path(__file__).parent
NAME = "暮しと供養のステーション"


def px(pid, w=2400):
    return f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?auto=compress&cs=tinysrgb&w={w}"


WALL = "1732419"   # 白壁に垂れるブーゲンビリア
DUSK = "11837424"  # 夕空とブーゲンビリア
PINK = "4913320"   # 家の外壁を覆うブーゲンビリア


def img(pid, left, top, w, h, pos="50% 50%"):
    return (f'<img src="{px(pid)}" alt="ブーゲンビリア" style="position:absolute;left:{left}px;top:{top}px;'
            f'width:{w}px;height:{h}px;object-fit:cover;object-position:{pos}">')


def ph1():  # 写真パネル左＋白地
    fs = fit(NAME, 1380, .12, 150)
    return f'''<div style="position:absolute;inset:0;background:#F6F2EE"></div>
{img(WALL, -200, -40, 1220, 1830)}
<div style="position:absolute;left:820px;top:0;width:{W-820}px;height:{H}px;background:#F6F2EE"></div>
<div style="position:absolute;left:820px;top:0;width:10px;height:{H}px;background:#B8337A"></div>
<div style="position:absolute;left:930px;top:0;bottom:0;width:1400px;display:flex;flex-direction:column;justify-content:center">
  <div style="font:700 {fs}px 'Zen Old Mincho',serif;letter-spacing:.12em;color:#3A2C33;line-height:1.15;white-space:nowrap">{NAME}</div>
  <div style="margin-top:40px;display:flex;align-items:center;gap:28px">
    {mark(BRAND, 84)}
    <span style="font:500 44px 'Zen Kaku Gothic New',sans-serif;letter-spacing:.2em;color:#6A5560">{SUB}</span>
  </div>
</div>'''


def ph2():  # 全面写真（夕空）＋文字
    fs = fit(NAME, 1420, .12, 150)
    return f'''<div style="position:absolute;inset:0;background:#1F2A33"></div>
{img(DUSK, 0, 0, W, H, "50% 30%")}
<div style="position:absolute;left:740px;top:0;width:{W-740}px;height:{H}px;background:#161D24;opacity:.82"></div>
<div style="position:absolute;left:860px;top:0;bottom:0;width:1460px;display:flex;flex-direction:column;justify-content:center">
  <div style="font:700 {fs}px 'Zen Old Mincho',serif;letter-spacing:.12em;color:#F6EEE6;line-height:1.15;white-space:nowrap">{NAME}</div>
  <div style="margin-top:40px;display:flex;align-items:center;gap:28px">
    {mark("#F6EEE6", 84)}
    <span style="font:500 44px 'Zen Kaku Gothic New',sans-serif;letter-spacing:.2em;color:#E3D6DC">{SUB}</span>
  </div>
</div>'''


def ph3():  # 文字左＋写真右（窓のように切り取る）
    fs = fit(NAME, 1380, .1, 150)
    return f'''<div style="position:absolute;inset:0;background:#F6F2EE"></div>
<div style="position:absolute;left:130px;top:0;bottom:0;width:1450px;display:flex;flex-direction:column;justify-content:center">
  <div style="display:flex;align-items:center;gap:28px">
    {mark(BRAND, 84)}
    <span style="font:500 44px 'Zen Kaku Gothic New',sans-serif;letter-spacing:.2em;color:#B8337A">{SUB}</span>
  </div>
  <div style="margin-top:36px;font:700 {fs}px 'Zen Maru Gothic',sans-serif;letter-spacing:.1em;color:#3A2C33;line-height:1.15;white-space:nowrap">{NAME}</div>
</div>
{img(PINK, 1680, 60, 660, 480, "50% 60%")}'''


def pv1():  # 袖看板：写真上＋縦書き
    return f'''<div style="position:absolute;inset:0;background:#F6F2EE"></div>
{img(WALL, -260, -20, 1120, 1678)}
<div style="position:absolute;left:0;top:820px;width:{H}px;height:{W-820}px;background:#F6F2EE"></div>
<div style="position:absolute;left:0;top:820px;width:{H}px;height:10px;background:#B8337A"></div>
<div style="position:absolute;left:0;right:0;top:900px;height:1260px;display:flex;justify-content:center">
  {vtext(NAME, int(1180/len(NAME)/1.08), "700 {fs}px 'Zen Old Mincho',serif", "#3A2C33")}
</div>
<div style="position:absolute;left:215px;bottom:40px">{mark(BRAND, 170)}</div>'''


PAGES = [
    ("H1 写真パネル（白壁のブーゲンビリア）", ph1, W, H),
    ("H2 全面写真（夕空）", ph2, W, H),
    ("H3 写真を窓のように", ph3, W, H),
    ("V1 袖看板・写真上", pv1, H, W),
]

if __name__ == "__main__":
    doc = (f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>看板 写真版</title>'
           f'<link rel="stylesheet" href="{FONTS}"><style>body{{margin:0;background:#888}}</style></head><body>'
           + "".join(page(lbl, fn(), w, h) for lbl, fn, w, h in PAGES) + "</body></html>")
    (HERE / "signs_photo.html").write_text(doc, encoding="utf-8")
