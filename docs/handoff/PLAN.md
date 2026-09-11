# PLAN: Cấu hình Năng Lực Số (CV 3456) theo Tỉ trọng & Cho phép Người dùng Tự chọn Bài/Tiết Tích hợp

## 1. Hiện trạng & Phân tích Nguyên nhân

### Hiện trạng thực tế
- Người dùng phản ánh đúng thực tế sư phạm: **"Không phải tiết nào cũng tích hợp năng lực số mà là chỉ chiếm tỉ trọng thôi, do người dùng chọn"**.
- Theo chương trình GDPT 2018 và hướng dẫn thực hiện CV 5512, CV 3456, TT 02/2025:
  + Môn học (như Toán THCS với 105–140 tiết/năm) có rất nhiều dạng bài: hình thành kiến thức mới, luyện tập bảng phấn, kiểm tra định kỳ (GK1, CK1, GK2, CK2), ôn tập cuối chương...
  + Năng lực số (NLS) chỉ nên tích hợp vào **các bài/tiết thực sự có điều kiện và học liệu số phù hợp** (vẽ hình GeoGebra, máy tính cầm tay, bảng tính Excel, mô phỏng số, biểu đồ thống kê, bài thực hành trải nghiệm, bài có AI...).
  + Do đó, NLS chỉ nên chiếm một **TỈ TRỌNG** nhất định (ví dụ 30%, 40%, 50% tổng số bài/tiết), và giáo viên / tổ chuyên môn được quyền **TỰ CHỌN** bài/tiết nào tích hợp.

### Lỗi thiết kế hiện tại trong Mã nguồn
1. **Trong Xây dựng Phụ lục (`xaydungphuluc.html` & `canvas_xaydungphuluc.html`)**:
   - Giao diện **đã có sẵn** thanh trượt tỉ trọng `#nlsRate` (0%–100%, mặc định 50%) và checkbox `#nlsEnabled`.
   - **Tuy nhiên, trong code xử lý (`selectedIntegration` và `fallbackNlsCodes`)**:
     Hàm `selectedIntegration` (dòng 1456) gọi `fallbackNlsCodes` một cách **vô điều kiện cho 100% tất cả các dòng bài học**.
     Dù người dùng kéo `#nlsRate` về 30% hay 50%, thì **100% bài học đều bị nhét mã NLS**! Không có bài nào được để trống hay ghi `-`.
   - Trong khi phần AI có cơ chế chọn tiết rất rõ ràng (`aiLessonPickerCard`, `aiSelectedLessonIds`, `syncAiSelectionFromRate`), phần NLS **chưa có cơ chế chọn bài/tiết** (`nlsSelectedLessonIds`), khiến người dùng không thể chủ động tick chọn bài nào tích hợp NLS.
2. **Trong Soạn KHBD (`soankhbd.html`, `canvas_soankhbd.html`, `js/khbd-app.js`)**:
   - `normalizeTeachingContext` (dòng 656) đang gán cứng `digital: true` làm giá trị mặc định không thể tắt sạch.
   - Nút đề xuất Bước 3 (`triggerStep3PedagogyAndDigitalRecommendations`, dòng 2244) tự động ép `toggleDigital.checked = true` và `integrations.digital = true`, không tôn trọng việc giáo viên đã chủ động tắt NLS cho bài này.

---

## 2. Giải pháp Kiến trúc Chi tiết

### Mục tiêu
1. **Tỉ trọng NLS thực chất (`nlsRate`)**:
   - Thanh trượt `nlsRate` (ví dụ 40%) sẽ xác định chính xác số lượng bài học cần tích hợp NLS:
     $$K = \text{round}\left(\frac{\text{nlsRate}}{100} \times \text{Tổng số bài}\right)$$
   - Chỉ đúng $K$ bài học được chọn mới có mã NLS. Các bài còn lại **không có mã NLS** (cột NLS ghi `-`).
2. **Người dùng được quyền tự chọn ("do người dùng chọn")**:
   - **Tự động gợi ý theo tỉ trọng**: Hệ thống xếp hạng ưu tiên sư phạm của các bài (bài có GeoGebra, máy tính cầm tay, Excel, STEM, AI đứng đầu; bài ôn tập, kiểm tra đứng cuối) và tự động chọn $K$ bài tối ưu nhất.
   - **Chủ động tick chọn tay**: Trong bảng danh mục bài học, người dùng có thể tick / bỏ tick checkbox NLS cho từng bài học theo đúng ý đồ của mình.
   - Có nút **"💻 Gợi ý NLS theo tỉ trọng"** và **"✕ Bỏ chọn NLS"**.
3. **Đồng bộ 100% giữa Phụ lục 1 và Phụ lục 3**:
   - Cột NLS ở Phụ lục 1 (Kế hoạch Tổ) và Phụ lục 3 (Kế hoạch Giáo viên) hoàn toàn khớp nhau: bài nào có NLS thì cả 2 cùng có; bài nào không tích hợp thì cả 2 cùng ghi `-`.
4. **Tôn trọng quyền bật/tắt trong Soạn KHBD (`soankhbd.html`)**:
   - `toggleDigitalCompetency` không bị ép bật `true`.
   - Nếu bài học trong PPCT không có NLS (ghi `-`), hệ thống tự động tắt công tắc NLS khi soạn bài đó.

---

## 3. Chi tiết các Bước Triển khai (Dành cho ChatGPT thực hiện)

### Bước 1: Xây dựng Cơ chế Quản lý Bài học NLS trong `canvas_xaydungphuluc.html` & `xaydungphuluc.html`

1. **Khai báo biến trạng thái tập bài chọn NLS**:
   ```javascript
   let nlsSelectedLessonIds = new Set();
   ```

2. **Hàm tính toán danh sách bài ứng viên và độ ưu tiên sư phạm cho NLS**:
   ```javascript
   function nlsCandidates() {
     return aiCandidates(); // Danh sách các bài học hợp lệ từ PPCT (không tính header, kiểm tra)
   }

   function prioritizedNlsLessons() {
     // Đánh giá điểm ưu tiên sư phạm công nghệ số của bài học môn học
     const candidates = nlsCandidates();
     const scoreLesson = (lessonName) => {
       const text = foldText(cleanLessonDescription(lessonName));
       let score = 5;
       if (/hinh hoc|tam giac|tu giac|duong tron|goc|doi xung|dong dang|dinh ly|thales|pythagore|lang tru|hinh hop/.test(text)) score += 5; // GeoGebra
       if (/thong ke|xac suat|bieu do|bang so lieu|du lieu|tan suat/.test(text)) score += 5; // Bảng tính Excel
       if (/thuc hanh va trai nghiem|trai nghiem|du an|stem/.test(text)) score += 4; // STEM / Thực hành
       if (/ham so|do thi|parabol|toa do/.test(text)) score += 4; // Vẽ đồ thị
       if (/phuong trinh|he phuong trinh|bat phuong trinh|nghiem|giai he/.test(text)) score += 3; // Máy tính Casio
       if (selectedAiLessons().some(l => l.includes(lessonName))) score += 2; // Bài có AI
       if (/on tap|kiem tra|danh gia|giua ky|cuoi ky/.test(text)) score -= 6; // Không ưu tiên NLS
       return score;
     };
     return [...candidates].sort((a, b) => scoreLesson(b.lesson) - scoreLesson(a.lesson));
   }
   ```

3. **Đồng bộ giữa Thanh trượt `nlsRate` và Tập bài được chọn**:
   ```javascript
   function syncNlsRateFromSelection() {
     const total = nlsCandidates().length;
     const selectedCount = nlsSelectedLessonIds.size;
     const rate = total ? Math.round(selectedCount / total * 100) : 0;
     const nlsRateEl = document.querySelector('#nlsRate');
     const nlsRateOutEl = document.querySelector('#nlsRateOut');
     if (nlsRateEl) nlsRateEl.value = String(rate);
     if (nlsRateOutEl) nlsRateOutEl.value = `${rate}% (${selectedCount}/${total} bài)`;
     return rate;
   }

   function syncNlsSelectionFromRate() {
     const total = nlsCandidates().length;
     const rate = Number(document.querySelector('#nlsRate')?.value) || 0;
     const targetCount = Math.round(rate / 100 * total);
     const prioritized = prioritizedNlsLessons();
     nlsSelectedLessonIds = new Set(prioritized.slice(0, targetCount).map(x => x.id));
     syncNlsRateFromSelection();
     updateAiPicker(); // Cập nhật lại giao diện bảng tick chọn
   }
   ```

4. **Cho phép người dùng tick/bỏ tick NLS từng bài**:
   ```javascript
   function toggleNlsLesson(lessonId, checked) {
     if (checked) nlsSelectedLessonIds.add(lessonId);
     else nlsSelectedLessonIds.delete(lessonId);
     syncNlsRateFromSelection();
     updateAiPicker();
   }

   function suggestNlsLessons() {
     syncNlsSelectionFromRate();
     notify(`Đã gợi ý ${nlsSelectedLessonIds.size} bài học tích hợp NLS theo tỉ trọng.`);
   }

   function clearNlsLessons() {
     nlsSelectedLessonIds.clear();
     syncNlsRateFromSelection();
     updateAiPicker();
     notify('Đã bỏ chọn tất cả bài học NLS.');
   }
   ```

---

### Bước 2: Nâng cấp Giao diện Bảng Phân phối / Chọn tiết trong `canvas_xaydungphuluc.html` & `xaydungphuluc.html`

1. **Cập nhật tiêu đề Card Mục 4**:
   Đổi từ:
   `4. Chọn chính xác tiết tích hợp AI`
   Thành:
   `4. Chọn chính xác bài tích hợp NLS & tiết tích hợp AI (Do người dùng quyết định)`
2. **Thêm nút điều khiển NLS trên thanh công cụ**:
   - Nút `💻 Gợi ý NLS theo tỉ trọng` (`onclick="suggestNlsLessons()"`)
   - Nút `✕ Bỏ NLS` (`onclick="clearNlsLessons()"`)
   - Huy hiệu thống kê: `📊 NLS: ${nlsSelectedLessonIds.size}/${total} bài (${nlsRate}%) · 🎯 AI: ${aiSelected.size}/${limit} tiết`
3. **Thêm cột checkbox NLS trong bảng `updateAiPicker()`**:
   - Thêm cột `<th>Tích hợp NLS (CV 3456)</th>` trước hoặc sau cột AI.
   - Mỗi dòng hiển thị:
     `<label class="font-semibold whitespace-nowrap"><input type="checkbox" ${nlsSelectedLessonIds.has(row.id)?'checked':''} onchange="toggleNlsLesson('${row.id}', this.checked)"> Tích hợp NLS</label>`

---

### Bước 3: Nâng cấp hàm `selectedIntegration` & `separateIntegration`

1. **Kiểm tra điều kiện xuất NLS theo lựa chọn của người dùng**:
   ```javascript
   function isLessonNlsSelected(lessonId, lessonName, c) {
     if (!c?.nls?.enabled) return false;
     // Nếu người dùng có danh sách chọn cụ thể
     if (typeof nlsSelectedLessonIds !== 'undefined' && nlsSelectedLessonIds.size > 0) {
       if (lessonId && nlsSelectedLessonIds.has(lessonId)) return true;
       if (lessonName) {
         const match = nlsCandidates().find(x => typeof lessonsMatch === 'function' ? lessonsMatch(x.lesson, lessonName) : x.lesson === lessonName);
         if (match && nlsSelectedLessonIds.has(match.id)) return true;
       }
       return false;
     }
     // Fallback nếu chưa khởi tạo bảng chọn: dựa theo tỉ trọng nlsRate
     const rate = Number(c?.nls?.rate ?? 50);
     if (rate <= 0) return false;
     if (rate >= 100) return true;
     const prioritized = typeof prioritizedNlsLessons === 'function' ? prioritizedNlsLessons() : [];
     const targetCount = Math.round(rate / 100 * prioritized.length);
     const topIds = new Set(prioritized.slice(0, targetCount).map(x => x.id));
     if (lessonId && topIds.has(lessonId)) return true;
     return false;
   }
   ```
2. **Áp dụng vào `selectedIntegration`**:
   - Nếu `!isLessonNlsSelected(rowId, lesson, c)`:
     `cleanNls = []` (Tuyệt đối không sinh mã NLS cho bài này).
   - Nếu `cleanNls.length === 0 && !hasAi`:
     Trả về `'-'`!
3. **Áp dụng vào `separateIntegration`**:
   - Dòng bài không có NLS: `nlsText = '-'`.
   - Dòng bài có NLS: `nlsText = cleanNlsColumnText(...)`.

---

### Bước 4: Chuẩn hóa `normalizeTeachingContext` & Đề xuất trong `js/khbd-app.js`

1. Trong `normalizeTeachingContext`:
   ```javascript
   const mergedIntegrations = Object.assign({
     digital: integrations.digital !== undefined ? Boolean(integrations.digital) : true,
     ai: Boolean(integrations.ai),
     foreignLanguage: Boolean(integrations.foreignLanguage),
     inclusive: Boolean(integrations.inclusive)
   }, Object.fromEntries(SUBJECT_CONTEXT_INTEGRATIONS.map(item => [item.id, Boolean(integrations[item.id])])));
   ```
2. Trong `triggerStep3PedagogyAndDigitalRecommendations`:
   Không cưỡng ép `toggleDigital.checked = true` nếu người dùng đã chủ động tắt NLS cho bài này:
   ```javascript
   const toggleDigital = document.getElementById("toggleDigitalCompetency");
   const isDigitalActive = toggleDigital ? toggleDigital.checked : Boolean(appState.teachingContext?.integrations?.digital);
   appState.teachingContext.integrations.digital = isDigitalActive;
   ```
3. Khi nhận diện từ PPCT (`applyPpctDetectedStandards`):
   Nếu bài học trong PPCT không có NLS (ghi `-` hoặc không chứa mã NLS), giữ `toggleDigitalCompetency.checked = false` và không nạp mã NLS.

---

## 4. Danh sách File Tác động

1. `xaydungphuluc.html` (Thêm cơ chế chọn bài NLS, slider có hiệu lực thực, checkbox NLS từng hàng).
2. `canvas_xaydungphuluc.html` (Đồng bộ 1-1 với xaydungphuluc.html cho Google Canvas).
3. `backupcode viettailieu/canvas_xaydungphuluc.html` (Đồng bộ bản backup mirror).
4. `js/khbd-app.js` (Tôn trọng trạng thái bật/tắt NLS do người dùng chọn, không ép cứng `digital: true`).
5. `tests/khbd-nls-rate-smoke.js` (Tạo mới smoke test kiểm thử tỉ trọng NLS).
6. `tests/xaydungphuluc-smoke.js` & `tests/canvas-xaydungphuluc-smoke.js` (Cập nhật kiểm thử).
7. `docs/handoff/IMPLEMENT.md` (ChatGPT ghi nhận triển khai).
8. `docs/handoff/VERIFY.md` (Antigravity thực hiện `/verify` nghiệm thu).

---

## 5. Kế hoạch Kiểm thử & Thẩm định (Verification Plan)

### Automated Tests
Tạo bài test `tests/khbd-nls-rate-smoke.js`:
1. **Case 1 (Tỉ trọng 0%)**: Khi `nlsRate = 0%` hoặc `nlsEnabled = false` -> 100% các dòng bài học trong Phụ lục 1 và 3 đều có cột NLS ghi `-`.
2. **Case 2 (Tỉ trọng 50%)**: Khi `nlsRate = 50%` -> Số bài có mã NLS đạt đúng xấp xỉ 50%, các bài còn lại ghi `-`.
3. **Case 3 (Chọn bài thủ công)**: Khi người dùng tick chọn 3 bài cụ thể trong `nlsSelectedLessonIds` -> Đúng 3 bài đó có mã NLS, tất cả các bài khác ghi `-`.
4. **Case 4 (Ưu tiên Sư phạm)**: Các bài Hình học (GeoGebra) và Thống kê (Excel) được ưu tiên chọn NLS trước các bài lý thuyết, kiểm tra.
5. **Case 5 (Đồng bộ PL1 & PL3)**: Phụ lục 1 và Phụ lục 3 khớp 100% cột NLS theo từng bài.
6. **Case 6 (Soạn KHBD)**: Tắt `toggleDigitalCompetency` thì giáo án không sinh mục tiêu NLS.

### Lệnh chạy kiểm thử:
```powershell
& "C:\Users\HoangThien\AppData\Local\OpenAI\Codex\runtimes\cua_node\b474a88d5d105afa\bin\node.exe" tests/khbd-nls-rate-smoke.js
& "C:\Users\HoangThien\AppData\Local\OpenAI\Codex\runtimes\cua_node\b474a88d5d105afa\bin\node.exe" tests/xaydungphuluc-smoke.js
& "C:\Users\HoangThien\AppData\Local\OpenAI\Codex\runtimes\cua_node\b474a88d5d105afa\bin\node.exe" tests/canvas-xaydungphuluc-smoke.js
```
