"""主题单独的一图流：preview/overview.png（1600x1000）。"""
import json
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE)
OUT = os.path.join(HERE, 'preview')
os.makedirs(OUT, exist_ok=True)

with open(os.path.join(HERE, 'package.json'), encoding='utf-8') as fh:
    VERSION = json.load(fh)['version']

REG = 'C:/Windows/Fonts/msyh.ttc'
BOLD = 'C:/Windows/Fonts/msyhbd.ttc'
F = lambda s, b=False: ImageFont.truetype(BOLD if b else REG, s)

W, H = 1600, 1160
BG = (12, 17, 23)
TEXT = (232, 241, 244)
DIM = (145, 165, 175)
FAINT = (92, 110, 121)
CYAN = (127, 216, 201)
ACCENT = (0, 158, 157)

img = Image.new('RGBA', (W, H), BG + (255,))
d = ImageDraw.Draw(img, 'RGBA')

g = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ImageDraw.Draw(g).ellipse([-340, -620, 1180, 640], fill=(0, 46, 50, 80))
img.alpha_composite(g.filter(ImageFilter.GaussianBlur(120)))


def badge(x, y, text):
    tw = d.textlength(text, font=F(13))
    d.rounded_rectangle([x, y, x + tw + 24, y + 26], 12, fill=ACCENT + (40,), outline=ACCENT + (130,), width=1)
    d.text((x + 12, y + 13), text, font=F(13), fill=CYAN, anchor='lm')
    return x + tw + 24


d.text((70, 46), '防风 Zephyr · 主题', font=F(44, True), fill=TEXT)
d.text((72, 110), '把 DSH 换成冷青雪原：一套配色、立绘背景、飘雪和启动画面', font=F(18), fill=DIM)
bx = badge(70, 152, 'dsh-zephyr-theme ' + VERSION)
badge(bx + 10, 152, '19 + 11 档色阶 · 对比度全 AA')

# ---------------- 左：两块画面 ----------------
d.text((70, 212), '① 画面', font=F(20, True), fill=CYAN)

hero = Image.open('assets/hero-dark.webp').convert('RGB').resize((640, 360), Image.LANCZOS)
img.paste(hero, (70, 250))
d.rounded_rectangle([70, 250, 709, 609], 10, outline=(0, 158, 157, 90), width=1)
hcx = 70 + 320
d.text((hcx, 250 + 92), 'ZEPHYR', font=F(10, True), fill=CYAN, anchor='mm')
d.text((hcx, 250 + 120), '今天，想做点什么？', font=F(19, True), fill=TEXT, anchor='mm')
d.text((hcx, 250 + 146), '从一个问题开始，剩下的交给防风。', font=F(9), fill=DIM, anchor='mm')
d.rounded_rectangle([hcx - 160, 250 + 170, hcx + 160, 250 + 210], 10,
                    fill=(24, 31, 39, 235), outline=(255, 255, 255, 40), width=1)
d.text((hcx - 142, 250 + 190), '说点什么…', font=F(10), fill=DIM, anchor='lm')
d.text((70, 622), '空状态页 · 立绘靠右留白 + 纯 CSS 飘雪', font=F(12.5), fill=FAINT)

splash = Image.open('assets/splash-dark.webp').convert('RGB').resize((300, 169), Image.LANCZOS)
img.paste(splash, (70, 660))
d.rounded_rectangle([70, 660, 369, 828], 8, outline=(0, 158, 157, 110), width=1)
d.text((70 + 72, 660 + 46), 'ZEPHYR', font=F(15, True), fill=TEXT, anchor='mm')
d.text((70 + 72, 660 + 68), '防风', font=F(10, True), fill=CYAN, anchor='mm')
d.rounded_rectangle([70 + 30, 660 + 92, 70 + 158, 660 + 94], 1, fill=(255, 255, 255, 40))
d.rounded_rectangle([70 + 30, 660 + 92, 70 + 118, 660 + 94], 1, fill=CYAN)
d.text((70 + 72, 660 + 116), '正在准备界面…', font=F(7), fill=FAINT, anchor='mm')

tx = 400
d.text((tx, 672), '启动画面', font=F(17, True), fill=TEXT)
for i, line in enumerate(['文字与进度条都是 DOM', '0 → 74% 带一道流光', '自动淡出后移除']):
    d.text((tx, 704 + i * 24), line, font=F(12.5), fill=DIM)
d.text((tx, 784), '时长 0–10s 可调', font=F(12.5), fill=CYAN)

# ---------------- 右：功能 ----------------
d.text((790, 212), '② 做法', font=F(20, True), fill=CYAN)

items = [
    ('只换令牌', '中性 19 档 + 品牌 11 档色阶 + 圆角，不碰任何组件类名，宿主升级不错位'),
    ('一套色阶两副面孔', '浅色读低档（雪白 #fbfdfd），暗色读高档（墨夜 #0c1116），跟随系统切换'),
    ('立绘空状态页', '挂在 [data-phase="hero"] 上，人物靠右留白，不挡标题和输入框'),
    ('飘雪', '纯 CSS 点阵，120px 瓦片位移正好一屏循环，无缝；尊重「减少动效」'),
    ('启动画面', '文字与进度条是 DOM，条从左涨到 74% 并带流光，淡出后自动移除'),
    ('时长可调 · 每页一次', 'splashMs 默认 2000，范围 0–10000；sessionStorage 记标记，刷新不重复等'),
    ('对比度全 AA', '正文 15.5:1、次要 7.7:1、浅色强调 4.8:1；强调只用 300–700 档'),
]
lx = 790
for i, (title, desc) in enumerate(items):
    y = 246 + i * 84
    d.ellipse([lx, y + 2, lx + 22, y + 24], fill=(0, 158, 157, 36), outline=ACCENT + (140,), width=1)
    d.text((lx + 11, y + 13), str(i + 1), font=F(12, True), fill=CYAN, anchor='mm')
    d.text((lx + 34, y - 3), title, font=F(18, True), fill=TEXT)
    line, ty = '', y + 26
    for ch in desc:
        if d.textlength(line + ch, font=F(12.5)) > 720:
            d.text((lx + 34, ty), line, font=F(12.5), fill=DIM)
            ty += 21
            line = ch
        else:
            line += ch
    if line:
        d.text((lx + 34, ty), line, font=F(12.5), fill=DIM)

# ---------------- 底部 ----------------
cards = [
    ('151 KB', '打包后体积，只剩一份 CSS'),
    ('两套主题', '墨夜 / 雪白 自动跟随系统'),
    ('一键还原', '移除 data-zephyr-ui 即恢复原样'),
]
cw, gap = 460, 26
for i, (title, desc) in enumerate(cards):
    x = 70 + i * (cw + gap)
    d.rounded_rectangle([x, 856, x + cw, 944], 14, fill=(18, 27, 37), outline=(255, 255, 255, 16), width=1)
    d.rounded_rectangle([x + 22, 872, x + 58, 875], 1, fill=ACCENT + (200,))
    d.text((x + 22, 886), title, font=F(17, True), fill=TEXT)
    d.text((x + 22, 916), desc, font=F(13), fill=DIM)

# ---------------- 版本改进 ----------------
d.text((70, 972), '本版改进', font=F(20, True), fill=CYAN)
d.text((216, 980), 'v' + VERSION + ' 相比上一版', font=F(13), fill=FAINT)
changes = [
    ('启动画面', '同一标签页只播一次，刷新不再重复等待'),
    ('包体积', 'CSS 改成外链，274 KB → 151 KB'),
    ('client.js', '182 KB → 1.2 KB，不再内联整份样式'),
]
for i, (tag, note) in enumerate(changes):
    y = 1020 + i * 40
    d.text((70, y), tag, font=F(13.5, True), fill=CYAN)
    d.text((164, y), note, font=F(13.5), fill=DIM)

d.text((W // 2, H - 22), '角色「防风 / Zephyr」· 虚拟歌姬企划组 · #009E9D',
       font=F(12), fill=(58, 72, 82), anchor='mm')

img.convert('RGB').save(os.path.join(OUT, 'overview.png'))
img.convert('RGB').save(os.path.join(OUT, 'overview.pdf'), 'PDF', resolution=150)
print('wrote preview/overview.png + .pdf', img.size)
