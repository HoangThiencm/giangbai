# PLAN: Nâng Cấp Ô Chữ Kỳ Diệu, Đua Xe Tùy Chỉnh Số Tổ, Thiết Kế Rung Chuông Vàng & Xóa "Quay lại SmartQuiz"

## 1. Tổng Quan Nhiệm Vụ

Bản kế hoạch giải quyết trọn vẹn 4 yêu cầu từ người dùng:
1. **Sửa triệt để Game Ô Chữ Kỳ Diệu (`game-crossword.html` & `trochoi.compiled.js`)**: Khắc phục lỗi nạp đề thi dài sinh ra 48 hàng với đáp án dài 45 chữ cái làm vỡ khung hình (như ảnh phản ánh). Giới hạn số hàng hợp lý (tối đa 8–10 hàng), làm sạch và chuẩn hóa đáp án ngắn gọn (3–14 ký tự), sửa thuật toán căn cột từ khóa dọc và bổ sung trợ giúp cho giáo viên.
2. **Game Đua Xe (`game-racing.html`)**: Cho phép người tổ chức tự chọn số tổ tham gia (từ 2 đến 6 tổ) và đặt tên tổ tùy ý thay vì cố định cứng 4 tổ. Tự động sinh làn đua, màu xe, cờ hiệu và bục trao giải Podium tương ứng.
3. **Thiết kế Game mới "Rung Chuông Vàng" (`game-bell.html`)**: Xây dựng đấu trường Rung Chuông Vàng kịch tính cho lớp học với sàn đấu thí sinh, đồng hồ đếm ngược, cơ chế loại trực tiếp, quyền Cứu trợ của thầy cô và hiệu ứng Rung chuông vàng đỉnh cao kèm pháo hoa confetti.
4. **Xóa "Quay lại SmartQuiz" trong `trochoi.compiled.js`**: Loại bỏ nút và dấu ngăn cách ở thanh điều hướng trên cùng của trang Game Giáo Dục, chỉ giữ lại nút "Về trang chủ".

---

## 2. Chi Tiết Thực Hiện Cho Coder

### PHẦN 1: Sửa Triệt Để Game Ô Chữ Kỳ Diệu (`game-crossword.html` & `trochoi.compiled.js`)

#### 1. Xử lý dữ liệu nạp ô chữ trong `trochoi.compiled.js`:
Tại hàm xử lý `crossword` (khoảng dòng 409-425) và phần nạp câu hỏi:
- Khi người dùng nạp từ bộ câu hỏi trắc nghiệm hoặc dán văn bản:
  - Giới hạn tối đa **8 - 10 cặp** (hàng ngang), không để vượt quá 10 hàng.
  - Lọc đáp án: Với mỗi câu hỏi, chỉ lấy đáp án ngắn gọn (từ khóa chính), loại bỏ các đáp án dài quá 14 ký tự hoặc cắt lấy cụm từ khóa đầu tiên:
  ```javascript
  const cleanAnswer = (ans) => {
      let s = String(ans || '').trim();
      // Bỏ tiền tố A., B., C., D. nếu có
      s = s.replace(/^[A-D]\s*[\.\):]\s*/i, '');
      // Chuẩn hóa bỏ dấu và ký tự đặc biệt
      let norm = s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^A-Za-z0-9]/g, '').toUpperCase();
      if (norm.length > 14) norm = norm.slice(0, 14); // Cắt tối đa 14 ký tự
      return norm;
  };
  ```
  - Từ khóa dọc (`keyword`): Giới hạn độ dài bằng số lượng hàng ngang hợp lệ.

#### 2. Nâng cấp toàn diện `game-crossword.html`:
Chỉnh sửa `game-crossword.html`:
- **Giới hạn & Chuẩn hóa hàng ngang:**
  ```javascript
  // Lấy tối đa 10 hàng có đáp án hợp lệ từ 2 đến 14 ký tự
  let entries = src.map((p, idx) => ({
      id: p.id ?? idx,
      clue: p.left || p.clue || p.prompt || `Câu ${idx + 1}`,
      answer: normalize(p.right || p.answer || '')
  })).filter(e => e.clue && e.answer && e.answer.length >= 2 && e.answer.length <= 15).slice(0, 10);
  ```
- **Thuật toán căn cột từ khóa dọc thông minh:**
  - Nếu có từ khóa dọc `keyword`, mỗi hàng tìm vị trí chữ cái tương ứng `kw[i]`.
  - Nếu trong đáp án có chữ cái đó, căn vị trí để cột vàng thẳng hàng.
  - Nếu đáp án không chứa chữ cái đó, lấy ký tự đầu tiên và cập nhật lại chữ cái cột vàng để không bị sai lệch chữ hiển thị.
- **Giao diện Modal trả lời & Trợ giúp:**
  - Render gợi ý bằng `<MathText text={row.clue} />` để hiển thị công thức toán sắc nét.
  - Hiển thị rõ số lượng chữ cái (ví dụ: `(7 chữ cái)`).
  - Tự động chuẩn hóa input khi gõ (bỏ dấu tiếng Việt, viết hoa, loại bỏ khoảng trắng).
  - Bổ sung nút **"Gợi ý 1 chữ cái"** (mở ngẫu nhiên 1 ký tự chưa mở trong hàng) và nút **"Hiện từ khóa"** khi lớp học gặp khó khăn.
  - Thiết kế bảng ô chữ responsive, tự động co giãn kích thước ô (cell) từ `w-7 h-7` đến `w-9 h-9` để vừa vặn trên mọi màn hình máy chiếu phòng học.

---

### PHẦN 2: Game Đua Xe Tùy Chỉnh Số Tổ (`game-racing.html`)

Chỉnh sửa `game-racing.html`:

#### 1. Định nghĩa bảng màu và tên mặc định cho 6 tổ:
```javascript
const DEFAULT_TEAMS = [
    { id: 't1', name: 'Tổ 1 - Scuderia Red', short: 'Tổ 1', color: '#ef4444', glow: 'shadow-red-500/50' },
    { id: 't2', name: 'Tổ 2 - Cyan Lightning', short: 'Tổ 2', color: '#06b6d4', glow: 'shadow-cyan-500/50' },
    { id: 't3', name: 'Tổ 3 - Golden Thunder', short: 'Tổ 3', color: '#eab308', glow: 'shadow-yellow-500/50' },
    { id: 't4', name: 'Tổ 4 - Neon Phantom', short: 'Tổ 4', color: '#a855f7', glow: 'shadow-purple-500/50' },
    { id: 't5', name: 'Tổ 5 - Emerald Rush', short: 'Tổ 5', color: '#10b981', glow: 'shadow-emerald-500/50' },
    { id: 't6', name: 'Tổ 6 - Orange Flame', short: 'Tổ 6', color: '#f97316', glow: 'shadow-orange-500/50' },
];
```

#### 2. Thêm Modal Cấu Hình Số Tổ Trước Khi Bắt Đầu:
- Trong trạng thái ban đầu (`showInstructions` hoặc màn hình Setup):
  - Cho phép người tổ chức chọn số lượng tổ: **2 tổ, 3 tổ, 4 tổ, 5 tổ hoặc 6 tổ** (các nút bấm chọn nhanh).
  - Các ô input cho phép giáo viên chỉnh sửa tên tổ trực tiếp (ví dụ: "Tổ 1", "Tổ 2", hoặc "Nhóm Sư Tử", "Nhóm Đại Bàng"...).
  - State `teams`: Lưu danh sách các tổ đã được chọn (`DEFAULT_TEAMS.slice(0, numTeams)` kèm tên do người dùng sửa).

#### 3. Đường đua và động học thích ứng động:
- Các làn đua (`lanes`), vị trí xe (`f1-car`), hộp quà bí ẩn (`mystery-box`) và bảng chọn đội trả lời (`team-pick`) được `map` động hoàn toàn từ mảng `teams`.
- Bảng xếp hạng trực tiếp và Bục vinh danh (Podium) tự động điều chỉnh hiển thị Top 1, Top 2, Top 3 theo đúng số tổ tham gia.

---

### PHẦN 3: Thiết Kế Game Mới "Rung Chuông Vàng" (`game-bell.html`)

Tạo mới file `game-bell.html`:

#### 1. Cấu trúc trang HTML & Thư viện:
- Chuẩn giao diện Tailwind CSS, KaTeX (toán học), FontAwesome 6, Canvas Confetti (`canvas-confetti.browser.min.js`), Web Audio API.
- Guard scripts: `js/security-guard.js`, `access-control.js`.

#### 2. Đấu trường Rung Chuông Vàng:
- **Thí sinh tham gia:**
  - Đọc từ `localStorage.getItem('gameData').participants` nếu có (học sinh CSDL/Excel), hoặc tự sinh danh sách 30 - 40 thí sinh theo lớp (SBD 01 đến SBD 40).
  - Sàn đấu hiển thị danh sách thí sinh:
    - Thí sinh đang thi đấu: Thẻ bo tròn màu xanh ngọc / vàng nổi bật, có tên/SBD.
    - Thí sinh bị loại: Màu xám mờ, gạch ngang, nằm ở khu vực "Chờ cứu trợ".
- **Tiến trình câu hỏi:**
  - Hiển thị Câu hỏi số hiện tại (ví dụ: Câu 5 / 15).
  - Nội dung câu hỏi và 4 lựa chọn A, B, C, D render chuẩn KaTeX với component `<MathText>`.
  - Đồng hồ đếm ngược 15 giây (hoặc tùy chỉnh 20s/30s) có thanh thời gian chạy mượt mà và âm thanh tích tắc hồi hộp.
  - Khi hết giờ: Phát tiếng chuông vang "Boong!", khóa nhận đáp án, hiển thị đáp án đúng màu xanh kèm lời giải thích.
- **Cơ chế Loại & Cứu trợ:**
  - Sau khi hiện đáp án đúng, Giáo viên bấm chọn thí sinh trả lời sai trên màn hình để loại (hoặc bấm nút "Loại nhanh theo tỉ lệ").
  - **Quyền Cứu Trợ của Thầy Cô:**
    - Nút bấm "Thầy cô cứu trợ": Cho phép "Cứu 50% thí sinh" hoặc "Cứu tất cả thí sinh" quay lại sàn đấu một cách hào hứng!
- **Màn Vinh Danh Rung Chuông Vàng:**
  - Thí sinh cuối cùng vượt qua câu hỏi xuất sắc rung chiếc chuông vàng lớn ở giữa màn hình.
  - Hiệu ứng chuông lắc lư ngân vang, pháo hoa nổ ngập tràn màn hình (`confetti`), vinh danh Quán Quân Rung Chuông Vàng của lớp học!

#### 3. Tích hợp vào hệ thống:
- Trong `trochoi.compiled.js`:
  Thêm game `bell` vào mảng `games` (khoảng dòng 1134):
  ```javascript
  {
    id: 'bell',
    name: 'Rung Chuông Vàng',
    icon: 'fa-bell',
    color: 'from-amber-400 to-yellow-600',
    purpose: 'Đấu trường kiến thức',
    description: 'Đấu trường sinh tử cả lớp — trả lời đúng để trụ lại, cứu trợ thầy cô và rung chuông vàng đỉnh cao!',
    suitable: 'Hoạt động ngoại khóa, ôn tập tổng kết, rung chuông vàng lớp học'
  }
  ```
- Trong `access-control.js`:
  Thêm vào bảng `pageKeys`:
  ```javascript
  'game-bell.html': 'smartquiz',
  ```

---

### PHẦN 4: Xóa "Quay lại SmartQuiz" trong `trochoi.compiled.js`

Tại file `trochoi.compiled.js` (khoảng dòng 1442-1449):
Xóa hoàn toàn khối `span` ngăn cách và `button` "Quay lại SmartQuiz":
```javascript
// XÓA ĐOẠN NÀY:
/*#__PURE__*/React.createElement("span", {
  className: "text-gray-300"
}, "|"), /*#__PURE__*/React.createElement("button", {
  onClick: () => window.location.href = 'smartquiz.html',
  className: "text-gray-500 hover:text-purple-600 font-bold transition"
}, /*#__PURE__*/React.createElement("i", {
  className: "fas fa-arrow-left mr-2"
}), "Quay lại SmartQuiz")
```
Thanh điều hướng trên cùng chỉ còn lại duy nhất nút:
```javascript
/*#__PURE__*/React.createElement("button", {
  onClick: () => window.location.href = 'index.html',
  className: "text-gray-500 hover:text-purple-600 font-bold transition"
}, /*#__PURE__*/React.createElement("i", {
  className: "fas fa-home mr-2"
}), "Về trang chủ")
```

---

### PHẦN 5: Bài Test Tự Động (`tests/game-suite-smoke.js`)

Tạo mới file `tests/game-suite-smoke.js`:
```javascript
const assert = require("assert");
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const crosswordHtml = fs.readFileSync(path.join(root, "game-crossword.html"), "utf8");
const racingHtml = fs.readFileSync(path.join(root, "game-racing.html"), "utf8");
const bellHtml = fs.readFileSync(path.join(root, "game-bell.html"), "utf8");
const trochoiJs = fs.readFileSync(path.join(root, "trochoi.compiled.js"), "utf8");
const accessJs = fs.readFileSync(path.join(root, "access-control.js"), "utf8");

// 1. Kiểm tra Ô chữ kỳ diệu
assert.match(crosswordHtml, /MathText/, "game-crossword.html phải có component MathText để render công thức");
assert.match(crosswordHtml, /entries\.slice\(0,\s*10\)|slice\(0,\s*Math\.min\(10/, "game-crossword.html phải giới hạn số hàng ngang tối đa 10");
assert.match(crosswordHtml, /kw-col/, "game-crossword.html có highlight cột từ khóa");

// 2. Kiểm tra Game Đua xe tùy chỉnh số tổ
assert.match(racingHtml, /numTeams|setNumTeams|teams/, "game-racing.html có cấu hình số tổ đua");
assert.match(racingHtml, /Tổ 5|t5|DEFAULT_TEAMS/, "game-racing.html hỗ trợ linh hoạt các tổ (ít nhất đến tổ 5/6)");

// 3. Kiểm tra Game Rung chuông vàng
assert.match(bellHtml, /Rung Chuông Vàng/i, "game-bell.html có tiêu đề Rung Chuông Vàng");
assert.match(bellHtml, /MathText/, "game-bell.html hỗ trợ MathText KaTeX");
assert.match(bellHtml, /cứu trợ|cuuTro|revive/i, "game-bell.html có cơ chế cứu trợ thí sinh");
assert.match(bellHtml, /confetti|canvas-confetti/i, "game-bell.html có pháo hoa chúc mừng rung chuông");

// 4. Kiểm tra trochoi.compiled.js
assert.match(trochoiJs, /id:\s*'bell'/, "trochoi.compiled.js đã đăng ký game bell");
assert.ok(!trochoiJs.includes("Quay lại SmartQuiz"), "trochoi.compiled.js đã xóa hoàn toàn 'Quay lại SmartQuiz'");

// 5. Kiểm tra access-control.js
assert.match(accessJs, /'game-bell\.html':\s*'smartquiz'/, "access-control.js bảo vệ route game-bell.html");

console.log("game-suite smoke: PASS");
```

---

## 3. Kế Hoạch Kiểm Thử & Nghiệm Thu (Verification Plan)

1. **Chạy test tự động:**
   ```powershell
   node tests/game-suite-smoke.js
   node tests/change-password-smoke.js
   node tests/canvas-tabs-permissions-smoke.js
   ```
2. **Kiểm tra giao diện & tính năng thủ công:**
   - Mở `trochoi.html`: Thanh header không còn chữ "Quay lại SmartQuiz", danh sách xuất hiện game **Rung Chuông Vàng**.
   - Thử mở `game-crossword.html` với bộ câu hỏi: Ô chữ hiển thị gọn gàng (tối đa 8-10 hàng), không bị vỡ hàng 45 chữ cái, modal trả lời render toán KaTeX chuẩn đẹp.
   - Thử mở `game-racing.html`: Có màn hình chọn 2, 3, 4, 5, 6 tổ đua, cho phép đặt tên tổ và đua xe mượt mà.
   - Thử mở `game-bell.html`: Sàn đấu hiển thị danh sách thí sinh, đồng hồ đếm ngược, bấm loại thí sinh sai, thử chức năng cứu trợ và vinh danh rung chuông vàng.
