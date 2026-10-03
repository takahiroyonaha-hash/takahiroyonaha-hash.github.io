"""手書き風文字版（白背景・ブーゲンビリア）のAffinity向けベクター版。文字はアウトライン化済み。

出力: signboard/affinity/hw_*.svg / .pdf / png/hw_*.png（affinity.py と同じ仕組み）
"""
import asyncio

import affinity as A
from affinity import (BRAND, H, INK, SOFT, W, bougain, doc, fit_size, lotus, rect, text_path, vtext_path)

FONTS = [
    ("klee", "KleeOne-SemiBold.ttf", .10),
    ("kurenaido", "ZenKurenaido-Regular.ttf", .10),
    ("syuku", "YujiSyuku-Regular.ttf", .08),
    ("yomogi", "Yomogi-Regular.ttf", .08),
]


def hw_h(fname, ls):
    bg = rect(0, 0, W, H, "#FFFFFF")
    fl = bougain(760, H, [
        (((-20, 40), (220, 10), (420, 120), (560, 60)), 7, 46),
        (((-20, 60), (120, 200), (160, 380), (120, 560)), 7, 44),
        (((60, 120), (260, 180), (330, 330), (300, 470)), 5, 38),
    ], 1)
    nx = 820
    fs = fit_size(A.NAME, fname, W - nx - 130, ls, 150)
    tx = (text_path(A.NAME, fname, fs, nx, 318, INK, ls, pid="shop-name")
          + text_path(A.SUB, fname, 46, nx + 130, 408, SOFT, .14, pid="sub-copy"))
    return bg, fl, lotus(nx, 370, 100), tx


def hw_v(fname):
    bg = rect(0, 0, H, W, "#FFFFFF")
    fl = bougain(H, 560, [
        (((-20, 30), (200, 0), (420, 90), (620, 40)), 7, 42),
        (((-20, 50), (100, 180), (140, 330), (90, 520)), 5, 40),
        (((620, 60), (500, 180), (470, 330), (520, 480)), 5, 40),
    ], 3)
    tx = vtext_path(A.NAME, fname, 114, 300, 640, INK, pid="shop-name")
    return bg, fl, lotus(200, 2210, 200), tx


def build():
    A.OUT.mkdir(exist_ok=True)
    A.font  # フォント読み込みは affinity.font がファイル名で行う
    files = []
    for key, fname, ls in FONTS:
        bg, fl, mk, tx = hw_h(fname, ls)
        svg = doc(f"看板 手書き {key}", W, H, [("background", bg), ("flowers", fl), ("logo", mk), ("text", tx)])
        files.append((f"hw_h_{key}", svg, W, H))
    for key, fname, ls in FONTS[:2]:
        bg, fl, mk, tx = hw_v(fname)
        svg = doc(f"袖看板 手書き {key}", H, W, [("background", bg), ("flowers", fl), ("logo", mk), ("text", tx)])
        files.append((f"hw_v_{key}", svg, H, W))
    for key, svg, w, h in files:
        (A.OUT / f"{key}.svg").write_text(svg, encoding="utf-8")
    return files


if __name__ == "__main__":
    asyncio.run(A.render(build()))
