# PLAN: Tích Hợp 5 Game Giáo Dục Mới Vào Hệ Thống trochoi.html

## 1. Phân Tích Kiến Trúc & Tính Khả Thi

### Kiến trúc hiện tại của `trochoi.html`:
- `trochoi.html` đóng vai trò là **Game Hub / Launcher**:
  1. Giáo viên chọn trò chơi trong danh mục `GAME_LIST`.
  2. Nạp nội dung bằng AI (`generateWithAI`) hoặc nạp từ file Word/LaTeX (`GameQuizImporter`).
  3. Xem trước và chỉnh sửa câu hỏi (`step === 'EDIT'`).
  4. Bấm "Chơi ngay" $\rightarrow$ Hệ thống lưu dữ liệu câu hỏi vào `localStorage.setItem('gameData', ...)` và điều hướng sang trang trò chơi độc lập:
     ```javascript
     window.location.href = `game-${selectedGame.id}.html`;
     ```
  5. Các game con hiện tại (`game-elimination.html`, `game-speedscore.html`, `game-unlock.html`, `game-teambattle.html`, `game-tower.html`, `game-matching.html`, `game-treasure.html`, `game-escape.html`) tự đọc `gameData` từ `localStorage` để khởi chạy.

### Kết luận khả thi:
**Hoàn toàn tích hợp được cả 5 game mới 100%** vào hệ thống mà không làm xáo trộn hay ảnh hưởng đến bất kỳ game nào đang chạy!

---

## 2. Danh Mục 5 Game Mới Cần Tích Hợp

| STT | Mã Game (`id`) | Tên Trò Chơi | Mục Tiêu Sư Phạm | Tệp Triển Khai | Dữ Liệu Đầu Vào |
|:---:|:---:|:---|:---|:---:|:---|
| **1** | `picture` | **Bức Tranh Bí Ẩn** | Khởi động, dẫn dắt vào bài mới | `game-picture.html` | 4–9 câu trắc nghiệm + 1 ảnh chủ đề bài học |
| **2** | `wheel` | **Vòng Quay May Mắn** | Kiểm tra bài cũ, gọi học sinh ngẫu nhiên | `game-wheel.html` | Danh sách học sinh CSDL + Câu hỏi trắc nghiệm |
| **3** | `millionaire` | **Ai Là Triệu Phú** | Ôn tập chuyên sâu, đại diện cá nhân/tổ | `game-millionaire.html` | 10–15 câu trắc nghiệm độ khó tăng dần + 3 quyền trợ giúp |
| **4** | `crossword` | **Ô Chữ Kỳ Diệu** | Củng cố, tổng kết chương/thuật ngữ | `game-crossword.html` | Các câu gợi ý hàng ngang + 1 từ khóa hàng dọc |
| **5** | `racing` | **Đua Xe 4 Tổ (F1)** | Thi đua đội nhóm 4 tổ trong lớp học | `game-racing.html` | Câu hỏi trắc nghiệm + Phân chia 4 tổ thi đấu |

---

## 3. Lộ Trình Kỹ Thuật Chi Tiết Cho Coder

### Bước 1: Khai báo 5 Game mới trong `trochoi.compiled.js`
Mở rộng danh mảng `GAME_LIST`:
```javascript
{
  id: 'picture',
  name: 'Bức Tranh Bí Ẩn',
  icon: 'fa-image',
  color: 'from-pink-500 to-rose-500',
  purpose: 'Khởi động / Vào bài',
  description: 'Mỗi câu đúng mở 1 mảnh ghép hé lộ bức tranh bí ẩn của bài học!',
  suitable: 'Dẫn dắt bài mới, kích thích tò mò'
},
{
  id: 'wheel',
  name: 'Vòng Quay May Mắn',
  icon: 'fa-dharmachakra',
  color: 'from-teal-400 to-emerald-600',
  purpose: 'Kiểm tra ngẫu nhiên',
  description: 'Quay chọn học sinh từ CSDL và quay điểm thưởng may mắn!',
  suitable: 'Kiểm tra bài cũ, gọi phát biểu'
},
{
  id: 'millionaire',
  name: 'Ai Là Triệu Phú',
  icon: 'fa-lightbulb',
  color: 'from-blue-600 to-indigo-900',
  purpose: 'Thang điểm tri thức',
  description: '15 câu hỏi kịch tính với 3 quyền trợ giúp (50:50, Hỏi cả lớp, Đổi câu)',
  suitable: 'Ôn tập cá nhân hoặc đại diện tổ'
},
{
  id: 'crossword',
  name: 'Ô Chữ Kỳ Diệu',
  icon: 'fa-border-all',
  color: 'from-violet-500 to-purple-600',
  purpose: 'Giải mã từ khóa',
  description: 'Giải các hàng ngang để tìm ra từ khóa chủ đề bài học!',
  suitable: 'Củng cố thuật ngữ, tổng kết chương'
},
{
  id: 'racing',
  name: 'Đua Xe 4 Tổ',
  icon: 'fa-car-side',
  color: 'from-orange-500 to-red-600',
  purpose: 'Thi đua 4 tổ',
  description: '4 xe đại diện 4 tổ trong lớp đua về đích theo kết quả trả lời!',
  suitable: 'Thi đua sôi nổi giữa các tổ'
}
```

### Bước 2: Tùy biến nạp dữ liệu đặc thù cho từng game trong `trochoi.compiled.js`
- **Game `picture` (Bức tranh bí ẩn):** Thêm ô chọn ảnh bài học tải lên (hoặc chọn sẵn từ kho ảnh mẫu AI).
- **Game `wheel` (Vòng quay may mắn):** Tái sử dụng khối chọn lớp học CSDL (`renderDuckSection` / `participantMode === 'database'`).
- **Game `millionaire` (Ai là triệu phú):** Tự động nhận diện độ khó tăng dần từ câu 1 đến câu 15.
- **Game `crossword` (Ô chữ kỳ diệu):** Bóc tách các cặp `[Gợi ý] - [Từ khóa]` tương tự bộ `parseMatchingPairs` của game Ghép đôi.
- **Game `racing` (Đua xe 4 tổ):** Tự động gán 4 tổ: Tổ 1 (Đỏ), Tổ 2 (Xanh), Tổ 3 (Vàng), Tổ 4 (Tím).

### Bước 3: Xây dựng 5 trang Game độc lập
1. **`game-picture.html`**:
   - Canvas/SVG chia lưới 2x2, 2x3, hoặc 3x3 phủ lên ảnh nền.
   - Khi chọn mảnh ghép $\rightarrow$ Modal hiện câu hỏi. Trả lời đúng $\rightarrow$ Hiệu ứng vỡ mảnh ghép hé lộ bức tranh kèm âm thanh chúc mừng.
2. **`game-wheel.html`**:
   - Vòng quay may mắn bằng HTML5 Canvas:
     * Vòng tròn học sinh: Quay chọn học sinh từ CSDL lớp.
     * Vòng tròn điểm số / quà tặng: 10đ, 20đ, 50đ, Hộp quà bí mật, Mất lượt, Nhân đôi.
3. **`game-millionaire.html`**:
   - Giao diện phỏng theo gameshow Ai Là Triệu Phú (khung câu hỏi xanh đậm viền vàng, cây thang tiền thưởng 15 mốc).
   - 3 nút quyền trợ giúp tương tác:
     * `50:50`: Ẩn ngay 2 phương án sai.
     * `Hỏi ý kiến cả lớp`: Hiển thị biểu đồ cột biểu quyết.
     * `Đổi câu hỏi`: Lấy câu hỏi dự phòng từ ngân hàng câu hỏi.
4. **`game-crossword.html`**:
   - Ma trận ô chữ ngang, căn chỉnh các chữ cái chứa Từ Khóa Hàng Dọc (cột highlight màu vàng).
   - Click vào từng hàng ngang $\rightarrow$ Hiện gợi ý câu hỏi. Gõ đúng $\rightarrow$ Lật từng ô chữ cái.
5. **`game-racing.html`**:
   - Đường đua 4 làn (Lane 1..4). Mỗi lần tổ trả lời đúng, xe tương ứng phóng nhanh về trước với khói nitro và âm thanh động cơ.

---

## 4. Kế Hoạch Kiểm Thử (Verification Plan)
1. Kiểm tra hiển thị đủ 13 trò chơi trên màn hình chính `trochoi.html` (8 game cũ + 5 game mới).
2. Kiểm tra nạp câu hỏi trắc nghiệm từ `taobaitap.html` và Word/LaTeX vào cả 5 game mới không bị lỗi.
3. Khởi chạy từng game con và xác nhận logic chơi game, âm thanh, hiệu ứng mượt mà trên máy chiếu / màn hình TV lớp học.
