"""生成配色表 preview/palette.png（色阶 + 语义对照 + 对比度校验）。"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE)
OUT = os.path.join(HERE, 'preview')
os.makedirs(OUT, exist_ok=True)

REG = 'C:/Windows/Fonts/msyh.ttc'
BOLD = 'C:/Windows/Fonts/msyhbd.ttc'
F = lambda s, b=False: ImageFont.truetype(BOLD if b else REG, s)


def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lum(rgb):
    def f(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (f(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = lum(hex2rgb(a)), lum(hex2rgb(b))
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


NEUTRAL = [('00', '#fbfdfd'), ('50', '#f4f8f8'), ('60', '#eef4f4'), ('75', '#e8efef'),
           ('100', '#e1eaeb'), ('150', '#d9e3e4'), ('200', '#cfdcdd'), ('300', '#b9cbcd'),
           ('400', '#93a9ad'), ('500', '#74868f'), ('600', '#5f7078'), ('700', '#3a4a56'),
           ('750', '#2b3a45'), ('800', '#23303a'), ('850', '#1d2730'), ('875', '#182129'),
           ('900', '#141c23'), ('950', '#10171d'), ('1000', '#0c1116')]
BRAND = [('50', '#e6f7f7'), ('100', '#ccf0ef'), ('200', '#9de4e2'), ('300', '#5fd3d0'),
         ('400', '#2ec1be'), ('450', '#12b0ad'), ('500', '#009e9d'), ('600', '#007a79'),
         ('700', '#00605f'), ('800', '#004a49'), ('900', '#003534')]

CHECKS = [
    ('暗 · 正文 / 页面底', '#e1eaeb', '#0c1116', 4.5),
    ('暗 · 次要 / 页面底', '#93a9ad', '#0c1116', 4.5),
    ('暗 · 强调 / 面板', '#2ec1be', '#141c23', 4.5),
    ('亮 · 正文 / 页面底', '#23303a', '#f4f8f8', 4.5),
    ('亮 · 次要 / 页面底', '#5f7078', '#f4f8f8', 4.5),
    ('亮 · 强调 / 页面底', '#007a79', '#f4f8f8', 4.5),
    ('亮 · 白字 / 强调底', '#ffffff', '#007a79', 4.5),
    ('暗 · 深字 / 强调底', '#0c1116', '#5fd3d0', 4.5),
]

W, H = 1600, 760
img = Image.new('RGB', (W, H), hex2rgb('#0b1016'))
d = ImageDraw.Draw(img)

d.text((70, 46), '防风 Zephyr · 配色表', font=F(38, True), fill=hex2rgb('#e8f1f4'))
d.text((70, 100), '一套色阶覆盖明暗：浅色读低档（雪白），暗色读高档（墨夜）', font=F(16), fill=hex2rgb('#8fa3ad'))

def strip(y, items, label):
    d.text((70, y - 26), label, font=F(13), fill=hex2rgb('#7c8f99'))
    cell = 74
    for i, (k, c) in enumerate(items):
        x = 70 + i * cell
        d.rectangle([x, y, x + cell - 4, y + 30], fill=hex2rgb(c), outline=hex2rgb('#55666f'))
        dark = lum(hex2rgb(c)) < 0.35
        d.text((x + (cell - 4) / 2, y + 15), k, font=F(9), fill=hex2rgb('#e8f1f4' if dark else '#1e2a30'), anchor='mm')

strip(148, NEUTRAL, '中性（19 档）')
strip(224, BRAND, '品牌（11 档，由 #009E9D 派生）')

y = 320
d.text((70, y), '关键对比度（WCAG）', font=F(17, True), fill=hex2rgb('#e8f1f4'))
for i, (label, fg, bg, need) in enumerate(CHECKS):
    col, row = i // 4, i % 4
    x = 70 + col * 760
    yy = y + 40 + row * 34
    ratio = contrast(fg, bg)
    ok = ratio >= need
    d.rounded_rectangle([x, yy + 3, x + 18, yy + 21], 4, fill=hex2rgb(fg), outline=hex2rgb(bg), width=2)
    d.text((x + 28, yy), label, font=F(13), fill=hex2rgb('#b9c8cf'))
    d.text((x + 560, yy), f'{ratio:.2f}:1', font=F(13, True), fill=hex2rgb('#7fd8c9' if ok else '#e06c75'), anchor='ra')
    d.text((x + 620, yy), 'PASS' if ok else 'LOW', font=F(11, True), fill=hex2rgb('#7fd8c9' if ok else '#e06c75'), anchor='ra')

d.text((70, 500), '圆角：xs2 / sm4 / md6 / lg8 / xl10 / panel12', font=F(13), fill=hex2rgb('#7c8f99'))
d.text((70, 526), '强调色只用 300–700 档；两端留给背景与描边', font=F(13), fill=hex2rgb('#7c8f99'))

img.save(os.path.join(OUT, 'palette.png'))
print('wrote preview/palette.png', img.size)
