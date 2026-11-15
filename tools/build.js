// 把 theme.css + backdrop.css 与 4 张背景图合成两样东西：
//   theme.css  —— host 侧首屏注入用（图片 base64 已内联）
//   client.js  —— client 侧兜底（没有 webServer 的宿主也能生效）
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));

const raw = [
  readFileSync(join(root, 'src', 'theme.css'), 'utf8'),
  readFileSync(join(root, 'src', 'backdrop.css'), 'utf8'),
].join('\n');

function dataUri(file) {
  const bytes = readFileSync(join(root, 'assets', file));
  return `data:image/webp;base64,${bytes.toString('base64')}`;
}

const images = {
  __HERO_DARK__: dataUri('hero-dark.webp'),
  __HERO_LIGHT__: dataUri('hero-light.webp'),
  __SPLASH_DARK__: dataUri('splash-dark.webp'),
  __SPLASH_LIGHT__: dataUri('splash-light.webp'),
};

let css = '/*!zephyr-theme*/\n' + raw;
for (const [token, uri] of Object.entries(images)) {
  css = css.split(token).join(uri);
}
const left = css.match(/__[A-Z_]+__/);
if (left) throw new Error(`占位符没有替换干净：${left[0]}`);

writeFileSync(join(root, 'theme.css'), css);
console.log(`theme.css written: ${(css.length / 1024).toFixed(1)} KB`);

// client 只做兜底：不内联 CSS，运行时从 /zephyr-theme.css 取。
const out = readFileSync(join(root, 'src', 'client.template.js'), 'utf8');
writeFileSync(join(root, 'client.js'), out);
console.log(`client.js written: ${(out.length / 1024).toFixed(1)} KB (外链模式)`);
