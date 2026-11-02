"""Hộp thoại kích hoạt bản quyền online một lần bấm."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from core.license import (
    get_machine_id,
    is_licensed,
    license_message,
    save_activation,
    verify_license_online,
)


class LicenseDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Kích hoạt bản quyền")
        self.setMinimumWidth(560)
        self.device_id = get_machine_id()
        licensed, email = is_licensed()
        root = QVBoxLayout(self)
        root.setSpacing(10)
        intro = QLabel(
            "Nhập Email và bấm Kích hoạt bản quyền. "
            "Thầy Thiên phê duyệt trên trang quản trị hoangthiencm.id.vn để mở khóa ứng dụng."
        )
        intro.setWordWrap(True)
        root.addWidget(intro)

        root.addWidget(QLabel("Email đăng ký"))
        self.email = QLineEdit(email)
        self.email.setPlaceholderText("ten@gmail.com")
        root.addWidget(self.email)

        root.addWidget(QLabel("Mã máy (Device ID)"))
        id_row = QHBoxLayout()
        self.device = QLineEdit(self.device_id)
        self.device.setReadOnly(True)
        copy_button = QPushButton("Copy Mã máy & Email")
        copy_button.clicked.connect(self._copy)
        id_row.addWidget(self.device, 1)
        id_row.addWidget(copy_button)
        root.addLayout(id_row)

        self.status = QLabel("Đã kích hoạt." if licensed else "Chưa kích hoạt.")
        self.status.setWordWrap(True)
        root.addWidget(self.status)

        row = QHBoxLayout()
        activate = QPushButton("Kích hoạt bản quyền")
        activate.setObjectName("primaryButton")
        close = QPushButton("Đóng")
        activate.clicked.connect(self._activate)
        close.clicked.connect(self.reject)
        row.addWidget(activate)
        row.addWidget(close)
        root.addLayout(row)

    def _email_text(self) -> str:
        return self.email.text().strip()

    def _copy(self) -> None:
        text = f"Email: {self._email_text()}\nMã máy: {self.device_id}"
        QApplication.clipboard().setText(text)
        self.status.setText("Đã copy Mã máy và Email.")

    def _require_email(self) -> str:
        email = self._email_text()
        if "@" not in email or email.startswith("@") or email.endswith("@"):
            QMessageBox.warning(self, "Thiếu Email", "Nhập Email đăng ký hợp lệ.")
            return ""
        return email

    def _activate(self) -> None:
        email = self._require_email()
        if not email:
            return
        self.status.setText("Đang gửi Email và Mã máy tới hoangthiencm.id.vn…")
        self.status.repaint()
        if not verify_license_online(email, self.device_id):
            self.status.setText(license_message() or "Chưa kích hoạt được.")
            return
        save_activation(email, "online")
        self.status.setText("Đã kích hoạt trên hoangthiencm.id.vn. " + license_message())
        self.accept()
