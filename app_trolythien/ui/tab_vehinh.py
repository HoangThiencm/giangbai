"""Phân hệ vẽ hình: dán đề hoặc ảnh, xuất một PNG 300 DPI."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QVBoxLayout

from core.geometry_engine import ensure_png_300dpi
from core.prompt_builder import build_vehinh_prompt
from ui.kit import WorkTab, field_label


class VeHinhTab(WorkTab):
    def __init__(self, parent=None) -> None:
        super().__init__(
            "Vẽ hình học",
            "Dán đề bài hoặc ảnh đề (Ctrl+V). Một nút Vẽ hình xuất đúng một ảnh PNG 300 DPI.",
            "Ve_hinh",
            "Vẽ hình",
            "Dán đề bài hình học. Ctrl+V dán chữ hoặc ảnh chụp đề. Ghi đủ số đo.",
            "Đề và ảnh (*.png *.jpg *.jpeg *.svg *.pdf *.txt *.docx);;Mọi tệp (*.*)",
            parent,
        )
        self.dual.editor.setMinimumHeight(200)

    def populate(self, layout: QVBoxLayout) -> None:
        return

    def finish(self) -> None:
        self.preview = QLabel("Chưa có ảnh. Dán đề hoặc ảnh, rồi bấm Vẽ hình.")
        self.preview.setObjectName("preview")
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview.setMinimumHeight(220)
        self.preview.setWordWrap(True)
        self.form_layout.addWidget(field_label("Xem trước"))
        self.form_layout.addWidget(self.preview)
        self.dual.image_attached.connect(self.show_source_image)

    def build_prompt(self, output_dir: Path) -> str:
        return build_vehinh_prompt(self.dual.text(), self.dual.files(), output_dir)

    def show_source_image(self, path: str) -> None:
        self._show_pixmap(Path(path), "Không mở được ảnh đề bài.")

    def show_result(self, path: str) -> None:
        super().show_result(path)
        image = _find_png(Path(path))
        if image is None:
            self.preview.setText("Chưa thấy ảnh PNG trong kết quả.")
            self.preview.setPixmap(QPixmap())
            return
        try:
            ensure_png_300dpi(image)
        except OSError:
            pass
        self._show_pixmap(image, f"Không mở được ảnh {image.name}")

    def _show_pixmap(self, image: Path, fail_text: str) -> None:
        pixmap = QPixmap(str(image))
        if pixmap.isNull():
            self.preview.setPixmap(QPixmap())
            self.preview.setText(fail_text)
            return
        scaled = pixmap.scaled(
            640,
            320,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.preview.setPixmap(scaled)
        self.preview.setText("")


def _find_png(path: Path) -> Path | None:
    if path.is_file() and path.suffix.lower() == ".png":
        return path
    folder = path if path.is_dir() else path.parent
    if not folder.is_dir():
        return None
    images = [item for item in folder.iterdir() if item.is_file() and item.suffix.lower() == ".png"]
    if not images:
        return None
    if path.is_file():
        stem = path.stem.lower()
        same = [item for item in images if item.stem.lower().startswith(stem) or stem.startswith(item.stem.lower())]
        if same:
            images = same
    return max(images, key=lambda item: item.stat().st_mtime)
