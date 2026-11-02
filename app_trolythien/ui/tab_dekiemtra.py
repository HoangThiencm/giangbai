"""Phân hệ đề kiểm tra: Công văn 7991, đề thường, và trộn mã đề."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from core.prompt_builder import (
    build_de_cv7991_prompt,
    build_de_thuong_prompt,
    build_tron_de_prompt,
)
from ui.kit import WorkTab, field_label

MODE_7991 = "1. Đề kiểm tra theo CV 7991 (từ Ma trận & Bảng đặc tả)"
MODE_THUONG = "2. Đề kiểm tra thông thường (từ Ma trận & Bảng đặc tả)"
MODE_TRON = "3. Trộn đề kiểm tra (Đa mã đề + Đáp án tổng hợp)"
MODE_TRON_NOTE = (
    "Tự động nhận diện: Đề thuần chữ (trộn nhanh) hoặc Đề có công thức "
    "(chuẩn hóa LaTeX -> chuyển đổi thành Word Equation)."
)


class DeKiemTraTab(WorkTab):
    def __init__(self, parent=None) -> None:
        super().__init__(
            "Đề kiểm tra",
            "Soạn đề từ ma trận, bảng đặc tả, hoặc trộn nhiều mã đề từ một đề gốc.",
            "De_kiem_tra",
            "Tạo đề",
            "Dán ma trận và bảng đặc tả. Có thể chọn file Word, PDF, Excel hoặc Markdown.",
            "Nguồn (*.docx *.pdf *.xlsx *.md);;Mọi tệp (*.*)",
            parent,
        )

    def populate(self, layout: QVBoxLayout) -> None:
        self.mode = QComboBox()
        self.mode.addItems([MODE_7991, MODE_THUONG, MODE_TRON])
        self.mode.currentIndexChanged.connect(self._sync_mode)
        layout.addWidget(field_label("Chế độ làm việc"))
        layout.addWidget(self.mode)
        self.mode_note = QLabel("")
        self.mode_note.setObjectName("pageHint")
        self.mode_note.setWordWrap(True)
        layout.addWidget(self.mode_note)

        self.exam_box = QWidget()
        exam_row = QHBoxLayout(self.exam_box)
        exam_row.setContentsMargins(0, 0, 0, 0)
        self.mon = QComboBox()
        self.mon.addItems(
            [
                "Toán",
                "Khoa học tự nhiên",
                "Ngữ văn",
                "Vật lí",
                "Hóa học",
                "Sinh học",
                "Lịch sử",
                "Địa lí",
                "Tin học",
                "Tiếng Anh",
                "GDCD",
            ]
        )
        self.lop = QComboBox()
        self.lop.addItems([f"Lớp {grade}" for grade in range(6, 13)])
        self.thoi_gian = QComboBox()
        self.thoi_gian.addItems(["45 phút", "60 phút", "90 phút"])
        self.ti_le = QComboBox()
        self.ti_le.addItems(
            [
                "100% trắc nghiệm",
                "70% trắc nghiệm / 30% tự luận",
                "50% trắc nghiệm / 50% tự luận",
                "30% trắc nghiệm / 70% tự luận",
                "100% tự luận",
            ]
        )
        for label, widget in (
            ("Môn học", self.mon),
            ("Khối lớp", self.lop),
            ("Thời gian làm bài", self.thoi_gian),
            ("Tỉ lệ trắc nghiệm/tự luận", self.ti_le),
        ):
            column = QVBoxLayout()
            caption = field_label(label)
            column.addWidget(caption)
            column.addWidget(widget)
            exam_row.addLayout(column)
        layout.addWidget(self.exam_box)

        self.mix_box = QWidget()
        mix_row = QHBoxLayout(self.mix_box)
        mix_row.setContentsMargins(0, 0, 0, 0)
        self.so_ma_de = QComboBox()
        self.so_ma_de.addItems(["2", "4", "6", "8"])
        self.so_ma_de.setCurrentText("4")
        self.ma_bat_dau = QComboBox()
        self.ma_bat_dau.setEditable(True)
        self.ma_bat_dau.addItems(["101", "201", "301", "401"])
        for label, widget in (
            ("Số lượng mã đề", self.so_ma_de),
            ("Tiền tố mã đề", self.ma_bat_dau),
        ):
            column = QVBoxLayout()
            column.addWidget(field_label(label))
            column.addWidget(widget)
            mix_row.addLayout(column)
        mix_row.addStretch(1)
        layout.addWidget(self.mix_box)
        self.mix_box.setVisible(False)

    def finish(self) -> None:
        self._sync_mode()

    def _sync_mode(self) -> None:
        mixing = self.mode.currentIndex() == 2
        self.exam_box.setVisible(not mixing)
        self.mix_box.setVisible(mixing)
        if mixing:
            self.run_button.setText("Trộn đề")
            self.mode_note.setText(MODE_TRON_NOTE)
            self.mode_note.setVisible(True)
            self.dual.editor.setPlaceholderText("Dán đề gốc kèm đáp án. " + MODE_TRON_NOTE)
            return
        self.run_button.setText("Tạo đề")
        self.mode_note.clear()
        self.mode_note.setVisible(False)
        self.dual.editor.setPlaceholderText(
            "Dán ma trận và bảng đặc tả. Có thể chọn file Word, PDF, Excel hoặc Markdown."
        )

    def build_prompt(self, output_dir: Path) -> str:
        pasted = self.dual.text()
        files = self.dual.files()
        if self.mode.currentIndex() == 2:
            return build_tron_de_prompt(
                self.so_ma_de.currentText(),
                self.ma_bat_dau.currentText(),
                pasted,
                files,
                output_dir,
            )
        if self.mode.currentIndex() == 1:
            return build_de_thuong_prompt(
                self.mon.currentText(),
                self.lop.currentText(),
                self.thoi_gian.currentText(),
                self.ti_le.currentText(),
                pasted,
                files,
                output_dir,
            )
        return build_de_cv7991_prompt(
            self.mon.currentText(),
            self.lop.currentText(),
            self.thoi_gian.currentText(),
            pasted,
            files,
            output_dir,
            self.ti_le.currentText(),
        )
