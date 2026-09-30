"""法事事務所 看板デザイン案のジェネレーター。

signs.html  … Canva取り込み用（1ページ=1看板、data-document-role="page"）
png/*.png   … 各案のプレビュー画像
"""
import asyncio
import pathlib

HERE = pathlib.Path(__file__).parent

NAMES = {
    "cs": "セレモニーステーション",
    "hb": "南風原セレモニーステーション",
    "kk": "暮しと供養のステーション",
}
SUB = "法事・法要・納骨・ご供養のご相談"
FONTS = ("https://fonts.googleapis.com/css2?"
         "family=Zen+Old+Mincho:wght@600;700&family=Shippori+Mincho+B1:wght@700;800"
         "&family=Zen+Kaku+Gothic+New:wght@500;700&family=Zen+Maru+Gothic:wght@500;700&display=swap")

W, H = 2400, 600  # 横長ファサード看板 3600×900mm 想定（1px = 1.5mm）


def mark(color, flame=None, size=300):
    """灯明（ともしび）＋ホーム（駅の乗降台）のシンボル。"""
    flame = flame or color
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
<circle cx="100" cy="100" r="88" fill="none" stroke="{color}" stroke-width="7"/>
<path d="M100 40 C124 72 130 102 100 130 C70 102 76 72 100 40 Z" fill="{flame}"/>
<path d="M54 152 L146 152" stroke="{color}" stroke-width="7" stroke-linecap="round"/>
</svg>'''


def fit(name, avail, ls, cap):
    return min(cap, int(avail / (len(name) * (1 + ls))))


def vtext(name, fs, font, color):
    """縦書き。writing-modeはWebフォントのサブセットで字が重なるため1文字ずつ積む。"""
    small = "ァィゥェォッャュョ"
    cells = []
    for ch in name:
        t = ""
        if ch == "ー":
            t = "transform:rotate(90deg);"
        elif ch in small:
            t = f"transform:translate({fs*0.12:.0f}px,-{fs*0.12:.0f}px);"
        cells.append(f'<span style="display:block;height:{fs*1.08:.0f}px;line-height:{fs*1.08:.0f}px;{t}">{ch}</span>')
    return (f'<div style="display:flex;flex-direction:column;align-items:center;text-align:center;'
            f'font:{font.format(fs=fs)};color:{color}">' + "".join(cells) + "</div>")


def kasuri(color, bg, h=64):
    """琉球絣の帯。十字（井桁）柄を少しずらして重ね、絣特有のにじみを出す。"""
    return f'''<svg width="{W}" height="{h}" xmlns="http://www.w3.org/2000/svg">
<defs><pattern id="k{h}{color[1:]}" width="96" height="{h}" patternUnits="userSpaceOnUse">
<rect width="96" height="{h}" fill="{bg}"/>
<g fill="{color}">
<rect x="44" y="{h/2-18}" width="8" height="36"/><rect x="30" y="{h/2-4}" width="36" height="8"/>
<rect x="47" y="{h/2-22}" width="3" height="6" opacity=".6"/><rect x="62" y="{h/2-2}" width="7" height="3" opacity=".6"/>
<rect x="4" y="{h/2-3}" width="10" height="6" opacity=".7"/><rect x="82" y="{h/2-3}" width="10" height="6" opacity=".7"/>
</g></pattern></defs>
<rect width="{W}" height="{h}" fill="url(#k{h}{color[1:]})"/></svg>'''


def hanablock(w, h, bg, line):
    """沖縄の花ブロック（透かしブロック）の柄。"""
    return f'''<svg width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">
<defs><pattern id="hb" width="120" height="120" patternUnits="userSpaceOnUse">
<rect width="120" height="120" fill="{bg}"/>
<g fill="none" stroke="{line}" stroke-width="9">
<circle cx="60" cy="60" r="42"/>
<circle cx="0" cy="0" r="42"/><circle cx="120" cy="0" r="42"/>
<circle cx="0" cy="120" r="42"/><circle cx="120" cy="120" r="42"/>
</g><rect x="0.5" y="0.5" width="119" height="119" fill="none" stroke="{line}" stroke-width="2" opacity=".5"/>
</pattern></defs><rect width="{w}" height="{h}" fill="url(#hb)"/></svg>'''


# ---- 5パターン -------------------------------------------------------------

def p1(name):  # 白壁と墨
    fs = fit(name, 1640, .14, 160)
    return f'''<div style="position:absolute;inset:0;background:#EFEBE3"></div>
<div style="position:absolute;left:0;right:0;bottom:0;height:18px;background:#2B2926"></div>
<div style="position:absolute;left:150px;top:141px">{mark("#2B2926", "#A8452F")}</div>
<div style="position:absolute;left:560px;top:0;bottom:18px;width:1700px;display:flex;flex-direction:column;justify-content:center">
  <div style="font:700 {fs}px 'Zen Old Mincho',serif;letter-spacing:.14em;color:#2B2926;line-height:1.1;white-space:nowrap">{name}</div>
  <div style="margin-top:44px;display:flex;align-items:center;gap:32px">
    <span style="display:block;width:120px;height:3px;background:#2B2926"></span>
    <span style="font:500 44px 'Zen Kaku Gothic New',sans-serif;letter-spacing:.2em;color:#4A4640">{SUB}</span>
  </div>
</div>'''


def p2(name):  # 琉球絣（藍）
    fs = fit(name, 1560, .12, 150)
    return f'''<div style="position:absolute;inset:0;background:#1F3550"></div>
<div style="position:absolute;left:0;top:0">{kasuri("#E9E2D2", "#1F3550")}</div>
<div style="position:absolute;left:0;bottom:0">{kasuri("#E9E2D2", "#1F3550")}</div>
<div style="position:absolute;left:150px;top:170px">{mark("#F2ECDF", "#E3B36A", 260)}</div>
<div style="position:absolute;left:520px;top:64px;bottom:64px;width:1760px;display:flex;flex-direction:column;justify-content:center">
  <div style="font:800 {fs}px 'Shippori Mincho B1',serif;letter-spacing:.12em;color:#F2ECDF;line-height:1.15;white-space:nowrap">{name}</div>
  <div style="margin-top:40px;font:500 44px 'Zen Kaku Gothic New',sans-serif;letter-spacing:.22em;color:#C9D2DC">{SUB}</div>
</div>'''


def p3(name):  # 花ブロック（琉球石灰岩＋赤瓦）
    fs = fit(name, 1540, .06, 160)
    return f'''<div style="position:absolute;inset:0;background:#F7F3EC"></div>
<div style="position:absolute;left:0;top:0">{hanablock(600, H, "#E3D8C2", "#CDBF9F")}</div>
<div style="position:absolute;left:600px;top:0;width:14px;height:{H}px;background:#B4553A"></div>
<div style="position:absolute;left:720px;top:0;bottom:0;width:1600px;display:flex;flex-direction:column;justify-content:center">
  <div style="font:500 44px 'Zen Kaku Gothic New',sans-serif;letter-spacing:.2em;color:#B4553A">{SUB}</div>
  <div style="margin-top:30px;font:700 {fs}px 'Zen Maru Gothic',sans-serif;letter-spacing:.06em;color:#3A332C;line-height:1.15;white-space:nowrap">{name}</div>
</div>
<div style="position:absolute;right:90px;bottom:60px">{mark("#3A332C", "#B4553A", 110)}</div>'''


def p4(name):  # 木と灯り
    fs = fit(name, 1640, .14, 140)
    wood = ("repeating-linear-gradient(90deg,rgba(0,0,0,.05) 0 3px,transparent 3px 23px,rgba(255,255,255,.035) 23px 25px,transparent 25px 61px),"
            "linear-gradient(180deg,#7A5A3E,#664A32)")
    return f'''<div style="position:absolute;inset:0;background:{wood}"></div>
<div style="position:absolute;inset:36px;border:3px solid rgba(243,230,207,.55)"></div>
<div style="position:absolute;left:0;right:0;top:0;bottom:0;text-align:center;display:flex;flex-direction:column;justify-content:center">
  <div style="display:flex;justify-content:center;align-items:center;gap:40px">
    <span style="display:block;width:80px;height:2px;background:#E9C58A"></span>
    <span style="font:500 42px 'Zen Kaku Gothic New',sans-serif;letter-spacing:.3em;color:#E9C58A">{SUB}</span>
    <span style="display:block;width:80px;height:2px;background:#E9C58A"></span>
  </div>
  <div style="margin-top:44px;font:700 {fs}px 'Zen Old Mincho',serif;letter-spacing:.14em;color:#F3E6CF;line-height:1.15;white-space:nowrap">{name}</div>
</div>'''


def p5(name):  # 夜の行灯（内照式）
    fs = fit(name, 1560, .12, 146)
    return f'''<div style="position:absolute;inset:0;background:#1D1C1A"></div>
<div style="position:absolute;left:120px;top:60px;bottom:60px;width:360px;border-radius:180px;background:radial-gradient(circle at 50% 50%,#F7E3B8 0,#E9B872 45%,#3A2E20 100%)"></div>
<div style="position:absolute;left:150px;top:150px">{mark("#2A2016", "#2A2016", 300)}</div>
<div style="position:absolute;left:580px;top:0;bottom:0;width:1720px;display:flex;flex-direction:column;justify-content:center">
  <div style="font:700 {fs}px 'Zen Old Mincho',serif;letter-spacing:.12em;color:#F6E9CF;line-height:1.15;white-space:nowrap;text-shadow:0 0 24px rgba(233,184,114,.45)">{name}</div>
  <div style="margin-top:36px;height:2px;width:100%;background:#9C8358"></div>
  <div style="margin-top:32px;font:500 42px 'Zen Kaku Gothic New',sans-serif;letter-spacing:.22em;color:#BDAE92">{SUB}</div>
</div>'''


def v2(name):  # 袖看板（縦）琉球絣
    return f'''<div style="position:absolute;inset:0;background:#1F3550"></div>
<div style="position:absolute;left:0;top:0;transform-origin:0 0;transform:rotate(90deg) translate(0,-600px)">{kasuri("#E9E2D2", "#1F3550", 56)}</div>
<div style="position:absolute;left:0;top:0;transform-origin:0 0;transform:rotate(90deg) translate(0,-56px)">{kasuri("#E9E2D2", "#1F3550", 56)}</div>
<div style="position:absolute;left:170px;top:90px">{mark("#F2ECDF", "#E3B36A", 260)}</div>
<div style="position:absolute;left:0;right:0;top:430px;height:1880px;display:flex;justify-content:center">
  {vtext(name, min(150, int(1800/len(name)/1.08)), "800 {fs}px 'Shippori Mincho B1',serif", "#F2ECDF")}
</div>'''


def v3(name):  # 袖看板（縦）花ブロック
    return f'''<div style="position:absolute;inset:0;background:#F7F3EC"></div>
<div style="position:absolute;left:0;top:0">{hanablock(600, 360, "#E3D8C2", "#CDBF9F")}</div>
<div style="position:absolute;left:0;top:360px;width:600px;height:14px;background:#B4553A"></div>
<div style="position:absolute;left:0;right:0;top:470px;height:1780px;display:flex;justify-content:center">
  {vtext(name, min(150, int(1640/len(name)/1.08)), "700 {fs}px 'Zen Maru Gothic',sans-serif", "#3A332C")}
</div>
<div style="position:absolute;left:245px;bottom:60px">{mark("#3A332C", "#B4553A", 110)}</div>'''


def chia(h=420, seed=0, petal="#7B6A9B", stem="#6F7D5A"):
    """南風原町の町花・チアの花穂。茎の上半分に小さな唇形の花を段々に付ける。"""
    parts = [f'<path d="M40 {h} C38 {h*.7:.0f} 42 {h*.4:.0f} 40 20" stroke="{stem}" stroke-width="4" fill="none"/>',
             f'<ellipse cx="22" cy="{h*.78:.0f}" rx="18" ry="7" fill="{stem}" transform="rotate(-30 22 {h*.78:.0f})"/>',
             f'<ellipse cx="58" cy="{h*.7:.0f}" rx="18" ry="7" fill="{stem}" transform="rotate(30 58 {h*.7:.0f})"/>']
    y, i = 30, 0
    while y < h * 0.55:
        side = -1 if (i + seed) % 2 else 1
        size = 7 + i * 0.9
        parts.append(f'<ellipse cx="{40 + side * size:.0f}" cy="{y:.0f}" rx="{size:.0f}" ry="{size*.55:.0f}" fill="{petal}" '
                     f'transform="rotate({side*-25} {40 + side*size:.0f} {y:.0f})"/>')
        parts.append(f'<circle cx="40" cy="{y+6:.0f}" r="{size*.45:.0f}" fill="{petal}" opacity=".7"/>')
        y += 16 + i * 1.5
        i += 1
    return f'<svg width="80" height="{h}" viewBox="0 0 80 {h}" xmlns="http://www.w3.org/2000/svg">{"".join(parts)}</svg>'


def p6(name):  # 町花チア
    fs = fit(name, 1500, .12, 150)
    stalks = "".join(
        f'<div style="position:absolute;left:{x}px;bottom:0">{chia(hh, k)}</div>'
        for k, (x, hh) in enumerate([(70, 430), (150, 520), (235, 380), (310, 470), (390, 340)]))
    return f'''<div style="position:absolute;inset:0;background:#F4F1EC"></div>
<div style="position:absolute;left:0;top:0;width:520px;height:{H}px;background:#E7E2EC"></div>
{stalks}
<div style="position:absolute;left:640px;top:0;bottom:0;width:1680px;display:flex;flex-direction:column;justify-content:center">
  <div style="font:700 {fs}px 'Zen Old Mincho',serif;letter-spacing:.12em;color:#3B3346;line-height:1.15;white-space:nowrap">{name}</div>
  <div style="margin-top:40px;display:flex;align-items:center;gap:28px">
    {mark("#3B3346", "#7B6A9B", 64)}
    <span style="font:500 44px 'Zen Kaku Gothic New',sans-serif;letter-spacing:.2em;color:#5E566A">{SUB}</span>
  </div>
</div>'''


PATTERNS = [
    ("p1", "A 白壁と墨", p1, W, H),
    ("p2", "B 琉球絣", p2, W, H),
    ("p3", "C 花ブロック", p3, W, H),
    ("p4", "D 木と灯り", p4, W, H),
    ("p5", "E 夜の行灯", p5, W, H),
    ("p6", "F 町花チア", p6, W, H),
    ("v2", "B' 袖看板・琉球絣", v2, H, W),
    ("v3", "C' 袖看板・花ブロック", v3, H, W),
]


def page(label, body, w, h, attrs=True):
    role = f' data-document-role="page" data-label="{label}"' if attrs else ""
    return (f'<div{role} style="position:relative;width:{w}px;height:{h}px;overflow:hidden;'
            f'margin:0 auto 40px">{body}</div>')


def build():
    pages = []
    for key, title, fn, w, h in PATTERNS:
        for nk, name in NAMES.items():
            pages.append((f"{key}_{nk}", f"{title}｜{name}", fn(name), w, h))
    doc = (f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>看板デザイン案</title>'
           f'<link rel="stylesheet" href="{FONTS}"><style>body{{margin:0;background:#888}}</style></head><body>'
           + "".join(page(lbl, body, w, h) for _, lbl, body, w, h in pages) + "</body></html>")
    (HERE / "signs.html").write_text(doc, encoding="utf-8")
    return pages


async def render(pages):
    from playwright.async_api import async_playwright
    out = HERE / "png"
    out.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = await b.new_page()
        for key, lbl, body, w, h in pages:
            await pg.set_viewport_size({"width": w, "height": h})
            await pg.set_content(f'<html><head><meta charset="utf-8"><link rel="stylesheet" href="{FONTS}">'
                                 f'<style>body{{margin:0}}</style></head><body>{page(lbl, body, w, h, False)}</body></html>')
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(out / f"{key}.png"))
        await pg.set_viewport_size({"width": 2400, "height": 600})
        await pg.goto((HERE / "signs.html").as_uri())
        await pg.evaluate("document.fonts.ready")
        await b.close()


if __name__ == "__main__":
    asyncio.run(render(build()))
