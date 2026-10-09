# ĐẶC TẢ KỸ THUẬT TRIỂN KHAI MVP
## MP-04: CHUYỂN ĐỘNG QUAY 180° QUANH TÂM VÀ ĐỐI CHIẾU BÓNG MỜ
*(Bản chuẩn v1.5.0 — MVP Tầng 1 đã kiểm thử đạt, đủ điều kiện làm mẫu chuẩn đầu tiên)*

**Phân nhánh:** Trợ lý Sư phạm Hoàng Thiên — Nhánh 2: Tạo bài tập & Học liệu tương tác  
**Tình trạng:** `[ĐÃ KIỂM THỬ ĐẠT & NGHIỆM THU — ĐỦ ĐIỀU KIỆN LÀM MẪU CHUẨN ĐẦU TIÊN v1.5.0]`  
**Tiêu chuẩn áp dụng:** Single-file Offline HTML, SVG Vector, Pointer Events API, Không thư viện ngoài  
**Phạm vi MVP:** 3 mẫu chong chóng (2 cánh, 3 cánh, 4 cánh). Mẫu mở rộng để ở Phase 2.  

---

### 1. CẤU TRÚC FILE HTML OFFLINE DỰ KIẾN
- **Độc lập 100% (Single File Self-Contained):**
  - Toàn bộ HTML, CSS và JavaScript được tích hợp trọn vẹn trong một file duy nhất (`MP04_Tam_Doi_Xung.html`).
  - Chạy mượt mà trực tiếp qua giao thức tệp cục bộ (`file:///`) trên máy tính để bàn, laptop giáo viên, máy tính bảng và bảng tương tác thông minh.
  - **Không phụ thuộc Internet:** Tuyệt đối không tải bất kỳ tài nguyên ngoại vi nào (không CDN font, không framework JS/CSS bên ngoài). Mọi định dạng phông chữ dùng phông hệ thống mượt mà (`system-ui, -apple-system, Segoe UI, Roboto, sans-serif`).
- **Khung cấu trúc mã nguồn:**
  ```html
  <!DOCTYPE html>
  <html lang="vi">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Mô phỏng MP-04: Tâm đối xứng</title>
    <style>
      /* CSS Reset & Bố cục Responsive & Tối ưu cảm ứng bảng tương tác */
    </style>
  </head>
  <body>
    <!-- KHỐI 1: HEADER & THANH CHỌN MẪU HÌNH -->
    <!-- KHỐI 2: KHUNG VẼ TƯƠNG TÁC VECTOR SVG (VIEWBOX 600x600) -->
    <!-- KHỐI 3: HỘP ĐIỀU KHIỂN & KHÁM PHÁ SƯ PHẠM (HỎI/ĐÁP [CÓ]/[KHÔNG]) -->

    <script>
      // Vanilla JavaScript đóng gói khép kín điều khiển máy trạng thái
    </script>
  </body>
  </html>
  ```

---

### 2. KÍCH THƯỚC VÙNG VẼ VÀ BỐ CỤC MÀN HÌNH
- **Thiết kế Responsive tối ưu cho bảng tương tác 16:9 và màn hình lớp học:**
  - Container trung tâm: Chiều rộng tối đa `max-width: 860px`, căn giữa màn hình, nền màu trắng sáng chuẩn sư phạm (`#ffffff`), tương phản rõ ràng trên nền xám dịu mắt (`#f8fafc`).
  - Khung vẽ chính: Sử dụng thẻ `<svg>` với thuộc tính `viewBox="0 0 600 600"` (tỷ lệ 1:1), tự động co giãn theo kích thước thiết bị mà vẫn bảo toàn tuyệt đối tọa độ toán học.
  - Tâm quay $O$: Đặt cố định chính xác tại tọa độ trung tâm $(x_0, y_0) = (300, 300)$.
- **Phân chia 3 vùng chức năng trên màn hình:**
  1. **Khu vực trên (Header & Tabs):**
     - Tiêu đề ngắn gọn: *"Khám phá hình có tâm đối xứng qua chuyển động quay nửa vòng"*.
     - 3 nút bấm chuyển đổi mẫu hình: `[ Chong chóng 2 cánh ]`, `[ Chong chóng 3 cánh ]`, `[ Chong chóng 4 cánh ]`. Chiều cao nút $\ge 48\text{ px}$, phông chữ to rõ.
  2. **Khu vực giữa (Khung vẽ SVG tương tác):**
     - Tâm $O$ cố định: Điểm tròn bán kính $8\text{ px}$, màu vàng viền đỏ, nhãn chữ $O$ in hoa đậm bên cạnh.
     - Cung ray kéo định hướng: Cung tròn bán kính $R = 195\text{ px}$ thể hiện đường ray quay từ $0^\circ$ (12 giờ) theo chiều kim đồng hồ đến $180^\circ$ (6 giờ).
     - Bóng mờ viền xanh: Nét đứt màu xanh lam (`#2563eb`), độ dày $2.5\text{ px}$, đứng yên cố định ở vị trí xuất phát $0^\circ$.
     - Chong chóng thực: Màu cam đỏ tươi sáng (`#ea580c`), viền đậm nét (`#c2410c`), quay quanh $O$.
     - Tay kéo cảm ứng (Control Handle): Điểm tròn màu đỏ tươi gắn trên cung ray, đường kính hiển thị $24\text{ px}$, vùng bắt cảm ứng ảo tối thiểu $50 \times 50\text{ px}$.
     - Nhãn đo góc quay: Hiển thị liên tục từ $0^\circ$ đến $180^\circ$ (không hiển thị số âm).
  3. **Khu vực dưới (Hộp khám phá sư phạm & Thanh công cụ GV):**
     - Vùng phản hồi tương tác: Khi góc $< 180^\circ$, hiển thị hướng dẫn kéo quay. Khi đạt mốc chuẩn hóa $180^\circ$, xuất hiện câu hỏi quan sát kèm 2 nút `[ CÓ ]` / `[ KHÔNG ]`.
     - Thanh nút công cụ: Nút **[ Đặt lại 0° ]** (to rõ cho học sinh) và Nút **[ Tự động quay (GV) ]** (chế độ hỗ trợ trình chiếu của giáo viên).

---

### 3. QUY ƯỚC TỌA ĐỘ GÓC VÀ MÔ HÌNH DỮ LIỆU 3 MẪU CHONG CHÓNG
Để bảo đảm tính nhất quán toán học và khớp tuyệt đối giữa mã code với hình ảnh trực quan trên màn hình:

- **Quy ước hệ góc SVG chuẩn:**
  - Tâm quay $O$: $(x_0, y_0) = (300, 300)$.
  - **Hướng $0^\circ$ (12 giờ):** Là hướng thẳng đứng **hướng lên trên** (dọc theo trục âm $y$ của SVG, vector chỉ phương $(0, -1)$).
  - **Chiều quay dương:** Theo chiều kim đồng hồ (Clockwise).
    + $0^\circ$: Hướng lên trên (12 giờ).
    + $90^\circ$: Hướng sang phải (3 giờ).
    + $180^\circ$: Hướng xuống dưới (6 giờ).
    + $270^\circ$: Hướng sang trái (9 giờ).
- **Quy ước dựng cánh gốc (`baseBladePath`):**
  - Cánh gốc được vẽ xuất phát từ gốc $(0, 0)$, thân cánh vươn thẳng đứng **lên trên** theo đúng hướng $0^\circ$ với bán kính $R = 180\text{ px}$.
  - Hình dạng cánh chuẩn SGK: Gốc thắt hẹp ở tâm $O$, nở rộng dạng quạt cong sang hai bên và bo tròn mút cánh.
  - Ví dụ SVG Path: `M 0 0 C 15 -30 45 -80 35 -140 C 25 -175 0 -185 0 -185 C 0 -185 -25 -175 -35 -140 C -45 -80 -15 -30 0 0 Z`.
- **Cấu hình góc các cánh cho 3 mẫu:**
  Khi vẽ, từng cánh được đặt vào vị trí bằng phép biến đổi: `transform="rotate(angle, 300, 300)"`.
  ```javascript
  const SHAPE_CONFIGS = {
    wings2: {
      id: 'wings2',
      name: 'Chong chóng 2 cánh',
      // 2 cánh thẳng hàng đối xứng qua O (đúng Hình 5.6 SGK): 1 cánh hướng lên, 1 cánh hướng xuống
      angles: [0, 180],
      hasCenterSymmetry: true,
      handleInitialAngle: 0 // Tay kéo xuất phát từ cánh phía trên (12 giờ)
    },
    wings3: {
      id: 'wings3',
      name: 'Chong chóng 3 cánh (Phản ví dụ)',
      // 3 cánh cách đều nhau 120°, có đúng 1 cánh hướng thẳng lên trên (12 giờ) khớp mô tả
      angles: [0, 120, 240], // Cánh 1: 0° (12h), Cánh 2: 120° (4h), Cánh 3: 240° (8h)
      hasCenterSymmetry: false,
      handleInitialAngle: 0 // Tay kéo xuất phát từ cánh phía trên (12 giờ)
    },
    wings4: {
      id: 'wings4',
      name: 'Chong chóng 4 cánh',
      // 4 cánh cách đều nhau đúng 90° (đúng Hình 5.7c SGK)
      angles: [0, 90, 180, 270], // 12h, 3h, 6h, 9h
      hasCenterSymmetry: true,
      handleInitialAngle: 0 // Tay kéo xuất phát từ cánh phía trên (12 giờ)
    }
  };
  ```
  *(Giải thích kiểm chứng mẫu 3 cánh: Khi quay $180^\circ$, cánh tại $0^\circ$ chuyển sang $180^\circ$ (chúc thẳng xuống dưới 6h), hai cánh còn lại chuyển sang $300^\circ$ và $60^\circ$. Vị trí phía trên $0^\circ$ hoàn toàn trống rỗng, làm lộ rõ bóng mờ viền xanh).*

---

### 4. CÁCH VẼ BÓNG MỜ VÀ HÌNH XOAY
- **Kiến trúc phân tầng 2 nhóm SVG (Two-Layer Architecture):**
  1. **Lớp bóng mờ vị trí ban đầu (`<g id="ghost-layer">`):**
     - Tạo ra một lần khi chọn mẫu hình.
     - Đồ họa: `stroke="#2563eb"`, `stroke-width="2.5"`, `stroke-dasharray="8,5"`, `fill="none"`, `opacity="0.45"`.
     - **Hoàn toàn tĩnh:** Đứng yên cố định ở góc xuất phát $0^\circ$ làm mốc đối chiếu khách quan.
  2. **Lớp hình thực thao tác (`<g id="active-layer">`):**
     - Chứa toàn bộ các cánh chong chóng màu cam đỏ: `fill="#ea580c"`, `fill-opacity="0.9"`, `stroke="#c2410c"`, `stroke-width="2"`.
     - Chuyển động xoay được áp dụng tập trung trên nhóm thẻ:  
       `transform="rotate(currentAngle, 300, 300)"`.
     - Hiệu năng tối đa $60\text{ fps}$, trình duyệt chỉ cập nhật ma trận biến đổi góc duy nhất.

---

### 5. CƠ CHẾ KÉO XOAY BẰNG CHUỘT VÀ CẢM ỨNG
- **Sử dụng Pointer Events API:**
  - Lắng nghe: `pointerdown`, `pointermove`, `pointerup`, `pointercancel`.
  - Trên thẻ SVG và phần tử tay kéo: Thiết lập thuộc tính CSS `touch-action: none;` để triệt tiêu hoàn toàn hành vi cuộn hoặc phóng to/thu nhỏ ngoài ý muốn trên bảng tương tác.
  - Sử dụng `handleElement.setPointerCapture(event.pointerId)` ngay khi chạm tay kéo, bảo đảm không bị mất tiêu điểm ngón tay kể cả khi học sinh kéo nhanh ra ngoài khung vẽ.
- **Cung ray định hướng và vị trí tay kéo:**
  - Một cung ray tròn nét đứt thanh mảnh (`stroke: #94a3b8; stroke-dasharray: 4,4; stroke-width: 2px`) được vẽ dẫn đường từ $0^\circ$ (12h) theo chiều kim đồng hồ đến $180^\circ$ (6h) với bán kính $R_{\text{handle}} = 195\text{ px}$.
  - Tọa độ tay kéo $(x_{\text{h}}, y_{\text{h}})$ luôn nằm chính xác trên cung ray này tương ứng với góc hiện tại $\theta$:
    $$x_{\text{h}} = 300 + R_{\text{handle}} \cdot \sin\left(\frac{\theta \cdot \pi}{180}\right)$$
    $$y_{\text{h}} = 300 - R_{\text{handle}} \cdot \cos\left(\frac{\theta \cdot \pi}{180}\right)$$
- **Thuật toán chiếu góc chống giật hình:**
  - Chuyển đổi tọa độ chạm sang hệ tọa độ SVG:
    ```javascript
    function getSVGPoint(event, svgElement) {
      const pt = svgElement.createSVGPoint();
      pt.x = event.clientX;
      pt.y = event.clientY;
      return pt.matrixTransform(svgElement.getScreenCTM().inverse());
    }
    ```
  - Tính góc tương đối từ tâm $O(300, 300)$ tới điểm chạm $(x, y)$:
    Vector: $dx = x - 300$, $dy = y - 300$.  
    Góc theo chiều kim đồng hồ so với hướng 12 giờ (trục âm $y$):
    $$\alpha = \text{atan2}(dx, -dy) \times \frac{180}{\pi}$$
    *(Hàm `atan2(dx, -dy)` cho giá trị $0^\circ$ tại 12h, $+90^\circ$ tại 3h, $\pm 180^\circ$ tại 6h, $-90^\circ$ tại 9h).*
  - **Khóa góc trong cung $0^\circ \to 180^\circ$:**
    + Nếu ngón tay di chuyển trong nửa bên phải ($dx \ge 0$ hoặc $\alpha \ge 0$): góc được lấy trực tiếp $\theta_{\text{raw}} = \alpha$.
    + Nếu ngón tay lệch sang nửa bên trái ($\alpha < 0$):
      * Nếu gần đỉnh trên ($\alpha > -90^\circ$): khóa chặt tại $0^\circ$.
      * Nếu gần đáy dưới ($\alpha \le -90^\circ$): khóa chặt tại $180^\circ$.
    + Giới hạn an toàn: $\theta = \max(0, \min(180, \theta_{\text{raw}}))$.
    + Nhãn hiển thị số đo góc: Luôn luôn nằm trong khoảng $[0^\circ, 180^\circ]$, tuyệt đối không xuất hiện số âm.

---

### 6. CHUẨN HÓA MỐC QUAY NỬA VÒNG (180°)
- **Quy tắc chuẩn hóa hiển thị:**
  - Nhằm triệt tiêu sai số phần cứng của màn hình cảm ứng, khi học sinh kéo ngón tay vào vùng rất gần $180^\circ$ (trong khoảng $178.5^\circ \le \theta \le 180^\circ$), hệ thống thực hiện chuẩn hóa giá trị góc thành đúng $180.0^\circ$.
  - **Bản chất sư phạm:** Đây là cơ chế **hỗ trợ căn đúng mốc nửa vòng**, giúp hình dừng đúng vị trí hình học chuẩn xác để học sinh dễ dàng quan sát đối chiếu.
  - **Không dùng cơ chế bắt dính tự động ("Snap"):** Chuyển động lướt đến $180^\circ$ diễn ra tự nhiên, không khựng giật, và **tuyệt đối không đi kèm bất kỳ hiệu ứng âm thanh hay viền sáng báo đúng/sai nào**.

---

### 7. LOGIC HIỂN THỊ CÂU HỎI VÀ LỜI DẪN QUAN SÁT SƯ PHẠM
Chuyển hóa hoàn toàn từ phong cách "chấm điểm trắc nghiệm" sang phong cách **"hỗ trợ quan sát và đối chiếu bằng chứng hình học"**:

- **Máy trạng thái tương tác:**
  - **`Trạng thái 1: Góc = 0°`**
    - Hướng dẫn thao tác: *"Chạm kéo điểm tròn đỏ theo cung tròn để quay nửa vòng (180°) quanh tâm O."*
    - Hộp câu hỏi nhận xét ẩn hoàn toàn.
  - **`Trạng thái 2: Đang kéo xoay (0° < Góc < 180°)`**
    - Cập nhật số đo góc: `Góc quay: X° / 180°`.
    - Bóng mờ đứng yên, hình thực xoay theo tay kéo. Hộp câu hỏi vẫn ẩn.
  - **`Trạng thái 3: Đạt đúng 180°`**
    - Tay kéo dừng ở cuối cung ray. Hình thực giữ nguyên trạng thái tĩnh tại góc $180^\circ$.
    - **Không có viền sáng, không đổi màu, không có chuông báo.**
    - Xuất hiện câu hỏi định hướng quan sát:  
      *"Sau khi quay nửa vòng quanh tâm O, hình có chồng khít lên bóng mờ ban đầu không?"*  
      kèm 2 nút lựa chọn: `[ CÓ ]` và `[ KHÔNG ]`.
  - **`Trạng thái 4: Sau khi chọn [CÓ] hoặc [KHÔNG]`**  
    Hệ thống đưa ra lời dẫn dắt quan sát khách quan, hỗ trợ giáo viên chốt kiến thức:
    - **Đối với mẫu 2 cánh và 4 cánh:**
      + *Nếu chọn [ CÓ ]:*  
        *"**Quan sát viền xanh:** Các cánh màu đỏ đã che khít hoàn toàn viền bóng mờ.  
        $\to$ Hình này **chồng khít với chính nó** sau khi quay nửa vòng quanh tâm O.  
        $\to$ **Kết luận:** Đây là hình có tâm đối xứng, điểm O là tâm đối xứng."*
      + *Nếu chọn [ KHÔNG ]:*  
        *"**Quan sát lại viền xanh:** Toàn bộ các mút cánh màu đỏ đều đã che kín viền nét đứt màu xanh, không còn phần bóng mờ nào bị lộ ra.  
        $\to$ Như vậy hình đã **chồng khít với chính nó** sau khi quay nửa vòng quanh tâm O.  
        $\to$ **Kết luận:** Đây là hình có tâm đối xứng, điểm O là tâm đối xứng."*
    - **Đối với mẫu 3 cánh (Phản ví dụ):**
      + *Nếu chọn [ KHÔNG ]:*  
        *"**Quan sát viền xanh:** Cánh phía trên khi quay nửa vòng đã chúc ngược xuống dưới, làm lộ rõ khoảng trống và đường viền xanh ban đầu ở phía trên.  
        $\to$ Hình **không chồng khít** với chính nó sau khi quay nửa vòng quanh tâm O.  
        $\to$ **Kết luận:** Chong chóng 3 cánh **không có tâm đối xứng**."*
      + *Nếu chọn [ CÓ ]:*  
        *"**Quan sát lại viền xanh:** Khoảng trống ở phía trên vẫn còn lộ rõ đường viền nét đứt màu xanh vì cánh ban đầu đã bị đảo xuống dưới.  
        $\to$ Hình **không chồng khít** với chính nó sau khi quay nửa vòng quanh tâm O.  
        $\to$ **Kết luận:** Chong chóng 3 cánh **không có tâm đối xứng**."*

---

### 8. CÁC YÊU CẦU KIỂM THỬ TỐI THIỂU (TEST CASES)
1. **Kiểm thử cảm ứng và khóa cuộn trang:** Thao tác vuốt kéo liên tục trên màn hình cảm ứng không gây hiện tượng trượt trang hay zoom khung nhìn.
2. **Kiểm thử dừng giữa chừng ($45^\circ, 90^\circ, 135^\circ$):** Nhả tay ở bất kỳ góc nào, hình giữ nguyên góc đó, câu hỏi [CÓ]/[KHÔNG] tuyệt đối không xuất hiện trước khi đạt $180^\circ$.
3. **Kiểm thử góc kéo ngoài cung:** Kéo ngón tay sang trái hoặc kéo giật mạnh: tay kéo vẫn bám mượt mà trên cung $0^\circ \to 180^\circ$, không nhảy góc âm, không giật hình.
4. **Kiểm thử độ chính xác thị giác tại $180^\circ$:**  
   - Mẫu 2 cánh và 4 cánh che phủ hoàn hảo viền bóng mờ.  
   - Mẫu 3 cánh lộ rõ khoảng trống phía trên (cánh chúc xuống dưới).
5. **Kiểm thử chuyển đổi tab:** Chọn tab mẫu hình khác tự động trả góc về $0^\circ$, đặt lại trạng thái ban đầu, xóa bỏ hộp nhận xét cũ.
6. **Kiểm thử nút Tự động quay (Auto Play):** Chỉ dùng hỗ trợ trình chiếu: hình quay đều trong $2.0$ giây đến $180^\circ$ rồi kích hoạt câu hỏi quan sát.
7. **Kiểm thử vận hành Offline:** File HTML mở trực tiếp từ ổ cứng (`file:///`), hoạt động trơn tru không cần kết nối mạng.

---

### 9. NHỮNG LỖI CẦN TRÁNH KHI LẬP TRÌNH
1. **Tuyệt đối không dùng thư viện ngoài:** Không引入 font hay script trực tuyến.
2. **Không để nhầm lẫn hệ tọa độ góc:** Bắt buộc tuân thủ quy ước: hướng 12 giờ là $0^\circ$, chiều kim đồng hồ là chiều tăng, cánh gốc vươn lên trên.
3. **Không để hiển thị số đo góc âm:** Thuật toán chuẩn hóa phải luôn bảo đảm hiển thị trong khoảng $0^\circ \le \theta \le 180^\circ$.
4. **Không kích hoạt viền sáng báo đáp án trước:** Tuyệt đối không thêm hiệu ứng sáng viền trước khi học sinh bấm chọn [CÓ] hoặc [KHÔNG].
5. **Không đưa yếu tố game hóa:** Không tính điểm, không có âm thanh reo hò, giữ đúng chuẩn mực sư phạm.
