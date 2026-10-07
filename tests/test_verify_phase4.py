"""Kiểm thử khóa bản quyền, tiêu đề, model agy và API license."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app_trolythien"))
os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ["TLHT_LICENSE_HOME"] = tempfile.mkdtemp(prefix="tlht_phase4_")

sys.stdout.reconfigure(encoding="utf-8")


def test_title_and_lock() -> None:
    from PySide6.QtWidgets import QApplication, QLabel, QPushButton

    from core.license import is_licensed, save_activation
    from ui.license_dialog import LicenseDialog
    from ui.main_window import MainWindow

    app = QApplication.instance() or QApplication([])
    window = MainWindow(auto_setup=False)
    window.show_license = lambda: None

    assert window.windowTitle() == "Trợ lý sư phạm", window.windowTitle()
    brands = [label.text() for label in window.findChildren(QLabel) if label.objectName() == "brand"]
    assert brands == ["Trợ lý sư phạm"], brands
    texts = [label.text() for label in window.findChildren(QLabel)]
    assert not any("Nền tảng giảng dạy" in text for text in texts)
    assert not any("Chạy ngầm agy.exe" in text for text in texts)
    assert not is_licensed()[0]
    assert window._app_locked
    assert not window.stack.isEnabled()
    assert window.nav_buttons and all(not button.isEnabled() for button in window.nav_buttons)
    assert not window.model_combo.isEnabled()
    assert not window.account_button.isEnabled()
    assert window.license_button.isEnabled()
    assert not window.lock_banner.isHidden()
    assert not window.vehinh.run_button.isEnabled()

    dialog = LicenseDialog()
    labels = [label.text() for label in dialog.findChildren(QLabel)]
    buttons = [button.text() for button in dialog.findChildren(QPushButton)]
    assert "Kích hoạt bản quyền" in buttons
    assert "Nhập Mã kích hoạt" not in buttons
    assert not any("offline" in text.lower() for text in labels + buttons)
    assert not hasattr(dialog, "key")
    dialog.close()

    email = "gv.phase4@example.com"
    save_activation(email, "online")
    window._apply_license_gate()
    assert is_licensed() == (True, email)
    assert not window._app_locked
    assert window.stack.isEnabled()
    assert all(button.isEnabled() for button in window.nav_buttons)
    assert window.license_button.isEnabled()
    assert window.vehinh.run_button.isEnabled()
    assert "★ BẢN QUYỀN CHÍNH THỨC - gv.phase4@example.com" in window.license_badge.text()

    window._fill_models([("agy-model-a", "Mô hình A"), ("agy-model-b", "Mô hình B")], prefer="")
    assert window.model_combo.currentData() == "agy-model-a"
    assert window.model_combo.count() == 2
    print("Test 1 (khóa app và tiêu đề): PASS")

    window.close()
    preflight = window._preflight
    if preflight is not None and preflight.isRunning():
        preflight.wait(1000)


def test_agy_models() -> None:
    import core.preflight as preflight

    parsed = preflight._parse_model_table(
        "fetching\n"
        "agy-one\tMô hình một\n"
        "agy-two\tMô hình hai\n"
    )
    assert parsed == [("agy-one", "Mô hình một"), ("agy-two", "Mô hình hai")]
    assert not hasattr(preflight, "_fallback_models")
    source = Path(preflight.__file__).read_text(encoding="utf-8")
    assert "gpt-oss-120b-medium" not in source
    original = preflight.find_agy
    preflight.find_agy = lambda: None
    try:
        assert preflight.fetch_available_models() == []
    finally:
        preflight.find_agy = original
    print("Test 2 (model lấy từ agy, không danh sách giả): PASS")


def test_online_api_client() -> None:
    import core.license as license

    from core.license import LICENSE_ONLINE_URL, license_message, verify_license_online

    assert LICENSE_ONLINE_URL == "https://hoangthiencm.id.vn/api/license.php"
    source = Path(license.__file__).read_text(encoding="utf-8")
    assert "issue_offline_key" not in source
    assert "verify_license_offline" not in source
    assert "mã offline" not in source.lower()
    state = {"status": "pending"}

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:
            length = int(self.headers.get("Content-Length") or 0)
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            assert payload["action"] == "verify"
            body = {
                "ok": state["status"] == "active",
                "status": state["status"],
                "email": payload["email"],
                "device_id": payload["device_id"],
                "message": "Máy đang chờ Thầy Thiên duyệt trên hoangthiencm.id.vn."
                if state["status"] != "active"
                else "Máy đã được duyệt trên hoangthiencm.id.vn.",
            }
            raw = json.dumps(body).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def log_message(self, fmt: str, *args) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    os.environ["TLHT_LICENSE_URL"] = f"http://127.0.0.1:{server.server_address[1]}/api/license.php"
    try:
        assert not verify_license_online("gv.phase4@example.com", "TLHT-AAAA-BBBB-CCCC")
        assert "chờ" in license_message().lower() or "duyệt" in license_message().lower()
        state["status"] = "active"
        assert verify_license_online("gv.phase4@example.com", "TLHT-AAAA-BBBB-CCCC")
    finally:
        server.shutdown()
        os.environ.pop("TLHT_LICENSE_URL", None)
    print("Test 3 (client kích hoạt online): PASS")


def test_license_api_and_admin() -> None:
    php = (ROOT / "api" / "license.php").read_text(encoding="utf-8")
    admin = (ROOT / "admin.html").read_text(encoding="utf-8")
    for token in (
        "flock",
        "licenses.json",
        "verify",
        "approve",
        "revoke",
        "delete",
        "'list'",
        "pending",
        "active",
        "HTTP_X_ADMIN_KEY",
        "TLHT_LICENSE_STORE",
    ):
        assert token in php, token
    assert "Bản Quyền App Desktop" in admin
    assert "api/license.php?action=list" in admin
    assert "desktopLicenseSearch" in admin
    for action in ("approve", "revoke", "delete"):
        assert f'data-license-action="{action}"' in admin
    print("Test 4 (api/license.php và admin.html): PASS")


if __name__ == "__main__":
    test_title_and_lock()
    test_agy_models()
    test_online_api_client()
    test_license_api_and_admin()
    print("\nALL PHASE 4 TESTS PASSED")
    os._exit(0)
