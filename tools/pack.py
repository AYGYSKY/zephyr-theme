"""把主题包打成可分发 tgz。

只带运行时文件：package.json / index.js / theme.css / client.js /
cordis.patch.yml / locale / icon。assets-source、preview、tools 都不进包。
"""
import glob
import json
import os
import tarfile

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open('package.json', 'r', encoding='utf-8') as fh:
    version = os.environ.get('ZEPHYR_VERSION') or json.load(fh)['version']

files = [
    'package.json',
    'index.js',
    'theme.css',
    'client.js',
    'cordis.patch.yml',
    'icon.png',
    'README.md',
]
files += sorted(glob.glob('locale/*.json'))

missing = [f for f in files if not os.path.exists(f)]
if missing:
    raise SystemExit('缺少文件：' + ', '.join(missing))

os.makedirs('dist', exist_ok=True)
out = 'dist/dsh-zephyr-theme-%s.tgz' % version
with tarfile.open(out, 'w:gz') as tf:
    for name in files:
        tf.add(name, arcname='package/' + name.replace(os.sep, '/'))

print('packed', out, round(os.path.getsize(out) / 1024, 1), 'KB')
with tarfile.open(out) as tf:
    for name in tf.getnames():
        print('  ', name)
