# PLAN: Di chuyển khối Cấu hình NLS & AI và Khắc phục lỗi Phụ lục 3 rỗng bảng

---

## 1. Yêu cầu & Mục tiêu

### Nhiệm vụ 1: Di chuyển khối Cấu hình NLS & AI
- **Vị trí hiện tại**: Đang nằm trong Mục 1 (cùng thẻ card với 11 trường thông tin hành chính trường học & giáo viên).
- **Vị trí mới**: Di chuyển xuống đặt **sau Mục 2** (Tài liệu & dữ liệu nguồn) và **trên Mục 3** (Chọn loại phụ lục).
- **Đánh số lại các mục**:
  - `1. Thông tin trường học & giáo viên` (trước là `1. Thông tin & cấu hình sư phạm`)
  - `2. Tài liệu & dữ liệu nguồn` (giữ nguyên)
  - `3. Cấu hình Năng lực số & Trí tuệ nhân tạo` (khối mới chuyển xuống)
  - `4. Chọn loại phụ lục` (trước là 3)
  - `5. AI đề xuất bài/tiết tích hợp NLS & AI; bạn rà soát và điều chỉnh` (trước là 4)
  - `6. Ý tưởng / chỉ đạo riêng` (trước là 5)
  - `7. Tiến trình xử lý` (trước là 6)
  - `8. Xem trước & xuất Word` (trước là 7)
- **Ý nghĩa**: Sau khi nạp thông tin trường (Mục 1) và nạp PPCT/tài liệu nguồn (Mục 2), hệ thống tính ra tổng số tiết và số bài PPCT thực tế (ví dụ: `95 tiết PPCT · 47 bài`). Người dùng cấu hình tỉ lệ % hoặc số tiết/bài NLS & AI ngay tại Mục 3 sẽ chuẩn xác và tiện lợi hơn.

### Nhiệm vụ 2: Khắc phục triệt để lỗi Phụ lục 3 mở ra / xuất Word không có dòng dữ liệu nào (bảng rỗng)
- **Hiện tượng**: Khi mở Phụ lục 3 (Tab 3) hoặc xuất file Word Phụ lục 3 (`Phu-luc-3-Toan-hoc.docx`), bảng "I. Phân phối chương trình" có 8 cột tiêu đề (`Bài học`, `Số tiết`, `Tiết CT`, `Tuần`, `Thiết bị dạy học (*)`, `Địa điểm dạy học (**)`, `Biểu hiện năng lực số`, `Biểu hiện năng lực AI`), nhưng **phần thân bảng hoàn toàn rỗng (0 dòng)**.
- **Nguyên nhân gốc**:
  1. Khi AI sinh Phụ lục 3, do giới hạn token hoặc do prompt hướng dẫn ("bạn chỉ trả nội dung cột integration..."), AI thường:
     - Bỏ qua thuộc tính `plan` (chỉ trả `{ title, specialties, duties }`), hoặc
     - Trả thuộc tính mang tên `schedule` hoặc `ppct` hoặc `items` thay vì `plan`, hoặc
     - Trả mảng `plan: []`.
  2. Trong hàm `normalizeAppendix(data, '3', c)`:
     - `data.plan = (data.plan || [])...` khiến `data.plan` nhận giá trị mảng rỗng `[]`.
     - `syncIntegrationFromAppendixOne(data.plan, ...)` duyệt qua `[]` trả về `[]`.
     - `appendixThreeTable(appendix.plan || [], c)` duyệt qua `[]` trả về `rows: []`.
  3. `appendixThreeTable` và `syncIntegrationFromAppendixOne` không có cơ chế fallback về `results['1']?.schedule`, `sourcePpctRows`, hay `defaultPpctRows(c)` khi `planRows` bị rỗng.
  4. Trong `renderPreview()` và `exportDocx(3)`: Chưa có rào chắn tự động phát hiện `planModel.rows.length === 0` để tái tạo lại từ PPCT nguồn/Phụ lục 1.

---

## 2. Phạm vi tệp tin cần sửa đổi (Scope)

Coder thực hiện đồng bộ trên 3 tệp HTML và 1 tệp test:
1. `xaydungphuluc.html`
2. `canvas_xaydungphuluc.html`
3. `backupcode viettailieu/canvas_xaydungphuluc.html`
4. `tests/xaydungphuluc-smoke.js` (bổ sung test kiểm tra fallback Phụ lục 3 không bao giờ rỗng)

---

## 3. Hướng dẫn chi tiết cho Coder

### PHẦN A: Di chuyển khối giao diện NLS & AI

Áp dụng đồng nhất cho cả 3 tệp (`xaydungphuluc.html`, `canvas_xaydungphuluc.html`, `backupcode viettailieu/canvas_xaydungphuluc.html`):

#### 1. Mục 1: Thu gọn chỉ còn thông tin trường học & giáo viên
- Sửa tiêu đề thẻ `<h2>`:
  ```html
  <h2 class="font-black mb-3">1. Thông tin trường học &amp; giáo viên</h2>
  ```
- Giữ nguyên toàn bộ lưới input hành chính (Trường, Tổ, Môn học, Khối lớp, Năm học, Giáo viên, Bộ sách, Số lớp, Số HS, Số GV...).
- **Cắt bỏ** toàn bộ:
  - Khối chứa 2 card NLS và AI: `<div class="grid md:grid-cols-2 gap-4 mt-5">...</div>` (hoặc `mt-4`).
  - Khối chứa 2 checkbox CLIL & Giáo dục hòa nhập: `<div class="mt-4 flex flex-wrap gap-4">...</div>`.
- Đóng thẻ `</section>` của Mục 1 ngay sau lưới input hành chính.

#### 2. Mục 3 mới: Tạo card Cấu hình Năng lực số & Trí tuệ nhân tạo
- Đặt thẻ `<section class="card p-5">` mới ngay dưới `</section>` của Mục 2 (Tài liệu & dữ liệu nguồn) và trước Mục "Chọn loại phụ lục":
  ```html
    <section class="card p-5"><h2 class="font-black mb-3">3. Cấu hình Năng lực số &amp; Trí tuệ nhân tạo</h2><div class="grid md:grid-cols-2 gap-4"><div class="border rounded-xl p-4"><div class="flex justify-between"><label><input id="nlsEnabled" type="checkbox" checked onchange="onNlsEnabledChange(this.checked)"> <b>Năng lực số (CV 3456 / TT 02)</b></label><output id="nlsRateOut">50%</output></div><div class="flex gap-2 items-center mt-2 mb-1"><select id="nlsUnit" class="field text-xs py-1 px-2 w-auto" onchange="onNlsUnitChange(this.value)"><option value="period" selected>Theo tổng số tiết PPCT</option><option value="lesson">Theo tổng số bài PPCT</option></select><input id="nlsCountInput" type="number" min="0" class="field text-xs py-0.5 px-1.5 w-16 text-center" onchange="syncNlsSelectionFromCount(this.value)" aria-label="Số tiết hoặc bài NLS"><span class="text-xs opacity-70">hoặc kéo tỉ lệ % bên dưới:</span></div><input id="nlsRate" class="w-full" type="range" min="0" max="100" value="50" oninput="syncNlsSelectionFromRate()"><label class="label mt-2">Phân bổ số lượng mã NLS / bài</label><select id="nlsDensity" class="field" onchange="toggleNlsCustomDensity(this.value)"><option value="adaptive" selected>Tự động theo tiết &amp; AI (Khuyên dùng)</option><option value="1-2">Cố định 1–2 mã/bài</option><option value="2-3">Cố định 2–3 mã/bài</option><option value="3-4">Cố định 3–4 mã/bài</option></select><div id="nlsAdaptiveOptions" class="mt-2 text-xs space-y-1 p-2.5 rounded-lg border" style="background:var(--paper);border-color:var(--line);color:var(--ink);"><div>• Bài 1 tiết: <b style="color:var(--brand)">Có AI → 0 NLS (1 AI); Không AI → 1 mã NLS</b></div><div>• Bài từ 2 tiết có AI: <b style="color:var(--brand)">1 mã NLS</b></div><label class="flex items-center gap-2"><span>• Bài từ 2 tiết không có AI:</span><select id="nlsNoAiDensity" class="field text-xs py-0.5 px-1.5 w-auto" style="background:var(--card);color:var(--ink);border-color:var(--line);"><option value="2" selected>2 mã</option><option value="2-3">2–3 mã</option></select></label></div></div><div class="border rounded-xl p-4"><div class="flex justify-between"><label><input id="aiEnabled" type="checkbox" checked onchange="onAiEnabledChange(this.checked)"> <b>Trí tuệ nhân tạo (QĐ 2422)</b></label><output id="aiRateOut">30%</output></div><div class="flex gap-2 items-center mt-2 mb-1"><select id="aiUnit" class="field text-xs py-1 px-2 w-auto" onchange="onAiUnitChange(this.value)"><option value="period" selected>Theo tổng số tiết PPCT</option><option value="lesson">Theo tổng số bài PPCT</option></select><input id="aiCountInput" type="number" min="0" class="field text-xs py-0.5 px-1.5 w-16 text-center" onchange="syncAiSelectionFromCount(this.value)" aria-label="Số tiết hoặc bài AI"><span class="text-xs opacity-70">hoặc kéo tỉ lệ % bên dưới:</span></div><input id="aiRate" class="w-full" type="range" min="0" max="100" value="30" oninput="syncAiSelectionFromRate()"><label class="label mt-2">Mật độ mã AI / tiết đã chọn</label><select id="aiDensity" class="field"><option value="1-2" selected>1–2 mã/bài</option><option value="2-3">2–3 mã/bài</option><option value="3-4">3–4 mã/bài</option></select></div></div></div><div class="mt-4 flex flex-wrap gap-4"><label><input id="clil" type="checkbox"> Thêm thuật ngữ Tiếng Anh chuyên ngành / CLIL</label><label><input id="inclusive" type="checkbox"> Giáo dục hòa nhập HS khuyết tật</label></div></section>
  ```
  *(Lưu ý: trong `canvas_xaydungphuluc.html`, các thẻ `select` và `input` không cần thuộc tính `onchange` inline vì hàm `bindFlexibleAllocationControls()` đã gán listener qua selector, nhưng giữ nguyên các `id` chuẩn).*

#### 3. Đánh số lại các mục tiếp theo:
- Đổi tiêu đề:
  - `4. Chọn loại phụ lục`
  - `5. AI đề xuất bài/tiết tích hợp NLS & AI; bạn rà soát và điều chỉnh`
  - `6. Ý tưởng / chỉ đạo riêng`
  - `7. Tiến trình xử lý`
  - `8. Xem trước & xuất Word`
- Cập nhật thông báo text trong code (nếu có chuỗi `Mục 3`, `Mục 7` liên quan đến fileList, đổi thành `Mục 5` và `Mục 8`).

---

### PHẦN B: Khắc phục triệt để lỗi Phụ lục 3 rỗng bảng

#### 1. Cập nhật hàm `appendixThreeTable(planRows, c)`
Trong cả 3 tệp HTML:
Tìm định nghĩa hàm `function appendixThreeTable(planRows,c){...}`:
Bổ sung cơ chế fallback ngay đầu hàm nếu `planRows` không có phần tử:
```javascript
function appendixThreeTable(planRows,c){
  const columns=APPENDIX_3_COLUMNS.map(x=>x[1]);
  let normal=0;
  const pl1Model=results?.['1']?.scheduleTable?normalizeIntegrationTable(results['1'].scheduleTable):null;
  const pl1NlsIdx=pl1Model?pl1Model.columns.findIndex(isNlsColumn):-1;
  const pl1AiIdx=pl1Model?pl1Model.columns.findIndex(isAiColumn):-1;
  const pl1LessonIdx=pl1Model?pl1Model.columns.map(normalizeHeaderKey).indexOf('lesson'):-1;
  
  // Tự động fallback nếu planRows rỗng hoặc undefined
  let effectiveRows = (Array.isArray(planRows) && planRows.length) ? planRows : [];
  if(!effectiveRows.length){
    if(results?.['1']?.schedule && Array.isArray(results['1'].schedule) && results['1'].schedule.length){
      effectiveRows = results['1'].schedule;
    } else if(typeof sourcePpctRows !== 'undefined' && Array.isArray(sourcePpctRows) && sourcePpctRows.length){
      effectiveRows = sourcePpctRows;
    } else if(typeof defaultPpctRows === 'function'){
      effectiveRows = defaultPpctRows(c || (typeof getConfig==='function'?getConfig():{}));
    }
  }

  const rows=(effectiveRows||[]).map((row,index)=>{
    if(row.isHeader)return {isHeader:true,cells:[row.lesson]};
    let nlsText='',aiText='';
    if(pl1Model&&pl1LessonIdx>=0){
      const pl1Row=pl1Model.rows.find(item=>!item.isHeader&&lessonsMatch((item.cells||[])[pl1LessonIdx],row.lesson));
      if(pl1Row){
        if(pl1NlsIdx>=0)nlsText=String((pl1Row.cells||[])[pl1NlsIdx]||'').trim();
        if(pl1AiIdx>=0)aiText=String((pl1Row.cells||[])[pl1AiIdx]||'').trim();
      }
    }
    if(!nlsText&&!aiText){
      const selected=selectedPeriodsForLesson(row.id||`ppct:${index}`,row.lesson);
      const sep=separateIntegration(row.integration,selected,normal,c,row.lesson,row.periods,row.id||`ppct:${index}`);
      nlsText=sep.nlsText;aiText=sep.aiText;
    }
    if(!aiText&&c?.ai?.enabled&&hasAiCode(row.integration)){
      const selected=selectedPeriodsForLesson(row.id||`ppct:${index}`,row.lesson);
      if(selected.length){aiText=cleanAiColumnText(row.integration,row.lesson);}
    }
    normal++;
    return {
      isHeader:false,
      cells:[
        String(row.lesson||'').trim(),
        String(row.periods||'').trim(),
        String(row.tietCT||'').trim(),
        String(row.week||'').trim(),
        String(row.devices||'').trim(),
        String(row.location||'').trim(),
        nlsText||'-',
        aiText||'-'
      ]
    };
  });
  return {columns,rows,lessonIndex:0};
}
```

#### 2. Cập nhật hàm `syncIntegrationFromAppendixOne(targetPlanRows, appendixOneTable, config)`
Trong cả 3 tệp HTML:
Tìm hàm `function syncIntegrationFromAppendixOne(targetPlanRows,appendixOneTable,config){...}`:
Bổ sung fallback nếu `targetPlanRows` rỗng:
```javascript
function syncIntegrationFromAppendixOne(targetPlanRows,appendixOneTable,config){
  let rows = (Array.isArray(targetPlanRows) && targetPlanRows.length) ? targetPlanRows : [];
  if(!rows.length){
    if(results?.['1']?.schedule && Array.isArray(results['1'].schedule) && results['1'].schedule.length){
      rows = results['1'].schedule;
    } else if(typeof sourcePpctRows !== 'undefined' && Array.isArray(sourcePpctRows) && sourcePpctRows.length){
      rows = sourcePpctRows;
    } else if(typeof defaultPpctRows === 'function'){
      rows = defaultPpctRows(config);
    }
  }
  return (rows||[]).map((row,index)=>{
    if(row.isHeader)return row;
    const integration=appendixOneIntegrationForLesson(row.lesson,{scheduleTable:appendixOneTable})||selectedIntegration(row.integration,selectedPeriodsForLesson(row.id||`ppct:${index}`,row.lesson),index,config,row.lesson,row.periods,row.id||`ppct:${index}`);
    return {...row,integration};
  });
}
```

#### 3. Cập nhật nhánh `no==='3'` trong `normalizeAppendix(data, no, c)`
Trong cả 3 tệp HTML:
Tìm đoạn:
```javascript
}else if(no==='3'){
  const defaultEquip=(typeof EQUIPMENT!=='undefined'&&c&&(EQUIPMENT[c.monHoc]||EQUIPMENT.default))?(EQUIPMENT[c.monHoc]||EQUIPMENT.default).slice(0,2).join(', '):'Thiết bị dạy học tối thiểu';
  data.plan=(data.plan||[]).map((row,i)=>{...
```
Sửa thành:
```javascript
}else if(no==='3'){
  const defaultEquip=(typeof EQUIPMENT!=='undefined'&&c&&(EQUIPMENT[c.monHoc]||EQUIPMENT.default))?(EQUIPMENT[c.monHoc]||EQUIPMENT.default).slice(0,2).join(', '):'Thiết bị dạy học tối thiểu';
  let planCandidate = (Array.isArray(data.plan) && data.plan.length) ? data.plan :
                      (Array.isArray(data.schedule) && data.schedule.length) ? data.schedule :
                      (Array.isArray(data.ppct) && data.ppct.length) ? data.ppct :
                      (Array.isArray(data.items) && data.items.length) ? data.items :
                      (Array.isArray(data.rows) && data.rows.length) ? data.rows : [];
  if (!planCandidate.length) {
    if (results['1'] && Array.isArray(results['1'].schedule) && results['1'].schedule.length) {
      planCandidate = results['1'].schedule;
    } else if (typeof sourcePpctRows !== 'undefined' && Array.isArray(sourcePpctRows) && sourcePpctRows.length) {
      planCandidate = sourcePpctRows;
    } else if (typeof defaultPpctRows === 'function') {
      planCandidate = defaultPpctRows(c);
    }
  }
  data.plan=(planCandidate||[]).map((row,i)=>{
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

#### 4. Cập nhật `renderPreview()` cho `activeTab === '3'`
Trong cả 3 tệp HTML:
Tìm `if(activeTab==='3'){`:
Thay vì chỉ lấy `r.planTable`, bảo đảm luôn có dữ liệu hàng:
```javascript
if(activeTab==='3'){
  let planModel=(r.planTable&&r.planTable.columns&&r.planTable.columns.length===8&&r.planTable.rows&&r.planTable.rows.length)?r.planTable:null;
  if(!planModel){
    if(!results['1']) results['1']=normalizeAppendix(fallback('1',getConfig()),'1',getConfig());
    planModel=appendixThreeTable(r.plan||[],getConfig());
    r.planTable=planModel;
  }
  preview.innerHTML=`<h3 class="font-black text-center my-4">${esc(r.title||'PHỤ LỤC 3 – KẾ HOẠCH GIÁO DỤC CỦA GIÁO VIÊN')}</h3><h4 class="font-bold">I. Phân phối chương trình</h4>${dynamicPpctTable(planModel)}<h4 class="font-bold mt-4">II. Chuyên đề lựa chọn</h4>${table([['topic','Chuyên đề'],['time','Thời điểm'],['devices','Thiết bị'],['location','Địa điểm']],r.specialties||[],'specialties')}`;
  return;
}
```

#### 5. Cập nhật `exportDocx(n, save=true)` cho Phụ lục 3
Trong cả 3 tệp HTML:
Tìm đoạn xuất docx của Phụ lục 3:
```javascript
}else{
  add(r.title||`PHỤ LỤC ${n}`,{center:true,bold:true,size:28});
  add('I. Phân phối chương trình',{bold:true});
  let planModel=(r.planTable&&r.planTable.columns&&r.planTable.columns.length===8&&r.planTable.rows&&r.planTable.rows.length)?r.planTable:null;
  if(!planModel){
    if(!results['1']) results['1']=normalizeAppendix(fallback('1',getConfig()),'1',getConfig());
    planModel=appendixThreeTable(r.plan||[],getConfig());
    r.planTable=planModel;
  }
  addPpct(planModel,'appendixThree');
  add('II. Chuyên đề lựa chọn',{bold:true});
  addTable([['topic','Chuyên đề'],['time','Thời điểm'],['devices','Thiết bị'],['location','Địa điểm']],r.specialties||[]);
};
```

---

## 4. Kiểm tra và xác minh (Verification Plan)

Coder thực hiện các bước kiểm tra sau:

### 1. Bổ sung test tự động trong `tests/xaydungphuluc-smoke.js`
Thêm kiểm thử chứng minh Phụ lục 3 không rỗng ngay cả khi AI trả về `{ plan: [] }` hoặc dữ liệu rỗng:
```javascript
const emptyPlanOutput = sandbox.appendixThreeTable([], splitConfig);
assert.ok(emptyPlanOutput.rows.length > 0, 'appendixThreeTable must fallback and never return 0 rows when default PPCT exists');
assert.equal(emptyPlanOutput.columns.length, 8, 'appendixThreeTable must retain 8 columns');
```

### 2. Chạy toàn bộ các bộ test tự động:
```bash
node tests/xaydungphuluc-smoke.js
node tests/canvas-xaydungphuluc-smoke.js
node tests/xaydungphuluc-math-smoke.js
node tests/sgk-knowledge-smoke.js
```
Tất cả đều phải trả về **PASS** 100%.

### 3. Ghi chép bàn giao
Sau khi hoàn tất, Coder ghi toàn bộ nội dung đã sửa và kết quả kiểm thử vào tệp:
`docs/handoff/IMPLEMENT.md`.
