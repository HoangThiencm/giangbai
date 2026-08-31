# IMPLEMENT: Liên thông Phụ lục 3 → Phụ lục 1 với Yêu cầu cần đạt GDPT 2018

## Phạm vi đã triển khai

- Khi nạp bảng Phụ lục 3, Phụ lục 3 vẫn dùng toàn bộ cột, thứ tự dòng và dữ liệu nguồn; ứng dụng chỉ nối cột `Mã NLS & AI (CV 3456 & QĐ 2422)`.
- Phụ lục 1 dùng bảng riêng năm cột: `STT`, `Bài học`, `Số tiết`, `Yêu cầu cần đạt`, `Mã NLS & AI (CV 3456 & QĐ 2422)`.
- Prompt Phụ lục 1 yêu cầu Gemini lấy đúng danh sách bài học/số tiết từ nguồn Phụ lục 3 và tự sinh `outcomes` theo Chương trình GDPT 2018. Cột Tiết CT, Tuần, Thiết bị và Địa điểm không được đưa sang bảng Phụ lục 1.
- Khi phản hồi AI thiếu `outcomes`, ứng dụng có câu dự phòng chuẩn CTGDPT để không tạo ô trống; phản hồi Gemini vẫn được ưu tiên tuyệt đối khi có.
- Việc chọn tối đa 12 tiết AI được giữ đồng bộ cho cả hai phụ lục. Đã sửa cả trường hợp nguồn PPCT chỉ đọc được dạng văn bản/PDF: mã AI chỉ giữ ở các tiết được chọn.
- Preview và Word dùng cùng mô hình bảng mới; mã NLS giữ màu xanh `0070C0`, mã AI giữ màu tím `7030A0`.

## File thay đổi

- `xaydungphuluc.html`
- `tests/xaydungphuluc-smoke.js`
- `docs/handoff/IMPLEMENT.md`

Không sửa `docs/handoff/PLAN.md`, `docs/handoff/VERIFY.md` hoặc `docs/handoff/.lock`; không commit/push.

## Kiểm thử đã chạy

- `node tests/xaydungphuluc-smoke.js` — PASS.
- `node tests/xaydungphuluc-integration-smoke.js` — PASS.
- `node --check` cho JavaScript nội tuyến — PASS.
- `git diff --check` — PASS.

## Cần nghiệm thu thủ công

Nạp một Phụ lục 3 thực tế, chọn vài tiết AI rồi sinh Phụ lục 1 và 3. Xác nhận Phụ lục 1 có đúng năm cột và Yêu cầu cần đạt từng bài; xác nhận Phụ lục 3 không đổi cột/dữ liệu nguồn ngoài cột mã. Mở DOCX trong Microsoft Word để đối chiếu trực quan với file mẫu.
