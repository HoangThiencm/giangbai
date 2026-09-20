# PLAN: Bỏ Dấu Ngoặc Vuông [ ] Ở Tên Các Năng Lực (Chung, Đặc Thù, Phẩm Chất) trong canvas_soankhbd

## 1. Hiện trạng & Nguyên nhân Gốc rễ (Root Cause)

### Hiện trạng
Khi tạo **I. Mục tiêu** trong `canvas_soankhbd.html`, kết quả AI sinh ra có dạng:
```markdown
## 2. Về năng lực

### a) Năng lực chung
- [Tự chủ và tự học]: Học sinh tự lực thực hiện các nhiệm vụ...
- [Giải quyết vấn đề và sáng tạo]: Học sinh phát hiện được quy luật...

### b) Năng lực đặc thù môn học
- [Tư duy và lập luận toán học]: Học sinh thực hiện được các thao tác...
- [Mô hình hóa toán học]: Học sinh sử dụng được đơn thức...
```
Người dùng yêu cầu bỏ các dấu ngoặc vuông `[ ]` bao quanh tên năng lực này, trả về dạng chuẩn công văn:
```markdown
## 2. Về năng lực

### a) Năng lực chung
- Tự chủ và tự học: Học sinh tự lực thực hiện các nhiệm vụ...
- Giải quyết vấn đề và sáng tạo: Học sinh phát hiện được quy luật...

### b) Năng lực đặc thù môn học
- Tư duy và lập luận toán học: Học sinh thực hiện được các thao tác...
- Mô hình hóa toán học: Học sinh sử dụng được đơn thức...
```

### Phân tích Root Cause
1. Trong file `js/khbd-prompts.js`:
   - Dòng 550 (`GENERATE_OBJECTIVES`):
     `- Mỗi năng lực chung viết đúng 1 dòng: \`- [Tên năng lực]: [mô tả hành vi cụ thể học sinh thực hiện trong bài học này]\`. CẤM nhãn Biểu hiện / Minh chứng.`
   - Dòng 563–570 (`GENERATE_OBJECTIVES` skeleton template):
     ```markdown
     ### a) Năng lực chung
     - [Tên năng lực chung 1 phù hợp môn {subject}]: [Mô tả hành vi cụ thể của học sinh trong bài học này]
     - [Tên năng lực chung 2 nếu có]: [Mô tả hành vi cụ thể của học sinh trong bài học này]
     
     ### b) Năng lực đặc thù môn học
     - [Tên năng lực đặc thù 1]: [Mô tả hành vi gắn với bài]
     - [Tên năng lực đặc thù 2]: [Mô tả hành vi gắn với bài]
     ```
   - Dòng 575 (Phẩm chất):
     `- [Tên phẩm chất]: [Mô tả hành vi quan sát được của học sinh trong bài]`
   - Dòng 1738 (`getPromptTemplate` runtime injection):
     `- Năng lực chung: CHỌN 1–2 năng lực phù hợp nhất với môn ${subjectName} từ danh sách gợi ý trên. Mỗi năng lực đúng 1 dòng: \`- [Tên năng lực]: [mô tả hành vi cụ thể trong bài]\`.`
   - Dòng 688–689 (`GENERATE_CORE_LESSON`):
     Chưa có chỉ thị rõ ràng về việc cấm dấu ngoặc vuông ở tên năng lực.
   
   $\rightarrow$ Mô hình LLM (Gemini) hiểu rằng `[Tên năng lực]:` là cú pháp bắt buộc phải xuất ra nguyên văn, dẫn tới việc bọc tên năng lực trong `[ ]`.

2. Trong `js/khbd-app.js`:
   - Hàm `applyObjectivesOutput` (dòng 7948) đã có các bộ chuẩn hoá mã NLS/AI nhưng chưa có bộ lọc làm sạch dấu ngoặc vuông `[ ]` thừa ở tên năng lực chung, năng lực đặc thù và phẩm chất.

---

## 2. Giải pháp Triển khai Chi tiết cho Coder

### Bước 1: Sửa Prompt trong `js/khbd-prompts.js`

1. Tại template `GENERATE_OBJECTIVES` (khoảng dòng 550–576):
   - Thay dòng 550 thành:
     ```javascript
     - Mỗi năng lực chung viết đúng 1 dòng: \`- Tên năng lực: mô tả hành vi cụ thể học sinh thực hiện trong bài học này\`. TUYỆT ĐỐI CẤM dùng dấu ngoặc vuông [ ] bao quanh tên năng lực, CẤM nhãn Biểu hiện / Minh chứng.
     ```
   - Thay dòng 553 thành:
     ```javascript
     - Mục 2.b (Năng lực đặc thù môn học): CHỈ 2–3 năng lực đặc thù nổi trội của môn {subject} gắn với bài học. Viết mỗi mục 1 dòng: \`- Tên năng lực: mô tả hành vi gắn với bài\`. TUYỆT ĐỐI CẤM dùng dấu ngoặc vuông [ ].
     ```
   - Cập nhật khung mẫu đầu ra (dòng 563–575):
     ```markdown
     ### a) Năng lực chung
     - Tên năng lực chung 1 phù hợp môn {subject}: Mô tả hành vi cụ thể của học sinh trong bài học này
     - Tên năng lực chung 2 nếu có: Mô tả hành vi cụ thể của học sinh trong bài học này
     
     ### b) Năng lực đặc thù môn học
     - Tên năng lực đặc thù 1: Mô tả hành vi gắn với bài
     - Tên năng lực đặc thù 2: Mô tả hành vi gắn với bài
     
     {digital_objectives_section}
     {ai_objectives_section}
     
     ## 3. Về phẩm chất & Giáo dục hòa nhập (hòa nhập chỉ khi được bật)
     - Tên phẩm chất: Mô tả hành vi quan sát được của học sinh trong bài
     ```

2. Tại `getPromptTemplate` (khoảng dòng 1737–1741):
   - Thay dòng 1738 thành:
     ```javascript
     - Năng lực chung: CHỌN 1–2 năng lực phù hợp nhất với môn ${subjectName} từ danh sách gợi ý trên. Mỗi năng lực đúng 1 dòng: \`- Tên năng lực: mô tả hành vi cụ thể trong bài\`. TUYỆT ĐỐI CẤM dùng dấu ngoặc vuông [ ] bao quanh tên năng lực.
     ```
   - Thay dòng 1740 thành:
     ```javascript
     - Năng lực đặc thù: 2–3 năng lực nổi trội của môn ${subjectName} (dạng \`- Tên năng lực: mô tả...\`, TUYỆT ĐỐI CẤM dùng ngoặc vuông [ ]). Phẩm chất: 1–2 phẩm chất (dạng \`- Tên phẩm chất: mô tả...\`, TUYỆT ĐỐI CẤM dùng ngoặc vuông [ ]).
     ```

3. Tại template `GENERATE_CORE_LESSON` (khoảng dòng 688–691):
   - Thêm chỉ thị rõ ràng:
     ```javascript
     - Mục 2.a (Năng lực chung): CHỈ 1–2 năng lực chung phù hợp đặc thù môn {subject} và bài dạy này; mỗi mục đúng 1 dòng mô tả hành vi. TUYỆT ĐỐI CẤM dùng ngoặc vuông [ ] bao quanh tên năng lực.
     - Mục 2.b (Năng lực đặc thù): 2–3 năng lực đặc thù của môn {subject}. TUYỆT ĐỐI CẤM dùng ngoặc vuông [ ].
     - Mục 3 (Phẩm chất): 1–2 phẩm chất gắn liền bài học (dạng \`- Tên phẩm chất: mô tả...\`, TUYỆT ĐỐI CẤM dùng ngoặc vuông [ ]).
     ```

> **LƯU Ý CỰC KỲ QUAN TRỌNG VỀ NLS VÀ AI:**
> KHÔNG ĐƯỢC chạm vào định dạng mã NLS và AI:
> `### c) Năng lực số: ***[Mã NLS]:*** ...`
> `### d) Năng lực AI: ***[Mã AI]:*** ...`
> Dấu ngoặc vuông ở mã NLS/AI (ví dụ `[5.3.TC2a]`, `[9.B2.1]`) là chuẩn Bộ GD&ĐT (TT 02/2025/TT-BGDĐT và QĐ 2422/QĐ-BGDĐT) và được khóa bởi các bài test hiện có.

---

### Bước 2: Hậu xử lý (Sanitization) Trong `js/khbd-app.js`

Để đảm bảo dù mô hình AI có sinh sót dấu ngoặc vuông thì người dùng vẫn luôn nhận được văn bản sạch, bổ sung hàm:

```javascript
/**
 * Loại bỏ dấu ngoặc vuông [ ] bao quanh tên năng lực (chung, đặc thù) và phẩm chất.
 * BẢO LƯU nguyên vẹn dấu ngoặc vuông ở mã NLS / AI (như [5.3.TC2a], [9.B2.1]).
 */
function stripSquareBracketsFromCompetencies(markdown) {
  if (!markdown) return "";
  const lines = String(markdown).split("\n");
  let currentSection = "";

  const updatedLines = lines.map(line => {
    const trimmed = line.trim();
    if (/^#{2,3}\s*a\)\s*Năng lực chung/i.test(trimmed)) {
      currentSection = "common";
      return line;
    }
    if (/^#{2,3}\s*b\)\s*Năng lực đặc thù/i.test(trimmed)) {
      currentSection = "subject";
      return line;
    }
    if (/^#{2,3}\s*c\)\s*Năng lực số/i.test(trimmed)) {
      currentSection = "digital";
      return line;
    }
    if (/^#{2,3}\s*d\)\s*Năng lực AI/i.test(trimmed)) {
      currentSection = "ai";
      return line;
    }
    if (/^#{2,3}\s*(?:3\.?\s*)?Về phẩm chất/i.test(trimmed)) {
      currentSection = "quality";
      return line;
    }
    if (/^#{1,3}\s+/i.test(trimmed)) {
      currentSection = "other";
      return line;
    }

    // Chỉ xử lý trong các phần: năng lực chung, năng lực đặc thù, phẩm chất
    if (currentSection === "common" || currentSection === "subject" || currentSection === "quality") {
      // Bắt các dạng:
      // - [Tự chủ và tự học]: mô tả
      // - [Tự chủ và tự học]: [mô tả]
      // * [Tự chủ và tự học]: mô tả
      const match = line.match(/^(\s*[-*]\s*)\[([^\]]+)\]\s*(:?)\s*(.*)$/);
      if (match) {
        const prefix = match[1];
        const compName = match[2].trim();
        const rest = match[4].replace(/^\[([\s\S]*?)\]$/, '$1').trim();
        return `${prefix}${compName}: ${rest}`;
      }
    }
    return line;
  });

  return updatedLines.join("\n");
}
```

Tích hợp vào pipeline của `applyObjectivesOutput(result, signal, options)` trong `js/khbd-app.js`:
```javascript
async function applyObjectivesOutput(result, signal, options = {}) {
  // ... các xử lý trước ...
  finalResult = applyPpctVerbatimObjectives(finalResult);
  finalResult = ensureObjectivesDigitalCodes(finalResult);
  finalResult = stripSquareBracketsFromCompetencies(finalResult); // <<-- Thêm ở đây
  finalResult = keepObjectivesOnly(stripDisabledObjectivesStandardSections(finalResult));
  appState.content.objectives = finalResult;
  saveStateToLocalStorage();
  return finalResult;
}
```
Và xuất hàm ra `window.stripSquareBracketsFromCompetencies = stripSquareBracketsFromCompetencies;` trong khối exports cuối file `js/khbd-app.js`.

---

### Bước 3: Tạo Test Suite Mới & Chạy Kiểm Thử

1. Tạo file kiểm thử mới `tests/khbd-competency-brackets-smoke.js`:
   - Kiểm tra `js/khbd-prompts.js`:
     + `GENERATE_OBJECTIVES` không chứa `- [Tên năng lực chung 1` hay `- [Tên năng lực]:`.
     + `GENERATE_OBJECTIVES` có chứa chỉ thị cấm ngoặc vuông: `TUYỆT ĐỐI CẤM dùng dấu ngoặc vuông [ ]`.
     + `getPromptTemplate('GENERATE_OBJECTIVES', ...)` sinh prompt không chứa `- [Tên năng lực]:`.
   - Kiểm tra hàm `stripSquareBracketsFromCompetencies`:
     + Đưa vào chuỗi Markdown chứa:
       ```markdown
       ## 2. Về năng lực
       ### a) Năng lực chung
       - [Tự chủ và tự học]: Học sinh tự lực thực hiện các nhiệm vụ cá nhân.
       - [Giải quyết vấn đề và sáng tạo]: Học sinh phát hiện quy luật.
       ### b) Năng lực đặc thù môn học
       - [Tư duy và lập luận toán học]: Học sinh thực hiện thao tác so sánh.
       - [Mô hình hóa toán học]: Học sinh sử dụng đơn thức.
       ### c) Năng lực số
       - ***[5.3.TC2a]:*** Mô tả nhiệm vụ số
       ### d) Năng lực AI
       - ***[9.B2.1]:*** Mô tả nhiệm vụ AI
       ## 3. Về phẩm chất
       - [Chăm chỉ]: Tích cực phát biểu xây dựng bài.
       ```
     + Kết quả sau khi chạy qua hàm:
       - Có `- Tự chủ và tự học: Học sinh tự lực...`
       - Có `- Giải quyết vấn đề và sáng tạo: Học sinh phát hiện...`
       - Có `- Tư duy và lập luận toán học: Học sinh thực hiện...`
       - Có `- Mô hình hóa toán học: Học sinh sử dụng...`
       - Có `- Chăm chỉ: Tích cực phát biểu...`
       - Không còn bất kỳ `[Tự chủ` hay `[Tư duy` nào.
       - VẪN BẢO LƯU NGUYÊN VẸN `***[5.3.TC2a]:***` và `***[9.B2.1]:***`.

2. Chạy toàn bộ test suite để đảm bảo không bị hồi quy:
   - `node tests/khbd-competency-brackets-smoke.js`
   - `node tests/canvas-soankhbd-smoke.js`
   - `node tests/canvas-prompts-integrity-smoke.js`
   - `node tests/khbd-competencies-smoke.js`
   - `node tests/khbd-nls-ai-bold-italic-smoke.js`
   - `node tests/ppct-settings-import-smoke.js`

---

## 3. Danh sách File Cần Chỉnh Sửa
1. `js/khbd-prompts.js` (Chỉnh sửa prompt và template `GENERATE_OBJECTIVES`, `GENERATE_CORE_LESSON`, `getPromptTemplate`)
2. `js/khbd-app.js` (Thêm hàm `stripSquareBracketsFromCompetencies`, gắn vào `applyObjectivesOutput` và export)
3. `tests/khbd-competency-brackets-smoke.js` (Tạo mới để kiểm thử tự động)
