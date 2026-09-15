# Kế hoạch Triển khai: Định Mức PPDH/KTDH Theo Số Tiết & Xuống Dòng Phân Vai GV/HS Chuẩn 5512

## 1. Yêu cầu & Căn cứ Thực tiễn

### Yêu cầu 1: Định mức Phương pháp (PPDH) và Kỹ thuật dạy học (KTDH) theo số tiết
- **Hiện trạng:** Hệ thống tự động đề xuất quá nhiều PPDH và KTDH cho bài 1 tiết (45 phút), rải khắp các kỹ thuật nặng (Trạm/Station, Mảnh ghép/Jigsaw, Phòng tranh/Gallery Walk, Dự án/PBL). Trong thực tế 45 phút, giáo viên không thể tổ chức nhiều kỹ thuật cồng kềnh như vậy, dẫn đến quá tải sư phạm và chắc chắn cháy giáo án.
- **Quy tắc chuẩn hóa:**
  1. **Bài 1 tiết (<= 45 phút):**
     - PPDH: Đúng **1 phương pháp chủ đạo** (ví dụ: Dạy học Khám phá HOẶC Giải quyết vấn đề; loại bỏ các phương pháp cồng kềnh như Dạy học Dự án, STEAM, Flipped classroom).
     - KTDH: Tối đa **1 – 2 kỹ thuật nhẹ, tinh gọn** trên toàn bài.
     - Phân bổ pha: Pha B chỉ dùng **1 kỹ thuật nhẹ** (*Think-Pair-Share* hoặc *Khăn trải bàn rút gọn*); các pha A, C, D dùng hình thức tự nhiên (Vấn đáp, Luyện tập cặp đôi); **chặn tuyệt đối** các kỹ thuật nặng (*Jigsaw, Station, Gallery walk, Mini-project, PBL, STEAM*).
  2. **Bài 2 tiết (90 phút):**
     - PPDH: Tối đa **2 phương pháp** (1 chủ đạo + 1 bổ trợ).
     - KTDH: Tối đa **2 – 3 kỹ thuật** trên toàn bài (cho phép 1 kỹ thuật hợp tác sâu như Khăn trải bàn, Sơ đồ tư duy ở Pha B hoặc C; Pha A/D dùng kỹ thuật nhanh).
  3. **Bài từ 3 tiết trở lên:**
     - PPDH: Tối đa **2 phương pháp**.
     - KTDH: Tối đa **3 – 4 kỹ thuật** (cho phép kỹ thuật phức hợp như Dự án, Bàn tay nặn bột).

### Yêu cầu 2: Xuống dòng phân vai GV và HS trong bảng tổ chức thực hiện
- **Hiện trạng:** Trong Cột trái bảng d) (Hoạt động của GV và HS), các bước tổ chức thực hiện đang bị dính liền thành một dòng/đoạn văn duy nhất:
  `+ Bước 1: Chuyển giao nhiệm vụ: (Kỹ thuật...) GV: Trình chiếu... HS: Quan sát...`
  Điều này làm văn bản bị dính chùm, rất rối mắt, vi phạm thể thức phân vai của Công văn 5512 và gây khó khăn khi giáo viên cầm giáo án lên lớp hoặc nộp thanh tra.
- **Quy tắc chuẩn hóa:**
  1. Trong từng bước (Bước 1, 2, 3, 4), **bắt buộc xuống dòng tách bạch rõ ràng**:
     - Dòng 1: Tiêu đề bước kèm phương pháp/kỹ thuật: `+ Bước 1: Chuyển giao nhiệm vụ (Kỹ thuật...):`
     - Dòng 2 (thụt lề): Lời thoại, câu lệnh, phát hiện lỗi sai của giáo viên: `<br>- **GV:** [Câu thoại trong ngoặc kép "...", hướng dẫn, can thiệp phân hóa]`
     - Dòng 3 (thụt lề): Hành động, sản phẩm trung gian của học sinh: `<br>- **HS:** [Thao tác cá nhân -> thảo luận nhóm -> báo cáo và phản biện]`
  2. Áp dụng cơ chế **2 lớp bảo vệ**:
     - *Lớp 1 (Prompt):* Chỉ đạo Gemini chèn `<br>` và format đúng cấu trúc `- **GV:**` và `- **HS:**`.
     - *Lớp 2 (Hậu xử lý tự động trong code):* Cả khi render web preview và khi xuất file Word (.docx), hệ thống tự động quét và chèn `<br>- ` trước `GV:` / `HS:` nếu chưa có ngắt dòng, đảm bảo 100% giáo án cũ lẫn mới đều tự động xuống dòng đẹp mắt.

---

## 2. Phạm vi Tệp Cần Tác Động

1. `js/khbd-app.js`:
   - Nâng cấp `applyTimeBudgetGateToPedagogy()` và `recommendPedagogyFromLesson()`:
     + Khi `isSinglePeriodLesson()`: Ép `methods` tối đa 1 mục, KTDH tối đa 1–2 mục nhẹ; loại bỏ toàn bộ kỹ thuật nặng (`jigsaw`, `station`, `gallery-tech`, `mini-project`, `pbl`, `steam`).
     + Khi 2 tiết: Giới hạn tối đa 2 PPDH và 2–3 KTDH.
   - Thêm hàm chuẩn hóa nội dung phân vai `formatKhbdRoleLineBreaks(markdown)` để tự động chèn `<br>- ` trước `GV:` và `HS:` trong bảng 2 cột mục d).
2. `canvas_soankhbd.html` & `backupcode viettailieu/canvas_soankhbd.html`:
   - Đồng bộ logic lọc định mức thời lượng và tự động xuống dòng phân vai cho môi trường Canvas.
3. `js/khbd-prompts.js`:
   - Bổ sung quy tắc thời lượng vào hợp đồng sư phạm: Bài 1 tiết BẮT BUỘC chỉ 1 PPDH và 1–2 KTDH nhẹ.
   - Cập nhật quy tắc Cột TRÁI bảng d): Mỗi bước BẮT BUỘC tách dòng bằng `<br>`:
     `+ Bước X: [Tên bước]:`
     `<br>- **GV:** [Lời thoại trong "...", hành động cụ thể]`
     `<br>- **HS:** [Hành động, sản phẩm cụ thể]`
4. `js/khbd-docx.js`:
   - Trong `parseTableCellParagraphs()`: Tự động nhận diện và tách dòng trước các nhãn `- **GV:**`, `- **HS:**`, `**GV:**`, `**HS:**`, `GV:`, `HS:` để tạo thành các đoạn (`Paragraph`) riêng biệt có thụt đầu dòng rõ ràng trong file Word.
5. `tests/khbd-pedagogy-rate-smoke.js` (Tạo mới hoặc cập nhật):
   - Kiểm thử định mức PPDH/KTDH cho bài 1 tiết và 2 tiết.
   - Kiểm thử tách dòng GV/HS trong bảng Markdown và TextRun/Paragraph Word.

---

## 3. Chi tiết Kỹ thuật Cần Triển Khai

### A. Chuẩn hóa định mức thời lượng (`js/khbd-app.js` & `canvas_soankhbd.html`)
```javascript
function applyTimeBudgetGateToPedagogy(rec, periodsCount) {
  if (!rec) return rec;
  const periods = periodsCount != null ? Number(periodsCount) : (isSinglePeriodLesson() ? 1 : 2);
  rec.techniques = rec.techniques || { A: [], B: [], C: [], D: [] };
  
  if (periods <= 1) {
    // 1 tiết (45 phút): 1 PPDH + 1-2 KTDH nhẹ
    rec.methods = (rec.methods || []).filter(id => !["pbl", "steam", "flipped", "project", "station"].includes(id)).slice(0, 1);
    const heavy = /jigsaw|station|mini-project|gallery-tech|pbl|steam|du-an/;
    const lightB = ["tps-tech", "tablecloth", "5w1h"];
    const currentB = (rec.techniques.B || []).filter(id => !heavy.test(String(id)));
    const chosenB = lightB.find(id => currentB.includes(id)) || currentB[0] || "tps-tech";
    rec.techniques.B = [chosenB];
    
    // Pha A, C, D: Tối đa 1 kỹ thuật nhẹ hoặc rỗng
    ["A", "C", "D"].forEach(phase => {
      rec.techniques[phase] = (rec.techniques[phase] || []).filter(id => !heavy.test(String(id))).slice(0, 1);
    });
    // Tổng số KTDH toàn bài không quá 2
    let totalCount = 0;
    ["B", "A", "C", "D"].forEach(phase => {
      if (totalCount >= 2) rec.techniques[phase] = [];
      else totalCount += rec.techniques[phase].length;
    });
  } else if (periods === 2) {
    // 2 tiết (90 phút): Tối đa 2 PPDH + 2-3 KTDH
    rec.methods = (rec.methods || []).slice(0, 2);
    let totalTech = 0;
    ["B", "C", "A", "D"].forEach(phase => {
      rec.techniques[phase] = (rec.techniques[phase] || []).slice(0, 1);
      totalTech += rec.techniques[phase].length;
      if (totalTech > 3) rec.techniques[phase] = [];
    });
  }
  return rec;
}
```

### B. Tự động xuống dòng phân vai GV/HS (`js/khbd-app.js` & `js/khbd-docx.js`)
Hàm chuẩn hóa tách dòng phân vai:
```javascript
function formatKhbdRoleLineBreaks(text) {
  let content = String(text || "");
  // Nếu GV: hoặc **GV:** dính liền sau tiêu đề bước hoặc nội dung khác mà chưa có <br>, chèn <br>- 
  content = content.replace(/([^\n>])\s*(?:\*\*)?GV\s*:(?:\*\*)?/gi, "$1<br>- **GV:**");
  // Nếu HS: hoặc **HS:** dính liền sau GV mà chưa có <br>, chèn <br>- 
  content = content.replace(/([^\n>])\s*(?:\*\*)?HS\s*:(?:\*\*)?/gi, "$1<br>- **HS:**");
  // Đảm bảo sau <br> có dạng chuẩn - **GV:** và - **HS:**
  content = content.replace(/<br>\s*-\s*(?:\*\*)?GV\s*:(?:\*\*)?/gi, "<br>- **GV:**");
  content = content.replace(/<br>\s*-\s*(?:\*\*)?HS\s*:(?:\*\*)?/gi, "<br>- **HS:**");
  return content;
}
```
Trong `js/khbd-docx.js` (`parseTableCellParagraphs`):
- Khi gặp dòng có chứa `GV:` hoặc `HS:`, nếu có `<br>` hoặc gạch đầu dòng `- `, tự động bóc tách thành các đoạn `Paragraph` riêng với `indent: { left: 360 }` cho dòng vai trò.

### C. Prompt sư phạm (`js/khbd-prompts.js`)
- Cập nhật chỉ dẫn cấu trúc Cột TRÁI:
  ```text
  - CỘT TRÁI — KỊCH BẢN THỰC CHIẾN PHÂN VAI RÕ RÀNG (ngăn các bước và vai trò bằng <br>):
    BẮT BUỘC từng bước phải xuống dòng riêng cho GV và HS theo mẫu sau:
    + Bước 1: Chuyển giao nhiệm vụ (Kỹ thuật...):
    <br>- **GV:** [Câu lệnh ngắn gọn trong ngoặc kép "...", hướng dẫn nhiệm vụ...]
    <br>- **HS:** [Tiếp nhận nhiệm vụ, hành động cụ thể...]
    <br>+ Bước 2: Thực hiện nhiệm vụ:
    <br>- **HS:** [Làm việc cá nhân X phút -> thảo luận cặp/nhóm Y phút tạo sản phẩm trung gian...]
    <br>- **GV:** [Quan sát, dự kiến 1 lỗi sai điển hình trong SGK và can thiệp phân hóa...]
    <br>+ Bước 3: Báo cáo, thảo luận:
    <br>- **HS:** [Đại diện báo cáo, các nhóm phản biện...]
    <br>- **GV:** [Điều hành, đặt câu hỏi gợi mở...]
    <br>+ Bước 4: Kết luận, nhận định:
    <br>- **GV:** [Nhận xét, chốt kiến thức cốt lõi...]
    <br>- **HS:** [Ghi bài vào vở...]
  - TUYỆT ĐỐI CẤM viết dính liền GV và HS trên cùng một dòng.
  ```

---

## 4. Kế Hoạch Kiểm Thử (Verification Plan)

1. **Kiểm thử Smoke tự động:**
   - Tạo bộ kiểm thử `tests/khbd-pedagogy-rate-smoke.js`:
     + Test case 1: Bài 1 tiết (`duration = "45 phút"` hoặc `1 tiết`): PPDH <= 1, KTDH <= 2, không có kỹ thuật nặng (`jigsaw`, `station`, `gallery`).
     + Test case 2: Bài 2 tiết (`duration = "90 phút"` hoặc `2 tiết`): PPDH <= 2, KTDH <= 3.
     + Test case 3: Dữ liệu Cột trái có dính liền `GV:... HS:...` được hàm chuẩn hóa tách thành các dòng `<br>- **GV:**` và `<br>- **HS:**`.
     + Test case 4: File Word export sinh ra đủ các `Paragraph` độc lập cho Bước, GV và HS.
   - Chạy toàn bộ các test hiện có:
     + `node tests/canvas-soankhbd-smoke.js`: PASS.
     + `node tests/khbd-integrations-smoke.js`: PASS.
     + `node tests/khbd-nls-ai-bold-italic-smoke.js`: PASS.
     + `node tests/khbd-docx-format-smoke.js`: PASS.
2. **Kiểm tra trực quan:**
   - Xem trước giao diện Web và file DOCX mẫu: Từng bước hiển thị rõ ràng 3 phần: Tiêu đề bước -> `- GV:` -> `- HS:`.

---

## 5. Tiêu Chí Nghiệm Thu (Acceptance Criteria)

1. Khi chọn bài 1 tiết: Hệ thống chỉ đề xuất duy nhất 1 PPDH và tối đa 1–2 KTDH nhẹ, loại bỏ các kỹ thuật nặng.
2. Khi chọn bài 2 tiết: Hệ thống đề xuất tối đa 2 PPDH và 2–3 KTDH.
3. Trong bảng tổ chức hoạt động dạy học: Tiêu đề bước, **GV:** và **HS:** luôn xuống dòng riêng biệt, có thụt đầu dòng chuẩn mực, không còn tình trạng dính chùm trên 1 dòng như ảnh phản ánh.
4. Cả `soankhbd.html` và `canvas_soankhbd.html` đều hoạt động đồng bộ và vượt qua 100% bài kiểm thử.
