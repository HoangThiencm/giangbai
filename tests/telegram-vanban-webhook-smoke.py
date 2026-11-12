"""Static smoke checks for the Telegram document webhook.

The real Telegram token, database, and Google Drive credentials intentionally live
only on hosting, so this test verifies the deployment contract without secrets.
"""
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
webhook = (ROOT / 'api' / 'telegram_vanban.php').read_text(encoding='utf-8')
vanban = (ROOT / 'api' / 'vanban.php').read_text(encoding='utf-8')
worker = (ROOT / 'cloudflare-worker' / 'worker.js').read_text(encoding='utf-8')
config = (ROOT / 'api' / 'config.sample.php').read_text(encoding='utf-8')

for value in [
    'HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN', 'hash_equals',
    'TELEGRAM_VANBAN_ALLOWED_CHATS', 'getFile', 'api.telegram.org/file/bot',
    "['document']", "['photo']", 'vbd_parse_document',
    'vbd_store_downloaded_document_file', 'inline_keyboard',
    'callback_query', 'sector:(\\d+)', 'office_telegram_updates', 'tesseract',
]:
    assert value in webhook, f'Missing webhook contract: {value}'

for value in ['function vbd_detect_sector', 'function vbd_current_academic_year', 'function vbd_store_downloaded_document_file']:
    assert value in vanban, f'Missing shared document helper: {value}'

assert "'sector' =>" in vanban
assert 'sector: chỉ một trong hanhchinh, chuyenmon, dang' in worker

for value in ['TELEGRAM_VANBAN_BOT_TOKEN', 'TELEGRAM_VANBAN_WEBHOOK_SECRET', 'TELEGRAM_VANBAN_ALLOWED_CHATS', 'TELEGRAM_VANBAN_DEFAULT_OWNER_ID']:
    assert value in config, f'Missing configuration: {value}'

print('telegram-vanban-webhook smoke: OK')
