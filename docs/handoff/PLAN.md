# PLAN: Bảo Mật Tuyệt Đối API Key (Không Lưu LocalStorage), Tải Key Ngay Khi Vào Web Và Hiển Thị Thanh Tiến Trình Thời Gian Thực Khi Trích Xuất PPCT

## Hiện trạng & 3 Yêu Cầu Thiết Kế Cốt Lõi

### 1. Bảo Mật API Key: Không Lưu Trong LocalStorage
- **Vấn đề**: Việc lưu key vào `localStorage` có nguy cơ bị lộ khi dùng chung máy tính hoặc qua kiểm tra DevTools.
- **Thiết kế mới**:
  * **Tuyệt đối không lưu API Key vào `localStorage` hay `sessionStorage`**.
  * Toàn bộ API Key (Gemini & Mistral) chỉ được lưu trữ an toàn trong CSDL máy chủ thông qua [api/user_gemini_keys.php](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/api/user_gemini_keys.php) của tài khoản đăng nhập.
  * Trong ứng dụng, key chỉ tồn tại trong bộ nhớ RAM (`apiKeys`, `mistralKeys`) trong suốt phiên làm việc hiện tại.
  * Tự động dọn dẹp sạch sẽ mọi key cũ còn vướng trong `localStorage` khi nạp trang.

---

### 2. Nạp Key Tức Thì Ngay Khi Vào Web (Instant Eager Load)
- Khi mở trang web:
  * Ứng dụng ngay lập tức gửi yêu cầu `fetch('api/user_gemini_keys.php', { method: 'GET', credentials: 'include' })` để lấy danh sách key từ CSDL máy chủ.
  * Cập nhật badge ngay lập tức: `🔑 X Gemini · Y Mistral`.
  * Trong `parseFiles()`: Luôn `await` tiến trình nạp key này để bảo đảm 100% có key trong RAM trước khi gọi AI nhận diện file PPCT, không bao giờ bị báo lỗi thiếu key.

---

### 3. Thanh Tiến Trình Thời Gian Thực (% Real-time Progress Bar) Khi Trích Xuất PPCT
- Khi giáo viên tải file PPCT lên (hoặc bấm nhận diện AI):
  * Bật thanh tiến trình thời gian thực `#progressContainer` với thông điệp rõ ràng theo từng chặng:
    * `15%`: *Đang đọc tệp dữ liệu PPCT...*
    * `40%`: *Đang gửi ngữ cảnh lên AI (Gemini/Mistral)...*
    * `75%`: *AI đang phân tích và trích xuất bảng PPCT...*
    * `90%`: *Đang khởi tạo Bảng PPCT 8 cột...*
    * `100%`: *✓ Đã nhận diện hoàn tất bảng PPCT!* (tự động ẩn sau 1.5s).
  * Giúp giáo viên quan sát rõ ràng từng giây hoạt động của hệ thống, chuyên nghiệp và mượt mà.

---

### 4. Quy Trình 2 Giai Đoạn Vẫn Duy Trì Hoàn Hảo
- **Giai đoạn 1**: Nạp file $\rightarrow$ Thanh tiến trình chạy $\rightarrow$ AI đọc và đẩy bảng PPCT gốc lên Mục 3 (Table View 8 cột) để giáo viên tick chọn 12 tiết AI.
- **Giai đoạn 2**: Bấm Sinh Phụ lục $\rightarrow$ Thanh tiến trình chạy $\rightarrow$ AI bù đắp YCCĐ cho Phụ lục 1 và tích hợp mã NLS Xanh (`0070C0`) / AI Tím (`7030A0`) $\rightarrow$ Xuất Word (.docx) chuẩn mực 6 phần.

## Phạm vi Kỹ Thuật trong `xaydungphuluc.html`
1. **Xóa Bỏ Hoàn Toàn `localStorage` Cho API Key**:
   - Bỏ các hàm `cacheUserKeys()` và `readStoredKeyList()`.
   - Khi lưu key ở Modal: Gửi `POST api/user_gemini_keys.php` trực tiếp lên CSDL, chỉ cập nhật biến trong RAM.
   - Thêm hàm dọn dẹp các key `khbd_*`, `gemini_*`, `xdpl_*` trong `localStorage`.
2. **Khởi Tạo Đồng Bộ Key Ngay Lập Tức**:
   - `syncUserKeysPromise = syncUserKeysFromServer()` được kích hoạt ngay đầu trang.
   - Hàm `ensureKeysLoaded()` trả về `await syncUserKeysPromise` trước khi gọi AI.
3. **Tích Hợp `setProgress` Thời Gian Thực Vào `parseFiles()`**:
   - Hiển thị tiến trình từ 0% đến 100% trong quá trình đọc file và AI nhận diện PPCT.
4. **Giữ Nguyên Giao Diện Table View 8 Cột & Xuất Word 2 Màu**:
   - Phụ lục 1 tự sinh YCCĐ; Phụ lục 3 giữ nguyên bảng nguồn; Xuất DOCX NLS Xanh `0070C0` / NLAI Tím `7030A0`.

## File tác động
- `xaydungphuluc.html` [XÓA BỎ LOCALSTORAGE KEY, ĐỒNG BỘ CSDL TỨC THÌ, THANH TIẾN TRÌNH THỜI GIAN THỰC KHI TRÍCH XUẤT PPCT]
- `tests/xaydungphuluc-smoke.js` [BỔ SUNG TEST CHO BẢO MẬT KHÔNG LƯU LOCALSTORAGE VÀ TIẾN TRÌNH TRÍCH XUẤT PPCT]
- `docs/handoff/PLAN.md` [GHI ĐÈ]
- `docs/handoff/.lock` [GHI MỚI / NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật kết quả nghiệm thu]

## Các bước thực hiện
1. **Bước 1: Tái Cấu Trúc Quản Lý Key Hoàn Toàn Bằng CSDL Máy Chủ**:
   - Xóa bỏ việc ghi key vào `localStorage`. Key chỉ lưu CSDL và lưu tạm trong RAM.
   - Nạp key tức thì ngay khi mở trang web.
2. **Bước 2: Gắn Thanh Tiến Trình Thời Gian Thực Vào `parseFiles()`**:
   - Hiển thị tiến độ % và thông báo động khi đọc file và gọi AI nhận diện.
3. **Bước 3: Cập Nhật và Chạy Kiểm Thử Tự Động**:
   - Chạy `node tests/xaydungphuluc-smoke.js` và `node tests/xaydungphuluc-integration-smoke.js`, xác nhận PASS 100%.

## Tiêu chí nghiệm thu
1. API Key tuyệt đối không còn bị lưu trong `localStorage` hay `sessionStorage`; chỉ lưu an toàn trên CSDL máy chủ và RAM phiên làm việc.
2. Vừa vào trang web là key được tự động nạp ngay từ CSDL (badge hiển thị đúng số lượng key tức thì).
3. Khi tải file PPCT lên: Thanh tiến trình thời gian thực hiển thị % và trạng thái rõ ràng từ 0% đến 100%.
4. Toàn bộ smoke test tự động đều PASS 100%.
