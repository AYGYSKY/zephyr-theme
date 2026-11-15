"""生成 hero / splash 效果对比图 preview/hero-preview.png、splash-preview.png。"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE)
OUT = os.path.join(HERE, 'preview')
os.makedirs(OUT, exist_ok=True)

REG = 'C:/Windows/Fonts/msyh.ttc'
BOLD = 'C:/Windows/Fonts/msyhbd.ttc'
F = lambda s, b=False: ImageFont.truetype(BOLD if b else REG, s)

W, H = 1400, 788
SCALE = W / 2560


def hero(path, dark):
    im = Image.open(path).resize((W, H), Image.LANCZOS)
    d = ImageDraw.Draw(im, 'RGBA')
    fg = (232, 241, 244) if dark else (30, 42, 48)
    dim = (150, 168, 176) if dark else (110, 128, 136)
    line = (255, 255, 255, 46) if dark else (0, 0, 0, 28)
    fill = (24, 31, 39) if dark else (255, 255, 255)
    cx = W // 2
    d.text((cx, 250), 'ZEPHYR', font=F(13, True), fill=(0, 158, 157), anchor='mm')
    d.text((cx, 292), '今天，想做点什么？', font=F(34, True), fill=fg, anchor='mm')
    d.text((cx, 330), '从一个问题开始，剩下的交给防风。', font=F(13), fill=dim, anchor='mm')
    bw, bh = 560, 70
    x0, y0 = cx - bw // 2, 400
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], 14, fill=fill, outline=line, width=1)
    d.text((x0 + 22, y0 + bh // 2), '说点什么…', font=F(13), fill=dim, anchor='lm')
    d.rounded_rectangle([x0 + bw - 82, y0 + 16, x0 + bw - 16, y0 + bh - 16], 9, fill=(0, 158, 157))
    d.text((x0 + bw - 49, y0 + bh // 2), '发送', font=F(10, True), fill=(255, 255, 255), anchor='mm')
    return im


def splash(path, dark):
    im = Image.open(path).resize((W, H), Image.LANCZOS)
    d = ImageDraw.Draw(im, 'RGBA')
    fg = (238, 246, 247) if dark else (30, 42, 48)
    dim = (180, 198, 206) if dark else (90, 112, 120)
    cx, cy = int(W * 0.28), H // 2
    d.text((cx, cy - 40), 'ZEPHYR', font=F(48, True), fill=fg, anchor='mm')
    d.text((cx, cy + 8), '防风', font=F(20, True), fill=(0, 158, 157), anchor='mm')
    d.text((cx, cy + 40), 'DeepSeek Harness · 主题', font=F(12), fill=dim, anchor='mm')
    bx0, bx1, by = cx - 140, cx + 140, cy + 96
    d.rounded_rectangle([bx0, by, bx1, by + 3], 2, fill=(255, 255, 255, 40) if dark else (0, 0, 0, 26))
    d.rounded_rectangle([bx0, by, bx0 + 207, by + 3], 2, fill=(0, 158, 157))
    d.text((cx, by + 24), '正在准备界面…', font=F(10), fill=dim, anchor='mm')
    return im


for name, dark in (('dark', True), ('light', False)):
    a = hero(f'assets/hero-{name}.webp', dark)
    b = splash(f'assets/splash-{name}.webp', dark)
    out = Image.new('RGB', (W, H * 2 + 20), (8, 12, 16))
    out.paste(a, (0, 0))
    out.paste(b, (0, H + 20))
    d = ImageDraw.Draw(out)
    d.text((18, 14), f'HERO · {name.upper()}', font=F(13, True), fill=(127, 216, 201))
    d.text((18, H + 34), f'SPLASH · {name.upper()}', font=F(13, True), fill=(0, 158, 157))
    if name == 'dark':
        out.save(os.path.join(OUT, 'hero-preview.png'))
    else:
        out.save(os.path.join(OUT, 'splash-preview.png'))
    print('wrote', name)

# 合并成一张双主题对比
a = Image.open(os.path.join(OUT, 'hero-preview.png'))
b = Image.open(os.path.join(OUT, 'splash-preview.png'))
combo = Image.new('RGB', (W, a.height + b.height + 20), (8, 12, 16))
combo.paste(b, (0, 0))
combo.paste(a, (0, b.height + 20))
combo.save(os.path.join(OUT, 'themes-preview.png'))
print('wrote themes-preview.png')
