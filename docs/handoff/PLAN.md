# PLAN: Phân hóa Triệt để Năng lực số (NLS) và Trợ lý AI Sư phạm theo Cấp độ Nhận thức từng Bài học trong Kho Tri thức SGK

## Hiện trạng & Phản ánh của Người dùng
- **Phản ánh từ User**:
  > *"nhưng mà năng lực số của cả các bài này giống nhau đều được hả? bài 1 mới nhận biết thôi mà. Bài 2 mới giải hệ pt, bài 3 thì lại liên quan giải bài toán bằng cách lập pt. Đây là tôi ví dụ. Mỗi bài đều có năng lực số, AI khác nhau chứ. Cho dù là nạp từ SGK hay nạp từ tri thức. Chỗ này bị nhầm lẫn nè"*

- **Khảo sát gốc rễ mã nguồn**:
  1. **Trong `js/khbd-standards.js`**:
     - Hàm `scoreOfficialStandard` khi chấm điểm nhánh `algebra`:
       Gom chung toàn bộ bài học có chữ "phuong trinh" vào một rổ, luôn cộng điểm tối đa cho `5.3`, `3.1`, `5.2`.
       Không phân biệt bài **Khái niệm / Nhận biết** (Bài 1) với bài **Rèn kỹ năng giải** (Bài 2) với bài **Mô hình hóa thực tế** (Bài 3).
  2. **Trong `recommendLessonDigitalCandidates` (`xaydungphuluc.html` & Canvas)**:
     - Dùng regex gộp trả về cùng bộ mã `5.3.TC2a, 3.1.TC2a, 5.2.TC2a` cho cả 3 bài.
  3. **Trong `lessonAppliedNlsDescription` (`xaydungphuluc.html` & Canvas)**:
     - Khi kiểm tra `isEquation`, sinh ra đúng một mẫu văn bản dập khuôn:
       * 5.3: *"Sử dụng máy tính cầm tay để tìm nghiệm, kiểm tra nghiệm và phần mềm GeoGebra/Desmos vẽ đồ thị minh họa nghiệm hình học..."*
       * 3.1: *"Sử dụng công cụ số (GeoGebra/trình chiếu) để mô hình hóa và trình bày các bước giải..."*
     - Hậu quả sư phạm: Bài 1 mới học "Khái niệm phương trình" (chưa học cách giải) nhưng bị gán "trình bày các bước giải" và "vẽ đồ thị minh họa nghiệm hình học"!
  4. **Trong `lessonAppliedAiDescription` (`xaydungphuluc.html` & Canvas)**:
     - Nhánh domain B luôn trả về câu cố định:
       *"Ứng dụng công cụ AI hỗ trợ gợi ý các bước giải bài ${clean}, học sinh đối chiếu kết quả với SGK..."*
     - Cả Bài 1, Bài 2, Bài 3 đều có chung một câu gợi ý giải bài tập, làm mất tính sư phạm phân hóa.
  5. **Dữ liệu CSDL máy chủ hosting (`hoangthiencm.id.vn`)**:
     - Kho tri thức Toán 9 đang lưu 32 bài học, trong đó Bài 1, Bài 2, Bài 3 đang chứa cùng các đoạn minh chứng NLS và gợi ý AI dập khuôn do được sinh từ engine cũ.

---

## Mục tiêu Cần đạt
1. **Phân hóa rõ rệt 3 cấp độ nhận thức sư phạm cho chủ đề Phương trình & Hệ phương trình (điển hình Toán 9 Bài 1, 2, 3)**:
   - **Bài 1 (Khái niệm, Nhận biết)**:
     * NLS: `1.1.TC2a, 5.3.TC2a, 3.1.TC2a`
     * Minh chứng: Khai thác video/học liệu số nhận diện dạng ax+by=c; Dùng máy tính cầm tay (CALC / tính giá trị biểu thức) kiểm tra cặp số (x0; y0) có là nghiệm không; Phần mềm sơ đồ tư duy hệ thống hóa cấu trúc tổng quát và tập nghiệm.
     * AI: Trợ lý AI tạo ví dụ ngẫu nhiên cặp số và phương trình/hệ phương trình để học sinh luyện tập kiểm tra nghiệm, phân tích nguyên nhân thỏa mãn hoặc không thỏa mãn định nghĩa.
   - **Bài 2 (Kỹ năng giải, Thuật toán giải)**:
     * NLS: `5.3.TC2a, 5.1.TC2a, 5.2.TC2a`
     * Minh chứng: Sử dụng chức năng giải hệ (EQUATION/SIMULT) trên máy tính cầm tay kiểm tra kết quả giải bằng phương pháp thế hoặc cộng đại số; Xử lý thông báo vô số nghiệm (Infinite Solutions) / vô nghiệm (No Solution) hoặc lỗi cú pháp; GeoGebra minh họa giao điểm 2 đường thẳng biểu diễn số nghiệm.
     * AI: Trợ lý AI phân tích hệ số đề xuất lựa chọn phương pháp giải tối ưu (phương pháp thế hay cộng đại số); học sinh tự biến đổi và kiểm chứng kết quả.
   - **Bài 3 (Giải bài toán thực tế / Mô hình hóa toán học)**:
     * NLS: `3.1.TC2a, 5.3.TC2a, 1.2.TC2a`
     * Minh chứng: Bảng tính Excel/Sheets lập bảng phân tích đại lượng (vận tốc, thời gian, quãng đường; năng suất...); Máy tính cầm tay giải hệ và kiểm tra đối chiếu điều kiện thực tế của ẩn (nghiệm nguyên, dương, nằm trong khoảng cho phép); Đánh giá tính hợp lý và độ tin cậy của kết quả số so với đời sống.
     * AI: Trợ lý AI phản biện bước chọn ẩn số, đặt điều kiện thực tế và gợi mở mối liên hệ ràng buộc giữa các đại lượng; học sinh tự xây dựng hệ phương trình, giải và chịu trách nhiệm.

2. **Mở rộng phân hóa sư phạm cho toàn bộ các dạng bài học Toán và các môn học**:
   - Khái niệm / Mở đầu vs Thuật toán / Biến đổi / Phép tính vs Bài toán thực tế / Mô hình hóa.
   - Hàm số & Đồ thị: Khái niệm (bảng giá trị TABLE) vs Vẽ đồ thị (GeoGebra khảo sát đỉnh/hướng) vs Bài toán thực tế.
   - Hình học: Khái niệm mở đầu vs Định lý/Tính toán (tỉ số lượng giác, hệ thức lượng) vs Hình học không gian 3D.
   - Thống kê: Bảng số liệu & Tần số vs Bảng tần số tương đối/ghép nhóm vs Phép thử & Xác suất thực nghiệm.

3. **Đồng bộ mã nguồn & CSDL**:
   - Cập nhật engine đề xuất trong `js/khbd-standards.js`.
   - Cập nhật các hàm sinh NLS & AI trong `xaydungphuluc.html`, `canvas_xaydungphuluc.html`, `backupcode viettailieu/canvas_xaydungphuluc.html`.
   - Cập nhật danh mục `DEFAULT_MATH_CATALOG` (Toán 6, 7, 8, 9).
   - Đẩy dữ liệu chuẩn hóa lên CSDL máy chủ hosting `hoangthiencm.id.vn` qua API `action=save`.
   - Bổ sung bộ kiểm thử tự động trong `tests/sgk-knowledge-smoke.js` và đảm bảo 100% test suites PASS.
