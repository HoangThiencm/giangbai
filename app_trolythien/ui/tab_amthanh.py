"""Phân hệ chuyển ghi âm thành văn bản."""

from __future__ import annotations

from pathlib import Path

from core.prompt_builder import build_amthanh_prompt
from ui.kit import WorkTab

AUDIO = (".m4a", ".mp3", ".wav", ".aac", ".mp4", ".ogg")


class AmThanhTab(WorkTab):
    def __init__(self, parent=None) -> None:
        super().__init__(
            "Chuyển ghi âm",
            "Chọn file ghi âm. Có thể dán thêm tên người nói và bối cảnh cuộc họp.",
            "Ghi_am",
            "Chuyển chữ",
            "Dán bối cảnh: ai nói, cuộc họp nào, từ ngữ chuyên môn cần giữ.",
            "Âm thanh (*.m4a *.mp3 *.wav *.aac *.mp4 *.ogg);;Mọi tệp (*.*)",
            parent,
        )

    def validate(self) -> str | None:
        files = self.dual.files()
        if not files:
            return "Chọn một file ghi âm."
        if Path(files[0]).suffix.lower() not in AUDIO:
            return "Tệp đã chọn không phải định dạng ghi âm hỗ trợ."
        if not self.output.path():
            return "Chọn thư mục lưu kết quả."
        return None

    def build_prompt(self, output_dir: Path) -> str:
        return build_amthanh_prompt(self.dual.text(), self.dual.files(), output_dir)
