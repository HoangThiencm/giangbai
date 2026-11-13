"""Static and runtime smoke checks for the Telegram document webhook.

The real Telegram token, database, and Google Drive credentials intentionally live
only on hosting, so this test verifies the deployment contract without secrets.
PDF text is extracted with the pure-PHP reader, without pdftotext.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
webhook = (ROOT / 'api' / 'telegram_vanban.php').read_text(encoding='utf-8')
vanban = (ROOT / 'api' / 'vanban.php').read_text(encoding='utf-8')
extractor = (ROOT / 'api' / 'pdf_text_extractor.php').read_text(encoding='utf-8')
worker = (ROOT / 'cloudflare-worker' / 'worker.js').read_text(encoding='utf-8')
config = (ROOT / 'api' / 'config.sample.php').read_text(encoding='utf-8')

for value in [
    'HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN', 'hash_equals',
    'TELEGRAM_VANBAN_ALLOWED_CHATS', 'getFile', 'api.telegram.org/file/bot',
    "['document']", "['photo']", 'vbd_parse_document',
    'vbd_store_downloaded_document_file', 'inline_keyboard',
    'callback_query', 'sector:(\\d+)', 'office_telegram_updates', 'tesseract',
    'vbd_pdf_extract_text', 'message is not modified',
    'owner_id=? OR owner_id=0 OR owner_id IS NULL',
    '[• ', '<b>Thể loại:</b>', 'show_alert',
    'Đã chuyển lĩnh vực sang', 'Đã xác nhận thông tin văn bản #',
    'merge:(\\d+):(\\d+)', 'Ghép vào VB trước', 'INTERVAL 30 MINUTE',
    'Đã ghép tệp vào Văn bản #', 'Đã chuyển tệp sang làm phụ lục',
]:
    assert value in webhook, f'Missing webhook contract: {value}'
for value in ['office_telegram_edits', 'Sửa từng mục', 'tvb_needs_manual', 'tvb_edit_begin']:
    assert value not in webhook, f'Wizard còn sót: {value}'

for value in [
    'function vbd_detect_sector', 'function vbd_current_academic_year',
    'function vbd_store_downloaded_document_file', 'function vbd_find_document_number',
    'function vbd_match_type_line', 'pdf_text_extractor.php',
]:
    assert value in vanban, f'Missing shared document helper: {value}'

assert "'sector' =>" in vanban
assert 'sector: chỉ một trong hanhchinh, chuyenmon, dang' in worker
assert 'function vbd_pdf_extract_text' in extractor
assert 'FlateDecode' in extractor and 'beginbfchar' in extractor and 'beginbfrange' in extractor
assert "if ($op === 'BT' || $op === 'ET')" in extractor
assert '$newline();' in extractor.split("if ($op === 'BT' || $op === 'ET')", 1)[1][:80]
assert 'stripos($head, $type)' not in vanban

for value in ['TELEGRAM_VANBAN_BOT_TOKEN', 'TELEGRAM_VANBAN_WEBHOOK_SECRET', 'TELEGRAM_VANBAN_ALLOWED_CHATS', 'TELEGRAM_VANBAN_DEFAULT_OWNER_ID']:
    assert value in config, f'Missing configuration: {value}'

main = webhook.split("if (!is_array($payload)", 1)[1]
update_at = main.find("$updateId = (int)($payload['update_id'] ?? 0);")
callback_at = main.find("callback_query")
assert 0 <= update_at < callback_at, 'update_id phải được gán trước khi xử lý callback'

callback = webhook.split('function tvb_process_callback', 1)[1].split('\nfunction ', 1)[0]
answer_at = callback.find('tvb_answer_callback')
edit_at = callback.find('tvb_edit_callback_message')
assert 0 <= answer_at < edit_at, 'answerCallbackQuery phải chạy trước editMessageText'
edit = webhook.split('function tvb_edit_callback_message', 1)[1].split('\nfunction ', 1)[0]
assert 'message is not modified' in edit
assert "Đã chọn " in callback and 'Đã xác nhận' in callback


def find_php() -> str:
    env = os.environ.get('PHP_BIN', '').strip()
    candidates = [env] if env else []
    which = shutil.which('php')
    if which:
        candidates.append(which)
    portable = Path(os.environ.get('TEMP', '/tmp')) / 'php-portable-834' / 'php.exe'
    candidates.append(str(portable))
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return candidate
    raise SystemExit('Không tìm thấy php để kiểm tra bóc tách PDF')


def find_pdf(folder: Path, prefix: str) -> Path | None:
    if not folder.is_dir():
        return None
    for path in folder.iterdir():
        if path.is_file() and path.suffix.lower() == '.pdf' and path.name.startswith(prefix):
            return path
    return None


php = find_php()
ext = str(Path(php).resolve().parent / 'ext')
runner = r'''<?php
define('VBD_SKIP_BOOT', true);
require $argv[1];
$draft = $argv[2] ?? '';
$contest = $argv[3] ?? '';
$out = ['cases' => []];
$readPdf = static function (string $path): array {
    $text = vbd_pdf_extract_text($path, 2);
    $parsed = vbd_regex_extract($text);
    return [
        'chars' => function_exists('mb_strlen') ? mb_strlen($text, 'UTF-8') : strlen($text),
        'has_vietnamese' => str_contains($text, 'KẾ HOẠCH'),
        'separated' => !str_contains($text, 'KẾ HOẠCHTổ chức') && !str_contains($text, 'KẾ HOẠCHHoạt'),
        'number' => $parsed['document_number'] ?? '',
        'type' => $parsed['document_type'] ?? '',
        'title' => $parsed['title'] ?? '',
        'date' => $parsed['document_date'] ?? '',
    ];
};
if ($draft !== '' && is_file($draft)) $out['pdf'] = $readPdf($draft);
if ($contest !== '' && is_file($contest)) $out['contest'] = $readPdf($contest);
$samples = [
    'admin' => "Số: 03 / KH - CM\nKẾ HOẠCH\nHoạt động chuyên môn tháng 11/2026\n",
    'party_qd' => "ĐẢNG ỦY TRƯỜNG\nSố: 193-QĐ/THCS\nQUYẾT ĐỊNH\nBan hành kế hoạch kiểm tra nội bộ tháng 11\n",
    'party_hd' => "Số: 02-HD/ĐU\nHƯỚNG DẪN\nTuyên truyền học tập nghị quyết tháng 11\n",
    'congvan' => "ỦY BAN NHÂN DÂN PHƯỜNG\nSố: 663/UBND-VP\nKính gửi: Các đơn vị\nV/v hướng dẫn thực hiện chuyên môn tháng 11\nCăn cứ Công văn số 2747/SGDĐT-GDPT ngày 22/10/2025 về việc khác\n",
    'spaced' => "Số: 45 / QĐ - SGDĐT\nV/v Triển khai chuyên môn tháng chín\nKính gửi: Hiệu trưởng\n",
    'blank_number' => "/M(D:20261112)\nSố: /KH-SGDĐT\nĐồng Nai, ngày tháng 11 năm 2026\nKẾ HOẠCH\nTổ chức Hội thi giáo viên dạy giỏi cơ sở giáo dục Trung học cơ sở\ncấp thành phố năm học 2026 - 2027\nCăn cứ Thông tư số 22/2019/TT-BGDĐT ngày 20/12/2019\nThực hiện Công văn số 4200/SGDĐT-GDPT&GDTX ngày 22/8/2026\n",
];
foreach ($samples as $name => $sample) {
    $parsed = vbd_regex_extract($sample);
    $out['cases'][$name] = [
        'number' => $parsed['document_number'] ?? '',
        'type' => $parsed['document_type'] ?? '',
        'title' => $parsed['title'] ?? '',
        'date' => $parsed['document_date'] ?? '',
    ];
}
echo json_encode($out, JSON_UNESCAPED_UNICODE);
'''
def find_contest() -> Path | None:
    folders = [Path.home() / 'Desktop', Path.home() / 'Documents', ROOT]
    for folder in folders:
        if not folder.is_dir():
            continue
        for path in folder.glob('*.pdf'):
            lowered = path.name.lower()
            if '2026-2027' in lowered and lowered.endswith('ph.pdf'):
                return path
    return None


draft = find_pdf(ROOT / 'TROLYTHIEN' / '8_TAO_BAO_CAO' / 'Dau_vao' / '09.11' / 'VAN BAN TRIEN KHAI', 'D')
contest = find_contest()
with tempfile.NamedTemporaryFile('w', suffix='.php', delete=False, encoding='utf-8') as handle:
    handle.write(runner)
    runner_path = handle.name
try:
    command = [php]
    if Path(ext).is_dir():
        command += ['-d', f'extension_dir={ext}', '-d', 'extension=mbstring']
    command += [runner_path, str(ROOT / 'api' / 'vanban.php'), str(draft or ''), str(contest or '')]
    completed = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
finally:
    os.remove(runner_path)
if completed.returncode != 0:
    sys.stderr.write(completed.stderr or completed.stdout)
    raise SystemExit(f'PHP smoke failed ({completed.returncode})')
if 'Warning' in (completed.stderr or '') or 'Fatal' in (completed.stderr or ''):
    sys.stderr.write(completed.stderr)
    raise SystemExit('PHP smoke in ra cảnh báo')
payload = json.loads(completed.stdout)
cases = payload['cases']
assert cases['admin']['number'] == '03/KH-CM', cases['admin']
assert cases['admin']['type'] == 'Kế hoạch', cases['admin']
assert cases['admin']['title'] == 'Hoạt động chuyên môn tháng 11/2026', cases['admin']
assert cases['party_qd']['number'] == '193-QĐ/THCS', cases['party_qd']
assert cases['party_qd']['type'] == 'Quyết định', cases['party_qd']
assert 'kiểm tra nội bộ' in cases['party_qd']['title'], cases['party_qd']
assert cases['party_hd']['number'] == '02-HD/ĐU', cases['party_hd']
assert cases['party_hd']['type'] == 'Hướng dẫn', cases['party_hd']
assert cases['congvan']['number'] == '663/UBND-VP', cases['congvan']
assert cases['congvan']['type'] == 'Công văn', cases['congvan']
assert cases['congvan']['title'].startswith('hướng dẫn thực hiện'), cases['congvan']
assert cases['spaced']['number'] == '45/QĐ-SGDĐT', cases['spaced']
assert cases['spaced']['type'] == 'Quyết định', cases['spaced']
blank = cases['blank_number']
assert blank['number'] == '/KH-SGDĐT', blank
assert blank['type'] == 'Kế hoạch', blank
assert blank['title'] == 'Tổ chức Hội thi giáo viên dạy giỏi cơ sở giáo dục Trung học cơ sở cấp thành phố năm học 2026 - 2027', blank
assert blank['date'] == '2026-11-12', blank
assert '4200' not in blank['number'] and blank['date'] != '2019-12-20'
if draft is not None:
    pdf = payload.get('pdf') or {}
    assert pdf.get('chars', 0) > 80, pdf
    assert pdf.get('has_vietnamese') is True, pdf
    assert pdf.get('number') == '03/KH-CM', pdf
    assert pdf.get('type') == 'Kế hoạch', pdf
    assert pdf.get('title') == 'Hoạt động chuyên môn tháng 11/2026', pdf
else:
    raise SystemExit('Thiếu PDF mẫu DỰ THẢO KE HOACH CM THANG 11.pdf')
if contest is None:
    raise SystemExit('Thiếu PDF mẫu KH THI GIÁO VIÊN DẠY GIỎI THCS 2026-2027 pH.pdf')
contest_pdf = payload.get('contest') or {}
assert contest_pdf.get('separated') is True, contest_pdf
assert contest_pdf.get('type') == 'Kế hoạch', contest_pdf
assert contest_pdf.get('title') == 'Tổ chức Hội thi giáo viên dạy giỏi cơ sở giáo dục Trung học cơ sở cấp thành phố năm học 2026 - 2027', contest_pdf
assert contest_pdf.get('number') == '7400/KH-SGDĐT', contest_pdf
assert contest_pdf.get('date') == '2026-11-12', contest_pdf
assert '4200' not in str(contest_pdf.get('number'))
assert contest_pdf.get('date') != '2019-12-20'

print('telegram-vanban-webhook smoke: OK')
