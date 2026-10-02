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

### Vá 14 — Trình chiếu 16:9 Fit-to-Screen hoàn hảo (Không thanh cuộn trong slide) & Loại bỏ hoàn toàn chất giáo án hành chính (Presentation Slides vs. Lesson Plans)

- **Phân biệt rạch ròi giữa Bài giảng Trình chiếu (Presentation Slide) và Giáo án (Lesson Plan / KHBD):**
  - **Bài giảng trình chiếu:** Sản phẩm chiếu lên màn hình máy chiếu hoặc TV cho TOÀN BỘ HỌC SINH quan sát và tương tác trong tiết học.
  - **Tuyệt đối cấm đưa vào slide các câu khẩu lệnh sư phạm giáo án:**
    + Cấm ghi các câu hướng dẫn tổ chức lớp của giáo viên: *"Hai học sinh lên bảng làm 2 câu"*, *"Cả lớp làm vào vở nháp"*, *"Quan sát nhận xét bài làm của bạn"*, *"Thảo luận nhóm đôi trong 3 phút"*, *"Đang thực hiện hoạt động..."*.
    + Cấm ghi mục tiêu hành chính giáo án: *"Mục tiêu bài học: Giúp học sinh nắm vững..."*.
    + Cấm đặt tên tiêu đề mang tính sư phạm nội bộ: *"Chốt kiến thức sư phạm"*, *"Nhiệm vụ học sinh tại lớp"*, *"Đánh giá kết quả vận dụng"*. Thay bằng tiêu đề chuẩn học thuật: *"ĐỀ BÀI & YÊU CẦU"*, *"CHÚ Ý QUAN TRỌNG"*, *"KẾT LUẬN THỰC TIỄN"*.
  - **Cấu trúc 2 cột thuần túy học thuật cho học sinh:**
    + Cột trái (`📌 PHẦN GHI BẢNG`): Chứa định nghĩa, công thức toán, dạng tổng quát, phương pháp giải, hệ thống bài tập và kết luận cốt lõi mà học sinh cần ghi nhớ hoặc chép vào vở.
    + Cột phải (`✍️ HOẠT ĐỘNG HỌC TẬP`): Chứa đề bài toán học to rõ, hình vẽ minh họa SVG chuẩn xác, câu hỏi trắc nghiệm tương tác, gợi ý và lời giải mẫu ẩn/hiện theo từng bước bấm chuột.
- **Trình chiếu 16:9 Fit-to-Screen hoàn hảo & Khóa thanh cuộn (Zero Internal Scrollbar):**
  - Trong Chế độ Trình chiếu (`mode-present`): Khung slide khóa tỷ lệ chuẩn 16:9 (`width: min(100vw, calc(100vh * 16 / 9))`, `height: min(100vh, calc(100vw * 9 / 16))`, `aspect-ratio: 16 / 9`).
  - Toàn bộ nội dung mỗi slide phải nằm gọn hoàn toàn trong khung nhìn 16:9, tuyệt đối không xuất hiện thanh cuộn dọc bên trong các cột (`overflow: hidden !important` trên `.col-board` và `.col-task`).
  - Cỡ chữ, khoảng cách đệm (padding, margin) và kích thước hình vẽ SVG được tính toán tối ưu để trình chiếu từ xa rõ nét mà không làm tràn khung.
  - Hỗ trợ nút toàn màn hình `[⛶ Toàn màn hình]` (F11) và phím bấm điều hướng mượt mà.

### Vá 15 — Chuẩn hóa Song ngữ 100% (Bilingual 100% Dual-Data Attribute Architecture)

- **Kiến trúc Song ngữ Dual-Data Attribute (100% Bilingual Presentation):**
  - Mọi khối `.content-block` đều được gán sẵn các thuộc tính:
    + `data-raw-vi="..."`: nội dung tiếng Việt gốc.
    + `data-raw-en="..."`: nội dung tiếng Anh học thuật đã biên dịch chuẩn xác 100%.
    + `data-title-vi="..."`: tiêu đề khối tiếng Việt.
    + `data-title-en="..."`: tiêu đề khối tiếng Anh.
  - Khi bấm chuyển ngữ `[🌐 Song ngữ (VI/EN)]`:
    + Chuyển sang EN: cập nhật ngay `strong.textContent = data-title-en`, `body.innerHTML = data-raw-en`.
    + Chuyển về VI: cập nhật ngay `strong.textContent = data-title-vi`, `body.innerHTML = data-raw-vi`.
    + Đảm bảo 100% tiêu đề, nhãn cột, heading slide, và nội dung toàn bộ khối đều chuyển đổi tức thì, không sót bất kỳ đoạn nào.
    + Gọi ngay `window.MathJax.typesetPromise()` sau khi hoán đổi ngôn ngữ để render lại toàn bộ công thức toán học.
- **Tự động cập nhật bản dịch khi giáo viên chỉnh sửa:**
  - Khi giáo viên sửa nội dung trực tiếp (WYSIWYG) hoặc qua modal chỉnh sửa: hàm lưu tự động cập nhật cả `data-raw-vi` và `data-raw-en` thông qua bộ dịch `smartTranslateText()` tự động bóc tách dấu câu.
  - Bảng từ điển `contentPhraseMap` và `termMap` phải được khai báo ở phạm vi toàn cục (global scope) ngay đầu thẻ `<script>` để `smartTranslateText()` luôn truy cập được, tránh lỗi `ReferenceError`.
  - Sử dụng biểu thức chính quy Unicode boundary `(?<![\p{L}\p{N}])` và `(?![\p{L}\p{N}])` với flag `gui` để nhận diện chính xác các từ vựng tiếng Việt có dấu.

### Vá 16 — Trợ giảng AI Đọc bài giảng Tiếng Anh (English Text-to-Speech / Pedagogical Read-Aloud)

- **Công nghệ Web Speech API thuần trình duyệt (100% Offline & Native):**
  - Sử dụng `window.speechSynthesis` và `SpeechSynthesisUtterance`, tích hợp sẵn trong mọi trình duyệt hiện đại (Chrome, Edge, Safari, Firefox), chạy offline trực tiếp qua giao thức `file:///` mà không cần server hay API key.
  - Tự động ưu tiên chọn các giọng đọc tiếng Anh tự nhiên chất lượng cao (`Google US English`, `Microsoft Natural`, `Samantha`,...).
- **Tốc độ đọc linh hoạt & chuẩn ngữ điệu sư phạm (Pedagogical Rates with Switcher):**
  - Mặc định đọc ở mức sư phạm `rate: 0.85` (chậm rãi, phát âm từng âm tiết tròn vành rõ chữ, có ngữ điệu ngắt nghỉ tự nhiên giúp học sinh dễ dàng nghe hiểu môn Toán bằng tiếng Anh).
  - Tích hợp nút điều chỉnh tốc độ đọc trực tiếp trên thanh điều khiển: **`[⚡ 0.85x]`** cho phép luân chuyển 4 nấc:
    + `⚡ 0.85x` (Chậm vừa - Mặc định sư phạm).
    + `⚡ 0.75x` (Rất chậm - Dành cho lớp mới bắt đầu nghe Toán tiếng Anh).
    + `⚡ 0.5x` (Siêu chậm - Phát âm cực chậm, hỗ trợ học sinh nghe kỹ từng âm vị toán học).
    + `⚡ 1.0x` (Tự nhiên - Tốc độ bản ngữ chuẩn).
    + Tự động lưu thiết lập vào `localStorage ('lecture_speech_rate_idx')`.
  - **Nút hướng dẫn tắt phụ đề tự động `[💬 Tắt phụ đề]`:** Cung cấp thông tin nhanh để giáo viên tắt tính năng Live Caption (phụ đề màu đen) của Windows (`Win + Ctrl + L`) hoặc Google Chrome.
- **Bộ chuyển đổi ký hiệu Toán học sang lời nói tiếng Anh tự nhiên (`mathToSpokenEnglish`):**
  - Tuyệt đối không để AI đọc các ký hiệu LaTeX thô (như gạch chéo `\`, ngoặc nhọn `{}`).
  - Tự động chuyển đổi các công thức, hàm số, phân số, phương trình sang tiếng Anh sư phạm:
    + `(ax+b)(cx+d) = 0` $\rightarrow$ *"open parenthesis a x plus b close parenthesis open parenthesis c x plus d close parenthesis equals 0"*
    + `P(x) = 0` $\rightarrow$ *"P of x equals 0"*
    + `x \ne 1` $\rightarrow$ *"x is not equal to 1"*
    + `\frac{a}{b}` $\rightarrow$ *"a over b"*
    + `x^2` $\rightarrow$ *"x squared"*, `x^3` $\rightarrow$ *"x cubed"*
    + `169\text{ m}^2` $\rightarrow$ *"169 square meters"*, `15\text{ m}` $\rightarrow$ *"15 meters"*
    + `\Leftrightarrow` $\rightarrow$ *"is equivalent to"*, `\Rightarrow` $\rightarrow$ *"implies that"*
- **Hai chế độ nghe đọc linh hoạt và phản hồi trực quan:**
  - **Nút trên thanh điều khiển `[🔊 Đọc Slide (EN)]`:** Tự động đọc lần lượt từ tiêu đề slide đến từng khối nội dung hiển thị; khối đang đọc sẽ phát sáng viền xanh tím nhẹ (`is-speaking`) giúp học sinh dõi mắt theo bài; nút chuyển thành `[⏹ Dừng đọc]` và tự động hủy đọc nếu giáo viên bấm chuyển slide.
  - **Nút loa `🔊` trên từng khối (`.btn-block-speak`):** Bố trí gọn gàng ở góc trên mỗi khối (`top: 6px; right: 8px;`); giáo viên hoặc học sinh bấm vào để nghe riêng khối đó; bấm lại để dừng ngay lập tức.

### Vá 17 — Cỡ chữ Chuẩn Trình chiếu TV Phòng học (28px - 30px) & Đồng bộ Trực quan Mắt Thấy - Tai Nghe (Screen-Audio Sync)

- **Chuẩn Cỡ chữ Trình chiếu TV Lớp học (28px - 30px):**
  - Màn hình lớp học thường là TV 55" - 65" - 75" hoặc máy chiếu, học sinh ngồi xa 6 - 8 mét. Cỡ chữ 15px - 16px (laptop) là quá nhỏ.
  - Trong Chế độ Trình chiếu (`mode-present`), cỡ chữ bài học được cố định chuẩn TV:
    + Thân khối bài học (`.content-block`): **28px** (khoảng cách dòng `line-height: 1.55` thoáng đãng, dễ đọc từ xa).
    + Tiêu đề khối (`strong`): **30px – 32px**.
    + Tiêu đề slide (`slide-heading-text`): **32px – 34px**.
    + Nhãn cột (`col-board-tag`, `col-task-tag`): **22px – 24px**.
    + Công thức toán học MathJax tự động phóng to đồng bộ, sắc nét, tương phản cao.
  - Bố trí nút chọn cỡ chữ trực tiếp trên thanh điều khiển: **`[🔤 TV 28px]`** cho phép chuyển đổi linh hoạt:
    + `TV 28px` (Chuẩn TV lớp học 55"-65" - Mặc định).
    + `TV Lớn 30px` (Dành cho TV 75"-85" hoặc phòng học rộng).
    + `Laptop 22px` (Khi soạn bài hoặc xem trên laptop nhỏ).
    + Tự động lưu cấu hình vào `localStorage`.
- **Đồng bộ Tuyệt đối Mắt Thấy - Tai Nghe (Visual & Audio Synchronization):**
  - Khi bấm đọc tiếng Anh (`[🔊 Đọc Slide (EN)]` hoặc nút loa `🔊` trên khối), nếu màn hình đang hiển thị Tiếng Việt:
    + Hệ thống **tự động chuyển giao diện slide sang Tiếng Anh** để học sinh nhìn thấy chữ tiếng Anh trên màn hình khớp 100% từng từ với giọng đọc AI, tránh tình trạng màn hình hiển thị tiếng Việt mà tai lại nghe tiếng Anh.
    + Khối đang đọc tự động phát sáng viền (`is-speaking`) để học sinh dễ dàng định vị điểm nhìn.
- **Phân biệt tính năng Phụ đề hệ điều hành (Windows Live Captions):**
  - Hộp đen phụ đề `Live Caption / More knowledge focus` ở góc dưới màn hình là tính năng có sẵn của hệ điều hành Windows 11 / Chrome (phím tắt `Win + Ctrl + L`), không phải do file HTML sinh ra. Giáo viên có thể tắt bằng cách bấm `Win + Ctrl + L` hoặc bấm nút `✕`.

### Vá 18 — Khắc phục triệt để lỗi che khuất đáy cuộn (Full Bottom Scroll Clearance & No Truncation)

- **Tự động kích hoạt con trỏ trượt khi nội dung vượt khung màn hình (`overflow-y: auto !important`):**
  - Khi trình chiếu ở cỡ chữ TV lớn (28px - 30px) hoặc các slide có nội dung dài/nhiều bước, nếu chiều cao cột vượt quá khung nhìn, hệ thống **tự động bật thanh cuộn trượt để kéo/lăn chuột xem toàn bộ nội dung** (`overflow-y: auto !important; overflow-x: hidden !important;`), tuyệt đối không bị che khuất, cắt cụt chữ hay mất thông tin bài học.
  - Thanh cuộn được thiết kế tinh tế, thanh mảnh (rộng 8px, màu xanh chàm dịu `#818cf8` bo tròn góc, hòa hợp với giao diện).
- **Ràng buộc chuẩn Flexbox cho lưới nội dung (`flex: 1 1 0; min-height: 0; height: 100%;`):**
  - Loại bỏ hoàn toàn công thức cứng `calc(100% - 44px)` vốn gây tràn khung 21px–30px ra ngoài `.slide-item`. Lưới bài giảng `.slide-content-grid` tự động co giãn vừa khít 100% diện tích khả dụng bên dưới tiêu đề slide.
- **Khoảng đệm an toàn đáy màn hình (Bottom Safety Padding 80px):**
  - Khung slide `.slide-item` được thiết lập khoảng đệm đáy an toàn `padding-bottom: 80px;` để mép dưới nội dung luôn dừng cao hơn thanh điều khiển nổi (nằm ở `bottom: 8px`), đảm bảo không bao giờ bị thanh công cụ che khuất dòng chữ cuối cùng.
- **Loại bỏ giới hạn chiều cao khối hiển thị (`max-height: none !important; overflow: visible !important;`):**
  - Các khối khi hiển thị (`.content-block.is-revealed`) không bị giới hạn 500px, tự động mở rộng theo đúng kích thước thực của nội dung, hình vẽ SVG và công thức toán.
- **Phần tử đệm ảo đáy cột (`::after` min-height: 85px):**
  - Bổ sung `body.mode-present .col-board::after, body.mode-present .col-task::after { content: ""; display: block; min-height: 85px; height: 85px; flex-shrink: 0; }`. Đảm bảo khi kéo lăn chuột đến tận cùng của bất kỳ cột nào, khối nội dung cuối cùng luôn cách đáy 85px, hiển thị 100% đầy đủ, không bao giờ bị che khuất.
- **Bảo toàn tuyệt đối hiển thị công thức MathJax (`inline-block` & `inline`):**
  - MathJax 3 sử dụng thẻ `<svg>` nội dòng để biểu diễn ký hiệu toán học. Cấm tuyệt đối việc dùng CSS dạng `.content-block svg` áp đặt `display: block` làm nhảy dòng công thức toán trong câu. Bắt buộc giữ `mjx-container { display: inline-block !important; }` và `mjx-container svg { display: inline !important; margin: 0 !important; }`.

### Vá 19 — Chuẩn Sư phạm Tách biệt Đề bài & Hướng dẫn giải (Problem & Guided Solution Split with Step Animation)

- **Nguyên tắc Sư phạm Bắt buộc: Đề bài riêng — Hướng dẫn giải riêng từng bước:**
  - Trong mọi hoạt động (Khám phá, Ví dụ, Luyện tập, Vận dụng, Bài tập):
    + **Khối ĐỀ BÀI (Problem Block):** Hiển thị riêng biệt (thường ở Bước 1 hoặc luôn hiển thị), chỉ chứa đề bài, số liệu, hình vẽ hoặc câu hỏi để học sinh có thời gian quan sát, ghi chép và tự tư duy giải quyết vấn đề.
    + **Khối HƯỚNG DẪN GIẢI / LỜI GIẢI (Solution Step Block):** Bắt buộc tách thành khối độc lập, gắn hiệu ứng bước (`data-step="2"`, `data-step="3"`,...). Khi giáo viên bấm chuyển bước thì lời giải mới xuất hiện, tuyệt đối không gộp chung đề bài và lời giải trong cùng 1 khối hiển thị đồng thời làm mất tính tương tác sư phạm.
- **Công cụ Hỗ trợ Thiết kế Trực quan (Design Mode Split Tool):**
  - Trong Chế độ Thiết kế: Tooltip nổi khi bôi đen văn bản tích hợp nút `[✂️ Tách Lời giải (+1 bước)]` giúp giáo viên chỉ cần quét chọn đoạn lời giải là hệ thống tự động tách thành khối Hướng dẫn giải riêng biệt mang hiệu ứng bước tiếp theo (`data-step="N+1"`).
  - Khối nội dung trong Chế độ Thiết kế hiển thị huy hiệu vai trò rõ ràng: `[📝 Đề bài]` màu vàng cam và `[💡 Lời giải]` màu xanh lá.

### Vá 20 — Tuân thủ Tuyệt đối Chuẩn Ký hiệu GDPT 2018 theo Cấp lớp & Nâng cao Chiều sâu Sư phạm (Curriculum Compliance & Pedagogical Depth)

- **Quy tắc Ký hiệu GDPT 2018 theo cấp học (Nghiêm cấm lấy kiến thức cấp trên đưa xuống cấp dưới):**
  - Căn cứ chính xác vào khối lớp đang dạy (Lớp 6, 7, 8, 9 THCS hay 10, 11, 12 THPT).
  - Với cấp THCS (Toán 6, 7, 8, 9 - SGK mới GDPT 2018 Kết nối tri thức, Cánh diều, Chân trời sáng tạo):
    + **TUYỆT ĐỐI CẤM dùng dấu tương đương `\Leftrightarrow` ($\Leftrightarrow$)** khi giải phương trình hoặc biến đổi biểu thức. Dấu tương đương thuộc kiến thức mệnh đề logic của THPT (Lớp 10).
    + **TUYỆT ĐỐI CẤM dùng dấu ngoặc vuông `[` (ký hiệu "hoặc" của hệ phương trình / tuyển mệnh đề cấp 3)** khi giải phương trình tích.
    + **TUYỆT ĐỐI CẤM kết luận tập nghiệm $S = \{...\}$:** Trong Toán THCS, không dùng thuật ngữ "tập nghiệm" hay ký hiệu $S = \{...\}$; bắt buộc kết luận bằng câu văn tự nhiên chỉ rõ từng nghiệm cụ thể (*"Vậy phương trình có nghiệm là..."*, *"Vậy phương trình có hai nghiệm là $x = ...$ và $x = ...$"*, *"Vậy phương trình vô nghiệm"*).
    + **BẮT BUỘC trình bày thuần túy bằng ngôn ngữ sư phạm tự nhiên**:
      * Dùng từ liên kết: *"Ta có: ..."*, *"suy ra"* (hoặc $\Rightarrow$), *"hay..."*, *"hoặc..."*.
      * Khi giải phương trình tích $(ax+b)(cx+d)=0$: Tách thành 2 phương trình riêng biệt:
        *"Ta có $ax+b=0$ hoặc $cx+d=0$."*
        *"1) Với $ax+b=0$, suy ra $x = -b/a$."*
        *"2) Với $cx+d=0$, suy ra $x = -d/c$."*
        *"Vậy phương trình có hai nghiệm là $x = -b/a$ và $x = -d/c$."*
- **Cấu trúc Chiều sâu Sư phạm theo Tính chất Tiết học:**
  - **Bài học mới (New Concept Lesson):**
    + Sau mỗi đơn vị kiến thức (mỗi mục/khái niệm vừa hình thành): Bắt buộc xây dựng **Bài tập kiểm tra đánh giá nhanh (Formative Assessment / Quiz Game tương tác)** với hệ thống nút bấm chọn phương án A, B, C, D đổi màu xanh (Đúng) / đỏ (Sai) tức thì và phân tích bẫy sai lầm của học sinh.
    + Kết thúc bài học: Bắt buộc có **Sơ đồ tư duy trực quan (SVG Mindmap / Concept Map)** hệ thống hóa toàn bộ mạng lưới kiến thức bài học và ứng dụng thực tiễn.
  - **Tiết Luyện tập chung / Ôn tập (Review / Practice Lesson):**
    + Bắt buộc có phần **Hệ thống hóa kiến thức trọng tâm** ở đầu tiết trước khi giải bài tập.
    + Chuyển linh hoạt từ các bài tập khô khan thành **Chuỗi thử thách trò chơi học tập tương tác** (Chặng 1: Vượt chướng ngại vật; Chặng 2: Giải mã mật mã; Chặng 3: Chinh phục thực tế,...).

### Vá 21 — Giữ nguyên vị trí Slide khi chuyển đổi Chế độ Thiết kế & Trình chiếu (Slide Preservation Across Modes)

- **Tự động cuộn đến đúng slide đang xem khi bật Thiết kế:**
  - Khi giáo viên đang xem Slide $N$ ở Chế độ Trình chiếu (`mode-present`) và bấm nút `[⚙️ Thiết kế]`: Hệ thống lập tức kích hoạt Chế độ Thiết kế và tự động cuộn màn hình (`scrollIntoView`) đến đúng vị trí Slide $N$, viền sáng màu chàm 1.5 giây để giáo viên nhận biết. Tuyệt đối không để màn hình nhảy về Slide 1 khiến giáo viên phải cuộn tìm kiếm.
- **Nhận diện slide hiển thị khi quay lại Trình chiếu:**
  - Khi giáo viên đang ở Chế độ Thiết kế, nếu đã cuộn đến hoặc click vào bất kỳ slide/khối nào, khi bấm nút `[🎬 Trình chiếu]`: Hệ thống tự động tính toán slide đang nằm gần đỉnh màn hình nhất (`getBoundingClientRect`) để mở trực tiếp đúng slide đó trong Chế độ Trình chiếu.
  - Khi click hoặc chỉnh sửa bất kỳ khối nào trong Chế độ Thiết kế, biến `currentSlideIndex` tự động cập nhật ngay lập tức theo slide tương ứng.

### Vá 22 — Phóng to Hình học & Ảnh minh họa (Interactive Lightbox Zoom)

- **Tôn chỉ sư phạm trực quan:** Trên màn hình máy chiếu hoặc TV lớp học, học sinh ngồi xa có thể khó nhìn rõ các chi tiết số liệu, góc, tên đỉnh trên hình học hoặc sơ đồ tư duy. Do đó, mọi hình vẽ SVG và ảnh minh họa đều được trang bị tính năng bấm vào để phóng to toàn màn hình.
- **Quy chuẩn kỹ thuật của Lightbox Zoom:**
  1. **Hiệu ứng trực quan khi di chuột:** Con trỏ chuột tự động đổi thành kính lúp `cursor: zoom-in`, hình vẽ nổi bật nhẹ (`filter: drop-shadow`) và hiển thị gợi ý `"🔍 Nhấn vào hình để phóng to"`.
  2. **Hộp thoại phóng to (Lightbox Dialog):**
     - Nền tối mờ sang trọng (`backdrop-filter: blur(8px)`).
     - Hình vẽ SVG vector được clone và co giãn tự động không vỡ nét lên tới 92vw / 80vh.
     - Thanh công cụ điều khiển: Nút `[➕ Phóng to]`, `[➖ Thu nhỏ]`, `[🔄 Kích thước chuẩn 100%]`, hiển thị tỷ lệ zoom hiện tại.
     - Cho phép lăn chuột (mouse wheel) để phóng to / thu nhỏ mượt mà.
     - Hỗ trợ giữ chuột kéo rê (pan/drag) để quan sát từng chi tiết khi đang zoom lớn.
     - Đóng nhanh bằng phím `Escape`, nút `✕` hoặc click ra ngoài vùng nền mờ.
  3. **Event delegation trên `#slideDeck`:** bắt click phóng to mọi `svg` (trừ `mjx-container`), `img`, `.figure-box`, `[data-zoomable]`. Click hình không được gọi `nextStep()`. Delegation vẫn còn sau `toggleBilingual` hoặc khi gán lại `innerHTML` trong chế độ Thiết kế.

### Vá 23 — Dẫn dắt Sư phạm 4 bước Độc lập (4-Step Pedagogical Scaffolding)

- Mỗi ví dụ, bài tập, luyện tập tách đúng 4 bước `data-step`, không gộp gợi ý với lời giải và đáp án:
  + Bước 1 (`data-step="1"`): Đề bài và hình vẽ ban đầu. Cột ghi bảng chỉ ghi tiêu đề mục hoặc để trống.
  + Bước 2 (`data-step="2"`): Gợi ý / dẫn dắt / câu hỏi tư duy. Cấm hiện đáp án hay lời giải.
  + Bước 3 (`data-step="3"`): Các bước giải chi tiết, biến đổi tương đương, tính toán.
  + Bước 4 (`data-step="4"`): Chốt đáp số và nội dung kiến thức cốt lõi để học sinh ghi bảng, chép vở.
- Đáp số cuối (câu «Vậy») chỉ hiện ở bước 4, ví dụ bằng `inline-anim` `data-step="4"`.
- **Nguyên tắc Đồng hành Đề bài - Hình vẽ:** SVG hoặc ảnh minh họa bắt buộc cùng `data-step` với đề bài hoặc tình huống mà nó minh họa (nhúng trong khối đề, hoặc khối hình cùng số bước). Cấm tách hình sang bước sau khiến đề bài bị trống hình.
- **Nguyên tắc Phân bước Tuần tự 2 cột:** Trong một slide, cấm gán cùng một số `data-step` (kể cả `data-step="1"`) cho cả Cột Ghi Bảng và Cột Hoạt Động. Mỗi lần bấm chỉ hiện một ý: bước 1 là đề bài kèm hình; bước sau mới tới cột còn lại.

### Vá 24 — Tương thích 100% Bút trình chiếu & Điều hướng Bàn phím đa năng (Universal Presenter & Key Navigation)

- Phím tiến: `ArrowRight`, `ArrowDown`, `PageDown`, `Space`, `Enter` gọi `nextStep()`.
- Phím lùi: `ArrowLeft`, `ArrowUp`, `PageUp`, `Backspace` gọi `prevStep()`.
- Phím màn hình đen `b` và `.` bật/tắt lớp `.blank-screen`.
- Gọi `preventDefault()` để trình duyệt không cuộn trang hoặc quay lại lịch sử.
- Sau khi bấm nút trên `.control-bar`, gọi `blur()` để phím `Space` không kích hoạt lại nút đang focus.

### Vá 25 — Công cụ Trợ giảng Trực quan: Con trỏ Laser Đỏ & Bút vẽ Đánh dấu trên Slide (Virtual Laser Pointer & In-Slide Annotation Canvas)

- `#laserPointer`: chấm đỏ 22px, `radial-gradient`, `box-shadow: 0 0 14px 4px rgba(239, 68, 68, 0.85)`, bám `clientX`/`clientY`. `toggleLaserMode` bật `body.laser-mode` và `cursor: none`.
- `#drawCanvas`: canvas phủ slide, dưới `#controlBar`. `togglePenMode` bật vẽ chuột và cảm ứng. `setPenColor('#ef4444', 3, false)` là bút đỏ; `setPenColor('rgba(250, 204, 21, 0.45)', 14, true)` là dạ quang. `clearDrawCanvas()` xóa nét; `updateSlideDisplay()` cũng xóa khi đổi slide.
- Phím `L` bật/tắt laser, `P` bật/tắt bút, `C` xóa nét, `Escape` tắt laser và bút. Bật bút thì tắt laser, và ngược lại.
- `#penPalette` chỉ hiện khi đang vẽ. Nút trên `#controlBar`: `[🔴 Laser]` và `[✏️ Vẽ]`.
- **Vá 25b:** Trong listener click của `#slideDeck`, nếu `document.body.classList.contains('laser-mode')` thì `return` ngay, không gọi `nextStep()`.

### Vá 26 — Cột Ghi bảng Sư phạm và giọng đọc tiếng Việt Natural

- Tiêu đề mục và định lí cốt lõi nằm ở đầu Cột Ghi bảng, `data-step="0"` (luôn hiện). Các slide ví dụ và luyện tập của cùng một mục phải bảo lưu khối đó (`core-board`), không thay bảng bằng đề bài.
- `getSweetVietnameseVoice()` chỉ nhận voice `vi` có chữ `Natural` (ưu tiên `HoaiMy` hoặc `NamMinh`). `speakBlockVi` không đọc bằng giọng Google. Nếu không có voice Natural, hiện toast: *"Để trải nghiệm giọng đọc AI Hoài My truyền cảm, Thầy/Cô vui lòng mở bài giảng trên trình duyệt Microsoft Edge."*
- `playAudioOrSpeech()` phát `audio/slide-N.mp3` giọng `vi-VN-HoaiMyNeural` trước. Không có file thì mới gọi `speakBlockVi`. File `Chay_Bai_12_Bang_Edge.bat` mở bài bằng `msedge`. Script `export_hoaimy_audio.py` dùng `edge_tts` để xuất các MP3 đó.

### Vá 27 — Đọc tiếng Việt từng khối, Chuẩn hóa từ viết tắt & đơn vị đo lường Toán - Lý - Hóa, Gom nhóm thanh điều khiển tinh gọn

- Khi nhấn loa `🔊` trên từng khối (`speakBlockAuto`), chỉ đọc DUY NHẤT khối đó bằng giọng Hoài My (`speakBlockVi(blockEl)`), không đọc cả slide. Nút `[🗣️ Đọc slide]` trên thanh điều khiển mới phát toàn bộ slide.
- **Bộ chuẩn hóa sư phạm `vietnameseMathToSpeech()`:** Tự động chuyển đổi toàn diện các từ viết tắt chuyên môn và đơn vị đo lường Toán - Lý - Hóa sang cách đọc tiếng Việt chuẩn:
  + Đơn vị độ dài: `120m` $\rightarrow$ *"120 mét"*, `250 m` $\rightarrow$ *"250 mét"*, `km`, `dm`, `cm`, `mm`.
  + Đơn vị kép & diện tích/thể tích: `500 km/h` $\rightarrow$ *"500 ki-lô-mét trên giờ"*, `m/s`, `m^2` $\rightarrow$ *"mét vuông"*, `m^3` $\rightarrow$ *"mét khối"*, `lít`, `ml`.
  + Đơn vị Lý - Hóa: `kg`, `g`, `N` (Niu-tơn), `J` (Jun), `W` (Oát), `Pa` (Pát-xcan), `V` (Vôn), `A` (Am-pe), `°C` (độ C), `%` (phần trăm), `mol`.
  + Số thập phân: `1,2` $\rightarrow$ *"1 phẩy 2"*, `8,6` $\rightarrow$ *"8 phẩy 6"*.
  + Từ viết tắt: `SGK` $\rightarrow$ *"sách giáo khoa"*, `GV`, `HS`, `HĐ1` $\rightarrow$ *"hoạt động 1"*, `(H.4.17)` $\rightarrow$ *"(Hình 4.17)"*, `tr.74` $\rightarrow$ *"trang 74"*, `tam giác ABC` $\rightarrow$ *"tam giác A B C"*, đoạn thẳng `AB` $\rightarrow$ *"A B"*.
  + Lượng giác & ký hiệu: $\sin, \cos, \tan, \cot$, căn bậc hai, phân số, góc, vuông góc, song song.
  + Ký hiệu dấu phẩy toán học: Đỉnh $P'$ $\rightarrow$ *"P phẩy"*, $M'$ $\rightarrow$ *"M phẩy"*, $N'$, $A'$, đoạn thẳng $AB'$ $\rightarrow$ *"A B phẩy"*, $P'P$ $\rightarrow$ *"P phẩy P"*, $y''$ $\rightarrow$ *"y hai phẩy"*, góc $19^\circ 30'$ $\rightarrow$ *"19 độ 30 phút"*. Tự động giải mã thực thể HTML `&#x27;` và `\prime` trước khi đọc.
- Thanh điều khiển `#controlBar` gom nhóm thành 4 cụm bo tròn (`.ctrl-group`): Điều hướng, Chọn tiết học, Công cụ trợ giảng, Cài đặt & Đa phương tiện, chống tràn màn hình.

### Vá 28 — Menu Chuột Phải Sư Phạm (Quick Context Menu cho Laser & Vẽ)

- Tích hợp menu chuột phải trên slide: Nhấn chuột phải hiện ngay menu nổi tại vị trí con trỏ gồm: 🔴 Con trỏ Laser (L), ✏️ Bút vẽ (P), 🟡 Dạ quang, 🗑️ Xóa nét (C), 📋 Bảng viết (W), ↪️ Tiến / ↩️ Lùi bước. Tiện lợi tối đa khi giảng dạy bằng chuột không dây hoặc bút cảm ứng.

### Vá 29 — Thanh công cụ đảo nổi chia nhóm, Chuột phải tích hợp đầy đủ công cụ và Bộ công cụ Sư phạm Đặc biệt (Đồng hồ đếm ngược, Vòng quay gọi tên, Thước hình học ảo, Bảng viết phấn đa bề mặt)

- **Thanh điều khiển nổi (`#controlBar`) gom 5 cụm độc lập (Floating Pill Islands):**
  + `.control-bar` có nền trong suốt (`background: transparent; border: none; box-shadow: none; pointer-events: none;`), các cụm `.ctrl-group` là những viên con nhộng nổi độc lập (`pointer-events: auto; background: rgba(15, 23, 42, 0.92); border-radius: 999px;`) có khoảng hở giữa các cụm. Khi giáo viên bấm vào khoảng hở hoặc phía trên thanh điều khiển, slide vẫn nhận lệnh chuyển bước bình thường.
  + Đưa các công cụ thao tác nhanh lên Menu Chuột Phải (`#contextMenu`) và loại bỏ các nút trùng lặp khỏi thanh điều khiển dưới đáy (bỏ `🔴 Laser`, `✏️ Vẽ`, `📋 Bảng viết` ở đáy để thanh công cụ luôn tinh gọn, thanh thoát).
- **Bộ Công cụ Sư phạm Tương tác Cao (Pedagogical Power Tools):**
  1. **Đồng hồ đếm ngược thông minh (`#pedagogicalTimerModal` & `#timerFloatingBadge`):**
     - Đếm ngược thời gian thảo luận nhóm, làm bài tập với các mốc nhanh: 1 phút, 2 phút, 3 phút, 5 phút, 10 phút hoặc cộng/trừ 30 giây.
     - Thanh tiến trình trực quan (Progress Bar) và hiệu ứng chuyển màu cảnh báo: Xanh $\rightarrow$ Vàng cam ($\le 30s$) $\rightarrow$ Đỏ nhấp nháy khi hết giờ.
     - Âm thanh tích tắc cảnh báo 5 giây cuối và chuông hoàn thành phát qua Native Web Audio API (100% offline, không cần tệp âm thanh bên ngoài).
     - Hỗ trợ thu nhỏ thành huy hiệu nổi gọn gàng ở góc trên bên phải màn hình (`#timerFloatingBadge`) để không che khuất bài giảng trong lúc học sinh làm bài; mở lại nhanh bằng phím tắt `T` hoặc click vào huy hiệu.
  2. **Vòng quay / Hộp chọn ngẫu nhiên học sinh (`#studentPickerModal`):**
     - Phục vụ gọi học sinh lên bảng hoặc phát biểu ý kiến: hỗ trợ chọn theo số thứ tự (sĩ số lớp 1..N) hoặc theo danh sách tên lớp (lưu tự động vào `localStorage`).
     - Hiệu ứng cuộn tên ngẫu nhiên kết hợp âm thanh vui nhộn và giai điệu fanfare chúc mừng khi dừng lại. Kích hoạt tức thì bằng phím tắt `R` hoặc Menu Chuột Phải.
  3. **Thước kẻ & Thước đo độ hình học ảo (`#virtualGeometryTools`):**
     - Thước thẳng 20 cm có vạch chia milimet và thước đo độ bán nguyệt $180^\circ$ trong suốt cao cấp.
     - Giáo viên có thể kéo thả di chuyển (`draggable`) tự do trên slide, bấm các nút xoay $\pm 15^\circ$ để đo trực tiếp cạnh, góc trên các hình vẽ SVG / ảnh bài học.
  4. **Bảng viết phấn nâng cấp Đa bề mặt (`#blackboardOverlay`):**
     - Hỗ trợ chuyển đổi nhanh 4 loại bề mặt bảng chuẩn học đường: 🟢 Bảng xanh truyền thống, ⚪ Bảng trắng hiện đại, 📐 Bảng ô ly vuông (tiện vẽ đồ thị / hình học), ⬛ Bảng đá đen.
     - Hộp phấn 4 màu trực quan: Trắng, Vàng, Đỏ/Hồng, Xanh dương; xóa sạch 1 chạm và đóng nhanh bằng phím `W` hoặc `Escape`.


## 5. Bộ khung mã HTML mẫu & Nguồn sự thật Master Template

> [!IMPORTANT]
> **QUY TẮC BẢO TOÀN KHUNG SƯỜN 100% (NGUỒN SỰ THẬT DUY NHẤT):**
> Mọi bài giảng HTML tạo ra (dù trên máy bàn, laptop, hay bất kỳ môi trường nào) **BẮT BUỘC PHẢI DÙNG FILE MẪU CHUẨN:**
> `TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html`
> (hoặc đọc trực tiếp từ `TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html`).
>
> **CẤM TUYỆT ĐỐI:** Tự ý viết lại CSS/JS từ đầu hoặc sinh file HTML giản lược. Bắt buộc giữ nguyên 100% toàn bộ thẻ `<head>`, cấu hình MathJax 3, toàn bộ 1.176 dòng CSS hiện đại, thanh điều khiển nổi `#controlBar`, Modal soạn thảo `#editModal`, Modal phóng to ảnh vector Lightbox `#imageLightboxBackdrop` và toàn bộ 2.094 dòng JS tương tác / Text-to-Speech phát âm tiếng Anh.
> Trợ lý chỉ việc nhân bản từ `master_lecture_template.html`, thay thông tin tiêu đề bài học và đưa nội dung các slide trích xuất từ PDF vào đúng vùng `#slideDeck` (`<section class="slide-item ...">`).

Skeleton dưới đây chạy được ngay khi lưu thành file `.html`. Khi soạn bài thật, thay mọi chỗ `[TRÍCH TỪ PDF]` bằng nội dung đã trích, rồi nhân slide cho đủ 8–12 hoặc 16–22 slides theo số tiết. Không giữ nguyên câu placeholder trong bài thành phẩm, và không bịa số liệu ngoài PDF.

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
    * { box-sizing: border-box; }
    body { margin: 0; font-family: "Segoe UI", Arial, sans-serif; background: #0f172a; color: #0f172a; }
    .slide-deck { height: 100vh; }
    .slide-item { display: none; height: 100%; background: #fff; }
    .slide-item.active { display: flex; flex-direction: column; }
    .slide-content-grid { flex: 1; display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding: 16px; }
    .col-board, .col-task { overflow: auto; padding: 8px; }
    .content-block { background: #f8fafc; border: 2px solid #0b3a82; border-radius: 10px; padding: 12px; margin-bottom: 10px; }
    .content-block[data-step="0"] { display: block; }
    .laser-pointer { display: none; position: fixed; width: 22px; height: 22px; margin-left: -11px; margin-top: -11px; border-radius: 50%; background: radial-gradient(circle, #fff 0%, #ef4444 45%, rgba(239, 68, 68, 0.2) 70%); box-shadow: 0 0 14px 4px rgba(239, 68, 68, 0.85); z-index: 950; pointer-events: none; }
    .laser-pointer.active { display: block; }
    body.laser-mode, body.laser-mode * { cursor: none !important; }
    .draw-canvas { position: fixed; inset: 0; z-index: 900; pointer-events: none; }
    body.pen-mode .draw-canvas { cursor: crosshair; }
    body.pen-mode { overflow: hidden; }
    #blackboardOverlay { display: none; position: fixed; inset: 0; z-index: 1200; background: #14532d; }
    #blackboardOverlay.active { display: block; }
    #penPalette { display: none; position: fixed; bottom: 64px; left: 50%; transform: translateX(-50%); z-index: 1100; gap: 6px; background: #0f172a; border-radius: 999px; padding: 6px 10px; }
    #penPalette.active { display: flex; }
    .control-bar { position: fixed; bottom: 8px; left: 50%; transform: translateX(-50%); display: flex; gap: 6px; z-index: 1000; }
    .btn-ctrl { font: inherit; border: 0; border-radius: 8px; padding: 8px 12px; cursor: pointer; }
  </style>
</head>
<body class="mode-present">
<div class="slide-deck" id="slideDeck">
  <section class="slide-item active" id="s1" data-slide-index="1" data-max-steps="4">
    <div class="slide-content-grid">
      <div class="col-board">
        <div class="content-block core-board" data-step="0"><strong>[Tiêu đề mục]</strong><br>[Định lí cốt lõi trích từ PDF]</div>
        <div class="content-block" data-step="2"><strong>Quy ước</strong><br>[Ký hiệu trích từ PDF]</div>
        <div class="content-block" data-step="4"><strong>Chốt</strong><br>[Hệ thức chốt trích từ PDF]</div>
      </div>
      <div class="col-task">
        <div class="content-block" data-step="1"><strong>Đề bài</strong><br>[TRÍCH TỪ PDF] <button type="button" onclick="speakBlockAuto(this.closest('.content-block'), null, event)">🔊</button></div>
        <div class="content-block" data-step="3"><strong>Hướng dẫn</strong><br>[TRÍCH TỪ PDF]</div>
      </div>
    </div>
  </section>
</div>
<div class="laser-pointer" id="laserPointer" aria-hidden="true"></div>
<canvas class="draw-canvas" id="drawCanvas"></canvas>
<div id="penPalette" class="pen-palette">
  <button type="button" onclick="setPenColor('#ef4444', 3, false)">🔴 Bút đỏ</button>
  <button type="button" onclick="setPenColor('rgba(250, 204, 21, 0.45)', 14, true)">🟡 Dạ quang</button>
  <button type="button" onclick="clearDrawCanvas()">🗑️ Xóa nét</button>
  <button type="button" onclick="togglePenMode(false)">✕</button>
</div>
<div id="blackboardOverlay"><canvas id="blackboardCanvas"></canvas></div>
<nav class="control-bar" id="controlBar">
  <button class="btn-ctrl" onclick="jumpToPeriod(1)">Tiết 1</button>
  <button class="btn-ctrl" onclick="jumpToPeriod(2)">Tiết 2</button>
  <button class="btn-ctrl" onclick="jumpToPeriod(3)">Tiết 3</button>
  <button class="btn-ctrl" onclick="prevStep()">◀ Trước</button>
  <button class="btn-ctrl" onclick="nextStep()">▶ Sau</button>
  <button class="btn-ctrl" id="btnLaser" onclick="toggleLaserMode()">🔴 Laser</button>
  <button class="btn-ctrl" id="btnPen" onclick="togglePenMode()">✏️ Vẽ</button>
  <button class="btn-ctrl" id="btnBlackboard" onclick="toggleBlackboard()">📋 Bảng viết</button>
</nav>
<script>
  var step = 0;
  function nextStep() { step += 1; }
  function prevStep() { step = Math.max(0, step - 1); }
  var currentLang = 'vi';
  var currentSlideIndex = 1;
  var totalSlides = 26;
  function jumpToPeriod(n) { var map = { 1: 1, 2: 9, 3: 16 }; currentSlideIndex = map[n] || 1; }
  function toggleBlackboard(force) {
    var el = document.getElementById('blackboardOverlay');
    var on = typeof force === 'boolean' ? force : !el.classList.contains('active');
    el.classList.toggle('active', on);
  }
  function speakBlockAuto(blockEl) { if (currentLang === 'en') return; }
  var penDrawing = false, penColor = '#ef4444', penWidth = 3, penHighlight = false;
  function toggleLaserMode(force) {
    var on = typeof force === 'boolean' ? force : !document.body.classList.contains('laser-mode');
    if (on) togglePenMode(false);
    document.body.classList.toggle('laser-mode', on);
    var dot = document.getElementById('laserPointer');
    if (dot) dot.classList.toggle('active', on);
  }
  function togglePenMode(force) {
    var on = typeof force === 'boolean' ? force : !document.body.classList.contains('pen-mode');
    if (on) toggleLaserMode(false);
    document.body.classList.toggle('pen-mode', on);
    var canvas = document.getElementById('drawCanvas');
    var palette = document.getElementById('penPalette');
    if (canvas) canvas.style.pointerEvents = on ? 'auto' : 'none';
    if (palette) palette.classList.toggle('active', on);
  }
  function setPenColor(color, width, isHighlighter) { penColor = color; penWidth = width; penHighlight = !!isHighlighter; }
  function clearDrawCanvas() {
    var canvas = document.getElementById('drawCanvas');
    if (!canvas) return;
    canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
  }
  function bindDrawCanvas() {
    var canvas = document.getElementById('drawCanvas');
    if (!canvas) return;
    canvas.addEventListener('mousedown', function (e) {
      if (!document.body.classList.contains('pen-mode')) return;
      penDrawing = true;
      var ctx = canvas.getContext('2d');
      ctx.beginPath();
      ctx.moveTo(e.clientX, e.clientY);
    });
    canvas.addEventListener('mousemove', function (e) {
      if (!penDrawing) return;
      var ctx = canvas.getContext('2d');
      ctx.strokeStyle = penColor;
      ctx.lineWidth = penWidth;
      ctx.lineTo(e.clientX, e.clientY);
      ctx.stroke();
    });
    window.addEventListener('mouseup', function () { penDrawing = false; });
  }
  document.addEventListener('mousemove', function (e) {
    var dot = document.getElementById('laserPointer');
    if (!dot || !document.body.classList.contains('laser-mode')) return;
    dot.style.left = e.clientX + 'px';
    dot.style.top = e.clientY + 'px';
  });
  document.addEventListener('DOMContentLoaded', bindDrawCanvas);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { toggleBlackboard(false); toggleLaserMode(false); togglePenMode(false); return; }
    if (e.key === 'w' || e.key === 'W' || e.key === 'b' || e.key === 'B') { toggleBlackboard(); return; }
    if (e.key === 'l' || e.key === 'L') { e.preventDefault(); toggleLaserMode(); return; }
    if (e.key === 'p' || e.key === 'P') { e.preventDefault(); togglePenMode(); return; }
    if (e.key === 'c' || e.key === 'C') { e.preventDefault(); clearDrawCanvas(); return; }
    if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') nextStep();
    if (e.key === 'ArrowLeft' || e.key === 'PageUp') prevStep();
  });
  document.getElementById('slideDeck').addEventListener('click', function (e) {
    if (document.body.classList.contains('laser-mode')) return;
    nextStep();
  });
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

