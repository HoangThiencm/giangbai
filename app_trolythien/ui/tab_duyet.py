"""Phân hệ duyệt giáo án và duyệt đề."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLineEdit, QVBoxLayout

from core.prompt_builder import build_duyet_prompt
from ui.kit import WorkTab, field_label


class DuyetTab(WorkTab):
    def __init__(self, parent=None) -> None:
        super().__init__(
            "Duyệt giáo án và duyệt đề",
            "Chọn loại hồ sơ, dán nhận xét hoặc chọn file giáo án, đề, đáp án.",
            "Duyet",
            "Duyệt hồ sơ",
            "Dán ghi chú duyệt, hoặc để trống nếu hồ sơ nằm trong tệp đã chọn.",
            "Hồ sơ (*.docx *.pdf *.md *.txt);;Mọi tệp (*.*)",
            parent,
        )

    def populate(self, layout: QVBoxLayout) -> None:
        row = QHBoxLayout()
        self.loai = QComboBox()
        self.loai.addItems(["Duyệt giáo án", "Duyệt đề"])
        self.thang = QLineEdit()
        self.thang.setPlaceholderText("Ví dụ: 9")
        self.to_cm = QLineEdit()
        self.to_cm.setPlaceholderText("Ví dụ: Tổ Toán")
        for label, widget in (("Loại việc", self.loai), ("Tháng", self.thang), ("Tổ chuyên môn", self.to_cm)):
            column = QVBoxLayout()
            column.addWidget(field_label(label))
            column.addWidget(widget)
            row.addLayout(column)
        layout.addLayout(row)

    def set_mode(self, mode: str) -> None:
        target = "Duyệt đề" if "đề" in mode.lower() else "Duyệt giáo án"
        index = self.loai.findText(target)
        if index >= 0:
            self.loai.setCurrentIndex(index)

    def validate(self) -> str | None:
        if not self.dual.text().strip() and not self.dual.files():
            return "Dán nội dung hồ sơ hoặc chọn tệp giáo án, đề."
        if not self.output.path():
            return "Chọn thư mục lưu kết quả."
        return None

    def build_prompt(self, output_dir: Path) -> str:
        return build_duyet_prompt(
            self.loai.currentText(),
            self.thang.text().strip(),
            self.to_cm.text().strip(),
            self.dual.text(),
            self.dual.files(),
            output_dir,
        )
