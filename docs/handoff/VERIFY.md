# VERIFY: Nghiệm thu Đồng Bộ API Key (Gemini & Mistral) CSDL Hai Chiều và Đồng Bộ Tỷ Lệ AI Hai Chiều Thời Gian Thực

## Kết luận
PASS

## Đối chiếu scope
1. **Đồng Bộ Hai Chiều Trực Tiếp Với CSDL Máy Chủ ([api/user_gemini_keys.php](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/api/user_gemini_keys.php))**:
   - `xaydungphuluc.html` tự động gọi `GET api/user_gemini_keys.php` với `credentials: 'include'` ngay khi tải trang (`DOMContentLoaded`) và khi mở Modal Key.
   - Nhận diện và nạp đầy đủ danh sách `keys` (Gemini) và `mistral_keys` (Mistral) của tài khoản người dùng từ CSDL máy chủ; tự động cache vào `localStorage` theo đúng định dạng `khbd_user_gemini_keys_${userEmail}` và `khbd_user_mistral_keys_${userEmail}`.
   - Modal Quản lý API Key hỗ trợ 2 ô nhập: `Gemini API Keys` và `Mistral API Keys`; nút **Lưu lên CSDL** gửi `POST api/user_gemini_keys.php` đồng bộ đồng nhất với `soankhbd.html`.
   - Badge hiển thị chính xác số lượng: `🔑 X Gemini · Y Mistral`.
2. **Đồng Bộ Tỷ Lệ AI Hai Chiều Thời Gian Thực Giữa Bảng Tick Bài và Thanh Slider**:
   - Khi tick/bỏ tick bài học hoặc các tiết của bài ở Mục 3: Thanh trượt `% Trí tuệ nhân tạo` và nhãn hiển thị ở Mục 4 tự động nhảy tỷ lệ % tương ứng.
   - Khi kéo thanh slider `% Trí tuệ nhân tạo`: Hệ thống tự động tính toán và tick chọn số lượng bài học tương ứng theo độ ưu tiên (Hình học, Thống kê, Trải nghiệm).
   - Bộ đếm hiển thị trực quan: `🎯 Đã chọn: X/12 tiết AI (Y% trên Z tiết)`.
3. **Ô Nạp PPCT & SGK Riêng Biệt, Nút Nhận Diện PPCT Mẫu**:
   - Khu vực 2 gồm 2 ô nạp tệp độc lập (`📄 Tải PPCT` và `📚 Tải SGK`), kèm nút `🔍 Nạp cấu trúc PPCT chuẩn theo Môn & Lớp`.
4. **Cơ Chế Liên Thông Phụ Lục 1 & Phụ Lục 3**:
   - Nạp file Phụ lục 3 $\rightarrow$ Phụ lục 3 giữ nguyên vẹn các cột tiến độ, Phụ lục 1 tự động được sinh đầy đủ cột `Yêu cầu cần đạt` chuẩn CT GDPT 2018.
5. **Xuất Word (.docx) & Preview 2 Màu Chuẩn Khung File Mẫu**:
   - Mã NLS Màu Xanh (`0070C0`), Mã NLAI Màu Tím (`7030A0`), đầy đủ 6 phần theo `Phụ lục 1 - Lớp 6 - Toán.docx`.

## Test đã chạy
- `node tests/xaydungphuluc-smoke.js` $\rightarrow$ PASS (kiểm tra đồng bộ CSDL API key Gemini & Mistral, đồng bộ 2 chiều slider AI, nạp PPCT/SGK riêng biệt, liên thông YCCĐ, màu NLS xanh / NLAI tím).
- `node tests/xaydungphuluc-integration-smoke.js` $\rightarrow$ PASS.
- Kiểm tra cú pháp JavaScript nội tuyến của `xaydungphuluc.html` qua `node --check` $\rightarrow$ PASS 100%.

## Pass / Fail từng tiêu chí
1. Đồng bộ API Key Gemini & Mistral từ CSDL máy chủ (`api/user_gemini_keys.php`) $\rightarrow$ **PASS**.
2. Modal lưu key đồng bộ lên CSDL hai chiều với `soankhbd.html` $\rightarrow$ **PASS**.
3. Badge hiển thị số lượng key `X Gemini · Y Mistral` $\rightarrow$ **PASS**.
4. Đồng bộ 2 chiều thời gian thực giữa bảng tick chọn AI và slider % AI $\rightarrow$ **PASS**.
5. Ô nạp PPCT và ô nạp SGK riêng biệt $\rightarrow$ **PASS**.
6. Liên thông tự sinh YCCĐ chuẩn GDPT 2018 cho Phụ lục 1 khi nạp Phụ lục 3 $\rightarrow$ **PASS**.
7. Xuất Word & Preview 2 màu (NLS Xanh `0070C0` - NLAI Tím `7030A0`) $\rightarrow$ **PASS**.

## Bug
- Không có lỗi tồn đọng.
