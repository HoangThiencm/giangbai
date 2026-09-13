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

### Bước 2: Chuẩn hóa thuật toán Knapsack Tối ưu Sư phạm & Tuyệt đối đúng số tiết đã chọn
1. Tại `canvas_xaydungphuluc.html`:
   - Bổ sung sự kiện `input` trên `#nlsCountInput`:
     ```javascript
     document.querySelector('#nlsCountInput')?.addEventListener('input', e => syncNlsSelectionFromCount(e.target.value));
     ```
   - Nâng cấp hàm `chooseNlsLessonsForPeriods(target)` bằng giải thuật Quy hoạch động Knapsack tối ưu điểm sư phạm (`score` từ `nlsLessonPriorityScore`):
     ```javascript
     function chooseNlsLessonsForPeriods(target, candidates = nlsCandidates()){
       const targetNum = Number(target) || 0;
       if (targetNum <= 0) return new Set();
       const eligible = candidates.filter(item => !item.isHeader && item.lesson);
       
       // dp[w] lưu { score: tổng_điểm_sư_phạm, ids: [danh_sách_id] }
       const dp = new Map();
       dp.set(0, { score: 0, ids: [] });

       for (const item of eligible){
         const p = item.periodCount || validPeriodCount(item.periods, item.tietCT) || 1;
         const s = typeof nlsLessonPriorityScore === 'function' ? nlsLessonPriorityScore(item.lesson) : 5;
         const currentEntries = [...dp.entries()];
         for (const [w, state] of currentEntries){
           const nextW = w + p;
           if (nextW <= targetNum){
             const nextScore = state.score + s;
             if (!dp.has(nextW) || dp.get(nextW).score < nextScore){
               dp.set(nextW, { score: nextScore, ids: [...state.ids, item.id] });
             }
           }
         }
       }

       // Ưu tiên cao nhất: Tìm đúng tổ hợp có tổng số tiết = targetNum và điểm sư phạm cao nhất
       if (dp.has(targetNum)) return new Set(dp.get(targetNum).ids);

       // Nếu không có cách ghép chính xác bằng targetNum, lấy tổ hợp có tổng tiết gần nhất (<= targetNum) với điểm sư phạm cao nhất
       const bestWeight = [...dp.keys()].reduce((max, w) => w > max ? w : max, 0);
       return new Set(dp.get(bestWeight)?.ids || []);
     }
     ```
   - Hàm `suggestNlsLessons()`:
     ```javascript
     function suggestNlsLessons(){
       const countVal = Number(document.querySelector('#nlsCountInput')?.value);
       if (countVal > 0) {
         syncNlsSelectionFromCount(countVal);
       } else {
         syncNlsSelectionFromRate();
       }
       notify(`Đã gợi ý chính xác ${nlsSelectedPeriodCount()} tiết NLS (${nlsSelectedLessonIds.size} bài) theo độ phù hợp sư phạm.`);
     }
     ```

### Bước 3: Đồng bộ 100% Phụ lục 3 từ Phụ lục 1 / File Nguồn PPCT
1. Khi sinh nội dung Phụ lục 3 trong `generateSelected` và `normalizeAppendix`:
   - Bảng I của Phụ lục 3 kế thừa 100% từ cấu trúc nguồn PPCT / Phụ lục 1 (`sourcePpctRows` hoặc `results['1']?.schedule`):
     - Dòng `isHeader === true`: Giữ nguyên dòng tiêu đề (`lesson: row.lesson`, `isHeader: true`).
     - Dòng bài học: Giữ nguyên `lesson`, `periods`, `tietCT`, `week`, `devices`, `location`.
     - Cột `Ghi chú`: Đồng bộ từ cột Ghi chú của Phụ lục 1 (hoặc hàm `formatNoteIntegration`).
2. Hàm `appendixThreeTable`:
   - Trả về cấu trúc 7 cột chuẩn: `['Bài học', 'Số tiết', 'Tiết CT', 'Tuần', 'Thiết bị dạy học (*)', 'Địa điểm dạy học (**)', 'Ghi chú']`.
   - Dòng `row.isHeader`: Trả về `{isHeader: true, cells: [row.lesson]}`.
   - Dòng bài học: Trả về `[row.lesson, row.periods, row.tietCT, row.week, row.devices, row.location, note || '-']`.
3. Xuất Word trong `exportDocx`:
   - Hàm `addPpct` khi gặp dòng `row.isHeader` xuất ra ô merge toàn bộ bảng `colspan="7"`, căn giữa, in đậm:
     ```javascript
     if (row.isHeader) {
       return new TableRow({
         cantSplit: true,
         children: [cell((row.cells || []).filter(Boolean).join(' '), { center: true, bold: true, colspan: columns.length, width: 100 })]
       });
     }
     ```
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
