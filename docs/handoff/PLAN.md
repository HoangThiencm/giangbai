# PLAN: Bảo Toàn & Nhận Diện Chuẩn Xác Cột Số Tiết, Tiết CT & Tuần (Phân Cách Bằng Dấu Phẩy) Dạng Phân Môn Song Song (3 Số + 1 Hình)

## Hiện trạng
1. **Lỗi nhận diện và dồn tuần tuyến tính đơn dòng (Linear Serialization) thay vì song song (Parallel Branching)**:
   - Trong tài liệu Kế hoạch dạy học môn Toán THCS (và các môn tích hợp như KHTN, Lịch sử - Địa lí), PPCT thường được trình bày theo từng khối phân môn trong cùng một học kỳ:
     * **Học kì I**: Khối **1. SỐ HỌC 6** (50 tiết, phân bổ Tuần 1–18 với định mức 3 tiết/tuần) được trình bày trước; tiếp theo là khối **2. HÌNH HỌC 6** (22 tiết, phân bổ song song Tuần 1–18 với định mức 1 tiết/tuần).
     * **Học kì II**: Khối **PHÂN SỐ, SỐ THẬP PHÂN, DỮ LIỆU & XÁC SUẤT** (51 tiết, Tuần 19–35, 3 tiết/tuần) và khối **HÌNH HỌC CƠ BẢN** (17 tiết, Tuần 19–35, 1 tiết/tuần).
   - Khi hệ thống `xaydungphuluc.html` nhận diện từ 4 bức ảnh/tệp PDF hoặc khi hàm `recalculatePpctSequences()` chạy:
     * Hệ thống mặc định gộp tuyến tính tuần tự từ trên xuống dưới (4 tiết/tuần liên tục từ dòng 1 đến N).
     * Hậu quả: 50 tiết Số học bị ép vào Tuần 1–13 (Bài 4 ở Tuần 2 bị dồn về Tuần 1); 22 tiết Hình học bị đẩy lùi sang Tuần 13–18 thay vì bắt đầu từ Tuần 1 song song với Số học.
2. **Quy ước định dạng Tiết CT và Tuần (Số nguyên phân cách bằng dấu phẩy `","`) chưa được áp dụng nhất quán**:
   - Các tiết trong cột "Tiết CT" và các tuần trong cột "Tuần" bản chất là các số nguyên.
   - Khi một bài học có nhiều tiết hoặc nhiều tuần (ví dụ: tiết 14, 15 hoặc tiết 25, 26, 27; tuần 6, 7 hoặc tuần 11, 12, 13), quy ước chuẩn phải phân cách bằng dấu phẩy `","` (dạng `14, 15`, `25, 26, 27`, `6, 7`, `11, 12`).
   - Hiện tại hàm bóc tách đôi khi dùng dấu gạch ngang, khoảng trắng hoặc ngắt dòng không đồng bộ dẫn đến việc nhận diện và tính toán sai lệch.
3. **Hàm `recalculatePpctSequences` tự động ghi đè làm mất dữ liệu Tuần & Tiết CT gốc**:
   - Mỗi khi thêm dòng, xóa dòng, sửa số tiết (`updatePpctLessonPeriods`) hoặc di chuyển dòng, hàm `recalculatePpctSequences` tự động chạy và tính lại `tietCT = 1..N` cùng `week = Math.ceil(period / 4)` đơn luồng, xóa sạch số tuần và số tiết CT do người dùng nhập hoặc do tệp gốc cung cấp.
4. **Bug gọi nhầm hàm chuẩn hóa `normalizeWeek` cho `tietCT`**:
   - Tại dòng 105 (`extractPpctRowsFromTable`) và dòng 124 (`extractPpctRows`), biến `obj.tietCT` đang bị gán bằng `normalizeWeek(obj.tietCT)` thay vì `formatTietCT(obj.tietCT)`.
5. **Prompt nhận diện AI (`ppctRecognitionPrompt`) chưa ràng buộc chặt chẽ bảo toàn số tuần phân môn song song**:
   - Prompt chưa nhấn mạnh quy tắc: khi bảng nguồn có các phân môn song song (Số học và Hình học cùng bắt đầu từ Tuần 1, hoặc KHTN Lý/Hóa/Sinh, Sử/Địa), AI phải giữ nguyên 100% giá trị cột `Số tiết`, `Tiết CT` và `Tuần` của từng dòng bài học, tuyệt đối không tự ý cộng dồn tuần nối tiếp.

## Phạm vi
1. **Bảo toàn tuyệt đối dữ liệu Số tiết, Tiết CT & Tuần từ tệp nguồn (PDF, DOCX, XLSX, Ảnh OCR, AI JSON)**:
   - Giữ nguyên vẹn 100% giá trị các cột `Số tiết`, `Tiết CT` và `Tuần` do tệp nguồn hoặc AI nhận diện đọc được.
   - Định dạng chuẩn: Các số nguyên phân cách bằng dấu phẩy `","` kèm dấu cách (ví dụ: Tiết CT `5, 6` hoặc `14, 15`; Tuần `6, 7` hoặc `11, 12`).
   - Không tự động đè tuần tuyến tính khi nạp tệp hay khi chỉnh sửa nội dung khác.
   - Cho phép người dùng chỉnh sửa tay (Inline Edit) tự do từng ô `Số tiết`, `Tuần` và `Tiết CT` ở Mục 3 mà không bị hệ thống tự ý tính lại đè mất.
2. **Nâng cấp thuật toán `recalculatePpctSequences` hỗ trợ Phân môn song song (Parallel Branching / Sub-subject Partitioning)**:
   - Nhận diện các điểm mốc phân môn và học kỳ:
     * Dòng tiêu đề phân môn: `1. SỐ HỌC`, `2. HÌNH HỌC`, `ĐẠI SỐ`, `HÌNH HỌC`, `VẬT LÍ`, `HÓA HỌC`, `SINH HỌC`, `LỊCH SỬ`, `ĐỊA LÍ`.
     * Dòng tiêu đề học kì: `HỌC KÌ I` (Tuần 1–18), `HỌC KÌ II` (Tuần 19–35).
   - Khi kích hoạt tính lại:
     * Cho phép nhận diện cấu trúc phân môn: Số học chạy theo định mức 3 tiết/tuần (Tuần 1..18, Tiết CT 1..50); Hình học chạy song song theo định mức 1 tiết/tuần (Tuần 1..18, Tiết CT 1..22).
     * Học kì II: Số học/Thống kê chạy Tuần 19..35 (Tiết CT 51..101); Hình học chạy Tuần 19..35 (Tiết CT 23..39).
     * Xuất chuỗi Tiết CT và Tuần dạng số nguyên phân cách dấu phẩy chuẩn (`1, 2, 3`, `14, 15`, `6, 7`).
     * Chỉ tính lại khi người dùng bấm nút `🔄 Tính lại Tiết CT & Tuần tự động` hoặc cung cấp tùy chọn rõ ràng (Tính tuyến tính / Tính theo phân môn song song).
3. **Cập nhật Prompt AI nhận diện PPCT (`ppctRecognitionPrompt`)**:
   - Bổ sung chỉ dẫn đặc thù:
     * Đọc chính xác số nguyên của cột `Số tiết`, `Tiết CT`, `Tuần` từ từng ô.
     * Khi có nhiều tiết/tuần trong 1 bài, phân cách bằng dấu phẩy (ví dụ: `"tietCT": "14, 15"`, `"week": "6, 7"`).
     * Bảo toàn nguyên vẹn số tuần và tiết CT của từng phân môn song song (Số học và Hình học cùng chạy Tuần 1–18; không tự ý dồn tuần Số trước Hình sau).
4. **Sửa các lỗi bóc tách chuỗi và chuẩn hóa dữ liệu**:
   - Sửa `normalizeWeek(obj.tietCT)` thành `formatTietCT(obj.tietCT)` trong `extractPpctRowsFromTable` và `extractPpctRows`.
   - Nâng cấp hàm `formatWeek` và `formatTietCT` để chuẩn hóa các số nguyên phân cách bằng dấu phẩy `","` (dạng `14, 15`, `6, 7`, `25, 26, 27`).
5. **Cập nhật bộ kiểm thử tự động**:
   - Kiểm thử bóc tách PPCT Toán 6 dạng 3 Số + 1 Hình bảo toàn đúng Tuần 1..18 cho cả 2 phân môn Số học và Hình học.
   - Kiểm thử định dạng số nguyên phân cách bằng dấu phẩy cho các tiết đôi/ba và tuần kép.

## Ngoài phạm vi
- Không can thiệp cấu trúc mã năng lực số (CV 3456) và mã AI (QĐ 2422).
- Không thay đổi các phụ lục khác ngoài `xaydungphuluc.html`.

## File dự kiến tác động
- `xaydungphuluc.html` [CHUẨN HÓA DẤU PHẨY CHO TIẾT CT & TUẦN, SỬA LỖI NORMALIZE TIETCT, NÂNG CẤP RECALCULATE HỖ TRỢ PHÂN MÔN SONG SONG, CẬP NHẬT PROMPT AI PPCT, BẢO TOÀN DỮ LIỆU NGUỒN]
- `tests/xaydungphuluc-smoke.js` [BỔ SUNG TEST CASE PPCT 3 SỐ + 1 HÌNH, ĐỊNH DẠNG DẤU PHẨY CHO TIẾT/TUẦN, PHÂN MÔN SONG SONG, BẢO TOÀN TUẦN VÀ TIẾT CT]
- `docs/handoff/PLAN.md` [GHI ĐÈ THEO QUY TRÌNH SURVEY]
- `docs/handoff/.lock` [GHI NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật khi nghiệm thu]

## Các bước thực hiện
1. **Bước 1: Chuẩn hóa định dạng số nguyên phân cách bằng dấu phẩy cho Tiết CT và Tuần trong `xaydungphuluc.html`**:
   - Cập nhật hàm `formatTietCT(value)`: Trích xuất các số nguyên và nối bằng `", "` (ví dụ `14, 15`, `25, 26, 27`).
   - Cập nhật hàm `formatWeek(value)`: Trích xuất các số nguyên tuần và nối bằng `", "` (ví dụ `6, 7`, `11, 12`).
   - Sửa bug `normalizeWeek(obj.tietCT)` thành `formatTietCT(obj.tietCT)` tại dòng 105 (`extractPpctRowsFromTable`) và dòng 124 (`extractPpctRows`).
2. **Bước 2: Nâng cấp `ppctRecognitionPrompt` trong `xaydungphuluc.html`**:
   - Thêm quy tắc nhận diện: Đối với các môn có phân môn song song (như Toán gồm Số học & Hình học, KHTN gồm Lý/Hóa/Sinh, Sử - Địa), AI phải đọc chính xác số nguyên của Số tiết, Tiết CT và Tuần từ từng ô của bảng nguồn (dùng dấu `","` ngăn cách); không được tự dồn tuần nối tiếp.
3. **Bước 3: Tối ưu cơ chế bảo toàn dữ liệu & nâng cấp `recalculatePpctSequences`**:
   - Tách biệt rõ giữa việc "nhập/sửa dữ liệu người dùng" và "tính lại tự động":
     * Khi sửa số tiết bài học (`updatePpctLessonPeriods`), chỉ cập nhật số tiết của bài đó, không tự động đè mất các ô Tuần đã có sẵn từ tệp nguồn.
     * Nâng cấp hàm `recalculatePpctSequences`: Nhận diện các nhóm/phân môn (`HỌC KÌ I`, `HỌC KÌ II`, `1. SỐ HỌC`, `2. HÌNH HỌC`, v.v.). Khi phát hiện cấu trúc phân môn song song (Toán 6–9: Số học 3 tiết/tuần, Hình học 1 tiết/tuần), tự động tính đúng Tiết CT luỹ kế và Số tuần song song (Tuần 1–18 cho HKI, Tuần 19–35 cho HKII), định dạng các số nguyên phân cách bằng dấu phẩy.
4. **Bước 4: Chuẩn hóa hiển thị ô Tuần và Tiết CT trên bảng và khi xuất Word**:
   - Đảm bảo các ô chứa nhiều tiết/tuần (dạng `14, 15` hoặc `6, 7`) hiển thị chuẩn xác, không bị lỗi dính chữ khi render HTML và khi xuất file Word (.docx).
5. **Bước 5: Cập nhật kiểm thử tự động trong `tests/xaydungphuluc-smoke.js`**:
   - Viết test case giả lập dữ liệu PPCT Toán 6 đầy đủ 4 trang (3 Số + 1 Hình) với 2 phân môn Số học & Hình học chạy song song Tuần 1–18 và Tuần 19–35.
   - Kiểm tra định dạng số nguyên phân cách bằng dấu phẩy `","` cho cả Tiết CT và Tuần.
   - Kiểm tra `extractPpctRowsFromTable`, `normalizeRecognizedPpct`, và `recalculatePpctSequences` bảo toàn chuẩn xác số tuần và tiết CT.
6. **Bước 6: Khóa trạng thái giao việc**:
   - Ghi nội dung `LOCK` vào `docs/handoff/.lock`.

## Rủi ro
1. **Rủi ro các môn học một mạch (như Tin học, Công nghệ 1 tiết/tuần) bị ảnh hưởng bởi thuật toán phân môn**:
   - *Giải pháp*: Thuật toán kiểm tra tên môn học và tiêu đề nhóm: nếu là môn đơn phân môn thì tính tuần tự 1 luồng chuẩn (35 tuần); nếu có tiêu đề phân môn (`SỐ HỌC`, `HÌNH HỌC`, `VẬT LÍ`, `HÓA HỌC`, `SINH HỌC`) thì áp dụng phân bổ song song tương ứng.
2. **Rủi ro người dùng muốn giữ nguyên số tuần đặc thù của trường không theo chuẩn**:
   - *Giải pháp*: Ưu tiên hàng đầu là **giữ nguyên 100% dữ liệu tệp nguồn tải lên** và dữ liệu chỉnh tay của giáo viên; chỉ tính toán lại khi người dùng bấm nút yêu cầu.

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - Chạy lệnh: `node tests/xaydungphuluc-smoke.js`
   - Chạy lệnh: `node tests/xaydungphuluc-integration-smoke.js`
2. **Kiểm thử thủ công**:
   - Mở `xaydungphuluc.html`:
     * Tải tệp PPCT Toán 6 có phân môn Số học (50 tiết) và Hình học (22 tiết).
     * Kiểm tra Bảng tại Mục 3:
       - Các bài có nhiều tiết: Tiết CT hiển thị dạng số nguyên phân cách bằng dấu phẩy (vd: `5, 6`, `14, 15`, `25, 26, 27`).
       - Các bài trải nhiều tuần: Tuần hiển thị dạng số nguyên phân cách bằng dấu phẩy (vd: `6, 7`, `11, 12`).
       - Phần Số học: Bài 1, 2, 3 ở Tuần 1; Bài 4 ở Tuần 2; Bài 5 ở Tuần 2... đến Tuần 18 (Tiết 50).
       - Phần Hình học: Bài 18 bắt đầu từ Tuần 1 (Tiết CT 1) và Tuần 2 (Tiết CT 2), trải dài đến Tuần 18 (Tiết CT 22).
       - Không còn hiện tượng Bài 4 bị dồn vào Tuần 1 hoặc Hình học bị đẩy sang Tuần 13–18.
     * Sửa số tiết hoặc chỉnh sửa ô bất kỳ -> Dữ liệu tuần của các bài khác không bị mất hoặc đảo lộn.
     * Xuất file Word Phụ lục 1, Phụ lục 3 -> Kiểm tra bảng in hiển thị đúng số tuần và tiết CT song song phân cách bằng dấu phẩy.

## Tiêu chí nghiệm thu
- [x] Nhận diện PPCT từ PDF/Word/Excel bảo toàn 100% cột `Số tiết`, `Tuần` và `Tiết CT` từ tệp gốc, không tự ý dồn tuần tuyến tính làm sai lệch cấu trúc 3 Số + 1 Hình.
- [x] Quy ước Tiết CT và Tuần gồm các số nguyên phân cách bằng dấu phẩy `","` (dạng `14, 15`, `6, 7`) được áp dụng nhất quán từ nhận diện, hiển thị đến xuất Word.
- [x] Đã sửa lỗi gọi nhầm `normalizeWeek` cho biến `tietCT` trong các hàm trích xuất bảng.
- [x] Thuật toán `recalculatePpctSequences` hỗ trợ thông minh cấu trúc phân môn song song (Số học 3 tiết/tuần, Hình học 1 tiết/tuần) khi phân bổ Tuần 1–18 và Tuần 19–35.
- [x] Cho phép giáo viên chỉnh sửa thủ công trực tiếp trên các ô `Tuần` và `Tiết CT` mà không bị ghi đè tự động ngoài ý muốn.
- [x] 100% các bài kiểm thử tự động trong `tests/xaydungphuluc-smoke.js` và `tests/xaydungphuluc-integration-smoke.js` chạy đạt kết quả PASS.
