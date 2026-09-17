# PLAN: Ngăn Chặn Tự Động Chọn Lại & Loại Bỏ PPDH / KTDH Khi Người Dùng Bỏ Tick (Chế Độ Soạn Rút Gọn `canvas_soankhbd`)

## User Review Required
> [!IMPORTANT]
> - Khi người dùng chủ động bỏ tick toàn bộ PPDH hoặc KTDH theo pha: Hệ thống tôn trọng tuyệt đối lựa chọn này, không tự động khôi phục lại khi bấm soạn bài.
> - Khi muốn hệ thống tự động đề xuất lại, người dùng chỉ cần bấm nút "⚡ Đề xuất PPDH & NLS" tại Bước 2/Khối 3.

---

## I. Hiện Trạng & Phân Tích Nguyên Nhân

### 1. Hiện tượng người dùng phản ánh
- Tại giao diện `canvas_soankhbd.html` (đặc biệt khi chuyển sang **Chế độ Soạn rút gọn 4–6 trang**):
  - Người dùng vào **Tab 0 -> Khối 3 (PPDH, Năng lực số & Môn)** và chủ động **bỏ tick** các kỹ thuật dạy học (KTDH) và phương pháp dạy học (PPDH),... vì muốn giáo án tinh gọn, dạy học trực tiếp/vấn đáp cơ bản, không cần các kỹ thuật phức tạp.
  - Tuy nhiên, khi bấm soạn bài (ví dụ nút **⚡ TẠO TOÀN BỘ GIÁO ÁN (1-CLICK)** hoặc các nút **Tạo Mục tiêu / Tạo Hoạt động**), hệ thống **tự động tick lại** các kỹ thuật/phương pháp này trên giao diện và trong dữ liệu.
  - Kết quả giáo án sinh ra vẫn bị AI ép tên các kỹ thuật dạy học (như *Think-Pair-Share*, *Khăn trải bàn*...) và PPDH vào tiến trình lớp học, đi ngược lại chủ ý tinh giản của người dùng.

---

### 2. Nguyên nhân kỹ thuật cốt lõi

#### Nguyên nhân 1: `ensurePedagogyFromLesson` ghi đè mảng rỗng (`js/khbd-app.js` dòng 2424–2458)
- Khi người dùng bỏ tick toàn bộ PPDH hoặc KTDH ở một pha (A, B, C, D), `appState.teachingContext.methods` hoặc `appState.teachingContext.phasePedagogy[phase].techniques` trở thành mảng rỗng `[]` (`length === 0`).
- Ở đầu mọi hành động sinh AI, hàm `getGenerationPromptContext()` (dòng 5273) được gọi và tự động chạy:
  ```javascript
  if (hasAnalyzedLessonContent()) {
    ensurePedagogyFromLesson({ silent: true });
    ensureIntegrationStandards({ silent: true });
  }
  ```
- Hàm `ensurePedagogyFromLesson` kiểm tra:
  ```javascript
  if (force || !(appState.teachingContext.methods || []).length) {
    appState.teachingContext.methods = rec.methods; // GHI ĐÈ LẠI MẶC ĐỊNH
    ...
  }
  ["A", "B", "C", "D"].forEach(phase => {
    const current = appState.teachingContext.phasePedagogy[phase]?.techniques || [];
    if (force || !current.length) {
      appState.teachingContext.phasePedagogy[phase].techniques = rec.techniques[phase] || []; // GHI ĐÈ LẠI KỸ THUẬT
      ...
    }
  });
  ```
- Vì `length === 0`, hàm này nhầm tưởng là "chưa từng khởi tạo PPDH" và tự động nhồi `rec.methods` và `rec.techniques[phase]` trở lại, làm mất lựa chọn bỏ tick của người dùng.

#### Nguyên nhân 2: Ép cứng fallback `"tps-tech"` trong `applyTimeBudgetGateToPedagogy` & `applyGate`
- Trong `js/khbd-app.js` (dòng 2336–2338) và inline script của `canvas_soankhbd.html` (dòng 1475–1478):
  ```javascript
  const currentB = (rec.techniques.B || []).filter(id => !isHeavyPedagogyId(id));
  const chosenB = KHBD_LIGHT_B_TECHNIQUES.find(id => currentB.includes(id)) || currentB[0] || "tps-tech";
  rec.techniques.B = chosenB && !isHeavyPedagogyId(chosenB) ? [chosenB] : ["tps-tech"];
  ```
  Fallback `|| "tps-tech"` khiến cho ngay cả khi `currentB` rỗng (người dùng đã bỏ tick hết ở pha B), hệ thống vẫn cưỡng ép `rec.techniques.B = ["tps-tech"]`!
- Thêm vào đó, trong `canvas_soankhbd.html`, `pruneAppState` và `pruneUi` bọc lấy các hàm render và applyGate, dẫn đến việc checkbox *Think-Pair-Share* bị tick lại trên DOM.

#### Nguyên nhân 3: Chỉ thị Prompt cưỡng ép AI tự chọn khi danh sách rỗng
- Trong `js/khbd-app.js` (`buildPedagogicalContext()`, dòng 5173–5175):
  ```javascript
  - Phương pháp dạy học được chọn: ${methodLabels.length ? methodLabels.join("; ") : `Chưa chọn; khi soạn chỉ được lấy 1–2 phương pháp phù hợp môn ${subjectName} lớp ${appState.selectedGrade} từ catalog...`}
  - Kỹ thuật dạy học theo pha: ${techniqueByPhase.length ? techniqueByPhase.join(" | ") : "Chưa chọn; chỉ dùng kỹ thuật catalog đúng pha A–E phù hợp môn/lớp, đúng nhãn."}
  ```
  Nếu danh sách rỗng, prompt lại ra lệnh cho AI: *"Chưa chọn; khi soạn chỉ được lấy 1–2 phương pháp... / chỉ dùng kỹ thuật catalog..."* — khiến AI bắt buộc phải tự thêm PPDH và KTDH vào giáo án!
- Trong `js/khbd-app.js` (`buildPhasePedagogyContext()`, dòng 5451–5454):
  Khi pha không có kỹ thuật nào, prompt chưa có chỉ thị cấm đưa kỹ thuật vào bài dạy.

#### Nguyên nhân 4: Ràng buộc trong Prompt mẫu (`js/khbd-prompts.js`)
- `ACTIVITY_TABLE_CONTRACT_COMPACT` chưa có điều khoản cấm gán KTDH / PPDH khi người dùng không chọn ở chế độ rút gọn.
- Các template hoạt động `GENERATE_ACTIVITY_B`, `GENERATE_ACTIVITY_C`, `GENERATE_ACTIVITY_D` (dòng 745, 811, 865) chứa các chỉ thị áp đặt: `+ Nêu rõ tên Kỹ thuật dạy học...`, `+ Áp dụng Kỹ thuật dạy học...`.

---

## II. Kế Hoạch Triển Khai Chi Tiết

### Module 1: Bảo Lưu Quyết Định Bỏ Tick Của Người Dùng (`js/khbd-app.js`)

1. **Khởi tạo và lưu trạng thái can thiệp của người dùng (`pedagogyConfigured`)**:
   - Trong hàm `normalizeTeachingContext(context)` (dòng ~817):
     ```javascript
     pedagogyConfigured: Boolean(source.pedagogyConfigured),
     ```
   - Trong các bộ lắng nghe sự kiện thay đổi checkbox:
     - `methodsPanel.querySelectorAll(".pedagogy-method")` (dòng ~1022): khi user click change, gán `appState.teachingContext.pedagogyConfigured = true;`.
     - `techPanel.querySelectorAll(".pedagogy-technique")` (dòng ~1043): khi user click change, gán `appState.teachingContext.pedagogyConfigured = true;`.
     - `actPanel.querySelectorAll(".pedagogy-activity")` (dòng ~1057): khi user click change, gán `appState.teachingContext.pedagogyConfigured = true;`.
   - Khi người dùng chủ động bấm nút đề xuất lại PPDH (`btnStep3PedagogyDigital` hoặc `btnSuggestPedagogyStandards`): hàm gọi `ensurePedagogyFromLesson({ force: true })`, cho phép ghi đè và cập nhật lại.

2. **Cập nhật `ensurePedagogyFromLesson` (dòng ~2424–2458)**:
   - Thêm điều kiện kiểm tra `pedagogyConfigured`:
     ```javascript
     const userConfigured = Boolean(appState.teachingContext?.pedagogyConfigured);
     ```
   - Khi `!force && userConfigured`: TUYỆT ĐỐI KHÔNG tự động gán `rec.methods`, `rec.techniques`, hay `rec.activities` nếu người dùng đã để mảng rỗng (`length === 0`).
   - Chỉ tự động gợi ý (`rec.methods`, `rec.techniques`, `rec.activities`) khi người dùng **chưa từng can thiệp cấu hình** (`!userConfigured`) hoặc khi bấm nút đề xuất (`force: true`).

3. **Loại bỏ cưỡng ép fallback `"tps-tech"` trong `applyTimeBudgetGateToPedagogy` (dòng ~2336–2338)**:
   - Sửa logic chọn kỹ thuật pha B cho bài 1 tiết / rút gọn:
     ```javascript
     const currentB = (rec.techniques.B || []).filter(id => !isHeavyPedagogyId(id));
     const chosenB = KHBD_LIGHT_B_TECHNIQUES.find(id => currentB.includes(id)) || currentB[0] || null;
     rec.techniques.B = chosenB && !isHeavyPedagogyId(chosenB) ? [chosenB] : [];
     ```
   - Nếu `currentB` rỗng (người dùng đã bỏ chọn hết ở pha B), `rec.techniques.B` phải giữ nguyên là mảng rỗng `[]`, không được tự ý chèn `"tps-tech"`.

---

### Module 2: Đồng Bộ Logic Gate & UI Trong `canvas_soankhbd.html` & Bản Backup

1. **Cập nhật `canvasTimeBudgetAndRoleBreaks` trong `canvas_soankhbd.html` & `backupcode viettailieu/canvas_soankhbd.html`**:
   - Sửa hàm `applyGate(rec, periodsHint)` (dòng ~1475–1478):
     ```javascript
     var currentB = (rec.techniques.B || []).filter(function (id) { return !HEAVY.test(String(id)); });
     var chosenB = LIGHT_B.filter(function (id) { return currentB.indexOf(id) !== -1; })[0] || currentB[0] || "";
     rec.techniques.B = chosenB ? [chosenB] : [];
     ```
     Loại bỏ hoàn toàn fallback `"tps-tech"`.
   - Trong `pruneUi()`: Nếu người dùng đã bỏ tick (không có KTDH nào trong pha B), không được tự ý tìm và tick lại bất kỳ checkbox nào.

2. **Truyền chế độ soạn đúng đắn vào context**:
   - Trong `handle1ClickGenerate` và các hàm gọi tạo bài:
     Đảm bảo `context = getGenerationPromptContext({ generationMode: isCompact ? 'compact' : 'detailed' })` được áp dụng nhất quán.

---

### Module 3: Chuẩn Hóa Chỉ Thị Prompt Khi Không Chọn PPDH/KTDH (`js/khbd-app.js` & `js/khbd-prompts.js`)

1. **Cập nhật `buildPedagogicalContext()` (`js/khbd-app.js` dòng ~5173–5175)**:
   - Sửa đổi khi `methodLabels.length === 0`:
     ```javascript
     - Phương pháp dạy học: KHÔNG áp dụng PPDH đặc thù riêng (người dùng không chọn hoặc đã bỏ tick). Sử dụng phương pháp dạy học thông thường, trực tiếp, vấn đáp gợi mở và luyện tập thực hành cơ bản. TUYỆT ĐỐI CẤM tự ý đưa tên PPDH ngoài danh mục hoặc gán PPDH phức tạp vào giáo án.
     ```
   - Sửa đổi khi `techniqueByPhase.length === 0`:
     ```javascript
     - Kỹ thuật dạy học: KHÔNG áp dụng kỹ thuật dạy học riêng nào (người dùng không chọn hoặc đã bỏ tick). Tiến trình dạy học diễn ra tự nhiên theo 4 bước chuẩn mực CV 5512 (giao nhiệm vụ, thực hiện, báo cáo, kết luận); TUYỆT ĐỐI KHÔNG tự ý đưa tên bất kỳ kỹ thuật dạy học nào (như Think-Pair-Share, Khăn trải bàn, Mảnh ghép, Trạm,...) vào bài dạy.
     ```
   - Sửa đổi khi `activityLabels.length === 0`:
     ```javascript
     - Hoạt động đặc thù môn học: Không chọn hoạt động đặc thù riêng.
     ```

2. **Cập nhật `buildPhasePedagogyContext(phase)` (`js/khbd-app.js` dòng ~5451–5454)**:
   - Khi pha đó không có KTDH nào (`techItems.length === 0`):
     - Không chèn kịch bản KTDH từ `buildDetailedPedagogyGuide`.
     - Xuất chỉ thị rõ ràng:
       ```javascript
       RÀNG BUỘC PHA ${phase}: Người dùng KHÔNG chọn kỹ thuật dạy học cho pha này. Tiến trình thực hiện theo các bước sư phạm trực tiếp tự nhiên, TUYỆT ĐỐI CẤM ghi tên bất kỳ kỹ thuật dạy học nào.
       ```

3. **Cập nhật `ACTIVITY_TABLE_CONTRACT_COMPACT` (`js/khbd-prompts.js` dòng ~344–350)**:
   - Bổ sung quy tắc bắt buộc cho chế độ soạn rút gọn:
     ```text
     - KỸ THUẬT & PHƯƠNG PHÁP DẠY HỌC: Ở chế độ soạn rút gọn, nếu trong bối cảnh sư phạm không có kỹ thuật dạy học hoặc phương pháp dạy học được chọn (người dùng đã bỏ tick), TUYỆT ĐỐI KHÔNG đưa tên kỹ thuật dạy học (như Think-Pair-Share, Khăn trải bàn, Mảnh ghép, Trạm,...) hay tên PPDH vào tiến trình; chỉ triển khai tiến trình 4 bước chuẩn CV 5512 trực tiếp, tinh gọn.
     ```

4. **Cập nhật template `GENERATE_ACTIVITY_B`, `GENERATE_ACTIVITY_C`, `GENERATE_ACTIVITY_D` (`js/khbd-prompts.js`)**:
   - Dòng ~745 (`GENERATE_ACTIVITY_B`): Thay `+ Nêu rõ tên Kỹ thuật dạy học...` bằng:
     `+ Kỹ thuật dạy học: Áp dụng và nêu tên kỹ thuật NẾU có kỹ thuật được chọn trong bối cảnh sư phạm; nếu KHÔNG có kỹ thuật được chọn (hoặc người dùng đã bỏ tick) thì tổ chức theo các bước trực tiếp/vấn đáp tự nhiên, TUYỆT ĐỐI KHÔNG tự bịa hoặc gán tên kỹ thuật.`
   - Dòng ~811 (`GENERATE_ACTIVITY_C`): Tương tự, chỉ áp dụng KTDH khi có kỹ thuật được chọn trong bối cảnh.
   - Dòng ~865 (`GENERATE_ACTIVITY_D`): Tương tự, chỉ áp dụng KTDH khi có kỹ thuật được chọn trong bối cảnh.

---

## III. Danh Sách File Cần Chỉnh Sửa

| Tệp tin | Vị trí | Mục đích thay đổi |
| :--- | :--- | :--- |
| `js/khbd-app.js` | Dòng ~817, ~1022–1062, ~2336–2338, ~2424–2458 | Thêm cờ `pedagogyConfigured`, ngăn `ensurePedagogyFromLesson` ghi đè khi user đã bỏ chọn; bỏ fallback `"tps-tech"` khi pha B rỗng |
| `js/khbd-app.js` | Dòng ~5173–5175, ~5425–5455 | Sửa prompt trong `buildPedagogicalContext` và `buildPhasePedagogyContext`: cấm AI tự chọn KTDH/PPDH khi mảng rỗng |
| `js/khbd-prompts.js` | Dòng ~344–350, ~745, ~811, ~865 | Thêm quy tắc vào `ACTIVITY_TABLE_CONTRACT_COMPACT` và biến chỉ thị KTDH thành có điều kiện trong Act B, C, D |
| `canvas_soankhbd.html` | Dòng ~1475–1478, ~1534–1560 | Sửa `applyGate` trong patch inline: bỏ fallback `"tps-tech"`, không ép tick lại DOM |
| `backupcode viettailieu/canvas_soankhbd.html` | Tương tự | Đồng bộ sửa đổi để vượt qua bài kiểm thử tương thích 1-1 |
| `tests/canvas-soankhbd-smoke.js` | Cuối file | Bổ sung test tự động xác nhận bỏ tick KTDH/PPDH không bị tự động chọn lại và prompt không cưỡng ép |

---

## IV. Kế Hoạch Kiểm Thử (Verification Plan)

### 1. Kiểm thử tự động (Automated Smoke Tests)
Chạy bộ test kiểm thử hiện có bằng Node.js:
1. `node tests/canvas-soankhbd-smoke.js`:
   - Đảm bảo cú pháp JavaScript trong cả 2 file `canvas_soankhbd.html` hợp lệ 100%.
   - Đảm bảo tương thích 1-1 giữa bản chính và bản backup.
   - Kiểm tra test case mới: Khi `methods = []` và `phasePedagogy.B.techniques = []`, `pedagogyConfigured = true`, gọi `ensurePedagogyFromLesson` không làm thay đổi mảng, và prompt sinh ra cấm AI tự thêm KTDH.
2. `node tests/khbd-pedagogy-rate-smoke.js`:
   - Kiểm tra các gate 1 tiết, 2 tiết và chuẩn hóa vai GV/HS không bị phá vỡ.
3. `node tests/khbd-pedagogy-script-smoke.js`:
   - Đảm bảo xuất Word DOCX và kịch bản thực chiến CV 5512 vẫn đạt chuẩn.
4. `node tests/khbd-dynamic-time-budgets-smoke.js`:
   - Đảm bảo phân bổ thời lượng 4 hoạt động A–D không bị ảnh hưởng.

### 2. Kiểm thử thủ công (Manual Verification)
1. Mở `canvas_soankhbd.html` trên trình duyệt:
2. Chọn bài học bất kỳ (ví dụ: *Tập hợp các số tự nhiên*, Lớp 6 - Toán).
3. Chọn chế độ soạn: **⚡ Soạn rút gọn (4–6 trang)**.
4. Chuyển sang Tab 0 -> **Subtab 3. PPDH, Năng lực số & Môn**:
   - Bỏ tick toàn bộ các checkbox trong mục *Phương pháp dạy học hiện đại*.
   - Bỏ tick toàn bộ các checkbox trong mục *Kĩ thuật dạy học tích cực* (pha A, B, C, D).
5. Bấm nút **⚡ TẠO TOÀN BỘ GIÁO ÁN (1-CLICK)**:
   - **Xác minh 1**: Kiểm tra lại Tab 0 Subtab 3 -> Các checkbox vẫn giữ nguyên trạng thái bỏ tick, KHÔNG bị tự động chọn lại.
   - **Xác minh 2**: Kiểm tra nội dung tạo ra ở Tab Hoạt động (III.B, III.C, III.D) và Tab Toàn bộ Giáo án -> Bảng tổ chức thực hiện 4 bước CV 5512 không bị chèn tên các kỹ thuật dạy học (như *Think-Pair-Share*, *Khăn trải bàn*...), tiến trình diễn ra gãy gọn, đúng bản chất yêu cầu của phiên bản rút gọn.
