# QUY CHUẨN SOẠN BÀI GIẢNG HTML TRÌNH CHIẾU TƯƠNG TÁC (NHÁNH 10)

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

### Vá 8 — Vẽ hình học SVG tuyệt đối chính xác (Mathematical Exactness in SVG)

- **Tôn chỉ sư phạm cốt tử:** Trong môn Toán và các môn KHTN, hình vẽ sai lệch tính chất hình học là sai lầm sư phạm nghiêm trọng (hình vuông vẽ thành hình chữ nhật, hình thang cân vẽ thành hình thoi, tam giác đều vẽ lệch, góc vuông không đúng 90°). Tuyệt đối không vẽ ước chừng bằng mắt thường.
- **Quy tắc toán học & tọa độ bắt buộc khi sinh SVG:**
  1. **Tỷ lệ 1:1 và viewBox:** Luôn thiết lập `viewBox="0 0 W H"` với tỷ lệ tọa độ thực và đặt `preserveAspectRatio="xMidYMid meet"`, không kéo dãn `width`/`height` CSS làm méo tỷ lệ hình học.
  2. **Hình vuông:** $width = height$ tuyệt đối. Góc 4 đỉnh phải đúng 90°. Nếu có dải viền/lối đi $x$ đều xung quanh thì khoảng cách 4 phía phải bằng nhau tuyệt đối.
  3. **Hình chữ nhật:** Chiều dài $a$ và chiều rộng $b$ phải khác nhau rõ rệt theo đúng tỷ lệ số liệu bài toán ($a \neq b$).
  4. **Hình thoi:** 4 cạnh bằng nhau ($AB=BC=CD=DA$), hai đường chéo cắt nhau tại trung điểm và vuông góc tại gốc tọa độ đối xứng.
  5. **Hình thang cân:** Hai đáy nằm trên hai đường thẳng song song ($y_1 = \text{const}, y_2 = \text{const}$), trục đối xứng thẳng đứng $x = x_{\text{center}}$, hai cạnh bên bằng nhau ($AD = BC$), hai góc kề đáy bằng nhau.
  6. **Tam giác đều / cân:** Tam giác đều cạnh $a$ thì chiều cao tính đúng $h = \frac{a\sqrt{3}}{2}$, đỉnh nằm chính giữa trung điểm đáy. Tam giác vuông có góc $90^\circ$ và ký hiệu góc vuông chuẩn (`<path>` hoặc `<polyline>` kích thước $8\times 8\text{ px}$ hoặc $10\times 10\text{ px}$).
  7. **Đường gióng kích thước (Dimension lines):** Vẽ song song với cạnh tương ứng, có vạch chặn/mũi tên hai đầu rõ ràng, con số ghi kích thước đặt ở vị trí trung tâm, dễ đọc.

### Vá 9 — Chế độ Dạy học Song ngữ (Bilingual Teaching Mode: VI / EN)

- **Mục tiêu:** Phục vụ các trường chuẩn quốc tế, lớp song ngữ Cambridge / IB, dự án STEM giảng dạy bằng tiếng Anh.
- **Cơ chế chuyển đổi (Instant Switch 0ms):**
  1. Thanh điều khiển có nút chuyển: `[🌐 VI / EN]` (hoặc `[🇻🇳 Tiếng Việt] / [🇬🇧 English]`).
  2. Cấu trúc lưu trữ dữ liệu song ngữ: Mỗi khối nội dung hoặc slide hỗ trợ cấu trúc song ngữ (thông qua thuộc tính `data-lang-vi` / `data-lang-en` hoặc các lớp con `.lang-vi` và `.lang-en`).
  3. Khi bấm chuyển đổi: Tự động đổi tức thì toàn bộ tiêu đề, đề mục ghi bảng, câu hỏi hoạt động, chú thích hình vẽ sang tiếng Anh mà không cần tải lại trang hay gián đoạn bài giảng.
  4. **Chuẩn thuật ngữ Toán học quốc tế (Bilingual Math Glossary):**
     - Phương trình tích: *Product Equation*
     - Phương trình chứa ẩn ở mẫu: *Equation with Rational Expressions / Algebraic Fractions*
     - Điều kiện xác định (ĐKXĐ): *Domain Restrictions / Constraints*
     - Tập nghiệm: *Solution Set*
     - Nghiệm của phương trình: *Solution / Root*
     - Biến đổi tương đương: *Equivalent Transformation*
     - Khử mẫu: *Clearing Denominators / Multiply by LCD*
     - Hằng đẳng thức: *Algebraic Identity*
     - Hoạt động khám phá: *Exploration Activity*
     - Luyện tập: *Practice / Exercise*
     - Vận dụng: *Application*
     - Đố vui / Thử thách: *Challenge / Quiz*
  5. Giữ nguyên công thức Toán MathJax ($x, y, =, \ge$), chuyển ngữ chuẩn xác các câu dẫn giải và kết luận.

### Vá 10 — Tách bước sư phạm giữa Đề bài và Lời giải (Step-by-step Pedagogical Split)

- **Tôn chỉ sư phạm tương tác:** Tuyệt đối không để Đề bài và Lời giải chi tiết xuất hiện cùng một lúc trong 1 bước trình chiếu. Phải cho học sinh cơ hội đọc đề, tư duy, thực hiện nhiệm vụ rồi giáo viên mới bấm chuyển bước hiện lời giải/đáp án đối chiếu.
- **Quy tắc khi tạo bài giảng ban đầu:** Mọi hoạt động khám phá, ví dụ mẫu, luyện tập, bài tập thực tế phải tách riêng: Đề bài/Yêu cầu (bước $n$) và Hướng dẫn giải/Lời giải chi tiết (bước $n+1$).
- **Công cụ tương tác tùy biến trong Chế độ Thiết kế:**
  1. **Quét chọn tách bước (Highlight & Split):** Giáo viên dùng chuột bôi đen đoạn văn bản cần tách (như đoạn "Bước giải:..."), nút nổi `[✂️ Tách thành bước mới (+1 step)]` lập tức xuất hiện ngay trên vùng chọn. Click vào là đoạn đó được tự động cắt ra thành một khối độc lập nằm liền kề với bước kế tiếp ($n+1$).
  2. **Nút `[✂️ Tách]` trên thanh công cụ của khối:** Tự động phát hiện điểm chia tách lời giải ("Bước giải:", "Lời giải:", "Hướng dẫn giải:", "Đáp án:") hoặc tách ngay đoạn đang bôi đen.
  3. Tất cả các khối sau khi tách đều có thể dịch chuyển thứ tự bước (`▲ ▼`), cài đặt hiệu ứng biến mất (`💨 Biến mất`) và lưu vĩnh viễn vào file khi bấm `[💾 Lưu bài giảng]`.

### Vá 11 — Di chuyển vị trí hiển thị của khối và Kéo thả trực quan (Drag & Drop Block Reordering)

- **Hoán đổi vị trí hiển thị thực tế trong DOM:** Nút `▲` và `▼` trên thanh công cụ của khối thực sự hoán đổi vị trí hiển thị của khối trong DOM (sử dụng `prev.before(el)` và `next.after(el)`), đảm bảo trật tự trình chiếu và bố cục bảng thay đổi theo ý giáo viên.
- **Kéo thả HTML5 Drag & Drop mượt mà:** Khối có tay cầm kéo thả `⠿` (`.drag-handle`), giáo viên có thể giữ chuột và kéo thả khối lên/xuống trong cùng một cột hoặc hoán đổi giữa 2 cột (Cột Ghi Bảng $\leftrightarrow$ Cột Hoạt Động).
- **Tuyệt đối không chặn bôi đen văn bản:** Khối nội dung chỉ được gán `draggable="true"` khi giáo viên nhấn chuột vào tay cầm `⠿`. Ở các vị trí khác trong khối, giáo viên tự do quét chọn (bôi đen) văn bản để sao chép hoặc click nút `[✂️ Tách]` mà không bị kéo giật phần tử ngoài ý muốn.
- **Bảo lưu thứ tự:** Thứ tự hiển thị sau khi kéo thả hoặc bấm nút `▲ ▼` được lưu tự động vào LocalStorage và lưu đè vĩnh viễn vào tệp HTML khi bấm `[💾 Lưu bài giảng]`.

### Vá 12 — Tinh gọn Tiêu đề, Nhãn cột và Loại bỏ nội dung trùng lặp / rườm rà (Header Minimalism & Clean Blackboard Content)

- **Tiêu đề Slide (Header Bar):** Chỉ hiển thị tên bài học chính (`BÀI 4: PHƯƠNG TRÌNH QUY VỀ PHƯƠNG TRÌNH BẬC NHẤT MỘT ẨN`), loại bỏ huy hiệu tiết (`Tiết 1: ...`, `Tiết 2: ...`) gây xuống dòng, chật chội và vỡ bố cục trên thanh điều hướng.
- **Nhãn cột ngắn gọn, trực diện:**
  - Cột trái: `📌 PHẦN GHI BẢNG` (tuyệt đối không ghi dài dòng `(BẢNG PHẤN GIÁO VIÊN)`).
  - Cột phải: `✍️ HOẠT ĐỘNG HỌC TẬP` (tinh gọn, tránh rườm rà).
- **Loại bỏ triệt để dòng "Đề mục" và ghi chú giáo án trong bảng:**
  - Khi khối ghi bảng đã có tiêu đề mục (ví dụ `<strong>1. PHƯƠNG TRÌNH TÍCH</strong>`, `<strong>2. PHƯƠNG TRÌNH CHỨA ẨN Ở MẪU</strong>`), tuyệt đối không lặp lại dòng `• Đề mục: 1. Phương trình tích.` hay `• Đề mục: 2. Phương trình chứa ẩn ở mẫu.`.
  - Tuyệt đối không đưa các câu ghi chú tiến trình giáo án của giáo viên (như `• Đang thực hiện các hoạt động hình thành kiến thức...`, `• Đang thực hiện hoạt động khám phá nhu cầu đặt điều kiện...`) vào phần ghi bảng của học sinh. Phần ghi bảng chỉ chứa công thức, dạng tổng quát, định nghĩa, chú ý hoặc quy tắc toán học cốt lõi.

### Vá 13 — Sửa trực quan trực tiếp trên Slide (WYSIWYG In-Place Editing) & Tự động dịch linh hoạt dấu câu (Punctuation-Agnostic Auto-Translation)

- **Sửa trực tiếp, trực quan trên slide (WYSIWYG):** Trong Chế độ Thiết kế (`⚙ Thiết kế`), giáo viên click chuột trực tiếp vào bất kỳ đoạn văn bản hay tiêu đề nào trên slide để sửa (như Word hay PowerPoint). Muốn xóa dấu 2 chấm, sửa chính tả hay thêm từ chỉ cần click và nhấn Backspace/gõ trực tiếp. Tuyệt đối không bắt giáo viên phải mở modal code textarea hay nhìn thấy mã SVG của MathJax.
- **Bảo vệ an toàn công thức Toán học MathJax:** Các thẻ công thức `<mjx-container>` được đặt `contenteditable="false"`, hoạt động như khối nguyên tử an toàn (không bị vỡ mã SVG). Click chuột vào công thức sẽ mở hộp thoại sửa nhanh mã LaTeX (`prompt`), MathJax tự động render lại ngay lập tức.
- **Tự động dịch thông minh bảo tồn dấu câu (Punctuation-Agnostic Translation):** Việc dịch thuật sang tiếng Anh khi bật Song ngữ là nhiệm vụ tự động của hệ thống. Bộ dịch của hệ thống tự động bóc tách dấu câu ở đuôi (`:`, `.`, `?`, `!`, `,`), nếu giáo viên xóa dấu 2 chấm ở bản tiếng Việt thì bản dịch tiếng Anh cũng tự động không có dấu 2 chấm. Giáo viên hoàn toàn tự do sửa văn bản mà không sợ làm mất khả năng dịch song ngữ.
- **Thêm hiệu ứng trực tiếp khi bôi đen (Inline Step Animation):** Giáo viên dùng chuột bôi đen bất kỳ đoạn chữ hay công thức nào $\rightarrow$ thanh công cụ nổi xuất hiện: `[👁️ Xuất hiện (+1 bước)]`, `[💨 Biến mất]`, `[⭐ Nổi bật]`. Đoạn được chọn được gắn hiệu ứng xuất hiện ngay trong đoạn văn bản hiện tại (hiển thị huy hiệu `⚡[Bước N]` trong Chế độ Thiết kế), không bị cắt khối, không sinh ra tiêu đề "HƯỚNG DẪN GIẢI / BƯỚC TIẾP THEO" làm vỡ bố cục slide.

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

## 6. Bảng kiểm tra toàn diện trước khi xuất xưởng (Pre-flight Checklist)

Trước khi xuất file HTML thành phẩm, bắt buộc đối chiếu đủ 7 tiêu chí kiểm tra thực chiến sau:

1. **Cho phép bôi đen quét chọn chuột (`user-select: text`):**
   - Tuyệt đối không để `user-select: none;` trên toàn trang `body` khiến người dùng không thể quét chọn văn bản.
   - Luôn thiết lập `user-select: text !important;` cho `.content-block`, `.block-body`, `.slide-item`, `.slide-deck` và `body.mode-design`.
   - Nút nổi tím `[✂️ Tách thành bước mới (+1 step)]` phải kích hoạt mượt mà khi người dùng bôi đen đoạn văn bản trong chế độ Thiết kế.

2. **Bộ Soạn thảo Đa phương tiện Toàn diện (Rich Editor Suite):**
   - Trên mỗi khối phải có nút trực quan: `▲ ▼`, `[✏️ Sửa]`, `[💨 Biến mất]`, `[✂️ Tách]`, `[👁️/⏱]`, `[✕]`.
   - Ở cuối mỗi cột phải có nút `[➕ Thêm khối ghi bảng]` và `[➕ Thêm hoạt động học sinh]`.
   - Modal soạn thảo phải có:
     + Ô sửa tiêu đề khối (`editTitleInput`) và ô nội dung (`editTextarea`).
     + Nút định dạng chữ (`<b>`, `<i>`, `<u>`, `<mark>`, `<br>`, `• `).
     + Nút công thức Toán LaTeX (`$..$`, `$$..$$`, `\frac{a}{b}`, `\sqrt{x}`, `x^2`, `\cdot`, `\Leftrightarrow`, `\neq`, `{Hệ}`).
     + Nút chèn ảnh mạng (URL) và tải ảnh từ máy tính (tự encode Base64 lưu trực tiếp vào file HTML để mang sang máy khác không bị mất ảnh).
     + Nút chèn video (YouTube nhúng responsive 16:9 hoặc video MP4).
     + Khung xem trước trực tiếp (Live Preview) với MathJax typeset thời gian thực.

3. **Hình học SVG chính xác tuyệt đối (Mathematical Exactness):**
   - Tọa độ đỉnh phải tính toán giải tích chính xác theo số liệu toán học; cấm vẽ ước chừng làm biến dạng hình học (hình vuông thành chữ nhật, hình thang cân thành hình thoi, tam giác đều lệch góc).
   - Thiết lập `viewBox` chuẩn và `preserveAspectRatio="xMidYMid meet"` để không bao giờ bị méo hình.

4. **Tách bước sư phạm Đề bài và Lời giải (Step-by-step Separation):**
   - Đề bài / Câu hỏi ở bước $n$.
   - Lời giải / Hướng dẫn giải ở bước $n+1$. Tuyệt đối không hiện cùng lúc.

5. **Hiệu ứng Trình chiếu và Biến mất:**
   - Mỗi khối có `data-step` để xuất hiện tuần tự khi bấm phím `Space`, `→` hoặc chạm vùng trống.
   - Hỗ trợ `data-exit-step` (bước biến mất / Fade Out) và tự động hiện lại khi lùi bước (`↩ Lùi 1 bước`).

6. **Chế độ Song ngữ (Bilingual Mode: VI / EN):**
   - Có nút `[🌐 Song ngữ (VI/EN)]` trên thanh điều khiển.
   - Chuyển đổi tức thì (0ms) tiêu đề bài học, tiêu đề tiết, nhãn cột, đề mục và các nút điều khiển sang Tiếng Anh học thuật chuẩn quốc tế.

7. **Lưu trực tiếp đè vào file (Save Lecture):**
   - Nút `[💾 Lưu bài giảng]` sử dụng File System Access API (`window.showSaveFilePicker()`) để ghi đè trực tiếp lên file đang mở.
   - Tự động làm sạch clone DOM (gỡ bỏ trạng thái tạm thời, modal, tooltip, đưa về Slide 1) trước khi lưu.

