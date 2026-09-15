# Kế hoạch Triển khai: Mở Công Khai giaoantichhop.html & Fix Triệt Để Xuống Dòng Phân Vai (Cache-Busting)

## 1. Yêu cầu & Căn cứ Thực tiễn

### Yêu cầu 1: Khắc phục lỗi `giaoantichhop.html` bắt đăng nhập
- **Hiện trạng:** Người dùng vào `giaoantichhop.html` bị chuyển hướng ép đăng nhập vào `login.html`.
- **Nguyên nhân gốc rễ:**
  1. File `giaoantichhop.html` tại dòng 4 nạp `<script src="access-control.js"></script>`.
  2. File `access-control.js` tại dòng 41 chứa cấu hình: `'giaoantichhop.html': 'soankhbd',`.
  3. Mặc dù giao diện header của `giaoantichhop.html` ghi rõ: `"Công khai · Không cần tài khoản"` (dòng 52), nhưng script `access-control.js` tự động kiểm tra `authToken` và chuyển hướng về `login.html` khi người dùng chưa đăng nhập.
- **Quy tắc chuẩn hóa:**
  1. `giaoantichhop.html` là công cụ **hoàn toàn công khai**, bất kỳ ai cũng có thể sử dụng trực tiếp mà không cần tài khoản.
  2. Xóa bỏ hoàn toàn `<script src="access-control.js"></script>` khỏi `giaoantichhop.html`.
  3. Xóa bỏ `'giaoantichhop.html': 'soankhbd',` khỏi `access-control.js`.

---

### Yêu cầu 2: Khắc phục triệt để "sao tôi không thấy thay đổi gì đâu" (Xuống dòng phân vai GV/HS)
- **Hiện trạng:**
  - Ảnh chụp thực tế của người dùng cho thấy các bước hoạt động vẫn nằm trên cùng 1 dòng:
    `+ Bước 1: Chuyển giao nhiệm vụ: (Kỹ thuật 5W1H) GV: Trình chiếu... HS: Quan sát...`
    `+ Bước 2: Thực hiện nhiệm vụ: (Kỹ thuật Think-Pair-Share) HS: ... GV: ...`
- **Nguyên nhân gốc rễ:**
  1. **Bộ nhớ đệm (Browser/CDN Cache):**
     - File `canvas_soankhbd.html` và `backupcode viettailieu/canvas_soankhbd.html` đang nạp các tệp script từ `https://hoangthiencm.id.vn/` với query param cũ:
       `?v=20260915-nls-ai-bi`
     - File `soankhbd.html` nạp script không kèm version query string (`js/khbd-app.js`, `js/khbd-docx.js`, `js/khbd-prompts.js`).
     - Trình duyệt và Cloudflare tiếp tục phân phối phiên bản `khbd-app.js` và `khbd-docx.js` cũ trong cache, chưa có logic tách dòng và khóa định mức.
  2. **Tiêu đề Bước dính liền GV/HS:**
     - Trong ảnh thực tế: `+ Bước 1: Chuyển giao nhiệm vụ: (Kỹ thuật 5W1H) GV:` — nhãn `GV:` đứng liền sau tiêu đề bước mà không có ngắt dòng `<br>`.
     - Hàm `formatKhbdRoleLineBreaks` cần đảm bảo tách dòng cả khi `GV:` hoặc `HS:` xuất hiện ngay sau tiêu đề bước `+ Bước X: ...`.
  3. **Khâu hiển thị xem trước (Preview):**
     - Cần đảm bảo `formatKhbdRoleLineBreaks` được gọi khi xem trước Markdown (`renderMathPreview`), khi tổng hợp toàn bộ giáo án (`getFullLessonPlanMarkdown`) và khi nạp bản nháp.

---

## 2. Phạm vi Tệp Cần Tác Động

1. `giaoantichhop.html`:
   - Xóa thẻ `<script src="access-control.js"></script>` ở dòng 4.
2. `access-control.js`:
   - Xóa `'giaoantichhop.html': 'soankhbd',` tại dòng 41.
3. `canvas_soankhbd.html`:
   - Nâng `version` trong `window.__KHBD_CANVAS__` thành `"20260915-rolebreak-v2"`.
   - Nâng query parameter cache-bust cho:
     + `khbd-prompts.js?v=20260915-rolebreak-v2`
     + `khbd-docx.js?v=20260915-rolebreak-v2`
     + `khbd-app.js?v=20260915-rolebreak-v2`
4. `backupcode viettailieu/canvas_soankhbd.html`:
   - Đồng bộ tương tự như `canvas_soankhbd.html`.
5. `soankhbd.html`:
   - Thêm `?v=20260915-rolebreak-v2` cho các thẻ script `js/khbd-prompts.js`, `js/khbd-docx.js`, `js/khbd-app.js`.
6. `js/khbd-app.js`:
   - Nâng cấp `formatKhbdRoleLineBreaks(text)` để nhận diện triệt để:
     + Nhãn `GV:` hoặc `HS:` đứng sau tiêu đề bước `+ Bước ...:` hoặc sau dấu ngoặc đơn `(...)` -> ngắt dòng `<br>- **GV:**` hoặc `<br>- **HS:**`.
     + Áp dụng `formatKhbdRoleLineBreaks` trong `getFullLessonPlanMarkdown()`, `renderMathPreview()` và khi nạp nội dung hoạt động.
7. `tests/giaoantichhop-public-access-smoke.js`:
   - Tạo mới test tĩnh: đảm bảo `giaoantichhop.html` không nạp `access-control.js` và `access-control.js` không khóa route `giaoantichhop.html`.

---

## 3. Chi tiết Kỹ thuật Cần Triển Khai

### A. Gỡ bỏ quyền truy cập khỏi `giaoantichhop.html` & `access-control.js`

Trong `giaoantichhop.html`:
```html
<!-- XÓA DÒNG NÀY: -->
<script src="access-control.js"></script>
```

Trong `access-control.js`:
```javascript
// XÓA MỤC NÀY:
'giaoantichhop.html': 'soankhbd',
```

### B. Nâng cấp Cache-Busting Version String

Tại `canvas_soankhbd.html` & `backupcode viettailieu/canvas_soankhbd.html`:
```javascript
window.__KHBD_CANVAS__ = {
  host: "https://hoangthiencm.id.vn",
  model: "gemini-3-flash-preview",
  version: "20260915-rolebreak-v2",
  connected: false
};
```
Và tại các vị trí nạp script hosting:
```html
<script src="https://hoangthiencm.id.vn/js/khbd-prompts.js?v=20260915-rolebreak-v2"></script>
<script src="https://hoangthiencm.id.vn/js/khbd-docx.js?v=20260915-rolebreak-v2"></script>
<script src="https://hoangthiencm.id.vn/js/khbd-app.js?v=20260915-rolebreak-v2"></script>
```

### C. Hoàn thiện hàm chuẩn hóa `formatKhbdRoleLineBreaks(text)`

```javascript
function formatKhbdRoleLineBreaks(text) {
  let content = String(text || "");
  // 1. Tách GV: sau tiêu đề bước hoặc nội dung khác mà chưa có <br>
  content = content.replace(/([^\n>])\s*(?:\*\*)?GV\s*:(?:\*\*)?/gi, "$1<br>- **GV:**");
  // 2. Tách HS: sau nội dung khác mà chưa có <br>
  content = content.replace(/([^\n>])\s*(?:\*\*)?HS\s*:(?:\*\*)?/gi, "$1<br>- **HS:**");
  // 3. Chuẩn hóa định dạng chuẩn có gạch đầu dòng sau <br>
  content = content.replace(/<br>\s*-\s*(?:\*\*)?GV\s*:(?:\*\*)?/gi, "<br>- **GV:**");
  content = content.replace(/<br>\s*-\s*(?:\*\*)?HS\s*:(?:\*\*)?/gi, "<br>- **HS:**");
  // 4. Dòng bắt đầu bằng GV:/HS: không có dấu gạch
  content = content.replace(/(^|<br>)\s*(?:\*\*)?GV\s*:(?:\*\*)?/gi, "$1- **GV:**");
  content = content.replace(/(^|<br>)\s*(?:\*\*)?HS\s*:(?:\*\*)?/gi, "$1- **HS:**");
  return content;
}
```

---

## 4. Kế hoạch Kiểm thử (Verification Plan)

### Automated Tests:
1. `node tests/giaoantichhop-public-access-smoke.js`:
   - Xác nhận `giaoantichhop.html` không chứa `access-control.js`.
   - Xác nhận `access-control.js` không chứa `giaoantichhop.html`.
2. `node tests/teacher-permissions-smoke.js`:
   - Xác nhận hệ thống phân quyền giáo viên vẫn hoạt động chính xác.
3. `node tests/khbd-pedagogy-rate-smoke.js`:
   - Xác nhận `formatKhbdRoleLineBreaks` tách đúng dòng cho các mẫu văn bản thực tế từ người dùng.
4. `node tests/canvas-soankhbd-smoke.js`:
   - Xác nhận `canvas_soankhbd.html` nạp script với version mới.

---
Mời Coder triển khai đúng theo kế hoạch trên.
