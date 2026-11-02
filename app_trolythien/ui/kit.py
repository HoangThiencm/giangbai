"""Mảnh giao diện dùng lại giữa các phân hệ."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QMimeData, QUrl, Signal
from PySide6.QtGui import QDesktopServices, QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.preflight import writable_dir
from core.prompt_builder import default_output_dir, document_files
from ui.widgets.path_selector import PathSelector

IMAGE_PASTE_EXT = {".png", ".jpg", ".jpeg", ".svg", ".webp"}


def page_header(title: str, hint: str) -> QWidget:
    box = QWidget()
    layout = QVBoxLayout(box)
    layout.setContentsMargins(0, 0, 0, 8)
    layout.setSpacing(4)
    heading = QLabel(title)
    heading.setObjectName("pageTitle")
    sub = QLabel(hint)
    sub.setObjectName("pageHint")
    sub.setWordWrap(True)
    layout.addWidget(heading)
    layout.addWidget(sub)
    return box


def card() -> tuple[QFrame, QVBoxLayout]:
    frame = QFrame()
    frame.setObjectName("card")
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(16, 16, 16, 16)
    layout.setSpacing(8)
    return frame, layout


def field_label(text: str) -> QLabel:
    label = QLabel(text)
    label.setObjectName("fieldLabel")
    return label


class PasteAwareEdit(QTextEdit):
    """Ctrl+V: chữ thì dán chữ, ảnh chụp màn hình thì giao cho DualInput lưu file."""

    def __init__(self, owner: DualInput) -> None:
        super().__init__()
        self._owner = owner

    def insertFromMimeData(self, source: QMimeData) -> None:  # noqa: N802
        if source is not None and source.hasImage():
            self._owner.save_image(source.imageData())
            return
        super().insertFromMimeData(source)


class DualInput(QWidget):
    """Ô dán chữ hoặc ảnh, chọn nhiều tệp, hoặc chọn cả thư mục."""

    image_attached = Signal(str)

    def __init__(self, placeholder: str, file_filter: str, parent=None) -> None:
        super().__init__(parent)
        self.file_filter = file_filter
        self.attached_items: list[str] = []
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(6)
        root.addWidget(field_label("Đầu vào"))
        self.editor = PasteAwareEdit(self)
        self.editor.setAcceptRichText(False)
        self.editor.setPlaceholderText(placeholder)
        self.editor.setMinimumHeight(140)
        root.addWidget(self.editor)

        row = QHBoxLayout()
        paste = QPushButton("Dán từ Clipboard")
        paste.clicked.connect(self.paste_clipboard)
        browse = QPushButton("Chọn tệp…")
        browse.clicked.connect(self.browse)
        browse_folder = QPushButton("Chọn cả thư mục…")
        browse_folder.clicked.connect(self.browse_folder)
        clear = QPushButton("Bỏ tệp")
        clear.clicked.connect(self.clear_file)
        row.addWidget(paste)
        row.addWidget(browse)
        row.addWidget(browse_folder)
        row.addWidget(clear)
        row.addStretch(1)
        self.file_label = QLabel("Chưa chọn tệp")
        self.file_label.setObjectName("pageHint")
        self.file_label.setWordWrap(True)
        root.addLayout(row)
        root.addWidget(self.file_label)

    def text(self) -> str:
        return self.editor.toPlainText()

    def files(self) -> list[str]:
        return list(self.attached_items)

    def paste_clipboard(self) -> None:
        mime = QApplication.clipboard().mimeData()
        if mime is None:
            return
        if mime.hasImage():
            image = QApplication.clipboard().image()
            self.save_image(image)
            return
        if mime.hasText() and mime.text():
            self.editor.insertPlainText(mime.text())

    def save_image(self, image) -> None:
        picture = _as_qimage(image)
        if picture.isNull():
            return
        folder = writable_dir() / ".runtime" / "clipboard_images"
        folder.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        path = folder / f"clip_{stamp}.png"
        if not picture.save(str(path), "PNG"):
            return
        self.set_attached([str(path)])

    def browse(self) -> None:
        paths, _ = QFileDialog.getOpenFileNames(self, "Chọn tệp nguồn", "", self.file_filter)
        if paths:
            self.set_attached(list(paths))

    def browse_folder(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Chọn thư mục hồ sơ", "")
        if path:
            self.set_attached([path])

    def set_attached(self, items: list[str]) -> None:
        self.attached_items = [item for item in items if item]
        self._refresh_label()
        for item in self.attached_items:
            path = Path(item)
            if path.is_file() and path.suffix.lower() in IMAGE_PASTE_EXT:
                self.image_attached.emit(str(path.resolve()))
                return

    def clear_file(self) -> None:
        self.attached_items = []
        self.file_label.setText("Chưa chọn tệp")

    def _refresh_label(self) -> None:
        items = self.attached_items
        if not items:
            self.file_label.setText("Chưa chọn tệp")
            return
        if len(items) == 1 and Path(items[0]).is_dir():
            folder = Path(items[0])
            count = len(document_files(folder))
            self.file_label.setText(f"Đã chọn thư mục: {folder.name} ({count} tệp)")
            return
        if len(items) == 1:
            self.file_label.setText(f"Đã chọn 1 tệp: {Path(items[0]).name}")
            return
        self.file_label.setText(f"Đã chọn {len(items)} tệp")


def _as_qimage(image) -> QImage:
    if isinstance(image, QImage):
        return image
    if isinstance(image, QPixmap):
        return image.toImage()
    return QImage()


class WorkTab(QWidget):
    """Khung chung: form riêng, đầu vào kép, thư mục lưu, nút chạy."""

    request_run = Signal(str, str)

    def __init__(
        self,
        title: str,
        hint: str,
        output_slug: str,
        run_label: str,
        placeholder: str,
        file_filter: str,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._result_path = ""
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        host = QWidget()
        root = QVBoxLayout(host)
        root.setContentsMargins(20, 18, 20, 12)
        root.addWidget(page_header(title, hint))
        frame, layout = card()
        self.form_layout = layout
        self.populate(layout)
        self.dual = DualInput(placeholder, file_filter)
        layout.addWidget(self.dual)
        self.output = PathSelector(
            mode="dir",
            title="Thư mục lưu kết quả",
            default=str(default_output_dir(output_slug)),
        )
        layout.addWidget(self.output)
        self.extra_row = QHBoxLayout()
        layout.addLayout(self.extra_row)
        self.run_button = QPushButton(run_label)
        self.run_button.setObjectName("primaryButton")
        self.run_button.clicked.connect(self._submit)
        layout.addWidget(self.run_button)
        self.finish()
        root.addWidget(frame)
        root.addStretch(1)
        scroll.setWidget(host)
        outer.addWidget(scroll)

    def populate(self, layout: QVBoxLayout) -> None:
        """Các ô tham số riêng của phân hệ."""

    def finish(self) -> None:
        """Nút phụ sau khi khung đầu vào và đầu ra đã có."""

    def validate(self) -> str | None:
        if not self.dual.text().strip() and not self.dual.files():
            return "Dán nội dung hoặc chọn một tệp nguồn."
        if not self.output.path():
            return "Chọn thư mục lưu kết quả."
        return None

    def build_prompt(self, output_dir: Path) -> str:
        raise NotImplementedError

    def output_dir(self) -> str:
        return self.output.path()

    def show_result(self, path: str) -> None:
        self._result_path = path

    def _submit(self) -> None:
        error = self.validate()
        if error:
            QMessageBox.warning(self, "Thiếu thông tin", error)
            return
        folder = Path(self.output.path())
        self.request_run.emit(self.build_prompt(folder), str(folder))

    def _add_open_button(self, label: str, predicate) -> QPushButton:
        button = QPushButton(label)
        button.setEnabled(False)

        def open_current() -> None:
            path = Path(self._result_path)
            if path.is_file() and predicate(path):
                QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))

        button.clicked.connect(open_current)
        self.extra_row.addWidget(button)
        self._open_button = button
        self._open_predicate = predicate
        return button

    def _refresh_open_button(self) -> None:
        button = getattr(self, "_open_button", None)
        predicate = getattr(self, "_open_predicate", None)
        if button is None or predicate is None:
            return
        path = Path(self._result_path) if self._result_path else None
        button.setEnabled(bool(path and path.is_file() and predicate(path)))
