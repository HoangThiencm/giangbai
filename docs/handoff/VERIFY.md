# VERIFY: Bot Telegram Quản lý văn bản (ngày ban hành, thể loại, trích yếu, phản hồi menu)

## Kết quả kiểm tra local của Coder: PASS

Bản PASS cũ (sửa GitHub Actions / obfuscate) không còn là kết quả của plan hiện tại.

### Đã chạy

- `php -l` với PHP 8.3.36 và mbstring: `api/pdf_text_extractor.php`, `api/vanban.php`, `api/telegram_vanban.php`. Không lỗi cú pháp.
- `python tests/telegram-vanban-webhook-smoke.py` in `telegram-vanban-webhook smoke: OK`.
- Ca synthetic và PDF `KH THI GIÁO VIÊN DẠY GỎI THCS - 2026-2027 pH.pdf`: thể loại `Kế hoạch`, trích yếu hội thi đủ câu, số `/KH-SGDĐT`, ngày `2026-11-12`. Không còn `4200/SGDĐT-GDPT` hay `2019-12-20`.

### Chưa kiểm

- Webhook Telegram thật (đổi lĩnh vực, modal xác nhận).
- `/verify` độc lập của Antigravity IDE.

## Việc tiếp theo

Antigravity IDE, chat mới: `/verify`.
