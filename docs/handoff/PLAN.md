# PLAN: Cải Tiến Thẻ & Modal Thông Báo Dạy Thay Theo Phản Hồi Người Dùng

## Hiện trạng & Phản hồi thực tế từ người dùng (ảnh chụp đính kèm)
Quan sát ảnh chụp màn hình thực tế từ người dùng (`media_1788687743253.png`):
1. **Tiêu đề thông báo bị lặp nội dung**:
   - Trong mẫu "Chuẩn Hành chính" (`official`), thẻ thông báo đang render cả 2 dòng cùng nội dung:
     `V/v phân công dạy thay Thứ Tư, ngày 09/09/2026`
     `<br>THÔNG BÁO PHÂN CÔNG DẠY THAY NGÀY 09/09/2026`
     dưới khối tiêu đề in hoa `THÔNG BÁO`. Điều này làm tiêu đề bị lặp 2 lần một cách thừa thãi và mất thẩm mỹ.
   - Người dùng yêu cầu: Tên thông báo lấy trực tiếp từ ô nhập liệu của user (`#dt-ann-title`), không lặp lại nội dung.
2. **Lời dặn dò cần có nút check bật/tắt**:
   - Hiện tại khối "Lời dặn dò của Tổ chuyên môn" luôn luôn hiển thị (nếu trống thì hiện gạch ngang `—`), chiếm nhiều diện tích trên ảnh khi tổ chuyên môn không có nhu cầu dặn dò thêm.
   - Người dùng yêu cầu: Thêm nút check (checkbox / switch) bật/tắt (hiện/ẩn) lời dặn dò. Khi tắt thì ẩn hoàn toàn khối lời dặn trên ảnh và khi copy tin nhắn Zalo.
3. **Chức danh người ký chưa chuẩn xác**:
   - Thẻ thông báo hiện ghi chức danh: `Đại diện Tổ trưởng chuyên môn`.
   - Người dùng chỉ rõ: Câu này không đúng trong quy chuẩn nhà trường, phải là `Tổ trưởng`.

---

## Phạm vi thực hiện

### 1. Tối Ưu Tiêu Đề Thông Báo & Chống Trùng Lặp (`#dt-ann-title` & Card Render)
- **Ô nhập liệu `#dt-ann-title`**: Người dùng có toàn quyền nhập tiêu đề thông báo theo ý muốn.
- **Theme `official` (Chuẩn Hành chính)**:
  - Khối tiêu đề gồm:
    `<h3 class="dt-ann-main-title">THÔNG BÁO</h3>`
    `<p class="dt-ann-sub">${officialSubject}</p>`
  - Trích yếu `officialSubject` được chuẩn hóa từ `title` do user nhập:
    + Nếu user nhập nội dung bắt đầu bằng `"THÔNG BÁO V/v ..."` hoặc `"THÔNG BÁO ..."`, loại bỏ tiền tố thừa `"THÔNG BÁO"` để thành `V/v ...` trang trọng.
    + Nếu tiêu đề đã có `V/v`, giữ nguyên `V/v ...`.
    + Nếu tiêu đề chưa có `V/v`, tự động thêm `V/v ${title}` hoặc hiển thị trực tiếp `title` gọn gàng.
    + **Tuyệt đối loại bỏ** việc nối chuỗi `<br>${escapeHtml(title)}` bên dưới dòng `V/v ...` như code cũ.
- **Theme `modern` và `emerald`**:
  - Tiêu đề chính to rõ hiển thị trực tiếp nội dung do user nhập vào `#dt-ann-title`:
    `<h3 class="dt-ann-main-title">${escapeHtml(title)}</h3>`
  - Dòng phụ `.dt-ann-sub` hiển thị thông tin thời gian hoặc tổ ban hành, không lặp lại cụm từ `"BẢNG PHÂN CÔNG DẠY THAY"` rồi lại `"THÔNG BÁO PHÂN CÔNG DẠY THAY"`.

### 2. Thêm Checkbox Bật/Tắt "Lời Dặn Dò"
- **Giao diện bảng điều khiển (`.dt-ann-controls`)**:
  - Tại nhãn của trường "Ghi chú / Dặn dò của Tổ chuyên môn", thêm checkbox điều khiển:
    ```html
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
        <label for="dt-ann-note" style="margin: 0;">Ghi chú / Dặn dò của Tổ chuyên môn:</label>
        <label style="display: inline-flex; align-items: center; gap: 6px; font-size: 0.82rem; font-weight: 600; cursor: pointer; color: #334155; user-select: none;">
            <input type="checkbox" id="dt-ann-show-note" checked onchange="renderAnnouncementCard()">
            <span>Hiển thị lời dặn</span>
        </label>
    </div>
    ```
- **Logic render thẻ thông báo (`renderAnnouncementCard`)**:
  - Đọc trạng thái `showNote = document.getElementById('dt-ann-show-note')?.checked ?? true`.
  - Nếu `showNote` là `true` VÀ có nội dung `note` (không rỗng): Render khối `.dt-ann-note`.
  - Nếu `showNote` là `false` HOẶC `note` rỗng: Không render khối `.dt-ann-note` (thẻ ảnh sẽ co gọn lại sạch sẽ, dành toàn bộ tiêu điểm cho bảng phân công).
- **Tương tác nút tiện ích**:
  - Khi bấm các chip mẫu nhanh (`Giờ giấc`, `Sổ đầu bài`, `Đột xuất`) hoặc bấm `AI Soạn thông báo Zalo`: Tự động gán `dt-ann-show-note.checked = true` để lời dặn hiển thị ngay.
- **Xuất tin nhắn Zalo (`buildAnnouncementZaloText`)**:
  - Chỉ đưa dòng `🔔 Lời dặn dò: ...` vào tin nhắn Zalo khi `showNote` được bật và có nội dung.

### 3. Chuẩn Hóa Chức Danh Ký Tên
- **Trong thẻ thông báo (`#dt-announcement-card`)**:
  - Sửa dòng chữ ký:
    Từ:
    ```html
    <div class="sign-box">
        <div><b>Đại diện Tổ trưởng chuyên môn</b></div>
        <div style="height:36px;"></div>
        <div><b>${escapeHtml(ttcm || 'TTCM')}</b></div>
    </div>
    ```
    Thành:
    ```html
    <div class="sign-box">
        <div><b>Tổ trưởng</b></div>
        <div style="height:36px;"></div>
        <div><b>${escapeHtml(ttcm || 'TTCM')}</b></div>
    </div>
    ```
- **Trong tin nhắn Zalo (`buildAnnouncementZaloText`)**:
  - Sửa chữ ký cuối tin:
    Từ `✍️ TTCM: ${ttcm || 'Tổ trưởng chuyên môn'}`
    Thành `✍️ Tổ trưởng: ${ttcm || 'TTCM'}`.

---

## File tác động
- `phancongtochuyenmon.html`:
  + Cập nhật HTML control `#dt-ann-show-note`.
  + Sửa hàm `renderAnnouncementCard()`:
    - Xử lý tiêu đề theme `official` và `modern` không bị trùng lặp, dùng đúng input của user.
    - Điều kiện hiển thị khối lời dặn dò theo checkbox.
    - Sửa chức danh ký tên thành `Tổ trưởng`.
  + Sửa hàm `buildAnnouncementZaloText()`:
    - Chỉ đưa lời dặn khi checkbox bật và có nội dung.
    - Sửa chức danh ký tên Zalo thành `Tổ trưởng`.
  + Cập nhật các hàm `applyAnnouncementQuickNote()` và `generateDayThayAnnouncementAI()` để bật lại checkbox nếu user đang tắt khi bấm thêm lời dặn.
- `docs/handoff/PLAN.md` (Kế hoạch này).
- `docs/handoff/.lock` (Tạo file khóa).

---

## Tiêu chí nghiệm thu (Verify Checklist)
1. **Tiêu đề thông báo**:
   - Khi chọn theme "Chuẩn Hành chính", không còn hiện tượng lặp 2 dòng trích yếu và tiêu đề in hoa nối đuôi nhau.
   - Khi user gõ tiêu đề tùy ý vào `#dt-ann-title`, tiêu đề trên card cập nhật ngay lập tức theo đúng nội dung user gõ.
2. **Checkbox bật/tắt Lời dặn dò**:
   - Khi checkbox được tick và có ghi chú: Thẻ ảnh hiển thị hộp Lời dặn dò trang trọng.
   - Khi bỏ tick checkbox: Hộp Lời dặn dò biến mất hoàn toàn trên thẻ ảnh, card tự động co gọn chiều cao.
   - Khi bấm các chip mẫu hoặc AI soạn: Checkbox tự động bật và hiển thị lời dặn.
   - Tin nhắn Zalo khi copy tôn trọng trạng thái bật/tắt này.
3. **Chức danh người ký**:
   - Hiển thị đúng `Tổ trưởng` (không còn chữ `Đại diện Tổ trưởng chuyên môn`).
