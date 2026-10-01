# PLAN: NÂNG CẤP BÀI GIẢNG HTML TƯƠNG TÁC (BÚT TRÌNH CHIẾU, ZOOM ẢNH KHÔNG NHẢY BƯỚC, DẪN DẮT SƯ PHẠM 4 BƯỚC)

## Hiện trạng
1. **Lỗi phóng to hình ảnh bị nhảy sang hiệu ứng khác:**
   - Trong `TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html` (dòng 3416-3421), sự kiện click trên `#slideDeck` bắt mọi cú nhấp chuột và gọi `nextStep()` trừ khi nhấp vào `button, a, input, textarea, .control-bar, #editModal`. Trình lắng nghe không loại trừ thẻ `svg`, `img`, `.figure-box` hoặc các phần tử chứa hình.
   - Hàm `initImageZoomListeners()` (dòng 3686-3703) sử dụng selector hẹp `.block-body svg, .block-body img`, bỏ sót các hình vẽ nằm trực tiếp dưới `.content-block`, `.col-task`, `.figure-box`.
   - Vòng đời sự kiện: `initImageZoomListeners()` chỉ chạy một lần lúc `DOMContentLoaded`. Khi người dùng bật Song ngữ (`toggleBilingual`) hoặc sau khi biên tập/tách bước, `innerHTML` bị gán lại làm mất toàn bộ event listener đã gắn trên các phần tử ảnh/SVG. Khi nhấp vào ảnh, sự kiện nổi bọt (bubble) lên `#slideDeck` và gọi `nextStep()`, khiến bài giảng tự chuyển sang hiệu ứng/bước tiếp theo thay vì mở Lightbox Zoom.
2. **Nội dung hiệu ứng chưa dẫn dắt sư phạm từng bước (hiện đồng thời gợi ý + lời giải + đáp án + ghi bảng):**
   - Trong `PROMPT_TAO_BAI_GIANG_HTML.md` và `.agents/rules/tao-bai-giang-html.md`, quy chuẩn tại Vá 10 và Vá 19 mới chỉ quy định tách 2 bước chung (Đề bài `data-step="1"` và Lời giải `data-step="2"`).
   - Trong các bài giảng mẫu hiện tại (`Bai_12...html`, `Bai_4...html`), các khối Hướng dẫn/Gợi ý phân tích và khối Lời giải chi tiết kèm kết quả tính toán cuối cùng đều bị gán chung `data-step="2"`.
   - Khi chuyển sang bước 2, toàn bộ gợi ý, lời giải mẫu, đáp số cuối cùng và nội dung ghi bảng hiện ra cùng một lúc; học sinh thấy ngay đáp án mà không có bước gợi mở tư duy, mất tính tương tác sư phạm.
3. **Không tương thích với bút trình chiếu (Wireless Presenter Remote) & phím quay lui:**
   - Trong `master_lecture_template.html` (dòng 3404-3413), sự kiện `keydown` chỉ hỗ trợ duy nhất `ArrowRight`, ` ` (Space) cho tiến bước và `ArrowLeft` cho lùi bước.
   - Các bút trình chiếu tiêu chuẩn (Logitech, Deli, Baseus, Targus,...) phát mã phím phần cứng chuẩn quốc tế:
     + Nút Tiến (Next): phát phím `PageDown` (hoặc `ArrowRight`, `ArrowDown`, `Space`).
     + Nút Lùi (Back/Previous): phát phím `PageUp` (hoặc `ArrowLeft`, `ArrowUp`, `Backspace`).
     + Nút Màn hình đen (Blank Screen): phát phím `b` hoặc `.` (Period).
   - Do thiếu xử lý `PageDown`, `PageUp`, `ArrowDown`, `ArrowUp`, `Backspace`, các nút trên bút trình chiếu bị vô hiệu hóa hoặc làm trình duyệt cuộn trang; giáo viên không thể bấm lùi bằng phím/bút mà bắt buộc phải dùng chuột bấm nút "Lùi 1 bước" trên thanh công cụ.
   - Bẫy Focus: Sau khi click chuột vào nút "Lùi 1 bước" trên thanh điều khiển, nút đó giữ focus. Khi bấm phím `Space` tiếp theo, trình duyệt kích hoạt lại sự kiện click của nút đó thay vì tiến bước bài giảng.

## Phạm vi
1. **Khung sườn Master Template (`master_lecture_template.html`):**
   - Nâng cấp bộ lắng nghe phím điều hướng: hỗ trợ đầy đủ `PageDown`, `PageUp`, `ArrowDown`, `ArrowUp`, `ArrowRight`, `ArrowLeft`, `Space`, `Backspace`, `Enter`, phím màn hình đen `b` / `.`, ngăn chặn cuộn trang mặc định khi đang trình chiếu.
   - Khử bẫy focus: gọi `.blur()` trên các nút thanh điều khiển sau khi click.
   - Tối ưu cơ chế Lightbox Zoom:
     + Dùng Event Delegation trực tiếp trên `#slideDeck` để bắt click phóng to mọi `svg:not(mjx-container *)`, `img`, `.figure-box`, `[data-zoomable]`.
     + Loại trừ tuyệt đối các phần tử hình ảnh, SVG và Lightbox khỏi trình kích hoạt `nextStep()` trên `#slideDeck`.
     + Đảm bảo sau khi đổi ngôn ngữ (`toggleBilingual`) hoặc chỉnh sửa nội dung trong chế độ Thiết kế, tính năng phóng to hình vẽ vẫn hoạt động trơn tru.
   - Cập nhật các slide mẫu trong template theo chuẩn dẫn dắt sư phạm 4 bước độc lập.
2. **Quy chuẩn Master Prompt & Rules (`PROMPT_TAO_BAI_GIANG_HTML.md` & `.agents/rules/tao-bai-giang-html.md`):**
   - Bổ sung **Vá 23 — Dẫn dắt Sư phạm 4 bước Độc lập (4-Step Pedagogical Scaffolding)**:
     + Bước 1 (`data-step="1"`): Đề bài & Hình vẽ ban đầu. Cột ghi bảng chỉ ghi tiêu đề mục hoặc để trống.
     + Bước 2 (`data-step="2"`): Gợi ý / Dẫn dắt / Câu hỏi tư duy sư phạm định hướng (cấm hiện đáp án hay lời giải).
     + Bước 3 (`data-step="3"`): Các bước giải chi tiết / Biến đổi tương đương / Tính toán.
     + Bước 4 (`data-step="4"`): Chốt đáp số & Nội dung kiến thức cốt lõi ghi bảng cho học sinh chép vở.
   - Bổ sung **Vá 24 — Tương thích 100% Bút trình chiếu & Điều hướng Bàn phím đa năng (Universal Presenter & Key Navigation)**.
   - Cập nhật chuẩn Event Delegation cho Lightbox Zoom trong Vá 22.
3. **Các bài giảng mẫu đã xuất (`Ket_qua/Bai_12...html` và `Ket_qua/Bai_4...html`):**
   - Cập nhật các đoạn script điều hướng (bút trình chiếu), delegation zoom ảnh và chuẩn hóa thứ tự các bước dẫn dắt trên các slide bài tập/ví dụ.
4. **Bộ kiểm thử tự động (`tests/trolythien-template-smoke.js` và `tests/trolythien-bai-giang-html-smoke.js`):**
   - Thêm các kiểm tra assert cho: `PageDown`, `PageUp`, `ArrowDown`, `ArrowUp`, `Backspace`, chặn nhảy bước khi click ảnh/SVG, và cấu trúc dẫn dắt bước sư phạm.

## Ngoài phạm vi
- Không thay đổi thiết kế giao diện đồ họa tổng thể hay bảng màu đã thống nhất.
- Không sửa đổi logic toán học hoặc nội dung trích xuất từ SGK trong các file PDF gốc.
- Không can thiệp vào các nhánh trợ lý khác (1 đến 9) trong `TROLYTHIEN`.

## File dự kiến tác động
1. `TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html`
2. `TROLYTHIEN/10_BAI_GIANG_HTML/PROMPT_TAO_BAI_GIANG_HTML.md`
3. `.agents/rules/tao-bai-giang-html.md`
4. `TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html`
5. `TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html`
6. `tests/trolythien-template-smoke.js`
7. `tests/trolythien-bai-giang-html-smoke.js`

## Các bước thực hiện
1. **Bước 1: Nâng cấp Master Template (`master_lecture_template.html`)**
   - Cập nhật hàm xử lý sự kiện bàn phím:
     + Nhận diện các phím tiến: `['ArrowRight', 'ArrowDown', 'PageDown', ' ', 'Enter']` $\rightarrow$ gọi `nextStep()`.
     + Nhận diện các phím lùi: `['ArrowLeft', 'ArrowUp', 'PageUp', 'Backspace']` $\rightarrow$ gọi `prevStep()`.
     + Nhận diện phím tắt màn hình đen (`b`, `.`) $\rightarrow$ bật/tắt lớp màn hình đen `.blank-screen`.
     + Gọi `e.preventDefault()` để tránh cuộn trang hoặc nhảy form.
   - Thêm cơ chế tự động hủy focus (`this.blur()`) trên tất cả các nút bấm trong `.control-bar`.
   - Cải tiến trình bắt click trên `#slideDeck`:
     + Loại trừ click nếu `e.target.closest('button, a, input, textarea, .control-bar, #editModal, .image-lightbox-dialog, .image-lightbox-backdrop, svg, img, .figure-box, [data-zoomable]')`.
     + Thiết lập Event Delegation toàn cục cho hình ảnh: khi click vào bất kỳ `svg` (ngoại trừ công thức `mjx-container`) hoặc `img`, tự động gọi `openImageLightbox(target, title)` mà không bị ảnh hưởng bởi việc thay đổi `innerHTML` sau khi chuyển ngôn ngữ.
   - Cập nhật các slide ví dụ mẫu trong template thể hiện rõ ràng cấu trúc dẫn dắt 4 bước (`data-step="1"` đến `data-step="4"`).
2. **Bước 2: Cập nhật Master Prompt & Rules (`PROMPT_TAO_BAI_GIANG_HTML.md` & `tao-bai-giang-html.md`)**
   - Bổ sung nội dung Vá 23 (Dẫn dắt Sư phạm 4 bước Độc lập) và Vá 24 (Hỗ trợ 100% Bút trình chiếu) vào cả 2 file.
   - Nâng cấp mô tả kỹ thuật của Vá 22 (Lightbox Zoom delegation).
   - Đảm bảo các từ khóa bắt buộc của smoke test hiện diện đầy đủ.
3. **Bước 3: Đồng bộ vào các bài giảng HTML mẫu (`Bai_12...html` và `Bai_4...html`)**
   - Cập nhật script điều khiển điều hướng phím, Lightbox Zoom delegation, và chia tách thứ tự `data-step` trên các slide ví dụ/luyện tập để dẫn dắt từng bước.
4. **Bước 4: Cập nhật và chạy Smoke Tests**
   - Bổ sung assertion kiểm tra các phím bút trình chiếu và kiểm tra loại trừ click hình ảnh vào `tests/trolythien-template-smoke.js` và `tests/trolythien-bai-giang-html-smoke.js`.
   - Chạy kiểm thử tự động bằng Node.js và xác nhận PASS 100%.

## Rủi ro
- Phím `Backspace` có thể gây quay lại trang web trước đó (Back navigation) trên một số trình duyệt cũ nếu không gọi `e.preventDefault()`. $\rightarrow$ Khắc phục: luôn gọi `e.preventDefault()` khi bắt phím `Backspace` ngoài các trường nhập liệu.
- Công thức MathJax bên trong SVG hoặc thẻ `<mjx-container>` có thể bị nhận nhầm là hình ảnh cần zoom nếu selector không lọc kỹ. $\rightarrow$ Khắc phục: sử dụng bộ lọc nghiêm ngặt `:not(mjx-container *)` và kiểm tra `el.closest('mjx-container')`.
- Khi tách thành 4 bước, nếu slide có quá nhiều nội dung có thể làm tăng số lần bấm phím của giáo viên. $\rightarrow$ Khắc phục: hiển thị rõ số bước hiện tại trên thanh điều khiển (ví dụ: `Bước 2/4`) và cho phép bấm phím tắt hoặc nút "Trang sau" để nhảy nhanh sang slide tiếp theo khi cần.

## Cách kiểm thử
1. **Kiểm tra tính năng Bút trình chiếu & Phím tắt:**
   - Giả lập sự kiện `keydown` với các phím: `PageDown`, `PageUp`, `ArrowDown`, `ArrowUp`, `Backspace`, `Space`, `ArrowRight`, `ArrowLeft`.
   - Xác nhận `nextStep()` và `prevStep()` được kích hoạt chính xác, không phát sinh lỗi cuộn trang.
2. **Kiểm tra Phóng to hình ảnh không bị nhảy bước:**
   - Kích hoạt sự kiện click vào các thẻ `<svg>`, `<img>` (kể cả trước và sau khi gọi `toggleBilingual()`).
   - Xác nhận Lightbox mở lên với class `active`, hình ảnh hiển thị rõ nét, và `currentStep` của slide KHÔNG bị tăng lên.
3. **Kiểm tra Dẫn dắt 4 bước sư phạm:**
   - Kiểm tra cấu trúc DOM của slide bài tập/ví dụ:
     + Bước 1: chỉ hiển thị Đề bài + Hình vẽ ban đầu.
     + Bước 2: hiển thị thêm phần Gợi ý / Dẫn dắt, Lời giải và Đáp án vẫn ẩn (`display: none` hoặc `opacity: 0`).
     + Bước 3: hiển thị Các bước giải chi tiết.
     + Bước 4: hiển thị Đáp số chốt và Nội dung ghi bảng.
4. **Chạy smoke test của hệ thống:**
   - `node tests/trolythien-template-smoke.js`
   - `node tests/trolythien-bai-giang-html-smoke.js`

## Tiêu chí nghiệm thu
1. Cắm bút trình chiếu (hoặc bấm `PageDown` / `PageUp` / `ArrowDown` / `ArrowUp` / `Backspace` / `Space`): Tiến/Lùi bài giảng mượt mà 100%, không bị kẹt ở nút lùi.
2. Nhấp chuột vào bất kỳ hình vẽ SVG hoặc ảnh minh họa nào: Phóng to Lightbox hiển thị ngay lập tức, không làm slide chuyển sang hiệu ứng hoặc bước tiếp theo.
3. Các hoạt động giải bài tập và ví dụ được dẫn dắt tuần tự qua 4 bước sư phạm rõ ràng: Đề bài $\rightarrow$ Gợi ý/Dẫn dắt $\rightarrow$ Lời giải chi tiết $\rightarrow$ Đáp án chốt & Ghi bảng.
4. Toàn bộ smoke test liên quan trong `tests/` chạy thành công (PASS).
