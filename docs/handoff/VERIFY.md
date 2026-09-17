# VERIFY: Chuẩn Hóa Mục II (Thiết Bị Dạy Học & Học Liệu) Cho Chế Độ Rút Gọn & Khi Không Dùng PPDH/KTDH Riêng

## Kết luận
PASS

## Đối chiếu scope theo `docs/handoff/PLAN.md`
- [x] **Module 1**: Cập nhật prompt gốc `GENERATE_MATERIALS` trong `js/khbd-prompts.js` (dòng 562): Thêm ràng buộc `TƯƠNG THÍCH SƯ PHẠM BẮT BUỘC`, cấm AI đưa học liệu của các kỹ thuật không được chọn (cấm phiếu trạm, cấm Exit Ticket, cấm thẻ màu, cấm bảng phụ A0) — **PASS**.
- [x] **Module 2**: Cập nhật `getPromptTemplate` trong `js/khbd-prompts.js` (dòng 1616–1636):
  - Khi `generationMode === 'compact'`: Bổ sung khối `RÀNG BUỘC CHẾ ĐỘ SOẠN RÚT GỌN (4–6 TRANG)` cấm phiếu trạm, Exit Ticket, thẻ màu, bảng phụ A0, rubric phức tạp — **PASS**.
  - Khi `!selectedMethods.length && !selectedTechniques.length`: Bổ sung khối `RÀNG BUỘC KHÔNG CHỌN PPDH/KTDH RIÊNG`, chỉ cho phép học liệu trực quan thông thường (máy chiếu/bài giảng điện tử nếu có, SGK, vở ghi, thước, máy tính cầm tay, phiếu bài tập ngắn nếu cần) — **PASS**.
- [x] **Module 3**: Bổ sung test hồi quy trong `tests/khbd-pedagogy-script-smoke.js` (dòng 165–177) xác nhận các ràng buộc Mục II rút gọn và không chọn PPDH/KTDH hoạt động chính xác — **PASS**.
- [x] **Không đụng file ngoài plan**: Chỉ sửa `js/khbd-prompts.js` và `tests/khbd-pedagogy-script-smoke.js`.

---

## Test đã chạy
1. `node tests/canvas-soankhbd-smoke.js` — **PASS 100%**:
   - Cú pháp JavaScript hợp lệ.
   - Tương thích 1-1 giữa hai bản Canvas.
2. `node tests/khbd-pedagogy-rate-smoke.js` — **PASS 100%**:
   - Định mức PPDH/KTDH theo số tiết và chuẩn hóa xuống dòng GV/HS.
3. `node tests/khbd-pedagogy-script-smoke.js` — **PASS 100%**:
   - Bộ test Mục II rút gọn và không chọn PPDH/KTDH đạt 100%.
   - Xuất Word DOCX và kịch bản thực chiến đạt chuẩn.
4. `node tests/khbd-dynamic-time-budgets-smoke.js` — **PASS 100%**:
   - Phân bổ thời lượng động A–D nguyên vẹn.
5. `node tests/canvas-prompts-integrity-smoke.js` — **PASS 100%**.
6. `node tests/canvas-soanbaigiang-smoke.js` — **PASS 100%**.
7. `node tests/khbd-subject-integrations-smoke.js` — **PASS 100%**.

---

## Bug
Không có.

