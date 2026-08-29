# PLAN: Tái Cấu trúc Giao diện Tab 0 thành 5 Tab Con Khoa học & Gọn gàng (soankhbd.html)

Trạng thái: KẾ HOẠCH ĐÃ DUYỆT

## Hiện trạng
- Tab 0 xếp chồng toàn bộ khối học liệu, thông tin bài dạy, PPDH, Năng lực số, Năng lực AI, Ngoại ngữ và Hòa nhập trên một trang dài, gây rối và phải cuộn trang nhiều lần.

## Phạm vi
1. **Thiết kế Hệ thống 5 Tab Con trong Tab 0 (`soankhbd.html`)**:
   - **Tab con 1: `tab0-sub-materials` (📁 1. Gửi file & Đọc SGK/PPCT)**:
     * Cột SGK: Vùng nạp PDF/ảnh (Ctrl+V) -> Nút "📖 Đọc sách giáo khoa" đặt ngay dưới -> Accordion xem chi tiết văn bản OCR.
     * Cột PPCT: Vùng nạp PDF/ảnh PPCT (Ctrl+V) -> Nút "📑 Đọc PPCT" đặt ngay dưới -> Accordion xem chi tiết phân tích PPCT.
     * Card tạo hình minh họa SGK đặt ở cuối tab này.
   - **Tab con 2: `tab0-sub-lesson-info` (✍️ 2. Nhập thông tin bài dạy & Lớp)**:
     * Tên Trường, Tổ Bộ môn, Họ tên Giáo viên, Môn học.
     * Tên Bài học, Thời lượng (số tiết), Phạm vi tiết dạy theo PPCT.
     * Bối cảnh lớp & Cơ sở vật chất: Sĩ số, Mức sẵn sàng, Cách tổ chức nhóm, Máy chiếu, Internet, Thiết bị học sinh, Đặc điểm lớp học.
     * Nút "✨ Đề xuất thông tin bài dạy" + Quản lý bản nháp.
   - **Tab con 3: `tab0-sub-pedagogy-digital` (⚡ 3. PPDH, Năng lực số & Tích hợp môn)**:
     * Nút hành động: `⚡ ĐỀ XUẤT PPDH, KỸ THUẬT & NĂNG LỰC SỐ (TT 02)`.
     * Bảng lựa chọn Phương pháp dạy học & Kỹ thuật dạy học 4 pha (A, B, C, D).
     * Khung Năng lực số chuẩn TT 02/2025 & CV 3456 (tự mở nhóm có 2–3 mục được tick).
     * Tích hợp môn đặc thù: Giáo dục địa phương, Tư tưởng HCM, GDQPAN (TT 08/2024), Quyền con người (QĐ 1309), GD Tài chính (QĐ 149)...
   - **Tab con 4: `tab0-sub-ai-competency` (✨ 4. Tích hợp Khung Năng lực AI - QĐ 2422)**:
     * Khung độc lập hoàn toàn cho Năng lực AI theo QĐ 2422/QĐ-BGDĐT.
     * Checkbox bật/tắt độc lập; khi bật thì Gemini tự chọn đúng 2–3 mục AI theo khối lớp (`6.A...`, `7.A...`, `8.A...`, `9.A...`).
   - **Tab con 5: `tab0-sub-language-inclusive` (🌐 5. Ngoại ngữ & Giáo dục Hòa nhập)**:
     * Tích hợp Ngoại ngữ (CLIL / thuật ngữ tiếng Anh).
     * Giáo dục hòa nhập: Hỗ trợ chức năng (chia nhỏ nhiệm vụ, học liệu chữ lớn, phân vai phù hợp...).
2. **Logic Điều khiển Chuyển Tab Con trong JS (`js/khbd-app.js`)**:
   - Viết hàm `switchTab0Subtab(subtabKey)`: Quản lý active tab và hiển thị đúng pane tương ứng.
   - Đồng bộ liên kết giữa Stepper 4 bước đầu trang và các tab con để giáo viên bấm vào bước nào sẽ tự nhảy vào tab con tương ứng.
   - Giữ nguyên toàn bộ ID inputs, event listeners và lưu trữ localStorage.
3. **Cập nhật Bộ kiểm thử tự động**:
   - Cập nhật `tests/khbd-4steps-workflow-smoke.js` kiểm tra sự tồn tại và tương tác của 5 sub-tabs trong Tab 0.

## Ngoài phạm vi
- Không thay đổi tên ID của bất kỳ input/select/checkbox nào để đảm bảo tính toàn vẹn 100% của dữ liệu.
- Không thay đổi logic của Tab 1 (Mục tiêu), Tab 2 (Thiết bị), Tab 3 (Tiến trình A–F).

## File dự kiến tác động
- `soankhbd.html`
- `js/khbd-app.js`
- `tests/khbd-4steps-workflow-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Các bước thực hiện
1. **Bước 1: Cấu trúc lại giao diện HTML trong `soankhbd.html`**:
   - Thêm `<div class="tab0-subtabs-nav">` với 5 nút tab con có icon trực quan.
   - Bọc từng khu vực tương ứng vào 5 `<div class="tab0-subtab-pane">`.
2. **Bước 2: Viết logic chuyển tab con trong `js/khbd-app.js`**:
   - Thêm hàm `switchTab0Subtab` và gắn sự kiện click cho các nút tab con.
   - Cập nhật Stepper để chuyển đúng tab con.
3. **Bước 3: Kiểm thử tự động**:
   - Chạy `node tests/khbd-4steps-workflow-smoke.js`.

## Tiêu chí nghiệm thu
1. Tab 0 hiển thị thanh điều hướng 5 Tab con rõ ràng, khoa học.
2. Mỗi Tab con hiển thị độc lập, gọn gàng, giảm 80% chiều cao cuộn trang.
3. Mọi chức năng nạp file, đọc SGK/PPCT, đề xuất PPDH/NLS/AI và lưu dữ liệu hoạt động trơn tru 100%.
4. Bộ kiểm thử tự động pass 100%.
