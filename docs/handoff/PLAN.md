# PLAN: Khắc Phục Lỗi Xuất Word (Hiển Thị Mã Nguồn Thô) & Tự Động Đồng Bộ API Key Theo Tài Khoản Đã Đăng Ký Trong `kttx.html`

## Hiện trạng
1. **Lỗi nghiêm trọng khi xuất file Word: Toàn bộ mã nguồn JavaScript bị in thẳng ra file `.doc`**:
   - Trong `kttx.html`, tại các hàm tạo file Word:
     * Dòng 460 (`exportWord` - Xuất Đề & Đáp án)
     * Dòng 544 (`exportMatrixToWord` - Xuất Ma trận)
     * Dòng 884 (`renderSpecHtml` - Xuất Bản đặc tả)
     bị chèn thẻ `<script src="js/security-guard.js"></script>` vào bên trong chuỗi template string HTML sinh file Word.
   - Do toàn bộ mã nguồn React/JavaScript của trang được đặt trong thẻ `<script type="text/babel">`, khi trình duyệt đọc đến ký tự `</script>` ở dòng 460, trình phân tích HTML (HTML parser) của trình duyệt **lập tức đóng luôn thẻ script chính**.
   - Hậu quả: Toàn bộ đoạn code JavaScript từ dòng 461 trở đi bị trình duyệt hiểu nhầm là văn bản HTML thô, khiến khi xuất Word, nội dung file bị dính toàn bộ mã nguồn template string chưa biên dịch (ví dụ: `${info.dept.toUpperCase()}`, `typeOrder.forEach(...)`, `if(q.type=='TF')...` như trong ảnh người dùng phản ánh).
   - Ngoài ra tại dòng 468 có thẻ đóng `</div>` mồ côi (không có thẻ mở `<div>` tương ứng).

2. **Chưa tự động cấp / đồng bộ API Key theo tài khoản đã đăng ký**:
   - Khi người dùng đăng nhập tài khoản (ví dụ: `hoangthiencm@gmail.com`), danh sách Gemini API Keys đã được lưu trên máy chủ CSDL và truy xuất được qua `api/user_gemini_keys.php`.
   - Tuy nhiên, `kttx.html` hiện tại chỉ đọc thụ động từ `localStorage.getItem('global_gemini_keys')`. Khi người dùng mở trang trên thiết bị mới, trình duyệt mới hoặc sau khi xóa cache, trang báo lỗi `Chưa có API Key AI` dù tài khoản đã đăng ký và nạp key trên hệ thống.
   - Trang thiếu hàm tự động gọi `syncUserKeysFromServer()` khi tải trang để nạp key từ CSDL máy chủ về ứng dụng.

## Phạm vi
1. **Sửa dứt điểm lỗi xuất file Word trong `kttx.html`**:
   - Xóa bỏ hoàn toàn các thẻ `<script src="js/security-guard.js"></script>` nằm trong chuỗi template string của:
     * `exportWord` (Đề thi & Hướng dẫn chấm)
     * `exportMatrixToWord` (Ma trận đề kiểm tra)
     * `renderSpecHtml` (Bản đặc tả đề kiểm tra)
   - Chuẩn hóa cấu trúc HTML xuất Word: loại bỏ thẻ `</div>` mồ côi, bổ sung thẻ `<meta charset='utf-8'>`, chuẩn hóa bảng biểu và công thức toán MathML/WordML.
2. **Cấp lại & Tự động đồng bộ API Key theo tài khoản người dùng**:
   - Viết hàm `syncUserKeysFromServer()` trong `kttx.html` để tự động gọi `GET api/user_gemini_keys.php` với credentials session khi khởi tạo ứng dụng.
   - Tự động nạp danh sách API Key hợp lệ vào State React và lưu cache vào `localStorage ('global_gemini_keys')` để `AIAdapter` hoạt động ngay lập tức mà không cần người dùng phải chọn lại file key thủ công.
   - Thêm nút / phản hồi trạng thái hiển thị số lượng Gemini API Key đã đồng bộ từ tài khoản.
3. **Xây dựng Bộ Kiểm thử Tự động (`tests/kttx-smoke.js`)**:
   - Kiểm tra không còn thẻ `</script>` bên trong các khối script của `kttx.html`.
   - Kiểm tra mã nguồn Babel/React phân tích cú pháp hợp lệ 100%.
   - Kiểm tra cơ chế tự động đồng bộ API key từ `api/user_gemini_keys.php`.
   - Kiểm tra chuỗi HTML xuất Word cho Đề, Ma trận và Bản đặc tả sinh ra chuẩn cú pháp, không chứa mã JavaScript thô.

## Ngoài phạm vi
- Không thay đổi thuật toán sinh đề AI của các dạng câu hỏi MC, TF, TLN, TL.
- Không thay đổi định dạng cấu trúc ma trận 3 mức độ (Biết - Hiểu - Vận dụng).

## File dự kiến tác động
- `kttx.html` [XÓA THẺ SCRIPT TRONG TEMPLATE WORD, CHUẨN HÓA HTML WORD EXPORT, THÊM TỰ ĐỘNG ĐỒNG BỘ API KEY TỪ SERVER]
- `tests/kttx-smoke.js` [TẠO MỚI TEST SUITE KIỂM THỬ XUẤT WORD VÀ ĐỒNG BỘ API KEY CỦA KTTX]
- `docs/handoff/PLAN.md` [GHI ĐÈ KẾ HOẠCH THEO QUY TRÌNH SURVEY]
- `docs/handoff/.lock` [GHI NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật khi nghiệm thu]

## Các bước thực hiện
1. **Bước 1: Sửa các hàm xuất Word trong `kttx.html`**:
   - Xóa bỏ dòng `<script src="js/security-guard.js"></script>` tại dòng 460, dòng 544, dòng 884.
   - Sửa dòng 468: Xóa thẻ `</div>` thừa.
   - Kiểm tra lại toàn bộ chuỗi template HTML của `exportWord`, `exportMatrixToWord`, `renderSpecHtml`.
2. **Bước 2: Triển khai tự động đồng bộ API Key theo tài khoản trong `kttx.html`**:
   - Thêm hàm `syncUserKeysFromServer()` kết nối tới `api/user_gemini_keys.php`.
   - Trong `useEffect` khi ứng dụng React mount:
     * Gọi `syncUserKeysFromServer()`.
     * Cập nhật danh sách `geminiKeys` trong state và cập nhật `hasGemini` thành `true`.
     * Đồng bộ vào `localStorage.setItem('global_gemini_keys', ...)`.
   - Cập nhật thông báo thanh công cụ: hiển thị số lượng key đã nhận diện từ tài khoản (ví dụ: `🔑 Đã nạp X Gemini API Keys từ tài khoản`).
3. **Bước 3: Xây dựng kiểm thử tự động `tests/kttx-smoke.js`**:
   - Kiểm tra cấu trúc file `kttx.html` không có `</script>` lồng bên trong khối script Babel.
   - Kiểm tra hàm `exportWord`, `exportMatrixToWord`, `renderSpecHtml` tạo chuỗi HTML sạch, thay thế đúng các biến `${info.dept}`, `${info.school}`, `${info.title}` và các câu hỏi.
   - Kiểm tra quy trình sync API keys từ server.
4. **Bước 4: Khóa trạng thái giao việc**:
   - Ghi nội dung `LOCK` vào `docs/handoff/.lock`.

## Rủi ro
1. **Rủi ro người dùng chưa đăng nhập hoặc mạng ngoại tuyến khi tải key từ server**:
   - *Giải pháp*: Hàm `syncUserKeysFromServer` có khối try/catch an toàn và fallback đọc từ `localStorage ('global_gemini_keys')` nếu đã có sẵn từ trước.

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - Chạy lệnh: `node tests/kttx-smoke.js`
   - Chạy lệnh: `node tests/run-all-tests.js`
2. **Kiểm thử thủ công**:
   - Mở `kttx.html` trên trình duyệt:
     * Kiểm tra ứng dụng React tải mượt mà, không bị màn hình trắng hay lỗi cú pháp console.
     * Kiểm tra API Key: Ứng dụng tự động kết nối và nạp danh sách Gemini API Keys đã đăng ký của tài khoản, không hiện cảnh báo thiếu key.
     * Tạo một bộ đề kiểm tra (hoặc dùng câu hỏi mẫu) $\to$ Bấm "Xuất đề & Đáp án" (.doc) $\to$ Mở file Word kiểm tra:
       + Tiêu đề Sở/Trường/Môn/Thời gian hiển thị đúng nội dung chữ (không còn hiện `${info.dept...}`).
       + Bảng Đúng/Sai, Trắc nghiệm, Đáp án và Lời giải hiển thị đầy đủ, không có đoạn mã JavaScript nào bị rò rỉ.
     * Thử bấm "Xuất Ma trận" và "Xuất Bản đặc tả" $\to$ Kiểm tra cả 2 file Word đều sạch đẹp.

## Tiêu chí nghiệm thu
- [ ] Không còn bất kỳ thẻ `</script>` nào nằm bên trong template string của `kttx.html`.
- [ ] File Word xuất ra (`KiemTra_...doc`, `MaTran_...doc`, `BanDacTa_...doc`) hiển thị nội dung đề thi, bảng ma trận và bản đặc tả hoàn chỉnh, 100% không còn dính mã nguồn JavaScript thô.
- [ ] `kttx.html` tự động đồng bộ và cấp Gemini API Key từ tài khoản CSDL (`api/user_gemini_keys.php`) khi vào trang.
- [ ] 100% kiểm thử tự động `tests/kttx-smoke.js` và toàn bộ test suite chạy đạt PASS.
