/**
 * Host half of the Zephyr theme bundle.
 *
 * The theme itself is pure CSS (see theme.css). The Client half can inject it too,
 * but a page reload would then paint the default look first and switch after the
 * bundle loads. Injecting the same stylesheet into the served index.html through
 * `webserver/index-inject` puts it in `<head>`, so the very first paint is already
 * Zephyr-coloured.
 *
 * The boot script mounts the splash layer (`#zephyr-splash`) and carries the
 * configured dwell time into CSS through one custom property, so changing
 * `splashMs` only needs a page reload — no rebuild.
 */
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

// 只有能在包目录里解析到 schemastery 时才提供图形化 Config；
// 解析不到就退化成纯 config 读取，插件照常工作。
let z = null
try {
  const mod = await import('@deepseek-ai/schemastery')
  z = mod.z || mod.default || null
} catch (err) {
  z = null
}

const ROOT = dirname(fileURLToPath(import.meta.url))
const CSS_FILE = join(ROOT, 'theme.css')
const CSS_ROUTE = '/zephyr-theme.css'

const SPLASH_DEFAULT_MS = 2000
const SPLASH_MAX_MS = 10000

export const Config = z
  ? z.object({
    splashMs: z.number()
      .min(0)
      .max(SPLASH_MAX_MS)
      .step(100)
      .default(SPLASH_DEFAULT_MS)
      .description('启动画面停留时长（毫秒）。默认 2000，0 = 不显示，最大 10000。改完刷新页面生效。'),
  })
  : undefined

const SPLASH_HTML =
  '<div class="zs-left">'
  + '<div class="zs-title">ZEPHYR</div>'
  + '<div class="zs-sub">防风</div>'
  + '<div class="zs-note">DeepSeek Harness · 主题</div>'
  + '<div class="zs-bar"><i></i></div>'
  + '<div class="zs-hint">正在准备界面…</div>'
  + '</div>'

export function normalizeSplashMs(value) {
  const n = Number(value)
  if (!Number.isFinite(n)) return SPLASH_DEFAULT_MS
  return Math.min(SPLASH_MAX_MS, Math.max(0, Math.round(n)))
}

export function buildBootScript(ms) {
  const fallback = normalizeSplashMs(ms)

  // 时长可以在浏览器里临时覆盖：localStorage['zephyr-splash-ms']，刷新即生效。
  let body = '(function(){try{'
    + 'var d=document,root=d.documentElement;'
    + 'root.setAttribute("data-zephyr-ui","");'
    + 'var ms=' + fallback + ';'
    + 'try{var v=parseInt(root.ownerDocument.defaultView.localStorage'
    + '.getItem("zephyr-splash-ms"),10);if(isFinite(v))ms=v;}catch(e){}'
    + 'ms=Math.max(0,Math.min(10000,Math.round(ms)));'
    + 'root.style.setProperty("--zephyr-splash-ms",ms+"ms");'
    + 'if(ms<=0||d.getElementById("zephyr-splash"))return;'
    // 同一个标签页只播一次：刷新不再重复等待。
    + 'var seen=0;'
    + 'try{seen=root.ownerDocument.defaultView.sessionStorage'
    + '.getItem("zephyr-splash-seen")?1:0;}catch(e){}'
    + 'if(seen)return;'
    + 'try{root.ownerDocument.defaultView.sessionStorage'
    + '.setItem("zephyr-splash-seen","1");}catch(e){}'
    + 'function mount(){'
    + 'if(!d.body||d.getElementById("zephyr-splash"))return;'
    + 'var s=d.createElement("div");'
    + 's.id="zephyr-splash";'
    + 's.setAttribute("aria-hidden","true");'
    + 's.innerHTML=' + JSON.stringify(SPLASH_HTML) + ';'
    + 'd.body.appendChild(s);'
    + 'setTimeout(function(){try{s.remove()}catch(e){}},ms+800);'
    + '}'
    + 'if(d.body)mount();else d.addEventListener("DOMContentLoaded",mount);'
    + '}catch(e){}})();'

  return body
}

let cachedCss = null

function readCss() {
  if (cachedCss !== null) return cachedCss
  try {
    cachedCss = readFileSync(CSS_FILE, 'utf8')
  } catch (err) {
    cachedCss = ''
  }
  return cachedCss
}

export function apply(ctx, config) {
  if (typeof ctx.on !== 'function') return

  const splashMs = normalizeSplashMs(config && config.splashMs)

  ctx.on('webserver/index-inject', (table) => {
    if (!Array.isArray(table)) return
    // 去重看内容是稳的：row 上自定义字段可能被宿主丢掉。
    const already = table.some((row) => row
      && typeof row.text === 'string'
      && row.text.includes('data-zephyr-ui'))
    if (already) return
    const css = readCss()
    if (!css) return
    table.push({ kind: 'style', text: css })
    table.push({ kind: 'script', placement: 'body', text: buildBootScript(splashMs) })
  })

  // 兜底路径：client 侧不再内联整份 CSS，需要时从这条路由取（带浏览器缓存）。
  ctx.inject(['webServer'], (scope) => {
    const dispose = scope.webServer.register({
      kind: 'exact',
      path: CSS_ROUTE,
      handler: (req, res) => {
        const css = readCss()
        res.writeHead(200, {
          'content-type': 'text/css; charset=utf-8',
          'cache-control': 'public, max-age=300',
          'x-content-type-options': 'nosniff',
        })
        res.end(css)
      },
    })
    return () => { if (typeof dispose === 'function') dispose() }
  })
}
