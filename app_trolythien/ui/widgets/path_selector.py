"""Ô nhập đường dẫn kèm nút chọn tệp hoặc chọn thư mục."""

from __future__ import annotations

from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget


class PathSelector(QWidget):
    def __init__(self, mode: str = "dir", title: str = "Đường dẫn", default: str = "", parent=None) -> None:
        super().__init__(parent)
        self.mode = mode
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(6)
        label = QLabel(title)
        label.setObjectName("fieldLabel")
        root.addWidget(label)
        row = QHBoxLayout()
        self.edit = QLineEdit(default)
        if mode == "dir":
            self.edit.setPlaceholderText("Thư mục lưu kết quả")
            button = QPushButton("Chọn thư mục…")
            button.clicked.connect(self._pick_dir)
        else:
            self.edit.setPlaceholderText("Đường dẫn tệp")
            button = QPushButton("Chọn tệp…")
            button.clicked.connect(self._pick_file)
        row.addWidget(self.edit, 1)
        row.addWidget(button)
        root.addLayout(row)

    def path(self) -> str:
        return self.edit.text().strip()

    def set_path(self, value: str) -> None:
        self.edit.setText(value)

    def _pick_dir(self) -> None:
        start = self.path()
        chosen = QFileDialog.getExistingDirectory(self, "Chọn thư mục", start)
        if chosen:
            self.edit.setText(chosen)

    def _pick_file(self) -> None:
        chosen, _ = QFileDialog.getOpenFileName(self, "Chọn tệp", self.path())
        if chosen:
            self.edit.setText(chosen)
