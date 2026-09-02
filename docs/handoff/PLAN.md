# PLAN: Khắc Phục Lỗi Xuất Word & Tự Động Đồng Bộ Gemini API Key Theo Tài Khoản Trong `matrande.html`

## Hiện trạng
1. **Lỗi thẻ `<script>` chèn nhầm bên trong chuỗi template string xuất Word**:
   - Trong `matrande.html`, tại các hàm tạo file Word:
     * Dòng 1714: bên trong hàm `exportWord` (Xuất Đề thi & Hướng dẫn chấm)
     * Dòng 1934: bên trong hàm `exportWordRaw` (Xuất Đề thi dạng thô)
     bị chèn thẻ `<script src="js/security-guard.js"></script>` vào bên trong chuỗi template string HTML sinh file Word.
   - Toàn bộ mã nguồn React/Babel của trang được bao bọc trong thẻ `<script type="text/babel">`. Khi trình duyệt đọc đến ký tự `</script>` ở dòng 1714, trình phân tích HTML (HTML parser) **lập tức đóng luôn thẻ script chính của trang**.
   - Hậu quả: Toàn bộ mã nguồn từ dòng 1715 trở đi bị trình duyệt coi là văn bản thô, làm hỏng quá trình xuất file Word và khiến mã nguồn JavaScript thô bị in thẳng ra file `.doc`.

2. **Chưa tự động đồng bộ Gemini API Key từ tài khoản CSDL**:
   - `matrande.html` hiện chỉ đọc khóa API từ `localStorage.getItem('global_gemini_keys')`.
   - Khi người dùng đăng nhập tài khoản trên thiết bị mới hoặc xóa cache trình duyệt, trang báo lỗi `Thiếu Gemini API Key` dù tài khoản đã có key lưu trên máy chủ CSDL (`api/user_gemini_keys.php`).
   - Cần bổ sung cơ chế tự động gọi `syncUserKeysFromServer()` kết nối tới `api/user_gemini_keys.php` ngay khi tải trang để nạp key vào React state và cache `localStorage`.

## Phạm vi
1. **Sửa dứt điểm lỗi xuất file Word trong `matrande.html`**:
   - Xóa bỏ hoàn toàn các thẻ `<script src="js/security-guard.js"></script>` nằm trong chuỗi template string của:
     * `exportWord` (dòng 1714)
     * `exportWordRaw` (dòng 1934)
   - Đảm bảo thẻ `<meta charset='utf-8'>` hợp lệ và cấu trúc HTML của cả 2 hàm xuất Word chuẩn chỉnh, không chứa thẻ đóng mồ côi.
2. **Cấp lại & Tự động đồng bộ Gemini API Key theo tài khoản**:
   - Thêm hàm `syncUserKeysFromServer()` gọi `GET api/user_gemini_keys.php` với session credentials.
   - Trong `useEffect` khi ứng dụng React mount: tự động gọi `syncUserKeysFromServer()`, chuẩn hóa danh sách key và lưu vào `localStorage ('global_gemini_keys')`.
   - Cập nhật trạng thái hiển thị: thông báo rõ số lượng Gemini API Key đã nạp từ tài khoản.
3. **Xây dựng Bộ Kiểm thử Tự động (`tests/matrande-smoke.js`)**:
   - Kiểm tra `matrande.html` không còn thẻ `</script>` nào nằm bên trong template string của khối Babel script.
   - Kiểm tra `exportWord` và `exportWordRaw` sinh chuỗi HTML Word chuẩn cú pháp.
   - Kiểm tra cơ chế tự động đồng bộ API Key từ `api/user_gemini_keys.php`.

## Ngoài phạm vi
- Không thay đổi thuật toán sinh đề AI ma trận (Biết - Hiểu - Vận dụng).
- Không can thiệp vào các logic AI Groq hoặc HuggingFace fallback sẵn có.

## File dự kiến tác động
- `matrande.html` [XÓA SCRIPT TRONG TEMPLATE WORD, BỔ SUNG TỰ ĐỘNG ĐỒNG BỘ GEMINI API KEY TỪ SERVER]
- `tests/matrande-smoke.js` [TẠO MỚI TEST SUITE KIỂM THỬ XUẤT WORD VÀ ĐỒNG BỘ API KEY CỦA MATRANDE]
- `docs/handoff/PLAN.md` [GHI ĐÈ KẾ HOẠCH THEO QUY TRÌNH SURVEY]
- `docs/handoff/.lock` [GHI NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật khi nghiệm thu]

## Các bước thực hiện
1. **Bước 1: Sửa các hàm xuất Word trong `matrande.html`**:
   - Xóa thẻ `<script src="js/security-guard.js"></script>` tại dòng 1714 (`exportWord`) và dòng 1934 (`exportWordRaw`).
   - Kiểm tra toàn bộ chuỗi template HTML của `exportWord` và `exportWordRaw` đảm bảo không còn thẻ script lồng nhau.
2. **Bước 2: Triển khai tự động đồng bộ Gemini API Key trong `matrande.html`**:
   - Thêm hàm `syncUserKeysFromServer()` kết nối tới `api/user_gemini_keys.php`.
   - Thêm logic nạp key tự động trong `useEffect` khi ứng dụng mount, cập nhật state và lưu cache `localStorage ('global_gemini_keys')`.
   - Hiển thị trạng thái số lượng API Key đã nạp từ tài khoản trên giao diện.
3. **Bước 3: Xây dựng kiểm thử tự động `tests/matrande-smoke.js`**:
   - Kiểm tra cấu trúc `matrande.html` có khối script Babel nguyên vẹn không bị ngắt sớm.
   - Kiểm tra 2 template Word không chứa thẻ script và khai báo `<meta charset='utf-8'>`.
   - Kiểm tra hàm `syncUserKeysFromServer` và quy trình nạp key.
4. **Bước 4: Khóa trạng thái giao việc**:
   - Ghi nội dung `LOCK` vào `docs/handoff/.lock`.

## Rủi ro
1. **Rủi ro người dùng mất mạng khi tải trang**:
   - *Giải pháp*: Hàm sync có try/catch an toàn và tự động dùng `readCachedGeminiKeys()` từ `localStorage` nếu không gọi được server.

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - Chạy lệnh: `node tests/matrande-smoke.js`
   - Chạy lệnh: `node tests/kttx-smoke.js`
   - Chạy lệnh: `node tests/xaydungphuluc-smoke.js`
2. **Kiểm thử thủ công**:
   - Mở `matrande.html` trên trình duyệt:
     * Ứng dụng tải mượt mà, không bị lỗi console cú pháp script.
     * Tự động nhận diện và hiển thị số lượng Gemini API Key đã đăng ký của tài khoản.
     * Tạo đề từ ma trận $\to$ Bấm "Xuất file Word" (`De_Thi_Toan_...doc`) và "Xuất Word Raw" $\to$ Mở file Word kiểm tra nội dung đề, bảng đáp án và lời giải hiển thị chuẩn đẹp, hoàn toàn không có mã JavaScript thô.

## Tiêu chí nghiệm thu
- [ ] Không còn thẻ `</script>` nào nằm bên trong template string của `matrande.html`.
- [ ] File Word xuất ra (`De_Thi_Toan_...doc`, `De_Thi_Toan_..._raw.doc`) hiển thị nội dung đề thi hoàn chỉnh, 100% không còn dính mã nguồn JavaScript thô.
- [ ] `matrande.html` tự động đồng bộ và nạp Gemini API Key từ tài khoản CSDL (`api/user_gemini_keys.php`) khi vào trang.
- [ ] 100% kiểm thử tự động `tests/matrande-smoke.js` chạy đạt PASS.
