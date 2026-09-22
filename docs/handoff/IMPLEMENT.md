# IMPLEMENT: Hoàn thiện nhánh Hoạt động B khi 1-Click Generate

## Phạm vi đã thực hiện

- `js/khbd-app.js`: Chuẩn hóa các tiêu đề nhánh SGK như `### 2. ...`, `### Hoạt động 2:` và `### Mục 2:` về dạng `### Hoạt động 2.2: ...` trước khi kiểm tra.
- `js/khbd-app.js`: Khi thiếu nhánh 2.k, chỉ yêu cầu AI sinh riêng nhánh đó rồi nối vào nội dung hiện có; không gửi lại toàn bộ Hoạt động B để sửa.
- `js/khbd-app.js`: Nếu AI vẫn thiếu nhánh hoặc lỗi khi sinh bổ sung, chèn khung CV 5512 có đủ bốn phần, bảng hai cột và bốn bước để 1-Click Generate tiếp tục các pha sau.
- `tests/khbd-activity-b-subsections-smoke.js`: Bổ sung kiểm thử chuẩn hóa tiêu đề, phát hiện mọi nhánh thiếu và khung dự phòng.

## Kiểm thử

- PASS: `node tests/khbd-activity-b-subsections-smoke.js`
- PASS: `node tests/soankhbd-generation-mode-smoke.js`
- PASS: `git diff --check`
