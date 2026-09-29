"""Smoke: chuyển sang Chuyên môn giữ nguyên bản gốc Hành chính."""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
PHP = (ROOT / "api" / "vanban.php").read_text(encoding="utf-8")
APP = (ROOT / "vanban-app.js").read_text(encoding="utf-8")
ADMIN = (ROOT / "quanlyvanban-hanhchinh.html").read_text(encoding="utf-8")

failures: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    if ok:
        print(f"PASS  {name}")
        return
    failures.append(name if not detail else f"{name}: {detail}")
    print(f"FAIL  {name}" + (f" — {detail}" if detail else ""))


def extract_php_function(name: str) -> str:
    match = re.search(rf"function {name}\(.*?\n\{{", PHP)
    if not match:
        return ""
    start = match.end() - 1
    depth = 0
    for index in range(start, len(PHP)):
        char = PHP[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return PHP[match.start() : index + 1]
    return ""


def extract_action_block() -> str:
    marker = "if ($action === 'transfer_sector' || $action === 'copy_sector')"
    start = PHP.find(marker)
    if start < 0:
        return ""
    next_action = PHP.find("\nif ($action ===", start + len(marker))
    return PHP[start:next_action if next_action > start else None]


def extract_js_function(name: str) -> str:
    match = re.search(rf"function {name}\(", APP)
    if not match:
        return ""
    brace = APP.find("{", match.end())
    if brace < 0:
        return ""
    depth = 0
    for index in range(brace, len(APP)):
        char = APP[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return APP[match.start() : index + 1]
    return ""


action = extract_action_block()
copy_files = extract_php_function("vbd_copy_document_files")
copy_storage = extract_php_function("vbd_copy_local_storage")
delete_storage = extract_php_function("vbd_delete_document_file_storage")
move_ui = extract_js_function("moveToChuyenMon")

check("khối transfer_sector/copy_sector còn tồn tại", bool(action))
check(
    "transfer_sector không UPDATE sector của bản ghi gốc",
    "UPDATE office_documents SET sector" not in action and "vbd_move_local_storage(" not in action,
)
check(
    "transfer_sector tạo bản ghi tích hợp",
    "INSERT INTO office_documents" in action and "vbd_copy_document_files(" in action,
)
check(
    "thông điệp chuyển giữ bản gốc Hành chính",
    "Đã chuyển ' . count($created) . ' văn bản sang ' . $label . ' (bản gốc tại Hành chính được giữ nguyên)." in action,
)
check("copy_sector vẫn còn thông điệp sao chép", "Đã sao chép ' . count($created)" in action)
check("action name transfer_sector và copy_sector giữ nguyên", "transfer_sector" in action and "copy_sector" in action)

check("có hàm vbd_copy_local_storage", "function vbd_copy_local_storage(" in copy_storage)
check("sao chép tệp vật lý bằng copy()", "@copy($src, $dst)" in copy_storage)
check("không di chuyển thư mục gốc khi sao chép", "rename(" not in copy_storage)

check("vbd_copy_document_files nhận fromDoc và toDoc", "array $fromDoc, array $toDoc" in copy_files)
check(
    "tệp cục bộ được tạo lại view_url và download_url theo document_id mới",
    "vbd_is_local_file_id" in copy_files
    and "vbd_local_file_url($toId, $storedName, false)" in copy_files
    and "vbd_local_file_url($toId, $storedName, true)" in copy_files,
)
check(
    "sau khi sao chép bản ghi thì sao chép thư mục tệp cục bộ",
    "vbd_copy_local_storage($fromId, $fromDoc, $toId, $toDoc)" in copy_files,
)

shared_sql = "SELECT COUNT(*) FROM office_document_files WHERE drive_file_id = ? AND document_id != ?"
check("có câu truy vấn đếm tệp Drive dùng chung", shared_sql in delete_storage)
delete_guard = delete_storage.find(shared_sql)
delete_call = delete_storage.find("drive_delete_file(")
check(
    "không xóa tệp Drive dùng chung trước khi đếm tham chiếu",
    delete_guard >= 0 and delete_call > delete_guard and "return null;" in delete_storage[delete_guard:delete_call],
)

check(
    "xác nhận chuyển nói rõ bản gốc Hành chính vẫn được lưu trữ",
    "Chuyển ${unique.length} văn bản sang Chuyên môn (bản gốc tại Hành chính vẫn được lưu trữ)?" in move_ui,
)
check("sau khi chuyển hiển thị data.message", "data.message" in move_ui)
check("sau khi chuyển tải lại danh sách Hành chính", "await load()" in move_ui)
check("UI vẫn gọi transfer_sector và copy_sector", "transfer_sector" in move_ui and "copy_sector" in move_ui)
check("nút dòng vẫn là data-action=\"transfer\"", 'data-action="transfer"' in APP)
check("modal vẫn có data-detail-action transfer và copy", 'data-detail-action="transfer"' in APP and 'data-detail-action="copy"' in APP)
check("nhãn nút Chuyển sang Chuyên môn còn nguyên", "Chuyển sang Chuyên môn" in APP)
check("nhãn nút Sao chép sang Chuyên môn còn nguyên", "Sao chép sang Chuyên môn" in APP)

check("giữ id transferSelectedBtn", 'id="transferSelectedBtn"' in ADMIN)
check("giữ id copySelectedBtn", 'id="copySelectedBtn"' in ADMIN)
check("nhãn chuyển hàng loạt còn nguyên", "Chuyển đã chọn sang Chuyên môn" in ADMIN)
check("nhãn sao chép hàng loạt còn nguyên", "Sao chép đã chọn sang Chuyên môn" in ADMIN)

php_bin = shutil.which("php")
if php_bin:
    syntax = subprocess.run([php_bin, "-l", str(ROOT / "api" / "vanban.php")], capture_output=True, text=True)
    check("cú pháp api/vanban.php", syntax.returncode == 0, (syntax.stdout or syntax.stderr).strip())
else:
    check("cú pháp api/vanban.php", PHP.count("{") == PHP.count("}"), "không có php, đối chiếu số ngoặc")

if failures:
    print(f"\nFAIL: {len(failures)} kiểm tra chưa đạt.")
    for item in failures:
        print(f" - {item}")
    sys.exit(1)

print("\nPASS: giữ bản gốc Hành chính khi chuyển sang Chuyên môn.")
