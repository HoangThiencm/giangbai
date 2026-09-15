# Kế hoạch Triển khai: Dàn Ngang Cân Đối Các Khối Tiện Ích Cổng Học Sinh (index.html)

## 1. Hiện trạng & Phân tích Nguyên nhân

### Hiện trạng thực tế:
- Khi học sinh đăng nhập vào hệ thống (như tài khoản học sinh Bùi Thị Mỹ Dung, Lớp 9/2), phần thân trang hiển thị 2 khối:
  1. Khối 1: **Lộ trình học tập — Bài học & Luyện tập theo SGK** (hiện đang có 1 thẻ bài học: `Toán 9`).
  2. Khối 2: **Hoạt động lớp học — Hoạt động & Tiện ích được phân quyền** (hiện đang có 1 thẻ tiện ích: `Bảng chia sẻ Padlet`).
- Người dùng phản ánh: *"Sao không dàn ngang cho đẹp với nhau"* kèm ảnh chụp màn hình thực tế.
- Quan sát ảnh chụp:
  + Cả hai khối đều chiếm toàn bộ chiều ngang màn hình một cách độc lập (`div.mb-8` xếp dọc từ trên xuống dưới).
  + Khối 1 chỉ có 1 thẻ `Toán 9` nằm bên trái, để trống 2/3 khoảng trắng bên phải.
  + Khối 2 nằm tút xuống bên dưới với tiêu đề riêng, cũng chỉ có 1 thẻ `Bảng chia sẻ Padlet` nằm bên trái và để trống 2/3 khoảng trắng bên phải.
  + Hai thẻ có kích thước, kiểu dáng và thiết kế hoàn toàn tương đồng (icon vuông góc trái, badge trạng thái góc phải, tiêu đề in đậm, mô tả tóm tắt và nút mũi tên hành động), nhưng lại bị xếp dọc rời rạc, làm lãng phí không gian màn hình lớn và tạo cảm giác mất cân đối.

### Mục tiêu kỹ thuật:
- Khi học sinh có cả nội dung Lộ trình học tập và Hoạt động tiện ích, hai khối này được dàn ngang cạnh nhau (bố cục 2 cột cân đối `lg:grid-cols-2` trên màn hình máy tính/tablet):
  + Cột trái: Khối Lộ trình học tập (Tiêu đề + Thẻ bài học `Toán 9`).
  + Cột phải: Khối Hoạt động lớp học (Tiêu đề + Thẻ tiện ích `Bảng chia sẻ Padlet`).
- Hai tiêu đề thẳng hàng ngang phía trên, hai thẻ bài học/tiện ích dàn ngang đối xứng phía dưới, tạo nên giao diện hiện đại, lấp đầy không gian hài hòa và trực quan.
- Tự động thích ứng linh hoạt:
  + Nếu học sinh chỉ có 1 trong 2 khối (chỉ có Lộ trình hoặc chỉ có Hoạt động), khối đó tự động mở rộng toàn màn hình (`lg:col-span-2`) với lưới 3 cột như cũ.
  + Trên thiết bị di động (`< lg`), hai khối tự động xếp chồng dọc mượt mà.

---

## 2. Phạm vi & Tệp Cần Chỉnh sửa

1. `index.html`: Bọc `studentLotrinhSection` và `studentActivitiesSection` vào container lưới 2 cột `studentSectionsWrap`, đồng thời cập nhật logic trong hàm `renderStudentPortal()` để tự động điều chỉnh layout linh hoạt.
2. `tests/student-portal-layout-smoke.js`: Tạo mới smoke test tự động kiểm tra bố cục dàn ngang của Cổng Học Sinh.

---

## 3. Chi tiết Yêu cầu Kỹ thuật cho Coder

### A. Cấu trúc HTML trong `index.html`
- Tại vùng hiển thị Cổng học sinh (`#studentPortalDeck`, khoảng dòng 1136–1158):
  Bọc cả 2 khối `#studentLotrinhSection` và `#studentActivitiesSection` vào một container chung `#studentSectionsWrap`:
  ```html
  <!-- Container dàn ngang 2 cột khi có cả 2 khối nội dung -->
  <div id="studentSectionsWrap" class="grid grid-cols-1 gap-8 mb-8">
      <!-- Nhóm 1: Lộ trình bài học theo khối lớp -->
      <div id="studentLotrinhSection" class="flex flex-col">
          <div class="flex items-center justify-between mb-4">
              <div>
                  <p class="section-kicker text-teal-600">Lộ trình học tập</p>
                  <h3 class="text-xl font-extrabold text-slate-900">Bài học &amp; Luyện tập theo SGK</h3>
              </div>
          </div>
          <div id="studentLotrinhGrid" class="grid grid-cols-1 sm:grid-cols-2 gap-4 flex-1"></div>
      </div>

      <!-- Nhóm 2: Hoạt động & Tiện ích được phân quyền -->
      <div id="studentActivitiesSection" class="flex flex-col">
          <div class="flex items-center justify-between mb-4">
              <div>
                  <p class="section-kicker text-indigo-600">Hoạt động lớp học</p>
                  <h3 class="text-xl font-extrabold text-slate-900">Hoạt động &amp; Tiện ích được phân quyền</h3>
              </div>
          </div>
          <div id="studentActivitiesGrid" class="grid grid-cols-1 sm:grid-cols-2 gap-4 flex-1"></div>
      </div>
  </div>
  ```

### B. Logic Điều phối Layout trong JavaScript (`index.html`)
- Trong hàm `renderStudentPortal(allowedPages, userName, userClassName)`:
  Sau khi tính toán `allowedMath` và `allowedTools`:
  ```javascript
  const hasMath = allowedMath.length > 0;
  const hasTools = studentToolsAllowed.length > 0;
  const wrap = document.getElementById('studentSectionsWrap');

  if (wrap) {
      if (hasMath && hasTools) {
          // Cả 2 khối cùng có nội dung -> Dàn ngang 2 cột đối xứng
          wrap.className = 'grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8';
          lotrinhSection.className = 'flex flex-col';
          activitiesSection.className = 'flex flex-col';
          lotrinhGrid.className = allowedMath.length > 1 ? 'grid grid-cols-1 sm:grid-cols-2 gap-4 flex-1' : 'grid grid-cols-1 gap-4 flex-1';
          activitiesGrid.className = studentToolsAllowed.length > 1 ? 'grid grid-cols-1 sm:grid-cols-2 gap-4 flex-1' : 'grid grid-cols-1 gap-4 flex-1';
      } else {
          // Chỉ có 1 khối -> Tràn đều toàn màn hình dạng lưới 3 cột
          wrap.className = 'grid grid-cols-1 gap-8 mb-8';
          if (hasMath) {
              lotrinhSection.className = 'w-full';
              lotrinhGrid.className = 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4';
          }
          if (hasTools) {
              activitiesSection.className = 'w-full';
              activitiesGrid.className = 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4';
          }
      }
  }
  ```

### C. Tạo Smoke Test Tự Động (`tests/student-portal-layout-smoke.js`)
- Kiểm tra tính toàn vẹn của cấu trúc DOM:
  1. Tồn tại container `#studentSectionsWrap`.
  2. `#studentLotrinhSection` và `#studentActivitiesSection` nằm trong `#studentSectionsWrap`.
  3. Khi có cả môn học và tiện ích, container kích hoạt layout `lg:grid-cols-2` dàn ngang 2 cột.
  4. Thẻ bên trong mỗi khối co giãn cân đối và không để trống khoảng trắng bất thường.

---

## 4. Tiêu chí Nghiệm thu (Acceptance Criteria)

1. **Giao diện Cổng Học Sinh trên máy tính (Desktop):**
   - Khi tài khoản học sinh được phân quyền 1 môn học (`Toán 9`) và 1 tiện ích (`Bảng chia sẻ Padlet`):
     + Khối `Lộ trình học tập` nằm ở cột bên trái.
     + Khối `Hoạt động lớp học` nằm ở cột bên phải.
     + Hai tiêu đề nằm ngang bằng nhau ở hàng trên; hai thẻ `Toán 9` và `Bảng chia sẻ Padlet` nằm ngang bằng nhau ở hàng dưới.
     + Khoảng cách cân đối, không còn khoảng trống thừa 2/3 màn hình.
2. **Khả năng thích ứng:**
   - Trên màn hình nhỏ (điện thoại), hai khối tự động xếp chồng theo thứ tự Lộ trình -> Hoạt động.
   - Nếu tài khoản chỉ có Lộ trình (không có Hoạt động) hoặc ngược lại, khối đó tự bung rộng 3 cột bình thường.
3. **Kiểm thử:**
   - `node tests/student-portal-layout-smoke.js`: PASS 100%.
   - `node tests/teacher-permissions-smoke.js`: PASS 100%.
   - `node tests/nav-chip-contrast-smoke.js`: PASS 100%.
