import sys
from PySide6.QtGui import QGuiApplication, QImage, QPainter, QColor
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QByteArray

app = QGuiApplication.instance() or QGuiApplication(sys.argv)
svg_data = QByteArray(b'<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect width="100" height="100" fill="red"/></svg>')
renderer = QSvgRenderer(svg_data)
img = QImage(100, 100, QImage.Format_ARGB32)
img.fill(QColor(255, 255, 255))
p = QPainter(img)
renderer.render(p)
p.end()
img.save("GIAO AN/hinh_ve_sgk/test_render.png")
print("Rendered test_render.png successfully!")
