# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] **Chặng 1 — Structural Indexing (`api/duyetde_ai.php?action=extract_matrix_index`)**:
  - Chỉ gửi PDF/văn bản ma trận & bảng đặc tả (Gemini Multimodal). Tuyệt đối không gửi đề thi.
  - Chuẩn hóa cấu trúc `SpecificationMatrixIndex`: `tong_quan` (tỉ lệ 40-30-20-10, tổng điểm 10.0, thời gian) và `danh_sach_chi_tieu` (mã `SPEC_xx`, `cac_y_con` cho Phần II Đúng/Sai, `yeu_cau_ngu_lieu`, `vi_tri_du_kien`).
- [x] **Chặng 2 — Human-in-the-loop + Slot Matching & Batching**:
  - `duyetde.html`: Nạp ma trận/đặc tả tự động trích xuất chỉ mục, hiển thị tóm tắt "Đã nhận diện X chỉ tiêu | Tỉ lệ: 40-30-20-10 | Tổng điểm: 10.0".
  - Nút "Bắt đầu rà soát đề" bị khóa cho đến khi giáo viên bấm "Xác nhận bảng chỉ mục".
  - `evaluate_exam`: Bắt buộc nhận `matrix_index`, chia theo từng phần (Phần I, II, III, Tự luận) để đối chiếu, không gửi đính kèm 8–9 trang PDF ma trận cùng đề thi.
- [x] **Chặng 3 — Recheck 1 SPEC siêu tốc**:
  - `recheck_question` chỉ nhận đúng 1 object chỉ tiêu (`spec` / `spec_id`), đối chiếu riêng câu đã sửa mà không đọc lại toàn bộ PDF ma trận.
- [x] **Tiêu chí thực chiến trường học**:
  - Cảnh báo thời lượng làm bài dự kiến và cảnh báo lệch tỉ lệ % điểm số ma trận tổng thể.
  - Bảo toàn mô tả hình vẽ / đồ thị cho các câu hình học, toán thực tế.
  - Mẫu biên bản thẩm định xuất Word có đầy đủ phần ký tên của Giáo viên ra đề, Tổ trưởng chuyên môn và Phó Hiệu trưởng (BGH).
  - Bổ sung nút xuất file Word Hướng dẫn chấm chính thức (`.docx`).
  - Hỗ trợ tải tệp PDF dung lượng lớn (lên đến ~8MB / 12MB base64) cho các bộ ma trận – đặc tả dài 6–10 trang.

## Test đã chạy
1. `node scratch/verify-pipeline.js` — **PASS 100%**:
   - Kiểm tra endpoint `extract_matrix_index` trong `api/duyetde_ai.php`: PASSED
   - Kiểm tra chuẩn hóa chỉ mục `duyetde_normalize_matrix_index`: PASSED
   - Kiểm tra phân nhóm theo phần `duyetde_group_specs_by_part`: PASSED
   - Kiểm tra cảnh báo thời lượng và tỷ lệ: PASSED
   - Kiểm tra luồng `confirmMatrixIndex` và khóa nút rà soát trong `duyetde.html`: PASSED
   - Kiểm tra xuất Word biên bản và đề thi/đáp án hoàn chỉnh: PASSED
2. `node scratch/verify-duyetde.js` — **PASS 100%**:
   - Kiểm tra cấu trúc DOM và tích hợp script/thư viện của `duyetde.html`: PASSED
   - Kiểm tra bảo vệ quyền `access-control.js`: PASSED
   - Kiểm tra bảng quản trị `admin.html`: PASSED
   - Kiểm tra thẻ công cụ `index.html`: PASSED
   - Kiểm tra mã hóa AES-256 trong `api/helpers.php` và `api/user_gemini_keys.php`: PASSED
   - Kiểm tra lưu trữ phiên bản và CSDL `api/duyetde.php`: PASSED
3. `node tests/khbd-user-ai-keys-smoke.js` — **PASS**
4. `node tests/duyetgiaoan-integration-smoke.js` — **PASS**
5. `node tests/duyetgiaoan-smoke.js` — **PASS**
6. `node tests/matrande-smoke.js` — **PASS**
7. `node tests/security-f12-smoke.js` — **PASS**

## Pass / Fail từng tiêu chí
- [x] Trích xuất ma trận độc lập không gửi kèm đề thi: **PASS**
- [x] Bóc tách đầy đủ 4 bẫy nghiệp vụ (Đúng/Sai `cac_y_con`, ma trận không mã câu `Target Specs`, `yeu_cau_ngu_lieu`, tỷ lệ % tổng thể): **PASS**
- [x] Cơ chế Human-in-the-loop xác nhận chỉ mục trước khi rà soát: **PASS**
- [x] Đối chiếu đề theo lô (Phần I, II, III, Tự luận) với Bảng chỉ mục JSON: **PASS**
- [x] Kiểm tra lại câu sửa (Re-verify) chỉ dùng 1 spec, phản hồi tức thì: **PASS**
- [x] Cảnh báo thời lượng và tỷ lệ ma trận: **PASS**
- [x] Xuất Đề thi, Đáp án và Biên bản thẩm định chuẩn form ký duyệt BGH ra `.docx`: **PASS**

## Bug
- Không phát hiện lỗi.