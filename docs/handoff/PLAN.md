# PLAN: Khắc phục lỗi Header Fetch, Tối ưu chọn NLS/AI chuẩn sư phạm & chính xác tuyệt đối, Đồng bộ 100% Phụ lục 3 từ Phụ lục 1

## 1. Tổng quan các vấn đề khảo sát & Phản biện Sư phạm

### Vấn đề 1: Lỗi `String contains non ISO-8859-1 code point` khi Mở Modal Tải/Lưu CSDL
- **Nguyên nhân**: `prefillCanvasDraftAccount` tự động lấy tên giáo viên có dấu (`"Hoàng Tấn Thiên"`) làm username và truyền vào HTTP Header `'X-User-Account'` trong `requestCanvasDraft`. Trình duyệt chuẩn W3C Fetch API cấm ký tự Unicode mã > 255 trong Header, gây ném ngoại lệ ngay lập tức.
- **Giải pháp**:
  - Dùng `encodeURIComponent(account)` khi gán vào `'X-User-Account'`.
  - Backend PHP `api/user_phuluc_draft.php` dùng `rawurldecode()`.
  - Sửa `prefillCanvasDraftAccount`: chỉ lấy username hợp lệ, không tự ý gán họ tên giáo viên có dấu vào ô username.

---

### Vấn đề 2: Chọn 28 tiết NLS lại ra 30 tiết (Không tuân thủ số tiết đã chọn)
- **Phản biện Sư phạm & Kỹ thuật**:
  - **Không phải "vét bừa" các bài 1 tiết**: Việc tích hợp NLS và AI vào môn học bắt buộc phải dựa trên **độ phù hợp sư phạm của từng bài học** (ví dụ: các bài có thực hành số, hình học trực quan GeoGebra, biểu đồ thống kê Excel, hoạt động trải nghiệm/STEM được tính điểm ưu tiên sư phạm cao; các bài ôn tập, kiểm tra định kỳ có điểm ưu tiên thấp).
  - **Tuyệt đối tuân thủ con số người dùng đã chọn**: Khi giáo viên đã định mức chọn **đúng 28 tiết NLS** (hoặc 12 tiết AI), hệ thống **tuyệt đối không được tự ý nhảy cóc lên 30 tiết** hay xê dịch làm tròn.
  - **Nguyên nhân code cũ bị nhảy số**:
    1. Cơ chế đồng bộ bị phụ thuộc vào thanh trượt `%` (`#nlsRate`), khi bấm gợi ý nó tự động quy đổi ngược từ % với phép làm tròn `Math.round`, làm ghi đè mất con số 28 tiết chính xác mà giáo viên đã nhập.
    2. Thuật toán chọn bài cũ dùng phép duyệt tham lam (Greedy) và ràng buộc cứng loại trừ bài đơn tiết, dẫn đến việc khi thiếu bài lẻ nó nhảy cóc sang bài 2-3 tiết làm vượt ngưỡng lên 30.
- **Giải pháp chuẩn xác**:
  - Áp dụng bài toán **0/1 Knapsack tối ưu hóa Sư phạm có ràng buộc Dung lượng chính xác (Exact Capacity Knapsack)**:
    - **Mục tiêu**: Tối đa hóa tổng điểm ưu tiên sư phạm $\sum \text{Score}_i$ của các bài học được tích hợp (ưu tiên các bài học phù hợp nhất với NLS theo Catalog chương trình).
    - **Ràng buộc cứng**: Tổng số tiết của các bài học được chọn $\sum \text{Periods}_i = \text{Target}$ **(chính xác tuyệt đối 100% bằng đúng con số giáo viên yêu cầu, ví dụ đúng 28 tiết)**.
  - Lắng nghe tức thì sự kiện `input` trên ô `#nlsCountInput` và `#aiCountInput`. Khi giáo viên đã chỉ định số lượng cụ thể, hệ thống cố định con số này, không để thanh trượt `%` làm tròn đè lên.

---

### Vấn đề 3: Phụ lục 3 bị mất Tiết CT, mất Tuần, mất tiêu đề Học kỳ/Chương và lệch so với Phụ lục 1
- **Phản biện Sư phạm**:
  - Nhận định của giáo viên: **"Phụ lục 1 làm chuẩn, Phụ lục 3 chỉ điều chỉnh lại từ Phụ lục 1"** là **chuẩn tắc 100% theo Công văn 5512/BGDĐT-GDTrH**:
    - Phụ lục 1 là Kế hoạch dạy học của Tổ chuyên môn, phê duyệt khung phân phối chương trình chung của cả khối.
    - Phụ lục 3 là Kế hoạch giáo dục của cá nhân giáo viên, bắt buộc phải kế thừa nguyên vẹn 100% khung PPCT đã duyệt của Tổ chuyên môn (Bài học, Số tiết, Tiết CT, Tuần, Thiết bị, Địa điểm, dòng tiêu đề Học kỳ/Chương).
    - Cột 7 của Phụ lục 3 là `Ghi chú`: đồng bộ nội dung tích hợp NLS & AI tương ứng từng bài từ Phụ lục 1.
- **Nguyên nhân code cũ gây lỗi**:
  - Khi sinh Phụ lục 3, code lại gửi prompt gọi AI Gemini sinh lại bảng PPCT. AI văn bản không thể ghi nhớ và khớp chính xác số thứ tự Tiết CT (1, 2, 5, 6...) và Tuần từ tệp tải lên, đồng thời AI tự tiện bỏ qua các dòng tiêu đề Học kỳ/Chương.
- **Giải pháp triệt để**:
  - **Tuyệt đối không cho AI sinh lại bảng PPCT ở Phụ lục 3**.
  - Kế thừa trực tiếp 100% từ Bảng nguồn PPCT / Phụ lục 1 sang Phụ lục 3:
    - Giữ nguyên từng bài, số tiết, **Tiết CT**, **Tuần**, thiết bị, địa điểm.
    - Giữ nguyên các dòng tiêu đề phân cấp: `HỌC KÌ I`, `1. SỐ HỌC 6`, `CHƯƠNG I. TẬP HỢP SỐ TỰ NHIÊN (13 tiết)` (`isHeader: true`).
    - Cột `Ghi chú`: Đồng bộ 100% từ cột Ghi chú của Phụ lục 1.
  - Khi xuất Word (`exportDocx`): Các dòng `isHeader: true` được merge toàn bộ 7 cột (`colspan="7"`), căn giữa, in đậm đúng chuẩn mẫu CV 5512.

---

## 2. Chi tiết các bước thực hiện cho Coder

### Bước 1: Sửa lỗi Fetch Header trong `canvas_xaydungphuluc.html` và `api/user_phuluc_draft.php`
1. Tại `canvas_xaydungphuluc.html`:
   - Hàm `requestCanvasDraft`: Bọc `'X-User-Account': encodeURIComponent(account)`.
   - Hàm `prefillCanvasDraftAccount`: Không lấy `#teacher` nếu có dấu tiếng Việt hoặc khoảng trắng.
2. Tại `api/user_phuluc_draft.php`:
   - Thêm `if (strpos($account, '%') !== false) $account = rawurldecode($account);`.

### Bước 2: Chuẩn hóa thuật toán Knapsack Tối ưu Sư phạm & Khắc phục triệt để lỗi 30/28 tiết

1. Tại `canvas_xaydungphuluc.html` (và đồng bộ sang `xaydungphuluc.html`, `backupcode viettailieu/canvas_xaydungphuluc.html`):
   - **Điểm 1 (Sửa `ppctRow` khoảng dòng 226)**:
     Thay:
     `integration: isHeader ? '' : (row.integration || (c ? integrationText(i, c, lesson) : '')),`
     Bằng:
     `integration: isHeader ? '' : (row.integration && row.integration !== '-' && row.integration !== '0' && row.integration !== String(i) ? row.integration : ''),`
     (Không gọi `integrationText(i, c, lesson)` vì hàm `integrationText(value)` chỉ nhận 1 tham số và trả về `String(i)`, làm ô tích hợp bị nhiễm số nguyên `0`, `1`...).

   - **Điểm 2 (Sửa `isLessonNlsSelected` khoảng dòng 1417)**:
     Thay thế toàn bộ hàm để bỏ so khớp lỏng lẻo `lessonsMatch(x.lesson, lessonName)` (nguyên nhân chính làm trùng bài "Bài 1", "Luyện tập chung" giữa HK1 và HK2, dẫn đến đếm dư 2 tiết làm 28 nhảy thành 30):
     ```javascript
     function isLessonNlsSelected(lessonId, lessonName, c, index){
       if(c?.nls && c.nls.enabled === false) return false;
       if(typeof nlsEnabled !== 'undefined' && nlsEnabled && nlsEnabled.checked === false) return false;
       const hasId = lessonId != null && String(lessonId) !== '';
       const hasExplicit = typeof nlsSelectedLessonIds !== 'undefined' && nlsSelectedLessonIds.size > 0;
       if(hasExplicit){
         if(hasId) return nlsSelectedLessonIds.has(lessonId);
         if(Number.isInteger(index) && typeof nlsCandidates === 'function'){
           const cands = nlsCandidates();
           if(cands[index]) return nlsSelectedLessonIds.has(cands[index].id);
         }
         if(lessonName && typeof nlsCandidates === 'function'){
           const match = nlsCandidates().find(x => x.lesson === lessonName);
           if(match && nlsSelectedLessonIds.has(match.id)) return true;
         }
         return false;
       }
       const rate = Number(c?.nls?.rate);
       if(Number.isFinite(rate) && rate <= 0) return false;
       const prioritized = typeof prioritizedNlsLessons === 'function' ? prioritizedNlsLessons() : [];
       if(!prioritized.length) return c?.nls?.enabled !== false;
       if(!Number.isFinite(rate)) return true;
       const targetCount = Math.round(rate / 100 * prioritized.length);
       const topIds = new Set(prioritized.slice(0, targetCount).map(x => x.id));
       if(hasId) return topIds.has(lessonId);
       if(Number.isInteger(index) && prioritized[index]) return topIds.has(prioritized[index].id);
       if(lessonName){
         const match = prioritized.find(x => x.lesson === lessonName);
         if(match && topIds.has(match.id)) return true;
       }
       return false;
     }
     ```

   - **Điểm 3 (Sửa `getConfig` khoảng dòng 1514)**:
     Trong object `nls:` thêm `count: Number(document.querySelector('#nlsCountInput')?.value) || 0`.

   - **Điểm 4 (Sửa `calculateComplianceReport` khoảng dòng 1669)**:
     Thay:
     `isNlsPeriodUnit=c.nls?.unit==='period',nlsTarget=c.nls?.enabled?(isNlsPeriodUnit?Math.round(periods*(Number(c.nls.rate)||0)/100):Math.ceil(rows.length*(Number(c.nls.rate)||0)/100)):0,`
     Bằng:
     `isNlsPeriodUnit=c.nls?.unit==='period',nlsTarget=c.nls?.enabled?(c.nls?.count>0?c.nls.count:(isNlsPeriodUnit?Math.round(periods*(Number(c.nls.rate)||0)/100):Math.ceil(rows.length*(Number(c.nls.rate)||0)/100))):0,`

   - **Điểm 5 (Sửa `integrationParts` khoảng dòng 1564)**:
     Thêm guard loại bỏ chuỗi không phải mã:
     `if(typeof raw==='string'&&!/(?:NLS|AI|TC|\d+\.[A-Z])/i.test(raw))return [];`

### Bước 3: Khắc phục triệt để lỗi Phụ lục 3 mất Tiết CT, Tuần, Tiêu đề chương

- **Nguyên nhân**:
  1. Khi sinh Phụ lục 1, AI chỉ trả về `{index, lesson, periods, outcomes}` (không có `tietCT` và `week`).
  2. Tại dòng 1709, `normalizeAppendix` cho `no === '3'` lại ưu tiên lấy `results['1'].schedule` trước `sourcePpctRows`:
     `const fullSchedule = results['1']?.schedule?.length ? results['1'].schedule : ...`
     Do `results['1'].schedule` đã bị AI lược bỏ `tietCT`, `week` và các dòng tiêu đề chương `isHeader: true`, Phụ lục 3 bị mất sạch toàn bộ thông tin này!

- **Cách sửa chi tiết**:
  1. **Tại dòng 1709 (`normalizeAppendix` cho `no === '3'`)**:
     Thay thế:
     ```javascript
     const fullSchedule=results['1']?.schedule?.length?results['1'].schedule:typeof sourcePpctRows!=='undefined'&&Array.isArray(sourcePpctRows)&&sourcePpctRows.length?sourcePpctRows:typeof defaultPpctRows==='function'?defaultPpctRows(c):[];
     ```
     Bằng (Ưu tiên tuyệt đối bảng nguồn PPCT đã tải lên `sourcePpctRows` hoặc PPCT chuẩn `defaultPpctRows`):
     ```javascript
     const fullSchedule=(typeof sourcePpctRows!=='undefined'&&Array.isArray(sourcePpctRows)&&sourcePpctRows.length)?sourcePpctRows:(typeof defaultPpctRows==='function'?defaultPpctRows(c):(results['1']?.schedule||[]));
     ```

  2. **Tại dòng 1649 (`normalizeAppendix` cho `no === '1'`)**:
     Khôi phục `tietCT`, `week`, `devices`, `location` từ nguồn PPCT khi map `data.schedule`:
     ```javascript
     let normalIndex=0;
     const sourceList=(sourcePpctRows.length?sourcePpctRows:(typeof defaultPpctRows==='function'?defaultPpctRows(c):[])).filter(r=>!r.isHeader);
     data.schedule=(data.schedule||[]).map((row,i)=>{
       const r=ppctRow(row,i,c);
       if(!r.isHeader){
         const src=sourceList[normalIndex++]||{};
         if(!r.tietCT&&src.tietCT) r.tietCT=src.tietCT;
         if(!r.week&&src.week) r.week=src.week;
         if(!r.devices) r.devices=src.devices||defaultEquip;
         if(!r.location) r.location=src.location||'Lớp học';
       }
       return {...r,outcomes:String(row.outcomes||row.outcome||row.requirements||'').trim()};
     }).filter(row=>row.lesson&&!isAdminLesson(row.lesson));
     ```

  3. **Xuất Word trong `exportDocx`**:
     Giữ nguyên merger dòng tiêu đề (`colspan: columns.length`) và bảng 7 cột chuẩn của Phụ lục 3 (`appendixThree`: `[20, 5, 6, 5, 15, 14, 35]`).
  4. Đồng bộ các sửa đổi sang file `xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html`.

---

## 3. Tiêu chí nghiệm thu (Verification Criteria)
1. **Lỗi Fetch Header**: Mở modal Tải/Lưu CSDL khi tài khoản là `"Hoàng Tấn Thiên"`, không ném lỗi `String contains non ISO-8859-1 code point`.
2. **Chọn tiết NLS**: Nhập `28` tiết vào ô `#nlsCountInput` $\rightarrow$ Hệ thống chọn các bài có điểm ưu tiên sư phạm cao nhất và đạt đúng **chính xác 28 tiết**, không tự ý nhảy thành 30 tiết.
3. **Phụ lục 3 chuẩn mẫu Word CV 5512**:
   - Xuất Word Phụ lục 3 có đầy đủ cột `Tiết CT` và `Tuần` như file PPCT tải lên.
   - Hiển thị đầy đủ các dòng tiêu đề Học kỳ, Chương (`HỌC KÌ I`, `CHƯƠNG I...`) merge toàn bộ 7 cột, căn giữa, in đậm.
   - Cột `Ghi chú` hiển thị đầy đủ mã NLS & AI đồng bộ 100% với Phụ lục 1.
4. Chạy smoke test `tests/canvas-xaydungphuluc-smoke.js` và `tests/xaydungphuluc-smoke.js` đạt PASS 100%.
