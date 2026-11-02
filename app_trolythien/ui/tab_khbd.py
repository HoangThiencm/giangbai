"""Phân hệ soạn kế hoạch bài dạy theo Công văn 5512."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLineEdit, QSpinBox, QVBoxLayout

from core.prompt_builder import build_khbd_prompt
from ui.kit import WorkTab, field_label


class KhbdTab(WorkTab):
    def __init__(self, parent=None) -> None:
        super().__init__(
            "Soạn KHBD",
            "Toán 6, 7, 8, 9 theo Công văn 5512. Dán yêu cầu hoặc chọn học liệu, rồi chọn thư mục lưu.",
            "KHBD",
            "Soạn bài",
            "Dán tên bài, yêu cầu cần đạt, hoặc ghi chú tiết dạy. Ctrl+V cũng được.",
            "Học liệu (*.pdf *.docx *.png *.jpg *.txt *.md);;Mọi tệp (*.*)",
            parent,
        )

    def populate(self, layout: QVBoxLayout) -> None:
        row = QHBoxLayout()
        self.mon = QComboBox()
        self.mon.addItems(["Toán", "Tin học", "Khoa học tự nhiên", "Ngữ văn", "Lịch sử và Địa lý"])
        self.lop = QComboBox()
        self.lop.addItems(["6", "7", "8", "9"])
        self.so_tiet = QSpinBox()
        self.so_tiet.setRange(1, 8)
        self.so_tiet.setValue(1)
        self.bo_sach = QComboBox()
        self.bo_sach.addItems(["Kết nối tri thức", "Cánh diều", "Chân trời sáng tạo"])
        for label, widget in (
            ("Môn", self.mon),
            ("Lớp", self.lop),
            ("Số tiết", self.so_tiet),
            ("Bộ sách", self.bo_sach),
        ):
            column = QVBoxLayout()
            column.addWidget(field_label(label))
            column.addWidget(widget)
            row.addLayout(column)
        layout.addLayout(row)
        self.ten_bai = QLineEdit()
        self.ten_bai.setPlaceholderText("Ví dụ: Phương trình tích")
        layout.addWidget(field_label("Tên bài"))
        layout.addWidget(self.ten_bai)

    def validate(self) -> str | None:
        if not self.ten_bai.text().strip() and not self.dual.text().strip() and not self.dual.files():
            return "Nhập tên bài, hoặc dán đề, hoặc chọn tệp học liệu."
        if not self.output.path():
            return "Chọn thư mục lưu kết quả."
        return None

    def build_prompt(self, output_dir: Path) -> str:
        return build_khbd_prompt(
            self.mon.currentText(),
            self.lop.currentText(),
            self.ten_bai.text().strip(),
            self.so_tiet.value(),
            self.bo_sach.currentText(),
            self.dual.text(),
            self.dual.files(),
            output_dir,
        )
