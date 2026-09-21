# PLAN: Nâng Cấp Toàn Diện Game "Đua Vịt Ngẫu Nhiên" Gọi Học Sinh (game-treasure.html)

## 1. Phân Tích Yêu Cầu & Mục Tiêu Sư Phạm

### Vấn đề hiện tại:
- `game-treasure.html` hiện tại chỉ là bài trắc nghiệm thông thường từng câu; mỗi câu đúng thì 1 con vịt tiến 1 bước trong bảng danh sách tĩnh dạng thẻ emoji. Trò chơi bị khô cứng, đơn điệu, không tạo được cảm giác một cuộc đua thực sự.

### Yêu cầu mới của giáo viên:
- Đây là trò chơi **"ĐUA VỊT NGẪU NHIÊN" (Random Duck Race Picker)** chuyên dụng để **gọi học sinh ngẫu nhiên** trong lớp:
  1. Cả lớp (30–45 học sinh) được gán mỗi em một chú vịt mang tên mình cùng xuất phát trên dòng sông.
  2. Bấm "Bắt đầu đua" $\rightarrow$ Đếm ngược 3.. 2.. 1.. TẤT CẢ các con vịt cùng bơi đua tự động trong thời gian thực (8–15 giây).
  3. Cơ chế đua kịch tính: các chú vịt bứt tốc ngẫu nhiên, vượt mặt nhau sít sao, tạo sự hồi hộp đỉnh điểm cho cả lớp.
  4. Chú vịt cán đích đầu tiên: Pháo hoa, nhạc chiến thắng, vinh danh học sinh may mắn được gọi lên bảng/trả lời câu hỏi.
  5. Hỗ trợ sư phạm: Cho phép hiện câu hỏi kiểm tra đính kèm (nếu có) hoặc loại học sinh đã được gọi khỏi lượt sau để không bị trùng lặp.

---

## 2. Nhiệm Vụ Chi Tiết Của Coder

Coder sẽ sửa đổi chính tại tệp: **`game-treasure.html`** (và cập nhật tên/mô tả trong **`trochoi.compiled.js`**).

---

### Bước 1: Cập nhật Tên & Mô tả trong `trochoi.compiled.js`
Tại khai báo `id: 'treasure'` trong danh mảng `GAME_LIST`:
```javascript
{
  id: 'treasure',
  name: 'Đua Vịt Ngẫu Nhiên',
  icon: 'fa-feather-pointed',
  color: 'from-cyan-400 to-blue-500',
  purpose: 'Gọi học sinh ngẫu nhiên',
  description: 'Mỗi học sinh một chú vịt bơi đua trên dòng sông — chú vịt về đích đầu tiên sẽ được gọi phát biểu hoặc nhận nhiệm vụ!',
  suitable: 'Khởi động, kiểm tra bài cũ, gọi học sinh ngẫu nhiên hào hứng'
}
```

---

### Bước 2: Tái cấu trúc toàn diện `game-treasure.html`

Tệp `game-treasure.html` được xây dựng lại thành một trò chơi đua vịt sông nước đồ họa Canvas/HTML5 sống động, 60 FPS, không phụ thuộc thư viện nặng ngoài CDN:

#### 1. Hệ thống Âm Thanh (Web Audio API - Chạy 100% Offline, Không cần file âm thanh ngoài):
Xây dựng module âm thanh thuần Web Audio:
- `playCountdownBeep(isGo)`: Tiếng tít tít 3-2-1 và tiếng còi bính boong khi xuất phát.
- `playQuack()`: Tiếng vịt quác quác vui nhộn `quack quack` khi bứt tốc ngẫu nhiên.
- `playSplash()`: Tiếng nước rẽ sóng bì bõm.
- `playVictoryFanfare()`: Giai điệu kèn chiến thắng rộn rã khi có vịt chạm vạch đích.
- Nút Bật/Tắt âm thanh tiện lợi ở góc màn hình.

#### 2. Đường Đua Sông Nước & Hoạt Họa Canvas (River Track Engine):
- **Bối cảnh dòng sông:**
  - Nước sông xanh mát với dải gradient và các gợn sóng nước trôi lững lờ.
  - Bờ sông 2 bên viền cỏ xanh và hoa súng, bèo tây nổi trên mặt nước.
  - Vạch xuất phát (Start Line) bằng cầu cảng gỗ và phao nước.
  - Vạch đích (Finish Line) cờ ca-rô trắng đen nổi bật vắt ngang sông cùng cờ chiến thắng.
- **Chú vịt hoạt hình & Bảng tên học sinh:**
  - Vẽ chú vịt vàng đáng yêu với mỏ cam, mắt to tròn, cánh chèo nước nhấp nhô nhịp nhàng (`quack wiggle`).
  - Mỗi chú vịt có màu nón hoặc vòng cổ khác nhau để phân biệt.
  - **Bảng tên học sinh:** Nổi bật ngay phía trên/trước đầu vịt, nền trắng viền bo tròn, chữ đậm rõ ràng, đảm bảo đọc rõ từ khoảng cách xa trên máy chiếu hoặc tivi lớp học.
- **Cơ chế đua kịch tính (Surge & Overtake Physics):**
  - Thời lượng cuộc đua: Có thể chọn 8s (Nhanh), 12s (Tiêu chuẩn), 16s (Kịch tính).
  - Vận tốc cơ sở được cộng hưởng bởi các xung tốc ngẫu nhiên (Random Speed Bursts) xuất hiện từng đợt.
  - Hiệu ứng tăng tốc: Biểu tượng bốc lửa 🚀 hoặc bọt nước tung tóe 💨 khi vịt bứt phá dẫn đầu.
  - Camera bám đuổi (Dynamic Camera) di chuyển mượt mà theo tốp vịt dẫn đầu về phía vạch đích.
  - Mini-leaderboard ở góc màn hình hiển thị Top 3 vịt đang dẫn đầu theo thời gian thực.

#### 3. Modal Vinh Danh Học Sinh Chiến Thắng (Victory Podium):
Khi chú vịt đầu tiên chạm vạch đích:
- Pháo giấy confetti nổ rực rỡ khắp màn hình (`canvas-confetti`).
- Kèn mừng chiến thắng vang lên.
- Hiện khung thông báo lớn trang trọng:
  ```
  🏆 CHÚC MỪNG: [TÊN HỌC SINH]! 🦆
  Học sinh may mắn được gọi trong lượt này!
  ```
- **Các tính năng sư phạm tích hợp:**
  - **Nút "Hiện câu hỏi kiểm tra"** (nếu có câu hỏi trong dữ liệu game): Mở modal câu hỏi trắc nghiệm/tự luận cho học sinh trả lời kèm đồng hồ đếm ngược 30 giây.
  - **Nút "Đua tiếp (Giữ nguyên danh sách)"**: Khởi động lượt đua mới với đầy đủ cả lớp.
  - **Nút "Đua tiếp (Loại bạn này khỏi lượt sau)"**: Tự động đánh dấu và loại em vừa thắng khỏi danh sách đua để tránh gọi trùng lặp, đảm bảo cơ hội cho các bạn khác.
  - **Nút "Lịch sử gọi tên"**: Xem danh sách các em đã được gọi trong tiết học.

#### 4. Quản lý danh sách học sinh (Roster Manager):
- Tự động nhận danh sách học sinh từ `trochoi.html` (đã có kết nối CSDL lớp học, Excel, hoặc nhập tay).
- Cho phép giáo viên chỉnh sửa danh sách trực tiếp trên màn hình:
  * Nút "Đổi lớp học (CSDL)"
  * Nút "Nhập danh sách mới / Import Excel"
  * Hiển thị tổng số học sinh đang tham gia cuộc đua (ví dụ: 38 học sinh).

---

## 3. Kế Hoạch Xác Minh (Verification Plan)

1. **Kiểm tra hiển thị và khởi tạo:**
   - Nạp danh sách từ CSDL lớp học (hoặc Excel/nhập tay 35-45 học sinh) $\rightarrow$ Toàn bộ học sinh xuất hiện trên đường đua với tên đầy đủ, vịt xếp gọn gàng tại vạch xuất phát.
2. **Kiểm tra cuộc đua thời gian thực:**
   - Bấm nút "BẮT ĐẦU ĐUA 🏁" $\rightarrow$ Đếm ngược 3-2-1 với âm thanh xuất phát.
   - Các chú vịt cùng bơi về đích với hiệu ứng sóng nước, bứt tốc ngẫu nhiên, đổi ngôi liên tục đầy hào hứng.
3. **Kiểm tra vạch đích và vinh danh:**
   - Vịt đầu tiên cán đích $\rightarrow$ Âm thanh chiến thắng, pháo hoa/confetti bung nở, popup hiện đúng tên học sinh về nhất.
4. **Kiểm tra tính năng sư phạm:**
   - Bấm "Đua tiếp & Loại em này" $\rightarrow$ Lượt sau em đó không còn trong đường đua, số lượng vịt giảm 1.
   - Bấm "Hiện câu hỏi" $\rightarrow$ Hiển thị câu hỏi kiểm tra trắc nghiệm cho học sinh trả lời.
