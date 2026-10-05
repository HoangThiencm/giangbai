import subprocess

test_html = """<!DOCTYPE html>
<html>
<head>
  <script>
    window.MathJax = {
      tex: {
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
        processEscapes: true
      },
      svg: { fontCache: 'global' }
    };
  </script>
  <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
</head>
<body>
  <div id="bad">
    $$\\begin{cases} \\mathbf{b = a \\cdot \\sin B = a \\cdot \\cos C} \\[4pt] \\mathbf{c = a \\cdot \\sin C = a \\cdot \\cos B} \\end{cases}$$
  </div>
</body>
</html>"""

with open('test_bad.html', 'w', encoding='utf-8') as f:
    f.write(test_html)

cmd = [
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    '--headless',
    '--disable-gpu',
    '--virtual-time-budget=5000',
    '--dump-dom',
    r'file:///c:/Users/HoangThien/Documents/GitHub/giangbai/test_bad.html'
]
res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
print('Output len:', len(res.stdout))
for line in res.stdout.splitlines():
    if '4pt' in line or 'merror' in line or 'data-mjx' in line:
        print(line[:120])
