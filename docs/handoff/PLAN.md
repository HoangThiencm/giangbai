# PLAN: Tự động đảo Key cho tài khoản Free (xử lý 503 High Demand), tối ưu danh sách bản Flash và đưa nút Cài đặt ra vị trí nổi bật

## Hiện trạng
1. **Đặc thù tài khoản Free (Google AI Studio Free Tier)**:
   - Người dùng sử dụng API Key miễn phí (Free Tier).
   - Bản **Pro** (`gemini-2.5-pro`) ở gói Free bị giới hạn rất ngặt nghèo (chỉ 2 lượt gọi/phút - 2 RPM, hạn mức token rất thấp), không phù hợp thực tế và không nên đưa vào danh sách để tránh giáo viên chọn nhầm gây lỗi.
   - Bản **Flash** (`gemini-2.5-flash`) là phiên bản tối ưu nhất cho Free (15 RPM, 1.500 lượt/ngày, 1 triệu token/phút), cùng với các bản Flash thế hệ mới như `gemini-3.7-flash` và `gemini-3-flash-preview`.
2. **Xử lý lỗi Quota (429) và Quá tải (503 High Demand) bằng Đảo Key**:
   - Khi tài khoản Free gặp lỗi 503 High Demand hoặc 429 Rate Limit: **Chỉ thực hiện đảo Key** sang API Key tiếp theo trong danh sách các key Free đã cấu hình, giữ nguyên model Flash đang chọn.
3. **Vị trí nút Cài đặt Model AI**:
   - Đưa nút ra **Top Navbar** (trên cùng cạnh nút "Khai báo tổ") và **Thanh công cụ TKB** dưới bảng để bấm đổi model hoặc kiểm tra model đang dùng bất cứ lúc nào.

---

## Phạm vi
- File `api/khbd_gemini.php`:
  + Cập nhật `khbd_gemini_should_rotate`: bổ sung mã `503` và các từ khóa `high demand`, `overloaded`, `temporarily unavailable` để khi gặp lỗi này, hệ thống **tự động đảo sang Key kế tiếp** trong danh sách key Free.
- File `phancongtochuyenmon.html`:
  + Cập nhật Modal `#gemini-model-modal`:
    * Xóa bỏ cả `gemini-2.5-pro` và `gemini-1.5-flash`.
    * Chỉ giữ các bản **Flash** tối ưu cho tài khoản Free:
      - `gemini-2.5-flash` (Mặc định - Ổn định và tối ưu nhất cho tài khoản Free).
      - `gemini-3.7-flash` (Bản Flash mới).
      - `gemini-3-flash-preview` (Bản Flash thử nghiệm).
      - Ô nhập model tùy chỉnh (nếu cần tự gõ).
  + Đưa nút mở Modal ra 2 vị trí nổi bật:
    1. **Top Navbar** (dòng ~1785 cạnh nút "Khai báo tổ"):
       `<button class="btn-toolbar btn-config" type="button" onclick="openGeminiModelModal()"><i class="fas fa-robot text-indigo-400"></i> AI: <span id="top-nav-ai-model-label">2.5 Flash</span></button>`.
    2. **Thanh công cụ TKB (`.tt-toolbar`)** (dòng ~1980):
       `<button type="button" class="btn-small" onclick="openGeminiModelModal()"><i class="fas fa-robot text-indigo-600"></i> Model: <span id="tt-toolbar-model-label">2.5 Flash</span></button>`.
  + Hàm `updateAiModelLabels(model)`: tự động cập nhật chữ hiển thị ở cả 3 vị trí.
- File `tests/timetable-render-smoke.js`:
  + Cập nhật kiểm thử: không còn `gemini-2.5-pro`, không còn `gemini-1.5-flash`; có nút trên Top Navbar và Toolbar TKB.

---

## Ngoài phạm vi
- Không can thiệp sang các mô-đun khác.
- Không tự ý chuyển model khi lỗi (chỉ xoay vòng key Free).

---

## File dự kiến tác động
- `api/khbd_gemini.php`
- `phancongtochuyenmon.html`
- `tests/timetable-render-smoke.js`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/.lock`

---

## Các bước thực hiện chi tiết cho Coder
1. **Bước 1: Mở khóa handoff**:
   - Xóa `docs/handoff/.lock` trước khi sửa source code.

2. **Bước 2: Cập nhật `api/khbd_gemini.php` tự động đảo Key khi 503 High Demand**:
   - Trong `khbd_gemini_should_rotate(int $status, string $error)`:
     ```php
     function khbd_gemini_should_rotate(int $status, string $error): bool
     {
         if (in_array($status, [403, 429, 503], true)) return true;
         $message = strtolower($error);
         return str_contains($message, 'quota')
             || str_contains($message, 'high demand')
             || str_contains($message, 'overloaded')
             || str_contains($message, 'unavailable')
             || str_contains($message, 'resource exhausted')
             || str_contains($message, 'rate limit')
             || str_contains($message, 'too many requests')
             || str_contains($message, 'operation timed out')
             || str_contains($message, 'timed out')
             || str_contains($message, 'could not connect');
     }
     ```

3. **Bước 3: Tối ưu danh sách Flash cho Free và đưa nút ra vị trí nổi bật trong `phancongtochuyenmon.html`**:
   - Trong `#gemini-model-modal`:
     Xóa bỏ các option Pro và 1.5. Danh sách dropdown chỉ gồm:
     ```html
     <option value="gemini-2.5-flash">Gemini 2.5 Flash (Khuyên dùng cho Free: Nhanh, nhẹ, ổn định)</option>
     <option value="gemini-3.7-flash">Gemini 3.7 Flash</option>
     <option value="gemini-3-flash-preview">Gemini 3 Flash Preview</option>
     <option value="custom">-- Model tùy chỉnh khác --</option>
     ```
   - Thêm nút Top Navbar (dòng ~1785 cạnh nút "Khai báo tổ"):
     ```html
     <button class="btn-toolbar btn-config" type="button" onclick="openGeminiModelModal()" title="Cài đặt Module Gemini AI">
         <i class="fas fa-robot text-indigo-400"></i> AI: <span id="top-nav-ai-model-label">2.5 Flash</span>
     </button>
     ```
   - Thêm nút tại `.tt-toolbar` (dòng ~1980):
     ```html
     <button type="button" class="btn-small" onclick="openGeminiModelModal()" title="Cài đặt Model Gemini AI">
         <i class="fas fa-robot text-indigo-600"></i> Model: <span id="tt-toolbar-model-label">2.5 Flash</span>
     </button>
     ```
   - Cập nhật hàm `updateAiModelLabels(model)` để đồng bộ nhãn cả 3 nơi:
     `#top-nav-ai-model-label`, `#tt-toolbar-model-label`, `#tt-active-model-label`.

4. **Bước 4: Kiểm thử và cập nhật `tests/timetable-render-smoke.js`**:
   - Chạy `node tests/timetable-render-smoke.js` -> 100% PASS.

5. **Bước 5: Ghi nhật ký vào `docs/handoff/IMPLEMENT.md` và tạo lại `docs/handoff/.lock` nội dung `LOCK`**.

---

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - Chạy `node tests/timetable-render-smoke.js` -> 100% PASS.
2. **Kiểm thử thủ công**:
   - Mở `phancongtochuyenmon.html`, kiểm tra nút trên Top Navbar và Toolbar TKB.
   - Bấm vào mở modal, xác nhận chỉ gồm các bản Flash phù hợp cho tài khoản Free (`2.5 Flash`, `3.7 Flash`, `3 Flash Preview` và tùy chỉnh), không còn bản Pro hay 1.5.
   - Xác nhận cơ chế tự động đảo sang key Free tiếp theo khi gặp 503 hoặc 429.
