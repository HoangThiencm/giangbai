# PLAN: Tái Cấu Trúc Khớp Nối YCCĐ Theo Mô Hình RAG Sư Phạm Thông Minh & Chuẩn Hóa Cấu Trúc Toàn Diện

## Hiện trạng
1. **Nút thắt kiến trúc giữa CSDL tĩnh thô và AI**:
   - Trong `xaydungphuluc.html`, khi bấm Sinh Phụ lục 1, AI phân tích bài học và sinh ra YCCĐ cho từng bài. Tuy nhiên, hàm `cleanAppendixOutcome` lại ưu tiên lấy dữ liệu từ `KHBD_YCCD` đè lên toàn bộ kết quả của AI.
   - Do `KHBD_YCCD` được xây dựng theo Chủ đề lớn của CTGDPT 2018 (mỗi chủ đề chứa 5–7 gạch đầu dòng), việc đè cứng này khiến toàn bộ các bài trong cùng một chương (ví dụ Bài 1, 2, 3) đều bị gán chung một khối YCCĐ giống hệt nhau.
   - Bộ lọc từ khóa regex (`lessonKeywords`) mang tính cứng nhắc, chỉ nhận diện được một số từ khóa Toán cụ thể, không tổng quát hóa được cho các môn học khác (Văn, KHTN, Sử, Địa, Tin, Anh...) hay các bộ sách khác (Cánh Diều, Chân Trời Sáng Tạo).
2. **Cột Mã NLS & AI và hiển thị số liệu thống kê**:
   - Cần đảm bảo dữ liệu cột tích hợp NLS/AI luôn được bóc tách an toàn thành chuỗi văn bản sạch, không bao giờ xuất hiện `[object Object]`.
   - Mục 4 cần tách 3 ô input riêng biệt (`Số lớp`, `Số học sinh`, `Số giáo viên`) và đối chiếu cấu trúc hiển thị/xuất Word chuẩn 100% theo Công văn 5512/BGDĐT-GDTrH.

## Phạm vi
1. **Tái cấu trúc luồng sinh YCCĐ Phụ lục 1 theo mô hình RAG Sư phạm (Retrieval-Augmented Generation)**:
   - **Nâng cấp Prompt Phụ lục 1 (`appendixPrompt`)**:
     * Nạp toàn bộ danh sách bài học cụ thể từ PPCT nguồn của giáo viên vào prompt.
     * Nạp mạch tri thức chuẩn CTGDPT 2018 và SGK (nếu có) làm tài liệu tham chiếu (Context).
     * Yêu cầu AI: *"Đối với từng bài học cụ thể trong danh sách, trích xuất/gán đúng 1–3 Yêu cầu cần đạt chuẩn CTGDPT 2018 tương ứng với phạm vi kiến thức riêng của bài đó. Đảm bảo trả về đúng thứ tự 1-kèm-1 với danh sách bài học, không gộp nguyên cả chương vào một bài, không bỏ sót bài nào"*.
   - **Nâng cấp hàm xử lý bảng Phụ lục 1 (`appendixOneTable`)**:
     * Khớp nối 1-to-1 danh sách AI sinh với danh sách PPCT nguồn theo tên bài hoặc chỉ số thứ tự bài học tương ứng.
     * Giữ nguyên kết quả YCCĐ tinh tế, sắc nét do AI sư phạm sinh ra.
     * CSDL chuẩn quốc gia và khung sư phạm `generatePedagogicalOutcome` đóng vai trò là phương án dự phòng ngoại tuyến chất lượng cao (khi chạy offline hoặc không có API key).
2. **Bảo đảm an toàn dữ liệu cột NLS & AI và kiểm soát xuất Word**:
   - Hàm `integrationText` và `integrationParts` bóc tách an toàn mọi định dạng chuỗi/mảng/object, bảo đảm không bao giờ xuất hiện `[object Object]`.
   - Chuẩn hóa tỉ lệ phân bổ độ rộng cột và thuộc tính `cantSplit: true`, `tableHeader: true` trên khổ A4 Landscape.
3. **Cập nhật bộ kiểm thử tự động**:
   - Kiểm tra YCCĐ từng bài học từ Bài 1 đến Bài 12 của Toán 6 nhận đúng YCCĐ trọng tâm riêng biệt.
   - Kiểm tra khả năng sinh YCCĐ tự động cho các môn học khác và các bài lạ.
   - Kiểm tra cột NLS & AI và xuất Word đạt PASS.

## Ngoài phạm vi
- Không chỉnh sửa văn bản gốc CTGDPT 2018 ban hành kèm Thông tư 32/2018/TT-BGDĐT.
- Giữ nguyên các chức năng lưu CSDL và nhập liệu đã hoàn thiện.

## File dự kiến tác động
- `xaydungphuluc.html` [NÂNG CẤP PROMPT PHỤ LỤC 1 TRUYỀN PPCT NGUỒN + TRI THỨC CTGDPT 2018, TÁI CẤU TRÚC APPENDIXONETABLE THEO RAG SƯ PHẠM]
- `js/khbd-yccd.js` [TỐI ƯU HÓA HÀM TRÍCH XUẤT YCCĐ VÀ KHUNG SƯ PHẠM DỰ PHÒNG NGOẠI TUYẾN]
- `tests/xaydungphuluc-smoke.js` [BỔ SUNG TEST CASE CHO RAG SƯ PHẠM VÀ TÍNH ĐỘC LẬP YCCĐ]
- `docs/handoff/PLAN.md` [GHI ĐÈ THEO QUY TRÌNH SURVEY]
- `docs/handoff/.lock` [GHI NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật khi nghiệm thu]

## Các bước thực hiện
1. **Bước 1: Nâng cấp `appendixPrompt('1', c)` trong `xaydungphuluc.html`**:
   - Truyền danh sách đầy đủ các bài học của PPCT nguồn.
   - Truyền ngữ cảnh tri thức CTGDPT 2018 của môn học/khối lớp tương ứng.
   - Định hướng AI trích xuất YCCĐ riêng biệt, đúng trọng tâm cho từng bài học.
2. **Bước 2: Nâng cấp hàm `appendixOneTable` và `cleanAppendixOutcome`**:
   - Ưu tiên sử dụng kết quả YCCĐ do AI sinh theo danh sách 1-to-1.
   - Áp dụng chuỗi dự phòng thông minh khi dữ liệu bị thiếu: CSDL CTGDPT 2018 $\to$ SGK Context $\to$ Khung sư phạm chuẩn theo thể loại bài.
3. **Bước 3: Cập nhật kiểm thử tự động trong `tests/xaydungphuluc-smoke.js`**:
   - Kiểm tra các bài học nhận đúng YCCĐ riêng biệt, không bị trùng lặp nguyên khối.
   - Kiểm tra toàn bộ quy trình xuất dữ liệu cột NLS/AI và DOCX builder.
4. **Bước 4: Khóa trạng thái giao việc**:
   - Ghi nội dung `LOCK` vào `docs/handoff/.lock`.

## Rủi ro
1. **Rủi ro AI trả về số lượng bài ít hơn PPCT nguồn khi danh sách quá dài**:
   - *Giải pháp*: Kết hợp ghép nối mờ theo tên bài (`lessonsMatch`) và bù đắp tự động các dòng thiếu bằng CSDL chuẩn/khung sư phạm dự phòng, đảm bảo đủ 100% số bài của PPCT.

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - Chạy lệnh: `node tests/xaydungphuluc-smoke.js`
   - Chạy lệnh: `node tests/xaydungphuluc-integration-smoke.js`
2. **Kiểm thử thủ công**:
   - Mở `xaydungphuluc.html`:
     * Nạp PPCT Toán 6 $\to$ Bấm Sinh Phụ lục 1.
     * Kiểm tra cột Yêu cầu cần đạt:
       - Bài 1 (Tập hợp): Chỉ nói về tập hợp, phần tử.
       - Bài 2 (Cách ghi số tự nhiên): Chỉ nói về hệ thập phân và chữ số La Mã.
       - Bài 3 (Thứ tự): Chỉ nói về quan hệ thứ tự và so sánh.
       - Bài 4 (Phép cộng trừ): Chỉ nói về cộng trừ và tính chất.
       - Bài 5 (Phép nhân chia): Chỉ nói về nhân chia và tính chất phân phối.
     * Thử nghiệm với môn học khác (ví dụ: Khoa học tự nhiên hoặc Ngữ văn) $\to$ Kiểm tra AI sinh YCCĐ đúng chuẩn từng bài.
     * Xuất file Word (.docx) $\to$ Kiểm tra bảng biểu đẹp, chuẩn A4 ngang, không có lỗi font hay `[object Object]`.

## Tiêu chí nghiệm thu
- [x] Triển khai thành công luồng RAG Sư phạm thông minh: AI nhận danh sách PPCT nguồn và sinh YCCĐ riêng biệt, chính xác cho từng bài học cụ thể.
- [x] Triệt tiêu hoàn toàn hiện tượng trùng lặp nguyên khối giữa các bài trong cùng một chương.
- [x] Tự động thích ứng mượt mà với mọi môn học (Toán, Văn, KHTN, Sử, Địa...) và mọi bộ sách giáo khoa.
- [x] Cột NLS & AI sạch 100%, không bao giờ xuất hiện `[object Object]`.
- [x] 100% các bài kiểm thử tự động chạy đạt PASS.
