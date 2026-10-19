# PLAN: Triển khai Mục 14 — Nhận diện văn bản & Chữ viết tay (OCR Thông minh)

## Hiện trạng
- Hệ thống Trợ lý Sư phạm Hoàng Thiên (`TROLYTHIEN`) hiện có 13 nhánh chức năng (1..13), được điều hướng qua `tro-ly-thien-menu.html` và `.agents/workflows/thien.md`.
- Dự án đã tích hợp sẵn các công cụ nền tảng:
  + `pymupdf` (`fitz` v1.26+) để bóc tách cấu trúc tài liệu PDF (text blocks, bounding boxes, vector drawings, tables, images).
  + `python-docx` để dựng tài liệu Word `.docx`.
  + Module `latex_to_omml` trong `TROLYTHIEN/engine/de_cuong_docx_helper.py` để biên dịch công thức LaTeX sang thẻ XML `m:oMath` (Word Equation gốc).
  + Engine `TROLYTHIEN/engine/ve_hinh_engine.py` để dựng hình học giải tích chuẩn xác qua Oxy.
- Chưa có nhánh **Mục 14: Nhận diện văn bản (OCR Thông minh)** để xử lý bài toán chuyển đổi PDF/ảnh chụp/chữ viết tay sang Word Equation với cơ chế nhận diện lai (Hybrid Pipeline), kiểm soát kép công thức, đánh dấu đỏ có mã truy vết `NDxx` và bảng đối soát an toàn dữ liệu.

## Phạm vi
1. Khởi tạo cấu trúc thư mục chức năng:
   - `TROLYTHIEN/14_NHAN_DIEN_VAN_BAN/Dau_vao/`: Nhận tệp PDF, ảnh scan, ảnh chụp viết tay (`.pdf`, `.png`, `.jpg`, `.jpeg`).
   - `TROLYTHIEN/14_NHAN_DIEN_VAN_BAN/Ket_qua/`: Nơi xuất file Word `.docx` chuẩn A4.
   - `TROLYTHIEN/14_NHAN_DIEN_VAN_BAN/HUONG_DAN_NHAN_DIEN_VAN_BAN.md`: Hướng dẫn quy chuẩn đầu vào, cách đặt tên file và nguyên tắc xử lý.
   - `TROLYTHIEN/14_NHAN_DIEN_VAN_BAN/PROMPT_NHAN_DIEN_VAN_BAN.md`: Master Prompt quy định thuật toán nhận diện, nguyên tắc bảo toàn, định dạng cảnh báo đỏ.
2. Xây dựng engine xử lý duy nhất `TROLYTHIEN/engine/nhan_dien_engine.py`:
   - **Quy chuẩn định dạng & bảo toàn:** Toàn bộ văn bản và bảng biểu thống nhất phông **Times New Roman, cỡ 14pt**. Bảng biểu bảo toàn đúng số hàng, số cột, **ô gộp (merged cells)** và viền gốc. Giữ trạng thái chữ gạch xóa (`strikethrough`) và ghi chú lề (`[Ghi chú lề: ...]`).
   - **Kiến trúc nhận diện lai (Hybrid Extraction Pipeline):** Vùng PDF có text dùng `PyMuPDF` lấy cấu trúc & text; vùng scan, ảnh chụp, chữ viết tay, công thức đưa qua Vision AI trích xuất Markdown + LaTeX trung gian.
   - **Quy tắc xử lý công thức toán (Kiểm soát kép):** Công thức rõ và OMML thành công xuất Word Equation `m:oMath` cỡ 14pt; công thức mờ hoặc lỗi OMML bắt buộc crop ảnh gốc chèn vào kèm nhãn đỏ `[Công thức chưa đọc rõ / Lỗi chuyển đổi — Mã NDxx]`.
   - **Bộ Tag chuẩn đánh dấu đỏ & truy vết (Red-Flag & Audit Tags `ND01, ND02...`):** In đậm, màu đỏ (`RGB: 255, 0, 0`) cho 5 tình huống (chữ mờ nhiều cách đọc, đọc được một phần, không đọc được + chèn ảnh cắt vùng nguồn, nội dung bị lẹm mép giấy, nghi bản gốc viết sai số liệu/chính tả thì giữ nguyên gốc màu đen + thêm ghi chú đề nghị kiểm tra màu đỏ).
   - **Xử lý hình ảnh & hình vẽ tay:** Mặc định cắt giữ nguyên cụm ảnh gốc. Tái tạo hình vẽ tay qua `ve_hinh_engine.py` là bước có điều kiện (chỉ khi có đủ dữ kiện tọa độ/nhãn đỉnh/góc vuông rõ ràng; luôn giữ song song hình tái tạo + ảnh cắt bản gốc + nhãn đỏ). Nếu mờ chỉ giữ ảnh cắt bản gốc + nhãn đỏ.
   - **Bước kiểm tra bỏ sót (Pre-export Verification) & Báo cáo đối chiếu (Audit Log):** Đối soát từng vùng trên trang nguồn; xuất bảng tổng hợp Audit Log ở trang cuối file Word liệt kê toàn bộ mã `NDxx` kèm trang, loại cảnh báo, ảnh cắt vùng nguồn. Xuất kèm tệp JSON lưu dữ liệu cấu trúc truy vết.
   - **Tuân thủ 5 điểm bổ sung:**
     + Chốt mô hình thực tế và fallback khi gọi Vision model.
     + Lưu kèm metadata JSON cấu trúc truy vết (`NDxx`, `page`, `bbox`, `type`, `raw_text`, `suggestion`).
     + Giữ nguyên ảnh nguồn gốc để làm căn cứ đối chứng (bản tiền xử lý tăng tương phản chỉ hỗ trợ nhận diện, không ghi đè ảnh gốc).
     + Kiểm tra kết quả hiển thị thực tế của `m:oMath`.
     + Báo cáo trạng thái trung thực: Phân biệt rõ "đã chuyển đổi, còn vị trí cần đối chiếu" và "đã được người dùng xác nhận", kết luận "đã có quy tắc kiểm soát; hiệu quả cần được xác minh qua bộ mẫu thử nghiệm".
3. Tích hợp Menu điều hướng:
   - Bổ sung Mục 14 vào `.agents/workflows/thien.md` và `TROLYTHIEN/tro-ly-thien-menu.html`.
4. Xây dựng Bộ mẫu thử nghiệm (Test Suite) bao gồm 5 ca khó để nghiệm thu trước khi triển khai rộng:
   - Ca 1: Bảng có ô gộp (merged cells) và đường viền phức tạp.
   - Ca 2: Công thức toán học phức tạp (phân số tầng, căn thức, hệ phương trình).
   - Ca 3: Hình vẽ vector có kèm nhãn chữ.
   - Ca 4: Chữ viết tay có chỗ mờ và chỗ sai phép tính rõ nét ($2+3=6$).
   - Ca 5: Văn bản bị cắt lẹm ở mép ảnh.

## Ngoài phạm vi
- Không sửa đổi mã nguồn và chức năng của các nhánh từ 1 đến 13.
- Không tự ý nối nét hoặc phục hồi chữ bị mất bằng nội dung do AI bịa đặt.
- Chưa triển khai đại trà ngoài bộ mẫu thử nghiệm cho đến khi nghiệm thu 5 ca khó đạt tiêu chuẩn.

## File dự kiến tác động
- `TROLYTHIEN/14_NHAN_DIEN_VAN_BAN/HUONG_DAN_NHAN_DIEN_VAN_BAN.md` (Tạo mới)
- `TROLYTHIEN/14_NHAN_DIEN_VAN_BAN/PROMPT_NHAN_DIEN_VAN_BAN.md` (Tạo mới)
- `TROLYTHIEN/engine/nhan_dien_engine.py` (Tạo mới)
- `TROLYTHIEN/tro-ly-thien-menu.html` (Cập nhật Menu cấp 1)
- `.agents/workflows/thien.md` (Cập nhật Menu cấp 1 và nhánh 14)
- `tests/nhan-dien-van-ban-smoke.py` (Tạo mới kịch bản test tự động)

## Các bước thực hiện
1. **Bước 1 (Khởi tạo thư mục):** Tạo cấu trúc `TROLYTHIEN/14_NHAN_DIEN_VAN_BAN/Dau_vao/` và `TROLYTHIEN/14_NHAN_DIEN_VAN_BAN/Ket_qua/`.
2. **Bước 2 (Soạn thảo văn bản quy chuẩn):**
   - Viết `HUONG_DAN_NHAN_DIEN_VAN_BAN.md` đặc tả đầy đủ 7 quy tắc chuẩn đầu ra và 5 điểm bổ sung.
   - Viết `PROMPT_NHAN_DIEN_VAN_BAN.md` chứa Master Prompt chuẩn cho Vision AI, định dạng thẻ `[NDxx]`.
3. **Bước 3 (Xây dựng Engine `nhan_dien_engine.py`):**
   - Bộ đọc PDF lai: tách văn bản số bằng `pymupdf` và trích xuất ảnh/vùng scan.
   - Bộ cắt ảnh (Bounding Box Cropper) lưu ảnh đối chứng từ file gốc chưa xử lý.
   - Bộ xử lý công thức: tích hợp `latex_to_omml` từ `de_cuong_docx_helper.py`, bắt lỗi fallback chèn ảnh cắt + mã `NDxx`.
   - Bộ sinh tài liệu Word `.docx`: thiết lập Times New Roman 14pt toàn diện, xử lý merged cells, tô đỏ `RGB(255, 0, 0)` cho các thẻ `NDxx`.
   - Bộ sinh bảng Audit Log ở trang cuối và xuất kèm file JSON metadata.
4. **Bước 4 (Bộ mẫu thử nghiệm & Kịch bản test):**
   - Tạo `tests/nhan-dien-van-ban-smoke.py` dựng 5 ca khó giả lập.
   - Chạy engine sinh file `.docx` mẫu và xác minh tính toàn vẹn.
5. **Bước 5 (Tích hợp Menu):**
   - Cập nhật mục 14 vào `tro-ly-thien-menu.html`.
   - Cập nhật mục 14 vào workflow `/thien` trong `.agents/workflows/thien.md`.
6. **Bước 6 (Báo cáo & Handoff):** Chạy kiểm thử tự động, chuẩn bị tài liệu nghiệm thu.

## Rủi ro
- *Rủi ro công thức LaTeX phức tạp gây crash `latex_to_omml`:* Giải pháp: Bọc `try...except`, khi lỗi lập tức chuyển sang Trường hợp 2 (chèn ảnh cắt vùng gốc + nhãn đỏ `[Công thức chưa đọc rõ / Lỗi chuyển đổi — Mã NDxx]`).
- *Rủi ro ảnh chữ viết tay bị nghiêng hoặc nhiễu:* Bản tăng tương phản/xoay chỉ dùng làm bản phụ trợ đưa vào AI đọc; ảnh cắt làm đối chứng bắt buộc cắt từ ảnh gốc nguyên bản.
- *Rủi ro AI tự ý sửa sai hoặc bịa chữ (Hallucination):* Ràng buộc chặt trong Prompt và bộ lọc Engine: Mọi đề xuất sửa sai phải tách biệt hoàn toàn trong ngoặc vuông màu đỏ, chữ bản gốc màu đen được bảo toàn 100%.

## Cách kiểm thử
1. Chạy test tự động:
   ```bash
   python tests/nhan-dien-van-ban-smoke.py
   ```
2. Kiểm tra tài liệu Word `.docx` sinh ra:
   - Xác nhận tất cả các đoạn văn và ô bảng đều dùng phông Times New Roman 14pt.
   - Xác nhận các công thức toán hợp lệ thành phần tử `m:oMath` cỡ 14pt.
   - Xác nhận các ô gộp trong bảng được merge chính xác.
   - Xác nhận các thẻ cảnh báo hiển thị đúng màu đỏ `RGB(255, 0, 0)` kèm mã `NDxx`.
   - Xác nhận trang cuối có Bảng đối soát (Audit Log) đầy đủ.
   - Xác nhận file JSON metadata được tạo song song và có tọa độ bbox chính xác.

## Tiêu chí nghiệm thu
- Thư mục `TROLYTHIEN/14_NHAN_DIEN_VAN_BAN/` có đủ `Dau_vao/`, `Ket_qua/`, `HUONG_DAN_NHAN_DIEN_VAN_BAN.md` và `PROMPT_NHAN_DIEN_VAN_BAN.md`.
- `TROLYTHIEN/engine/nhan_dien_engine.py` vận hành thông suốt qua CLI:
  ```bash
  python -m TROLYTHIEN.engine.nhan_dien_engine --input "đường_dẫn"
  ```
- Bộ mẫu thử nghiệm 5 ca khó chạy thành công, sinh file Word hợp lệ đạt chuẩn 14pt.
- Menu `/thien` và `tro-ly-thien-menu.html` có mục 14 được cập nhật đồng bộ.
- Kết luận nghiệm thu ghi rõ: "Đã có quy tắc kiểm soát; hiệu quả cần được xác minh qua bộ mẫu thử nghiệm".
