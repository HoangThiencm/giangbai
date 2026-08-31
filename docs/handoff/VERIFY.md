# VERIFY: Nghiệm thu Toàn Diện Bảo Mật Key, Tải Key Ngay Khi Vào Web, Thanh Tiến Trình PPCT Thời Gian Thực & Bộ Chọn Model Gemini Mặc Định 3.7 Flash

## Kết luận
PASS

## Đối chiếu scope
1. **Bảo Mật API Key Tuyệt Đối (Không Lưu LocalStorage)**:
   - Đã loại bỏ hoàn toàn cơ chế đọc/ghi key từ `localStorage` và `sessionStorage`.
   - Key chỉ tồn tại trong RAM (`apiKeys`, `mistralKeys`) sau khi đồng bộ với `api/user_gemini_keys.php`; lưu từ Modal chỉ POST lên CSDL máy chủ rồi cập nhật RAM.
   - Khi khởi động trang, ứng dụng tự động dọn dẹp các key legacy cũ trong `localStorage` mà không làm mất thông tin tài khoản hay giao diện.
2. **Nạp Key Ngay Lập Tức Khi Vào Web (Instant Eager Load)**:
   - `syncUserKeysPromise` kích hoạt nạp key từ CSDL máy chủ ngay khi trang mở ra.
   - Hàm `ensureKeysLoaded()` dùng chung promise này: Luôn bảo đảm 100% key đã nạp xong vào RAM trước khi gửi prompt tới Gemini/Mistral, ngăn chặn triệt để lỗi "Chưa có Gemini hoặc Mistral API Key".
3. **Thanh Tiến Trình Thời Gian Thực (% Real-time Progress Bar) Khi Trích Xuất PPCT**:
   - Khi tải file PPCT lên: `#progressContainer` hiển thị tiến trình mượt mà qua các mốc: 15% (Đọc tệp), 40% (Gửi ngữ cảnh lên AI), 75% (AI phân tích và trích xuất bảng PPCT), 90% (Dựng Bảng PPCT 8 cột), 100% (Hoàn tất và tự ẩn sau 1.5s).
   - Nhánh parser dự phòng và lỗi đọc tệp cũng luôn đóng tiến trình đúng quy chuẩn.
4. **Bộ Chọn Model Gemini `#selectModel` & Fallback Thông Minh**:
   - Thêm dropdown chọn model tại header với `Gemini 3.7 Flash` làm mặc định, hỗ trợ đầy đủ các model (3.6, 3.5, 2.5 Flash...).
   - `thinkingBudget: 0` được gửi kèm payload để phản hồi nhanh nhất.
   - Khi Gemini 3.7 Flash gặp sự cố tạm thời 5xx/timeout/429 ở key cuối, hệ thống tự động fallback sang `Gemini 2.5 Flash` mà không làm thay đổi model đã lưu của người dùng.
5. **Quy Trình 2 Giai Đoạn & Giao Diện Table View 8 Cột**:
   - Giai đoạn 1: Nạp file $\rightarrow$ AI đọc và đẩy bảng PPCT gốc lên Mục 3 (Table View 8 cột) để giáo viên tick chọn 12 tiết AI.
   - Giai đoạn 2: Bấm Sinh Phụ lục $\rightarrow$ AI bù đắp YCCĐ cho Phụ lục 1 và tích hợp mã NLS Xanh / AI Tím $\rightarrow$ Xuất Word chuẩn 6 phần.

## Test đã chạy
- `node tests/xaydungphuluc-smoke.js` $\rightarrow$ PASS (kiểm tra không persist key vào localStorage, dọn key legacy, eager-load/await chung promise, các mốc tiến trình PPCT, bộ chọn model Gemini 3.7 Flash và fallback 2.5 Flash, 8 cột table view, xuất Word 2 màu).
- `node tests/xaydungphuluc-integration-smoke.js` $\rightarrow$ PASS.
- Kiểm tra cú pháp JavaScript nội tuyến của `xaydungphuluc.html` qua `node --check` $\rightarrow$ PASS 100%.

## Pass / Fail từng tiêu chí
1. Không còn lưu key vào localStorage; key bảo mật trên CSDL và RAM $\rightarrow$ **PASS**.
2. Nạp key tức thì từ CSDL ngay khi vào web $\rightarrow$ **PASS**.
3. Tải file PPCT hiển thị thanh tiến trình % thời gian thực rõ ràng $\rightarrow$ **PASS**.
4. Luồng gọi AI nhận diện PPCT luôn chờ key sẵn sàng trước khi gửi prompt $\rightarrow$ **PASS**.
5. Bộ chọn model Gemini 3.7 Flash mặc định kèm fallback 2.5 Flash $\rightarrow$ **PASS**.
6. Bảng Mục 3 hiển thị dạng Table View 8 cột với checkbox chọn 12 tiết AI $\rightarrow$ **PASS**.
7. Liên thông tự sinh YCCĐ cho Phụ lục 1 và xuất Word 2 màu (NLS Xanh `0070C0` / NLAI Tím `7030A0`) $\rightarrow$ **PASS**.

## Bug
- Không có lỗi tồn đọng.
