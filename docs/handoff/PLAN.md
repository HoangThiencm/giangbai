# PLAN: Bổ sung Modal Cài đặt / Chọn Module Gemini cho nhận diện Thời khóa biểu và AI trong Quản lý tổ chuyên môn

## Hiện trạng
1. **Triệu chứng & Thực tế**:
   - Hiện tại trong `phancongtochuyenmon.html`, hàm `scanTimetableWithAI` (dòng ~6633) đang cố định (hardcode) model AI:
     `body: JSON.stringify({ model: 'gemini-2.5-flash', payload, timeout: 90 })`
   - Người dùng không có cách nào lựa chọn chuyển đổi sang các model khác (như `gemini-2.5-pro` khi ảnh TKB mờ hoặc phức tạp, `gemini-1.5-flash` khi model 2.5 bị nghẽn quota, hoặc `gemini-3.7-flash`, `gemini-3-flash-preview`...).
   - Người dùng cũng không thể quan sát được hiện tại hệ thống đang sử dụng model nào để xử lý.

2. **Nhu cầu**:
   - Bổ sung Modal Cài đặt / Chọn Module Gemini (hoặc dropdown chọn nhanh model) trực tiếp tại giao diện tab Thời khóa biểu GV (`#view-timetable`) và trong cài đặt chung của hệ thống.
   - Cho phép người dùng linh hoạt đổi model ngay trước khi quét ảnh TKB để tránh lỗi Quota hoặc tăng độ chính xác theo nhu cầu.

---

## Phạm vi
- File `phancongtochuyenmon.html`:
  + Bổ sung Modal Cài đặt Model Gemini (`#gemini-model-modal`) với danh sách các model phổ biến:
    * `gemini-2.5-flash` (Khuyên dùng: Nhanh, nhẹ, OCR thị giác tốt, ít tốn quota).
    * `gemini-2.5-pro` (Thông minh cao, suy luận sâu với bảng mờ/phức tạp).
    * `gemini-1.5-flash` (Bản ổn định dự phòng khi 2.5 quá tải).
    * `gemini-3.7-flash` (Model mới nhất).
    * `gemini-3-flash-preview` (Bản thử nghiệm).
    * Ô nhập model tùy chỉnh (Custom Model Name).
  + Bổ sung nút mở Modal / Dropdown chọn nhanh Model cạnh nút "Khung tiết" và "AI nhận diện TKB" tại thẻ nhập TKB (`#tt-import-details`):
    `<button type="button" class="btn-small" onclick="openGeminiModelModal()"><i class="fas fa-robot"></i> <span id="tt-active-model-label">Gemini 2.5 Flash</span></button>`
  + Quản lý lưu trữ model:
    * Hàm `getTimetableGeminiModel()`: ưu tiên đọc từ `localStorage.getItem('phancong_gemini_model')` hoặc `localStorage.getItem('gemini_model')` hoặc `state.info.gemini_model`, fallback về `'gemini-2.5-flash'`.
    * Hàm `saveTimetableGeminiModel(model)`: lưu vào `localStorage` và cập nhật nhãn hiển thị trên giao diện.
  + Cập nhật hàm `scanTimetableWithAI()`: sử dụng `getTimetableGeminiModel()` khi gửi payload tới `api/khbd_gemini.php`.
- File `tests/timetable-render-smoke.js`:
  + Thêm assertion kiểm tra sự hiện diện của modal/dropdown chọn model Gemini, hàm `getTimetableGeminiModel` và việc dùng model động trong `scanTimetableWithAI`.

---

## Ngoài phạm vi
- Không can thiệp sang backend `api/khbd_gemini.php` (backend này đã hỗ trợ regex chấp nhận mọi model Gemini hợp lệ dạng `gemini-[a-z0-9._-]+`).
- Không làm thay đổi cấu trúc dữ liệu lưu trữ TKB trong cơ sở dữ liệu.

---

## File dự kiến tác động
- `phancongtochuyenmon.html`
- `tests/timetable-render-smoke.js`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/.lock`

---

## Các bước thực hiện chi tiết cho Coder
1. **Bước 1: Mở khóa handoff**:
   - Xóa `docs/handoff/.lock` trước khi sửa source code.

2. **Bước 2: Xây dựng HTML Modal Cài đặt Model Gemini trong `phancongtochuyenmon.html`**:
   - Bổ sung cấu trúc modal `#gemini-model-modal`:
     ```html
     <div class="modal-overlay" id="gemini-model-modal">
         <div class="modal-card" style="max-width: 480px;">
             <div class="modal-header">
                 <h2><i class="fas fa-robot text-indigo-600"></i> Cài đặt Model Gemini AI</h2>
                 <button class="modal-close" onclick="closeGeminiModelModal()">&times;</button>
             </div>
             <div class="modal-body">
                 <p style="margin: 0 0 12px 0; font-size: 0.82rem; color: #64748b;">
                     Chọn module AI dùng để nhận diện Thời khóa biểu và hỗ trợ phân công:
                 </p>
                 <div class="form-group" style="margin-bottom: 12px;">
                     <label style="font-weight: 700; font-size: 0.82rem; display: block; margin-bottom: 6px;">Chọn phiên bản AI:</label>
                     <select id="cfg-gemini-model-select" class="form-control" onchange="onGeminiModelSelectChange(this.value)">
                         <option value="gemini-2.5-flash">Gemini 2.5 Flash (Khuyên dùng: Nhanh, nhẹ, tiết kiệm quota)</option>
                         <option value="gemini-2.5-pro">Gemini 2.5 Pro (Suy luận sâu, thông minh cao, ảnh mờ/khó)</option>
                         <option value="gemini-1.5-flash">Gemini 1.5 Flash (Bản ổn định dự phòng)</option>
                         <option value="gemini-3.7-flash">Gemini 3.7 Flash</option>
                         <option value="gemini-3-flash-preview">Gemini 3 Flash Preview</option>
                         <option value="custom">-- Model tùy chỉnh khác --</option>
                     </select>
                 </div>
                 <div class="form-group" id="cfg-gemini-model-custom-wrap" style="display: none; margin-bottom: 12px;">
                     <label style="font-weight: 700; font-size: 0.82rem; display: block; margin-bottom: 6px;">Tên model tùy chỉnh:</label>
                     <input type="text" class="form-control" id="cfg-gemini-model-custom" placeholder="VD: gemini-2.5-flash-lite">
                 </div>
                 <div style="font-size: 0.78rem; color: #475569; background: #f8fafc; padding: 10px; border-radius: 8px; border: 1px solid #e2e8f0; line-height: 1.4;">
                     <i class="fas fa-lightbulb text-amber-500"></i> <b>Mẹo:</b> Nếu <code>2.5-flash</code> báo lỗi hết Quota (429), bạn có thể tạm chuyển sang <code>1.5-flash</code> hoặc <code>2.5-pro</code>, hoặc bổ sung thêm 2-3 API key trong phần Cài đặt tài khoản.
                 </div>
             </div>
             <div class="modal-footer">
                 <button class="btn-small" onclick="closeGeminiModelModal()">Đóng</button>
                 <button class="btn-small btn-small-primary" onclick="saveGeminiModelConfig()"><i class="fas fa-check"></i> Lưu cài đặt</button>
             </div>
         </div>
     </div>
     ```

3. **Bước 3: Bổ sung nút bấm mở modal tại thẻ Nhập ảnh TKB (`#tt-import-details`)**:
   - Tại dòng ~1961 trong `phancongtochuyenmon.html`, đặt cạnh nút "Khung tiết":
     ```html
     <button type="button" class="btn-small" onclick="openGeminiModelModal()" title="Cài đặt module Gemini AI">
         <i class="fas fa-robot text-indigo-600"></i> <span id="tt-active-model-label">2.5 Flash</span>
     </button>
     ```

4. **Bước 4: Viết các hàm điều khiển JS trong `phancongtochuyenmon.html`**:
   - `getTimetableGeminiModel()`:
     Lấy từ `localStorage.getItem('phancong_gemini_model')` || `localStorage.getItem('gemini_model')` || `'gemini-2.5-flash'`.
   - `formatGeminiModelShortLabel(model)`:
     Trả về nhãn ngắn gọn, VD: `'2.5 Flash'`, `'2.5 Pro'`, `'1.5 Flash'`...
   - `openGeminiModelModal()`:
     Đọc model hiện tại, gán giá trị vào select và input custom, mở modal `#gemini-model-modal`.
   - `closeGeminiModelModal()`:
     Đóng modal `#gemini-model-modal`.
   - `onGeminiModelSelectChange(val)`:
     Ẩn/hiện trường input `cfg-gemini-model-custom-wrap`.
   - `saveGeminiModelConfig()`:
     Lấy giá trị từ select (hoặc custom input nếu chọn custom), lưu vào `localStorage.setItem('phancong_gemini_model', model)` và `localStorage.setItem('gemini_model', model)`, cập nhật `tt-active-model-label`, đóng modal và thông báo `showToast('Đã lưu model AI: ' + model, 'success')`.
   - Cập nhật `scanTimetableWithAI()`:
     Thay vì `model: 'gemini-2.5-flash'`, sử dụng:
     ```javascript
     const activeModel = getTimetableGeminiModel();
     // body: JSON.stringify({ model: activeModel, payload, timeout: 90 })
     ```
   - Khởi tạo nhãn ban đầu khi trang load trong `renderTimetableView()` hoặc `initTimetableWorkspace()`.

5. **Bước 5: Cập nhật kiểm thử tự động trong `tests/timetable-render-smoke.js`**:
   - Kiểm tra `phancongtochuyenmon.html` có chứa `gemini-model-modal`, `openGeminiModelModal`, `getTimetableGeminiModel`.
   - Kiểm tra `scanTimetableWithAI` không còn hardcode chuỗi `model: 'gemini-2.5-flash'` mà sử dụng hàm/biến động `getTimetableGeminiModel()`.
   - Chạy `node tests/timetable-render-smoke.js` -> 100% PASS.

6. **Bước 6: Ghi nhật ký vào `docs/handoff/IMPLEMENT.md` và tạo lại `docs/handoff/.lock` nội dung `LOCK`**.

---

## Rủi ro và Biện pháp dự phòng
- *Rủi ro*: Người dùng nhập sai tên model tùy chỉnh khiến Gemini báo lỗi HTTP 404 / 422.
  *Biện pháp*: Backend `api/khbd_gemini.php` đã có regex kiểm tra hợp lệ; trên frontend có danh sách dropdown các model chuẩn sẵn để người dùng chọn nhanh không sợ gõ nhầm.

---

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - Chạy `node tests/timetable-render-smoke.js` -> 100% PASS.
2. **Kiểm thử thủ công trên trình duyệt**:
   - Mở `phancongtochuyenmon.html`, chuyển sang tab **2. Thời khoá biểu GV**.
   - Mở thẻ **Nhập ảnh Thời khóa biểu**, xác nhận có nút hiển thị model AI (mặc định "2.5 Flash").
   - Bấm vào nút model -> Modal **Cài đặt Model Gemini AI** xuất hiện.
   - Thử đổi sang `gemini-2.5-pro` hoặc `gemini-1.5-flash` và bấm Lưu. Xác nhận nhãn nút trên giao diện đổi sang model tương ứng.
   - Bấm **AI nhận diện TKB**, mở DevTools tab Network kiểm tra payload gửi lên `api/khbd_gemini.php` có trường `model` đúng với model vừa chọn.
