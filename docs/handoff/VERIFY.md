# VERIFY

## Kết luận
PASS

## Đối chiếu scope
1. **Sửa lỗi xuất file Word (Đề thi, Ma trận, Bản đặc tả) trong `kttx.html`**:
   - Đã gỡ bỏ hoàn toàn thẻ `<script src="js/security-guard.js"></script>` khỏi cả 3 template HTML sinh Word (`exportWord`, `exportMatrixToWord`, `renderSpecHtml`).
   - Loại bỏ thẻ đóng `</div>` mồ côi tại header đề thi và chuẩn hóa thẻ `<meta charset='utf-8'>`.
   - Trình phân tích Babel/React không còn bị ngắt sớm bởi thẻ `</script>`, đảm bảo file Word (.doc) xuất ra hiển thị nội dung câu hỏi, bảng ma trận, bản đặc tả và công thức toán MathML/WordML sạch đẹp, không còn dính mã JavaScript thô.
2. **Cấp lại & Tự động đồng bộ Gemini API Key từ tài khoản CSDL**:
   - Triển khai hàm `syncUserKeysFromServer()` kết nối tới `api/user_gemini_keys.php` với session đăng nhập hiện tại.
   - Tự động nạp key vào React state khi mount và cache vào `localStorage ('global_gemini_keys')`.
   - Hiển thị thông báo trạng thái rõ ràng về số lượng Gemini API Key đã nạp từ tài khoản/bộ nhớ tạm.
3. **Kiểm thử tự động (`tests/kttx-smoke.js`)**:
   - Kiểm tra khối Babel không bị ngắt, 3 template Word không chứa thẻ script, template đề thi không chứa thẻ div thừa, cơ chế gọi `api/user_gemini_keys.php` và fallback an toàn đều đạt chuẩn.

## Test đã chạy
- `node tests/kttx-smoke.js` $\to$ PASS
- `node tests/xaydungphuluc-smoke.js` $\to$ PASS
- `node tests/xaydungphuluc-integration-smoke.js` $\to$ PASS

## Pass / Fail từng tiêu chí
- [x] Không còn bất kỳ thẻ `</script>` nào nằm bên trong template string của `kttx.html`: PASS
- [x] File Word xuất ra (`KiemTra_...doc`, `MaTran_...doc`, `BanDacTa_...doc`) hiển thị nội dung đề thi, bảng ma trận và bản đặc tả hoàn chỉnh, 100% không còn dính mã nguồn JavaScript thô: PASS
- [x] `kttx.html` tự động đồng bộ và cấp Gemini API Key từ tài khoản CSDL (`api/user_gemini_keys.php`) khi vào trang: PASS
- [x] Kiểm thử tự động `tests/kttx-smoke.js` chạy đạt PASS: PASS

## Bug
*(Không có)*
