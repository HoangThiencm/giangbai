# PLAN: Khắc Phục Triệt Để Lỗi Tự Động Chèn Khung AI Vào Hoạt Động Khi Giáo Viên Không Bật Tích Hợp (soankhbd.html)

## Hiện trạng & Nguyên nhân gốc rễ (Root Cause Analysis)
Khi giáo viên **không kích chọn** ô `✨ Năng lực AI` (`toggleAiCompetency`, tương đương `appState.teachingContext.integrations.ai === false`), AI vẫn tự động chèn kịch bản AI (Dạng 1: Kiểm chứng lỗi AI, Dạng 2: Prompting AI) và marker `**[AI: {Mã} - ...]**` vào các hoạt động (A, B, C, D, E).

### 4 Nguyên nhân chính:
1. **`buildIntegrationActivityConstraint(phase)` trong `js/khbd-app.js` (dòng 4661–4696)**:
   - Hệ thống mặc định bật Năng lực số (`digital: true`).
   - Điều kiện kiểm tra `if (!digitalOn && !aiOn) return ""` bị vượt qua vì `digitalOn === true`.
   - Hàm này sau đó trả về chuỗi ép buộc Gemini:
     *"Khi pha ${phase} có tích hợp NLS/AI, BẮT BUỘC dùng đúng 1 trong 3 dạng kịch bản thực chiến: - Dạng 1: Kiểm chứng & Phản biện lỗi sai của AI... - Dạng 2: Prompting tư duy môn học... - Dạng 3: Phần mềm chuyên dụng NLS..."*
   - Trong 3 dạng thì có tới 2 dạng là của AI. Gemini hiểu lầm là được quyền chọn Dạng 1 hoặc Dạng 2, dẫn tới việc tự động sinh kịch bản AI và gán marker `[AI]`.
   - Khi `aiOn === false`, hàm này hoàn toàn thiếu câu lệnh phủ định (negative constraint) cấm AI.

2. **`buildPedagogicalContext()` trong `js/khbd-app.js` (dòng 4603)**:
   - Khối văn bản hướng dẫn tích hợp NLS/AI được nhúng cứng vào mọi prompt mà không kiểm tra cờ `aiOn`:
     *"TÍCH HỢP NLS & AI THỰC CHIẾN GẮN MÔN HỌC: ... CHỈ tích hợp tại 1–2 vị trí then chốt, đắc địa nhất theo 3 dạng: (1) Kiểm chứng phản biện lỗi sai AI, (2) Prompting gợi mở bước giải..."*

3. **`ACTIVITY_TABLE_CONTRACT` và template prompt trong `js/khbd-prompts.js`**:
   - `ACTIVITY_TABLE_CONTRACT` (dòng 247–253) và các mẫu `GENERATE_ACTIVITY_B` (dòng 661), `GENERATE_ACTIVITY_C` (dòng 706), `GENERATE_ACTIVITY_D` (dòng 758) chứa các câu cố định: *"+ Khi có NLS/AI: Tích hợp thực chiến theo đúng 1 trong 3 dạng (Dạng 1: Kiểm chứng phản hồi AI... Dạng 2: Prompting... Gắn marker [AI: ...])"*.
   - Trong `getPromptTemplate(templateKey, context)` thiếu chỉ thị ghi đè cấp cao cấm triệt để AI khi `context.aiCompetencyEnabled === false`.

4. **Thiếu bộ lọc hậu xử lý (Post-processing Sanitizer) cho nội dung Hoạt động**:
   - `stripDisabledObjectivesStandardSections` hiện tại chỉ lọc mục tiêu phần I (`editorObjectives`).
   - Khi Gemini trả về nội dung hoạt động (A–E) trong `applyActivityOutput` và `clipKhbdActivityMarkdown`, không có hàm nào bóc tách hoặc loại bỏ các marker `[AI: ...]`, `**[AI]**` hay các câu lệnh prompting AI sinh nhầm khi giáo viên tắt cờ AI.

---

## Phạm vi can thiệp

### 1. File dự kiến tác động
- `js/khbd-app.js`:
  + Sửa `buildIntegrationActivityConstraint(phase)`: Tách biệt hoàn toàn logic giữa NLS và AI. Khi `!aiOn`, cấm tuyệt đối Dạng 1, Dạng 2 và cấm gắn bất kỳ marker `[AI]`. Khi chỉ bật NLS (`digitalOn && !aiOn`), chỉ cho phép duy nhất Dạng 3 (Phần mềm chuyên dụng NLS).
  + Sửa `buildPedagogicalContext()`: Điều kiện hóa mục Tích hợp thực chiến theo đúng cờ `digitalOn` và `aiOn`. Thêm chỉ thị cấm AI rõ ràng khi `!aiOn`.
  + Thêm hàm hậu xử lý `stripDisabledActivityIntegrations(markdown)`: Tự động loại bỏ sạch các tag `**[AI: ...]**`, `[AI: ...]`, `**[AI]**`, `[AI]` và các đoạn văn kịch bản AI sinh nhầm khi `!aiOn`. Tương tự với NLS khi `!digitalOn`.
  + Tích hợp `stripDisabledActivityIntegrations` vào `applyActivityOutput`, `clipKhbdActivityMarkdown` và sự kiện `toggleAiCompetency` khi giáo viên bỏ tick AI trên giao diện.
- `js/khbd-prompts.js`:
  + Trong `getPromptTemplate(templateKey, context)`: Khi `!context.aiCompetencyEnabled`, nối thêm chỉ thị cấm ghi đè nghiêm ngặt:
    *"QUY TẮC BẮT BUỘC VỀ KHUNG NĂNG LỰC AI: Giáo viên KHÔNG bật tích hợp Khung năng lực AI (QĐ 2422). Bỏ qua mọi gợi ý về AI/Dạng 1/Dạng 2/[AI] ở trên. TUYỆT ĐỐI CẤM chèn bất kỳ marker [AI], [AI: ...], CẤM kịch bản kiểm chứng phản biện AI, CẤM prompting AI vào giáo án."*
- `tests/khbd-ai-integration-gate.test.js` (NEW):
  + Bộ test kiểm tra tự động:
    1. Khi `aiOn === false`, `buildIntegrationActivityConstraint()` không sinh ra Dạng 1, Dạng 2 hay tag `[AI]`.
    2. Khi `aiOn === false`, `getPromptTemplate()` cho hoạt động A/B/C/D/E có chỉ thị cấm AI nghiêm ngặt.
    3. Hàm `stripDisabledActivityIntegrations()` làm sạch hoàn toàn các marker `**[AI: 7.A1.MR1 - Kiểm chứng phản hồi AI]**` và `[AI]` khỏi bảng d) khi tắt AI, nhưng giữ nguyên marker `[NLS]` nếu NLS bật.

### 2. Ngoài phạm vi
- Không thay đổi logic khi giáo viên CHỦ ĐỘNG BẬT cờ Khung AI (`aiOn === true`).
- Không ảnh hưởng đến các màn hình khác (`nghiencuubaihoc.html`, `xaydungphuluc.html`, etc.).

---

## Chi tiết các bước thực hiện cho Coder

### Bước 1: Sửa `buildIntegrationActivityConstraint(phase)` trong `js/khbd-app.js`
1. Tách rẽ nhánh rõ ràng theo `digitalOn` và `aiOn`:
   - Nếu `!digitalOn && !aiOn`:
     Trả về cảnh báo nghiêm ngặt cấm cả NLS và AI:
     `QUY TẮC NLS/AI CHO PHA ${phase}: Giáo viên KHÔNG bật Năng lực số và KHÔNG bật Năng lực AI. TUYỆT ĐỐI CẤM đưa bất kỳ kịch bản nào liên quan đến NLS/AI, CẤM chèn marker [NLS], [AI] vào hoạt động.`
   - Nếu `digitalOn && !aiOn`:
     + Cung cấp DUY NHẤT kịch bản Dạng 3 (Phần mềm chuyên dụng NLS: GeoGebra, Desmos, bảng tính Excel, máy tính cầm tay, PhET...) với marker `[NLS: {Miền/Mã} - {Tên phần mềm}]`.
     + Kèm theo lệnh cấm nghiêm khắc:
       `CẤM TUYỆT ĐỐI: Giáo viên KHÔNG bật Khung năng lực AI (QĐ 2422). TUYỆT ĐỐI CẤM đưa Dạng 1 (kiểm chứng phản hồi AI), Dạng 2 (prompting AI), TUYỆT ĐỐI CẤM chèn bất kỳ tag [AI], [AI: ...] nào.`
   - Nếu `aiOn && !digitalOn`:
     + Cung cấp kịch bản Dạng 1 & Dạng 2 (AI).
     + Kèm theo lệnh cấm NLS.
   - Nếu `digitalOn && aiOn`:
     + Cho phép chọn 1 trong 3 dạng như hiện tại.

### Bước 2: Sửa `buildPedagogicalContext()` trong `js/khbd-app.js`
Tại dòng 4603:
- Thay vì ghi chung "TÍCH HỢP NLS & AI THỰC CHIẾN GẮN MÔN HỌC...", kiểm tra `digitalOn` và `aiOn`:
  - Nếu `!aiOn`: Thêm dòng cấm rõ ràng:
    `- NĂNG LỰC AI (QĐ 2422): KHÔNG BẬT. CẤM tự ý đưa kịch bản AI, prompt AI hay marker [AI] vào bất kỳ hoạt động nào.`
  - Nếu `!digitalOn`: Thêm dòng cấm NLS rõ ràng:
    `- NĂNG LỰC SỐ (CV 3456): KHÔNG BẬT. CẤM tự ý đưa kịch bản NLS hay marker [NLS] vào giáo án.`

### Bước 3: Cập nhật `getPromptTemplate` trong `js/khbd-prompts.js`
Trong hàm `getPromptTemplate(templateKey, context)`:
- Kiểm tra nếu `!context.aiCompetencyEnabled`:
  Thêm chỉ thị phủ định có độ ưu tiên cao:
  ```javascript
  result += `\n\nLỆNH BẮT BUỘC KHÓA NĂNG LỰC AI: Giáo viên KHÔNG kích hoạt Khung năng lực AI (QĐ 2422). Bỏ qua toàn bộ các hướng dẫn hoặc ví dụ mẫu liên quan đến AI (Dạng 1 kiểm chứng phản hồi AI, Dạng 2 prompting AI) trong hợp đồng biên soạn. TUYỆT ĐỐI CẤM đưa nội dung AI hoặc gắn bất kỳ marker [AI], [AI: ...] vào bài.`;
  ```
- Tương tự, nếu `!context.digitalCompetencyEnabled`:
  Thêm chỉ thị khóa NLS tương ứng.

### Bước 4: Viết hàm hậu xử lý `stripDisabledActivityIntegrations` trong `js/khbd-app.js`
1. Định nghĩa hàm:
   ```javascript
   function stripDisabledActivityIntegrations(markdown) {
     const context = normalizeTeachingContext(appState.teachingContext);
     const digitalOn = Boolean(context.integrations.digital);
     const aiOn = Boolean(context.integrations.ai);
     let text = String(markdown || "");
     if (!aiOn) {
       // Xóa sạch các marker AI
       text = text.replace(/\*\*\[?AI(?::[^\]\n]+)?\]?\*\*/gi, "")
                  .replace(/\[AI(?::[^\]\n]+)?\]/gi, "");
       // Xóa các dòng hướng dẫn prompt AI nếu có lọt vào
       text = text.replace(/^[ \t]*[-+*]?[ \t]*Hướng dẫn Prompt AI.*$/gmi, "")
                  .replace(/^[ \t]*[-+*]?[ \t]*Mẫu Prompt:.*$/gmi, "");
     }
     if (!digitalOn) {
       text = text.replace(/\*\*\[?NLS(?::[^\]\n]+)?\]?\*\*/gi, "")
                  .replace(/\[NLS(?::[^\]\n]+)?\]/gi, "");
     }
     return text;
   }
   ```
2. Gọi hàm này trong `applyActivityOutput`:
   `finalResult = stripDisabledActivityIntegrations(finalResult);`
3. Gọi hàm này trong `clipKhbdActivityMarkdown`:
   `clipped = stripDisabledActivityIntegrations(clipped);`
4. Khi giáo viên toggle bỏ tick `toggleAiCompetency`:
   Duyệt qua `appState.content.activities` (A, B, C, D, E) và áp dụng `stripDisabledActivityIntegrations` để dọn sạch ngay lập tức nếu trước đó đã từng sinh có AI.

### Bước 5: Viết bộ test `tests/khbd-ai-integration-gate.test.js`
- Chạy qua `node tests/khbd-ai-integration-gate.test.js`.
- Kiểm tra các test cases:
  1. `aiOn = false`: `buildIntegrationActivityConstraint("B")` chứa lệnh cấm AI và KHÔNG chứa "Dạng 1" hay "Dạng 2".
  2. `aiOn = false`: `stripDisabledActivityIntegrations` làm sạch chuỗi `**[AI: 7.A1.MR1 - Kiểm chứng phản hồi AI]**`.
  3. `aiOn = true`: Giữ nguyên marker AI bình thường.

---

## Tiêu chí nghiệm thu (Acceptance Criteria)
1. Khi giáo viên **không kích chọn** `✨ Năng lực AI`:
   - Soạn Hoạt động A, B, C, D, E: **Hoàn toàn không có** bất kỳ marker `[AI]`, `[AI: ...]`, kịch bản phản biện AI, hay prompting AI nào xuất hiện.
   - Nếu có bật NLS (`digital: true`), giáo án chỉ chứa kịch bản NLS thuần túy (GeoGebra, phần mềm môn học, bảng tính) với marker `[NLS: ...]`.
2. Khi giáo viên **kích chọn** `✨ Năng lực AI`:
   - Kịch bản AI hoạt động bình thường, đúng 1–2 vị trí then chốt, đúng chuẩn QĐ 2422.
3. Test suite tự động PASS 100%.