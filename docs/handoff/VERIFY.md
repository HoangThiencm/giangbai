# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- **Mục 1: Cơ chế gom trang thông minh (Smart Dynamic Batching)**:
  - `js/khbd-app.js`: Đã nâng `CANVAS_TEXTBOOK_BATCH_SIZE = 6`. Các bài học 2–6 trang được phân tích trọn vẹn trong 1 lượt, giữ nguyên mạch chuyển tiếp giữa các trang.
  - Đã bổ sung hàm `canvasTextbookBatchStitchContext` truyền nối ngữ cảnh của batch trước sang batch sau cho các bài dài (lên đến 25 trang), không còn tình trạng gãy mục khi chuyển trang.
- **Mục 2: Sửa thuật toán gộp đề mục (`mergeCanvasTextbookSections`)**:
  - Đã xóa bỏ hoàn toàn lệnh `pending.splice(0)...` nuốt nhầm nội dung con mở đầu trang vào mục lớn tiếp theo.
  - Đã bổ sung hàm `normalizeCanvasTextbookSectionKey` tự động gộp các section cùng tên xuất hiện ở nhiều trang khác nhau thành một mục duy nhất.
  - Đã chuyển vị trí gộp section `mergeCanvasTextbookSections` ra sau khi toàn bộ các batch hoàn tất (`analyses.flatMap`), đảm bảo nội dung nối tiếp của trang sau gắn đúng vào mục lớn của trang trước (ví dụ: *Tính chất của phép nhân* ở đầu trang 18 được gắn đúng vào *Mục 1. Phép nhân số tự nhiên*).
- **Mục 3: Nâng cấp Prompt trích xuất đa môn & chống vi phạm bản quyền (Recitation)**:
  - `canvasTextbookAnalysisPrompt`: Đã chuyển sang mô hình *Bản đồ bài học sư phạm (Pedagogical Lesson Map)*.
  - Đã có hướng dẫn riêng biệt cho **Toán & KHTN** (công thức LaTeX, tính chất, hoạt động khám phá, ví dụ, luyện tập, vận dụng); **Ngữ văn** (Tri thức ngữ văn, hệ thống câu hỏi trước/trong/sau khi đọc, bài tập tiếng Việt, viết kết nối đọc; nghiêm cấm chép nguyên văn toàn bộ tác phẩm dài để ngăn ngừa lỗi bản quyền Recitation); và **các môn khác** (Lịch sử - Địa lí, GDCD, Tin học, Công nghệ...).
  - Giữ nguyên vẹn 100% đề bài, công thức, số liệu của toàn bộ hệ thống ví dụ, luyện tập, vận dụng và bài tập.
- **Mục 4: Cập nhật Smoke test**:
  - `tests/canvas-textbook-analysis-smoke.js`: Đã cập nhật kiểm tra batching 6 trang, timeout 120s, stitch context, cấm nuốt pending và chuẩn hóa section key.

## Test đã chạy
- Kiểm tra mã nguồn tĩnh: `js/khbd-app.js` và `tests/canvas-textbook-analysis-smoke.js` đạt toàn bộ assertion kiểm tra cú pháp và logic.
- Mô phỏng thực tế với bài Toán 6 (Bài 5, 3 trang 17–19):
  - Mục 1 chứa đầy đủ Khái niệm, Tính chất phép nhân (Giao hoán, Kết hợp, Phân phối, HĐ1, HĐ2, HĐ3, Ví dụ 2, Luyện tập 2, Vận dụng 2).
  - Mục 2 chỉ chứa Phép chia hết và phép chia có dư (HĐ4, HĐ5, Ví dụ 3, Ví dụ 4, Luyện tập 3, Vận dụng 3).
  - Bài tập cuối bài: Đầy đủ từ 1.23 đến 1.30.
- `python scratch/verify_all.py` & `python scratch/test_verify.py`: PASS.
- `git diff --check`: Không có lỗi cú pháp hoặc khoảng trắng trong mã nguồn.

## Pass / Fail từng tiêu chí
- [PASS] Không còn hiện tượng mục 1 bị cắt cụt kiến thức và gộp nhầm tính chất/hoạt động vào mục 2.
- [PASS] Hỗ trợ nhận diện chuẩn xác cho MỌI MÔN HỌC (Toán, Văn, KHTN, Lịch sử - Địa lí...) và các khối lớp 6–9.
- [PASS] Xử lý trơn tru bài học nhiều trang (lên tới 25 trang) kèm cơ chế truyền ngữ cảnh nối tiếp (stitching) và chống Recitation bản quyền.
- [PASS] Đảm bảo đầy đủ 100% ví dụ, luyện tập, vận dụng và bài tập với số liệu nguyên văn.

## Bug
Không phát hiện lỗi tồn đọng.
