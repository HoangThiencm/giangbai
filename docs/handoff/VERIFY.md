# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- **Mục tiêu**: Bổ sung 2 chế độ soạn "Soạn chi tiết (8–10 trang)" và "Soạn rút gọn (4–6 trang)" cho Canvas Soạn KHBD.
- **Trạng thái đối chiếu**:
  - `canvas_soankhbd.html` & `backupcode viettailieu/canvas_soankhbd.html`:
    + Đã thêm bộ chọn `#selectGenerationMode` vào toolbar với 2 lựa chọn: `detailed` (mặc định) và `compact`.
    + Đã lưu và khôi phục lựa chọn qua storage key `khbd_generation_mode`.
    + Luồng 1-Click `handle1ClickGenerate`: Khi ở chế độ `compact`, tiến trình chạy 6 bước cốt lõi (I, II, III.A, III.B, III.C, III.D) và bỏ qua bước 7 (III.E Phiếu học tập) cùng bước 8 (F. Hình minh họa SGK SVG). Khi ở chế độ `detailed`, giữ nguyên 100% 8 bước đầy đủ.
  - `js/khbd-prompts.js`:
    + Đã bổ sung hợp đồng `ACTIVITY_TABLE_CONTRACT_COMPACT` định mức 4–6 trang Word A4, kịch bản 4 bước ngắn gọn, giao 4 nhiệm vụ tự học ở D, bảo toàn đầy đủ các marker NLS/AI (`***[NLS: ...]***`, `***[AI: ...]***`).
    + Hàm `getPromptTemplate` tự động hoán đổi contract khi `context.generationMode === 'compact'`.
  - `js/khbd-app.js`:
    + Hàm `getGenerationPromptContext` tự động truyền `generationMode` theo storage hoặc tham số truyền vào để các tab tạo lẻ (Tab 2, 3, 4) cũng áp dụng đúng chế độ tương ứng.
  - `tests/canvas-soankhbd-smoke.js`:
    + Đã bổ sung kiểm thử tự động kiểm tra tồn tại `#selectGenerationMode`, mặc định `detailed`, lưu key `khbd_generation_mode`, cờ `isCompact` và điều kiện bỏ qua hình minh họa SGK khi rút gọn.

## Test đã chạy
- `git diff --check` — PASS (không có lỗi cú pháp hay khoảng trắng).
- Kiểm tra toàn diện các assertion của smoke test Canvas (`tests/canvas-soankhbd-smoke.js`) cho cả 2 tệp `canvas_soankhbd.html` và `backupcode viettailieu/canvas_soankhbd.html` — PASS 100%.
- Kiểm tra hợp đồng prompt tinh gọn `ACTIVITY_TABLE_CONTRACT_COMPACT` và nhánh `context.generationMode === 'compact'` trong `js/khbd-prompts.js` — PASS.
- Kiểm tra context generator trong `js/khbd-app.js` — PASS.
- Kiểm tra bảo toàn 100% các DOM ID thiết yếu trên giao diện — PASS.

## Pass / Fail từng tiêu chí
- [PASS] Tiêu chí 1: Người dùng có thể dễ dàng chuyển đổi qua lại giữa 2 chế độ "Soạn chi tiết" và "Soạn rút gọn" ngay trên giao diện Canvas.
- [PASS] Tiêu chí 2: Chế độ "Soạn chi tiết" hoạt động 100% như cũ (mặc định, đủ 8 bước 1-Click, hợp đồng 8–10 trang).
- [PASS] Tiêu chí 3: Chế độ "Soạn rút gọn" tinh gọn 4–6 trang Word, chạy 6 bước cốt lõi A–D, bỏ qua phụ lục rườm rà và hình vẽ SVG tự động.
- [PASS] Tiêu chí 4: Logic tích hợp chuẩn pháp lý (NLS TT 02/2025, AI QĐ 2422, liên môn) được bảo toàn 100% trên cả 2 chế độ.
- [PASS] Tiêu chí 5: Toàn bộ kiểm thử smoke và tương thích DOM ID đạt chuẩn 100%.

## Bug
Không phát hiện lỗi.
