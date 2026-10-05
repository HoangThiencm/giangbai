import subprocess
import re

with open('test_good.html', 'r', encoding='utf-8') as f:
    print('test_good content:')
    print(f.read())

cmd = [
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    '--headless',
    '--disable-gpu',
    '--virtual-time-budget=5000',
    '--dump-dom',
    r'file:///c:/Users/HoangThien/Documents/GitHub/giangbai/test_good.html'
]
res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

for m in re.finditer(r'<g[^>]*merror[^>]*>.*?</g>', res.stdout, re.DOTALL):
    print('Found merror in DOM:', m.group(0)[:200])

for m in re.finditer(r'data-mjx-error="([^"]+)"', res.stdout):
    print('data-mjx-error:', m.group(1))
