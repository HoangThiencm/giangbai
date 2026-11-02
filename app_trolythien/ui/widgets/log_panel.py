"""Khung log thời gian thực, phần trăm và nút mở kết quả."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class LogPanel(QWidget):
    open_folder_clicked = Signal()
    open_result_clicked = Signal()
    stop_clicked = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("logPanel")
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 8, 12, 10)
        root.setSpacing(6)

        header = QHBoxLayout()
        title = QLabel("Tiến trình")
        title.setObjectName("logTitle")
        self.status = QLabel("Sẵn sàng")
        self.status.setObjectName("logStatus")
        header.addWidget(title)
        header.addStretch(1)
        header.addWidget(self.status)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setFormat("%p%")

        self.log = QPlainTextEdit()
        self.log.setObjectName("logView")
        self.log.setReadOnly(True)
        self.log.setMaximumBlockCount(1000)
        self.log.setPlaceholderText("Nhật ký agy hiện ở đây khi chạy.")
        self.log.setMinimumHeight(120)
        self.log.setMaximumHeight(180)

        buttons = QHBoxLayout()
        self.stop_button = QPushButton("Dừng")
        self.stop_button.setObjectName("stopButton")
        self.stop_button.setEnabled(False)
        self.open_result_button = QPushButton("Mở tệp kết quả")
        self.open_result_button.setEnabled(False)
        self.open_folder_button = QPushButton("Mở thư mục chứa")
        self.clear_button = QPushButton("Xóa log")
        buttons.addWidget(self.stop_button)
        buttons.addWidget(self.open_result_button)
        buttons.addWidget(self.open_folder_button)
        buttons.addStretch(1)
        buttons.addWidget(self.clear_button)

        root.addLayout(header)
        root.addWidget(self.progress)
        root.addWidget(self.log)
        root.addLayout(buttons)

        self.stop_button.clicked.connect(self.stop_clicked.emit)
        self.open_result_button.clicked.connect(self.open_result_clicked.emit)
        self.open_folder_button.clicked.connect(self.open_folder_clicked.emit)
        self.clear_button.clicked.connect(self.log.clear)

    def append_log(self, text: str) -> None:
        self.log.appendPlainText(text)
        bar = self.log.verticalScrollBar()
        bar.setValue(bar.maximum())

    def set_progress(self, value: int) -> None:
        self.progress.setValue(max(0, min(100, int(value))))

    def set_busy(self, busy: bool) -> None:
        self.stop_button.setEnabled(busy)
        if busy:
            self.status.setText("Đang chạy ngầm…")

    def set_status(self, text: str) -> None:
        self.status.setText(text)

    def set_result_ready(self, ready: bool) -> None:
        self.open_result_button.setEnabled(ready)
