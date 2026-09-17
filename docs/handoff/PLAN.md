# PLAN: Tối Ưu Giao Diện Lịch Báo Giảng — Đưa Cấu Hình PPCT & Lịch Nghỉ Vào Modal Setting, Thu Gọn Cảnh Báo

## User Review Required
> [!IMPORTANT]
> - **Yêu cầu từ người dùng**:
>   1. Đưa toàn bộ khu vực cấu hình PPCT (Khối, Môn, tệp PPCT, AI nhận diện, JSON, textarea nhập PPCT, Thư viện kho PPCT đã nạp) và Ngày nghỉ & dạy bù vào **Modal Setting** riêng (hoặc ẩn bớt), giúp giao diện chính của Tab 4 "Lịch báo giảng" thoáng đãng, chuyên nghiệp và tập trung vào việc tra cứu/in sổ báo giảng.
>   2. **Thu gọn khối cảnh báo lệch số tiết** ("Cần kiểm tra PPCT trước khi gửi email"): Hiện tại đang in hàng chục dòng cảnh báo màu vàng trải dài nhiều trang màn hình. Cần ẩn bớt/thu gọn thành một thẻ thông báo có thể đóng/mở (collapsible `<details>`) và giới hạn chiều cao cuộn, mặc định thu gọn gọn gàng.

---

## I. Thiết Kế Kỹ Thuật Chi Tiết

### Module 1: Tạo Modal Setting "Cấu hình PPCT & Lịch nghỉ" (`#baogiang-config-modal`)
1. **Cấu trúc Modal**:
   - Sử dụng chuẩn modal hiện có của hệ thống (`class="modal-overlay"`, `class="modal-card"` với `max-width: 900px`).
   - `id="baogiang-config-modal"`.
   - **Header**:
     - Tiêu đề: `<h2><i class="fas fa-sliders"></i> Cài đặt PPCT & Lịch nghỉ</h2>`.
     - Nút đóng: `<button class="modal-close" onclick="closeBaoGiangConfigModal()">&times;</button>`.
   - **Body** (bên trong chia 2 tab con hoặc 2 block rõ ràng):
     - **Phần 1: Khai báo & Nạp PPCT**:
       - Chọn Khối (`#bg-ppct-grade`) và Môn (`#bg-ppct-subject`).
       - Nạp tệp qua AI: `#bg-ppct-file`, nút `#bg-scan-ppct`, nút Xóa PPCT, status `#bg-ppct-status`.
       - Nạp qua JSON: Tải mẫu JSON, copy AI prompt, `#bg-ppct-json-file`, nút nạp JSON.
       - Textarea nhập trực tiếp: `#bg-curriculum` kèm dòng gợi ý định dạng mới.
       - Thư viện kho PPCT đã nạp: `#bg-ppct-library` (các thẻ card thống kê bài/tiết từng khối-môn).
     - **Phần 2: Ngày nghỉ và dạy bù**:
       - Form thêm ngoại lệ: `#bg-ex-date`, `#bg-ex-type`, `#bg-ex-scope`, `#bg-ex-target`, `#bg-ex-lesson`, nút Thêm.
       - Danh sách ngoại lệ: `#bg-exceptions`.
   - **Footer**:
     - Nút "Đóng" (`closeBaoGiangConfigModal()`).
     - Nút "Lưu & Áp dụng" (`closeBaoGiangConfigModal(); renderBaoGiangView(); showToast(...)`).
2. **Hàm JavaScript điều khiển modal**:
   - `openBaoGiangConfigModal()`: thêm class `active` vào modal `#baogiang-config-modal`.
   - `closeBaoGiangConfigModal()`: bỏ class `active` khỏi modal `#baogiang-config-modal`.

### Module 2: Tinh Gọn Thanh Công Cụ & Giao Diện Chính Tab 4 (`view-baogiang`)
1. Trên thanh tiêu đề / toolbar của Tab 4:
   - Thêm nút nổi bật:
     `<button type="button" class="btn-small" onclick="openBaoGiangConfigModal()"><i class="fas fa-sliders"></i> Cài đặt PPCT & Lịch nghỉ</button>`
   - Giữ nút "Lưu kế hoạch" (`saveToDB()`).
2. Bỏ khối `<details open>` cồng kềnh, bỏ dropdown khối/môn nằm lộ thiên và bỏ `<details>` ngày nghỉ dạy bù ở giao diện chính (vì toàn bộ đã được chuyển vào Modal Setting).
3. Giao diện chính Tab 4 giờ đây chỉ còn:
   - Thanh tiêu đề & nút mở Cài đặt.
   - Hàng bộ lọc nghiệp vụ: Ngày bắt đầu Tuần 1, Chọn Giáo viên, Chọn Tháng, Chế độ xem (Sổ ngày / Lưới tuần / Bảng tổng hợp).
   - Khối cảnh báo thu gọn (Module 3).
   - Bảng/sổ lịch báo giảng chi tiết (`#bg-schedule`).

### Module 3: Thu Gọn Cảnh Báo "Cần kiểm tra PPCT trước khi gửi email"
1. Trong `renderBaoGiangBaseView()` (dòng ~4030) và `renderBaoGiangView()` (dòng ~4043):
   - Thay thế việc chèn trực tiếp thẻ `<div>` cảnh báo trải dài bằng thẻ `<details>`:
     ```html
     <details class="bg-warning-box" style="margin:0 0 12px;padding:10px 14px;border:1px solid #fbbf24;border-radius:8px;background:#fffbeb;color:#92400e;font-size:.88rem;">
         <summary style="font-weight:700;cursor:pointer;display:flex;align-items:center;gap:8px;user-select:none;">
             <i class="fas fa-triangle-exclamation"></i>
             <span>Cần kiểm tra PPCT trước khi gửi email (${warnings.length} cảnh báo — Bấm để xem/ẩn)</span>
         </summary>
         <div style="margin-top:8px;padding-top:8px;border-top:1px dashed #fcd34d;max-height:180px;overflow-y:auto;line-height:1.6;">
             ${warnings.map(message => escapeHtml(message)).join('<br>')}
         </div>
     </details>
     ```
   - Mặc định thẻ `<details>` này **KHÔNG có thuộc tính `open`** (tự đóng), chỉ chiếm đúng 1 dòng thông báo trang nhã (chiều cao ~36px).
   - Khi người dùng muốn xem danh sách cảnh báo, click để mở ra; vùng nội dung có `max-height: 180px; overflow-y: auto;` giúp cuộn mượt mà mà không đẩy lệch giao diện.

### Module 4: Bảo Toàn Tương Thích & Kiểm Thử
1. Tất cả ID phần tử HTML (`bg-curriculum`, `bg-ppct-file`, `bg-scan-ppct`, `bg-ppct-status`, `bg-ppct-grade`, `bg-ppct-subject`, `bg-exceptions`, `bg-schedule`, v.v.) được giữ nguyên vẹn 100% để các hàm JavaScript hiện hành và các bộ smoke test không bị ảnh hưởng.
2. Bổ sung kiểm thử tự động trong `tests/baogiang-teacher-month-smoke.js`:
   - Xác nhận `#baogiang-config-modal` tồn tại và chứa đầy đủ `#bg-curriculum`, `#bg-ppct-grade`, `#bg-ppct-subject`.
   - Xác nhận có nút mở modal `openBaoGiangConfigModal()`.
   - Xác nhận cảnh báo lệch PPCT được bọc trong thẻ `<details>` thu gọn.

---

## II. Danh Sách Tệp Cần Chỉnh Sửa

| Tệp tin | Vị trí | Mục tiêu thay đổi |
| :--- | :--- | :--- |
| `phancongtochuyenmon.html` | Dòng ~2020 - 2038 | Dọn dẹp giao diện chính Tab 4, thêm nút `openBaoGiangConfigModal()` |
| `phancongtochuyenmon.html` | Dòng ~2710 (Khu vực modal) | Thêm `#baogiang-config-modal` chứa cấu hình PPCT và Ngày nghỉ / dạy bù |
| `phancongtochuyenmon.html` | Dòng ~4030 & ~4043 | Thu gọn cảnh báo lệch tiết thành `<details>` cuộn tối đa 180px |
| `phancongtochuyenmon.html` | Dòng ~4050 | Thêm 2 hàm `openBaoGiangConfigModal()` và `closeBaoGiangConfigModal()` |
| `tests/baogiang-teacher-month-smoke.js` | Cuối file | Thêm assertions kiểm tra modal và cấu trúc collapsible cảnh báo |

---

## III. Kế Hoạch Kiểm Thử (Verification Plan)

### Kiểm thử tự động
- `node tests/baogiang-teacher-month-smoke.js` — PASS.
- `node tests/baogiang-weekday-segment-smoke.js` — PASS.
- `node tests/baogiang-recognition-smoke.js` — PASS.
- `node tests/timetable-render-smoke.js` — PASS.
- `node tests/attendance-autosync-smoke.js` — PASS.
