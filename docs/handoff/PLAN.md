# Kế hoạch Triển khai: Sửa Lỗi Tương Phản Màu Chữ Huy Hiệu Navbar trên Cổng Học Sinh (index.html)

## 1. Hiện trạng & Phân tích Nguyên nhân

### Hiện trạng thực tế:
- Khi học sinh đăng nhập vào hệ thống (`index.html`), trên thanh điều hướng (Navbar) ở góc phải xuất hiện huy hiệu:
  `[icon mũ cử nhân] Cổng Học Sinh`
- Người dùng phản ánh: *"Chữ ở trên bị điệp với màu nền nhìn không rõ"*.
- Quan sát ảnh chụp thực tế màn hình của học sinh Bùi Thị Mỹ Dung (Lớp 9/2):
  + Nền navbar là nền sáng (`bg-white/90` viền `border-slate-200/70`).
  + Huy hiệu có icon màu xanh lá (`text-emerald-500`) nhưng dòng chữ **"Cổng Học Sinh"** lại có màu trắng xám nhợt nhạt gần như tàng hình, hoàn toàn chìm vào màu nền xanh nhạt (`bg-emerald-50`), gây khó đọc và mất thẩm mỹ nghiêm trọng.
  + Tương tự, ở giao diện giáo viên, chip `[icon sao] Cập nhật đồng bộ` cũng gặp tình trạng chữ trắng trên nền trắng.

### Nguyên nhân kỹ thuật gốc rễ:
1. **Quy tắc CSS `.nav-chip` lỗi thời từ giao diện Dark Mode cũ:**
   Trong thẻ `<style>` của `index.html` (dòng 674–678):
   ```css
   .nav-chip {
       background: rgba(255, 255, 255, 0.08);
       border: 1px solid rgba(255, 255, 255, 0.12);
       color: #e2e8f0; /* <-- ĐÂY LÀ NGUYÊN NHÂN CHÍNH: Màu chữ xám trắng nhạt */
   }
   ```
   Trước đây khi navbar dùng màu nền đen tối, `color: #e2e8f0` hiển thị bình thường. Nhưng khi navbar chuyển sang nền trắng (`bg-white/90`), quy tắc CSS này vẫn giữ nguyên `color: #e2e8f0`.
2. **Độ ưu tiên CSS đè lên class Tailwind:**
   Trong JavaScript khi khởi tạo giao diện học sinh (dòng 1540):
   ```javascript
   navBadge.className = 'nav-chip rounded-full px-3 py-1.5 text-xs font-semibold whitespace-nowrap bg-emerald-50 text-emerald-700 border border-emerald-200 shadow-sm';
   navBadge.innerHTML = '<i class="fas fa-graduation-cap mr-1 text-emerald-500"></i> Cổng Học Sinh';
   ```
   Mặc dù có class Tailwind `text-emerald-700`, nhưng quy tắc `.nav-chip { color: #e2e8f0; }` trong `<style>` nội bộ được trình duyệt áp dụng với mức ưu tiên tương đương hoặc ghi đè sau class tiện ích Tailwind CDN, khiến màu chữ bị cưỡng ép về `#e2e8f0` (trắng nhạt).

---

## 2. Phạm vi & Tệp Cần Chỉnh sửa

1. `index.html`: Cập nhật CSS `.nav-chip` và lớp màu chữ của huy hiệu Cổng Học Sinh trong JS.
2. `tests/nav-chip-contrast-smoke.js`: Tạo mới bộ kiểm thử tự động kiểm tra tương phản màu chữ thanh navbar cho cả giáo viên và học sinh.

---

## 3. Chi tiết Yêu cầu Kỹ thuật cho Coder

### A. Cập nhật CSS `.nav-chip` trong `index.html`
- Tại dòng 674–678 của `index.html`, thay đổi quy tắc CSS `.nav-chip` để phù hợp với nền navbar sáng (`bg-white/90`):
  ```css
  /* CŨ */
  .nav-chip {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.12);
      color: #e2e8f0;
  }

  /* MỚI: Tông màu Slate nhã nhặn, tương phản cao, rõ ràng trên nền sáng */
  .nav-chip {
      display: inline-flex;
      align-items: center;
      background: #f1f5f9;
      border: 1px solid #e2e8f0;
      color: #334155;
  }
  ```

### B. Cập nhật Huy hiệu Học sinh trong JavaScript (`index.html`)
- Tại dòng 1540 của `index.html`, khi gán giao diện Cổng Học Sinh:
  ```javascript
  /* CŨ */
  navBadge.className = 'nav-chip rounded-full px-3 py-1.5 text-xs font-semibold whitespace-nowrap bg-emerald-50 text-emerald-700 border border-emerald-200 shadow-sm';
  navBadge.innerHTML = '<i class="fas fa-graduation-cap mr-1 text-emerald-500"></i> Cổng Học Sinh';

  /* MỚI: Sử dụng class màu đậm rõ nét text-emerald-800 và icon text-emerald-600, kèm màu chữ tường minh để không bao giờ bị đè */
  navBadge.className = 'nav-chip rounded-full px-3 py-1.5 text-xs font-bold whitespace-nowrap bg-emerald-50 text-emerald-800 border border-emerald-200 shadow-sm';
  navBadge.style.color = '#065f46';
  navBadge.innerHTML = '<i class="fas fa-graduation-cap mr-1.5 text-emerald-600"></i> Cổng Học Sinh';
  ```

### C. Cập nhật Chip Mặc định Giáo viên trong HTML (`index.html`)
- Tại dòng 1098–1100 của `index.html`:
  ```html
  <!-- CŨ -->
  <span class="nav-chip rounded-full px-3 py-2 text-xs font-semibold whitespace-nowrap">
      <i class="fas fa-sparkles mr-1 text-indigo-300"></i> Cập nhật đồng bộ
  </span>

  <!-- MỚI: Tương phản rõ ràng trên nền trắng -->
  <span class="nav-chip rounded-full px-3 py-1.5 text-xs font-semibold whitespace-nowrap bg-slate-100 text-slate-700 border border-slate-200">
      <i class="fas fa-sparkles mr-1.5 text-indigo-500"></i> Cập nhật đồng bộ
  </span>
  ```

### D. Bổ sung Smoke Test Kiểm tra Tương phản (`tests/nav-chip-contrast-smoke.js`)
- Tạo bài kiểm thử tự động đảm bảo:
  1. `.nav-chip` trong `index.html` không chứa `color: #e2e8f0`.
  2. Huy hiệu Cổng Học sinh dùng màu chữ đậm (`#065f46` / `text-emerald-800`), độ tương phản chuẩn WCAG AA trên nền `bg-emerald-50`.
  3. Chip mặc định giáo viên có icon và chữ dễ đọc trên nền sáng.

---

## 4. Tiêu chí Nghiệm thu (Acceptance Criteria)

1. **Hiển thị trực quan:**
   - Mở `index.html` với tài khoản học sinh (như học sinh Bùi Thị Mỹ Dung, Lớp 9/2):
     Huy hiệu `Cổng Học Sinh` hiển thị chữ màu xanh đậm ngọc bích (`#065f46`), sắc nét, nổi bật và tương phản hoàn hảo trên nền xanh ngọc nhẹ (`bg-emerald-50`), hoàn toàn không bị chìm/điệp với màu nền.
   - Mở `index.html` với tài khoản giáo viên:
     Chip `Cập nhật đồng bộ` hiển thị chữ xám đậm rõ ràng trên nền xám nhạt, không còn tình trạng chữ trắng trên nền trắng.
2. **Kiểm thử tự động:**
   - Chạy `node tests/nav-chip-contrast-smoke.js` đạt PASS 100%.
   - Chạy `node tests/teacher-permissions-smoke.js` đạt PASS 100%.
