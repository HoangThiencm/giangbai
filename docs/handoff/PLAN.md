# PLAN: Chuẩn Hóa Mục II (Thiết Bị Dạy Học & Học Liệu) Cho Chế Độ Rút Gọn & Khi Không Dùng PPDH/KTDH Riêng

## User Review Required
> [!IMPORTANT]
> - Ở **Chế độ Soạn rút gọn (4–6 trang)** hoặc khi **người dùng không chọn PPDH / KTDH riêng**: Mục **II. Thiết bị dạy học và học liệu** phải được tinh giản tối đa, chỉ liệt kê đồ dùng dạy học trực quan và thiết bị cơ bản.
> - **Tuyệt đối cấm** AI tự ý liệt kê học liệu của các phương pháp/kỹ thuật nâng cao không được sử dụng trong bài (như: Phiếu học tập phân hóa theo trạm, Phiếu Exit Ticket, Bộ thẻ màu đánh giá nhanh, Bảng phụ A0...).

---

## I. Hiện Trạng & Phân Tích Nguyên Nhân

### 1. Hiện tượng
- Khi soạn giáo án ở **Chế độ Soạn rút gọn** hoặc khi người dùng đã bỏ tick các PPDH/KTDH và không tạo Pha E (Hồ sơ đánh giá), AI vẫn sinh ra mục II với nội dung rườm rà, hình thức:
  ```text
  + Hệ thống phiếu học tập (Phiếu số 1: Bài toán mở đầu và Ví dụ 1; Phiếu số 2: Bài tập phân hóa theo trạm; Phiếu số 3: Exit Ticket).
  + Bộ thẻ màu (Xanh, Vàng, Đỏ) phục vụ kỹ thuật đánh giá nhanh mức độ hiểu bài và bảng phụ khổ A0 cho hoạt động nhóm.
  ```
- Đây là lỗi mâu thuẫn sư phạm nghiêm trọng ("râu ông nọ cắm cằm bà kia"):
  1. *Phiếu phân hóa theo trạm*: Chỉ dùng khi áp dụng PPDH Dạy học theo trạm.
  2. *Exit Ticket*: Thuộc KTDH Exit Ticket hoặc Pha E (Hồ sơ đánh giá). Bản rút gọn không có Pha E.
  3. *Bộ thẻ màu*: Thuộc KTDH Thẻ màu.
  4. *Bảng phụ khổ A0*: Thuộc KTDH Khăn trải bàn hoặc thảo luận nhóm lớn.

### 2. Nguyên nhân kỹ thuật
1. Trong `js/khbd-prompts.js` (`GENERATE_MATERIALS`):
   - Mẫu chỉ dẫn và ví dụ chỉ có yêu cầu chung chung: *"Tạo danh mục thiết bị và học liệu thiết yếu, cụ thể cho đúng bài dạy..."*, *"Phiếu học tập, bảng phụ nhóm và các dụng cụ trực quan phục vụ bài dạy."*
   - Thiếu hoàn toàn điều khoản ràng buộc: Học liệu phải bám sát các PPDH/KTDH đã chọn.
2. Trong `getPromptTemplate('GENERATE_MATERIALS', context)` (`js/khbd-prompts.js`):
   - Chưa xử lý trường hợp `context.generationMode === 'compact'`.
   - Chưa kiểm tra trường hợp `context.methods` và `context.techniques` rỗng (người dùng không chọn hoặc đã bỏ tick).
   - Dẫn đến LLM tự do suy diễn và lấy các học liệu nâng cao từ catalog đưa vào Mục II cho dài.

---

## II. Kế Hoạch Triển Khai Chi Tiết

### Module 1: Cập Nhật Prompt `GENERATE_MATERIALS` Trong `js/khbd-prompts.js`
1. Sửa chỉ thị `GENERATE_MATERIALS` (dòng ~553–573):
   - Bổ sung nguyên tắc tương thích 100% với PPDH/KTDH:
     - Danh mục thiết bị và học liệu CHỈ được liệt kê các công cụ phục vụ trực tiếp cho các PPDH và KTDH đã được chọn trong Bối cảnh sư phạm.
     - **TUYỆT ĐỐI CẤM** tự ý đưa tên hoặc học liệu của các phương pháp/kỹ thuật KHÔNG được chọn:
       + CẤM "phiếu theo trạm" nếu không chọn PPDH Dạy học theo trạm.
       + CẤM "Exit Ticket / vé ra cửa" nếu không chọn KTDH Exit Ticket hoặc ở chế độ rút gọn (đã bỏ Pha E).
       + CẤM "thẻ màu (Xanh, Vàng, Đỏ)" nếu không chọn KTDH Thẻ màu.
       + CẤM "bảng phụ khổ A0" nếu không chọn KTDH Khăn trải bàn / Phòng tranh.
   - Định dạng chuẩn mực đầu ra khi tinh gọn:
     - **1. Đối với Giáo viên**: SGK, SGV, Kế hoạch bài dạy; Thiết bị trình chiếu / bài giảng điện tử (trình chiếu hình ảnh, đề bài, bảng số liệu); Thước kẻ, dụng cụ trực quan bộ môn (nếu có); Phiếu học tập/bài tập ngắn (chỉ khi có bài tập cần phát tay).
     - **2. Đối với Học sinh**: SGK, vở ghi, đồ dùng học tập thiết yếu của môn học (bút, thước kẻ, máy tính cầm tay,...).

### Module 2: Bổ Sung Ràng Buộc Trong `getPromptTemplate` (`js/khbd-prompts.js`)
1. Trong hàm `getPromptTemplate(templateKey, context)`:
   - Khi `templateKey === 'GENERATE_MATERIALS'`:
     - Nếu `context.generationMode === 'compact'`:
       Chèn chỉ thị đặc thù chế độ rút gọn:
       ```text
       RÀNG BUỘC CHẾ ĐỘ SOẠN RÚT GỌN (4–6 TRANG):
       - Đây là giáo án rút gọn, không có Pha E (Hồ sơ học tập & Đánh giá).
       - Thiết bị và học liệu phải tinh giản tối đa, phục vụ dạy học trực tiếp, vấn đáp và luyện tập cơ bản.
       - TUYỆT ĐỐI CẤM liệt kê: phiếu theo trạm, phiếu Exit Ticket, bộ thẻ màu đánh giá nhanh, bảng phụ A0, rubric đánh giá phức tạp.
       ```
     - Nếu `(!context.methods || context.methods.length === 0) && (!context.techniques || context.techniques.length === 0)`:
       Chèn chỉ thị cấm học liệu kỹ thuật chuyên biệt:
       ```text
       RÀNG BUỘC KHÔNG CHỌN PPDH/KTDH RIÊNG:
       - Người dùng không áp dụng PPDH hoặc KTDH chuyên biệt nào (đã bỏ tick).
       - Học liệu chỉ gồm phương tiện trực quan thông thường (máy chiếu/bài giảng điện tử nếu có, SGK, vở ghi, thước, máy tính cầm tay, phiếu bài tập ngắn nếu cần).
       - TUYỆT ĐỐI CẤM tự ý đưa học liệu của bất kỳ kỹ thuật nâng cao nào vào bài.
       ```

### Module 3: Kiểm Thử Tự Động (Smoke Tests)
1. Cập nhật `tests/canvas-soankhbd-smoke.js` hoặc `tests/khbd-pedagogy-script-smoke.js`:
   - Thêm test case kiểm tra `getPromptTemplate('GENERATE_MATERIALS', { generationMode: 'compact', methods: [], techniques: [] })`.
   - Xác nhận prompt sinh ra chứa đầy đủ các chỉ thị cấm phiếu trạm, Exit Ticket, thẻ màu, bảng A0.
   - Chạy toàn bộ test suites hiện có đảm bảo PASS 100%.

---

## III. Danh Sách File Cần Chỉnh Sửa

| Tệp tin | Vị trí | Mục đích thay đổi |
| :--- | :--- | :--- |
| `js/khbd-prompts.js` | Dòng ~553–573 (`GENERATE_MATERIALS`) | Cập nhật prompt gốc Mục II: cấm học liệu kỹ thuật không chọn, chuẩn hóa khung tinh gọn |
| `js/khbd-prompts.js` | Dòng ~1610–1650 (`getPromptTemplate`) | Bổ sung logic chèn ràng buộc rút gọn và không chọn PPDH/KTDH cho `GENERATE_MATERIALS` |
| `tests/canvas-soankhbd-smoke.js` | Cuối file | Bổ sung test kiểm thử tự động cho prompt `GENERATE_MATERIALS` |

---

## IV. Kế Hoạch Kiểm Thử (Verification Plan)

### 1. Kiểm thử tự động
- `node tests/canvas-soankhbd-smoke.js` — PASS 100%.
- `node tests/khbd-pedagogy-rate-smoke.js` — PASS 100%.
- `node tests/khbd-pedagogy-script-smoke.js` — PASS 100%.

### 2. Kiểm thử nội dung Prompt (Node VM)
- Chạy thử nghiệm tạo prompt `GENERATE_MATERIALS` với ngữ cảnh rút gọn + mảng methods/techniques rỗng:
  - Khẳng định prompt có chỉ thị cấm "phiếu trạm", "Exit Ticket", "thẻ màu", "bảng phụ A0".
