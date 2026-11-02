"""Phân hệ bài giảng HTML 16:9."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLineEdit, QSpinBox, QVBoxLayout

from core.prompt_builder import build_baigiang_prompt
from ui.kit import WorkTab, field_label


class BaiGiangTab(WorkTab):
    def __init__(self, parent=None) -> None:
        super().__init__(
            "Bài giảng HTML",
            "Chọn môn, lớp, số tiết và PDF sách giáo khoa. File HTML mở được trên trình duyệt.",
            "Bai_giang_HTML",
            "Tạo bài giảng",
            "Dán thêm yêu cầu tiết dạy nếu PDF chưa đủ. Ctrl+V cũng được.",
            "PDF sách (*.pdf);;Mọi tệp (*.*)",
            parent,
        )

    def populate(self, layout: QVBoxLayout) -> None:
        row = QHBoxLayout()
        self.mon = QComboBox()
        self.mon.addItems(["Toán", "Tin học", "Khoa học tự nhiên", "Ngữ văn", "Lịch sử và Địa lý"])
        self.lop = QComboBox()
        self.lop.addItems(["6", "7", "8", "9"])
        self.so_tiet = QSpinBox()
        self.so_tiet.setRange(1, 6)
        self.so_tiet.setValue(1)
        for label, widget in (("Môn", self.mon), ("Lớp", self.lop), ("Số tiết", self.so_tiet)):
            column = QVBoxLayout()
            column.addWidget(field_label(label))
            column.addWidget(widget)
            row.addLayout(column)
        layout.addLayout(row)
        self.ten_bai = QLineEdit()
        self.ten_bai.setPlaceholderText("Tên bài, nếu muốn ghi đè tên đọc từ PDF")
        layout.addWidget(field_label("Tên bài"))
        layout.addWidget(self.ten_bai)

    def finish(self) -> None:
        self._add_open_button("Mở bài giảng trên trình duyệt", lambda path: path.suffix.lower() == ".html")

    def validate(self) -> str | None:
        pdfs = [item for item in self.dual.files() if item.lower().endswith(".pdf")]
        if not pdfs and not self.dual.text().strip():
            return "Chọn file PDF sách hoặc dán nội dung bài."
        if not self.output.path():
            return "Chọn thư mục lưu kết quả."
        return None

    def build_prompt(self, output_dir: Path) -> str:
        return build_baigiang_prompt(
            self.mon.currentText(),
            self.lop.currentText(),
            self.so_tiet.value(),
            self.ten_bai.text().strip(),
            self.dual.text(),
            self.dual.files(),
            output_dir,
        )

    def show_result(self, path: str) -> None:
        super().show_result(path)
        self._refresh_open_button()
