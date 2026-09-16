# PLAN: Nâng cấp Kịch bản Sư phạm 4 bước, Khắc phục lỗi Failed to fetch Hoạt động C, và Chia tỉ lệ cột 2:1

## Hiện trạng

1. **Ý 1 - Kịch bản sư phạm 4 bước còn nặng tính "văn mẫu hành chính"**:
   - Cột "Hoạt động của GV và HS" đang sinh theo khuôn mẫu chung chung: GV chỉ ra lệnh ngắn ("Các em hãy làm HĐ1, HĐ2..."), thiếu hẳn hành động thao tác cụ thể của học sinh, thiếu dự kiến câu trả lời/sản phẩm của học sinh (cả câu trả lời đúng và lỗi sai/ngộ nhận điển hình), thiếu diễn biến chất vấn - phản biện thực tế giữa GV-HS và HS-HS ở bước Báo cáo, thiếu nhận xét chốt kiến thức và quy tắc then chốt ở bước Kết luận.
2. **Ý 2 - Lỗi `TypeError: Failed to fetch` khi tạo Hoạt động C (Luyện tập)**:
   - Prompt C (`GENERATE_ACTIVITY_C`) rất dài (17.868 ký tự).
   - Mô hình Canvas mặc định là `gemini-3-flash-preview` có cơ chế suy luận/thinking nội bộ, mất hơn 85 giây để xử lý.
   - Xung đột timeout đa tầng: Client `js/khbd-app.js` khống chế 75s, Server PHP khống chế 55s, Web Server LiteSpeed ngắt kết nối ở ~60s làm rớt kết nối mạng đột ngột dẫn đến `Failed to fetch`.
   - Thực nghiệm cho thấy mô hình `gemini-2.5-flash` xử lý cùng Prompt C chỉ mất **16,5 giây** (nhanh gấp 5 lần, HTTP 200 ổn định tuyệt đối).
3. **Ý 3 - Bảng hoạt động dạy học đang chia đều 50% - 50%**:
   - Hiện tại trong `js/khbd-docx.js` (dòng 909) và trên Web CSS, bảng 2 cột hoạt động đang chia đều `[4819, 4820]` dxa (50% - 50%).
   - Cột GV - HS chứa toàn bộ 4 bước sư phạm, lời thoại và kịch bản phân vai nên bị ép hẹp, chữ xuống dòng vụn vặt làm kéo dài trang giáo án. Trong khi cột Nội dung chỉ ghi bảng tóm tắt lại bị thừa nhiều khoảng trống.

---

## Phạm vi

1. **Nâng cấp Prompt Sư phạm trong `js/khbd-prompts.js` và `js/khbd-app.js`**:
   - Bổ sung chỉ dẫn kịch bản thực chiến vào hợp đồng bảng 2 cột (`ACTIVITY_TABLE_CONTRACT` và các prompt nhánh B, C, D):
     + **Bước 1 (Chuyển giao)**: GV nêu câu lệnh rõ ràng, phương tiện (phiếu học tập/bảng nhóm), thời gian và phân công vai trò.
     + **Bước 2 (Thực hiện)**: Thao tác của HS; **bắt buộc có "Dự kiến câu trả lời của HS"** (kết quả và lỗi sai điển hình); GV quan sát, gợi mở xử lý phân hóa.
     + **Bước 3 (Báo cáo)**: Diễn biến báo cáo (chiếu bài/dán bảng), lời thoại chất vấn - phản biện giữa các nhóm và câu hỏi gợi mở của GV.
     + **Bước 4 (Kết luận)**: GV nhận xét tinh thần học tập, chốt kiến thức chuẩn mực và nhấn mạnh "quy tắc vàng" / chú ý quan trọng cần ghi nhớ.
2. **Khắc phục lỗi mạng và tối ưu tốc độ sinh**:
   - Cấu hình model mặc định của Canvas trong `canvas_soankhbd.html` & `backupcode viettailieu/canvas_soankhbd.html` sang `gemini-2.5-flash` (nhanh, ổn định).
   - Thêm cơ chế tự động Fallback trong `api/canvas_gemini.php`: nếu model chính gặp lỗi hoặc quá thời gian, tự động chuyển sang `gemini-2.5-flash` trước khi trả lỗi.
   - Nâng client timeout trong `js/khbd-app.js` lên 95.000ms.
3. **Chia tỉ lệ cột bảng hoạt động thành 2 : 1 (66.7% : 33.3%)**:
   - Trong `js/khbd-docx.js`: Điều chỉnh độ rộng cột 2 cột `isActivityTwoCol` từ `[4819, 4820]` thành `[6426, 3213]` dxa (tổng 9.639 dxa: cột GV-HS chiếm 2 phần ~66.7%, cột Nội dung chiếm 1 phần ~33.3%).
   - Trong `css/khbd-styles.css` (và style của Canvas): Định nghĩa CSS cho bảng 2 cột của `.preview-rendered table` để cột 1 chiếm `66.67%` và cột 2 chiếm `33.33%`.
4. **Nâng version cache-busting**:
   - Nâng lên `20260916-textbook-exact-v18` cho toàn bộ các file HTML, JS liên quan.

---

## Ngoài phạm vi

- Không thay đổi cấu trúc bảng 2 cột sang 3 cột hay nhiều hàng (vẫn giữ đúng chuẩn bảng 2 cột, 1 hàng của hệ thống).
- Không sửa đổi logic bóc tách SGK Vision Bước 0.

---

## File dự kiến tác động

1. `js/khbd-prompts.js`
2. `js/khbd-docx.js`
3. `css/khbd-styles.css`
4. `canvas_soankhbd.html`
5. `backupcode viettailieu/canvas_soankhbd.html`
6. `api/canvas_gemini.php`
7. `js/khbd-app.js`
8. `tests/khbd-table-columns-smoke.js`
9. `tests/canvas-prompts-integrity-smoke.js`
10. `tests/canvas-activity-b-multi-branches-smoke.js`

---

## Các bước thực hiện

### Bước 1: Nâng cấp kịch bản sư phạm 4 bước trong `js/khbd-prompts.js`
- Cập nhật mục `CỘT TRÁI — KỊCH BẢN THỰC CHIẾN PHÂN VAI RÕ RÀNG`:
  + Bước 1: Giao rõ nhiệm vụ, thời gian, công cụ.
  + Bước 2: Bắt buộc mô tả thao tác và **Dự kiến câu trả lời của HS** (kết quả và lỗi sai điển hình môn học).
  + Bước 3: Diễn biến thảo luận, đối thoại chất vấn - phản biện thực tế.
  + Bước 4: GV nhận xét, chốt kiến thức và quy tắc cốt lõi ghi vở.

### Bước 2: Đổi tỉ lệ cột 2:1 trong `js/khbd-docx.js` và `css/khbd-styles.css`
- Trong `js/khbd-docx.js` dòng 908:
  ```javascript
  const columnWidths = isActivityTwoCol
    ? [6426, 3213]
    : Array.from({ length: columnCount }, (_, idx) => { ... });
  ```
- Trong `css/khbd-styles.css`:
  ```css
  .preview-rendered table th:first-child:nth-last-child(2),
  .preview-rendered table td:first-child:nth-last-child(2) {
    width: 66.67%;
  }
  .preview-rendered table th:last-child:nth-child(2),
  .preview-rendered table td:last-child:nth-child(2) {
    width: 33.33%;
  }
  ```

### Bước 3: Cấu hình Model và Fallback chống lỗi `Failed to fetch`
- Trong `canvas_soankhbd.html` và `backupcode viettailieu/canvas_soankhbd.html`:
  + Sửa `model: "gemini-2.5-flash"` trong `window.__KHBD_CANVAS__`.
  + Đồng bộ nhãn footer: `<span id="footerModelName">gemini-2.5-flash</span>`.
- Trong `api/canvas_gemini.php`:
  + Thêm cơ chế nếu model được yêu cầu gặp lỗi timeout/network, thử lại một lần với `gemini-2.5-flash`.
- Trong `js/khbd-app.js`:
  + Tăng `timeoutMs` lên `95000` ở dòng 7386.

### Bước 4: Đồng bộ Cache Busting `v18` và Cập nhật Tests
- Nâng version lên `20260916-textbook-exact-v18` trong Canvas HTML, JS headers.
- Cập nhật test `tests/khbd-table-columns-smoke.js` assert `[6426, 3213]`.
- Cập nhật test `tests/canvas-prompts-integrity-smoke.js` và `tests/canvas-activity-b-multi-branches-smoke.js` lên version `v18`.

---

## Rủi ro

- Khi thay đổi tỉ lệ cột, các bảng khác không phải 2 cột hoạt động không được bị ảnh hưởng. Giải pháp: Chỉ áp dụng `isActivityTwoCol` và bộ chọn CSS `th:first-child:nth-last-child(2)` cho đúng bảng 2 cột.
- Kịch bản sư phạm chi tiết hơn có thể làm tăng dung lượng đầu ra của Gemini. Giải pháp: Yêu cầu hành văn cô đọng, trực diện, không dài dòng.

---

## Cách kiểm thử

1. Chạy `node tests/khbd-table-columns-smoke.js` kiểm tra độ rộng cột xuất Word `[6426, 3213]`.
2. Chạy `node tests/canvas-prompts-integrity-smoke.js` và `node tests/canvas-activity-b-multi-branches-smoke.js` đảm bảo tương thích cache-busting `v18`.
3. Chạy `node tests/canvas-soankhbd-smoke.js`, `canvas-gemini-api-smoke.js`.
4. Gọi thử nghiệm trực tiếp Prompt C với API `canvas_gemini.php` đo thời gian dưới 25s, không bị lỗi mạng.

---

## Tiêu chí nghiệm thu

1. Cột bảng hoạt động xuất Word (.docx) chia đúng tỉ lệ 2 : 1 (`6.426 dxa` cho GV-HS và `3.213 dxa` cho Nội dung).
2. Tạo Hoạt động C trên Canvas phản hồi nhanh, mượt mà, triệt tiêu 100% lỗi `Failed to fetch`.
3. Kịch bản dạy học có đủ chi tiết sư phạm: câu lệnh GV, thao tác HS, dự kiến câu trả lời/lỗi sai của HS, diễn biến chất vấn - phản biện và chốt kiến thức.
4. Toàn bộ test liên quan đạt PASS 100%.


