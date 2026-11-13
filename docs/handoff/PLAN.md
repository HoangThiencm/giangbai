# PLAN

## Hiện trạng
1. **Phân hệ Quản lý văn bản:** Đã có giao diện đầy đủ chia theo 3 lĩnh vực tại `quanlyvanban.html`, `quanlyvanban-hanhchinh.html`, `quanlyvanban-chuyenmon.html`, `quanlyvanban-dang.html`, được điều hướng bởi `vanban-hub.js` và xử lý logic bởi `vanban-app.js`.
2. **Cơ sở dữ liệu & Lưu trữ:**
   - Bảng MySQL `office_documents` đã có sẵn các trường: `owner_id`, `academic_year`, `sector` (`hanhchinh`, `chuyenmon`, `dang`), `direction` (`incoming`/`outgoing`), `document_number`, `title`, `document_date`, `organization`, `document_type`, `summary_text`, `source_text`, `report_required`, `report_due_at`, `report_status`, `report_note`, `drive_folder_id`.
   - Bảng `office_document_files` lưu thông tin tệp, liên kết xem/tải từ Google Drive hoặc local storage fallback (`storage/vanban/`).
   - Cây thư mục Google Drive đã chuẩn hóa: `04_QUAN_LY_VAN_BAN/<SECTOR>/NAM_HOC_<YEAR>/<VAN_BAN_DEN|VAN_BAN_DI>/<Số hiệu - Trích yếu>/`.
3. **Trích xuất thông tin (AI / Regex):**
   - Đã có hàm `vbd_parse_document($source)` trong `api/vanban.php` kết hợp regex tiếng Việt và AI qua Cloudflare Workers AI (`cloudflare-worker/worker.js` mode `document`) để nhận diện số ký hiệu, ngày ban hành, nơi ban hành, trích yếu, yêu cầu và hạn báo cáo.
4. **Khoảng trống cần bổ sung:**
   - Chưa có cổng tiếp nhận tự động (Webhook) kết nối với Telegram Bot API.
   - Chưa có cơ chế tải tệp đính kèm tự động từ tin nhắn Telegram (PDF/ảnh), chuyển giao cho bộ trích xuất, tự động phân loại lĩnh vực (`sector`), lưu vào CSDL, đẩy tệp lên Google Drive và gửi phản hồi tương tác kèm nút bấm (Inline Keyboard) để người dùng xác nhận/đổi lĩnh vực trực tiếp trong nhóm Telegram.

## Phạm vi
1. **Endpoint tiếp nhận Telegram Webhook (`api/telegram_vanban.php`):**
   - Tiếp nhận sự kiện Telegram Webhook, bảo mật bằng header `X-Telegram-Bot-Api-Secret-Token`.
   - Lọc kiểm tra quyền hạn qua danh sách `TELEGRAM_ALLOWED_CHAT_IDS` (nhóm hoặc cá nhân được phép gửi văn bản).
   - Xử lý các tin nhắn có tệp tài liệu (`document`: PDF, DOCX...) hoặc ảnh (`photo`).
2. **Tải tệp & Xử lý nội dung:**
   - Tải tệp từ Telegram Bot API (`getFile` $\rightarrow$ tải binary về thư mục đệm an toàn).
   - Trích xuất văn bản từ tệp (đọc text layer từ PDF hoặc gửi sang AI phân tích).
   - Nâng cấp bộ nhận diện để tự động gán nhãn lĩnh vực (`sector` là `hanhchinh`, `chuyenmon`, hoặc `dang`) dựa vào cơ quan ban hành, thể thức và trích yếu.
3. **Lưu trữ hệ thống:**
   - Tạo bản ghi mới trong `office_documents` với năm học hiện hành và người sở hữu mặc định (`TELEGRAM_DEFAULT_OWNER_ID` hoặc admin).
   - Đẩy tệp lên Google Drive đúng cấu trúc thư mục theo lĩnh vực và ghi bản ghi vào `office_document_files`.
4. **Phản hồi & Tương tác trên Telegram:**
   - Gửi tin nhắn thông báo kết quả nhận diện rõ ràng (Số/Ký hiệu, Ngày ban hành, Nơi gửi, Trích yếu, Hạn xử lý, Lĩnh vực tự động phân loại, Link xem trên web).
   - Gắn nút bấm Inline Keyboard: `[✅ Xác nhận]`, `[🏛 Chuyển Hành chính]`, `[🎓 Chuyển Chuyên môn]`, `[🚩 Chuyển Đảng]`.
   - Xử lý `callback_query` khi người dùng bấm nút: cập nhật ngay trường `sector` hoặc trạng thái trong CSDL và sửa tin nhắn phản hồi của Bot để xác nhận thao tác thành công.
5. **Cấu hình & Quản trị:**
   - Bổ sung các hằng số cấu hình vào `api/config.sample.php` và hỗ trợ nạp từ `api/config.php` hoặc `global_config.json`.

## Ngoài phạm vi
1. Tích hợp trực tiếp Zalo OA (để dành triển khai ở giai đoạn tiếp theo sau khi hệ sinh thái Telegram hoạt động ổn định).
2. Thay đổi giao diện web (`quanlyvanban*.html`) hay các tính năng cốt lõi khác của hệ sinh thái (KHBD, padlet, sổ điểm...).
3. Xử lý các tệp vượt quá 20MB (giới hạn download của Telegram Bot API tiêu chuẩn).

## File dự kiến tác động
1. `api/telegram_vanban.php` (Tạo mới): Endpoint Webhook tiếp nhận, tải tệp, gọi nhận diện, ghi DB/Drive và gửi/sửa tin nhắn Telegram.
2. `api/vanban.php`: Tinh chỉnh/export các hàm nghiệp vụ (`vbd_parse_document`, `vbd_save_document`, `vbd_upload_document_file_to_drive`, `vbd_academic_year_current`) để tái sử dụng an toàn từ CLI/Webhook mà không phụ thuộc phiên đăng nhập web người dùng.
3. `cloudflare-worker/worker.js`: Bổ sung trường `sector` (`hanhchinh`, `chuyenmon`, `dang`) vào prompt trích xuất văn bản trong mode `document`.
4. `api/config.sample.php`: Bổ sung tài liệu và các hằng số cấu hình:
   - `TELEGRAM_VANBAN_BOT_TOKEN`
   - `TELEGRAM_VANBAN_WEBHOOK_SECRET`
   - `TELEGRAM_VANBAN_ALLOWED_CHATS`
   - `TELEGRAM_VANBAN_DEFAULT_OWNER_ID`
5. `tests/telegram-vanban-webhook-smoke.py` (Tạo mới): Kịch bản kiểm thử giả lập Webhook Telegram với tài liệu PDF mẫu, xác thực token, kiểm tra phân loại lĩnh vực và cập nhật callback.

## Các bước thực hiện
1. **Bước 1 - Cấu hình & Định hình phân loại lĩnh vực:**
   - Bổ sung nhận diện `sector` trong regex/AI của `api/vanban.php` và `cloudflare-worker/worker.js`:
     - Nhận diện `dang`: Cơ quan Đảng (Đảng ủy, Chi bộ, Ban Tuyên giáo, UBKT...), thể thức ký hiệu (-NQ/CB, -QĐ/ĐU...), Hướng dẫn 05-HD/VPTW.
     - Nhận diện `chuyenmon`: Phòng/Sở GD&ĐT, Tổ chuyên môn, nội dung liên quan dạy học, thi đua giáo viên/học sinh, đề kiểm tra, thời khóa biểu...
     - Nhận diện `hanhchinh`: Các văn bản điều hành chung, tài chính, cơ sở vật chất, PCCC, công văn hành chính theo NĐ 30/2020/NĐ-CP.
2. **Bước 2 - Xây dựng Endpoint Webhook (`api/telegram_vanban.php`):**
   - Kiểm tra `X-Telegram-Bot-Api-Secret-Token`.
   - Xử lý payload JSON gửi từ Telegram:
     - Lọc theo `chat.id` hợp lệ.
     - Kiểm tra nếu tin nhắn có `document` (lấy `file_id`, `file_name`, `mime_type`) hoặc `photo` (lấy ảnh kích thước lớn nhất).
     - Gửi tin nhắn tạm thời phản hồi người dùng: *"⏳ Đang tiếp nhận và phân tích văn bản..."*
3. **Bước 3 - Tải tệp & Trích xuất:**
   - Gọi API Telegram `https://api.telegram.org/bot<TOKEN>/getFile?file_id=<ID>` để lấy `file_path`.
   - Tải file nhị phân về thư mục tạm `storage/vanban_temp/`.
   - Trích xuất văn bản:
     - Với PDF dạng text: dùng parser trích xuất văn bản trang đầu (1-3 trang).
     - Gửi nội dung qua `vbd_parse_document()` (kết hợp Cloudflare AI Worker) để lấy toàn bộ trường thông tin kèm `sector`.
4. **Bước 4 - Lưu trữ dữ liệu & Tệp:**
   - Ghi bản ghi vào `office_documents` với các thông tin đã bóc tách.
   - Gọi cơ chế lưu trữ Google Drive (`google_drive.php`) hoặc fallback lưu local, ghi bản ghi vào `office_document_files`.
   - Dọn dẹp tệp tạm trong `storage/vanban_temp/`.
5. **Bước 5 - Phản hồi Telegram với Inline Keyboard:**
   - Chỉnh sửa (editMessageText) tin nhắn tạm thời thành tin nhắn chi tiết:
     ```text
     📄 ĐÃ TIẾP NHẬN VĂN BẢN
     - Lĩnh vực: [Hành chính / Chuyên môn / Đảng]
     - Số/Ký hiệu: ...
     - Ngày ban hành: ...
     - Cơ quan ban hành: ...
     - Trích yếu: ...
     - Hạn báo cáo: ...
     - Tệp đính kèm: [Tên file] (Đã lưu Drive)
     ```
   - Đính kèm cụm nút:
     - Dòng 1: `[🏛 Chuyển Hành chính]` | `[🎓 Chuyển Chuyên môn]` | `[🚩 Chuyển Đảng]`
     - Dòng 2: `[✅ Xác nhận chính xác]` | `[🔗 Mở trên Web]`
6. **Bước 6 - Xử lý Callback Query:**
   - Khi người dùng bấm nút đổi lĩnh vực (`action:set_sector:<doc_id>:<sector>`), cập nhật cột `sector` trong CSDL `office_documents`.
   - Cập nhật tin nhắn Telegram phản ánh trạng thái mới, thông báo popup `answerCallbackQuery` cho người bấm.
7. **Bước 7 - Tự động hóa kiểm thử:**
   - Viết script kiểm thử smoke test `tests/telegram-vanban-webhook-smoke.py` kiểm tra mọi luồng: xác thực secret, gửi payload giả lập, bóc tách dữ liệu, cập nhật callback.

## Rủi ro
1. **Tệp scan không có text layer:**
   - *Rủi ro:* Trình đọc PDF không lấy được chữ khiến AI không nhận diện được trích yếu.
   - *Giảm thiểu:* Khi văn bản trích xuất được dưới 50 ký tự, fallback sử dụng OCR của Gemini API hoặc cảnh báo trên Telegram để người dùng nhập/sửa trích yếu thủ công qua nút bấm.
2. **Giới hạn kích thước file của Telegram Bot API:**
   - *Rủi ro:* Bot tiêu chuẩn chỉ tải được tệp tối đa 20MB.
   - *Giảm thiểu:* Kiểm tra `file_size` ngay trong payload; nếu quá 20MB, phản hồi thông báo hướng dẫn người dùng nén hoặc tải trực tiếp trên giao diện web.
3. **Thời gian xử lý vượt quá timeout của Telegram Webhook (thường là 50-60s):**
   - *Rủi ro:* Nếu tải file từ Telegram + gọi AI + upload Google Drive mất nhiều thời gian, Telegram có thể gửi lại request trùng lặp.
   - *Giảm thiểu:* Phản hồi HTTP 200 sớm hoặc sử dụng cURL non-blocking/cơ chế queue nhanh, kiểm tra trùng lặp qua `message_id` hoặc mã định danh của tin nhắn.
4. **An toàn bảo mật:**
   - *Rủi ro:* Kẻ xấu gửi webhook giả mạo hoặc spam nhóm chat.
   - *Giảm thiểu:* Bắt buộc kiểm tra token bí mật (`secret_token`) và whitelist ID nhóm chat được phép sử dụng.

## Cách kiểm thử
1. **Kiểm thử đơn vị & API nội bộ:**
   - Chạy smoke test script kiểm tra `telegram_vanban.php` với header hợp lệ và không hợp lệ (kỳ vọng mã 403 Forbidden khi thiếu secret token).
   - Kiểm tra hàm trích xuất `vbd_parse_document` với các chuỗi trích yếu văn bản Đảng, Chuyên môn, Hành chính để đảm bảo trường `sector` trả về chính xác.
2. **Kiểm thử tích hợp Telegram Webhook:**
   - Giả lập payload JSON của Telegram gửi văn bản PDF vào webhook.
   - Kiểm tra bản ghi xuất hiện trong MySQL `office_documents` với đầy đủ số ký hiệu, trích yếu, lĩnh vực.
   - Kiểm tra tệp đính kèm được lưu trong `office_document_files`.
   - Giả lập bấm nút inline callback query đổi lĩnh vực từ Hành chính sang Đảng, kiểm tra DB cập nhật thành công.
3. **Kiểm thử giao diện:**
   - Mở `quanlyvanban-hanhchinh.html`, `quanlyvanban-chuyenmon.html`, `quanlyvanban-dang.html` để kiểm tra văn bản vừa được bot đẩy vào hiển thị đúng danh mục và có thể tải/xem tệp.

## Tiêu chí nghiệm thu
1. Có file `api/telegram_vanban.php` hoạt động chuẩn, bảo mật bằng Secret Token và lọc Chat ID.
2. Bot tự động bóc tách được số hiệu, ngày ban hành, trích yếu, hạn báo cáo và phân loại chính xác 3 lĩnh vực (Hành chính / Chuyên môn / Đảng).
3. Văn bản và tệp đính kèm được tự động lưu vào CSDL và Google Drive theo cấu trúc chuẩn của hệ thống hiện tại.
4. Tin nhắn phản hồi trên Telegram có đầy đủ thông tin tóm tắt và các nút bấm Inline Keyboard cho phép chuyển đổi lĩnh vực linh hoạt.
5. Kịch bản kiểm thử smoke test tự động chạy thành công mà không có lỗi.
