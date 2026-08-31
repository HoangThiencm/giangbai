# IMPLEMENT: Lọc SGK, chọn đích danh 12 tiết AI và phân biệt màu NLS/AI

## Phạm vi đã triển khai

- `xaydungphuluc.html` nhận diện bảng PPCT độc lập với bảng hành chính, giữ nguyên bảng nguồn và chỉ thêm cột cuối `Mã NLS & AI (CV 3456 & QĐ 2422)`.
- Khi tải tệp SGK có tên chứa `SGK` / `Sách giáo khoa`, ứng dụng chỉ đưa vào yêu cầu AI các tên bài, mục tiêu/yêu cầu cần đạt và hoạt động khám phá, luyện tập, vận dụng. Nội dung này được giới hạn để tránh đưa toàn văn SGK vào yêu cầu.
- Sau khi đọc PPCT, giáo viên có danh sách checkbox để chọn tối đa 12 tiết AI. Nút gợi ý ưu tiên Hình học, Thống kê và Trải nghiệm, rồi mới bổ sung các bài còn lại đến giới hạn. Prompt chỉ cho phép mã AI với chính xác các bài đã chọn; mã AI cũng bị loại khỏi các dòng không được chọn ở bước chuẩn hóa dữ liệu.
- Preview và Word tách mã NLS màu xanh `0070C0` và mã AI màu tím `7030A0`. Word dùng `TextRun` riêng cho từng phần mã.
- Thanh tiến trình tiếp tục có trạng thái hoàn tất, tự ẩn và nút đóng.
- Khung xuất Phụ lục 1 giữ đủ sáu phần hành chính theo CV 5512 (tiêu ngữ, tiêu đề, I, II, III và ký duyệt), đồng thời tái lập cấu trúc/định dạng gần nhất có thể trong DOCX; không cam kết hiển thị giống hệt trên mọi phiên bản Office.

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

Tải PPCT và một SGK thật, tự chọn/gợi ý 12 tiết rồi sinh Phụ lục 1. Mở DOCX xuất ra trong Microsoft Word để đối chiếu trực quan căn lề, font và màu xanh/tím với file mẫu; khác biệt giữa các phiên bản Office cần được xác nhận thực tế.
