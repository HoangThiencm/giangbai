# MASTER PROMPT & QUY CHUẨN SOẠN BÀI DẠY HTML (DẠY THÊM, PHỤ ĐẠO, BỒI DƯỠNG)
**Trợ lý Sư phạm Hoàng Thiên • Nhánh 3: Tạo bài tập • Chức năng 9**

> ⚠️ **BẮT BUỘC ĐỌC KỸ TRƯỚC KHI THỰC HIỆN:**  
> Tài liệu này là kim chỉ nam tối thượng cho AI khi soạn bài dạy HTML tại `TROLYTHIEN/2_TAO_BAI_TAP/`. Bất kỳ AI nào (kể cả trên máy mới, phiên chat mới) bắt buộc phải tuân thủ 100% quy trình kỹ thuật và tôn chỉ sư phạm dưới đây, **tuyệt đối không làm sai lệch hay tự ý cắt bớt bước**.

---

## PHẦN 1: TÔN CHỈ SƯ PHẠM CỐT TỬ (BẮT BUỘC PHẢI THẤM NHUẦN)

### 1.1. Mục Tiêu Tối Thượng: Rèn Luyện Kỹ Năng Thực Chiến Cho Học Sinh THCS
* **Đóng vai Chuyên gia Sư phạm THCS thực chiến:** Mục tiêu số 1 là tạo ra hệ thống bài tập gom nhóm để **rèn cho học sinh kỹ năng giải toán thông qua rèn luyện lặp lại**, giúp các em tự tin làm chủ kiến thức, sau đó mới mở rộng và phát triển tư duy.
* **Không ôm đồm bồi dưỡng học sinh giỏi cao siêu hay Olympic!**
* **Ma trận phân bổ chuẩn mực 80% — 20%:**
  1. **80% DÀNH CHO HỌC SINH TRUNG BÌNH — KHÁ:**
     - **~40% Mức 1 (Thông hiểu — Rèn kỹ thuật giải):** Các bài tập nhận diện công thức, áp dụng trực diện, rèn kỹ thuật tính toán nền tảng.
     - **~40% Mức 2 (Vận dụng vừa sức & Thực tế đời sống):** Các bài toán biến thể nhẹ, ghép nối các bước giải, hoặc bài toán mô hình hóa thực tế quen thuộc trong SGK (đo bóng cây, bóng tháp, thang dựa tường, độ dốc...).
  2. **20% MỞ RỘNG CHO KHÁ — GIỎI THEO TỪNG DẠNG TOÁN:**
     - Các bài toán nâng cao vừa sức thi vào lớp 10 (mức điểm 8.5 – 9.0), phân tích đa giác hoặc kẻ đường phụ.
     - **Tuyệt đối cấm** bài toán cực trị cao siêu, bất đẳng thức Olympic vượt tầm học sinh THCS.

### 1.2. Giới Hạn Vùng Kiến Thức Cấp Học (Curriculum Scope Constraint)
1. **100% Kiến thức Cấp 2 (THCS):**
   - ❌ **CẤM TUYỆT ĐỐI:** Định lý Sin, Định lý Côsin (đây là kiến thức Toán 10 THPT).
   - ❌ **CẤM TUYỆT ĐỐI:** Công thức cộng lượng giác $\tan(a \pm b), \sin(a \pm b)$ (Toán 11 THPT).
   - ❌ **CẤM TUYỆT ĐỐI:** Góc lượng giác tù $> 90^\circ$ (Toán 9 THCS chỉ học góc nhọn $0^\circ < \alpha < 90^\circ$. Nếu gặp tam giác tù, bắt buộc kẻ đường cao ngoài để đưa về tam giác vuông và dùng góc kề bù nhọn).
2. **Không lấy kiến thức lớp trên cho bài lớp dưới:**
   - Không lấy kiến thức lớp 9 dạy cho bài lớp 6, 7, 8.
3. **CẤM TUYỆT ĐỐI ký hiệu tương đương $\iff$ ở cấp THCS:**
   - Trình bày toán học tự nhiên chuẩn SGK: dùng các từ `"nên"`, `"hay"`, `"suy ra"`, `"hoặc"`, `"do đó"`.
4. **Bao quát đầy đủ các chuyên đề trọng tâm của bài học:**
   - Ví dụ Bài 12 Toán 9: **Bắt buộc phải có cụm bài tập chuyên sâu về "GIẢI TAM GIÁC VUÔNG"** rèn cả 2 trường hợp:
     + Trường hợp 1: Biết 1 cạnh và 1 góc nhọn.
     + Trường hợp 2: Biết 2 cạnh.

### 1.3. HỆ THỐNG 8 BẢN VÁ SƯ PHẠM THỰC CHIẾN (CHUẨN TÔN THÂN — VŨ HỮU BÌNH) — CHỐNG SOẠN TẦM BẬY
> ⚠️ **BẢN VÁ KỶ LUẬT THỰC CHIẾN:** AI tuyệt đối không được nói lý thuyết suông rồi khi soạn thì "toàn tầm bậy" (bịa số lẻ, nghiệm căn quái dị, nhảy bước, sai kiến thức). Bắt buộc tuân thủ 8 bản vá:
1. **Vá 1 (Thiết kế số liệu mẫu mực):** Nghiệm phương trình/hệ phương trình phải là số nguyên hoặc phân số tối giản đẹp. Tam giác vuông phải dùng bộ ba Pythagore nguyên $(3,4,5), (5,12,13)...$ hoặc góc đặc biệt ($30^\circ, 45^\circ, 60^\circ$). Cấm tam giác vi phạm bất đẳng thức tam giác. Biểu thức rút gọn phải tinh gọn, trong sáng.
2. **Vá 2 (Cụm bài tập rèn luyện tương tự):** Cấm nhảy cóc lộn xộn. Mỗi dạng toán bắt buộc gồm cụm 3–4 bài: *Bài mẫu kinh điển $\rightarrow$ Bài tương tự 1 (luyện tay đổi số) $\rightarrow$ Bài biến thể 2 (gài bẫy nhẹ / đổi chiều tư duy) $\rightarrow$ Bài mở rộng / thực tế 3*.
3. **Vá 3 (Phân tích đi lên Thầy Vũ Hữu Bình):** Khối `🧭 Phân tích tìm hướng giải` bắt buộc dùng sơ đồ phân tích đi lên ($A \Leftarrow B \Leftarrow C$). Chỉ rõ mấu chốt tại sao nghĩ ra cách vẽ đường phụ hoặc biến đổi trung gian.
4. **Vá 4 (Kỷ luật trình bày tự luận THCS):** Cấm 100% ký hiệu $\iff, <=>, \Leftrightarrow$. Dùng từ nối tự nhiên chuẩn SGK: `"Điều kiện xác định"`, `"Ta có"`, `"suy ra"`, `"nên"`, `"hay"`, `"do đó"`, `"Vậy..."`. Không nhảy bước biến đổi.
5. **Vá 5 (Khóa chặt cấp học):** 100% kiến thức THCS. Cấm tuyệt đối định lý Sin, Cosin, công thức cộng lượng giác, góc tù $> 90^\circ$, bất đẳng thức Olympic/Cauchy nhiều biến. Không lấy kiến thức lớp trên dạy lớp dưới.
6. **Vá 6 (Vẽ hình SVG chính xác 1:1):** Tính tọa độ giải tích Oxy chính xác 100%, góc vuông thật, tam giác chuẩn tỉ lệ, lề an toàn $\ge 40\text{px}$, không đè nhãn chữ, không lộ đáp án trên hình (để dấu `?`).
7. **Vá 7 (Cảnh báo cạm bẫy sát sườn):** Khối `⚠️ Cạm bẫy` phải chỉ ra đúng lỗi học sinh hay bị trừ điểm khi đi thi (quên ĐKXĐ, quên thử lại, chia 2 vế cho 0 làm mất nghiệm, nhầm $\sin/\cos$, bấm máy Casio nhầm Rad/Deg).
8. **Vá 8 (Cơ chế phân tầng Kép: Chiếu & In A4):** Slide trực quan cho GV đứng lớp; Chế độ in A4 (`Ctrl + P`) tự động ẩn lời giải/cạm bẫy để xuất thành phiếu bài tập rèn luyện chuẩn mực có rubric tự đánh giá.
9. **Vá 9 (Kỹ thuật số tự nhiên có gạch trên đầu & Chuẩn hóa công thức Word Equation):**
   - Số tự nhiên có các chữ số gạch trên đầu ($\overline{ab}, \overline{abc}, \overline{3*5}, \overline{17*}, \overline{2x3y}$...):
     + Trong Word: BẮT BUỘC dùng cấu trúc Overbar `<m:bar><m:barPr><m:pos m:val="top"/></m:barPr><m:e>...</m:e></m:bar>`. TUYỆT ĐỐI CẤM dùng accent `<m:acc>` (vì dấu mũ accent làm gãy nét, biến thành ký tự rác hoặc dấu móc chéo đè lên chữ số).
     + Trong HTML/Web: Bắt buộc dùng `\overline{...}` trong MathJax/KaTeX hoặc CSS `<span style="text-decoration: overline;">...</span>`.
   - 100% công thức toán học trong Word phải là Native Word Equation (`m:oMath`), tuyệt đối không để lọt chuỗi LaTeX thô (`\text{ƯCLN}`, `\frac...`) làm hỏng giao diện.
   - Tập trung tối đa bài tập rèn luyện kỹ năng thực chiến (drill & practice): Đặc biệt rèn kỹ năng cho học sinh yếu, trung bình lặp lại quen tay; lược bỏ lý thuyết rườm rà; cập nhật năm học 2026 - 2027 và bỏ cấp Phòng GD&ĐT.

---

## PHẦN 2: QUY TRÌNH THỰC THI 3 BƯỚC (BẮT BUỘC DÙNG PYTHON BUILD SCRIPT)

> 🚨 **CẢNH BÁO NGUY HIỂM — CẤM VIẾT TRỰC TIẾP FILE HTML 400KB:**  
> File bài dạy HTML hoàn chỉnh có dung lượng **~400 KB** (hơn 15.000 dòng). Giới hạn token của AI không thể ghi hết file HTML trong một lệnh, dẫn đến file bị cắt cụt giữa chừng và hỏng toàn bộ.  
> **QUY TRÌNH BẮT BUỘC:** AI phải viết script Python để biên dịch dữ liệu và ghép vào `master_bai_day_html_template.html`.

```
[File PDF SGK trong Dau_vao/]
         │
         ▼
[BƯỚC 1: Đọc PDF & Phân tích cấu trúc bài học]
         │
         ▼
[BƯỚC 2: Viết script build_[ten_bai]_html.py ghép vào Master Template]
         │
         ▼
[BƯỚC 3: Chạy script sinh file ra Ket_qua/ & Chạy verify kiểm định]
```

### Bước 1: Đọc PDF SGK đầu vào
* Đọc file PDF trong `TROLYTHIEN/2_TAO_BAI_TAP/Dau_vao/` (dùng thư viện `fitz`/PyMuPDF hoặc `pdfplumber` trong Python).
* Trích xuất: Định nghĩa, Định lí, Ví dụ mẫu, Bài tập SGK, hình vẽ minh họa, và số liệu thực tế.

### Bước 2: Viết Script Python Builder `build_[ten_bai]_html.py`
AI tạo một script Python đặt ngay tại `TROLYTHIEN/2_TAO_BAI_TAP/build_[ten_bai]_html.py` với cấu trúc chuẩn:
1. Đọc template gốc: `TROLYTHIEN/2_TAO_BAI_TAP/templates/master_bai_day_html_template.html`.
2. Khai báo danh sách `data = [...]` gồm đủ **20 slide** (4 Slide Lý thuyết + 16 Slide Bài tập phân tầng).
3. Mỗi bài tập gồm: `debai`, `svg_code` (nếu có hình), `analysis` (Hướng giải), `solution` (Lời giải), `pitfall` (Cạm bẫy), `extension` (Khai thác).
4. Thay thế chính xác **7 placeholder** vào template:
   - `{{TEN_BAI_HOC}}`: Tên bài học chính.
   - `{{TEN_CHUYEN_DE}}`: Tiêu đề chuyên đề rèn luyện.
   - `__TOTAL_SLIDES__`: Tổng số slide (ví dụ `20`).
   - `__JUMP_OPTIONS__`: Các `<option value="1">...</option>` cho danh mục nhảy slide.
   - `__SLIDES_HTML__`: HTML ghép từ 20 slide.
   - `__PRINT_HTML__`: Nội dung phiếu in A4 (Phần I, II, III gom nhóm, Phần IV Rubric).
   - `__ORIGINAL_SVGS_JSON__`: JSON map chứa mã SVG gốc theo ID bài tập: `json.dumps(original_svgs_map)`.
5. Ghi file kết quả ra: `TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua/[Ten_Bai_Hoc].html`.

### Bước 3: Chạy script và kiểm tra kết quả
* Chạy `python TROLYTHIEN/2_TAO_BAI_TAP/build_[ten_bai]_html.py`.
* Chạy script verify kiểm tra: 20 slide, không sót placeholder, không có dấu $\iff$, không có kiến thức cấp 3, đầy đủ ID cho hình vẽ.

---

## PHẦN 3: QUY CHUẨN CẤU TRÚC SLIDE VÀ HÌNH VẼ SVG

### 3.1. Cấu Trúc Khung Hình Vẽ SVG (Bắt Buộc Đầy Đủ Để Zoom, Resize & Kéo Thả)
Mọi slide bài tập hình học bắt buộc phải sử dụng đúng cấu trúc DOM sau để các tính năng kéo dãn chuột (resize), phóng to (zoom), tách nổi (float) và đổi vị trí hoạt động hoàn hảo:

```html
<div class="diagram-panel" id="diagramPanel_{pid}">
  <div class="diagram-dock-header">
    <span class="dock-header-title">📐 HÌNH MINH HỌA 1:1</span>
    <div class="dock-header-btns">
      <button type="button" class="btn-dock-ctrl btn-pos-toggle" id="btnPos_{pid}" onclick="toggleDiagramUnderProblem('{pid}')" title="Chuyển hình vẽ xuống phía dưới đề bài">⬇️ Dưới đề</button>
      <button type="button" class="btn-dock-ctrl btn-float-toggle" id="btnFloat_{pid}" onclick="toggleFloatDiagram('{pid}')" title="Tách hình nổi, kéo thả tự do khắp màn hình">🆓 Tách nổi</button>
      <button type="button" class="btn-dock-ctrl" onclick="zoomSlideDiagram('{pid}', 0.2)" title="Phóng to hình vẽ">➕</button>
      <button type="button" class="btn-dock-ctrl" onclick="zoomSlideDiagram('{pid}', -0.2)" title="Thu nhỏ hình vẽ">➖</button>
      <button type="button" class="btn-dock-ctrl" onclick="resetSlideDiagram('{pid}')" title="Đặt lại kích thước và vị trí">↺</button>
      <button type="button" class="btn-dock-ctrl" onclick="zoomActiveSlideDiagram('{pid}')" title="Phóng to toàn màn hình (Lightbox)">🔍</button>
    </div>
  </div>
  <div class="diagram-wrapper" id="diagramWrapper_{pid}">
    <div class="diagram-scalable" id="diagramScale_{pid}">
      {svg_code}
    </div>
  </div>
  <div class="image-actions-bar">
    <input type="file" id="fileInput_{pid}" accept="image/*" style="display:none;" onchange="handleImageUpload(event, '{pid}')">
    <button type="button" class="img-btn-upload" onclick="document.getElementById('fileInput_{pid}').click()" title="Thay bằng ảnh chụp hoặc hình vẽ tự vẽ">📷 Chèn ảnh bài {pid}</button>
    <button type="button" class="img-btn-remove" id="btnRemoveImg_{pid}" onclick="removeCustomImage('{pid}')" style="display:none;" title="Xóa ảnh ngoài, dùng lại hình gốc">🗑️ Hình gốc</button>
    <button type="button" class="img-btn-zoom" onclick="zoomActiveSlideDiagram('{pid}')" title="Phóng to chi tiết">🔍 Phóng to</button>
  </div>
</div>
```

* **Yêu cầu đối với SVG:**
  - `viewBox="0 0 480 260"` (hoặc tỷ lệ tương đương), padding an toàn $\ge 35\text{px}$ để đỉnh không bị cắt chữ.
  - **Tuyệt đối không lộ đáp án:** Yếu tố chưa biết để dấu `?` hoặc để trống theo đúng SGK.

### 3.2. Cấu Trúc Khối Nội Dung (Content Panel)
Cột nội dung phải có đủ 4 khối sư phạm:
1. `problem-box`: Đề bài ngắn gọn, rõ ràng, công thức kẹp `$..$`.
2. `analysis-box`: Khối **🧭 PHÂN TÍCH TÌM HƯỚNG GIẢI** (nhận diện dấu hiệu, chọn công thức).
3. `solution-box`: Khối **💡 LỜI GIẢI MẪU MỰC** (trình bày trực diện, từng bước chuẩn mực).
4. `pitfall-box` & `extension-box`: Cảnh báo cạm bẫy và khai thác mở rộng thi vào lớp 10.

---

## PHẦN 4: FILE MẪU CHUẨN THAM CHIẾU (GOLDEN REFERENCE)

Mọi AI khi làm việc tại bất kỳ máy nào hãy mở và tham khảo trực tiếp file mẫu đã kiểm định thành công:
* **Script mẫu hoàn chỉnh:** `TROLYTHIEN/2_TAO_BAI_TAP/build_bai_12_toan9_html.py`
* **File template gốc:** `TROLYTHIEN/2_TAO_BAI_TAP/templates/master_bai_day_html_template.html`
* **File kiểm định mẫu:** `TROLYTHIEN/2_TAO_BAI_TAP/verify_bai_12.py`

---

## PHẦN 5: BẢN VÁ LỖI CÔNG THỨC TOÁN & CƠ CHẾ KIỂM DUYỆT SÂU (DEEP AUDITING)

1. **Khắc phục lỗi hiển thị text thô `\mathrm{UCLN}`:** Ký hiệu toán học tiếng Việt trong Word Equation phải dùng `\text{ƯCLN}` hoặc `\text{BCNN}`. TUYỆT ĐỐI CẤM tự động thay thế thành `\mathrm{UCLN}` vì XSLT của Word sẽ ngộ nhận và in nguyên văn chuỗi `\mathrm{UCLN}` ra trang in.
2. **Cơ chế Kiểm duyệt sâu (Deep XML Math Auditing):** Tuyệt đối KHÔNG kiểm tra hời hợt bằng `p.text` (vì python-docx bỏ qua text trong `<m:oMath>`). Phải quét sâu vào từng thẻ `<m:t>` trong `<m:oMath>` và `<w:t>` để phát hiện và triệt tiêu 100% tàn dư LaTeX thô.
3. **Triệt tiêu ô vuông rỗng (`<m:e/>`):** Bọc số âm trong ngoặc `({-2}; 1)` và bọc lũy thừa biểu thức trong ngoặc `-{(A+B)}^2` để tránh mồ côi dấu mở ngoặc.
4. **Tiêu đề đáp án:** Bắt buộc dùng `add_answer_header` (`Đáp số & Hướng dẫn Đề số X`), cấm để phát sinh chữ `Bài Đáp số Đề X.`.
