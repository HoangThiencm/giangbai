# PLAN: So Khớp Chính Xác Yêu Cầu Cần Đạt (YCCĐ) Theo Bài Học Với Chiến Lược Dự Phòng 4 Tầng & Chuẩn Hóa Định Dạng Bảng Xuất Word (A4 Ngang)

## Hiện trạng
1. **Lệch pha nghiêm trọng giữa Tên bài học và Yêu cầu cần đạt ("Râu ông nọ cắm cằm bà kia")**:
   - Trong `xaydungphuluc.html`, hàm `appendixOneTable` thực hiện ánh xạ YCCĐ từ danh sách AI sinh (`generatedRows`) sang danh sách PPCT nguồn (`source`).
   - Khi tên bài học từ PPCT nguồn có sự khác biệt nhỏ về tiền tố/câu chữ so với tên bài AI trả về (ví dụ: "Bài 5: Phép nhân và phép chia số tự nhiên" vs "Phép nhân và phép chia"), phép tìm kiếm `generatedRows.find(item => item.lesson === row.lesson)` bị thất bại.
   - Hệ thống tự động rơi vào fallback `generatedRows[normal]` (lấy bài học tại chỉ số thứ tự `normal`). Vì danh sách AI sinh thường ít dòng hơn hoặc sắp xếp khác, chỉ số `normal` bị lệch vị trí, dẫn đến việc:
     * Bài 5 (Phép nhân và phép chia) bị gán nhầm YCCĐ của Bài 1, 2, 3 (Thuật ngữ tập hợp, số La Mã, thứ tự số tự nhiên).
     * Bài 6 (Luyện tập chung) bị gán nhầm YCCĐ của Bài 8 (Ước và bội).
     * Các bài tiếp theo bị gán nhầm YCCĐ của chương sau (Số nguyên tố, hợp số, phân số...).
   - Khi fallback không tìm thấy trong CSDL, hệ thống chưa có khung câu chữ sư phạm chuẩn hóa theo loại bài học, dẫn đến việc nội dung bị rỗng hoặc lấy sai lệch.
2. **Định dạng bảng trong file Word (.docx) chia đều cột ($100/N\%$), chưa phân bổ tỉ lệ theo nội dung**:
   - Trong hàm `exportDocx`, hàm `addPpct` và `addTable` chia đều độ rộng mọi cột bằng `width: 100 / columns.length`.
   - Đối với Phụ lục 1 (5 cột), mỗi cột bị chia 20%:
     * Cột STT (chỉ chứa 1 chữ số) và Cột Số tiết (chỉ chứa số 1–4) lại chiếm tới 20% chiều rộng trang.
     * Cột Yêu cầu cần đạt (chứa nội dung dài nhiều gạch đầu dòng) chỉ được chia 20%, khiến văn bản bị bóp nghẹt, co dúm và kéo dài nhiều trang.
   - Đối với Phụ lục 3 (7 cột), mỗi cột bị chia 14.28%, khiến cột Tuần/Số tiết quá rộng trong khi cột Bài học và Thiết bị/Địa điểm bị chật.
   - Cần chuẩn hóa tỉ lệ phân bổ độ rộng cột (Column Width Distribution) cho từng bảng trong Phụ lục 1, Phụ lục 2 và Phụ lục 3 khi xuất Word.

## Phạm vi
1. **Chiến lược xử lý & dự phòng 4 tầng (Multi-tiered Fallback Strategy) cho Yêu cầu cần đạt**:
   - **Tầng 1: So khớp CSDL CTGDPT 2018 (`KHBD_YCCD` trong `js/khbd-yccd.js`)**:
     * Khớp theo từ khóa cốt lõi của bài học (ví dụ: `phép nhân chia`, `số tự nhiên`, `ước chung`, `tam giác đều`...).
     * Đối với bài *Luyện tập chung / Ôn tập chương*: Tự động gom YCCĐ củng cố từ các bài học liền trước của chương đó.
   - **Tầng 2: Trích xuất từ tệp SGK đính kèm (nếu người dùng có tải lên)**:
     * Trích xuất mục tiêu bài học ("Học xong bài này em sẽ...") từ khối SGK tương ứng của tên bài đó.
   - **Tầng 3: AI Sư phạm sinh có kiểm chứng ngữ nghĩa (Semantic Validation)**:
     * Nếu AI sinh ra YCCĐ có chứa các từ khóa trong tên bài học đó $\rightarrow$ Chấp nhận.
     * Nếu AI sinh nội dung của bài khác (ví dụ: bài Phép nhân mà trả về YCCĐ Tập hợp) $\rightarrow$ Từ chối, chuyển sang Tầng 4.
     * Tuyệt đối không dùng fallback `generatedRows[normal]` khi tên bài không khớp.
   - **Tầng 4: Khung YCCĐ Sư phạm chuẩn hóa theo Thể loại bài học (Không bao giờ để râu ông nọ cắm cằm bà kia)**:
     * *Bài học lý thuyết mới*:
       `- Nhận biết và phát biểu được các khái niệm, quy tắc, tính chất trọng tâm của [Tên bài].\n- Vận dụng được kiến thức, kĩ năng đã học để giải quyết các bài tập và tình huống thực tiễn liên quan.`
     * *Bài Luyện tập / Ôn tập / Thực hành*:
       `- Củng cố, hệ thống hóa và khắc sâu các kiến thức, kĩ năng trọng tâm của [Tên bài].\n- Rèn luyện kĩ năng tính toán, phân tích và vận dụng linh hoạt các phương pháp giải bài tập.`
     * *Bài Đánh giá định kỳ (Giữa kỳ / Cuối kỳ)*:
       `- Đánh giá mức độ đạt được các yêu cầu cần đạt về phẩm chất, năng lực học sinh theo chương trình môn học đến thời điểm kiểm tra.`
     * *Bài Chuyên đề / STEM / Trải nghiệm*:
       `- Vận dụng kiến thức liên môn để giải quyết vấn đề thực tiễn, phát triển tư duy sáng tạo và kĩ năng hợp tác nhóm.`
   - **Tầng 5: Cho phép Giáo viên chỉnh sửa trực tiếp (Inline Edit)**:
     * Giáo viên có thể nhấp chuột chỉnh sửa trực tiếp từng ô YCCĐ ngay tại bảng xem trước ở Mục 7 hoặc Mục 3 trước khi xuất file Word.
2. **Chuẩn hóa tỉ lệ độ rộng cột và định dạng trang in file Word (.docx)**:
   - Thiết lập chuẩn khổ giấy A4 Landscape ($297\text{ mm} \times 210\text{ mm} = 16.838 \times 11.906\text{ dxa}$), lề trang $20\text{ mm}$ ($1.134\text{ dxa}$).
   - Phân bổ độ rộng cột tối ưu theo nội dung thực tế:
     * **Phụ lục 1 (Bảng Kế hoạch dạy học - 5 cột)**:
       - STT: 5%
       - Bài học: 22%
       - Số tiết: 6%
       - Yêu cầu cần đạt: 47%
       - Mã NLS & AI (CV 3456 & QĐ 2422): 20%
     * **Phụ lục 1 (Bảng Thiết bị dạy học - 5 cột)**:
       - STT: 6%, Tên thiết bị: 34%, Số lượng: 15%, Sử dụng trong bài học: 30%, Ghi chú: 15%.
     * **Phụ lục 1 (Bảng Phòng học bộ môn - 5 cột)**:
       - STT: 6%, Tên phòng: 30%, Số lượng: 14%, Phạm vi sử dụng: 35%, Ghi chú: 15%.
     * **Phụ lục 1 (Bảng Kiểm tra, đánh giá định kỳ - 5 cột)**:
       - Bài kiểm tra: 22%, Thời gian: 12%, Thời điểm: 12%, Hình thức: 18%, Yêu cầu cần đạt: 36%.
     * **Phụ lục 2 (Bảng Hoạt động giáo dục - 9 cột)**:
       - Chủ đề: 16%, YCCĐ: 26%, Thời lượng: 7%, Thời điểm: 7%, Địa điểm: 10%, Chủ trì: 9%, Phối hợp: 8%, Điều kiện: 8%, NLS & AI: 9%.
     * **Phụ lục 3 (Bảng Kế hoạch giáo dục của giáo viên - 7 cột)**:
       - Bài học: 22%
       - Số tiết: 6%
       - Tiết CT: 8%
       - Tuần: 6%
       - Thiết bị dạy học (*): 18%
       - Địa điểm dạy học (**): 16%
       - Mã NLS & AI (CV 3456 & QĐ 2422): 24%
   - Thêm thuộc tính `cantSplit: true` trên từng hàng và `tableHeader: true` trên hàng tiêu đề để bảng khi ngắt trang không bị cắt ngang dòng chữ.
3. **Cập nhật bộ kiểm thử tự động**:
   - Kiểm tra độ so khớp chính xác YCCĐ cho từng bài trong toàn bộ chương trình Toán 6 (Bài 1 đến Bài 43).
   - Kiểm tra chiến lược fallback 4 tầng khi gặp bài học tên mới/lạ không khớp CSDL.
   - Kiểm tra định dạng độ rộng cột trong file Word xuất ra khớp với bảng tỉ lệ chuẩn.

## Ngoài phạm vi
- Không chỉnh sửa văn bản gốc CTGDPT 2018 ban hành kèm Thông tư 32/2018/TT-BGDĐT.
- Không thay đổi các chức năng lưu CSDL và nhập liệu đã hoàn thiện.

## File dự kiến tác động
- `js/khbd-yccd.js` [NÂNG CẤP THUẬT TOÁN SO KHỚP TỪ KHÓA CHỦ ĐỀ, XỬ LÝ BÀI LUYỆN TẬP CHUNG/ÔN TẬP VÀ KHUNG YCCĐ SƯ PHẠM DỰ PHÒNG]
- `xaydungphuluc.html` [LOẠI BỎ FALLBACK INDEX NORMAL SAI LỆCH, TRIỂN KHAI CHIẾN LƯỢC 4 TẦNG, PHÂN BỔ TỈ LỆ CỘT CHUẨN TRONG DOCX]
- `tests/xaydungphuluc-smoke.js` [BỔ SUNG TEST CASE KHỚP YCCĐ BÀI 5, BÀI 6, TEST FALLBACK SƯ PHẠM VÀ TỈ LỆ ĐỘ RỘNG CỘT DOCX]
- `docs/handoff/PLAN.md` [GHI ĐÈ THEO QUY TRÌNH SURVEY]
- `docs/handoff/.lock` [GHI NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật khi nghiệm thu]

## Các bước thực hiện
1. **Bước 1: Nâng cấp hàm `findOfficialYccdRows` và `getCleanOfficialYccd` trong `js/khbd-yccd.js`**:
   - Bổ sung trích xuất từ khóa chủ đề (Semantic Topic Normalization).
   - Bổ sung nhận diện ngữ cảnh cho các bài "Luyện tập", "Luyện tập chung", "Ôn tập chương" dựa trên chủ đề của bài học trước đó.
   - Thêm hàm sinh khung YCCĐ sư phạm chuẩn theo loại bài (`generatePedagogicalOutcome(lesson, subject, grade)`).
2. **Bước 2: Cập nhật hàm `appendixOneTable` trong `xaydungphuluc.html`**:
   - Bỏ lệnh gán fallback nguy hiểm `|| generatedRows[normal]`.
   - Tìm kiếm bài học tương ứng trong `generatedRows` bằng so khớp mờ tên bài học (`cleanLessonName`).
   - Thực hiện kiểm tra tính phù hợp (Relevance Check): Nếu nội dung outcome do AI sinh không chứa từ khóa của bài học hoặc bị rỗng, lập tức áp dụng Chiến lược dự phòng 4 tầng (CSDL $\to$ SGK Context $\to$ Khung sư phạm).
3. **Bước 3: Chuẩn hóa tỉ lệ độ rộng cột trong `exportDocx` (`xaydungphuluc.html`)**:
   - Định nghĩa bảng tỉ lệ phần trăm cụ thể cho từng loại bảng (Phụ lục 1 Kế hoạch dạy học 5 cột, Phụ lục 1 Thiết bị/Phòng/KTĐG, Phụ lục 2, Phụ lục 3 PPCT 7 cột).
   - Truyền đúng thuộc tính `width: { size: colWidthPct, type: WidthType.PERCENTAGE }` cho từng `TableCell`.
   - Đặt `cantSplit: true` cho `TableRow` và `tableHeader: true` cho hàng tiêu đề.
4. **Bước 4: Cập nhật kiểm thử tự động trong `tests/xaydungphuluc-smoke.js`**:
   - Thêm test case kiểm tra bài "Bài 5: Phép nhân và phép chia số tự nhiên" nhận đúng YCCĐ về phép nhân/chia/luỹ thừa, không chứa từ khóa tập hợp/La Mã.
   - Thêm test case kiểm tra bài "Luyện tập chung" nhận đúng YCCĐ củng cố phép tính số tự nhiên.
   - Thêm test case kiểm tra fallback bài học lạ sinh đúng khung sư phạm tương ứng.
   - Thêm test case kiểm tra cấu hình độ rộng cột cho bảng Phụ lục 1 (5 cột) và Phụ lục 3 (7 cột) trong file Word.
5. **Bước 5: Khóa trạng thái giao việc**:
   - Ghi nội dung `LOCK` vào `docs/handoff/.lock`.

## Rủi ro
1. **Rủi ro tên bài học đặc thù của các bộ sách khác nhau (Cánh diều, Kết nối tri thức, Chân trời sáng tạo)**:
   - *Giải pháp*: Thuật toán chuẩn hóa tách lấy các từ khóa toán học cốt lõi (ví dụ: "phép nhân", "phép chia", "số tự nhiên", "ước chung", "bội chung", "hình bình hành"...) thay vì so khớp cứng toàn chuỗi, đảm bảo tương thích 100% với cả 3 bộ sách giáo khoa.
2. **Rủi ro bảng Word tràn lề trên một số phiên bản Word cũ**:
   - *Giải pháp*: Tổng tỉ lệ các cột trong mỗi bảng luôn được tính toán bằng đúng 100%, kết hợp lề trang 20mm chuẩn A4 ngang giúp bảng tự động khớp khít toàn trang in trên mọi phiên bản Word.

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - Chạy lệnh: `node tests/xaydungphuluc-smoke.js`
   - Chạy lệnh: `node tests/xaydungphuluc-integration-smoke.js`
2. **Kiểm thử thủ công**:
   - Mở `xaydungphuluc.html`:
     * Nạp bảng PPCT Toán 6 mẫu hoặc tải tệp 4 trang chụp.
     * Bấm Sinh Phụ lục 1 -> Kiểm tra cột "Yêu cầu cần đạt":
       - Bài 1, 2, 3: Chứa YCCĐ về tập hợp, số tự nhiên, chữ số La Mã.
       - Bài 4, 5, 6, 7: Chứa YCCĐ về phép cộng, trừ, nhân, chia, luỹ thừa, thứ tự thực hiện phép tính (không còn bị gán nhầm tập hợp).
       - Bài 8, 9, 10, 11, 12: Chứa YCCĐ về quan hệ chia hết, dấu hiệu chia hết, số nguyên tố, ước chung, bội chung.
       - Bài 18, 19, 20: Chứa YCCĐ về hình tam giác đều, hình vuông, lục giác đều, hình chữ nhật, hình thoi.
     * Thử thêm 1 bài tên lạ (vd: "Chuyên đề STEM mô hình toán học") -> Kiểm tra sinh ra khung YCCĐ sư phạm chuẩn, không lấy nhầm bài khác.
     * Xuất file Word Phụ lục 1 và Phụ lục 3 (`.docx`):
       - Mở file trong Microsoft Word: Khổ giấy chuẩn A4 Landscape.
       - Cột STT, Số tiết, Tuần nhỏ gọn (5–8%); Cột Yêu cầu cần đạt và Tên bài học rộng rãi (45–48%), canh chỉnh hoàn hảo, không bị tràn lề hay co dúm chữ.

## Tiêu chí nghiệm thu
- [x] 100% bài học trong Phụ lục 1 có Yêu cầu cần đạt khớp chính xác với tên bài và nội dung CTGDPT 2018 (triệt tiêu hoàn toàn lỗi "râu ông nọ cắm cằm bà kia").
- [x] Các bài Luyện tập chung, Ôn tập chương nhận đúng YCCĐ củng cố của chủ đề tương ứng.
- [x] Triển khai trọn vẹn Chiến lược dự phòng 4 tầng (CSDL $\to$ SGK $\to$ AI có kiểm chứng $\to$ Khung sư phạm theo thể loại bài), không bao giờ gán nhầm nội dung bài khác.
- [x] File Word (.docx) xuất ra chuẩn khổ A4 Landscape, các cột được phân bổ tỉ lệ độ rộng tối ưu theo nội dung thực tế (cột số ngắn 5–8%, cột nội dung chính 45–48%).
- [x] Đặt `cantSplit: true` và `tableHeader: true` cho các bảng trong file Word giúp ngắt trang chuẩn đẹp.
- [x] 100% các bài kiểm thử tự động chạy đạt PASS.
