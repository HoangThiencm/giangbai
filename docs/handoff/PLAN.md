# PLAN: Nâng Cấp Toàn Diện Game "Đua Xe F1 Mario Kart - Đại Chiến 4 Tổ" (game-racing.html)

## 1. Phân Tích Yêu Cầu & Định Hướng Nâng Cấp

### Vấn đề hiện tại:
- `game-racing.html` hiện tại chỉ có 4 biểu tượng emoji trượt ngang trên nền xám đơn điệu.
- Lối chơi lần lượt từng tổ khiến 3 tổ còn lại phải ngồi chờ, làm mất tính gắn kết và thi đua đồng đội sôi nổi trong lớp học.
- Thiếu cảm giác tốc độ, không có âm thanh gầm rú của động cơ, không có vạch xuất phát/vạch đích thực thụ hay các yếu tố vật phẩm kịch tính.

### Định hướng mới:
Biến `game-racing.html` thành trò chơi **"ĐUA XE F1 MARIO KART - ĐẠI CHIẾN 4 TỔ"** bùng nổ không khí lớp học:
1. **Đồ họa tốc độ cao (Arcade F1 Canvas/CSS Engine):** Đường đua nhựa đường 4 làn xe với vạch sơn kẻ đường cuộn chuyển động liên tục, 4 siêu xe F1 đồ họa sắc nét, hiệu ứng lửa phụt đuôi ống xả Nitro Turbo 🔥, khói lốp xe drift 💨, đèn xuất phát 5 đèn đỏ F1 chuẩn quốc tế.
2. **Cơ chế thi đấu Cả 4 Tổ Cùng Tham Gia (Simultaneous Team Battle):** Mỗi câu hỏi hiện ra với đồng hồ đếm ngược (30 giây), cả 4 tổ cùng thảo luận. Giáo viên tích chọn các tổ có đáp án đúng $\rightarrow$ Tất cả các xe trả lời đúng CÙNG BỐC ĐẦU PHÓNG VỌT LÊN TRƯỚC trong tiếng động cơ gầm rú!
3. **Hộp vật phẩm ngẫu nhiên Mario Kart (Mystery Boxes 🎁):** Xuất hiện ngẫu nhiên giúp lật ngược thế cờ (Tên lửa Nitro 🚀, Khiên bảo vệ 🛡️, Vỏ chuối trượt bánh 🍌, Tia sét tăng tốc ⚡).
4. **Hệ thống âm thanh sống động (Web Audio API):** Tiếng rồ ga *Vroom Vroom!*, rít lốp ôm cua *Screeech!*, còi xuất phát 5 đèn F1, kèn chiến thắng Fanfare và bục vinh quang Podium 3 bậc (Hạng 1 🥇, Hạng 2 🥈, Hạng 3 🥉).

---

## 2. Nhiệm Vụ Chi Tiết Của Coder

Coder sẽ nâng cấp trực tiếp tệp: **`game-racing.html`**.

---

### Bước 1: Nâng cấp Giao diện Đường Đua & Hiệu Ứng F1
Thay thế khối đường đua đơn điệu cũ bằng hệ thống đường đua F1 hiện đại:
- **Nền đường đua:** Nhựa đường xám đen (`#0f172a`), các vạch sơn trắng phân làn có animation lướt nhanh liên tục (`trackMove 0.4s linear infinite`), hàng rào bảo hộ đỏ-trắng và khán đài cờ hoa 2 bên.
- **Đèn xuất phát F1 (Starting Lights):** Khi bắt đầu cuộc đua, hiển thị dàn 5 đèn đỏ lần lượt bật sáng (`🔴 🔴 🔴 🔴 🔴`) kèm tiếng đếm ngược, sau đó đồng loạt chuyển xanh (`🟢 🟢 🟢 🟢 🟢 GO!`) kích hoạt cuộc đua.
- **4 Siêu xe F1 sắc nét:**
  - 🔴 **Tổ 1 - Scuderia Red:** Đỏ rực lửa
  - 🔵 **Tổ 2 - Cyan Lightning:** Xanh tia chớp
  - 🟡 **Tổ 3 - Golden Thunder:** Vàng sấm sét
  - 🟣 **Tổ 4 - Neon Phantom:** Tím bóng ma
  *(Mỗi xe được thiết kế dạng SVG/CSS sắc nét với cánh gió trước sau, buồng lái, lốp xe thể thao).*
- **Hiệu ứng tốc độ cao:**
  - Lửa phụt đuôi ống xả Nitro Turbo xanh/cam khi bứt tốc (`nitro-flame`).
  - Vệt khói lốp xe trắng cuộn phía sau (`smoke-trail`).
  - Camera bám theo khoảng cách dẫn đầu về vạch đích ca-rô trắng đen (`finish-line`).

---

### Bước 2: Cơ Chế Cả 4 Tổ Cùng Tham Gia (Simultaneous Battle)
Tái cấu trúc luồng câu hỏi:
1. **Hiển thị câu hỏi & Đếm ngược:**
   - Câu hỏi trắc nghiệm (với đầy đủ KaTeX qua `<MathText>`).
   - Đồng hồ đếm ngược 30 giây (có thể điều chỉnh 15s/30s/45s) kèm thanh tiến trình co dần.
   - Âm thanh tích tắc nhẹ nhàng kích thích sự tập trung thảo luận của cả 4 tổ.
2. **Bảng chấm điểm đa tổ (Multi-Team Scoring):**
   - Dưới câu hỏi, hiển thị 4 nút bấm to nổi bật tương ứng 4 tổ:
     * `[ 1. Tổ 1 Đỏ ]`
     * `[ 2. Tổ 2 Xanh ]`
     * `[ 3. Tổ 3 Vàng ]`
     * `[ 4. Tổ 4 Tím ]`
   - Giáo viên chỉ cần click vào các tổ có đáp án đúng (hoặc ấn phím tắt `1`, `2`, `3`, `4` trên bàn phím), nút sẽ sáng lên màu xanh lá kèm tick `✓`.
   - Bấm nút **"XÁC NHẬN BỨT TỐC 🏎️💨"**:
     * Tất cả các xe được tick chọn ĐỒNG LOẠT VỌT TIẾN LÊN PHÍA TRƯỚC!
     * Tổ nào có chuỗi đúng liên tiếp $\ge 2$ sẽ kích hoạt **SUPER NITRO** (vọt xa gấp đôi kèm lửa phụt rực rỡ).
     * Tổ nào trả lời sai thì xe rung lắc nhẹ, xịt khói xám.

---

### Bước 3: Hộp Vật Phẩm May Mắn (Mario Kart Mystery Boxes 🎁)
Cứ sau mỗi 2–3 câu hỏi, trên đường đua xuất hiện ngẫu nhiên các hộp quà `?` xoay tròn:
- Khi xe chạm hộp quà:
  - 🚀 **Tên lửa Nitro:** Xe tự động vọt thêm 1 đoạn lớn, vượt qua các xe khác.
  - 🛡️ **Khiên bảo vệ:** Nhận lá chắn phát sáng, câu sau nếu sai không bị tụt lại.
  - 🍌 **Vỏ chuối trơn:** Đặt bẫy khiến xe của 1 tổ đối thủ bị xoay trượt 360 độ và chậm lại 1 nhịp.
  - ⚡ **Tia sét tăng tốc:** Nhân đôi điểm số cho tổ trong lượt tiếp theo.
*(Có thể bật/tắt tính năng Hộp vật phẩm trong phần Cài đặt của giáo viên).*

---

### Bước 4: Hệ Thống Âm Thanh Web Audio API (100% Offline)
Tích hợp bộ âm thanh thuần Web Audio:
- `soundEngine.f1Lights()`: Tiếng bíp bíp theo nhịp 5 đèn F1 và tiếng còi bính boong khi đèn xanh bật.
- `soundEngine.engineRev()`: Tiếng động cơ rồ ga *Vroom Vroom!* (dao động sóng sawtooth 90Hz $\rightarrow$ 350Hz kèm bộ lọc lowpass).
- `soundEngine.tireScreech()`: Tiếng rít lốp bốc khói *Screeech!*.
- `soundEngine.nitroBoost()`: Tiếng xả khí nén và phụt lửa Nitro *Whoooosh!*.
- `soundEngine.podiumFanfare()`: Giai điệu kèn mừng chiến thắng rộn rã khi xe cán vạch đích.
- Nút Bật/Tắt âm thanh ở góc trên màn hình.

---

### Bước 5: Bục Vinh Quang Podium 3 Bậc (Victory Podium)
Khi có xe đầu tiên chạm vạch đích:
- Pháo hoa và pháo giấy confetti nổ rực rỡ (`canvas-confetti`).
- Kèn Fanfare chiến thắng vang lên.
- Hiển thị bục vinh quang 3 bậc chuẩn thể thao:
  * 🥇 **Bậc 1 (Vàng - Cao nhất):** Tổ vô địch cuộc đua, cúp vàng lấp lánh.
  * 🥈 **Bậc 2 (Bạc):** Tổ về nhì.
  * 🥉 **Bậc 3 (Đồng):** Tổ về ba.
  * 🏅 **Tổ 4:** Bảng danh dự "Tinh thần thi đua".
- Bảng tổng kết chi tiết: Số câu đúng từng tổ, thời gian phản xạ, danh hiệu "Vua tốc độ", "Chiến thần Drift".
- Nút "Đua lại" và "Về menu".

---

## 3. Kế Hoạch Xác Minh (Verification Plan)
1. **Khởi chạy `game-racing.html`:** Xác nhận đèn 5 đèn đỏ F1 bật tắt mượt mà, đường đua nhựa đường cuộn chuyển động sống động.
2. **Kiểm tra cơ chế thi đua cả 4 tổ:** Xác nhận cả 4 tổ cùng tham gia trả lời câu hỏi, giáo viên tích chọn nhiều tổ cùng lúc và các xe đều bứt tốc đồng thời.
3. **Kiểm tra âm thanh:** Xác nhận tiếng động cơ, còi xuất phát, tiếng rít lốp và kèn chiến thắng hoạt động tốt không bị rè hay lỗi.
4. **Kiểm tra vạch đích và Podium:** Xác nhận xe về nhất kích hoạt pháo giấy confetti, bục vinh quang 3 bậc hiển thị chính xác thứ hạng 4 tổ.
