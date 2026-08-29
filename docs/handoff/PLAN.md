# PLAN: Hoàn thiện Giao diện & Dữ liệu Ngoại ngữ CLIL và Giáo dục Hòa nhập (soankhbd.html)

Trạng thái: KẾ HOẠCH ĐÃ DUYỆT

## Hiện trạng
- Tab con 5 (Ngoại ngữ & Hòa nhập) còn sơ sài, thiếu bộ chọn 4 cấp độ CLIL (A1–B2) và 6 loại khuyết tật HSKT theo thực tế sư phạm.

## Phạm vi
1. **Thiết kế lại Giao diện Tab con 5 (`soankhbd.html`)**:
   - **Card 1 (Màu xanh lục - Viền xanh lá)**:
     * Toggle `toggleForeignLanguage`.
     * Grid 4 radio pills: `clilLevel` (A1, A2, B1, B2).
   - **Card 2 (Màu tím nhạt - Viền tím)**:
     * Toggle `toggleInclusiveSupport`.
     * Danh sách 6 checkbox loại khuyết tật (`disability-type-choice`).
     * Nhóm giải pháp hỗ trợ chức năng (`support-choice`).
2. **Cập nhật Logic Lưu trữ trong JS (`js/khbd-app.js`)**:
   - Thêm `clilLevel` (mặc định "A1") và `disabilityTypes: []` vào `teachingContext`.
   - Bắt sự kiện change cho radio `clilLevel` và checkbox `disability-type-choice`, tự động lưu vào `localStorage`.
   - Khôi phục trạng thái checked chính xác khi mở lại trang hoặc nạp bản nháp.
3. **Cập nhật Prompt Engineering (`js/khbd-prompts.js`)**:
   - Khi bật Ngoại ngữ: Truyền đúng cấp độ CLIL (A1: tra thuật ngữ, A2: câu lệnh ngắn, B1/B2: thảo luận/báo cáo) vào prompt.
   - Khi bật Hòa nhập: Truyền chính xác loại khuyết tật HSKT đã chọn và giải pháp hỗ trợ để AI đưa ra chỉ dẫn sư phạm màu tím trong các hoạt động.
4. **Cập nhật Bộ kiểm thử tự động**:
   - Cập nhật `tests/khbd-4steps-workflow-smoke.js` kiểm tra sự tồn tại của 4 mức CLIL và 6 loại khuyết tật HSKT.

## Ngoài phạm vi
- Không đổi tên ID của các checkbox `toggleForeignLanguage`, `toggleInclusiveSupport`, `.support-choice`.

## File dự kiến tác động
- `soankhbd.html`
- `js/khbd-app.js`
- `js/khbd-prompts.js`
- `tests/khbd-4steps-workflow-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Các bước thực hiện
1. **Bước 1: Cập nhật cấu trúc HTML Tab con 5 trong `soankhbd.html`**:
   - Xây dựng 2 Box giao diện đẹp mắt (Box xanh lục CLIL + Box tím HSKT).
2. **Bước 2: Quản lý State & Sự kiện trong `js/khbd-app.js`**:
   - Bổ sung trường `clilLevel` và `disabilityTypes` trong `normalizeTeachingContext`.
   - Gắn event listeners lưu và render dữ liệu.
3. **Bước 3: Tích hợp Prompt AI trong `js/khbd-prompts.js`**:
   - Format prompt hướng dẫn chi tiết theo cấp độ CLIL và loại khuyết tật.
4. **Bước 4: Kiểm thử tự động**:
   - Chạy `node tests/khbd-4steps-workflow-smoke.js`.

## Tiêu chí nghiệm thu
1. Tab con 5 hiển thị đúng 100% mẫu giao diện theo 2 ảnh chụp.
2. 4 mức CLIL (A1, A2, B1, B2) chọn được mượt mà, lưu vào localStorage.
3. 6 loại khuyết tật HSKT chọn được linh hoạt, lưu vào localStorage.
4. Prompt AI bám sát dữ liệu CLIL và HSKT khi tạo giáo án.
5. Bộ kiểm thử tự động pass 100%.
