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

### Bước 4: Sửa triệt để lỗi Gợi ý AI chọn 140 tiết, bài 1 tiết bị chọn cả NLS và AI, và thiếu Bảng Thiết bị / Phòng học ở Phụ lục 1

1. **Sửa hàm `suggestAiLessons`**:
   - **Nguyên nhân**: Hàm cũ viết `aiSelectedLessonIds = new Set(prioritizedAiPeriods().map(x=>x.id));` nên khi người dùng bấm nút "Gợi ý chọn tiết AI", nó chọn toàn bộ 140 tiết của cả năm học, làm bài nào cũng có AI.
   - **Cách sửa**:
     ```javascript
     function suggestAiLessons(){
       const countVal = Number(document.querySelector('#aiCountInput')?.value);
       if (countVal > 0) syncAiSelectionFromCount(countVal);
       else syncAiSelectionFromRate();
       notify(`Đã gợi ý chính xác ${selectedAiPeriodIds().size} tiết AI (${selectedAiLessons().length} bài) theo độ phù hợp sư phạm.`);
     }
     ```

2. **Quy ước bài 1 tiết chỉ có NLS hoặc AI (Ràng buộc loại trừ tuyệt đối)**:
   - **Nguyên tắc Sư phạm**: Bài 1 tiết chỉ có thời lượng 45 phút, không được ôm đồm cả NLS và AI. Nếu đã tích hợp NLS thì không tích hợp AI, và ngược lại.
   - **Cơ chế hoạt động**:
     - Khi chọn NLS cho bài 1 tiết: Hệ thống tự động xóa toàn bộ tiết AI của bài đó (`toggleAiLessonRow(lessonId, false)`).
     - Khi chọn AI cho bài 1 tiết: Hệ thống tự động bỏ tick NLS của bài đó (`nlsSelectedLessonIds.delete(lessonId)`).
     - Trong `canUseAiPeriod`: Bỏ qua các bài 1 tiết đã có trong `nlsSelectedLessonIds`.
     - Trong `canUseNlsLesson`: Bỏ qua các bài 1 tiết đã có tiết AI được chọn.
     - Trong bảng Mục 5 (`updateAiPicker`): Với bài 1 tiết, nếu đã tick NLS thì checkbox AI bị bỏ tick; nếu đã tick AI thì checkbox NLS bị bỏ tick. Tuyệt đối không cho phép 1 bài 1 tiết được tick cả hai.

3. **Bảo toàn hiển thị NLS trong cột Ghi chú Phụ lục 1**:
   - Khi bài 1 tiết được chọn NLS và không có AI, `getExpectedNlsCount(1, false, c)` trả về `1` $\rightarrow$ mã NLS được xuất đầy đủ vào cột Ghi chú (không còn bị rỗng hay chỉ xuất mã AI).

4. **Khôi phục Bảng Thiết bị (Mục 3) và Phòng học (Mục 4) của Phụ lục 1**:
   - Khi tệp PPCT tải lên không có bảng thiết bị/phòng học riêng, `normalizeAppendix` cho Phụ lục 1 phải tự động nạp thiết bị và phòng học chuẩn theo quy định CV 5512 từ `fallback('1', c)`:
     ```javascript
     data.devices = (sourceDevices.length ? sourceDevices : (Array.isArray(data.devices) && data.devices.length ? data.devices : fallback('1', c).devices)) || [];
     data.rooms = (sourceRooms.length ? sourceRooms : (Array.isArray(data.rooms) && data.rooms.length ? data.rooms : fallback('1', c).rooms)) || [];
     ```
   - Trong `data.schedule`: Đảm bảo mỗi dòng bài học đều có `devices` (nếu thiếu thì gán `defaultEquip`) và `location` (nếu thiếu thì gán `'Lớp học'`), giúp tiêu chí Thiết bị & địa điểm trong Thẩm định đạt 89/89 bài (100% Đạt).

### Bước 5: Thông báo Popup số tiết đã chọn / còn lại khi chọn bằng tay & Khóa chặn khi vượt quá hạn mức

1. **Yêu cầu & Hành vi người dùng**:
   - Khi giáo viên tick hoặc bỏ tick bằng tay ở bảng Mục 5 (cho cả NLS và AI):
     - Hiển thị popup toast thông báo tức thì: **Đã chọn bao nhiêu tiết / Mục tiêu bao nhiêu tiết / Còn lại bao nhiêu tiết**.
     - **Nếu vượt quá mục tiêu đã cài đặt**: Tuyệt đối **không cho chọn nữa**; tự động hoàn tác checkbox (bỏ tick ngay) và bật popup cảnh báo:
       `⚠️ Đã đạt giới hạn mục tiêu (X/Y tiết). Không thể chọn thêm bài này (Z tiết). Số tiết còn lại: 0.`

2. **Triển khai kỹ thuật**:
   - **Với NLS (`toggleNlsLesson(lessonId, checked, el)`)**:
     - Lấy số tiết của bài học `p = lesson.periodCount || validPeriodCount(...) || 1`.
     - Lấy số tiết mục tiêu: `target = Number(document.querySelector('#nlsCountInput')?.value) || Math.round((Number(document.querySelector('#nlsRate')?.value)||0)/100 * allocationTotals().totalPeriods)`.
     - Khi `checked === true`:
       - Nếu `target > 0 && currentCount + p > target`:
         - Revert checkbox: `if (el) el.checked = false;`
         - Bật toast cảnh báo: `⚠️ Đã đạt giới hạn: Đã chọn ${currentCount}/${target} tiết NLS. Không thể chọn thêm bài này (${p} tiết). Còn lại: ${Math.max(0, target - currentCount)} tiết.`
         - Kết thúc, không thêm vào `nlsSelectedLessonIds`.
       - Nếu hợp lệ:
         - Thêm vào `nlsSelectedLessonIds`.
         - Nếu là bài 1 tiết: tự động hủy AI của bài đó (`toggleAiLessonRow(lessonId, false)`).
         - Bật toast: `✓ Đã chọn NLS: ${afterCount}/${target||'∞'} tiết (${nlsSelectedLessonIds.size} bài). Còn lại: ${target > 0 ? Math.max(0, target - afterCount) : '—'} tiết.`
     - Khi `checked === false`:
       - Xóa khỏi `nlsSelectedLessonIds`.
       - Bật toast: `Đã bỏ chọn NLS bài này (-${p} tiết). Hiện tại: ${afterCount}/${target||'∞'} tiết. Còn lại: ${target > 0 ? Math.max(0, target - afterCount) : '—'} tiết.`

   - **Với AI (`toggleAiLesson(id, checked, el)` và `toggleAiLessonRow(lessonId, checked, el)`)**:
     - Lấy số tiết mục tiêu AI: `target = Number(document.querySelector('#aiCountInput')?.value) || Math.round((Number(document.querySelector('#aiRate')?.value)||0)/100 * allocationTotals().totalPeriods)`.
     - Khi `checked === true`:
       - Kiểm tra nếu `target > 0 && currentAiCount + addCount > target`:
         - Revert checkbox: `if (el) el.checked = false;`
         - Bật toast: `⚠️ Đã đạt giới hạn: Đã chọn ${currentAiCount}/${target} tiết AI. Không thể chọn thêm (${addCount} tiết). Còn lại: ${Math.max(0, target - currentAiCount)} tiết.`
         - Kết thúc, không thêm vào `aiSelectedLessonIds`.
       - Nếu hợp lệ:
         - Nếu là bài 1 tiết: tự động bỏ tick NLS của bài đó (`nlsSelectedLessonIds.delete(lessonId)`).
         - Thêm vào `aiSelectedLessonIds`.
         - Bật toast: `✓ Đã chọn AI: ${afterCount}/${target||'∞'} tiết. Còn lại: ${target > 0 ? Math.max(0, target - afterCount) : '—'} tiết.`
     - Khi `checked === false`:
       - Xóa khỏi `aiSelectedLessonIds`.
       - Bật toast: `Đã bỏ chọn tiết AI. Hiện tại: ${afterCount}/${target||'∞'} tiết. Còn lại: ${target > 0 ? Math.max(0, target - afterCount) : '—'} tiết.`

   - Trong template HTML của `updateAiPicker`:
     Truyền tham chiếu `this` vào các hàm:
     `onchange="toggleNlsLesson('${row.id}',this.checked,this)"`
     `onchange="toggleAiLessonRow('${row.id}',this.checked,this)"`
     `onchange="toggleAiLesson('${x.id}',this.checked,this)"`

3. **Đồng bộ**: Áp dụng đồng thời trên `canvas_xaydungphuluc.html`, `xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html`.

---

## 3. Tiêu chí nghiệm thu (Verification Criteria)
1. **Chọn tay NLS**:
   - Khi tick bài học: Popup hiển thị rõ số tiết đã chọn và số tiết còn lại theo mục tiêu.
   - Khi tổng số tiết cộng dồn vượt quá số tiết mục tiêu (ví dụ quá 28 tiết): Checkbox tự bỏ tick và hiện cảnh báo không cho chọn tiếp.
2. **Chọn tay AI**:
   - Khi tick tiết AI: Popup hiển thị số tiết đã chọn và số tiết còn lại.
   - Khi vượt quá hạn mức AI đã cài đặt: Checkbox tự bỏ tick và hiện thông báo khóa chặn.
3. **Quy ước bài 1 tiết**: Tuyệt đối không bài 1 tiết nào được chọn đồng thời cả NLS và AI.
4. **Báo cáo Thẩm định Sư phạm**: Đạt chuẩn 100% tất cả các tiêu chí.
5. Chạy smoke test `tests/canvas-xaydungphuluc-smoke.js` và `tests/xaydungphuluc-smoke.js` đạt PASS 100%.

