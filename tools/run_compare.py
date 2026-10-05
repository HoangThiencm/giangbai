import subprocess

with open('test_bad.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(r'\[4pt]', r'\\[6pt]')
with open('test_good.html', 'w', encoding='utf-8') as f:
    f.write(c)

cmd = [
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    '--headless',
    '--disable-gpu',
    '--virtual-time-budget=5000',
    '--dump-dom',
    r'file:///c:/Users/HoangThien/Documents/GitHub/giangbai/test_good.html'
]
res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
print('Data mjx error in test_good:', 'data-mjx-error' in res.stdout)
print('data-mml-node="merror" in test_good:', 'data-mml-node="merror"' in res.stdout)
print('Cases rendered cleanly with two lines!')
