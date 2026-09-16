# PLAN

## Hiện trạng & Nguyên nhân gốc rễ (Root Cause)
- **ĐÃ RÀ SOÁT VÀ TÌM RA ĐÚNG NGUYÊN NHÂN MẤT HOẠT ĐỘNG 2.2**:
  1. Khi Gemini tạo giáo án cho Hoạt động B, Gemini sinh đủ cả `### Hoạt động 2.1: 1. PHÉP NHÂN...` và `### Hoạt động 2.2: 2. PHÉP CHIA...`.
  2. Sau khi Gemini trả về kết quả, hệ thống gọi chuỗi hàm xử lý hậu kỳ: `applyActivityOutput("B", ...)` -> `clipKhbdActivityMarkdown("B", ...)` -> `keepBestActivityBlock(text, "B")`.
  3. Trong `js/khbd-app.js` (dòng 5894), hàm `activityHeadingRegex("B")` được viết là:
     `B: "B[\\.\\s:]|HOẠT[ \\t]*ĐỘNG[ \\t]*2\\b|HÌNH[ \\t]*THÀNH"`
     Do `\b` (ranh giới từ) sau số 2 có thể tách trước dấu chấm `.`, regex này **vô tình khớp luôn cả `### Hoạt động 2.1` và `### Hoạt động 2.2`**.
  4. Hậu quả: `keepBestActivityBlock` phát hiện có 3 tiêu đề khớp regex `B` (gồm `## B. HOẠT ĐỘNG 2:`, `### Hoạt động 2.1:`, `### Hoạt động 2.2:`), nên tưởng nhầm đây là các bản sinh lặp của toàn bộ Hoạt động B. Hàm này liền **cắt xén tách thành 3 khối riêng biệt và chỉ giữ lại đúng 1 khối có điểm số cao nhất**, vứt bỏ hoàn toàn `Hoạt động 2.2`!

---

## Phạm vi thực hiện

### 1. Sửa `activityHeadingRegex` và `keepBestActivityBlock` trong `js/khbd-app.js`
- **File**: `js/khbd-app.js`, `canvas_soankhbd.html`, `backupcode viettailieu/canvas_soankhbd.html`.
- **Giải pháp**:
  - Sửa `activityHeadingRegex(key)`:
    - Đối với `B`: Dùng regex chặn chặt chẽ không cho khớp các nhánh con:
      `B: "B[\\.\\s:]|(?:HOẠT[ \\t]*ĐỘNG|HĐ)[ \\t]*2(?!\\.\\d)\\b|HÌNH[ \\t]*THÀNH"`
    - Các mục A, C, D: Đảm bảo chỉ khớp tiêu đề cấp lớn `HOẠT ĐỘNG 1`, `HOẠT ĐỘNG 3`, `HOẠT ĐỘNG 4`.
  - Trong `keepBestActivityBlock(text, actKey)`:
    - Đảm bảo khi `actKey === "B"`, toàn bộ nội dung chứa `Hoạt động 2.1`, `Hoạt động 2.2`, ..., `Hoạt động 2.N` được bảo toàn nguyên vẹn 100%, không bao giờ bị cắt xén hay lược bỏ nhánh con.

### 2. Cập nhật kiểm thử tự động
- **File**: `tests/khbd-activity-b-subsections-smoke.js`, `tests/khbd-textbook-exact-structure-smoke.js`.
- Bổ sung test kiểm tra trực tiếp qua chuỗi hàm `clipKhbdActivityMarkdown("B", sampleWith2Branches)` và `applyActivityOutput("B", sampleWith2Branches)`:
  - Bắt buộc đầu ra phải chứa đủ cả `Hoạt động 2.1` và `Hoạt động 2.2`.

---

## Ngoài phạm vi
- Không thay đổi logic của các Hoạt động A, C, D, E khác.

---

## File dự kiến tác động
- `js/khbd-app.js`
- `canvas_soankhbd.html`
- `backupcode viettailieu/canvas_soankhbd.html`
- `tests/khbd-activity-b-subsections-smoke.js`
- `tests/khbd-textbook-exact-structure-smoke.js`

---

## Các bước thực hiện
1. Sửa `activityHeadingRegex` trong `js/khbd-app.js` để loại trừ `(?!\.\d)`.
2. Bảo vệ `keepBestActivityBlock` không chia nhỏ Hoạt động B khi chứa nhiều nhánh con.
3. Đồng bộ vào `canvas_soankhbd.html` và `backupcode viettailieu/canvas_soankhbd.html`.
4. Viết bổ sung assertion trong `tests/khbd-activity-b-subsections-smoke.js`.
5. Chạy toàn bộ test suites và bàn giao.

---

## Tiêu chí nghiệm thu
1. `clipKhbdActivityMarkdown("B", text)` giữ nguyên 100% tất cả các nhánh con `Hoạt động 2.1`, `Hoạt động 2.2`, `Hoạt động 2.3`...
2. Đầu ra trên màn hình khi tạo bài Phép nhân và Phép chia số tự nhiên hiển thị đầy đủ 2 bảng:
   - `### Hoạt động 2.1: 1. PHÉP NHÂN SỐ TỰ NHIÊN`
   - `### Hoạt động 2.2: 2. PHÉP CHIA HẾT VÀ PHÉP CHIA CÓ DƯ`
3. 100% test suites PASS.
