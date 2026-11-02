"""Phân hệ tạo bài tập và đề thi."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QComboBox, QHBoxLayout, QSpinBox, QVBoxLayout

from core.prompt_builder import build_baitap_prompt
from ui.kit import WorkTab, field_label


class BaiTapTab(WorkTab):
    def __init__(self, parent=None) -> None:
        super().__init__(
            "Tạo bài tập và đề thi",
            "Trắc nghiệm, tự luận, hoặc ma trận Công văn 7991. Dán đề nguồn hoặc chọn file.",
            "Bai_tap",
            "Tạo đề",
            "Dán bài học, mạch kiến thức, hoặc đề mẫu. Ctrl+V cũng được.",
            "Nguồn (*.pdf *.docx *.txt *.md);;Mọi tệp (*.*)",
            parent,
        )

    def populate(self, layout: QVBoxLayout) -> None:
        row = QHBoxLayout()
        self.hinh_thuc = QComboBox()
        self.hinh_thuc.addItems(["Trắc nghiệm", "Tự luận", "Công văn 7991"])
        self.muc_do = QComboBox()
        self.muc_do.addItems(["Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao", "Trộn bốn mức"])
        self.so_cau = QSpinBox()
        self.so_cau.setRange(1, 50)
        self.so_cau.setValue(10)
        for label, widget in (
            ("Hình thức", self.hinh_thuc),
            ("Mức độ", self.muc_do),
            ("Số câu", self.so_cau),
        ):
            column = QVBoxLayout()
            column.addWidget(field_label(label))
            column.addWidget(widget)
            row.addLayout(column)
        layout.addLayout(row)

    def build_prompt(self, output_dir: Path) -> str:
        return build_baitap_prompt(
            self.so_cau.value(),
            self.hinh_thuc.currentText(),
            self.muc_do.currentText(),
            self.dual.text(),
            self.dual.files(),
            output_dir,
        )
