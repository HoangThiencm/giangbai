# VERIFY: Nghiệm thu Hiển Thị Toàn Bộ Bảng PPCT Nguồn, Đọc & Điều Chỉnh Số Tiết Thực Tế, Tick Chọn 12 Tiết AI Và Xuất Word 2 Màu

## Kết luận
PASS

## Đối chiếu scope
1. **Đọc & Hiển Thị Toàn Bộ Bảng PPCT Nhận Diện Lên Hệ Thống**:
   - Khi tải file Phụ lục 3 (hoặc PPCT) lên: Hệ thống bóc tách và hiển thị ngay toàn bộ danh sách các bài học với đầy đủ thông tin:
     + Tên bài học thực tế từ file nguồn (`lesson`).
     + Số tiết thực tế (`periods`) kèm ô input cho phép giáo viên tăng/giảm trực tiếp.
     + Thông tin chi tiết: `Tiết CT`, `Tuần`, `Thiết bị dạy học`, `Địa điểm dạy học`.
     + Các checkbox tiết con (`Tiết 1`, `Tiết 2`... `Tiết N`) tương ứng đúng số lượng số tiết của bài.
2. **Bộ Bóc Tách Số Tiết Đa Kênh Chuẩn Xác**:
   - Nhận diện đúng số tiết từ các định dạng: số nguyên (`2`, `3`), ngoặc đơn (`(2 tiết)`, `[3 tiết]`), chữ (`2 tiết`, `2-3 tiết`), và khoảng `Tiết CT` (`1-3` $\rightarrow$ 3 tiết, `1, 2` $\rightarrow$ 2 tiết).
   - Khi sửa số tiết của một bài: Danh sách checkbox tiết con tự động cập nhật số lượng, tỷ lệ % AI và Preview/DOCX được làm mới đồng bộ.
3. **Tick Chọn 12 Tiết Tích Hợp Khung Năng Lực AI (QĐ 2422)**:
   - Giáo viên tick chọn trực tiếp trên từng bài/tiết (tối đa 12 tiết); có nút `✨ Gợi ý 12 tiết chuẩn` và `✕ Bỏ chọn tất cả`.
   - Năng lực số (NLS - CV 3456) được tích hợp tự động theo tỷ lệ % và mật độ.
4. **Cơ Chế Liên Thông Phụ Lục 1 & Phụ Lục 3**:
   - Nạp file Phụ lục 3 $\rightarrow$ Phụ lục 3 giữ nguyên 100% bảng nguồn, Phụ lục 1 tự động sinh đầy đủ cột `Yêu cầu cần đạt` chuẩn CT GDPT 2018.
5. **Xuất Word (.docx) & Preview 2 Màu Chuẩn Khung File Mẫu**:
   - Mã NLS Màu Xanh (`0070C0`), Mã NLAI Màu Tím (`7030A0`), đầy đủ 6 phần theo `Phụ lục 1 - Lớp 6 - Toán.docx`.
6. **Đồng Bộ API Key Gemini & Mistral CSDL Máy Chủ (`api/user_gemini_keys.php`)**:
   - Nhận diện và đồng bộ 100% danh sách key cá nhân của tài khoản người dùng.

## Test đã chạy
- `node tests/xaydungphuluc-smoke.js` $\rightarrow$ PASS (kiểm tra hiển thị đầy đủ bảng PPCT, bóc tách số tiết đa kênh, sửa số tiết, tick chọn 12 tiết AI, xuất Word 2 màu).
- `node tests/xaydungphuluc-integration-smoke.js` $\rightarrow$ PASS.
- Kiểm tra cú pháp JavaScript nội tuyến của `xaydungphuluc.html` qua `node --check` $\rightarrow$ PASS 100%.

## Pass / Fail từng tiêu chí
1. Nạp file Phụ lục 3 $\rightarrow$ hiển thị toàn bộ bảng PPCT với đầy đủ Tên bài, Số tiết, Tiết CT, Tuần, Thiết bị, Địa điểm $\rightarrow$ **PASS**.
2. Bóc tách chính xác số tiết đa kênh và cho phép tăng/giảm số tiết $\rightarrow$ **PASS**.
3. Checkbox tick chọn 12 tiết AI hiển thị trực quan trên từng bài $\rightarrow$ **PASS**.
4. Liên thông tự sinh YCCĐ chuẩn GDPT 2018 cho Phụ lục 1 từ file Phụ lục 3 $\rightarrow$ **PASS**.
5. Xuất Word & Preview 2 màu (NLS Xanh `0070C0` - NLAI Tím `7030A0`) $\rightarrow$ **PASS**.
6. Đồng bộ API Key CSDL hai chiều với `soankhbd.html` $\rightarrow$ **PASS**.

## Bug
- Không có lỗi tồn đọng.
