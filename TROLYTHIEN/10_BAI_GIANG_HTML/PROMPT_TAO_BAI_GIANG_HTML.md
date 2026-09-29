# MASTER PROMPT — TẠO BÀI GIẢNG HTML (TỪ PDF)

Dùng khi người dùng chọn **10/ Tạo bài giảng HTML (từ PDF)** trong trợ lý `/thien`.

## 1. Thông tin quy trình

Trước khi đọc PDF và trước khi viết file HTML, bắt buộc hỏi đúng 3 thông tin. Thiếu thông tin nào thì dừng và hỏi tiếp. Không suy diễn.

1. **Môn gì?** (Toán, Khoa học tự nhiên, Ngữ văn, Lịch sử - Địa lý, Tin học,...)
2. **Lớp mấy?** (Lớp 6, 7, 8, 9,...)
3. **Mấy tiết (thời lượng)?** (1 tiết = 45 phút, 2 tiết = 90 phút,...)

Chỉ sau khi có đủ Môn, Lớp và Số tiết mới được thực hiện các bước sau.

## 2. Quy tắc trích xuất đầu vào

- Đọc file PDF SGK, bài học, tài liệu giảng dạy trong `TROLYTHIEN/10_BAI_GIANG_HTML/Dau_vao/`.
- Nếu thư mục trống hoặc không có PDF đúng bài, yêu cầu người dùng đặt file vào đó rồi dừng.
- Trích nguyên văn các mục sách: khám phá, định nghĩa, ví dụ, luyện tập, số liệu, hình và câu hỏi.
- Giữ ký hiệu, đơn vị, dữ liệu bảng đúng như PDF.

## 3. Quy tắc xuất file đầu ra

- Xuất đúng một file: `TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/[Tên_Bài].html`.
- `[Tên_Bài]` lấy từ tên bài trong PDF, viết không dấu cách thừa, không ghi đè file khác nếu chưa được yêu cầu.
- Không lưu HTML ở thư mục khác.

## 4. Bảy điểm vá thực chiến

### Vá 1 — Single-file Standalone HTML

- Một file `.html` standalone, độc lập 100%. CSS, script điều khiển và icon SVG nằm trong file.
- Công thức Toán được phép gọi CDN ổn định MathJax 3 (`tex-svg.js`). Phần còn lại không phụ thuộc server.
- Mở trực tiếp bằng `file:///` trên trình duyệt. Không cần web server, localhost hay Node.js.

### Vá 2 — Bố cục Dual-Mode (Thiết kế / Trình chiếu 16:9)

- Nút chuyển **Chế độ Thiết kế**: cuộn dọc toàn bộ giáo án để giáo viên tra cứu.
- Nút chuyển **Chế độ Trình chiếu**: mỗi slide là khung 16:9, một slide một màn.
- Điều hướng: phím `←` `→`, phím Space, nút Trước/Sau, vuốt chạm trái/phải.
- Toàn màn hình bằng F5 hoặc nút toàn màn hình của trình duyệt.

### Vá 3 — Bảng 2 cột sư phạm chuẩn CV 5512 và GDPT 2018

Mỗi hoạt động chính có bảng 2 cột:

| Hoạt động của Giáo viên | Hoạt động của Học sinh |
| --- | --- |
| Việc GV giao, câu hỏi, cách tổ chức | Việc HS làm, sản phẩm, cách báo cáo |

Đủ 4 bước, không bỏ bước, không để trống cột:

1. Chuyển giao nhiệm vụ
2. Thực hiện nhiệm vụ
3. Báo cáo, thảo luận
4. Kết luận, nhận định

Cột GV mô tả việc giao và chốt. Cột HS mô tả việc làm cụ thể. Không viết một cột rồi để cột kia trắng.

### Vá 4 — MathJax 3

Cấu hình trước khi tải script:

```javascript
MathJax = { tex: { inlineMath: [['$', '$'], ['\\(', '\\)']], displayMath: [['$$', '$$'], ['\\[', '\\]']] } }
```

- Dùng script `tex-svg.js` của MathJax 3.
- Công thức trong dòng viết `$..$`. Công thức riêng khối viết `$$..$$`.
- Vá CSS để SVG không bị vỡ xuống dòng:

```css
mjx-container svg { display: inline !important; }
```

- Sau khi cập nhật DOM hoặc chuyển slide, gọi `MathJax.typesetPromise()`.

### Vá 5 — Tương tác sư phạm 2 chiều

- Nút ẩn/hiện đáp án và gợi ý: `<button onclick="toggleAnswer(...)">`.
- Câu hỏi trắc nghiệm: chọn phương án thì đúng đổi màu xanh, sai đổi màu đỏ ngay, kèm lời giải chi tiết lấy từ PDF.
- Đồng hồ đếm ngược cho hoạt động nhóm.
- Hộp ghi nhớ (callout) để chốt kiến thức.

### Vá 6 — Bảo toàn dữ liệu gốc từ PDF

- Bám sát 100% ngữ cảnh PDF: khám phá, định nghĩa, ví dụ, luyện tập, số liệu thực tế.
- Không bịa số liệu, định nghĩa, công thức, ví dụ hay câu hỏi ngoài sách.
- Nếu PDF không có một mục, ghi rõ “PDF không nêu” thay vì tự tạo nội dung.

### Vá 7 — Phân bổ thời lượng theo số tiết

- 1 tiết = 45 phút: 8–12 slides.
- 2 tiết = 90 phút: 16–22 slides, chia rõ Tiết 1 và Tiết 2.
- Phông sans-serif, cỡ chữ lớn, tương phản cao, đọc được từ cuối phòng học.
- Mỗi slide một ý chính. Không nhồi nhiều hoạt động vào một slide.

## 5. Bộ khung mã HTML mẫu

Skeleton dưới đây chạy được ngay khi lưu thành file `.html`. Khi soạn bài thật, thay mọi chỗ `[TRÍCH TỪ PDF]` bằng nội dung đã trích, rồi nhân slide cho đủ 8–12 hoặc 16–22 slides theo số tiết. Không giữ nguyên câu placeholder trong bài thành phẩm.

```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>[Tên bài] — [Môn] lớp [Lớp]</title>
  <script>
    MathJax = { tex: { inlineMath: [['$', '$'], ['\\(', '\\)']], displayMath: [['$$', '$$'], ['\\[', '\\]']] } };
  </script>
  <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" async></script>
  <style>
    :root { color-scheme: light; }
    * { box-sizing: border-box; }
    body { margin: 0; font-family: "Segoe UI", Arial, sans-serif; background: #e8eef6; color: #102033; font-size: 22px; line-height: 1.45; }
    header.bar { display: flex; gap: 12px; align-items: center; padding: 12px 16px; background: #0b3a82; color: #fff; position: sticky; top: 0; z-index: 5; }
    header.bar button, .nav button, .quiz button, .timer button, .answer-toggle { font: inherit; font-size: 18px; border: 0; border-radius: 8px; padding: 8px 14px; cursor: pointer; }
    header.bar button { background: #fff; color: #0b3a82; font-weight: 700; }
    .deck { padding: 16px; }
    .slide { background: #fff; border: 3px solid #0b3a82; border-radius: 12px; padding: 28px; margin: 0 auto 20px; max-width: 1100px; }
    .deck.present .slide { display: none; width: min(100vw - 24px, calc((100vh - 92px) * 16 / 9)); aspect-ratio: 16 / 9; overflow: auto; }
    .deck.present .slide.active { display: block; }
    h1, h2 { margin: 0 0 12px; line-height: 1.25; }
    h1 { font-size: 40px; }
    h2 { font-size: 32px; color: #0b3a82; }
    table.script { width: 100%; border-collapse: collapse; font-size: 18px; }
    table.script th, table.script td { border: 2px solid #102033; padding: 10px; vertical-align: top; }
    table.script th { background: #0b3a82; color: #fff; }
    .callout { background: #fff6d8; border-left: 8px solid #b45309; padding: 12px 16px; font-weight: 700; }
    .hidden { display: none; }
    .quiz button { display: block; width: 100%; text-align: left; margin: 8px 0; background: #f4f7fb; border: 2px solid #0b3a82; }
    .quiz button.correct { background: #166534; color: #fff; }
    .quiz button.wrong { background: #b91c1c; color: #fff; }
    .timer { font-size: 48px; font-weight: 800; letter-spacing: 2px; }
    mjx-container svg { display: inline !important; }
    .icon { width: 28px; height: 28px; vertical-align: middle; }
  </style>
</head>
<body>
  <header class="bar">
    <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="4" width="18" height="14" fill="none" stroke="#fff" stroke-width="2"/><path d="M8 20h8" stroke="#fff" stroke-width="2"/></svg>
    <strong>[Môn] · Lớp [Lớp] · [Số tiết]</strong>
    <button type="button" id="modeBtn" onclick="toggleMode()">Chế độ Trình chiếu 16:9</button>
    <span id="counter">Thiết kế</span>
  </header>
  <main class="deck design" id="deck">
    <section class="slide active">
      <h1>[Tên bài trích từ PDF]</h1>
      <p>Môn: [Môn]. Lớp: [Lớp]. Thời lượng: [Số tiết] ([phút] phút).</p>
      <p class="callout">Ghi nhớ: [Khái niệm chốt trích từ PDF]</p>
    </section>
    <section class="slide">
      <h2>Hoạt động theo CV 5512 và GDPT 2018</h2>
      <table class="script">
        <thead>
          <tr><th>Hoạt động của Giáo viên</th><th>Hoạt động của Học sinh</th></tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Bước 1: Chuyển giao nhiệm vụ.</strong> [Lệnh giao việc trích từ PDF]</td>
            <td>Nhận nhiệm vụ, nhắc lại yêu cầu bằng lời của mình.</td>
          </tr>
          <tr>
            <td><strong>Bước 2: Thực hiện nhiệm vụ.</strong> Quan sát, gợi ý đúng chỗ vướng trong PDF.</td>
            <td>Làm [khám phá / ví dụ / luyện tập] đúng số liệu PDF.</td>
          </tr>
          <tr>
            <td><strong>Bước 3: Báo cáo, thảo luận.</strong> Mời nhóm trình bày, chất vấn lệch so với sách.</td>
            <td>Báo cáo sản phẩm, đối chiếu với bạn.</td>
          </tr>
          <tr>
            <td><strong>Bước 4: Kết luận, nhận định.</strong> Chốt đúng định nghĩa / quy tắc trong PDF.</td>
            <td>Ghi kiến thức chốt vào vở, nêu một ví dụ vừa làm.</td>
          </tr>
        </tbody>
      </table>
    </section>
    <section class="slide">
      <h2>Ví dụ trong sách</h2>
      <p>Công thức trong dòng: $[công thức PDF]$.</p>
      <p>$$[công thức khối trích từ PDF]$$</p>
      <button type="button" class="answer-toggle" onclick="toggleAnswer('ans1')">Ẩn/hiện đáp án</button>
      <div id="ans1" class="hidden callout">[Lời giải trích từ PDF, không bịa]</div>
    </section>
    <section class="slide">
      <h2>Trắc nghiệm</h2>
      <div class="quiz" id="quiz1">
        <p>[Câu hỏi trích từ PDF]</p>
        <button type="button" onclick="chooseQuiz(this, false)">A. [Phương án PDF]</button>
        <button type="button" onclick="chooseQuiz(this, true)">B. [Phương án đúng trong PDF]</button>
        <button type="button" onclick="chooseQuiz(this, false)">C. [Phương án PDF]</button>
        <button type="button" onclick="chooseQuiz(this, false)">D. [Phương án PDF]</button>
        <p id="quizExplain" class="hidden">[Lời giải chi tiết trích từ PDF]</p>
      </div>
    </section>
    <section class="slide">
      <h2>Thảo luận nhóm</h2>
      <p class="timer" id="clock">05:00</p>
      <button type="button" onclick="startTimer(5)">Bắt đầu đếm ngược</button>
      <p>Nhiệm vụ: [Câu hỏi thảo luận có trong PDF].</p>
    </section>
  </main>
  <footer class="nav" style="display:flex;gap:12px;justify-content:center;padding:12px;">
    <button type="button" onclick="moveSlide(-1)">← Trước</button>
    <button type="button" onclick="moveSlide(1)">Sau →</button>
  </footer>
  <script>
    var deck = document.getElementById("deck");
    var slides = Array.prototype.slice.call(document.querySelectorAll(".slide"));
    var index = 0;
    var present = false;
    var timerId = null;

    function typeset() {
      if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise();
    }

    function showSlide(next) {
      index = (next + slides.length) % slides.length;
      slides.forEach(function (slide, i) { slide.classList.toggle("active", i === index); });
      var counter = document.getElementById("counter");
      counter.textContent = present ? ("Slide " + (index + 1) + "/" + slides.length) : "Thiết kế";
      typeset();
    }

    function moveSlide(step) {
      if (!present) { present = true; deck.className = "deck present"; }
      showSlide(index + step);
    }

    function toggleMode() {
      present = !present;
      deck.className = present ? "deck present" : "deck design";
      document.getElementById("modeBtn").textContent = present ? "Chế độ Thiết kế" : "Chế độ Trình chiếu 16:9";
      showSlide(present ? index : 0);
    }

    function toggleAnswer(id) {
      var node = document.getElementById(id);
      node.classList.toggle("hidden");
      typeset();
    }

    function chooseQuiz(button, correct) {
      var siblings = button.parentNode.querySelectorAll("button");
      Array.prototype.forEach.call(siblings, function (item) {
        item.classList.remove("correct", "wrong");
        item.disabled = true;
      });
      button.classList.add(correct ? "correct" : "wrong");
      document.getElementById("quizExplain").classList.remove("hidden");
    }

    function startTimer(minutes) {
      var left = minutes * 60;
      var clock = document.getElementById("clock");
      if (timerId) clearInterval(timerId);
      timerId = setInterval(function () {
        left -= 1;
        if (left < 0) { clearInterval(timerId); clock.textContent = "00:00"; return; }
        var m = String(Math.floor(left / 60)).padStart(2, "0");
        var s = String(left % 60).padStart(2, "0");
        clock.textContent = m + ":" + s;
      }, 1000);
    }

    document.addEventListener("keydown", function (event) {
      if (event.key === "ArrowRight" || event.key === " ") { event.preventDefault(); moveSlide(1); }
      if (event.key === "ArrowLeft") { event.preventDefault(); moveSlide(-1); }
    });

    var touchX = null;
    document.addEventListener("touchstart", function (event) { touchX = event.changedTouches[0].clientX; });
    document.addEventListener("touchend", function (event) {
      if (touchX == null) return;
      var dx = event.changedTouches[0].clientX - touchX;
      if (dx < -40) moveSlide(1);
      if (dx > 40) moveSlide(-1);
      touchX = null;
    });

    typeset();
  </script>
</body>
</html>
```
