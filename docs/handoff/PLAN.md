# PLAN: Đồng Bộ 2 Phiên Bản Soạn (Chi Tiết / Rút Gọn) & Nút 1-Click Sang Trang `soankhbd.html`

## User Review Required
> [!IMPORTANT]
> - **Yêu cầu người dùng**: Đồng bộ tính năng **2 phiên bản soạn giáo án** (Soạn chi tiết 8–10 trang / Soạn rút gọn 4–6 trang) và nút **⚡ TẠO TOÀN BỘ GIÁO ÁN (1-CLICK)** từ `canvas_soankhbd.html` sang trang chuẩn `soankhbd.html`.
> - **Lợi ích**:
>   1. Cho phép giáo viên chọn giữa bản soạn chuẩn đầy đủ (8-10 trang) và bản tinh gọn (4-6 trang).
>   2. Vẫn giữ nguyên khả năng tự do chọn Model AI (Gemini 2.5 Flash / 2.0 Flash) và tự cắm API Key cá nhân của `soankhbd.html` để chạy tốc độ cao, không bị nghẽn giờ cao điểm.

---

## I. Thiết Kế Kỹ Thuật Chi Tiết

### Module 1: Cập Nhật Giao Diện `soankhbd.html`
1. **Nút Tạo 1-Click trên Header Actions**:
   - Thêm vào `.header-actions` (trước nút `btnCancelGeneration`):
     ```html
     <button id="btn1ClickGenerate" class="btn btn-special" title="Tự động tạo lần lượt toàn bộ giáo án từ đầu đến cuối">
       <i data-lucide="zap"></i> ⚡ TẠO TOÀN BỘ GIÁO ÁN (1-CLICK)
     </button>
     ```
2. **Bộ chọn Chế độ soạn trong Toolbar Grid**:
   - Thêm vào `.toolbar-grid` (giữa Môn học và Danh mục bài học):
     ```html
     <div class="tool-group">
       <label for="selectGenerationMode">Chế độ soạn:</label>
       <select id="selectGenerationMode" aria-label="Chế độ soạn giáo án">
         <option value="detailed" selected>📋 Soạn chi tiết (8–10 trang)</option>
         <option value="compact">⚡ Soạn rút gọn (4–6 trang)</option>
       </select>
     </div>
     ```

### Module 2: Xử Lý Logic Trong `js/khbd-app.js`
1. **Quản lý State `generationMode`**:
   - Khởi tạo: đọc từ `localStorage.getItem('khbd_generation_mode') || 'detailed'`.
   - Đồng bộ trạng thái vào `#selectGenerationMode`.
   - Lắng nghe sự kiện `change` trên `#selectGenerationMode`: lưu vào `localStorage` và cập nhật `appState.generationMode`.
2. **Tích hợp vào Ngữ Cảnh Prompt (`getGenerationPromptContext`)**:
   - Đảm bảo hàm chuẩn bị ngữ cảnh prompt luôn truyền `generationMode: appState.generationMode` vào `getPromptTemplate(...)` (trong `js/khbd-prompts.js` đã có sẵn logic xử lý `context.generationMode === 'compact'`).
3. **Logic Thực Thi 1-Click (`btn1ClickGenerate`)**:
   - Kiểm tra bài học đã chọn/nhập (nếu chưa có thì thông báo và focus vào ô chọn bài).
   - Hiển thị hộp thoại xác nhận rõ ràng:
     - Chế độ **Soạn rút gọn (4–6 trang)**: Chạy 6 bước cốt lõi, bỏ mục III.E (Hồ sơ học tập) và hình minh họa SGK.
     - Chế độ **Soạn chi tiết (8–10 trang)**: Chạy đầy đủ 8 bước.
   - Quản lý trạng thái nút bấm: Disable `btn1ClickGenerate`, Enable `btnCancelGeneration`, hiển thị thanh tiến trình floating progress bar.
   - Tuần tự thực thi qua `executeStep`:
     1. I. Mục tiêu bài học (CV 5512 & NLS/AI)
     2. II. Thiết bị dạy học và học liệu
     3. III.A Hoạt động Khởi động
     4. III.B Hoạt động Hình thành kiến thức
     5. III.C Hoạt động Luyện tập
     6. III.D Hoạt động Vận dụng & Tự học
     7. (Nếu detailed): III.E Hồ sơ học tập & F. Hình minh họa SGK
     8. Tự động tổng hợp và điều hướng sang Tab Toàn bộ Giáo án (.DOCX).
   - Hỗ trợ hủy tiến trình an toàn khi bấm `btnCancelGeneration` (AbortController).

### Module 3: Kiểm Thử Tự Động (`tests/soankhbd-generation-mode-smoke.js`)
- Tạo bộ kiểm thử mới kiểm tra:
  1. `soankhbd.html` có chứa `#btn1ClickGenerate` và `#selectGenerationMode`.
  2. Giá trị mặc định là `detailed`, có tùy chọn `compact`.
  3. `js/khbd-app.js` khởi tạo đúng `generationMode` và xử lý sự kiện click của `#btn1ClickGenerate`.
  4. Prompt context trong `js/khbd-prompts.js` trả về nội dung rút gọn khi `generationMode: 'compact'`.

---

## II. Danh Sách File Cần Chỉnh Sửa

| Tệp tin | Vị trí | Mục đích thay đổi |
| :--- | :--- | :--- |
| `soankhbd.html` | Dòng ~116 & ~145 | Thêm nút `#btn1ClickGenerate` và dropdown `#selectGenerationMode` |
| `js/khbd-app.js` | Khởi tạo & Event Listeners | Khởi tạo `generationMode`, xử lý lưu/đổi chế độ, hàm tạo 1-Click |
| `tests/soankhbd-generation-mode-smoke.js` | Tệp mới | Smoke test kiểm tra 2 phiên bản và 1-Click trên `soankhbd.html` |

---

## III. Kế Hoạch Kiểm Thử (Verification Plan)

### Kiểm thử tự động
- `node tests/soankhbd-generation-mode-smoke.js` — PASS.
- `node tests/canvas-soankhbd-smoke.js` — PASS.
- `node tests/baogiang-teacher-month-smoke.js` — PASS.
