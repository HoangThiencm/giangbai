"""Kiểm tra agy.exe đã cài và đã đăng nhập AI hay chưa."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

CREATE_NO_WINDOW = 0x08000000


def app_dir() -> Path:
    """Thư mục gốc của app, kể cả khi đóng gói PyInstaller."""
    if getattr(sys, "frozen", False):
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            return Path(meipass)
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[1]


def writable_dir() -> Path:
    """Nơi ghi prompt tạm. Bản đóng gói không ghi vào thư mục giải nén."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return app_dir()


def find_agy() -> str | None:
    """Tìm agy.exe trên PATH rồi trong %LOCALAPPDATA%\\agy."""
    names = ("agy.exe", "agy") if sys.platform == "win32" else ("agy",)
    for name in names:
        found = shutil.which(name)
        if found and Path(found).is_file():
            return str(Path(found))
    local = os.environ.get("LOCALAPPDATA", "")
    roots = []
    if local:
        roots.append(Path(local) / "agy")
    for root in roots:
        direct = [root / "bin" / "agy.exe", root / "agy.exe", root / "bin" / "agy"]
        for path in direct:
            if path.is_file():
                return str(path)
        if root.is_dir():
            for path in root.rglob("agy.exe"):
                if path.is_file():
                    return str(path)
    return None


def check_agy_installed() -> tuple[bool, str]:
    path = find_agy()
    if path:
        return True, path
    return False, "Chưa tìm thấy agy.exe trong PATH hoặc %LOCALAPPDATA%\\agy"


def _model_names(stdout: str) -> list[str]:
    names: list[str] = []
    for model_id, _label in _parse_model_table(stdout):
        names.append(model_id)
    if names:
        return names
    for raw in (stdout or "").splitlines():
        line = raw.strip()
        if not line:
            continue
        lowered = line.lower()
        if lowered.startswith("fetch") or lowered.startswith("usage"):
            continue
        token = line.split()[0].strip()
        if token and any(char.isalpha() for char in token) and "\\" not in token:
            names.append(token)
    return names


def _parse_model_table(stdout: str) -> list[tuple[str, str]]:
    """Đọc bảng `id<TAB>tên` từ stdout của `agy models`."""
    models: list[tuple[str, str]] = []
    for raw in (stdout or "").splitlines():
        parts = [part.strip() for part in raw.split("\t") if part.strip()]
        if not parts:
            continue
        if parts[0].lower().startswith(("fetch", "usage")):
            continue
        if len(parts) >= 2:
            models.append((parts[0], parts[1]))
        elif " " not in parts[0]:
            models.append((parts[0], parts[0]))
    return models


def fetch_available_models(timeout: float = 45) -> list[tuple[str, str]]:
    """Trả đúng các dòng `agy models` in ra. Không có danh sách giả lập."""
    agy = find_agy()
    if not agy:
        return []
    flags = CREATE_NO_WINDOW if sys.platform == "win32" else 0
    try:
        res = subprocess.run(
            [agy, "models"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            cwd=str(writable_dir()),
            creationflags=flags,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    if res.returncode != 0:
        return []
    return _parse_model_table(res.stdout)


def check_agy_login(timeout: float = 45) -> tuple[bool, str]:
    """Chạy `agy models`. Đã đăng nhập thì trả (True, tên model)."""
    installed, agy_or_reason = check_agy_installed()
    if not installed:
        return False, agy_or_reason
    flags = CREATE_NO_WINDOW if sys.platform == "win32" else 0
    try:
        completed = subprocess.run(
            [agy_or_reason, "models"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            cwd=str(writable_dir()),
            creationflags=flags,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return False, "Lệnh agy models quá thời gian chờ"
    except OSError as exc:
        return False, str(exc)
    models = _model_names(completed.stdout)
    if completed.returncode == 0 and models:
        return True, models[0]
    blob = f"{completed.stdout}\n{completed.stderr}".strip()
    reason = blob or f"agy models thoát với mã {completed.returncode}"
    return False, reason[:500]


def open_agy_install() -> None:
    """Mở PowerShell để người dùng thấy script cài agy chính thức."""
    command = "irm https://antigravity.google/cli/install.ps1 | iex"
    subprocess.Popen(
        ["powershell.exe", "-NoExit", "-ExecutionPolicy", "Bypass", "-Command", command]
    )


def open_agy_login() -> tuple[bool, str]:
    """Mở cửa sổ lệnh `agy` để đăng nhập Google."""
    installed, agy_or_reason = check_agy_installed()
    if not installed:
        return False, agy_or_reason
    subprocess.Popen(
        ["cmd.exe", "/c", "start", "Dang nhap AGY", "cmd.exe", "/k", agy_or_reason],
        cwd=str(writable_dir()),
    )
    return True, agy_or_reason
