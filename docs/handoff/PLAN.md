# PLAN: Sửa triệt để lỗi Hoạt động B chỉ giữ lại nhánh 2.1 và bị nuốt mất nhánh 2.2

## 1. Hiện trạng & Nguyên nhân gốc rễ (Root Cause Analysis)

Khi người dùng soạn bài (kể cả 1-Click Generate), bài học có 2 mục lớn (như Toán 6 Bài 5: Mục 1 Phép nhân, Mục 2 Phép chia) chỉ xuất hiện:
```markdown
### Hoạt động 2.1: 1. PHÉP NHÂN SỐ TỰ NHIÊN (23 phút)
...
```
và sau đó dừng luôn ở 2.1 rồi nhảy sang **C. HOẠT ĐỘNG 3: LUYỆN TẬP**, hoàn toàn biến mất **Hoạt động 2.2: 2. PHÉP CHIA HẾT VÀ PHÉP CHIA CÓ DƯ**.

### Kết quả khảo sát thực nghiệm chính xác 100%:
1. **Gemini API THỰC TẾ ĐÃ SINH ĐẦY ĐỦ CẢ 2.1 VÀ 2.2**:
   - Khi gửi Prompt B lên API (`canvas_gemini.php`), Gemini trả về HTTP 200, độ dài 5.161 ký tự, chứa cả:
     - `### Hoạt động 2.1: 1. PHÉP NHÂN SỐ TỰ NHIÊN (23 phút)`
     - `### Hoạt động 2.2: 2. PHÉP CHIA HẾT VÀ PHÉP CHIA CÓ DƯ (22 phút)`
2. **Thủ phạm: Hàm hậu xử lý `clipKhbdActivityMarkdown` xén mất nhánh 2.2**:
   - Sau khi Gemini trả về kết quả, ứng dụng chạy qua pipeline `applyActivityOutput("B", result)` -> gọi `clipKhbdActivityMarkdown("B", finalResult)` (dòng 7191 và dòng 6417 trong `js/khbd-app.js`).
   - Trong `clipKhbdActivityMarkdown`, dòng 6417 gọi:
     `let clipped = keepBestActivityBlock(lines.slice(start, end).join("\n").trim(), actKey);`
   - Trong `keepBestActivityBlock(text, "B")` (dòng 5939 `js/khbd-app.js`):
     Hàm này tìm các dòng tiêu đề của Hoạt động B bằng regex `activityHeadingRegex("B")`.
   - Trong `activityHeadingRegex` (dòng 5904 `js/khbd-app.js`):
     ```javascript
     B: "B[\\.\\s:]|HOẠT[ \\t]*ĐỘNG[ \\t]*2\\b|HÌNH[ \\t]*THÀNH"
     ```
   - **LỖI LOGIC REGEX**: Ký hiệu ranh giới từ `\b` sau số `2` coi dấu chấm `.` trong `2.1` và `2.2` là ký tự phân cách từ (`\W`). Do đó:
     - Dòng `## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI`: khớp regex!
     - Dòng `### Hoạt động 2.1: 1. PHÉP NHÂN SỐ TỰ NHIÊN`: **cũng khớp regex**!
     - Dòng `### Hoạt động 2.2: 2. PHÉP CHIA HẾT VÀ PHÉP CHIA CÓ DƯ`: **cũng khớp regex**!
   - **HẬU QUẢ TAI HẠI**: `keepBestActivityBlock` ngỡ rằng Gemini sinh lặp lại 3 phiên bản Hoạt động 2 trùng lặp (Block 0: tiêu đề chung, Block 1: nhánh 2.1, Block 2: nhánh 2.2).
   - Hàm này tiến hành chấm điểm `scoreKhbdActivityBlock` cho từng khối và chỉ lấy **duy nhất khối có điểm cao nhất** (Khối 1: nhánh 2.1 dài 2.710 ký tự vs Khối 2 dài 2.368 ký tự).
   - Kết quả: **Nhánh 2.2 bị vứt bỏ hoàn toàn ngay trong khâu xử lý nội bộ của client**, chỉ còn trơ trọi nhánh 2.1 đưa vào editor!

---

## 2. Phạm vi can thiệp

1. **Sửa biểu thức chính quy nhận diện tiêu đề chính `activityHeadingRegex` trong `js/khbd-app.js`**:
   - Bổ sung negative lookahead `(?!\\.\\d+)` sau các số thứ tự hoạt động 1, 2, 3, 4 để không bao giờ nhận nhầm các tiểu mục con (`2.1`, `2.2`, `2.3`, `1.1`...) thành tiêu đề hoạt động chính.
2. **Gia cố hàm `keepBestActivityBlock` trong `js/khbd-app.js`**:
   - Tiêu đề hoạt động cấp lớn bắt buộc là heading cấp 2 (`^##\s+`) hoặc không phải là nhánh con `###\s*Hoạt\s*động\s*\d+\.\d+`.
   - Khi `actKey === "B"`, tuyệt đối không được phân tách các nhánh con `2.1`, `2.2` thành các block cạnh tranh để loại trừ nhau.
3. **Nâng version cache-busting**:
   - Nâng version từ `v16` lên `v17` (`20260916-textbook-exact-v17`) trong `canvas_soankhbd.html`, `backupcode viettailieu/canvas_soankhbd.html`, `js/khbd-app.js`, `js/khbd-prompts.js`.
4. **Bổ sung test hồi quy**:
   - Kiểm tra trực tiếp `clipKhbdActivityMarkdown('B', text)` với dữ liệu đa nhánh 2.1 và 2.2, đảm bảo 100% giữ nguyên vẹn toàn bộ các nhánh con.

---

## 3. Ngoài phạm vi

- Không thay đổi prompt SGK hay prompt sư phạm.
- Không thay đổi giao diện Canvas.

---

## 4. Danh sách file tác động

1. `js/khbd-app.js`
2. `canvas_soankhbd.html`
3. `backupcode viettailieu/canvas_soankhbd.html`
4. `js/khbd-prompts.js`
5. `tests/khbd-activity-b-subsections-smoke.js` (hoặc test mới `tests/canvas-activity-b-multi-branches-smoke.js`)

---

## 5. Chi tiết các bước triển khai (Dành cho Coder)

### Bước 1: Sửa `activityHeadingRegex` trong `js/khbd-app.js`
Tại dòng 5901 `js/khbd-app.js`:
```javascript
function activityHeadingRegex(key) {
  const map = {
    A: "A[\\.\\s:]|HOẠT[ \\t]*ĐỘNG[ \\t]*1(?!\\.\\d+)\\b|MỞ[ \\t]*ĐẦU\\b",
    B: "B[\\.\\s:]|HOẠT[ \\t]*ĐỘNG[ \\t]*2(?!\\.\\d+)\\b|HÌNH[ \\t]*THÀNH",
    C: "C[\\.\\s:]|HOẠT[ \\t]*ĐỘNG[ \\t]*3(?!\\.\\d+)\\b|LUYỆN[ \\t]*TẬP\\b",
    D: "D[\\.\\s:]|HOẠT[ \\t]*ĐỘNG[ \\t]*4(?!\\.\\d+)\\b|VẬN[ \\t]*DỤNG\\b",
    E: "E[\\.\\s:]|HỒ[ \\t]*SƠ|PHIẾU[ \\t]*HỌC[ \\t]*TẬP|PHỤ[ \\t]*LỤC",
    F: "F[\\.\\s:]|HÌNH[ \\t]*MINH[ \\t]*HỌA"
  };
  return new RegExp(`^#{1,3}\\s*(?:${map[key]})`, "i");
}
```

### Bước 2: Gia cố `keepBestActivityBlock` trong `js/khbd-app.js`
Tại dòng 5939 `js/khbd-app.js`:
Bảo đảm không lấy các dòng tiêu đề tiểu mục `### Hoạt động 2.k:` làm điểm cắt block:
```javascript
function keepBestActivityBlock(text, actKey) {
  const source = String(text || "").trim();
  if (!source) return source;
  const headingRe = activityHeadingRegex(actKey);
  const lines = source.split(/\r?\n/);
  const starts = [];
  lines.forEach((line, index) => {
    const trimmed = line.trim();
    // Tuyệt đối không coi nhánh con 2.1, 2.2... là điểm bắt đầu một block độc lập cạnh tranh
    if (/^#{3,4}\s*(?:\d+\.\s*)?Hoạt\s*động\s*\d+\.\d+/i.test(trimmed)) return;
    if (headingRe.test(trimmed)) starts.push(index);
  });
  if (starts.length <= 1) return source;
  const blocks = starts.map((start, idx) => {
    const end = idx + 1 < starts.length ? starts[idx + 1] : lines.length;
    return lines.slice(start, end).join("\n").trim();
  });
  return blocks.sort((a, b) => scoreKhbdActivityBlock(b, actKey) - scoreKhbdActivityBlock(a, actKey))[0];
}
```

### Bước 3: Đồng bộ Cache Busting `v17`
- Trong `canvas_soankhbd.html` & `backupcode viettailieu/canvas_soankhbd.html`:
  - `khbd-prompts.js?v=20260916-textbook-exact-v17`
  - `khbd-app.js?v=20260916-textbook-exact-v17`
- Trong `js/khbd-prompts.js` và `js/khbd-app.js`: cập nhật header version `v17`.

### Bước 4: Viết bài test kiểm chứng `tests/canvas-activity-b-multi-branches-smoke.js`
- Đưa dữ liệu mẫu có cả Hoạt động 2.1 và 2.2 vào `clipKhbdActivityMarkdown("B", text, { subsectionCount: 2 })`.
- Xác nhận đầu ra:
  - BẮT BUỘC chứa cả `Hoạt động 2.1` VÀ `Hoạt động 2.2`.
  - Độ dài nội dung đầy đủ không bị cắt cụt.

---

## 6. Tiêu chí kiểm thử nghiệm thu (Verification Criteria)

1. Test `node tests/canvas-activity-b-multi-branches-smoke.js` đạt PASS 100%.
2. Tất cả các test canvas hiện có đạt PASS 100%.
3. Sau khi người dùng 1-Click Generate trên Canvas, Hoạt động B phải hiển thị đầy đủ trọn vẹn cả **Hoạt động 2.1** và **Hoạt động 2.2**, không còn bị dừng giữa chừng.
