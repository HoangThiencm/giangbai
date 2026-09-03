# IMPLEMENT: Pipeline 3 chặng bóc tách Ma trận – Đặc tả dài (duyetde)

## Đã làm

1. **Chặng 1 — Structural Indexing** (`api/duyetde_ai.php` `action=extract_matrix_index`):
   - Chỉ gửi PDF/văn bản ma trận và bảng đặc tả (Gemini Multimodal). Không gửi đề thi.
   - Chuẩn hóa `SpecificationMatrixIndex`: `tong_quan` (tỉ lệ 40-30-20-10, tổng điểm, thời gian) + `danh_sach_chi_tieu` (`id` SPEC_xx, `cac_y_con` cho Đúng/Sai, `yeu_cau_ngu_lieu`, `vi_tri_du_kien` có thể trống khi ma trận chỉ ghi số lượng).
2. **Chặng 2 — Human-in-the-loop + Slot Matching & Batching**:
   - `duyetde.html`: sau khi nạp ma trận/đặc tả tự bóc tách, hiện "Đã nhận diện X chỉ tiêu | Tỉ lệ: 40-30-20-10 | Tổng điểm: 10.0". Nút rà soát khóa đến khi giáo viên xác nhận chỉ mục.
   - `evaluate_exam` bắt buộc nhận JSON chỉ mục, đối chiếu theo từng Phần I / II / III / Tự luận. Không đính kèm 8–9 trang PDF ma trận cùng đề thi.
3. **Chặng 3 — Recheck 1 SPEC**:
   - `recheck_question` chỉ nhận đúng 1 object chỉ tiêu (`spec` / `spec_id`). Không đọc lại PDF ma trận.
4. **Bổ sung thực chiến**: cảnh báo thời lượng và lệch tỉ lệ/điểm; giữ mô tả hình vẽ; xuất biên bản có chỗ ký GV – Tổ trưởng – BGH; xuất hướng dẫn chấm chính thức `.docx`.
5. Nâng hạn PDF (tới ~8MB file / 12MB base64) để nhận ma trận 6–10 trang.

## File đã sửa

- `api/duyetde_ai.php`
- `duyetde.html`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/.lock` (LOCK)

## Không đụng

- `matrande.html`, `soankhbd.html`, `duyetgiaoan.html`, `thitructuyen.html`
- `docs/handoff/PLAN.md`
- Không commit

## Kiểm thử

- Không có PHP CLI trên máy này.
- Không verify trên trình duyệt (không có browser tools / PHP server trong phiên này).
- Rà soát tĩnh: `extract_matrix_index` không nhận đề thi; `evaluate_exam` không gọi `duyetde_file_parts(..., 'matrix'|'spec')`; `recheck_question` không đính PDF ma trận.
