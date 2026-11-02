"""Phân hệ chuẩn hóa thể thức văn bản."""

from __future__ import annotations

from pathlib import Path

from core.prompt_builder import build_chuanhoa_prompt
from ui.kit import WorkTab


class ChuanHoaTab(WorkTab):
    def __init__(self, parent=None) -> None:
        super().__init__(
            "Chuẩn hoá văn bản",
            "Chọn file Word hoặc dán nội dung. Thể thức theo Nghị định 30/2020/NĐ-CP và văn bản Đảng.",
            "Chuan_hoa",
            "Chuẩn hoá",
            "Dán toàn văn cần chuẩn hóa thể thức. Ctrl+V cũng được.",
            "Word (*.docx);;Mọi tệp (*.*)",
            parent,
        )

    def finish(self) -> None:
        self._add_open_button("Mở file Word", lambda path: path.suffix.lower() == ".docx")

    def build_prompt(self, output_dir: Path) -> str:
        return build_chuanhoa_prompt(self.dual.text(), self.dual.files(), output_dir)

    def show_result(self, path: str) -> None:
        super().show_result(path)
        self._refresh_open_button()
