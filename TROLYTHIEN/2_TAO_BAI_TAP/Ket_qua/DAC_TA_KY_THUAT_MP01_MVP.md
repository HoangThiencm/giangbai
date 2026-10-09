# BẢN ĐẶC TẢ KỸ THUẬT MP-01 (MVP TẦNG 1)
## CẮT GHÉP DIỆN TÍCH HÌNH BÌNH HÀNH THÀNH HÌNH CHỮ NHẬT
**Hệ thống Trợ lý Sư phạm Hoàng Thiên — Nhánh 2: Tạo bài tập & Học liệu tương tác**  
**Giai đoạn:** Đặc tả kỹ thuật MVP (Chuẩn bị lập trình)  
**Mã tài liệu:** `DAC_TA_KY_THUAT_MP01_MVP.md`  
**Trạng thái:** Bản thiết kế kỹ thuật chi tiết — Sẵn sàng thẩm định — Chưa viết mã HTML  

---

### I. KIẾN TRÚC TỆP & CÔNG NGHỆ (OFFLINE STANDALONE)

1. **Định dạng tệp:**
   - Một tệp duy nhất: `MP01_Dien_Tich_Hinh_Binh_Hanh.html`.
   - Vị trí lưu trữ: `TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua/MP01_Dien_Tich_Hinh_Binh_Hanh.html`.
   - Mở và chạy trực tiếp qua giao thức tệp cục bộ (`file:///`) trên mọi trình duyệt hiện đại (Chrome, Edge, Firefox, Cốc Cốc, Safari).
   - **Tự chứa 100% (Zero Dependencies):** Tuyệt đối không dùng thư viện ngoài (không jQuery, không React, không D3.js, không Bootstrap), không nạp phông chữ Google Fonts hay tài nguyên từ CDN. Phông chữ sử dụng hệ thống chuẩn: `system-ui, -apple-system, Segoe UI, Roboto, sans-serif`.

2. **Công nghệ đồ họa & Tương tác:**
   - **Đồ họa Vector SVG:** Thẻ `<svg>` chuẩn với `viewBox="0 0 700 480"`, co giãn sắc nét trên mọi màn hình (máy tính xách tay, máy chiếu lớp học, bảng tương tác thông minh 4K).
   - **Tương tác Pointer Events API:** Sử dụng đồng thời `pointerdown`, `pointermove`, `pointerup`, `pointercancel`.
   - **Khóa cuộn trang:** Khai báo CSS `touch-action: none;` trên vùng SVG và thanh trượt để chống tuyệt đối hiện tượng ngón tay làm cuộn hoặc phóng to trang web khi dạy học.
   - **Bắt điểm chạm:** Sử dụng `element.setPointerCapture(e.pointerId)` để ngón tay không bị trượt mất đối tượng khi thao tác nhanh.

---

### II. HỆ TỌA ĐỘ TOÁN HỌC & LƯỚI Ô VUÔNG CHUẨN XÁC

Để đảm bảo mô phỏng không bị lệch dù chỉ $1\text{ px}$, hệ tọa độ toán học được thiết lập theo tỷ lệ lưới ô vuông 1:1 tương thích nguyên bản SGK Toán 6 Tập 1 (H.4.15a và H.4.15b):

```
     0   50  100  150  200  250  300  350  400  450  500  550  600  650  700 (X)
  0 +---+---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
 50 +---+---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   | A +===+===+===+===+ B |   |   |   |   |  y = 100 (Đáy trên, rộng 4 ô)
100 +---+---+---+---+---|---|---|---|---|---+---+---+---+---+
    |   |   |   |   | | |   |   |   |   | | |   |   |   |   |  h = 3 ô = 150 px
150 +---+---+---+---+---|---|---|---|---|---+---+---+---+---+
    |   |   |   |   | | |   |   |   |   | | |   |   |   |   |
200 +---+---+---+---+---|---|---|---|---|---+---+---+---+---+
    |   |   |   | D | | H |   |   |   | C | | H'|   |   |   |  y = 250 (Đáy dưới, rộng 4 ô)
250 +---+---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
(Y)
```

1. **Thông số đơn vị lưới (Grid Unit):**
   - Độ dài cạnh 1 ô vuông: $u = 50\text{ px}$.
   - Khung lưới vẽ từ $X_{\min} = 50\text{ px}$ đến $X_{\max} = 650\text{ px}$ (12 cột); từ $Y_{\min} = 50\text{ px}$ đến $Y_{\max} = 350\text{ px}$ (6 hàng).
   - Đường kẻ lưới mảnh: nét vẽ `stroke="#e2e8f0"`, độ dày `stroke-width="1"`.
   - Vạch tọa độ đáy nằm ở dòng kẻ $Y = 250\text{ px}$; vạch đỉnh nằm ở dòng kẻ $Y = 100\text{ px}$.

2. **Bảng tọa độ toán học chính xác các đỉnh (Tuyệt đối không có sai số):**

| Điểm | Vai trò trong hình học | Tọa độ SVG $(X, Y)$ | Ghi chú vị trí lưới |
| :---: | :--- | :---: | :--- |
| **D** | Đỉnh dưới bên trái hình bình hành ban đầu | $(150, 250)$ | Cột 3, Hàng 5 |
| **H** | Chân đường cao hạ từ đỉnh $A$ xuống cạnh đáy | $(200, 250)$ | Cột 4, Hàng 5 ($DH = 1\text{ ô} = 50\text{ px}$) |
| **C** | Đỉnh dưới bên phải hình bình hành ban đầu | $(350, 250)$ | Cột 7, Hàng 5 ($DC = a = 4\text{ ô} = 200\text{ px}$) |
| **A** | Đỉnh trên bên trái hình bình hành ban đầu | $(200, 100)$ | Cột 4, Hàng 2 ($AH = h = 3\text{ ô} = 150\text{ px}$) |
| **B** | Đỉnh trên bên phải hình bình hành ban đầu | $(400, 100)$ | Cột 8, Hàng 2 ($AB = a = 4\text{ ô} = 200\text{ px}$) |
| **H'**| Chân đường cao mới của hình chữ nhật sau khi ghép | $(400, 250)$ | Cột 8, Hàng 5 ($H H' = a = 4\text{ ô} = 200\text{ px}$) |

3. **Kiểm tra tính chất hình học:**
   - Cạnh đáy dưới $DC$: đi từ $(150, 250)$ đến $(350, 250) \implies$ nằm ngang, độ dài $= 200\text{ px} = 4\text{ ô} = a$.
   - Cạnh đỉnh trên $AB$: đi từ $(200, 100)$ đến $(400, 100) \implies$ nằm ngang, độ dài $= 200\text{ px} = 4\text{ ô} = a$.
   - Cạnh bên trái $DA$: vector $\vec{DA} = (200 - 150, 100 - 250) = (+50, -150)$ (sang phải 1 ô, lên trên 3 ô).
   - Cạnh bên phải $CB$: vector $\vec{CB} = (400 - 350, 100 - 250) = (+50, -150)$ (sang phải 1 ô, lên trên 3 ô).
   - **Kết luận hình học:** $\vec{DA} = \vec{CB} \implies DA \parallel CB$ và $DA = CB$. Các tọa độ được thiết kế để khi tịnh tiến tam giác đến vị trí đích, hình ghép khít thành hình chữ nhật trên lưới.
   - **Ghi chú nguồn tọa độ:** *Hệ tọa độ này mô hình hóa hình SGK với giả định hình bình hành có đáy 4 ô, chiều cao 3 ô, độ lệch ngang 1 ô như ảnh trang SGK đã cung cấp.*

---

### III. CẤU TRÚC ĐỐI TƯỢNG HÌNH HỌC TRONG SVG

Đồ họa SVG được phân chia thành 6 lớp (Layers) rõ ràng theo thứ tự từ dưới lên trên:

1. **Lớp 1 — Lưới ô vuông nền (Grid Layer):**
   - Tập hợp các đường thẳng `<line>` ngang và dọc cách nhau đều đặn $50\text{ px}$.
   - Màu sắc: `#e2e8f0` (xám xanh nhạt), không gây chói mắt.

2. **Lớp 2 — Bóng mờ vị trí ban đầu của tam giác cắt (Ghost Outline Layer):**
   - Đa giác `<polygon points="150,250 200,250 200,100" />`.
   - Thuộc tính đồ họa: `fill="rgba(226, 232, 240, 0.45)"`, viền nét đứt `stroke="#94a3b8"`, `stroke-dasharray="6,4"`, độ dày `2px`.
   - Luôn hiển thị cố định để học sinh đối chiếu: khi tam giác di chuyển đi nơi khác, bóng mờ vẫn nhắc nhở vị trí xuất phát của nó.

3. **Lớp 3 — Phần còn lại của hình bình hành (Fixed Remaining Polygon):**
   - Đa giác `<polygon points="200,250 350,250 400,100 200,100" />`.
   - Màu tô: Nền lam nhạt trang nhã `fill="#e0f2fe"`, viền xanh đậm `stroke="#0284c7"`, độ dày `2.5px`.
   - Đối tượng này cố định hoàn toàn $100\%$ trong suốt quá trình học sinh thao tác.

4. **Lớp 4 — Tam giác vuông thao tác trượt (Sliding Triangle):**
   - Đa giác `<polygon points="150,250 200,250 200,100" />` đặt trong nhóm `<g id="slidingTriangle">`.
   - Vị trí tịnh tiến: Điều khiển bằng thuộc tính `transform="translate(dx, 0)"`.
   - Màu tô: Nền hổ phách/vàng ấm `fill="#fef3c7"`, viền cam đậm `stroke="#d97706"`, độ dày `2.5px`.
   - *Tác dụng sư phạm:* Màu sắc phân biệt giúp học sinh dễ dàng theo dõi chuyển động dời hình của mảnh tam giác.

5. **Lớp 5 — Ký hiệu sư phạm & Đường gióng ban đầu (Labels & Height):**
   - Đường cao $AH$: `<line x1="200" y1="100" x2="200" y2="250" stroke="#ef4444" stroke-width="2" stroke-dasharray="5,4" />`.
   - Ký hiệu góc vuông tại $H$: Khung vuông nhỏ cạnh $12\text{ px}$ tại góc $(200, 250)$ (`<path d="M 200 238 L 212 238 L 212 250" />`).
   - Nhãn chữ $h$: Đặt tại tọa độ $(185, 180)$, màu đỏ đậm `#dc2626`, phông in nghiêng `font-weight="bold"`.
   - Nhãn chữ $a$: Đặt dưới cạnh đáy tại $(250, 275)$, màu xanh đậm `#0369a1`, kèm mũi tên 2 đầu chỉ độ dài đáy $4\text{ ô}$.

6. **Lớp 6 — Kích thước hình chữ nhật mới (Chỉ hiện khi đạt 100%):**
   - Sau khi ghép thành hình chữ nhật $H H' B A$:
     + Đường gióng đáy mới: Kích thước từ $X = 200$ đến $X = 400$, nhãn *“Chiều dài = a (4 ô)”*.
     + Đường gióng cạnh đứng mới: Kích thước từ $Y = 100$ đến $Y = 250$ tại $X = 400$, nhãn *“Chiều rộng = h (3 ô)”*.
     + Ban đầu ẩn hoàn toàn (`opacity: 0`), chuyển đổi mượt sang hiển thị (`opacity: 1`) khi hoàn tất ghép.

---

### IV. CƠ CHẾ KÉO CƠ HỌC & ĐỘNG HỌC THANH TRƯỢT (MECHANICAL SLIDER)

1. **Khoảng biến thiên dời hình:**
   - Biến trạng thái: $t \in [0, 1]$ (tương ứng $0\% \to 100\%$).
   - Quãng dời ngang: $\Delta X = t \times 200\text{ px}$ (chính xác bằng độ dài cạnh đáy $a = 4\text{ ô} \times 50\text{ px}$).
   - Độ dời đứng: $\Delta Y \equiv 0\text{ px}$ (tuyệt đối không cho di chuyển tự do lên/xuống).

2. **Thanh trượt điều khiển vật lý (Physical Track & Handle):**
   - Bố trí thanh trượt trực quan phía dưới khung hình:
     + Rãnh trượt: Đường nằm ngang từ $X_{\text{start}} = 150$ đến $X_{\text{end}} = 350$ (độ dài $200\text{ px}$), tại độ cao $Y = 320\text{ px}$.
     + Tay kéo tròn màu đỏ: Thẻ `<circle cx="..." cy="320" r="24" fill="#ef4444" stroke="#ffffff" stroke-width="4" />`.
     + **Kích thước vùng chạm lớn (Touch Target):** Đường kính $48\text{ px} - 52\text{ px}$, hỗ trợ hoàn hảo cho ngón tay học sinh lớp 6 trên màn hình cảm ứng hoặc bảng thông minh.
   - **Quy tắc cơ học tự nhiên:**
     + Bỏ tính năng nhấp chuột vào rãnh để nhảy vị trí.
     + Bắt buộc học sinh phải chạm giữ tay kéo và rê từ từ từ trái sang phải.

3. **Chuẩn hóa dung sai cảm ứng (Tolerance Normalization):**
   - Nhằm triệt tiêu sai số cảm ứng phần cứng khi ngón tay gần chạm đích:
     $$\text{Nếu } \Delta X \ge 195\text{ px } (t \ge 0.975) \implies \text{Hệ thống tự động chuẩn hóa } t = 1.0 \ (\Delta X = 200\text{ px}).$$
   - Quá trình chuẩn hóa êm ái, không giật cục ("Snap"), không chuông reo báo trước.

4. **Khóa trạng thái quan sát tại đích (Goal State Locking):**
   - Khi $t = 1.0$ (tam giác vuông đã áp khít hoàn toàn vào cạnh bên phải tạo thành hình chữ nhật khép kín):
     + Hệ thống đặt cờ `isLocked = true`.
     + Tay kéo đỏ mờ nhẹ (`opacity: 0.5; pointer-events: none;`).
     + Khóa toàn bộ thao tác kéo ngược.
     + Mục đích: Giữ hình chữ nhật tĩnh tuyệt đối, chống rung giật ngón tay làm mất hoặc chập chờn hộp câu hỏi.
   - Thao tác duy nhất mở khóa: Bấm nút `[ ↺ Đặt lại ban đầu ]`.

---

### V. TRẠNG THÁI HIỂN THỊ & HỘP QUAN SÁT SƯ PHẠM 2 TẦNG

Toàn bộ tiến trình dạy học qua phần mềm tuân thủ 4 mốc trạng thái:

```
[Mốc 1: 0%]            [Mốc 2: 1%-99%]          [Mốc 3: 100%]           [Mốc 4: Chốt bài]
Hình bình hành  --->   Đang trượt     --->   Hình chữ nhật khít  --->  Hiện lời giải thích
Hiện hướng dẫn         Bóng mờ vị trí cũ     Khóa kéo (Lock)           Hiện công thức S=a.h
Chưa có câu hỏi        Chưa có câu hỏi       Hiện 2 tầng câu hỏi       Mở nút Đặt lại
```

1. **Mốc 1 ($t = 0$ — Ban đầu):**
   - Hiển thị hình bình hành nguyên vẹn, đường cao nét đứt $h$, cạnh đáy $a$.
   - Tay kéo ở vị trí $0\%$.
   - Lời dẫn gợi mở: *“Chạm giữ tay kéo màu đỏ và trượt sang phải để cắt ghép hình.”*

2. **Mốc 2 ($0 < t < 1$ — Đang thao tác):**
   - Tam giác màu vàng trượt dần sang phải theo tay kéo.
   - Bóng mờ vị trí cũ màu xám nét đứt xuất hiện rõ nét.
   - Lưới ô vuông bên dưới giúp quan sát tiến trình dời hình.
   - Tuyệt đối không hiển thị câu hỏi hay gợi ý giữa chừng.

3. **Mốc 3 ($t = 1.0$ — Đạt đích $100\%$):**
   - Tam giác vuông ghép khít vào phần khuyết bên phải, tạo thành hình chữ nhật $H H' B A$ hoàn chỉnh trên lưới.
   - Khóa kéo tại đích (`isLocked = true`).
   - Hiển thị **Hộp quan sát trung tính** (nền `#f8fafc`, viền xám `#cbd5e1`, không dùng viền xanh lá gợi ý trước):
     > *Câu hỏi: “Khi cắt và ghép lại như vậy, diện tích hình có thay đổi không?”*  
     > - Nút 1: `[ Không thay đổi ]`
     > - Nút 2: `[ Có thay đổi ]`

4. **Mốc 4 (Sau khi học sinh bấm chọn nhận xét):**
   - Hệ thống phản hồi bằng lời dẫn giải thích khách quan:
     > *“Ta chỉ cắt và ghép lại, không thêm bớt phần nào nên diện tích không đổi. Trên lưới, hình chữ nhật mới có chiều dài bằng đáy a, chiều rộng bằng chiều cao h.”*
   - Sau đó hiển thị công thức chốt kiến thức:
     $$\mathbf{S = a \cdot h}$$
   - Nút `[ ↺ Đặt lại ban đầu ]` sáng lên cho phép thực hiện lại thao tác.

---

### VI. CÔNG CỤ TRÌNH CHIẾU DÀNH CHO GIÁO VIÊN (TEACHER AUTO-PLAY)

1. **Nút điều khiển:** `[ 🎬 Tự động ghép (GV) ]` bố trí gọn gàng tại thanh công cụ phụ dưới đáy màn hình.
2. **Cơ chế diễn hoạt mượt mà:**
   - Thời gian trượt: $2.5\text{ giây}$.
   - Tốc độ: Hàm làm chậm hai đầu `easeInOutQuad(progress)` giúp học sinh quan sát rõ khoảnh khắc bắt đầu tách và khoảnh khắc ghép khít.
   - Tự động dừng tại $100\%$ và hiển thị hộp câu hỏi để giáo viên điều hành lớp học thảo luận.

---

### VII. BẢNG MÃ MÀU SƯ PHẠM TRUNG TÍNH (COLOR SYSTEM)

| Thành phần | Mã màu Hex | Ý nghĩa sư phạm |
| :--- | :---: | :--- |
| **Nền trang** | `#f8fafc` | Trung tính, dịu mắt, chống lóa trên máy chiếu |
| **Lưới ô vuông** | `#e2e8f0` | Mảnh, rõ từng ô để đếm, không gây rối mắt |
| **Phần cố định hình bình hành** | `#e0f2fe` (viền `#0284c7`) | Lam nhạt dịu mát, thể hiện phần khung vững chắc |
| **Tam giác trượt** | `#fef3c7` (viền `#d97706`) | Vàng hổ phách nổi bật, tập trung thị giác vào chuyển động |
| **Bóng mờ vị trí cũ** | `rgba(226,232,240,0.45)` (viền `#94a3b8`) | Nét đứt nhắc nhở vị trí ban đầu |
| **Đường cao h** | `#ef4444` | Đỏ nổi bật, phân biệt rõ với các cạnh của hình |
| **Tay kéo cảm ứng** | `#ef4444` (viền `#ffffff`) | Điểm nhấn trực giác mời gọi tương tác chạm |
| **Hộp câu hỏi nhận xét** | `#ffffff` (viền `#cbd5e1`) | Trung tính tuyệt đối, không tiết lộ kết quả sớm |
| **Nút lựa chọn** | `#f1f5f9` (chữ `#1e293b`) | Trung tính, biến đổi màu xanh đậm nhẹ nhàng khi chọn |

---

### VIII. MA TRẬN KIỂM THỬ THỰC ĐỊA TRÊN THIẾT BỊ (TEST MATRIX)

Bản code khi hoàn thành bắt buộc phải vượt qua 6 bài test kiểm định:

| STT | Tình huống kiểm thử | Hành vi kỳ vọng |
| :---: | :--- | :--- |
| **1** | Mở tệp offline qua `file:///` | Trang tải tức thì $< 0.2\text{s}$, không báo lỗi thiếu thư viện hay phông chữ. |
| **2** | Kéo tay trượt từ $0\% \to 100\%$ | Tam giác di chuyển mượt mà 60fps, không rung lắc, bóng mờ vị trí cũ hiển thị đầy đủ. |
| **3** | Độ khít tại $100\%$ | Cạnh huyền tam giác trùng khít $100\%$ với cạnh bên phải, không để lộ khe hở hay đường viền lệch ô. |
| **4** | Khóa trạng thái tại đích | Khi đạt $100\%$, ngón tay không thể kéo ngược; hình tĩnh tuyệt đối. |
| **5** | Đặt lại ban đầu | Bấm `[ ↺ Đặt lại ]`, hình ảnh và tay kéo trở về $0\%$ ngay lập tức, mở khóa tương tác. |
| **6** | Thao tác cảm ứng bảng thông minh | Chạm giữ và vuốt trên màn hình không làm cuộn trang web hay phóng to trình duyệt. |

---

### IX. KẾT LUẬN & TRẠNG THÁI BÀN GIAO

- Bản đặc tả kỹ thuật này đã chốt tọa độ toán học chi tiết từng pixel, bảo đảm tính khép kín hình học tuyệt đối ($DA \parallel CB$, $a = 4\text{ ô}$, $h = 3\text{ ô}$, quãng trượt $= 200\text{ px} = a$).
- **Cam kết kỷ luật quy trình:** Toàn bộ mã nguồn HTML/JS **chưa được viết**. Đang chờ Thầy Hoàng Thiên thẩm định và phê duyệt bản Đặc tả kỹ thuật này trước khi chuyển sang bước code file mẫu đầu tiên!
