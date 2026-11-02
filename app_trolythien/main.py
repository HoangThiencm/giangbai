"""Điểm khởi chạy Trợ lý Sư phạm Hoàng Thiên."""

from __future__ import annotations

import ctypes
import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from ui.main_window import MainWindow  # noqa: E402

APP_STYLE = """
QWidget {
    color: #0f172a;
    font-family: "Segoe UI";
    font-size: 13px;
    background: #f8fafc;
}
QMainWindow { background: #f8fafc; }
#sidebar { background: #0f172a; }
#brandLogo { background: transparent; }
#brand {
    background: transparent;
    color: #f8fafc;
    font-size: 18px;
    font-weight: 700;
}
#brandTag, #sideNote {
    background: transparent;
    color: #cbd5e1;
    font-size: 12px;
}
#navButton {
    background: transparent;
    color: #e2e8f0;
    text-align: left;
    padding: 10px 12px;
    border: none;
    border-radius: 8px;
}
#navButton:hover { background: #1e293b; }
#navButton:checked { background: #2563eb; color: #f8fafc; font-weight: 600; }
#pageTitle {
    background: transparent;
    font-size: 22px;
    font-weight: 700;
    color: #0f172a;
}
#pageHint { background: transparent; color: #475569; }
#card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
}
#fieldLabel { background: transparent; color: #1e293b; font-weight: 600; }
QLineEdit, QPlainTextEdit, QTextEdit, QComboBox, QSpinBox {
    background: #fff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 6px 8px;
    selection-background-color: #2563eb;
}
QScrollArea, QScrollArea > QWidget > QWidget { background: transparent; }
#statusHeader {
    background: #fff;
    border-bottom: 1px solid #e2e8f0;
}
#statusOk { background: transparent; color: #1d4ed8; font-weight: 700; }
#statusBad { background: transparent; color: #9f1239; font-weight: 700; }
#licenseOn { background: transparent; color: #d97706; font-weight: 700; }
#licenseOff { background: transparent; color: #b45309; font-weight: 700; }
#dashButton {
    text-align: left;
    padding: 16px;
    min-height: 72px;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
}
#dashButton:hover { background: #eff6ff; border-color: #d97706; }
#preview {
    background: #fff;
    border: 1px dashed #cbd5e1;
    border-radius: 8px;
    color: #475569;
}
QPushButton {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 8px 12px;
}
QPushButton:hover { background: #eff6ff; }
#primaryButton {
    background: #2563eb;
    color: white;
    border: none;
    font-weight: 600;
    padding: 10px 14px;
}
#primaryButton:hover { background: #1d4ed8; }
#primaryButton:disabled { background: #93c5fd; color: #f8fafc; }
#logPanel { background: #f8fafc; border-top: 1px solid #e2e8f0; }
#logTitle { background: transparent; font-weight: 700; color: #0f172a; }
#logStatus { background: transparent; color: #475569; }
#logView {
    background: #0f172a;
    color: #e7eef4;
    border-radius: 8px;
    font-family: Consolas, "Segoe UI";
    font-size: 12px;
}
#stopButton { background: #8c2f2f; color: white; border: none; }
#stopButton:disabled { background: #c9b4b4; color: #f7f4f4; }
QProgressBar {
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    background: #fff;
    text-align: center;
    height: 18px;
}
QProgressBar::chunk { background: #2563eb; border-radius: 5px; }
"""


def _set_app_user_model_id() -> None:
    if sys.platform != "win32":
        return
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("HoangThien.TroLySuPham.4.0")
    except (AttributeError, OSError):
        return


def main() -> int:
    _set_app_user_model_id()
    app = QApplication(sys.argv)
    app.setApplicationName("Trợ Lý Sư Phạm Hoàng Thiên")
    app.setStyle("Fusion")
    app.setStyleSheet(APP_STYLE)
    icon_path = APP_DIR / "assets" / "app_icon.ico"
    if icon_path.is_file():
        app.setWindowIcon(QIcon(str(icon_path)))
    window = MainWindow()
    if icon_path.is_file():
        window.setWindowIcon(QIcon(str(icon_path)))
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
