"""Phân hệ báo cáo chuyên môn, biên bản họp tổ và kế hoạch hoạt động."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QComboBox, QLineEdit, QVBoxLayout

from core.prompt_builder import build_baocao_prompt
from ui.kit import WorkTab, field_label


class BaoCaoTab(WorkTab):
    def __init__(self, parent=None) -> None:
        super().__init__(
            "Báo cáo, biên bản & kế hoạch tổ",
            "Biên bản họp tổ Toán - Tin (3 phần chuẩn), Kế hoạch hoạt động tháng theo form THCS Trần Phú, Báo cáo theo NĐ 30, hoặc Sáng kiến kinh nghiệm.",
            "Bao_cao",
            "Soạn văn bản",
            "Dán văn bản triển khai, định hướng công tác tới, dàn ý, số liệu hoặc phân công... Ctrl+V cũng được.",
            "Minh chứng (*.docx *.pdf *.xlsx *.txt *.md *.png);;Mọi tệp (*.*)",
            parent,
        )

    def populate(self, layout: QVBoxLayout) -> None:
        self.loai = QComboBox()
        self.loai.addItems([
            "Biên bản họp tổ Toán - Tin",
            "Kế hoạch hoạt động tổ theo tháng",
            "Báo cáo chuyên môn",
            "Sáng kiến kinh nghiệm",
        ])
        layout.addWidget(field_label("Loại văn bản"))
        layout.addWidget(self.loai)

        self.tieu_de = QLineEdit()
        self.don_vi = QLineEdit()
        self.thoi_diem = QLineEdit()

        for label, widget in (
            ("Tiêu đề", self.tieu_de),
            ("Đơn vị", self.don_vi),
            ("Thời điểm", self.thoi_diem),
        ):
            layout.addWidget(field_label(label))
            layout.addWidget(widget)

        self.loai.currentTextChanged.connect(self._on_loai_changed)
        self._on_loai_changed(self.loai.currentText())

    def _on_loai_changed(self, text: str) -> None:
        kind = (text or "").lower()
        if "biên bản" in kind:
            self.tieu_de.setPlaceholderText("Biên bản họp tổ chuyên môn lần 1 tháng 10/2026")
            if not self.don_vi.text().strip():
                self.don_vi.setText("Trường THCS Trần Phú - Tổ Toán - Tin học")
            if not self.thoi_diem.text().strip():
                self.thoi_diem.setText("Tháng 10/2026 - Năm học 2026 - 2027")
        elif "kế hoạch" in kind or "tháng" in kind:
            self.tieu_de.setPlaceholderText("Báo cáo và Kế hoạch hoạt động tổ Toán – Tin học tháng 10/2026")
            if not self.don_vi.text().strip():
                self.don_vi.setText("Trường THCS Trần Phú - Tổ Toán - Tin học")
            if not self.thoi_diem.text().strip():
                self.thoi_diem.setText("Tháng 10/2026 - Năm học 2026 - 2027")
        elif "sáng kiến" in kind:
            self.tieu_de.setPlaceholderText("Tên sáng kiến kinh nghiệm (VD: Ứng dụng AI trong giảng dạy Toán...)")
            if not self.don_vi.text().strip():
                self.don_vi.setText("Trường THCS Trần Phú")
            if not self.thoi_diem.text().strip():
                self.thoi_diem.setText("Năm học 2026 - 2027")
        else:
            self.tieu_de.setPlaceholderText("Tiêu đề báo cáo chuyên môn theo Nghị định 30")
            if not self.don_vi.text().strip():
                self.don_vi.setText("Trường THCS Trần Phú - Tổ Toán - Tin học")
            if not self.thoi_diem.text().strip():
                self.thoi_diem.setText("Tháng 10/2026")

    def set_mode(self, mode: str) -> None:
        target = "Báo cáo chuyên môn"
        lower = (mode or "").lower()
        if "biên bản" in lower or "bien ban" in lower or "họp tổ" in lower:
            target = "Biên bản họp tổ Toán - Tin"
        elif "kế hoạch" in lower or "ke hoach" in lower or "tháng" in lower:
            target = "Kế hoạch hoạt động tổ theo tháng"
        elif "sáng kiến" in lower or "sang kien" in lower:
            target = "Sáng kiến kinh nghiệm"
        index = self.loai.findText(target)
        if index >= 0:
            self.loai.setCurrentIndex(index)

    def validate(self) -> str | None:
        if not self.tieu_de.text().strip() and not self.dual.text().strip() and not self.dual.files():
            return "Nhập tiêu đề, hoặc dán nội dung, hoặc chọn tệp minh chứng/văn bản căn cứ."
        if not self.output.path():
            return "Chọn thư mục lưu kết quả."
        return None

    def build_prompt(self, output_dir: Path) -> str:
        return build_baocao_prompt(
            self.loai.currentText(),
            self.tieu_de.text().strip(),
            self.don_vi.text().strip(),
            self.thoi_diem.text().strip(),
            self.dual.text(),
            self.dual.files(),
            output_dir,
        )
