# IMPLEMENT: Bảo toàn PPCT nguồn, chuẩn hóa bảng phụ lục và tiến trình sinh AI

## Phạm vi đã triển khai

- Giữ dữ liệu PPCT tải lên làm nguồn ưu tiên: trích xuất nội dung `.docx`, `.pdf`, `.txt` và `.xlsx`; nhận diện các dòng có `Tuần`, STT, bài học và số tiết.
- Bổ sung chỉ thị bảo toàn PPCT nguồn trong prompt Gemini; kết quả Phụ lục 1 và 3 được chuẩn hóa và thay lại bằng các dòng PPCT đã nhận diện, chỉ lấy nội dung tích hợp NLS/AI từ AI.
- Khi không có tệp nguồn, Phụ lục 1 và 3 sinh sẵn đủ 35 tuần, có STT và cột `Tuần`.
- Chuẩn hóa preview và DOCX: bảng Phụ lục 1 gồm thiết bị (TT 38/2021), phòng bộ môn (TT 14/2020), PPCT, kiểm tra định kỳ; Phụ lục 3 có cột Tuần. DOCX có đầu trang hành chính hai cột và bảng chữ ký.
- Xóa hẳn phần “Phương pháp & kĩ thuật dạy học”; thêm thanh tiến trình nổi với phần trăm; thay mật độ NLS/AI bằng các dải `1–2`, `2–3`, `3–4 mã/bài`.
- Không sửa `PLAN.md`, `VERIFY.md` hoặc `.lock`; không commit/push.

## File thay đổi

- `xaydungphuluc.html`: triển khai parser, bảo toàn PPCT, schema/preview/DOCX có cột Tuần, header/chữ ký, progress bar và mật độ mã mới.
- `tests/xaydungphuluc-smoke.js`: bổ sung assert cho bảo toàn PPCT, cột Tuần, parser bảng tính, progress UI, bảng DOCX chuẩn và việc xóa mục phương pháp.
- `docs/handoff/IMPLEMENT.md`: báo cáo triển khai này.

## Kiểm thử đã chạy

- `node tests/xaydungphuluc-smoke.js` — PASS.
- `node tests/xaydungphuluc-integration-smoke.js` — PASS.
- Kiểm tra cú pháp JavaScript nội tuyến bằng `new Function(...)` — PASS.
- `git diff --check` — PASS.

## Vấn đề còn lại

- Cần `/verify` trên trình duyệt với file PPCT thực tế để xác minh tất cả hàng/cột của từng định dạng nguồn và mở DOCX đã xuất.
