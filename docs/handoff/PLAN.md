# KẾ HOẠCH BÀN GIAO TRIỂN KHAI (HANDOFF PLAN)

## 1. Hiện trạng & Phản ánh từ Người dùng
1. **Vấn đề 1 (Câu văn ngô nghê/vô nghĩa do ghép thô tên bài học)**:
   - **Phản ánh từ User**:
     > *"Nó sinh ra các câu vô nghĩa, khi nó gắn tên bài vô cho có:*
     > *`[NLS: 5.3.TC2a - Sử dụng máy tính cầm tay (chức năng tính giá trị biểu thức / phím CALC) để kiểm tra các cặp số/giá trị cho trước có phải là nghiệm của Khái niệm phương trình và hệ hai phương trình bậc nhất hai ẩn hay không.]`*
     > *Nghiệm của khái niệm phương trình là gì?"*
   - **Bản chất vấn đề**:
     Tên bài học trong chương trình/SGK thường chứa các từ ngữ chỉ mục tiêu sư phạm như `"Khái niệm phương trình..."`, `"Nhận biết tam giác đều..."`, `"Mở đầu về số hữu tỉ..."`. Khi engine tự động nối thô chuỗi `${clean}` vào vị trí thực thể toán học (`nghiệm của ${clean}`), câu văn trở thành *"nghiệm của Khái niệm phương trình..."*, gây phi lý về mặt thuật ngữ toán học và sư phạm.

2. **Vấn đề 2 (Cấu trúc bảng Phụ lục 3 - Kế hoạch giáo dục của giáo viên)**:
   - **Phản ánh từ User**:
     > *"Ở phụ lục 3 chúng ta cũng nên tách ra cột Biểu hiện khung năng lực số và biểu hiện khung năng lực AI đi nhỉ,"*
   - **Bản chất vấn đề**:
     - Trong Phụ lục 1 (Kế hoạch dạy học của Tổ chuyên môn), bảng đã được tách thành 2 cột riêng biệt:
       * Cột 5: `Biểu hiện năng lực số` (Màu xanh lam `#0070C0`)
       * Cột 6: `Biểu hiện năng lực AI` (Màu tím `#7030A0`)
     - Trong khi đó, Phụ lục 3 hiện tại vẫn dùng bảng 7 cột truyền thống, trong đó cột 7 là `Mã NLS & AI (CV 3456 & QĐ 2422)` gộp chung cả hai nội dung vào cùng một ô.
     - Giáo viên và nhà trường cần sự đồng bộ tuyệt đối về mặt hình thức giữa Phụ lục 1 và Phụ lục 3: Tách Phụ lục 3 thành 8 cột, có 2 cột riêng biệt cho NLS và AI.

---

## 2. Khảo sát Gốc rễ Mã nguồn (Root Cause Analysis)

### Gốc rễ Vấn đề 1: Ghép thô `${clean}` trong `lessonAppliedNlsDescription` và `lessonAppliedAiDescription`
- **Vị trí**:
  - `canvas_xaydungphuluc.html` (dòng 1443–1446)
  - `backupcode viettailieu/canvas_xaydungphuluc.html` (dòng 1443–1446)
  - `xaydungphuluc.html` (dòng 1428–1431)
- **Cơ chế gây lỗi**:
  Hàm `cleanLessonDescription(lesson)` hiện tại chỉ lọc bỏ các tiền tố `"Bài 1."`, `"Chủ đề 2."`, nhưng giữ nguyên nội dung bài:
  `"Bài 1. Khái niệm phương trình và hệ hai phương trình bậc nhất hai ẩn"` $\rightarrow$ `clean = "Khái niệm phương trình và hệ hai phương trình bậc nhất hai ẩn"`.
  Tại dòng 1444 (`lessonAppliedNlsDescription`):
  ```javascript
  if (isConceptEq) return `Sử dụng máy tính cầm tay (chức năng tính giá trị biểu thức / phím CALC) để kiểm tra các cặp số/giá trị cho trước có phải là nghiệm của ${clean} hay không.`;
  ```
  $\rightarrow$ Biến thành: `...có phải là nghiệm của Khái niệm phương trình và hệ hai phương trình bậc nhất hai ẩn hay không.` (Khái niệm không thể có nghiệm, chỉ có phương trình/hệ phương trình mới có nghiệm).
- **Các mẫu câu khác bị ảnh hưởng tương tự**:
  1. `c.startsWith('1.1')`: `...nhận biết khái niệm và các trường hợp nghiệm của ${clean}.`
  2. `c.startsWith('3.1')`: `...hệ thống hóa định nghĩa, dạng tổng quát và tập nghiệm bài ${clean}.`
  3. `lessonAppliedAiDescription` (domain B): `...kiểm tra nghiệm bài ${clean}; giải thích lý do vì sao một trường hợp thỏa mãn hoặc không thỏa mãn định nghĩa.`
  4. `lessonAppliedAiDescription` (domain A): `...dẫn đến khái niệm bài ${clean}...`

### Gốc rễ Vấn đề 2: Cấu trúc 7 cột của Phụ lục 3
- **Vị trí**:
  - `canvas_xaydungphuluc.html` (dòng 66–68, dòng 216–220, dòng 1506–1511, dòng 1545)
  - `backupcode viettailieu/canvas_xaydungphuluc.html`
  - `xaydungphuluc.html`
  - `tests/xaydungphuluc-smoke.js` (dòng 136)
- **Cơ chế hiện tại**:
  1. `PPCT_COLUMNS` và `PLAN_COLUMNS` đang dùng chung cấu hình 7 cột:
     `[['lesson','Bài học'],['periods','Số tiết'],['tietCT','Tiết CT'],['week','Tuần'],['devices','Thiết bị dạy học (*)'],['location','Địa điểm dạy học (**)'],['integration','Mã NLS & AI (CV 3456 & QĐ 2422)']]`
  2. Trong `normalizeAppendix('3', c)`:
     `data.planTable = preservedPpctTable(data.plan, c)`
     `preservedPpctTable` gọi `ppctTableFromRows`, vốn trả về 7 cột gộp chung mã `row.integration`.
  3. `DOCX_WIDTHS.appendixThree` chỉ có 7 kích thước `[22, 6, 8, 6, 18, 16, 24]`.
  4. Báo cáo thẩm định `calculateComplianceReport` kiểm tra tính đồng bộ NLS & AI giữa PL1 và PL3 dựa trên trường `row.integration` của `data.plan`.

---

## 3. Phạm vi Giải quyết (Scope)
- **Thuộc phạm vi (In Scope)**:
  1. Xây dựng hàm chuẩn hóa thực thể toán học `cleanMathEntityName(lessonName)` để tách các cụm sư phạm (`Khái niệm`, `Mở đầu về`, `Làm quen với`...) ra khỏi tên đối tượng toán học.
  2. Rà soát và sửa toàn bộ các câu ghép chuỗi trong `lessonAppliedNlsDescription` và `lessonAppliedAiDescription` bảo đảm chuẩn 100% ngữ pháp tiếng Việt và ngôn ngữ học thuật toán học.
  3. Tách cấu trúc Phụ lục 3 thành 8 cột:
     - Cột 1: `Bài học`
     - Cột 2: `Số tiết`
     - Cột 3: `Tiết CT`
     - Cột 4: `Tuần`
     - Cột 5: `Thiết bị dạy học (*)`
     - Cột 6: `Địa điểm dạy học (**)`
     - Cột 7: `Biểu hiện năng lực số` (hoặc `Biểu hiện khung năng lực số`)
     - Cột 8: `Biểu hiện năng lực AI` (hoặc `Biểu hiện khung năng lực AI`)
  4. Cập nhật bảng xem trước HTML (`dynamicPpctTable` và `renderPreview`).
  5. Cập nhật bảng xuất Word DOCX (`DOCX_WIDTHS.appendixThree`, `exportDocx`, `addPpct`).
  6. Mở rộng regex `isNlsColumn` và `isAiColumn` để khớp linh hoạt cả "Biểu hiện năng lực số" và "Biểu hiện khung năng lực số".
  7. Đồng bộ cả 3 file: `canvas_xaydungphuluc.html`, `backupcode viettailieu/canvas_xaydungphuluc.html` (đảm bảo byte-identical), và `xaydungphuluc.html`.
  8. Cập nhật các bộ kiểm thử smoke tests (`tests/xaydungphuluc-smoke.js`, `tests/xaydungphuluc-math-smoke.js`).
- **Ngoài phạm vi (Out of Scope)**:
  - Không thay đổi bảng Phụ lục 1 hoặc Phụ lục 2.
  - Không thay đổi logic chia tiết, phân phối số tiết (PPCT) của môn học.
  - Không làm thay đổi cơ chế báo cáo thẩm định 100% CV 5512.

---

## 4. Danh sách File Tác động (Target Files)
1. `canvas_xaydungphuluc.html`
2. `backupcode viettailieu/canvas_xaydungphuluc.html` (bắt buộc giống hệt file 1)
3. `xaydungphuluc.html`
4. `tests/xaydungphuluc-smoke.js`
5. `tests/xaydungphuluc-math-smoke.js`

---

## 5. Kế hoạch Triển khai Chi tiết cho ChatGPT (Step-by-step Implementation Plan)

### Bước 1: Xử lý Lỗi ghép chuỗi vô nghĩa trong mô tả NLS và AI
1. **Thêm hàm bóc tách thực thể toán học `cleanMathEntityName`**:
   Đặt ngay sau `cleanLessonDescription`:
   ```javascript
   function cleanMathEntityName(lessonName) {
     const clean = typeof cleanLessonDescription === 'function' ? cleanLessonDescription(lessonName) : String(lessonName || '').trim();
     return clean.replace(/^(?:khái niệm về|khái niệm|nhận biết|mở đầu về|làm quen với|định nghĩa về|tìm hiểu về)\s+/i, '').trim() || clean;
   }
   ```
2. **Cập nhật trong `lessonAppliedNlsDescription(code, label, lesson)`**:
   - Lấy thêm: `const entity = cleanMathEntityName(clean);`
   - Tại nhánh `c.startsWith('5.3')`:
     - Khi `isConceptEq`:
       * Cũ: `Sử dụng máy tính cầm tay (chức năng tính giá trị biểu thức / phím CALC) để kiểm tra các cặp số/giá trị cho trước có phải là nghiệm của ${clean} hay không.`
       * Mới: `Sử dụng máy tính cầm tay (chức năng tính giá trị biểu thức / phím CALC) để kiểm tra các cặp số/giá trị cho trước có phải là nghiệm của ${entity} hay không.`
       $\rightarrow$ Kết quả: `...có phải là nghiệm của phương trình và hệ hai phương trình bậc nhất hai ẩn hay không.`
   - Tại nhánh `c.startsWith('1.1') || c.startsWith('1.')`:
     - Khi `isConceptEq`:
       * Cũ: `Khai thác học liệu số, video bài giảng trực quan nhận biết khái niệm và các trường hợp nghiệm của ${clean}.`
       * Mới: `Khai thác học liệu số, video bài giảng trực quan nhận biết khái niệm, dạng tổng quát và các trường hợp nghiệm của ${entity}.`
   - Tại nhánh `c.startsWith('3.1') || c.startsWith('3.')`:
     - Khi `isConceptEq`:
       * Cũ: `Sử dụng công cụ số (phần mềm vẽ sơ đồ tư duy / bảng biểu) để hệ thống hóa định nghĩa, dạng tổng quát và tập nghiệm bài ${clean}.`
       * Mới: `Sử dụng công cụ số (phần mềm vẽ sơ đồ tư duy / bảng biểu) để hệ thống hóa định nghĩa, dạng tổng quát và tập nghiệm của ${entity}.`
   - Tại nhánh `c.startsWith('5.2')`:
     - Khi `isConceptEq`:
       * Đổi: `...quan sát và kiểm tra các dấu hiệu nhận biết trong bài ${clean}.` (thêm chữ "trong").
3. **Cập nhật trong `lessonAppliedAiDescription(code, label, lesson)`**:
   - Lấy thêm: `const entity = cleanMathEntityName(clean);`
   - Tại nhánh `domain === 'B'`:
     - Khi `isConceptEq`:
       * Cũ: `Ứng dụng công cụ AI hỗ trợ tạo các ví dụ ngẫu nhiên về số liệu/phương trình để học sinh luyện tập nhận biết khái niệm và kiểm tra nghiệm bài ${clean}; giải thích lý do vì sao một trường hợp thỏa mãn hoặc không thỏa mãn định nghĩa.`
       * Mới: `Ứng dụng công cụ AI hỗ trợ tạo các ví dụ ngẫu nhiên về số liệu/phương trình để học sinh luyện tập nhận biết khái niệm và kiểm tra nghiệm của ${entity}; giải thích lý do vì sao một trường hợp thỏa mãn hoặc không thỏa mãn định nghĩa.`
   - Tại nhánh `domain === 'A'`:
     - Khi `isConceptEq`:
       * Đổi: `Sử dụng trợ lý AI gợi mở tình huống thực tiễn dẫn đến khái niệm trong bài ${clean}, học sinh chủ động trao đổi, đối chiếu với SGK và giữ quyền quyết định cuối cùng.`

---

### Bước 2: Nâng cấp Phụ lục 3 thành 8 cột (Tách riêng NLS và AI)
1. **Định nghĩa danh mục cột cho Phụ lục 3 (`APPENDIX_3_COLUMNS`)**:
   - Trong phần khai báo hằng số đầu file (dòng 65–68):
     ```javascript
     const APPENDIX_1_COLUMNS=[['stt','STT'],['lesson','Bài học'],['periods','Số tiết'],['outcomes','Yêu cầu cần đạt'],['nls','Biểu hiện năng lực số'],['ai','Biểu hiện năng lực AI']];
     const PPCT_COLUMNS=[['lesson','Bài học'],['periods','Số tiết'],['tietCT','Tiết CT'],['week','Tuần'],['devices','Thiết bị dạy học (*)'],['location','Địa điểm dạy học (**)'],['integration','Mã NLS & AI (CV 3456 & QĐ 2422)']];
     const APPENDIX_3_COLUMNS=[['lesson','Bài học'],['periods','Số tiết'],['tietCT','Tiết CT'],['week','Tuần'],['devices','Thiết bị dạy học (*)'],['location','Địa điểm dạy học (**)'],['nls','Biểu hiện năng lực số'],['ai','Biểu hiện năng lực AI']];
     const SCHEDULE_COLUMNS=PPCT_COLUMNS,PLAN_COLUMNS=APPENDIX_3_COLUMNS;
     ```
2. **Cập nhật regex nhận diện cột (`isNlsColumn`, `isAiColumn`)**:
   - Cho phép cả cụm từ "Biểu hiện năng lực số" và "Biểu hiện khung năng lực số":
     ```javascript
     function isNlsColumn(label){return /^biểu hiện\s+(?:khung\s+)?năng\s+lực\s+số$/i.test(String(label||'').trim())}
     function isAiColumn(label){return /^biểu hiện\s+(?:khung\s+)?năng\s+lực\s+ai$/i.test(String(label||'').trim())}
     ```
3. **Xây dựng hàm `appendixThreeTable(planRows, c)`**:
   - Viết hàm chuyên trách tạo bảng 8 cột cho Phụ lục 3:
     ```javascript
     function appendixThreeTable(planRows, c) {
       const columns = APPENDIX_3_COLUMNS.map(x => x[1]);
       let normal = 0;
       const rows = (planRows || []).map((row, index) => {
         if (row.isHeader) return { isHeader: true, cells: [row.lesson] };
         const { nlsText, aiText } = separateIntegration(
           row.integration,
           selectedPeriodsForLessonId(row.id || `ppct:${index}`),
           normal,
           c,
           row.lesson,
           row.periods
         );
         normal++;
         return {
           isHeader: false,
           cells: [
             String(row.lesson || '').trim(),
             String(row.periods || '').trim(),
             String(row.tietCT || '').trim(),
             String(row.week || '').trim(),
             String(row.devices || '').trim(),
             String(row.location || '').trim(),
             nlsText || '-',
             aiText || '-'
           ]
         };
       });
       return { columns, rows, lessonIndex: 0 };
     }
     ```
4. **Cập nhật `normalizeAppendix('3', c)`**:
   - Sử dụng `appendixThreeTable` để gán vào `data.planTable`:
     ```javascript
     }else if(no==='3'){
       const defaultEquip=(typeof EQUIPMENT!=='undefined'&&c&&(EQUIPMENT[c.monHoc]||EQUIPMENT.default))?(EQUIPMENT[c.monHoc]||EQUIPMENT.default).slice(0,2).join(', '):'Thiết bị dạy học tối thiểu';
       data.plan=(data.plan||[]).map((row,i)=>{
         const r=ppctRow(row,i,c);
         if(!r.isHeader){
           if(!r.devices)r.devices=defaultEquip;
           if(!r.location)r.location='Lớp học';
         }
         return r;
       }).filter(row=>row.lesson&&!isAdminLesson(row.lesson));
       if(!results['1'])results['1']=normalizeAppendix(fallback('1',c),'1',c);
       data.plan=syncIntegrationFromAppendixOne(data.plan,results['1'].scheduleTable,c);
       data.planTable=appendixThreeTable(data.plan,c);
     }
     ```
5. **Cập nhật hiển thị xem trước Preview Phụ lục 3 trong `renderPreview`**:
   - Dòng 1536:
     ```javascript
     if(activeTab==='3'){
       preview.innerHTML=`<h3 class="font-black text-center my-4">${esc(r.title||'PHỤ LỤC')}</h3><h4 class="font-bold">I. Phân phối chương trình</h4>${dynamicPpctTable(r.planTable||appendixThreeTable(r.plan||[],getConfig()))}<h4 class="font-bold mt-4">II. Chuyên đề lựa chọn</h4>${table([['topic','Chuyên đề'],['time','Thời điểm'],['devices','Thiết bị'],['location','Địa điểm']],r.specialties||[],'specialties')}`;
       return;
     }
     ```
6. **Cập nhật độ rộng cột xuất Word DOCX (`DOCX_WIDTHS.appendixThree`)**:
   - Dòng 1545:
     ```javascript
     appendixThree: [20, 5, 6, 5, 14, 12, 19, 19]
     ```
     (Tổng 100%: Bài học 20%, Số tiết 5%, Tiết CT 6%, Tuần 5%, Thiết bị 14%, Địa điểm 12%, NLS 19%, AI 19%).
   - Trong `exportDocx(n)`:
     `addPpct(r.planTable || appendixThreeTable(r.plan || [], getConfig()), 'appendixThree');`

---

### Bước 3: Đồng bộ Backup và Cập nhật Smoke Tests
1. **Đồng bộ file backup**:
   - Sao chép toàn bộ nội dung từ `canvas_xaydungphuluc.html` sang `backupcode viettailieu/canvas_xaydungphuluc.html` để đảm bảo 100% byte-identical.
2. **Cập nhật `tests/xaydungphuluc-smoke.js`**:
   - Cập nhật chuỗi kiểm tra `appendixThree`:
     * Cũ: `'appendixThree:[22,6,8,6,18,16,24]'`
     * Mới: `'appendixThree:[20,5,6,5,14,12,19,19]'`
   - Bổ sung kiểm tra sự hiện diện của `APPENDIX_3_COLUMNS` và `appendixThreeTable`.
3. **Cập nhật `tests/xaydungphuluc-math-smoke.js`**:
   - Bổ sung assertion kiểm tra Phụ lục 3 có đúng 8 cột dữ liệu:
     * Cột 7: `isNlsColumn` trả về true.
     * Cột 8: `isAiColumn` trả về true.
     * Kiểm tra văn bản sinh ra không còn chứa cụm từ vô nghĩa `"nghiệm của Khái niệm phương trình"`.

---

## 6. Rủi ro & Phương án Giảm thiểu (Risks & Mitigations)
1. **Rủi ro phá vỡ tính tương thích ngược của `normalizeIntegrationTable`**:
   - *Phân tích*: Nếu bảng đầu vào có cả `isNlsColumn` và `isAiColumn`, hàm `normalizeIntegrationTable` phải giữ nguyên 8 cột mà không được tự ý gộp lại thành `INTEGRATION_COLUMN_LABEL`.
   - *Giải pháp*: `normalizeIntegrationTable` đã có sẵn dòng kiểm tra `if(columns.some(isNlsColumn)&&columns.some(isAiColumn)) return ...;`. Việc nâng cấp regex `isNlsColumn` và `isAiColumn` bảo đảm điều kiện này luôn được kích hoạt an toàn.
2. **Rủi ro đứt gãy đồng bộ dữ liệu giữa Phụ lục 1 và Phụ lục 3**:
   - *Phân tích*: Báo cáo thẩm định `calculateComplianceReport` kiểm tra trường `row.integration` trong mảng `data.plan`.
   - *Giải pháp*: `data.plan` tiếp tục lưu trữ trường `row.integration` (kế thừa 100% từ Phụ lục 1 qua `syncIntegrationFromAppendixOne`). Bảng `data.planTable` chỉ làm nhiệm vụ phân rã thành 8 cột để hiển thị UI và xuất Word. Nhờ vậy, tiêu chí thẩm định *"Đồng bộ NLS & AI (PL1–PL3)"* luôn đạt 100%.

---

## 7. Kế hoạch Kiểm thử & Thẩm định (Verification Plan)
1. **Kiểm thử tự động (Unit / Smoke Tests)**:
   - Chạy lệnh: `node tests/xaydungphuluc-smoke.js`
   - Chạy lệnh: `node tests/xaydungphuluc-math-smoke.js`
   - Chạy toàn bộ test suite: `node tests/run-all-tests.js` (yêu cầu 61/61 suites PASS 100%).
2. **Kiểm tra ngữ nghĩa chuỗi sinh ra**:
   - Với bài học `"Bài 1. Khái niệm phương trình và hệ hai phương trình bậc nhất hai ẩn"`:
     * Mô tả NLS 5.3: `...nghiệm của phương trình và hệ hai phương trình bậc nhất hai ẩn hay không.` (Không còn chữ "Khái niệm").
     * Mô tả AI 9.B2.1: `...kiểm tra nghiệm của phương trình và hệ hai phương trình bậc nhất hai ẩn;...`
3. **Kiểm tra Phụ lục 3 có 8 cột**:
   - Cột 7: `Biểu hiện năng lực số`, chứa mã NLS và mô tả màu xanh `#0070C0`.
   - Cột 8: `Biểu hiện năng lực AI`, chứa mã AI và mô tả màu tím `#7030A0`.
   - Xuất Word Phụ lục 3 ra file `.docx` kiểm tra bảng có đúng 8 cột, công thức Toán OMML nguyên vẹn.

---

## 8. Tiêu chí Nghiệm thu (Acceptance Criteria)
1. `cleanMathEntityName` loại bỏ triệt để các tiền tố sư phạm khi ghép vào đối tượng nghiệm toán học.
2. Tuyệt đối không còn bất kỳ câu nào có dạng `"nghiệm của Khái niệm phương trình..."`.
3. Phụ lục 3 có đúng 8 cột ở cả giao diện HTML Preview lẫn trong file Word DOCX xuất ra.
4. Cột 7 và 8 của Phụ lục 3 hiển thị tách biệt rõ ràng giữa NLS và AI, khớp 100% với Phụ lục 1.
5. Cả 61 bộ kiểm thử `node tests/run-all-tests.js` đều PASS 100%.
6. File `canvas_xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html` đồng nhất 100% (byte-for-byte).
