# PLAN: Phân Rã Chi Tiết 100% YCCĐ Từng Bài Học (Toán 6 Bài 1–43), Theo Dõi Ngữ Cảnh Chương Cho Bài Ôn Tập & Chuẩn Hóa Gạch Đầu Dòng

## Hiện trạng
1. **Yêu cầu cần đạt bị dính dấu phẩy một dòng thay vì tách thành các gạch đầu dòng**:
   - Khi mảng YCCĐ được chuyển sang chuỗi qua phép gán mặc định hoặc khi AI trả về danh sách phân tách bằng dấu phẩy, hàm `formatOutcomeLines` chỉ tìm kiếm ký tự xuống dòng `\n- ` mà chưa phân tách các câu mục tiêu sư phạm nối bằng dấu phẩy.
   - Hậu quả: Nhiều bài xuất ra một đoạn văn bản dài liền tù tì: `Nhận biết được tập hợp các số tự nhiên,Biểu diễn được số tự nhiên trong hệ thập phân,Biểu diễn được các số tự nhiên từ 1 đến 30 bằng cách sử dụng các chữ số La Mã`.
2. **Bài Luyện tập chung, Ôn tập chương bị gán lệch mạch kiến thức (Số học bị gán sang Hình học)**:
   - Khi gặp bài "Luyện tập chung" hoặc "Ôn tập chương", hàm tìm kiếm `findOfficialYccdRows` chưa theo dõi chính xác ngữ cảnh Chương/Mục hiện tại mà chỉ dựa vào `previousLesson` cục bộ.
   - Khi điểm số khớp từ khóa chung (như `thực hành`, `bài tập`) của một bài hình học cao hơn, bài ôn tập số học bị gán nhầm sang YCCĐ hình học hoặc ngược lại.
3. **Các bài học liên tiếp trong cùng một chương vẫn bị trùng lặp nguyên khối YCCĐ**:
   - Trong `js/khbd-yccd.js`, mới chỉ có Bài 1–12 được override bóc tách. Toàn bộ các bài còn lại từ Bài 13 đến Bài 43 vẫn đang dùng chung các khối YCCĐ của cả chương:
     * Bài 13, 14, 15, 16, 17 (Chương Số nguyên): Cùng nhận chung khối 4–6 gạch đầu dòng về cả cộng, trừ, nhân, chia, dấu ngoặc, ước và bội số nguyên.
     * Bài 18, 19, 20 (Chương Hình học trực quan): Cùng nhận chung khối mô tả và vẽ tất cả các hình tam giác đều, hình vuông, lục giác đều, hình chữ nhật, hình thoi, hình thang.
     * Bài 23, 24, 25, 26, 27 (Chương Phân số): Cùng nhận chung khối về mở rộng phân số, so sánh, hỗn số và 4 phép tính.
     * Bài 28, 29, 30, 31 (Chương Số thập phân): Cùng nhận chung khối về số thập phân âm, tính toán, làm tròn và tỉ số phần trăm.
     * Bài 32, 33, 34, 35, 36, 37 (Chương Hình học phẳng): Cùng nhận chung khối về điểm, đường thẳng, tia, đoạn thẳng, trung điểm, góc và số đo góc.
     * Bài 38, 39, 40, 41 (Chương Thống kê): Cùng nhận chung khối về bảng thống kê, biểu đồ tranh, biểu đồ cột và cột kép.

## Phạm vi
1. **Chuẩn hóa toàn diện hàm `formatOutcomeLines`**:
   - Tự động nhận diện mảng, chuỗi nối bằng dấu phẩy `,` hoặc chấm phẩy `;` giữa các câu mục tiêu hành vi sư phạm (`Nhận biết`, `Biểu diễn`, `Thực hiện`, `Vận dụng`, `Mô tả`, `Giải thích`, `Tính`, `So sánh`, `Đọc`, `Xác định`, `Nêu`, `Lựa chọn`, `Tạo lập`, `Vẽ`, `Sử dụng`, `Làm quen`).
   - Luôn định dạng mỗi ý thành một dòng gạch đầu dòng riêng biệt `- [Nội dung mục tiêu].`
2. **Bộ theo dõi Ngữ cảnh Chương / Mạch kiến thức (Chapter & Domain Tracker)**:
   - Theo dõi xuyên suốt dòng tiêu đề chương (ví dụ: `CHƯƠNG I. SỐ TỰ NHIÊN`, `CHƯƠNG II. SỐ NGUYÊN`, `CHƯƠNG III. HÌNH HỌC TRỰC QUAN`, `CHƯƠNG IV. PHÂN SỐ VÀ SỐ THẬP PHÂN`, `CHƯƠNG V. MỘT SỐ YẾU TỐ HÌNH HỌC PHẲNG`, `CHƯƠNG VI. MỘT SỐ YẾU TỐ THỐNG KÊ VÀ XÁC SUẤT`).
   - Bài *Luyện tập chung / Ôn tập chương* ở chương nào thì chỉ nhận YCCĐ củng cố tổng hợp của đúng chương đó, tuyệt đối không bị nhảy sang mạch kiến thức khác.
3. **Phân rã chi tiết 100% YCCĐ cho từng bài học từ Bài 1 đến Bài 43 trong `js/khbd-yccd.js`**:
   - Cung cấp danh mục YCCĐ chuẩn xác, đúng phạm vi hạt nhân của từng bài học đơn lẻ:
     * **Bài 13**: Số nguyên âm, trục số, số đối, thứ tự số nguyên.
     * **Bài 14**: Phép cộng và phép trừ số nguyên, tính chất giao hoán/kết hợp.
     * **Bài 15**: Quy tắc dấu ngoặc trong tính toán số nguyên.
     * **Bài 16**: Phép nhân số nguyên, tính chất phân phối.
     * **Bài 17**: Phép chia hết, quan hệ chia hết, ước và bội của số nguyên.
     * **Bài 18**: Tam giác đều, hình vuông, lục giác đều (nhận dạng, mô tả yếu tố, vẽ).
     * **Bài 19**: Hình chữ nhật, hình thoi, hình bình hành, hình thang cân (mô tả yếu tố, vẽ).
     * **Bài 20**: Chu vi và diện tích các hình phẳng trong thực tiễn.
     * **Bài 21**: Trục đối xứng của hình phẳng.
     * **Bài 22**: Tâm đối xứng của hình phẳng.
     * **Bài 23**: Phân số có tử/mẫu âm, hai phân số bằng nhau.
     * **Bài 24**: Tính chất cơ bản của phân số, so sánh phân số, hỗn số dương.
     * **Bài 25**: Phép cộng và phép trừ phân số, quy tắc dấu ngoặc.
     * **Bài 26**: Phép nhân và phép chia phân số, tính chất phép tính.
     * **Bài 27**: Hai bài toán về phân số và ứng dụng thực tiễn.
     * **Bài 28**: Số thập phân âm, số đối, so sánh số thập phân.
     * **Bài 29**: Bốn phép tính với số thập phân.
     * **Bài 30**: Làm tròn và ước lượng số thập phân.
     * **Bài 31**: Tỉ số, tỉ số phần trăm và bài toán thực tiễn.
     * **Bài 32**: Điểm, đường thẳng, quan hệ điểm thuộc đường thẳng, 3 điểm thẳng hàng.
     * **Bài 33**: Điểm nằm giữa hai điểm, khái niệm tia.
     * **Bài 34**: Khái niệm đoạn thẳng, độ dài đoạn thẳng.
     * **Bài 35**: Trung điểm của đoạn thẳng.
     * **Bài 36**: Khái niệm góc, điểm trong của góc, các góc đặc biệt (vuông, nhọn, tù, bẹt).
     * **Bài 37**: Khái niệm số đo góc và đo góc bằng thước.
     * **Bài 38**: Thu thập và phân loại dữ liệu theo tiêu chí.
     * **Bài 39**: Bảng thống kê và biểu đồ tranh.
     * **Bài 40**: Biểu đồ cột và biểu đồ cột kép.
     * **Bài 42**: Mô hình xác suất trong trò chơi, thí nghiệm đơn giản.
     * **Bài 43**: Xác suất thực nghiệm và mô tả bằng phân số.
4. **Cập nhật bộ kiểm thử tự động**:
   - Kiểm tra định dạng đầu ra của `formatOutcomeLines` luôn trả về các dòng `- ` độc lập.
   - Kiểm tra toàn bộ 43 bài học Toán 6 và các bài Ôn tập chương nhận đúng YCCĐ riêng biệt, không có 2 bài học lý thuyết khác nhau bị trùng lặp YCCĐ.

## Ngoài phạm vi
- Không chỉnh sửa văn bản gốc CTGDPT 2018.
- Giữ nguyên các chức năng lưu CSDL và nhập liệu đã hoàn thiện.

## File dự kiến tác động
- `js/khbd-yccd.js` [MỞ RỘNG BÓC TÁCH CHI TIẾT TOÀN BỘ BÀI 1–43 VÀ THEO DÕI NGỮ CẢNH CHƯƠNG TOÁN 6–9]
- `xaydungphuluc.html` [NÂNG CẤP FORMATOUTCOMELINES BẺ DẤU PHẨY THÀNH GẠCH ĐẦU DÒNG, THEO DÕI CHAPTER CONTEXT TRONG APPENDIXONETABLE]
- `tests/xaydungphuluc-smoke.js` [BỔ SUNG TEST CASE CHO BÀI 13–17, 18–20, ÔN TẬP CHƯƠNG VÀ ĐỊNH DẠNG GẠCH ĐẦU DÒNG]
- `docs/handoff/PLAN.md` [GHI ĐÈ THEO QUY TRÌNH SURVEY]
- `docs/handoff/.lock` [GHI NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật khi nghiệm thu]

## Các bước thực hiện
1. **Bước 1: Nâng cấp hàm `formatOutcomeLines` trong `xaydungphuluc.html`**:
   - Nhận diện các câu mục tiêu bị dính dấu phẩy `,` hoặc mảng `[]`, tự động tách thành từng gạch đầu dòng riêng biệt `- ...`.
2. **Bước 2: Bổ sung toàn bộ bảng bóc tách YCCĐ chi tiết từ Bài 1 đến Bài 43 trong `js/khbd-yccd.js`**:
   - Cập nhật `KHBD_LESSON_YCCD_OVERRIDES` bao phủ đầy đủ 43 bài học của Toán 6.
   - Nâng cấp `findOfficialYccdRows` nhận diện tham số `chapterTopic` / `domain` để các bài Luyện tập chung, Ôn tập chương luôn lấy đúng YCCĐ củng cố của chương hiện hành.
3. **Bước 3: Nâng cấp `appendixOneTable` trong `xaydungphuluc.html`**:
   - Theo dõi tiêu đề chương hiện hành khi duyệt qua danh sách các dòng của PPCT nguồn.
   - Truyền ngữ cảnh chương vào hàm `cleanAppendixOutcome` cho các bài ôn tập/luyện tập.
4. **Bước 4: Cập nhật kiểm thử tự động trong `tests/xaydungphuluc-smoke.js`**:
   - Thêm test case cho Bài 13, Bài 14, Bài 15, Bài 16, Bài 17.
   - Thêm test case cho Bài 18, 19, 20.
   - Thêm test case cho bài Ôn tập chương I, Ôn tập chương III.
   - Thêm test case kiểm tra mọi đầu ra đều là định dạng gạch đầu dòng `- `.
5. **Bước 5: Khóa trạng thái giao việc**:
   - Ghi nội dung `LOCK` vào `docs/handoff/.lock`.

## Rủi ro
1. **Rủi ro các câu văn có dấu phẩy thông thường bên trong mệnh đề (ví dụ: "cộng, trừ, nhân, chia")**:
   - *Giải pháp*: Regex bẻ dòng chỉ bẻ ở dấu phẩy đứng TRƯỚC các động từ hành vi sư phạm viết hoa hoặc sau dấu chấm câu, giữ nguyên dấu phẩy liệt kê thuật ngữ bên trong câu.

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - Chạy lệnh: `node tests/xaydungphuluc-smoke.js`
   - Chạy lệnh: `node tests/xaydungphuluc-integration-smoke.js`
2. **Kiểm thử thủ công**:
   - Mở `xaydungphuluc.html`:
     * Bấm Sinh Phụ lục 1 $\to$ Kiểm tra:
       - Bài 1, Bài 2: Các ý được tách thành từng gạch đầu dòng `- ` rõ ràng, không dính dấu phẩy.
       - Bài 13 (Tập hợp số nguyên): Chỉ chứa YCCĐ số nguyên âm, trục số, số đối, thứ tự.
       - Bài 14 (Phép cộng trừ số nguyên): Chỉ chứa YCCĐ cộng trừ số nguyên.
       - Bài 15 (Quy tắc dấu ngoặc): Chỉ chứa YCCĐ quy tắc dấu ngoặc.
       - Bài 16 (Phép nhân số nguyên): Chỉ chứa YCCĐ phép nhân và tính chất phân phối.
       - Bài Ôn tập chương I / III: Nhận đúng YCCĐ củng cố số tự nhiên / số nguyên (không bị nhảy sang hình học).
     * Xuất file Word Phụ lục 1 và Phụ lục 3 $\to$ Kiểm tra văn bản chuẩn đẹp từng dòng.

## Tiêu chí nghiệm thu
- [x] 100% Yêu cầu cần đạt được định dạng thành các gạch đầu dòng `- ` rõ ràng, không còn hiện tượng dính dấu phẩy thành một dòng dài.
- [x] Phân rã chi tiết 100% YCCĐ cho toàn bộ 43 bài học Toán 6 (Bài 13 đến Bài 43 không còn bài nào bị dồn cụm giống nhau).
- [x] Các bài Luyện tập chung, Ôn tập chương nhận đúng YCCĐ củng cố của chương hiện hành theo mạch kiến thức Số học / Hình học / Thống kê.
- [x] 100% các bài kiểm thử tự động chạy đạt PASS.
