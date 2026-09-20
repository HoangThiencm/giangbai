# IMPLEMENT: Khôi phục đủ 4 mục (a/b/c/d) và đủ 4 bước cho Hoạt động Mục B

Đã triển khai đúng `docs/handoff/PLAN.md`.

## Thay đổi

### 1. `js/khbd-prompts.js` — `ACTIVITY_TABLE_CONTRACT_COMPACT`
- Chế độ Soạn rút gọn vẫn BẮT BUỘC đủ 4 mục CV 5512: `#### a) Mục tiêu:`, `#### b) Nội dung:`, `#### c) Sản phẩm:`, `#### d) Tổ chức thực hiện:` (kể cả nhánh 2.1, 2.2...).
- Bảng Cột 1 BẮT BUỘC đủ 4 bước quy chuẩn: `+ Bước 1: Chuyển giao nhiệm vụ:` … `+ Bước 4: Kết luận, nhận định:`.
- Khác biệt Rút gọn chỉ còn ở độ dài câu thoại / 1 ví dụ trọng tâm — không bỏ khung cấu trúc.
- `GENERATE_ACTIVITY_B` / `expandActivityBSkeleton` vốn đã nhắc đủ 4 mục + bảng 4 bước; giữ nguyên.

### 2. `js/khbd-app.js` — viết lại `repairActivityBlockFourParts`
- Nhận diện đủ 4 cờ: `hasA`, `hasB`, `hasC`, `hasD`.
- Chuẩn hóa / chèn `#### a) Mục tiêu:` khi thiếu (câu sư phạm tĩnh).
- Chèn `#### b) Nội dung:` / `#### c) Sản phẩm:` / `#### d) Tổ chức thực hiện:` bằng câu sư phạm tĩnh khi thiếu.
- **Đã xóa** logic bóc `step1` / Cột 2 rồi `.slice(0, 400)` — không còn cắt LaTeX hay đứt câu, không phá kịch bản 4 bước.

### 3. Guard `ensureKhbdDocxFallback` (2 HTML)
- Đồng bộ đúng PLAN: `typeof window.docxGenerator !== "undefined" || typeof window.DocxGenerator !== "undefined"`.
- Cập nhật assert tương ứng trong `tests/canvas-soankhbd-smoke.js` để suite PLAN PASS.

### 4. `tests/khbd-table-columns-smoke.js`
- Thêm case Hoạt động B thiếu `a) Mục tiêu` → phải tự bổ sung `#### a) Mục tiêu:`.
- Assert giữ đủ Bước 1..4 và không cắt LaTeX/câu dài cột phải.
- Assert `repairActivityBlockFourParts` không còn `.slice(0, 400)`.
- Assert COMPACT contract có khung a/b/c/d và 4 bước quy chuẩn.

## Test đã chạy (100% PASS)

- `node tests/khbd-table-columns-smoke.js`
- `node tests/canvas-prompts-integrity-smoke.js`
- `node tests/canvas-soankhbd-smoke.js`
- `node tests/khbd-pedagogy-rate-smoke.js`
- `node tests/khbd-nls-ai-bold-italic-smoke.js`

## File đã đụng

1. `js/khbd-prompts.js`
2. `js/khbd-app.js`
3. `canvas_soankhbd.html`
4. `backupcode viettailieu/canvas_soankhbd.html`
5. `tests/khbd-table-columns-smoke.js`
6. `tests/canvas-soankhbd-smoke.js` (assert guard docx theo PLAN)
7. `docs/handoff/IMPLEMENT.md`

UI E2E / Canvas generation → Antigravity `/verify`.
