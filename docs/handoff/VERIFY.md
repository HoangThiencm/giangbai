# VERIFY: Nghiệm thu Khớp Chuẩn Biểu Mẫu PPCT 7 Cột và Thanh Tiến Trình Tự Động Ẩn Khi Hoàn Tất 100%

## Kết luận
PASS

## Đối chiếu scope
1. **Khớp Chuẩn Biểu Mẫu PPCT 7 Cột của Người Dùng**:
   - Bảng phân phối chương trình và kế hoạch dạy học đã định nghĩa đúng 7 cột chuẩn:
     1. `Bài học`
     2. `Số tiết`
     3. `Tiết CT`
     4. `Tuần`
     5. `Thiết bị dạy học (*)`
     6. `Địa điểm dạy học (**)`
     7. `Mã NLS & AI (CV 3456 & QĐ 2422)` (cột bổ sung duy nhất)
   - Hỗ trợ các dòng tiêu đề phân cấp chương `isHeader: true` gộp ô (`HỌC KÌ I`, `1. SỐ HỌC 6`, `CHƯƠNG I. ...`, `HỌC KÌ II`).
   - Parser bảo toàn 100% dữ liệu gốc từ file người dùng tải lên; Siêu Prompt Gemini AI chỉ điền vào cột số 7 `Mã NLS & AI`.
   - File xuất Word `.docx` chuẩn A4, viền nét đơn, độ rộng cột 30/7/8/7/12/11/25%, căn giữa các cột số liệu; đầy đủ chú thích `(*)` TT 38/2021 và `(**)` TT 14/2020; chữ ký phê duyệt 2 bên.
2. **Thanh Tiến Trình Thời Gian Thực (% Floating Progress Bar)**:
   - **Đã khắc phục triệt để lỗi 100% không dừng / không ẩn**:
     + Khi đạt `percent >= 100`, spinner xoay lập tức dừng lại và được thay thế bằng biểu tượng tích xanh `✓`.
     + Sau 1.5 giây kể từ khi hoàn tất, thanh tiến trình tự động kích hoạt hiệu ứng fade-out và ẩn hoàn toàn (`hideProgress()`), không còn che khuất bảng dữ liệu phía dưới.
     + Bổ sung nút đóng `✕` thủ công trên thanh tiến trình cho phép người dùng đóng ngay lập tức.
     + Nhánh hủy tác vụ / lỗi hiển thị thông báo và tự ẩn sau 2 giây an toàn.
3. **Các tính năng đã hoàn thiện trước đó**:
   - Đã xóa bỏ hoàn toàn khối "Phương pháp & kĩ thuật dạy học".
   - Dropdown mật độ mã hỗ trợ đầy đủ các dải linh hoạt: `1–2 mã/bài`, `2–3 mã/bài`, `3–4 mã/bài`.
   - Tự động dùng chung API Key đã lưu từ `soankhbd.html` (`khbd_user_gemini_keys_...`).
   - Nhúng `js/security-guard.js` và `access-control.js` bảo vệ mã nguồn.

## Test đã chạy
- `node tests/xaydungphuluc-smoke.js` $\rightarrow$ PASS (kiểm tra 7 cột, tiết CT, spanning headers, chú thích, chữ ký, `hideProgress`, timer 1.5s, nút `✕`).
- `node tests/xaydungphuluc-integration-smoke.js` $\rightarrow$ PASS.
- Kiểm tra cú pháp JavaScript nội tuyến của `xaydungphuluc.html` qua `node --check` $\rightarrow$ PASS 100%.

## Pass / Fail từng tiêu chí
1. Khớp biểu mẫu PPCT 7 cột chuẩn của người dùng $\rightarrow$ **PASS**.
2. Bảo toàn 100% dữ liệu nguồn từ file tải lên và chỉ bổ sung cột NLS & AI $\rightarrow$ **PASS**.
3. Dừng spinner và tự động ẩn thanh tiến trình sau 1.5s khi đạt 100% $\rightarrow$ **PASS**.
4. Nút đóng `✕` thủ công trên thanh tiến trình $\rightarrow$ **PASS**.
5. Xóa khối phương pháp dạy học $\rightarrow$ **PASS**.
6. Dropdown dải mật độ mã `1-2`, `2-3`, `3-4` $\rightarrow$ **PASS**.
7. Toàn bộ smoke test tự động $\rightarrow$ **PASS**.

## Bug
- Không có lỗi tồn đọng.
