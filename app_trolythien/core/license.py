"""Mã máy và kích hoạt bản quyền online qua hoangthiencm.id.vn."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
import winreg
from datetime import datetime, timezone
from pathlib import Path

CREATE_NO_WINDOW = 0x08000000
_SECRET = b"TLHT-HoangThien-SuPham-4.0"
_LAST_MESSAGE = ""

# API duyệt máy trên web Thầy Thiên. Kiểm thử có thể ghi đè bằng TLHT_LICENSE_URL.
LICENSE_ONLINE_URL = "https://hoangthiencm.id.vn/api/license.php"


def license_message() -> str:
    return _LAST_MESSAGE


def _note(text: str) -> None:
    global _LAST_MESSAGE
    _LAST_MESSAGE = text


def license_home() -> Path:
    override = os.environ.get("TLHT_LICENSE_HOME", "").strip()
    if override:
        return Path(override)
    local = os.environ.get("LOCALAPPDATA", "").strip() or str(Path.home())
    return Path(local) / "TroLyHoangThien"


def license_path() -> Path:
    return license_home() / "license.dat"


def _machine_guid() -> str:
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography") as key:
            value, _kind = winreg.QueryValueEx(key, "MachineGuid")
    except OSError:
        return ""
    return str(value).strip()


def _wmic_uuid() -> str:
    flags = CREATE_NO_WINDOW if sys.platform == "win32" else 0
    try:
        completed = subprocess.run(
            ["wmic", "csproduct", "get", "uuid"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=8,
            creationflags=flags,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    lines = [
        line.strip()
        for line in (completed.stdout or "").splitlines()
        if line.strip() and line.strip().lower() != "uuid"
    ]
    return lines[0] if lines else ""


def _raw_machine_token() -> str:
    guid = _machine_guid()
    if guid:
        return "guid:" + guid
    uuid = _wmic_uuid()
    if uuid and uuid.upper() not in {"FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF", "00000000-0000-0000-0000-000000000000"}:
        return "uuid:" + uuid
    name = os.environ.get("COMPUTERNAME", "").strip() or "unknown"
    return "name:" + name


def get_machine_id() -> str:
    """Băm mã phần cứng thành TLHT-XXXX-XXXX-XXXX, cố định trên cùng một máy."""
    cached = getattr(get_machine_id, "_cached", "")
    if cached:
        return cached
    digest = hashlib.sha256(_raw_machine_token().encode("utf-8")).hexdigest().upper()
    body = digest[:12]
    machine_id = "TLHT-" + "-".join(body[i : i + 4] for i in range(0, 12, 4))
    setattr(get_machine_id, "_cached", machine_id)
    return machine_id


def _license_url() -> str:
    env = os.environ.get("TLHT_LICENSE_URL", "").strip()
    if env:
        return env
    return LICENSE_ONLINE_URL


def verify_license_online(email: str, device_id: str) -> bool:
    """Gửi Email và Mã máy tới hoangthiencm.id.vn. Chỉ máy status active mới mở khóa."""
    url = _license_url()
    clean_email = email.strip().lower()
    clean_device = device_id.strip().upper()
    body = json.dumps(
        {"action": "verify", "email": clean_email, "device_id": clean_device},
        ensure_ascii=False,
    ).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", "User-Agent": "TroLyHoangThien"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            raw = response.read().decode("utf-8", errors="replace")
    except (OSError, urllib.error.URLError, TimeoutError) as exc:
        _note(f"Không kết nối được hoangthiencm.id.vn. {exc}")
        return False
    text = raw.strip()
    if not text:
        _note("hoangthiencm.id.vn không trả nội dung. Hãy thử lại.")
        return False
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        _note("Phản hồi kích hoạt online không đọc được. Hãy thử lại.")
        return False
    if not isinstance(payload, dict):
        _note("Phản hồi kích hoạt online không đúng định dạng.")
        return False
    status = str(payload.get("status") or "").strip().lower()
    message = str(payload.get("message") or "").strip()
    record_email = str(payload.get("email") or clean_email).strip().lower()
    record_device = str(payload.get("device_id") or payload.get("device") or clean_device).strip().upper()
    if record_email != clean_email or record_device != clean_device:
        _note("Máy chủ trả về Email hoặc Mã máy khác với máy này.")
        return False
    if status == "active" or (payload.get("ok") is True and status in {"", "active"}):
        _note(message or "Đã kích hoạt online trên hoangthiencm.id.vn.")
        return True
    _note(message or "Chưa được duyệt trên hoangthiencm.id.vn. Thầy Thiên phê duyệt trên trang quản trị rồi bấm lại Kích hoạt bản quyền.")
    return False


def _sign(payload: dict) -> str:
    body = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hmac.new(_SECRET, body.encode("utf-8"), hashlib.sha256).hexdigest()


def save_activation(email: str, mode: str = "online") -> None:
    payload = {
        "email": email.strip(),
        "device_id": get_machine_id(),
        "mode": "online",
        "activated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }
    if mode != "online":
        _note("Chỉ lưu kích hoạt online.")
        return
    record = {"payload": payload, "sig": _sign(payload)}
    folder = license_home()
    folder.mkdir(parents=True, exist_ok=True)
    license_path().write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    _note("Đã lưu bản quyền.")


def current_license() -> dict | None:
    path = license_path()
    if not path.is_file():
        return None
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    payload = record.get("payload") if isinstance(record, dict) else None
    signature = record.get("sig") if isinstance(record, dict) else ""
    if not isinstance(payload, dict) or not isinstance(signature, str):
        return None
    if not hmac.compare_digest(signature, _sign(payload)):
        return None
    if str(payload.get("device_id") or "").upper() != get_machine_id():
        return None
    mode = str(payload.get("mode") or "")
    email = str(payload.get("email") or "").strip()
    if not email or mode != "online":
        return None
    return payload


def is_licensed() -> tuple[bool, str]:
    payload = current_license()
    if not payload:
        return False, ""
    return True, str(payload.get("email") or "")
