写在前面的话：
你好我叫AYGY暗夜古韵
或者你可以叫我
ANSE安娜斯千

贴纸与形象来自虚拟歌姬「防风Zephyr」企划组，按授权允许非商用二次分发，禁止商用。
关注防风Zephyr


# 防风主题 Zephyr Theme（dsh-zephyr-theme）

把 DSH 界面换成防风（Zephyr）的冷青配色：墨夜 / 雪白两套、角色立绘空状态背景、
飘雪，以及一个带进度动画的启动画面。

## 做了什么

- **只替换设计令牌**：中性 19 档 + 品牌 11 档色阶 + 圆角，不碰任何组件类名
- **一套色阶覆盖明暗**：浅色读低档（雪白），暗色读高档（墨夜），跟随系统自动切换
- **空状态页背景**：`[data-phase="hero"]` 上挂立绘（暗/亮两张），叠加飘雪点阵
- **启动画面**：host 注入 `#zephyr-splash`，文字与进度条是 DOM，进度条会涨、有流光
- **可关闭**：所有规则都挂在 `html[data-zephyr-ui]` 下，移除插件立刻还原

> 需要 DSH **44.7.0 或更高**。

## 安装

```bash
dsh plugin --profile web add github:AYGYSKY/zephyr-theme
```
把 `dist/dsh-zephyr-theme-0.1.1.tgz` 发给对方，在 DSH 里对助手说：

> 装一下这个插件：<你保存它的位置>\dsh-zephyr-theme-0.1.1.tgz

或者解压到目录后装那个目录（link 安装，改文件即时生效）。装完**刷新页面**。

## 配置：启动画面时长

| 项 | 默认 | 范围 | 说明 |
|---|---|---|---|
| `splashMs` | `2000` | `0` – `10000` | 启动画面停留毫秒数；`0` = 不显示 |

三种改法：

1. **浏览器里临时试**（刷新即生效）：
   `localStorage.setItem('zephyr-splash-ms', '5000')`
2. **包内 `cordis.patch.yml`**：改完重新安装
3. **profile 层 override**：改完重启 DSH

进度条、淡出、纯色遮罩都按 `splashMs` **等比缩放**，改成几秒都不会出现
“条涨完了还在干等”。

## 已知限制

- 设置页里的图形表单需要包目录能解析到 `@deepseek-ai/schemastery`。
  link 安装时解析不到会退化成无表单（插件照常工作）；**tgz 安装**时包在
  profile 的 `node_modules` 下，能正常解析，表单会出现。
- 启动画面**同一个标签页只播一次**（用 sessionStorage 记标记），刷新不再重复等待；
  换新标签页或清掉站点数据后会再播一次。

## 文件结构

```
zephyr-theme/
├── package.json / cordis.patch.yml / index.js   # 插件本体
├── theme.css         # 构建产物：完整 CSS（图片 base64 内联）
├── client.js         # 构建产物：client 兜底（1.2 KB，CSS 走外链，不内联）
├── src/theme.css     # 源码：色阶替换
├── src/backdrop.css  # 源码：hero 背景、飘雪、启动画面
├── src/client.template.js
├── assets/*.webp     # 进包的四张背景（hero/splash × 暗亮）
├── assets-source/    # 母版：抠好的立绘（不进包）
├── preview/          # 设计稿（不进包）
│   ├── overview.png      # 主题介绍图
│   ├── palette.png       # 配色表 + 对比度校验
│   ├── themes-preview.png# hero/splash × 明暗 四联
│   ├── hero-preview.png
│   └── splash-preview.png
└── tools/            # build.js / pack.py / make_onepager.py / make_palette.py / make_preview.py
```

## 开发

```bash
node tools/build.js            # 改完 src/ 里的 CSS 后重新合成
python tools/pack.py           # 出 dist/*.tgz
python tools/make_onepager.py  # 重新生成一图流（PNG + PDF）
python tools/make_palette.py   # 重新生成配色表
python tools/make_preview.py   # 重新生成效果对比图
```

## 素材说明

贴纸与形象来自虚拟歌姬「防风Zephyr」企划组，按授权允许非商用二次分发，禁止商用。
