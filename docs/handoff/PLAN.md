# Kế hoạch Triển khai: Chuẩn Hóa In Đậm & In Nghiêng Cho Năng Lực Số (NLS) và Năng Lực AI

## 1. Yêu cầu & Căn cứ Chuyên môn

- **Yêu cầu từ Chuyên môn / Thanh tra GD:**
  Tại tất cả các vị trí tích hợp **Khung Năng lực Số (NLS)** (Thông tư 02/2025/TT-BGDĐT, CV 3456/BGDĐT-GDPT) và **Khung Năng lực Trí tuệ Nhân tạo (AI)** (QĐ 2422/QĐ-BGDĐT), văn bản giáo án **bắt buộc phải được IN ĐẬM VÀ IN NGHIÊNG** (`bold` + `italic`) để làm nổi bật minh chứng tích hợp khi thẩm định và thanh tra chuyên môn.
- **Phạm vi áp dụng trong Kế hoạch bài dạy (KHBD):**
  1. **Mục I. MỤC TIÊU:**
     - Tiêu đề mục: `***c) Năng lực số***` và `***d) Năng lực AI***` (hoặc Heading 3 có thuộc tính in nghiêng).
     - Các dòng chỉ tiêu / mã năng lực con: Cả mã năng lực và nội dung chỉ báo phải được in đậm & in nghiêng (ví dụ: `- ***1.1.TC1a:*** *Học sinh sử dụng phần mềm GeoGebra để vẽ hình và kiểm chứng kết quả.*` hoặc `- ***[NLS: 1.1.TC1a]***: *...*`).
  2. **Mục III. TIẾN TRÌNH DẠY HỌC (Các Hoạt động A, B, C, D, E):**
     - Các thẻ Marker tích hợp: `***[NLS: {Miền/Mã} - {Tên phần mềm}]***` (hoặc `***[NLS]***`), `***[AI: {Mã} - Nội dung tích hợp]***` (hoặc `***[AI]***`) phải vừa in đậm, vừa in nghiêng.
     - Khi xuất file Word (.docx): Marker NLS / AI nhận `bold: true` VÀ `italics: true` (kèm màu và shading nhận diện).
     - Trên giao diện Web: Badge `.khbd-badge-nls` và `.khbd-badge-ai` hiển thị với `font-weight: 700; font-style: italic;`.
  3. **Bộ Sinh Prompt & Chuẩn Hóa Tự Động (Gemini):**
     - Prompt chỉ đạo AI sinh đúng cú pháp Markdown `***...***` cho các thẻ NLS / AI và mục tiêu NLS / AI.
     - Parser Markdown sang Docx hỗ trợ đầy đủ cú pháp 3 sao `***...***` (chuyển thành `TextRun` có `bold: true` và `italics: true`).
     - Bộ lọc/dọn dẹp tag (`stripDisabledActivityIntegrations`, `ensureObjectivesDigitalCodes`) tương thích trơn tru với định dạng 3 sao.

---

## 2. Danh sách Tệp Cần Chỉnh Sửa

1. `js/khbd-docx.js`:
   - Bổ sung `italics: true` cho NLS và AI trong `markerRunColor()`.
   - Chuyển tiếp thuộc tính `italics` trong `pushMarkerWithMath()`.
   - Mở rộng regex và bộ bóc tách inline Markdown trong `parseInlineTextToRuns()` để hỗ trợ khối 3 sao `***...***` và 3 gạch dưới `___...___`.
2. `css/khbd-styles.css`:
   - Bổ sung `font-style: italic;` cho `.khbd-badge-nls`, `.khbd-badge-ai` (hoặc `.khbd-badge`).
   - Cập nhật `.preview-rendered .khbd-nls` và `.preview-rendered .khbd-ai` để đảm bảo văn bản tích hợp thể hiện rõ nét phong cách in đậm / in nghiêng.
3. `js/khbd-prompts.js`:
   - Nâng cấp marker mẫu trong hợp đồng đầu ra và các prompt pha A, B, C, D sang dạng `***[NLS: ...]***` và `***[AI: ...]***`.
   - Cập nhật `digitalObjectivesSection` và `aiObjectivesSection` trong `getPromptTemplate()` sang định dạng `***[Mã]***: *[Mô tả]*`.
   - Bổ sung quy tắc: "BẮT BUỘC: Các vị trí tích hợp NLS và AI phải được in đậm và in nghiêng (dùng cú pháp Markdown ***...***)".
4. `js/khbd-app.js`:
   - Cập nhật hàm `insertObjectivesMissingStandards()` để xuất bullet lines NLS/AI dạng `- ***${code}:*** *${label}*`.
   - Nâng cấp regex làm sạch và kiểm định trong `stripDisabledActivityIntegrations()`, `activityOutputProblem()` hỗ trợ cú pháp `***`.
5. `tests/khbd-integrations-smoke.js` & `tests/khbd-dynamic-integrations-smoke.js`:
   - Cập nhật các assertion kiểm tra `markerRunColor` cho NLS và AI khớp với `{ ..., bold: true, italics: true }`.
6. `tests/khbd-nls-ai-bold-italic-smoke.js` (Tạo mới):
   - Kiểm tra toàn diện quy trình in đậm & in nghiêng: parse markdown `***`, thuộc tính Docx TextRun, CSS badge, và prompt contract.

---

## 3. Chi tiết Kỹ thuật Cần Triển khai

### A. Module Xuất Word: `js/khbd-docx.js`
1. Tại `markerRunColor(text)`:
   ```javascript
   if (/^\[?NLS(?::[^\]\n]+)?\]?$/i.test(t)) return { color: "0369A1", shading: "E0F2FE", bold: true, italics: true };
   if (/^\[?AI(?::[^\]\n]+)?\]?$/i.test(t)) return { color: "6D28D9", shading: "F3E8FF", bold: true, italics: true };
   ```
2. Tại `pushMarkerWithMath(token, markerInfo, baseStyles)`:
   ```javascript
   runs.push(this.coloredTextRun(token, {
     bold: markerInfo ? markerInfo.bold : baseStyles.bold,
     italics: markerInfo ? (markerInfo.italics ?? baseStyles.italics) : baseStyles.italics,
     color: markerInfo ? markerInfo.color : color,
     shading: markerInfo ? markerInfo.shading : undefined
   }));
   ```
3. Tại `parseInlineTextToRuns(text, color, styles)`:
   Cập nhật `regex` inline để bắt `\*\*\*[\s\S]+?\*\*\*` trước `\*\*` và `\*`:
   ```javascript
   const regex = /(\$\$[\s\S]+?\$\$|\\\[[\s\S]+?\\\]|\\\([\s\S]+?\\\)|(?<!\$)\$(?!\$)(?:\\.|[^$\n])+?\$(?!\$)|\*\*\*[\s\S]+?\*\*\*|\*\*[\s\S]+?\*\*|(?<![\w\\])___(?!\s|_)[^_\n]+?(?<!\s)___(?!\w)|(?<![\w\\])__(?!\s|_)[^_\n]+?(?<!\s)__(?!\w)|(?<!\*)\*(?!\*)[^*\n]+?\*(?!\*)|(?<![\w\\])_(?!\s|_)[^_\n]+?(?<!\s)_(?![\w_])|`[^`]+?`|\[(?:NLS|AI|GDQPAN|HCM|QCN|CLIL|GDTC|TAICHINH|STEM|TN-AO|TNAO|MT-NLX|GDĐP-MT|GDDP-MT|BĐKH-SDG|BDKH-SDG|Di sản ĐP|Di san DP|Speech AI|Bản sắc VN|Ban sac VN|CDTG)(?::\s*[^\]\r\n]+)?\])/gi;
   ```
   Xử lý token bắt đầu bằng `***` hoặc `___`:
   ```javascript
   } else if ((token.startsWith("***") && token.endsWith("***")) || (token.startsWith("___") && token.endsWith("___"))) {
     const biText = token.substring(3, token.length - 3);
     const markerInfo = this.markerRunColor(biText);
     if (markerInfo) {
       pushMarkerWithMath(biText, markerInfo, { ...styles, bold: true, italics: true });
     } else {
       runs.push(...this.parseInlineTextToRuns(biText, color, { ...styles, bold: true, italics: true }));
     }
   }
   ```

### B. CSS Giao diện Web: `css/khbd-styles.css`
1. Bổ sung `font-style: italic;` cho các thẻ badge NLS và AI:
   ```css
   .khbd-badge-nls {
     background-color: #e0f2fe;
     color: #0369a1;
     border: 1px solid #7dd3fc;
     font-style: italic;
   }

   .khbd-badge-ai {
     background-color: #f3e8ff;
     color: #6d28d9;
     border: 1px solid #c084fc;
     font-style: italic;
   }
   ```
2. Đảm bảo phần hiển thị xem trước của các heading và nội dung NLS/AI:
   ```css
   .preview-rendered .khbd-nls,
   .preview-rendered .khbd-nls * {
     color: #0369a1;
   }
   .preview-rendered .khbd-ai,
   .preview-rendered .khbd-ai * {
     color: #6d28d9;
   }
   ```

### C. Prompts & Xử lý Logic: `js/khbd-prompts.js` & `js/khbd-app.js`
1. Trong `js/khbd-prompts.js`:
   - Thay toàn bộ các hướng dẫn marker `**[NLS: ...]**` thành `***[NLS: ...]***` và `**[AI: ...]**` thành `***[AI: ...]***`.
   - Trong `getPromptTemplate()`:
     ```javascript
     const digitalObjectivesSection = context.digitalCompetencyEnabled
       ? `### c) Năng lực số\n- ***[Mã NLS đã chọn, ví dụ 1.1.TC1a]:*** *[Mô tả nhiệm vụ số gắn với bài]*`
       : '';
     const aiObjectivesSection = context.aiCompetencyEnabled
       ? `### d) Năng lực AI\n- ***[Mã AI đã chọn]:*** *[Mô tả nhiệm vụ AI gắn với bài]*`
       : '';
     ```
2. Trong `js/khbd-app.js`:
   - Tại `insertObjectivesMissingStandards()`:
     ```javascript
     bulletLines: digital.map(row => `- ***${row.item.officialCode}:*** *${row.item.officialLabel}*`)
     ```
     ```javascript
     bulletLines: ai.map(row => `- ***${row.item.officialCode}:*** *${row.item.officialLabel}*`)
     ```
   - Tại `stripDisabledActivityIntegrations()`:
     Cập nhật regex loại bỏ marker khi tắt để bắt cả `\*{1,3}`:
     ```javascript
     text = text.replace(/\*{1,3}\[?NLS(?::[^\]\n]+)?\]?\*{1,3}/gi, "")
                .replace(/\[NLS(?::[^\]\n]+)?\]/gi, "");
     ```
     (Tương tự với AI).

---

## 4. Kiểm thử & Tiêu chí Nghiệm thu (Verification Plan)

1. **Smoke Tests Tự Động:**
   - Chạy `node tests/khbd-integrations-smoke.js`: PASS.
   - Chạy `node tests/khbd-dynamic-integrations-smoke.js`: PASS.
   - Chạy `node tests/khbd-docx-format-smoke.js`: PASS.
   - Tạo và chạy `node tests/khbd-nls-ai-bold-italic-smoke.js`: PASS 100%.
2. **Kiểm tra File Word (.docx):**
   - Khi gọi `generator.parseInlineTextToRuns("***[NLS: 1.1.TC1a - GeoGebra]***")`:
     Run sinh ra phải có `w:b` (bold = true) VÀ `w:i` (italics = true), mã màu `0369A1`, shading `E0F2FE`.
   - Khi gọi `generator.parseInlineTextToRuns("***[AI: 8.A1.1 - Kiểm chứng phản hồi AI]***")`:
     Run sinh ra phải có `w:b` (bold = true) VÀ `w:i` (italics = true), mã màu `6D28D9`, shading `F3E8FF`.
3. **Kiểm tra Giao diện Web:**
   - Badge NLS và AI trên giao diện preview có cả `font-weight: 700` và `font-style: italic`.
   - Mục I.2.c và I.2.d hiển thị đúng quy cách in đậm & in nghiêng theo yêu cầu chuyên môn.
