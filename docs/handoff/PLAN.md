# PLAN: Tự động Nhận diện và Tick Chọn Mã NLS & AI từ PPCT Kèm Bảng Thông báo trong soankhbd.html

## Hiện trạng
1. **Chưa tự động đồng bộ mã NLS & AI từ nội dung PPCT**:
   - Trong `soankhbd.html`, khi người dùng nạp PPCT (dán ảnh/PDF qua Dropzone rồi bấm "Đọc PPCT", hoặc dán văn bản Markdown PPCT trực tiếp vào ô `#editorPpct`):
     + Hệ thống chỉ mới tự động trích xuất phạm vi tiết dạy (`lessonScopeSuggestion`) và thời lượng (`durationSuggestion`).
     + Nếu trong PPCT có ghi chú về AI, hệ thống chỉ hiển thị một thông báo toast nhắc nhở giáo viên tự điền tay (`showToast("PPCT có ghi chú tích hợp AI. Hãy tick Năng lực AI...")`).
     + Hệ thống hoàn toàn **bỏ qua các mã Năng lực số** (ví dụ `1.1.TC1a`, `5.3.TC2a`...) và **mã Khung năng lực AI** (ví dụ `6.A1.1`, `8.A1.1`...) đã được thiết kế sẵn trong bảng PPCT (đặc biệt là bảng Phụ lục 1 hoặc Phụ lục 3 xuất ra từ công cụ Xây dựng phụ lục).
2. **Thiếu phản hồi trực quan cho giáo viên**:
   - Giáo viên phải chuyển sang Bước 3 ("PPDH, Năng lực số & AI"), tự bật các nút toggle và tự tìm trong danh sách để tick lại từng mã.
   - Chưa có bảng thông báo (modal popup) xác nhận: *"Căn cứ theo PPCT, hệ thống đã chọn đúng mã Năng lực số và mã Khung AI tự động"*.

## Phạm vi
- Bổ sung bộ phân tích nhận diện mã NLS (chuẩn TT 02 / CV 3456) và mã AI (chuẩn QĐ 2422) từ văn bản PPCT trong `js/khbd-app.js`.
- Tự động bật toggle `toggleDigitalCompetency` và `toggleAiCompetency` khi phát hiện mã tương ứng.
- Tự động tick chọn các mã chuẩn đó trong `appState.teachingContext.standards` và hiển thị trên giao diện danh mục (`digitalStandardsPanel` & `aiStandardsPanel`).
- Xây dựng modal bảng thông báo popup trong `soankhbd.html` hiển thị danh sách các mã đã tự động chọn căn cứ theo PPCT.
- Kích hoạt cả khi bấm "Đọc PPCT" xong lẫn khi người dùng dán/chỉnh sửa văn bản PPCT vào ô `#editorPpct`.
- Bổ sung bài kiểm thử tự động (smoke test) xác minh quy trình nhận diện và tự tick mã chuẩn.

## Ngoài phạm vi
- Không thay đổi thuật toán sinh giáo án 4 hoạt động, không đổi cấu trúc prompt xuất Word KHBD.
- Không can thiệp vào các API backend.

## File dự kiến tác động
- `soankhbd.html` (thêm cấu trúc modal thông báo đồng bộ chuẩn PPCT)
- `js/khbd-app.js` (hàm nhận diện mã, đồng bộ state/checkbox và hiển thị modal)
- `tests/soankhbd-ppct-standards-smoke.js` (file test mới kiểm thử tính năng)

## Các bước thực hiện

### Bước 1: Xây dựng hàm bóc tách mã NLS & AI từ PPCT `extractStandardsFromPpctText`
Trong `js/khbd-app.js`:
1. Viết hàm `extractStandardsFromPpctText(text, topic, grade)`:
   - Nếu văn bản có cấu trúc bảng Markdown (`| STT | Bài học | ... | Mã NLS & AI |`), tìm đúng hàng của bài học đang chọn (`topic`). Nếu không thấy bài hoặc văn bản là đoạn trích riêng cho bài đó, quét trên toàn bộ văn bản.
   - **Nhận diện mã NLS**:
     + Regex quét mã theo chuẩn TT 02 / CV 3456: `\b(\d+\.\d+\.TC[12][a-z]?)\b` (hoặc bóc tách từ `[NLS: ...]` hay `mã - mô tả`).
     + Lọc theo dải lớp hiện hành: Lớp 6–7 nhận mã `TC1`, Lớp 8–9 nhận mã `TC2`.
     + Đối chiếu với danh mục `KHBD_STANDARDS.digital.entries` để lấy `entry` chuẩn.
   - **Nhận diện mã AI**:
     + Regex quét mã theo chuẩn QĐ 2422: `\b([6-9]\.A\d+\.\d+)\b` (hoặc bóc tách từ `[AI: ...]`).
     + Lọc theo đúng khối lớp hiện hành (ví dụ lớp 8 thì chỉ nhận mã `8.A...`).
     + Đối chiếu với danh mục `KHBD_STANDARDS.ai.entries` để lấy `entry` chuẩn.
   - Trả về đối tượng: `{ digital: [entry1, entry2], ai: [entry1], matchedLines: [...] }`.

### Bước 2: Xây dựng hàm tự động tick chọn chuẩn `applyPpctDetectedStandards`
Trong `js/khbd-app.js`:
1. Hàm `applyPpctDetectedStandards(detected, { showModal = true } = {})`:
   - Nếu có mã NLS (`detected.digital.length > 0`):
     + Bật toggle: `document.getElementById('toggleDigitalCompetency').checked = true`.
     + Cập nhật state: `appState.teachingContext.integrations.digital = true`.
     + Chuyển đổi các `entry` thành records bằng `standardToRecord('digital', entry, grade, true)`.
     + Áp dụng vào state: `applySuggestedStandardRecords('digital', catalog, records)`.
   - Nếu có mã AI (`detected.ai.length > 0`):
     + Bật toggle: `document.getElementById('toggleAiCompetency').checked = true`.
     + Cập nhật state: `appState.teachingContext.integrations.ai = true`.
     + Chuyển đổi các `entry` thành records bằng `standardToRecord('ai', entry, grade, true)`.
     + Áp dụng vào state: `applySuggestedStandardRecords('ai', catalog, records)`.
   - Cập nhật giao diện:
     + `renderStandardsCatalog()`
     + `renderSubjectIntegrations()`
     + `saveStateToLocalStorage()`
     + `updateWorkflowStepper()`
   - Nếu `showModal === true` và có ít nhất 1 mã NLS hoặc AI được nhận diện:
     + Gọi hàm hiển thị bảng thông báo popup `showPpctStandardsNotificationModal(detected)`.

### Bước 3: Thêm Modal thông báo tự động chọn mã chuẩn trong `soankhbd.html`
1. Thêm cấu trúc HTML cho Modal (sử dụng phong cách giao diện sẵn có của `soankhbd.html`):
   ```html
   <div id="modalPpctStandardsDetected" class="modal-overlay" style="display:none;" tabindex="-1">
     <div class="modal-card" style="max-width: 580px;">
       <div class="modal-header">
         <h3 style="display:flex;align-items:center;gap:0.5rem;margin:0;color:#0f766e;">
           <i data-lucide="check-circle-2"></i> Tự động chọn chuẩn từ PPCT
         </h3>
         <button type="button" class="btn-close-modal" onclick="closePpctStandardsModal()">✕</button>
       </div>
       <div class="modal-body" style="padding:1rem 0;">
         <p style="font-size:0.92rem;margin-bottom:0.75rem;">
           Căn cứ theo nội dung <b>Phân phối chương trình (PPCT)</b> đã nạp, hệ thống đã tự động nhận diện và tick chọn đúng các biểu hiện năng lực cho bài học:
         </p>
         <div id="ppctDetectedStandardsList" style="space-y:0.5rem;"></div>
         <p class="text-muted" style="font-size:0.82rem;margin-top:0.75rem;">
           Các mục này đã được đồng bộ vào <b>Bước 3 (PPDH, Năng lực số & AI)</b>. Bạn có thể xem lại hoặc tùy chỉnh bất kỳ lúc nào.
         </p>
       </div>
       <div class="modal-footer" style="display:flex;justify-content:flex-end;gap:0.5rem;">
         <button type="button" class="btn btn-outline-primary" onclick="goToStep3Pedagogy()">Xem tại Bước 3</button>
         <button type="button" class="btn btn-primary" onclick="closePpctStandardsModal()">Đã hiểu</button>
       </div>
     </div>
   </div>
   ```
2. Hàm `showPpctStandardsNotificationModal(detected)`:
   - Điền danh sách mã và nhãn kèm huy hiệu màu (Xanh dương cho NLS: `#0070C0`, Tím cho AI: `#7030A0`).
   - Kích hoạt hiển thị modal và làm mới icon Lucide.

### Bước 4: Tích hợp vào luồng đọc PPCT và ô nhập `#editorPpct`
1. Trong `handleGeneratePpctAnalysis()`:
   - Sau khi có `cleanedResult`, gọi `const detected = extractStandardsFromPpctText(cleanedResult, currentTopic, appState.selectedGrade)`.
   - Nếu `detected.digital.length || detected.ai.length`, gọi `applyPpctDetectedStandards(detected, { showModal: true })`.
2. Trong `setupEditorPreviewSync("editorPpct", ...)`:
   - Khi người dùng dán hoặc sửa text trong `#editorPpct`, sau khoảng debounce (500ms), tự động kiểm tra xem có mã NLS/AI mới xuất hiện hay không; nếu có thì kích hoạt nhận diện và hỏi/đồng bộ.

### Bước 5: Viết Smoke Test và Kiểm thử
1. Tạo tệp kiểm thử `tests/soankhbd-ppct-standards-smoke.js`:
   - Nạp đoạn văn bản PPCT có chứa mã NLS (`1.1.TC1a`, `5.3.TC1a`) và mã AI (`6.A1.1`).
   - Kiểm tra `extractStandardsFromPpctText` trích xuất chính xác danh sách mã.
   - Kiểm tra `applyPpctDetectedStandards` tự động bật checkbox NLS và AI, nạp đúng danh sách chuẩn vào state và render DOM.
   - Kiểm tra modal thông báo hiển thị đúng danh sách mã và nhãn chuẩn.
2. Chạy:
   - `node tests/soankhbd-ppct-standards-smoke.js`
   - `node tests/xaydungphuluc-smoke.js`
   - `node tests/canvas-xaydungphuluc-smoke.js`

## Rủi ro
- Khi người dùng dán toàn bộ bảng PPCT cả năm (nhiều bài học), hàm trích xuất cần lọc đúng dòng/hàng tương ứng với tên bài học hiện hành (`appState.selectedLesson` hoặc `appState.customTopic`) để không lấy nhầm mã của bài khác.
- Đảm bảo việc tick tự động không ghi đè nếu trước đó giáo viên đã chủ động tùy biến thủ công (có thông báo rõ ràng trong modal).

## Cách kiểm thử
1. `node tests/soankhbd-ppct-standards-smoke.js` -> PASS.
2. Mở `soankhbd.html` trên trình duyệt:
   - Dán một đoạn PPCT có cột `Mã NLS & AI (CV 3456 & QĐ 2422): [NLS: 1.1.TC1a - Khai thác học liệu số] [AI: 6.A1.1 - Sử dụng AI có kiểm chứng]`.
   - Bấm "Đọc PPCT" (hoặc dán vào ô nội dung PPCT).
   - Modal thông báo popup xuất hiện ngay trên màn hình: *"Căn cứ theo PPCT, hệ thống đã tự động nhận diện và tick chọn..."*.
   - Chuyển sang Tab 0 Subtab 3: Thấy công tắc NLS và AI đã được bật, các ô checkbox tương ứng với `1.1.TC1a` và `6.A1.1` đã được tick chọn sẵn.

## Tiêu chí nghiệm thu
- Tự động bóc tách chính xác mã NLS và mã AI từ nội dung PPCT (cả văn bản dán lẫn kết quả đọc từ file).
- Tự động bật toggle và tick chọn đúng các biểu hiện chuẩn tương ứng trong danh mục.
- Hiển thị bảng thông báo popup rõ ràng, chuyên nghiệp thông báo cho giáo viên về các mã đã được tự động chọn căn cứ theo PPCT.
- Toàn bộ smoke test tự động đều PASS.
