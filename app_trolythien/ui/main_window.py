"""Cửa sổ chính: kiểm tra agy, sidebar và mười phân hệ trên bảng điều khiển."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QThread, QTimer, QUrl, Qt, Signal
from PySide6.QtGui import QDesktopServices, QPixmap
from PySide6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from core.bridge import AntigravityWorker
from core.license import is_licensed
from core.preflight import app_dir, check_agy_installed, check_agy_login, fetch_available_models
from core.prompt_builder import knowledge_ready
from ui.license_dialog import LicenseDialog
from ui.setup_dialog import SetupDialog
from ui.tab_amthanh import AmThanhTab
from ui.tab_baigiang import BaiGiangTab
from ui.tab_baocao import BaoCaoTab
from ui.tab_baitap import BaiTapTab
from ui.tab_chuanhoa import ChuanHoaTab
from ui.tab_dekiemtra import DeKiemTraTab
from ui.tab_duyet import DuyetTab
from ui.tab_khbd import KhbdTab
from ui.tab_vehinh import VeHinhTab
from ui.widgets.log_panel import LogPanel


class PreflightThread(QThread):
    """installed, logged_in, default_model, [(model_id, tên hiển thị), ...]."""

    done = Signal(bool, bool, str, object)

    def run(self) -> None:
        installed, info = check_agy_installed()
        if not installed:
            self.done.emit(False, False, info, fetch_available_models())
            return
        logged_in, detail = check_agy_login()
        models = fetch_available_models()
        self.done.emit(True, logged_in, detail if logged_in else "", models)


class Dashboard(QWidget):
    open_module = Signal(str, str)

    def __init__(self, modules: list[tuple[str, str, str]], parent=None) -> None:
        super().__init__(parent)
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 18, 20, 12)
        title = QLabel("Bảng điều khiển")
        title.setObjectName("pageTitle")
        hint = QLabel("Mười một phân hệ trợ lý sư phạm. Chọn một thẻ để mở đúng màn hình làm việc.")
        hint.setObjectName("pageHint")
        hint.setWordWrap(True)
        root.addWidget(title)
        root.addWidget(hint)
        grid = QGridLayout()
        grid.setSpacing(10)
        for index, (key, name, blurb) in enumerate(modules):
            button = QPushButton(f"{name}\n{blurb}")
            button.setObjectName("dashButton")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _checked=False, item=key, label=name: self.open_module.emit(item, label))
            grid.addWidget(button, index // 2, index % 2)
        root.addLayout(grid)
        root.addStretch(1)


class MainWindow(QMainWindow):
    def __init__(self, auto_setup: bool = True) -> None:
        super().__init__()
        self.auto_setup = auto_setup
        self.setWindowTitle("Trợ lý sư phạm")
        self._app_locked = False
        self.resize(1240, 820)
        self.setMinimumSize(980, 680)
        self.worker: AntigravityWorker | None = None
        self.ai_ready = False
        self.model_name = ""
        self._activity = "AI đang suy luận"
        self._tick_phase = 0
        self._ticker = QTimer(self)
        self._ticker.setInterval(800)
        self._ticker.timeout.connect(self._tick_activity)
        self._output_dir = ""
        self._result_path = ""
        self._active_page: QWidget | None = None
        self._preflight: PreflightThread | None = None

        self.khbd = KhbdTab()
        self.baitap = BaiTapTab()
        self.dekiemtra = DeKiemTraTab()
        self.baigiang = BaiGiangTab()
        self.vehinh = VeHinhTab()
        self.chuanhoa = ChuanHoaTab()
        self.duyet = DuyetTab()
        self.baocao = BaoCaoTab()
        self.amthanh = AmThanhTab()

        self.modules = [
            ("khbd", "Soạn KHBD", "Toán 6–9, Công văn 5512"),
            ("baitap", "Tạo bài tập và đề thi", "Công văn 7991, trắc nghiệm, tự luận"),
            ("dekiemtra", "Đề kiểm tra", "Ma trận, Công văn 7991, trộn mã đề"),
            ("duyet-ga", "Duyệt giáo án", "Biên bản và phiếu nhận xét"),
            ("duyet-de", "Duyệt đề", "Ma trận, đáp án, lỗi chuyên môn"),
            ("baocao", "Báo cáo chuyên môn", "Văn bản theo Nghị định 30"),
            ("bienban-to", "Biên bản họp tổ Toán - Tin", "3 phần chuẩn: Triển khai văn bản, Đánh giá, Công tác tới"),
            ("kehoach-to", "Kế hoạch tổ theo tháng", "Form THCS Trần Phú, kèm bảng thi đua và phân công"),
            ("sangkien", "Sáng kiến kinh nghiệm", "Cấu trúc sáng kiến của nhà giáo"),
            ("baigiang", "Bài giảng HTML", "Trình chiếu 16:9 tương tác"),
            ("vehinh", "Vẽ hình học", "Một ảnh PNG 300 DPI"),
            ("chuanhoa", "Chuẩn hoá văn bản", "Nghị định 30 và văn bản Đảng"),
            ("amthanh", "Chuyển ghi âm", "Bóc tách lời nói ra Word và văn bản"),
        ]
        self.page_by_key = {
            "khbd": self.khbd,
            "baitap": self.baitap,
            "dekiemtra": self.dekiemtra,
            "duyet-ga": self.duyet,
            "duyet-de": self.duyet,
            "baocao": self.baocao,
            "bienban-to": self.baocao,
            "kehoach-to": self.baocao,
            "sangkien": self.baocao,
            "baigiang": self.baigiang,
            "vehinh": self.vehinh,
            "chuanhoa": self.chuanhoa,
            "amthanh": self.amthanh,
        }

        shell = QWidget()
        shell_layout = QHBoxLayout(shell)
        shell_layout.setContentsMargins(0, 0, 0, 0)
        shell_layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(248)
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(14, 18, 14, 16)
        side_layout.setSpacing(6)
        logo = QLabel()
        logo.setObjectName("brandLogo")
        icon_png = app_dir() / "assets" / "app_icon.png"
        if icon_png.is_file():
            logo.setPixmap(
                QPixmap(str(icon_png)).scaled(
                    42,
                    42,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        brand = QLabel("Trợ lý sư phạm")
        brand.setObjectName("brand")
        side_layout.addWidget(logo)
        side_layout.addWidget(brand)
        side_layout.addSpacing(8)

        self.stack = QStackedWidget()
        self.dashboard = Dashboard(self.modules)
        self.dashboard.open_module.connect(self.open_module)
        self.pages: list[QWidget] = [
            self.dashboard,
            self.khbd,
            self.baitap,
            self.dekiemtra,
            self.baigiang,
            self.vehinh,
            self.chuanhoa,
            self.duyet,
            self.baocao,
            self.amthanh,
        ]
        labels = [
            "⌂  Tổng quan",
            "▦  Soạn KHBD",
            "✎  Tạo bài tập",
            "▤  Đề kiểm tra",
            "▶  Bài giảng HTML",
            "△  Vẽ hình",
            "☰  Chuẩn hoá",
            "✓  Duyệt hồ sơ",
            "≡  Báo cáo",
            "♪  Chuyển ghi âm",
        ]
        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)
        self.nav_buttons: list[QPushButton] = []
        for index, (page, label) in enumerate(zip(self.pages, labels)):
            self.stack.addWidget(page)
            button = QPushButton(label)
            button.setObjectName("navButton")
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.nav_group.addButton(button, index)
            self.nav_buttons.append(button)
            side_layout.addWidget(button)
            if hasattr(page, "request_run"):
                page.request_run.connect(self.start_task)
        self.nav_buttons[0].setChecked(True)
        self.nav_group.idClicked.connect(self._on_nav)
        side_layout.addStretch(1)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        right_layout.addWidget(self._build_header())
        self.lock_banner = QLabel(
            "Ứng dụng đang khóa. Bấm Bản quyền để kích hoạt Online trên hoangthiencm.id.vn hoặc nhập mã offline."
        )
        self.lock_banner.setObjectName("licenseOff")
        self.lock_banner.setWordWrap(True)
        self.lock_banner.setContentsMargins(16, 8, 16, 8)
        self.lock_banner.setVisible(False)
        right_layout.addWidget(self.lock_banner)
        self.log_panel = LogPanel()
        right_layout.addWidget(self.stack, 1)
        right_layout.addWidget(self.log_panel)
        self.log_panel.open_folder_clicked.connect(self.open_output_folder)
        self.log_panel.open_result_clicked.connect(self.open_result)
        self.log_panel.stop_clicked.connect(self.stop_worker)

        shell_layout.addWidget(sidebar)
        shell_layout.addWidget(right, 1)
        self.setCentralWidget(shell)
        self._apply_license_gate()
        self._start_preflight()
        if self._app_locked:
            QTimer.singleShot(0, self.show_license)

    def _build_header(self) -> QWidget:
        header = QFrame()
        header.setObjectName("statusHeader")
        row = QHBoxLayout(header)
        row.setContentsMargins(16, 10, 16, 10)
        self.status_dot = QLabel("●")
        self.status_dot.setObjectName("statusBad")
        self.status_text = QLabel("Đang kiểm tra agy…")
        self.status_text.setObjectName("statusBad")
        self.license_badge = QLabel("Chưa kích hoạt")
        self.license_badge.setObjectName("licenseOff")
        model_caption = QLabel("Mô hình AI:")
        model_caption.setObjectName("pageHint")
        self.model_combo = QComboBox()
        self.model_combo.setObjectName("modelCombo")
        self.model_combo.setMinimumWidth(240)
        self.model_combo.setMaximumWidth(420)
        self.account_button = QPushButton("Quản lý tài khoản")
        self.account_button.clicked.connect(self.show_setup)
        self.license_button = QPushButton("Bản quyền")
        self.license_button.clicked.connect(self.show_license)
        row.addWidget(self.status_dot)
        row.addWidget(self.status_text)
        row.addSpacing(12)
        row.addWidget(self.license_badge)
        row.addStretch(1)
        row.addWidget(model_caption)
        row.addWidget(self.model_combo)
        row.addWidget(self.account_button)
        row.addWidget(self.license_button)
        return header

    def _on_nav(self, index: int) -> None:
        if self._app_locked:
            return
        self.stack.setCurrentIndex(index)

    def _set_app_locked(self, locked: bool) -> None:
        """Khóa tab, sidebar và thao tác soạn khi chưa có bản quyền. Nút Bản quyền luôn bật."""
        self._app_locked = locked
        self.stack.setEnabled(not locked)
        for button in self.nav_buttons:
            button.setEnabled(not locked)
        self.account_button.setEnabled(not locked)
        self.license_button.setEnabled(True)
        self.lock_banner.setVisible(locked)
        self.log_panel.setEnabled(not locked)
        if locked:
            self.model_combo.setEnabled(False)
        else:
            self.model_combo.setEnabled(self.model_combo.count() > 0)
        self._set_run_enabled(not locked)

    def _set_license_badge(self, active: bool, email: str) -> None:
        if active and email:
            self.license_badge.setText(f"★ BẢN QUYỀN CHÍNH THỨC - {email}")
            name = "licenseOn"
        elif active:
            self.license_badge.setText("★ BẢN QUYỀN CHÍNH THỨC")
            name = "licenseOn"
        else:
            self.license_badge.setText("Chưa kích hoạt")
            name = "licenseOff"
        self.license_badge.setObjectName(name)
        self.license_badge.style().unpolish(self.license_badge)
        self.license_badge.style().polish(self.license_badge)

    def _apply_license_gate(self) -> None:
        active, email = is_licensed()
        self._set_license_badge(active, email)
        self._set_app_locked(not active)

    def show_license(self) -> None:
        dialog = LicenseDialog(self)
        dialog.exec()
        self._apply_license_gate()

    def _start_preflight(self) -> None:
        ready, detail = knowledge_ready()
        if not ready:
            self.status_text.setText(detail)
            return
        self._preflight = PreflightThread(self)
        self._preflight.done.connect(self._on_preflight)
        self._preflight.start()

    def _on_preflight(self, installed: bool, logged_in: bool, detail: str, models: object) -> None:
        catalog = list(models) if isinstance(models, (list, tuple)) else []
        self._apply_status(installed and logged_in, detail if logged_in else "", catalog)
        if self.auto_setup and not (installed and logged_in):
            self.show_setup()

    def _apply_status(self, ready: bool, model: str, models: list | None = None) -> None:
        self.ai_ready = ready
        if models:
            self._fill_models(models, prefer=model)
        elif model and self.model_combo.count() == 0:
            self.model_combo.addItem(model, model)
            self._select_model(model)
        elif model:
            self._select_model(model)
        name = "statusOk" if ready else "statusBad"
        self.status_dot.setObjectName(name)
        self.status_text.setObjectName(name)
        self.status_dot.style().unpolish(self.status_dot)
        self.status_dot.style().polish(self.status_dot)
        self.status_text.style().unpolish(self.status_text)
        self.status_text.style().polish(self.status_text)
        self.model_combo.setEnabled((not self._app_locked) and (ready or self.model_combo.count() > 0))
        if ready:
            self.status_text.setText("AI đã kết nối")
            self.model_name = str(self.model_combo.currentData() or model or "")
            return
        self.status_text.setText("AI chưa sẵn sàng")
        self.model_name = str(self.model_combo.currentData() or "")

    def _fill_models(self, models: list, prefer: str = "") -> None:
        current = str(self.model_combo.currentData() or "")
        self.model_combo.blockSignals(True)
        self.model_combo.clear()
        seen: set[str] = set()
        for item in models:
            if not isinstance(item, (list, tuple)) or len(item) < 1:
                continue
            model_id = str(item[0]).strip()
            label = str(item[1]).strip() if len(item) > 1 else model_id
            if not model_id or model_id in seen:
                continue
            seen.add(model_id)
            self.model_combo.addItem(label or model_id, model_id)
        self.model_combo.blockSignals(False)
        if self.model_combo.count() and not (prefer or current):
            self.model_combo.setCurrentIndex(0)
        self._select_model(prefer or current)
        self.model_name = str(self.model_combo.currentData() or "")
        if self._app_locked:
            self.model_combo.setEnabled(False)

    def _select_model(self, model_id: str) -> None:
        wanted = (model_id or "").strip()
        if not wanted:
            self.model_name = str(self.model_combo.currentData() or "")
            return
        for index in range(self.model_combo.count()):
            data = str(self.model_combo.itemData(index) or "")
            text = self.model_combo.itemText(index)
            if wanted in {data, text}:
                self.model_combo.setCurrentIndex(index)
                self.model_name = data
                return
        self.model_name = str(self.model_combo.currentData() or "")

    def _tick_activity(self) -> None:
        if not self._ticker.isActive():
            return
        self._tick_phase = (self._tick_phase + 1) % 4
        dots = "." * self._tick_phase
        self.log_panel.set_status(f"{self._activity}{dots}")

    def _on_worker_log(self, text: str) -> None:
        self.log_panel.append_log(text)
        clean = " ".join((text or "").split())
        if clean and not clean.startswith("AI đang suy luận"):
            self._activity = clean[:80]

    def show_setup(self) -> None:
        dialog = SetupDialog(self)
        dialog.status_ready.connect(lambda model: self._apply_status(True, model))
        dialog.exec()
        if dialog.model_name:
            self._apply_status(True, dialog.model_name)
        elif not self.ai_ready:
            self._apply_status(False, "")

    def open_module(self, key: str, label: str) -> None:
        if self._app_locked:
            return
        page = self.page_by_key[key]
        if key == "duyet-de":
            self.duyet.set_mode("đề")
        elif key == "duyet-ga":
            self.duyet.set_mode("giáo án")
        elif key == "bienban-to":
            self.baocao.set_mode("biên bản")
        elif key == "kehoach-to":
            self.baocao.set_mode("kế hoạch")
        elif key == "sangkien":
            self.baocao.set_mode("sáng kiến")
        elif key == "baocao":
            self.baocao.set_mode("báo cáo")
        index = self.pages.index(page)
        self.nav_buttons[index].setChecked(True)
        self.stack.setCurrentIndex(index)

    def start_task(self, prompt: str, output_dir: str) -> None:
        active, _email = is_licensed()
        if not active:
            QMessageBox.warning(
                self,
                "Chưa kích hoạt",
                "Cần kích hoạt bản quyền bằng Email và Mã máy trước khi gửi việc.",
            )
            self.show_license()
            if not is_licensed()[0]:
                return
        if not self.ai_ready:
            QMessageBox.warning(
                self,
                "Chưa sẵn sàng",
                "Cần cài agy và đăng nhập AI trước khi gửi lệnh. Hộp thoại môi trường sẽ mở.",
            )
            self.show_setup()
            if not self.ai_ready:
                return
        if self.worker is not None and self.worker.isRunning():
            QMessageBox.information(
                self,
                "Đang chạy",
                "Một việc đang chạy ngầm. Hãy đợi xong hoặc bấm Dừng trước khi chạy việc khác.",
            )
            return
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        self._output_dir = output_dir
        self._result_path = ""
        self._active_page = self.stack.currentWidget()
        self.log_panel.log.clear()
        self.log_panel.set_progress(0)
        self._activity = "AI đang suy luận"
        self._tick_phase = 0
        self.log_panel.set_status("Đang chạy ngầm…")
        self.log_panel.set_busy(True)
        self.log_panel.set_result_ready(False)
        self._ticker.start()
        self._set_run_enabled(False)
        model_id = str(self.model_combo.currentData() or "")
        self.model_name = model_id
        self.worker = AntigravityWorker(prompt, output_dir, model=model_id, parent=self)
        self.worker.signal_log.connect(self._on_worker_log)
        self.worker.signal_progress.connect(self.log_panel.set_progress)
        self.worker.signal_finished.connect(self._on_finished)
        self.worker.start()

    def stop_worker(self) -> None:
        if self.worker is not None and self.worker.isRunning():
            self.log_panel.append_log("Đang dừng tiến trình agy…")
            self.worker.stop()

    def _on_finished(self, ok: bool, message: str) -> None:
        self._ticker.stop()
        self.log_panel.set_busy(False)
        self._set_run_enabled(True)
        path = Path(message) if message else None
        if ok and path is not None and path.exists():
            self._result_path = str(path)
            self.log_panel.set_status("Xong")
            self.log_panel.set_result_ready(path.is_file())
            if path.is_dir():
                self._output_dir = str(path)
            elif path.is_file():
                self._output_dir = str(path.parent)
            page = self._active_page
            if page is not None and hasattr(page, "show_result"):
                page.show_result(str(path))
            return
        if ok:
            self.log_panel.set_status("Xong, chưa thấy file mới")
            self.log_panel.append_log(message)
            return
        self.log_panel.set_status("Chưa xong")
        self.log_panel.append_log(message)

    def open_output_folder(self) -> None:
        page = self._active_page or self.stack.currentWidget()
        folder = self._output_dir or getattr(page, "output_dir", lambda: "")()
        if not folder:
            return
        Path(folder).mkdir(parents=True, exist_ok=True)
        self._open_path(Path(folder))

    def open_result(self) -> None:
        if self._result_path:
            self._open_path(Path(self._result_path))

    def _open_path(self, path: Path) -> None:
        if path.exists():
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))

    def _set_run_enabled(self, enabled: bool) -> None:
        for page in self.pages:
            button = getattr(page, "run_button", None)
            if button is not None:
                button.setEnabled(enabled)

    def closeEvent(self, event) -> None:  # noqa: N802
        self._ticker.stop()
        self.stop_worker()
        if self.worker is not None and self.worker.isRunning():
            self.worker.wait(1500)
        super().closeEvent(event)
