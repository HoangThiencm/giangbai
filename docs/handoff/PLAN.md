# PLAN

## Hiện trạng

1. **Đứt gãy liên kết đề mục giữa các trang do xử lý đơn lẻ (`CANVAS_TEXTBOOK_BATCH_SIZE = 1`)**:
   - Trong `js/khbd-app.js` (dòng 6710), `CANVAS_TEXTBOOK_BATCH_SIZE` được gán cứng bằng `1` (mỗi trang ảnh/PDF gửi thành 1 request API riêng).
   - Khi bài học kéo dài từ 2 trang trở lên (như Toán 6 Bài 5 dài 3 trang từ 17–19):
     - Trang 17 chỉ chứa phần đầu của `1. PHÉP NHÂN SỐ TỰ NHIÊN`.
     - Trang 18 chứa phần tiếp theo của Mục 1 (`Tính chất của phép nhân`, HĐ1, HĐ2, HĐ3, tính chất giao hoán, kết hợp, phân phối, Ví dụ 2, Luyện tập 2, Vận dụng 2) và nửa dưới mới bắt đầu `2. PHÉP CHIA HẾT VÀ PHÉP CHIA CÓ DƯ`.
     - Do trang 18 được phân tích độc lập mà không biết ngữ cảnh trang 17, phần đầu trang 18 bị coi là nội dung mồ côi (không có số to cấp 1 đứng trước).
2. **Lỗi thuật toán gộp đề mục (`mergeCanvasTextbookSections` dòng 6748–6758)**:
   - Thuật toán duyệt danh sách section: nếu gặp mục nhỏ không có số cấp 1 (như `Tính chất của phép nhân`), nó đưa vào mảng `pending`.
   - Khi gặp mục cấp 1 tiếp theo (`2. PHÉP CHIA HẾT VÀ PHÉP CHIA CÓ DƯ`), thuật toán chạy:
     `pending.splice(0).forEach(item => absorbCanvasTextbookSection(next, item));`
   - Dẫn đến việc **nuốt trọn toàn bộ tính chất phép nhân của Mục 1 vào Mục 2**. Hậu quả: Mục 1 bị rỗng kiến thức cốt lõi, Mục 2 bị lẫn lộn kiến thức của cả phép nhân lẫn phép chia, các hoạt động HĐ4, HĐ5 bị đảo lộn đứng trước HĐ1, HĐ2, HĐ3.
3. **Thách thức bài học dài và nguy cơ chặn bản quyền (Recitation) đối với mọi môn học**:
   - Với các bài học dài nhiều trang (đặc biệt môn Ngữ văn có thể lên tới 20–25 trang gồm Tri thức ngữ văn, văn bản đọc chính, thực hành tiếng Việt, viết đoạn văn): nếu bắt AI sao chép nguyên văn tác phẩm văn học thì Gemini kích hoạt bộ lọc bản quyền `RECITATION` và từ chối xử lý.
   - Cần một cấu trúc trích xuất chuẩn mực: **Bản đồ bài học sư phạm (Pedagogical Lesson Map)** cho MỌI MÔN HỌC (Toán, Ngữ văn, KHTN, Lịch sử - Địa lí, Tin học...), tập trung vào khung đề mục, khái niệm, tính chất, hệ thống hoạt động và bài tập, không sao chép tác phẩm văn xuôi dài để triệt tiêu nguy cơ vi phạm bản quyền.

---

## Phạm vi

1. **Cơ chế gom trang thông minh (Smart Dynamic Batching)**:
   - Nâng cấp `prepareCanvasTextbookAnalysisBatches` trong `js/khbd-app.js`:
     - Với các bài học thông thường ($\le 6$ trang ảnh hoặc toàn bộ bài học ngắn): Gom toàn bộ các trang vào **1 lượt phân tích duy nhất** (Multi-image prompt). Gemini 2.5 Flash có context window 1 triệu token, xử lý trọn vẹn 3–6 trang trong một lượt giúp nhận thức toàn cảnh bài học liên tục, xóa bỏ hoàn toàn hiện tượng cắt đứt giữa các trang.
     - Với các bài học dài (từ 7 đến 25 trang, ví dụ môn Ngữ văn): Gom theo cụm 6 trang/lượt có kèm cơ chế truyền nối ngữ cảnh (stitching) giữa các batch.
2. **Sửa thuật toán ghép nối đề mục (`mergeCanvasTextbookSections` & `absorbCanvasTextbookSection`)**:
   - Bỏ cơ chế nuốt `pending` vào `next` section.
   - Nếu có nội dung mở đầu trang không mang chỉ số cấp 1, nội dung đó phải được tự động ghép nối vào mục lớn cuối cùng của trang/lượt trước đó.
   - Hỗ trợ gộp các section có cùng tên hoặc cùng chỉ số đề mục trên nhiều trang khác nhau thành một mục duy nhất.
3. **Nâng cấp Prompt phân tích SGK đa môn học (`canvasTextbookAnalysisPrompt`)**:
   - Thiết lập chỉ dẫn chuyên môn: *"Trích xuất Bản đồ bài học (Pedagogical Lesson Map) phục vụ thiết kế kế hoạch bài dạy, tuyệt đối không chép nguyên trang văn bản"*.
   - Quy định rõ ràng theo từng phân môn:
     - **Toán & KHTN**: Trích xuất đầy đủ công thức toán học/khoa học dạng LaTeX `$ ... $`, định nghĩa, tính chất, định lý, hoạt động khám phá (HĐ), ví dụ mẫu, luyện tập và vận dụng.
     - **Ngữ văn**: Trích xuất hộp Tri thức ngữ văn, thể loại, hệ thống câu hỏi đọc hiểu (trước khi đọc, trong khi đọc, sau khi đọc), thực hành tiếng Việt, nhiệm vụ viết kết nối với đọc; **tuyệt đối không chép lại nguyên văn toàn văn bản/tác phẩm truyện, thơ dài** để ngăn ngừa bộ lọc bản quyền Recitation.
     - **Các môn khác (Lịch sử - Địa lí, GDCD, Tin học, Công nghệ...)**: Trích xuất cấu trúc đề mục, các câu hỏi khai thác tư liệu/hình ảnh/bản đồ, bài tập luyện tập và vận dụng.
4. **Đồng bộ hiển thị ngữ cảnh (`formatCanvasTextbookContext`)**:
   - Hiển thị đầy đủ cây kiến thức: Từng Đề mục lớn $\to$ Các mục con / Kiến thức cốt lõi $\to$ Toàn bộ danh sách HĐ, Luyện tập, Vận dụng, Bài tập được phân bổ đúng mục, không sót và không bị đảo lộn.

---

## Ngoài phạm vi

- Không can thiệp vào mô hình ngôn ngữ lớn hoặc logic sinh kế hoạch bài dạy ở Tab 2 và Tab 3 sau khi ngữ cảnh đã được tạo.
- Không thay đổi giao diện chung của trang `canvas_soankhbd.html`.

---

## File dự kiến tác động

- `js/khbd-app.js` (Điều chỉnh batching, prompt phân tích học liệu đa môn, thuật toán gộp đề mục đa trang).
- `canvas_soankhbd.html` & `backupcode viettailieu/canvas_soankhbd.html` (Đồng bộ nếu có logic inline liên quan).
- `tests/canvas-textbook-analysis-smoke.js` (Bổ sung test kiểm tra tính toàn vẹn đề mục đa trang và đa môn).

---

## Các bước thực hiện

1. **Cập nhật kích thước gom batch trong `js/khbd-app.js`**:
   - Cải tiến `prepareCanvasTextbookAnalysisBatches`: với danh sách trang hoặc ảnh $\le 6$, đưa tất cả vào cùng 1 batch để phân tích đa ảnh liền mạch. Với danh sách $> 6$ trang (như Ngữ văn 15–25 trang), chia thành các batch 6 trang kèm nhãn định danh trang.
2. **Sửa đổi thuật toán gộp section trong `js/khbd-app.js`**:
   - Trong `mergeCanvasTextbookSections`, xóa bỏ dòng lệnh `pending.splice(0).forEach(...)` nuốt nội dung vào `next`.
   - Xây dựng hàm ghép nối liên trang: gộp các mục cùng tên xuất hiện ở nhiều batch, đưa nội dung đầu trang vào mục cuối cùng của batch trước.
3. **Cải tiến `canvasTextbookAnalysisPrompt`**:
   - Thêm hướng dẫn chuyên biệt cho từng môn học (Toán, Văn, KHTN...).
   - Quy định rõ ràng việc trích xuất cấu trúc phân cấp: Đề mục lớn $\to$ Tiểu mục $\to$ Hoạt động/Câu hỏi/Bài tập.
   - Thêm quy tắc chống vi phạm bản quyền Recitation đối với văn bản đọc hiểu môn Ngữ văn.
4. **Cập nhật `formatCanvasTextbookContext`**:
   - Đảm bảo định dạng đầu ra hiển thị chuẩn xác từng đề mục lớn, kèm đầy đủ các tính chất, ví dụ, bài tập theo đúng thứ tự logic sư phạm.
5. **Kiểm thử**:
   - Chạy các smoke test kiểm tra phân tích cấu trúc SGK.
   - Kiểm tra mô phỏng với dữ liệu Toán 6 Bài 5 (đảm bảo Tính chất phép nhân nằm trọn trong Mục 1, Mục 2 chỉ có Phép chia).
6. **Ghi nhận `docs/handoff/IMPLEMENT.md`** và bàn giao cho `/verify`.

---

## Rủi ro & Cách phòng tránh

- **Rủi ro dung lượng mạng khi gửi nhiều ảnh cùng lúc**:
  - *Cách phòng tránh*: Hàm `compressDataUrl` trong code đã tự động tối ưu hóa và nén ảnh về kích thước an toàn trước khi gửi media part, bảo đảm tổng dung lượng gói tin dưới 2MB.
- **Rủi ro timeout khi phân tích bài dài 20–25 trang**:
  - *Cách phòng tránh*: Giữ timeout an toàn `timeoutMs: 120000` (2 phút) và cập nhật thanh tiến trình theo từng batch 6 trang.
- **Rủi ro dính Recitation khi gặp tác phẩm văn học**:
  - *Cách phòng tránh*: Prompt nghiêm cấm chép toàn văn tác phẩm, chỉ trích xuất thông tin xuất xứ, thể loại và hệ thống câu hỏi đọc hiểu.

---

## Cách kiểm thử

1. **Kiểm thử logic ghép mục liên trang**:
   - Nạp 3 trang ảnh Toán 6 Bài 5:
     - Kiểm tra kết quả trích xuất: `1. PHÉP NHÂN SỐ TỰ NHIÊN` phải chứa đầy đủ: Nhân hai số tự nhiên, Tính chất phép nhân, HĐ1, HĐ2, HĐ3, Ví dụ 1, Ví dụ 2, Luyện tập 1, Luyện tập 2, Vận dụng 1, Vận dụng 2.
     - `2. PHÉP CHIA HẾT VÀ PHÉP CHIA CÓ DƯ` chỉ chứa: Chia hai số tự nhiên, HĐ4, HĐ5, Ví dụ 3, Ví dụ 4, Luyện tập 3, Vận dụng 3.
     - Phần Bài tập cuối bài: Đầy đủ từ 1.23 đến 1.30.
2. **Kiểm thử đa môn (Ngữ văn, KHTN...)**:
   - Kiểm tra prompt hỗ trợ nhận diện các trường đặc thù của Ngữ văn (Tri thức ngữ văn, Trước khi đọc, Trong khi đọc, Sau khi đọc, Viết kết nối với đọc) mà không bị lỗi bản quyền.
3. **Kiểm thử smoke test**:
   - Chạy `tests/canvas-textbook-analysis-smoke.js` và `scratch/verify_all.py` bảo đảm toàn bộ bài kiểm tra đạt PASS 100%.

---

## Tiêu chí nghiệm thu

1. Không còn hiện tượng mục 1 bị cắt cụt kiến thức và gộp nhầm tính chất/hoạt động vào mục 2.
2. Hỗ trợ nhận diện chuẩn xác cho MỌI MÔN HỌC (Toán, Văn, KHTN, Lịch sử - Địa lí...) và các khối lớp 6–9.
3. Xử lý trơn tru bài học nhiều trang (lên tới 25 trang) mà không bị lỗi bản quyền Recitation và không bị timeout.
4. Trình tự sư phạm của các hoạt động (HĐ, Luyện tập, Vận dụng, Bài tập) hoàn toàn ăn khớp 100% với nguyên bản SGK.

