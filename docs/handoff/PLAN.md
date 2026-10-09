# KẾ HOẠCH TRIỂN KHAI (PLAN): MP-01 — MÔ PHỎNG DIỆN TÍCH HÌNH BÌNH HÀNH (MVP TẦNG 1)

## 1. Mục tiêu
Hoàn thiện, tinh chỉnh kỹ thuật tương tác và kiểm thử toàn diện mã nguồn HTML mô phỏng offline: **MP-01 — Cắt ghép diện tích hình bình hành thành hình chữ nhật** theo đúng các yêu cầu nghiêm ngặt trong `docs/handoff/TASK.md`, `TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua/DAC_TA_KY_THUAT_MP01_MVP.md`, và quy chuẩn `TROLYTHIEN/2_TAO_BAI_TAP/QUY_CHUAN_XAY_DUNG_MO_PHONG.md`.

Đảm bảo mô phỏng chạy hoàn hảo 100% offline (Zero CDN, Zero external dependencies), chính xác tuyệt đối về hình học tọa độ, triệt tiêu lỗi cảm ứng trên bảng thông minh và bảo đảm tính trung tính sư phạm.

---

## 2. Danh sách file dự kiến tác động
- **Duy nhất 1 file:** `TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua/MP01_Dien_Tich_Hinh_Binh_Hanh.html`
- **Quy tắc bất biến:** Tuyệt đối không chỉnh sửa các file tài liệu đặc tả (`.md`) hay bất kỳ file nào khác ngoài file trên.

---

## 3. Các bước thực hiện chi tiết cho Coder

### Bước 1: Chuẩn hóa kích thước vùng chạm (Touch Target) & Trợ năng (A11y)
- Nâng bán kính tay kéo đỏ `#sliderHandle` lên `r="25"` (đường kính $50\text{ px}$) để đáp ứng tiêu chuẩn nghiêm ngặt $\ge 50\text{ px}$ trong `TASK.md` (hiện đang là $r=23$, đường kính $46\text{ px}$).
- Bổ sung các thuộc tính trợ năng và điều khiển bàn phím cho tay kéo:
  - `tabindex="0"`, `role="slider"`, `aria-valuenow="0"`, `aria-valuemin="0"`, `aria-valuemax="100"`, `aria-label="Thanh trượt cắt ghép hình bình hành"`.
  - Cập nhật giá trị `aria-valuenow` động theo tiến độ $\%$.

### Bước 2: Tinh chỉnh cơ chế kéo Pointer Events mượt mà, chống giật và chuẩn hóa tọa độ
- **Chống giật điểm chạm (Touch Offset):** Khi `pointerdown`, ghi nhận khoảng cách tương đối giữa điểm chạm và tâm tay kéo:
  ```javascript
  const pt = getSvgPoint(e);
  dragOffset = pt.x - (TRACK_START + currentDx);
  ```
- **Chuẩn hóa biến đổi tọa độ SVG:** Sử dụng API chuẩn `svg.createSVGPoint()` kết hợp `svg.getScreenCTM().inverse()` để chuyển đổi chính xác tọa độ con trỏ sang hệ tọa độ SVG trên mọi kích cỡ hiển thị, DPI, tỷ lệ co giãn và bảng tương tác thông minh.
- **Khóa triệt để rãnh trượt:** Thêm `pointer-events: none;` cho `#sliderControls .slider-track` và `#sliderProgress` để triệt tiêu mọi khả năng click nhảy cóc.
- **Chống mở menu ngữ cảnh (Context Menu):** Thêm `e.preventDefault()` trên sự kiện `contextmenu` của vùng vẽ SVG để chống việc giữ tay lâu trên bảng thông minh / thiết bị di động làm bật context menu hệ thống.
- **Hỗ trợ phím mũi tên:** Thêm sự kiện `keydown` trên `#sliderHandle`: phím `ArrowRight`/`ArrowUp` tăng $5\%$, `ArrowLeft`/`ArrowDown` giảm $5\%$ (khi chưa bị khóa `isLocked`).
- **Chuẩn hóa con trỏ của tam giác trượt:** Đặt `.sliding-polygon { cursor: default; }` (vì điều khiển thông qua thanh trượt vật lý, tránh gây hiểu nhầm cho học sinh là có thể nhấc rời tam giác tự do).

### Bước 3: Hoàn thiện trạng thái nút Giáo viên (Teacher Auto-Play)
- Trong hàm `toggleAutoPlay()`:
  - Khi bắt đầu chạy tự động: Đổi nhãn nút thành `⏹ Dừng (GV)` và đổi kiểu hiển thị trực quan (active state).
  - Khi người dùng bấm dừng hoặc khi diễn hoạt kết thúc đạt $100\%$: Khôi phục lại nhãn nút `🎬 Tự động ghép (GV)`.

### Bước 4: Chuẩn hóa Typographic Toán học & Nhãn sư phạm
- Chuẩn hóa các nhãn toán học theo quy chuẩn in nghiêng biến số, in đứng ký hiệu/đơn vị:
  - Đáy $a$: `<tspan font-style="italic">a</tspan> = 4 ô` (không in nghiêng cả cụm "= 4 ô").
  - Kích thước hình chữ nhật mới: `Chiều dài = <tspan font-style="italic">a</tspan> (4 ô)`, `Chiều rộng = <tspan font-style="italic">h</tspan> (3 ô)`.
  - Công thức chốt: `<tspan font-style="italic">S</tspan> = <tspan font-style="italic">a</tspan> · <tspan font-style="italic">h</tspan>`.

### Bước 5: Tinh chỉnh phản hồi sư phạm 2 nút trung tính
- Trong `handleChoice(isChanged)`:
  - Nếu học sinh chọn `[ Không thay đổi ]` (chính xác): Hiển thị phản hồi tán thành và giải thích rõ nguyên lý bảo toàn (các mảnh chỉ đổi chỗ, không thêm bớt).
  - Nếu học sinh chọn `[ Có thay đổi ]` (bẫy trực giác về hình dạng): Hiển thị phản hồi gợi mở khách quan: *"Lưu ý: Mặc dù hình dạng đổi từ hình bình hành sang hình chữ nhật, nhưng ta chỉ cắt và ghép các mảnh sẵn có mà không thêm bớt phần nào, nên diện tích được bảo toàn (không thay đổi)."*

### Bước 6: Khử đường nứt render đồ họa SVG (Seam Rendering)
- Thêm `shape-rendering="geometricPrecision"` trên thẻ `<svg>` và các thẻ `<polygon>` để trình duyệt tính toán khử răng cưa chính xác tuyệt đối, không để lộ vệt hở nhỏ tại đường biên ghép chéo $CB$ (từ $(350, 250)$ đến $(400, 100)$).

---

## 4. Rủi ro và giải pháp kỹ thuật

| Rủi ro kỹ thuật | Nguyên nhân tiềm ẩn | Giải pháp triệt để |
| :--- | :--- | :--- |
| **Nhảy cóc vị trí tay kéo khi chạm** | Tính toán `svgX - TRACK_START` trực tiếp mà không trừ đi vị trí ngón tay chạm vào mép hình tròn | Lưu `dragOffset` lúc `pointerdown`, tính `currentDx = svgX - TRACK_START - dragOffset` |
| **Lệch tọa độ cảm ứng khi phóng to/thu nhỏ** | Dùng `scaleX = 700 / rect.width` có thể sai số khi có CSS margin/padding/letterboxing | Dùng `svg.createSVGPoint().matrixTransform(svg.getScreenCTM().inverse())` |
| **Bảng tương tác bị cuộn trang hoặc hiện menu chuột phải** | Trình duyệt di động kích hoạt cử chỉ cuộn hoặc giữ lâu kích hoạt menu | Giữ vững `touch-action: none;` và chặn sự kiện `contextmenu` |
| **Phụ thuộc tài nguyên mạng (CDN)** | Vô tình chèn link font hoặc script ngoài | Tuân thủ zero-dependency, dùng font hệ thống |

---

## 5. Lệnh kiểm thử cụ thể (Test / Lint / Syntax Check)

Coder chạy các lệnh kiểm tra sau bằng PowerShell:

1. **Kiểm tra không chứa liên kết ngoại (Zero CDN / No external links):**
   ```powershell
   Select-String -Path "TROLYTHIEN\2_TAO_BAI_TAP\Ket_qua\MP01_Dien_Tich_Hinh_Binh_Hanh.html" -Pattern "https?://|cdn|googleapis"
   ```
   *Yêu cầu:* Kết quả trống (không tìm thấy liên kết ngoại).

2. **Kiểm tra cú pháp JavaScript & HTML (Node.js syntax check):**
   ```powershell
   node -e "const fs = require('fs'); const content = fs.readFileSync('TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua/MP01_Dien_Tich_Hinh_Binh_Hanh.html', 'utf8'); const script = content.match(/<script>([\s\S]*?)<\/script>/)[1]; new Function(script); console.log('JS Syntax: PASS');"
   ```
   *Yêu cầu:* Xuất ra `JS Syntax: PASS`.

3. **Kiểm tra kích thước bán kính tay kéo (Target diameter $\ge 50\text{ px}$):**
   ```powershell
   Select-String -Path "TROLYTHIEN\2_TAO_BAI_TAP\Ket_qua\MP01_Dien_Tich_Hinh_Binh_Hanh.html" -Pattern 'sliderHandle.*r="2[5-9]"'
   ```
   *Yêu cầu:* Có dòng khớp $r \ge 25$.

4. **Kiểm tra mở thực tế trên trình duyệt offline:**
   ```powershell
   Start-Process msedge "$((Get-Item 'TROLYTHIEN\2_TAO_BAI_TAP\Ket_qua\MP01_Dien_Tich_Hinh_Binh_Hanh.html').FullName)"
   ```
