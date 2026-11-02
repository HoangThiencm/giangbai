"""Hộp thoại cài agy, đăng nhập Gmail và hồ sơ tài khoản."""

from __future__ import annotations

import ctypes
import json
import os
import re
from ctypes import wintypes
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QUrl, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QComboBox, QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from core.preflight import check_agy_installed, check_agy_login, open_agy_install, open_agy_login

DOCS = "https://antigravity.google/docs/cli/install"
CRED_TARGET = "gemini:antigravity"
CRED_TYPE_GENERIC = 1
CRED_PERSIST_LOCAL_MACHINE = 2
_EMAIL_LOG = re.compile(r"applyAuthResult:\s*email=([^\s,]+)", re.IGNORECASE)


class _FileTime(ctypes.Structure):
    _fields_ = [("lo", wintypes.DWORD), ("hi", wintypes.DWORD)]


class _Credential(ctypes.Structure):
    _fields_ = [
        ("Flags", wintypes.DWORD),
        ("Type", wintypes.DWORD),
        ("TargetName", wintypes.LPWSTR),
        ("Comment", wintypes.LPWSTR),
        ("LastWritten", _FileTime),
        ("CredentialBlobSize", wintypes.DWORD),
        ("CredentialBlob", ctypes.c_void_p),
        ("Persist", wintypes.DWORD),
        ("AttributeCount", wintypes.DWORD),
        ("Attributes", ctypes.c_void_p),
        ("TargetAlias", wintypes.LPWSTR),
        ("UserName", wintypes.LPWSTR),
    ]


def profile_home() -> Path:
    override = os.environ.get("TLHT_PROFILE_HOME", "").strip()
    if override:
        return Path(override)
    local = os.environ.get("LOCALAPPDATA", "").strip() or str(Path.home())
    return Path(local) / "TroLyHoangThien" / "agy_profiles"


def _advapi32():
    library = ctypes.windll.advapi32
    pointer = ctypes.POINTER(_Credential)
    library.CredReadW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(pointer)]
    library.CredReadW.restype = wintypes.BOOL
    library.CredWriteW.argtypes = [ctypes.POINTER(_Credential), wintypes.DWORD]
    library.CredWriteW.restype = wintypes.BOOL
    library.CredDeleteW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD]
    library.CredDeleteW.restype = wintypes.BOOL
    library.CredFree.argtypes = [ctypes.c_void_p]
    return library


def read_credential_blob(target: str = CRED_TARGET) -> bytes:
    if sys_platform_unsupported():
        return b""
    library = _advapi32()
    found = ctypes.POINTER(_Credential)()
    if not library.CredReadW(target, CRED_TYPE_GENERIC, 0, ctypes.byref(found)):
        return b""
    try:
        item = found.contents
        size = int(item.CredentialBlobSize)
        if size <= 0 or not item.CredentialBlob:
            return b""
        return ctypes.string_at(item.CredentialBlob, size)
    finally:
        library.CredFree(found)


def write_credential_blob(blob: bytes, target: str = CRED_TARGET) -> bool:
    if sys_platform_unsupported() or not blob:
        return False
    library = _advapi32()
    buffer = ctypes.create_string_buffer(blob)
    target_buf = ctypes.create_unicode_buffer(target)
    user_buf = ctypes.create_unicode_buffer("antigravity")
    item = _Credential()
    item.Type = CRED_TYPE_GENERIC
    item.TargetName = ctypes.cast(target_buf, wintypes.LPWSTR)
    item.CredentialBlobSize = len(blob)
    item.CredentialBlob = ctypes.cast(buffer, ctypes.c_void_p)
    item.Persist = CRED_PERSIST_LOCAL_MACHINE
    item.UserName = ctypes.cast(user_buf, wintypes.LPWSTR)
    return bool(library.CredWriteW(ctypes.byref(item), 0))


def delete_credential(target: str = CRED_TARGET) -> bool:
    if sys_platform_unsupported():
        return False
    library = _advapi32()
    return bool(library.CredDeleteW(target, CRED_TYPE_GENERIC, 0))


def sys_platform_unsupported() -> bool:
    return os.name != "nt"


def _cli_log_path() -> Path:
    return Path.home() / ".gemini" / "antigravity-cli" / "cli.log"


def _email_from_log() -> str:
    path = _cli_log_path()
    if not path.is_file():
        return ""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""
    found = _EMAIL_LOG.findall(text)
    if not found:
        return ""
    return found[-1].strip()


def _email_from_storage() -> str:
    path = Path(os.environ.get("APPDATA", "")) / "antigravity" / "app_storage.json"
    if not path.is_file():
        return ""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ""

    found = ""

    def walk(node: object, key: str = "") -> None:
        nonlocal found
        if found:
            return
        if isinstance(node, dict):
            for name, value in node.items():
                if name.endswith("lastLoginUsername") and isinstance(value, str) and "@" in value:
                    found = value.strip()
                    return
                walk(value, name)
        elif isinstance(node, list):
            for item in node:
                walk(item, key)

    walk(payload)
    return found


def current_gmail() -> str:
    """Email Gmail agy vừa xác thực. Nhật ký CLI ưu tiên hơn hồ sơ IDE."""
    return _email_from_log() or _email_from_storage()


def _index_path() -> Path:
    return profile_home() / "accounts.json"


def _load_index() -> list[dict]:
    path = _index_path()
    if not path.is_file():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    rows = payload.get("profiles") if isinstance(payload, dict) else None
    if not isinstance(rows, list):
        return []
    clean = []
    for row in rows:
        if isinstance(row, dict) and "@" in str(row.get("email") or ""):
            clean.append(row)
    return clean


def _write_index(rows: list[dict]) -> None:
    folder = profile_home()
    folder.mkdir(parents=True, exist_ok=True)
    _index_path().write_text(
        json.dumps({"profiles": rows}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def list_profiles() -> list[str]:
    emails = []
    for row in _load_index():
        email = str(row.get("email") or "").strip()
        if email and email not in emails and (profile_home() / str(row.get("file") or "")).is_file():
            emails.append(email)
    return emails


def _safe_name(email: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", email.strip().lower()).strip("_") or "account"


def save_current_profile(email: str = "") -> tuple[bool, str]:
    address = (email or current_gmail()).strip()
    blob = read_credential_blob()
    if not address or "@" not in address:
        return False, "Chưa đọc được email Gmail đang đăng nhập."
    if not blob:
        return False, "Chưa có phiên agy trong Windows Credential để lưu."
    folder = profile_home()
    folder.mkdir(parents=True, exist_ok=True)
    file_name = _safe_name(address) + ".cred"
    (folder / file_name).write_bytes(blob)
    rows = [row for row in _load_index() if str(row.get("email") or "").lower() != address.lower()]
    rows.append(
        {
            "email": address,
            "file": file_name,
            "saved_at": datetime.now().replace(microsecond=0).isoformat(sep=" "),
        }
    )
    _write_index(rows)
    return True, address


def activate_profile(email: str) -> tuple[bool, str]:
    wanted = email.strip().lower()
    for row in _load_index():
        if str(row.get("email") or "").strip().lower() != wanted:
            continue
        path = profile_home() / str(row.get("file") or "")
        if not path.is_file():
            return False, "Không thấy tệp hồ sơ đã lưu."
        if not write_credential_blob(path.read_bytes()):
            return False, "Không ghi lại được phiên đăng nhập agy."
        return True, str(row.get("email"))
    return False, "Chưa có hồ sơ cho email này."


class SetupDialog(QDialog):
    """Hiện trạng cài đặt, Gmail đang dùng và các hồ sơ đã lưu."""

    status_ready = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Môi trường và tài khoản Gmail")
        self.setMinimumWidth(560)
        self.model_name = ""
        root = QVBoxLayout(self)
        root.setSpacing(10)
        intro = QLabel(
            "Ứng dụng cần agy.exe và một phiên đăng nhập Google trước khi gửi việc. "
            "Hồ sơ Gmail giúp chuyển tài khoản khi hết hạn mức."
        )
        intro.setWordWrap(True)
        root.addWidget(intro)

        self.install_label = QLabel("AGY: đang kiểm tra…")
        self.install_label.setWordWrap(True)
        self.login_label = QLabel("Đăng nhập: đang kiểm tra…")
        self.login_label.setWordWrap(True)
        root.addWidget(self.install_label)
        root.addWidget(self.login_label)

        root.addWidget(QLabel("Tài khoản AI (Google Account)"))
        self.account_label = QLabel("Gmail đang dùng: đang đọc…")
        self.account_label.setWordWrap(True)
        root.addWidget(self.account_label)
        self.profile_combo = QComboBox()
        self.profile_combo.setObjectName("accountProfiles")
        root.addWidget(self.profile_combo)

        docs = QLabel(f'<a href="{DOCS}">Hướng dẫn cài agy</a>')
        docs.setOpenExternalLinks(False)
        docs.linkActivated.connect(lambda _url: QDesktopServices.openUrl(QUrl(DOCS)))
        root.addWidget(docs)

        row = QHBoxLayout()
        self.install_button = QPushButton("Thiết lập agy")
        self.login_button = QPushButton("Đăng nhập Gmail")
        self.switch_button = QPushButton("Đổi tài khoản Gmail")
        self.new_button = QPushButton("Đăng nhập tài khoản mới")
        self.recheck_button = QPushButton("Kiểm tra lại")
        self.close_button = QPushButton("Đóng")
        self.install_button.clicked.connect(open_agy_install)
        self.login_button.clicked.connect(self._login)
        self.switch_button.clicked.connect(self._switch)
        self.new_button.clicked.connect(self._login_new)
        self.recheck_button.clicked.connect(self.refresh)
        self.close_button.clicked.connect(self.accept)
        row.addWidget(self.install_button)
        row.addWidget(self.login_button)
        row.addWidget(self.switch_button)
        root.addLayout(row)
        extra = QHBoxLayout()
        extra.addWidget(self.new_button)
        extra.addWidget(self.recheck_button)
        extra.addWidget(self.close_button)
        extra.addStretch(1)
        root.addLayout(extra)
        self.refresh()

    def refresh(self) -> None:
        self._fill_profiles()
        email = current_gmail()
        if email:
            self.account_label.setText("Gmail đang dùng: " + email)
        else:
            self.account_label.setText("Gmail đang dùng: chưa đọc được email. Hãy đăng nhập rồi bấm Kiểm tra lại.")
        installed, info = check_agy_installed()
        self.login_button.setEnabled(installed)
        self.new_button.setEnabled(installed)
        self.switch_button.setEnabled(installed or self.profile_combo.count() > 0)
        self.install_button.setEnabled(not installed)
        if not installed:
            self.install_label.setText("AGY: chưa cài. " + info)
            self.login_label.setText("Đăng nhập: chưa kiểm tra vì chưa có agy.exe.")
            self.model_name = ""
            return
        self.install_label.setText("AGY: đã có tại " + info)
        self.login_label.setText("Đăng nhập: đang gọi agy models…")
        self.login_label.repaint()
        ok, detail = check_agy_login()
        if ok:
            self.model_name = detail
            fresh = current_gmail() or email
            if fresh:
                self.account_label.setText("Gmail đang dùng: " + fresh)
                save_current_profile(fresh)
                self._fill_profiles(select=fresh)
            self.login_label.setText("Đăng nhập: đã xác thực. Mô hình: " + detail)
            self.status_ready.emit(detail)
            return
        self.model_name = ""
        self.login_label.setText("Đăng nhập: chưa xong. " + detail)

    def _fill_profiles(self, select: str = "") -> None:
        current = select or self.profile_combo.currentText()
        self.profile_combo.blockSignals(True)
        self.profile_combo.clear()
        emails = list_profiles()
        if emails:
            self.profile_combo.addItems(emails)
        else:
            self.profile_combo.addItem("Chưa lưu hồ sơ nào")
        if current:
            index = self.profile_combo.findText(current)
            if index >= 0:
                self.profile_combo.setCurrentIndex(index)
        self.profile_combo.blockSignals(False)

    def _login(self) -> None:
        email = current_gmail()
        if email:
            save_current_profile(email)
            self._fill_profiles(select=email)
        ok, detail = open_agy_login()
        if not ok:
            self.login_label.setText("Không mở được đăng nhập. " + detail)
            return
        self.login_label.setText(
            "Đã mở cửa sổ lệnh agy. Hoàn tất đăng nhập Google trong trình duyệt, rồi bấm Kiểm tra lại."
        )

    def _login_new(self) -> None:
        email = current_gmail()
        blob = read_credential_blob()
        if blob and not email:
            self.account_label.setText("Chưa đọc được email để lưu hồ sơ. Bấm Kiểm tra lại trước khi đăng nhập tài khoản mới.")
            return
        if blob and email:
            ok, detail = save_current_profile(email)
            if not ok:
                self.account_label.setText(detail)
                return
            self._fill_profiles(select=email)
            if not delete_credential():
                self.account_label.setText("Đã lưu hồ sơ nhưng chưa xoá được phiên hiện tại.")
                return
        ok, detail = open_agy_login()
        if not ok:
            self.login_label.setText("Không mở được đăng nhập. " + detail)
            return
        self.account_label.setText("Đã lưu hồ sơ cũ và mở đăng nhập Google mới. Xong thì bấm Kiểm tra lại.")

    def _switch(self) -> None:
        selected = self.profile_combo.currentText().strip()
        active = current_gmail()
        if "@" in selected and selected.lower() != active.lower():
            if active:
                saved, detail = save_current_profile(active)
                if not saved:
                    self.account_label.setText(detail)
                    return
            ok, detail = activate_profile(selected)
            if not ok:
                self.account_label.setText(detail)
                return
            self.account_label.setText(
                f"Đã chuyển phiên agy sang {detail}. Bấm Kiểm tra lại để xác nhận Gmail."
            )
            return
        if active:
            saved, detail = save_current_profile(active)
            if not saved and read_credential_blob():
                self.account_label.setText(detail)
                return
        if read_credential_blob() and not delete_credential():
            self.account_label.setText("Không đóng được phiên Gmail hiện tại.")
            return
        ok, detail = open_agy_login()
        if not ok:
            self.login_label.setText("Không mở được đăng nhập. " + detail)
            return
        self.account_label.setText(
            "Đã đóng phiên hiện tại. Đăng nhập Gmail khác trong cửa sổ agy, rồi bấm Kiểm tra lại."
        )
