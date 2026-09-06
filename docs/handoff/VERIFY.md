# VERIFY

## Kết luận
PASS

## Đối chiếu scope

### Phần 1: Nạp phân công từ TKB toàn tổ & Tự động phiên lớp sau nhận diện
- [x] **Nút Nạp phân công từ TKB toàn tổ (1-Click Sync)**:
  + Tab 1 (`#view-phancong`): Thêm nút `⚡ Nạp phân công từ TKB toàn tổ` (`btn-small-primary`) trên thanh thống kê tiến độ `.live-stats-banner` (cạnh nút Xem Ma trận Đợt này).
  + Tab 2 (`#view-timetable`): Thêm nút `⚡ Dịch TKB toàn tổ sang Phân công` (`btn-small-primary`) trên thanh công cụ tác vụ (`#tt-right-panel`, cạnh nút Lưu tất cả lên CSDL).
  + Tab 2 (`#view-timetable`): Đổi nhãn nút đơn lẻ thành `Dịch GV này sang Phân công` để phân biệt rõ ràng.
  + Tab 2 Cột trái (`#tt-left-panel`): Thêm nút nhanh `⚡ Nạp phân công toàn tổ` ngay dưới dòng tiến độ `Đã có TKB: X / Y giáo viên`.
- [x] **Tự động phiên lớp khi AI nhận diện TKB**:
  + Checkbox `#tt-auto-apply-assign` đặt mặc định `checked`.
  + Hàm `applyAiTimetableResult`: Khi checkbox bật, tự động gọi `applyTimetableToAssignments(selectedTimetableTeacherId, { silent: true, skipRender: true })` và hiển thị Toast thông báo số lớp đã được phiên tự động.
- [x] **Hàm `syncAllAssignmentsFromTimetables()`**:
  + Có hộp thoại `confirm()` xác nhận theo tên đợt hiện tại.
  + Đếm chính xác số GV và tổng số lượt lớp được gán, cập nhật `state.classes`, dọn sạch `state.unassigned`.
  + Gọi `saveCurrentPhaseSnapshot()`, `saveToLocal()` và `render()` cập nhật tức thì Tab 1.
- [x] **Cải tiến bóc tách ô TKB & Khớp môn**:
  + `parseTimetableCell` / `splitSubjectAndClass`: Tách chính xác các định dạng `Toán 95`, `Toán 9A1`, `Toán/95`, `Toán - 95`.
  + `matchSubjectFromTimetableLabel`: Khớp thông minh các alias `toan` -> Toán, `tin` -> Tin học, `hdtn` -> HĐTN, `shl` / `sinh hoạt lớp` kèm tên lớp -> Chủ nhiệm.

### Phần 2: Tính năng Tạo ảnh thông báo dạy thay thông minh bằng AI & Canvas
- [x] **Thư viện `html2canvas`**: Đã tích hợp bản 1.4.1 trên `<head>` của `phancongtochuyenmon.html` (đồng bộ cùng CDN với `vehinh.html`).
- [x] **Nút trên Sổ Dạy Thay (`view-daythay`)**: Thêm nút `✨ Tạo ảnh thông báo (AI)` (`btn-small-primary`) trên thanh công cụ chi tiết.
- [x] **Modal & Card thông báo chuẩn sư phạm**:
  + Modal `#substitute-announcement-modal` với bộ điều khiển chọn ngày, tiêu đề thông báo, lời dặn dò.
  + Card đồ họa `#dt-announcement-card` thiết kế trang trọng: Tiêu đề trường (`state.info.school`), Tổ chuyên môn (`state.info.title`), bảng phân công chi tiết (Buổi, Tiết, Lớp, Môn, GV vắng & lý do, GV dạy thay), lời dặn dò và chữ ký đại diện TTCM.
- [x] **AI Soạn thông báo**: Nút `✨ AI Soạn thông báo Zalo` kết nối `api/khbd_gemini.php` (Gemini 2.5 Flash) soạn lời dặn dò và caption Zalo chuẩn văn phong nhà trường.
- [x] **Xuất bản 1-Click**:
  + `📋 Sao chép ảnh`: Xuất blob PNG qua `html2canvas` và ghi thẳng vào Clipboard để dán ngay `Ctrl+V` vào Zalo (kèm fallback tải ảnh).
  + `💾 Tải ảnh PNG`: Tải file `Thong_Bao_Day_Thay_YYYYMMDD.png` chất lượng cao về máy.
  + `📝 Sao chép tin Zalo`: Sao chép văn bản tóm tắt có emoji để gửi kèm ảnh.

---

## Test đã chạy
1. `tests/smartquiz-smoke.js`: PASS.
2. `tests/xaydungphuluc-smoke.js`: PASS.
3. Kiểm tra tính duy nhất của toàn bộ 140 HTML IDs: 100% unique, 0 ID trùng lặp.
4. Kiểm tra sự tồn tại của đầy đủ DOM elements và thư viện (`html2canvas`, nút nạp TKB Tab 1/Tab 2, `#tt-auto-apply-assign` checked, nút `Tạo ảnh thông báo (AI)`, modal `#substitute-announcement-modal`, card `#dt-announcement-card`): PASS.
5. Kiểm tra cú pháp và thực thi toàn bộ script JS trong VM sandbox: PASS, 0 lỗi cú pháp.
6. Unit test `parseTimetableCell`: Nhận diện chuẩn xác `Toán 95`, `Toán 9A1`, `Toán/95`, `Toán - 95` và định dạng object: PASS.
7. Unit test `matchSubjectFromTimetableLabel`: Khớp chuẩn xác alias `toan`, `tin`, `hdtn`, `shl` (với class): PASS.
8. Kiểm tra `syncAllAssignmentsFromTimetables()`: Nạp đồng loạt các lớp từ TKB của tất cả giáo viên vào `teacher.assignments`, làm sạch kho `state.unassigned`: PASS.
9. Kiểm tra `applyAiTimetableResult`: Tự động phiên các lớp từ TKB sang phân công của giáo viên khi nhận diện xong: PASS.
10. Kiểm tra bộ hàm tạo ảnh thông báo dạy thay (`openDayThayAnnouncementModal`, `renderAnnouncementCard`, `generateDayThayAnnouncementAI`, `copyAnnouncementImage`, `downloadAnnouncementImage`, `copyAnnouncementZaloText`): PASS.

---

## Pass / Fail từng tiêu chí
- Tiêu chí 1: Có nút nổi bật `⚡ Nạp phân công từ TKB toàn tổ` trực tiếp trên Tab 1 và Tab 2, không bị giấu trong menu con -> PASS
- Tiêu chí 2: Bấm 1 click nạp toàn bộ lớp từ TKB của cả 11 giáo viên vào bảng phân công đợt hiện tại -> PASS
- Tiêu chí 3: Kho lớp chưa gán (`state.unassigned`) bên trái được dọn sạch và thẻ của tất cả giáo viên hiển thị đủ các lớp được phân công -> PASS
- Tiêu chí 4: Khi AI nhận diện TKB của giáo viên mới, hệ thống tự động phiên luôn các lớp sang phân công của giáo viên đó nếu tuỳ chọn đang bật -> PASS
- Tiêu chí 5: Có nút `✨ Tạo ảnh thông báo (AI)` trên thanh công cụ của Sổ Dạy Thay -> PASS
- Tiêu chí 6: Xuất được ảnh thông báo dạy thay thiết kế chuẩn sư phạm, sắc nét (PNG), cho phép copy trực tiếp vào clipboard để paste Zalo và tải về máy -> PASS
- Tiêu chí 7: AI Gemini hỗ trợ soạn nội dung thông báo / lời dặn dò văn phong nhà trường và văn bản gửi Zalo tiện lợi -> PASS

---

## Bug
Không phát hiện bug.
