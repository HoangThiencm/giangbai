# PLAN: Rà Soát & Chuẩn Hóa Mô Tả NLS & AI Trong `canvas_xaydungphuluc`

## 1. Bối cảnh & Hiện trạng Khảo sát (Survey Findings)

Khảo sát toàn bộ hệ thống sinh và làm giàu mô tả NLS & AI trong `canvas_xaydungphuluc.html` và `xaydungphuluc.html` đã phát hiện **4 nhóm vấn đề nghiêm trọng**:

### Vấn đề 1: Trùng lặp mô tả giữa các mã NLS khác chức năng (NLS Code Conflation & Duplication)
- Trong hàm `lessonAppliedNlsFallback` (dùng cho các phân môn và trường hợp phi-Toán) và `lessonAppliedNlsDescription`:
  - **Nhóm 5 (Giải quyết vấn đề)**: Các mã `5.1` (Xử lý sự cố kỹ thuật), `5.2` (Xác định nhu cầu và giải pháp công nghệ), `5.3` (Sử dụng sáng tạo công nghệ số), `5.4` (Tự phát hiện khoảng trống năng lực số) đều bị gộp chung vào một điều kiện `c.startsWith('5.3')||c.startsWith('5.2')||c.startsWith('5.')` và trả về câu mô tả giống hệt nhau:
    `"Sử dụng ${kit.tool} để ${kit.practice} trong bài ${title}; học sinh đối chiếu với SGK và hoàn thành sản phẩm học tập."`
  - **Nhóm 1 (Khai thác dữ liệu)**: Mã `1.1` (Tìm kiếm, lọc dữ liệu) và `1.3` (Quản lý, lưu trữ, tổ chức dữ liệu số) cùng bị gộp chung một mô tả khai thác học liệu.
  - **Nhóm 2 (Giao tiếp & hợp tác)**: Cả 6 mã từ `2.1` đến `2.6` (Tương tác, Chia sẻ, Trách nhiệm công dân, Hợp tác, Văn hóa ứng xử mạng, Quản lý danh tính số) đều rơi vào `c.startsWith('2.')` và trả về cùng một câu chia sẻ học tập.
  - **Nhóm 3 (Sáng tạo nội dung số)**: Các mã `3.1` (Phát triển nội dung), `3.2` (Tái tạo/tích hợp), `3.3` (Bản quyền số), `3.4` (Lập trình/tự động hóa) bị gộp chung vào mô tả sơ đồ hóa của 3.1.
  - **Nhóm 4 (An toàn)**: Các mã `4.1` (Bảo vệ thiết bị/phần cứng/phần mềm), `4.2` (Bảo vệ dữ liệu cá nhân & quyền riêng tư), `4.4` (Bảo vệ môi trường số) bị gộp chung một mô tả.
- **Hậu quả thực tế**: Khi một bài học được chọn 2 mã NLS (ví dụ `5.2.TC1a` và `5.3.TC1a`, hoặc `1.1.TC1a` và `1.3.TC1a`), bảng PPCT xuất hiện 2 dòng **hoàn toàn giống hệt nhau từng chữ**, vi phạm nguyên tắc sư phạm và không phân biệt được mục tiêu của từng năng lực thành phần theo Thông tư 02/2025/TT-BGDĐT & Công văn 3456/BGDĐT-GDPT.

### Vấn đề 2: Trùng lặp mô tả giữa các mã AI khác chức năng (AI Code Conflation & Duplication)
- Trong `lessonAppliedAiFallback`:
  - Đối với các môn phi-Tin học, hệ thống ép chuyển toàn bộ mã Miền A sang Miền B (`if(!isInformaticsSubject(subject)&&domain==='A') domain='B'`).
  - Sau đó, toàn bộ các mã Miền B (gồm 13 mã độc lập từ lớp 6 đến lớp 9: `6.B1.1`, `6.B2.1`, `7.B2.1`, `7.B2.2`, `7.B3.1`, `8.B1.1`, `8.B2.1`, `8.B3.1`, `9.B2.1`, `9.B2.2`, `9.B2.3`, `9.B3.1`, `9.B3.2`) **đều bị ép trả về duy nhất 1 câu mẫu môn học bị gán cứng**:
    + Trong Vật lí: Tất cả mã Miền B đều biến thành câu *"Sử dụng trợ lý AI gợi mở cách tiếp cận, giải thích hiện tượng vật lí và gợi ý các bước làm thí nghiệm..."*.
    + Trong Hoá học: Tất cả mã Miền B đều biến thành câu *"Sử dụng trợ lý AI hỗ trợ tra cứu phương trình hoá học, giải thích tính chất chất và kiểm tra bước tính toán..."*.
    + Trong Lịch sử: Tất cả mã Miền B đều biến thành câu *"Sử dụng trợ lý AI tra cứu bối cảnh lịch sử, gợi ý câu hỏi tìm hiểu bài..."*.
    + Trong Địa lí: Tất cả mã Miền B đều biến thành câu *"Sử dụng trợ lý AI hỗ trợ tìm kiếm số liệu địa lí, gợi mở phân tích biểu đồ..."*.
  - Toàn bộ Miền C (24 mã về thuật toán, dữ liệu huấn luyện, mô hình) trả về duy nhất 1 câu dự án chung.
  - Toàn bộ Miền D (19 mã về thiết kế, giải quyết vấn đề, đánh giá sản phẩm) trả về duy nhất 1 câu đánh giá độ tin cậy chung.
- **Hậu quả thực tế**:
  - Mã `7.B3.1` (YCCĐ: *Thể hiện việc khai báo trung thực khi có sử dụng AI trong sản phẩm học tập*) bị mất hoàn toàn nội hàm "khai báo trung thực", biến thành câu "làm thí nghiệm" hoặc "tra cứu bối cảnh".
  - Mã `8.B1.1` (YCCĐ: *Nhận diện rủi ro thuật toán thiên vị hoặc nội dung lừa đảo giả mạo do AI tạo ra*) bị mất nội hàm nhận diện rủi ro và deepfake.
  - Mã `9.B2.3` (YCCĐ: *Phân tích dấu hiệu nội dung giả mạo do AI tạo ra; đề xuất cách ứng phó*) bị mất nội hàm phát hiện giả mạo.
  - Mã `8.B2.1` (YCCĐ: *Bảo vệ dữ liệu cá nhân, tôn trọng bản quyền khi dùng AI*) bị biến thành câu chung chung.

### Vấn đề 3: Bắt nhầm môn Toán cho các môn học khác (Math Keyword Hijacking)
- Trong `lessonAppliedNlsDescription` và `lessonAppliedAiDescription`, biến `isMath` được xác định bằng:
  `const isMath = isEquation || isFunction || isPoly || isArith || isGeo || isStat || isExperiential || /toan/i.test(mathHay);`
  Đoạn mã này **không hề kiểm tra môn học thực tế** (`subjectName`), mà chỉ dựa vào regex tìm từ khóa trong tên bài học.
- Các regex tìm từ khóa toán học bị viết lỏng lẻo (thiếu ranh giới từ `\b` hoặc bắt các cụm từ phổ thông tiếng Việt):
  1. `/goc/` (dự định bắt "góc" trong hình học) bắt nhầm chữ "nguồn gốc" trong **Lịch sử 6: Bài 4. Nguồn gốc loài người** -> bài Lịch sử bị biến thành bài hình học (mô tả: dùng phần mềm GeoGebra dựng hình, vẽ thêm yếu tố phụ, áp dụng định lý)!
  2. `/tu giac/` (dự định bắt "tứ giác") bắt nhầm chữ "tự giác" trong **GDCD 7: Bài 3. Học tập tự giác, tích cực** -> bài GDCD bị biến thành bài chứng minh hình học!
  3. `\bnghiem\b` (dự định bắt "nghiệm" phương trình) bắt nhầm chữ "trải nghiệm" trong **Ngữ văn 7: Bài 8. Trải nghiệm để trưởng thành** -> bài Ngữ văn bị biến thành bài giải phương trình/hệ phương trình đại số!
  4. `/do thi/` (dự định bắt "đồ thị" hàm số) bắt nhầm chữ "đô thị" trong **Lịch sử 7, 9 & Địa lí 7, 9: Đô thị: Lịch sử và hiện tại** -> bài Lịch sử/Địa lí bị gán mô tả vẽ đồ thị hàm số và bấm máy tính Casio!
  5. `/so nguyen/` (dự định bắt "số nguyên") bắt nhầm chữ "nguyên liệu" trong **Hoá học 6: Bài 13. Một số nguyên liệu** -> bài Hoá học bị gán mô tả thực hành tính toán trên tia số/trục số!
  6. `/phuong trinh/` (dự định bắt "phương trình đại số") bắt nhầm "phương trình hoá học" trong **Hoá học 8: Bài 5, 6** -> bài Hoá học bị gán mô tả bấm Casio giải hệ phương trình SIMULT và dùng phương pháp thế/cộng đại số!
  7. Quét `toan` không có ranh giới từ bắt nhầm chữ "toàn cầu", "toàn phần" trong **Vật lí 9 (Phản xạ toàn phần)**, **Lịch sử 9 (xu thế toàn cầu hoá)**, **Tin học 6 (Mạng thông tin toàn cầu)** -> biến tất cả thành môn Toán!
- Quét thực tế trên toàn bộ chương trình THCS phát hiện **hơn 52 bài học thuộc các môn phi-Toán** bị dính lỗi hiển thị mô tả Toán học này.

### Vấn đề 4: Nội dung công cụ và hành vi sư phạm chưa sát với đặc thù từng môn
- Hiện tại `nlsSubjectToolkit` chỉ định nghĩa một công cụ duy nhất `tool` và một hành động `practice` cho toàn bộ môn học, không thay đổi theo mục tiêu từng bài hay từng mã năng lực.
- Cần bộ công cụ số và hành vi chuẩn xác cho từng nhóm môn:
  - **Vật lí**: Cảm biến đo số, video thí nghiệm mô phỏng PhET, phần mềm đồ thị động lực học, xử lý sai số đo đạc thực nghiệm.
  - **Hoá học**: Bảng tuần hoàn tương tác số (Ptable), mô hình phân tử 3D, cân bằng và mô phỏng phản ứng hoá học, tra cứu an toàn hoá chất (MSDS).
  - **Sinh học**: Kính hiển vi kỹ thuật số, học liệu mô phỏng 3D tế bào/cơ quan/quá trình sinh học, phần mềm phân loại và định danh sinh vật.
  - **Lịch sử**: Bản đồ/lược đồ lịch sử số, bảo tàng ảo 3D, kho tư liệu số chính thống, đối chiếu và trích dẫn nguồn sử liệu số.
  - **Địa lí**: Bản đồ số, Google Earth, hệ thống thông tin địa lí (GIS), biểu đồ thời tiết khí hậu tương tác.
  - **Ngữ văn**: Học liệu số văn học, từ điển số, sơ đồ tư duy phân tích tác phẩm, không gian học tập chia sẻ bài viết/hùng biện.
  - **Tin học**: Môi trường lập trình, phần mềm xử lý văn bản/bảng tính/trình chiếu, công cụ quản trị dữ liệu và thuật toán số.
  - **Công nghệ, GDCD, Ngoại ngữ, Âm nhạc, Mĩ thuật, GDTC, HĐTN-HN**: Tương thích theo đặc thù môn.

---

## 2. Kế hoạch Giải pháp Kỹ thuật

### 2.1. Chuẩn hóa Định danh Môn học & Chấm dứt Tình trạng "Bắt nhầm môn Toán"
1. **Ưu tiên kiểm tra môn học thực tế (`subjectName`)**:
   - Chỉ kích hoạt các nhánh mô tả Toán học (Đại số, Hình học, Số học, Giải phương trình...) khi `foldSubjectName(subjectName)` thực sự là môn Toán:
     `const isActualMath = /toan|toan hoc/i.test(foldSubjectName(subjectName));`
   - Nếu môn học không phải là Toán (Vật lí, Hoá học, Sinh học, Lịch sử, Địa lí, Ngữ văn, GDCD, Tin học...): **Tuyệt đối không chạy logic nhận diện toán học**.
2. **Sửa toàn bộ regex nhận diện phân môn Toán có ranh giới từ chặt chẽ**:
   - `isEquation`: Phải kiểm tra `/\b(phuong trinh|he phuong trinh|bat phuong trinh)\b/i` VÀ loại trừ rõ ràng `/hoa hoc|phan ung/i`.
   - `isGeo`: Phải dùng `/\b(hinh hoc|doan thang|tam giac|tu giac|duong tron|goc vuong|goc nhon|goc tu|hinh vuong|hinh chu nhat|hinh thang|hinh binh hanh|hinh thoi|lang tru|hinh hop|hinh lap phuong|thales|pythagore)\b/i`. Không dùng `/goc/` trơ trọi (tránh `nguồn gốc`); không dùng `tu giac` không biên từ (tránh `tự giác`).
   - `isFunction`: Phải dùng `/\b(ham so|do thi ham so|parabol|he so goc|toa do)\b/i`. Không dùng `/do thi/` đơn lẻ (tránh `đô thị`).
   - `isArith`: Phải dùng `/\b(so tu nhien|so nguyen|phan so|so thap phan|so huu ti|so thuc|so vo ti)\b/i`. Không để `so nguyen` khớp với `nguyên liệu`.
   - `isSolvingEq`: Phải kiểm tra rõ ràng `/\bnghiem cua phuong trinh|giai he phuong trinh|giai phuong trinh|phuong phap the|cong dai so\b/i`. Loại trừ từ `trải nghiệm`.

### 2.2. Ma trận Mô tả NLS Độc lập theo Từng Mã (TT 02/2025 & CV 3456)
Thay thế cơ chế gộp nhóm bằng bảng ánh xạ hành vi sư phạm riêng biệt cho từng mã NLS:

- **1.1.TC1a/TC2a** (Duyệt, tìm kiếm, lọc dữ liệu/thông tin số):
  `Khai thác và chọn lọc học liệu số, tư liệu hình ảnh/video trực quan phục vụ tìm hiểu bài ${title}; đối chiếu với SGK.`
- **1.2.TC1a/TC2a** (Đánh giá dữ liệu/thông tin số):
  `Đánh giá độ tin cậy, tính chính xác và tính phù hợp của dữ liệu/thông tin số thu thập được khi học bài ${title}.`
- **1.3.TC1a/TC2a** (Quản lý dữ liệu/thông tin số):
  `Tổ chức, lưu trữ và sắp xếp có cấu trúc các tệp tài liệu, bảng số liệu hoặc sản phẩm học tập số của bài ${title}.`
- **2.1.TC1a/TC2a** (Tương tác thông qua công nghệ số):
  `Sử dụng các kênh và công cụ số tương tác để trao đổi, thảo luận nhiệm vụ học tập bài ${title}.`
- **2.2.TC1a/TC2a** (Chia sẻ thông tin và nội dung qua công nghệ số):
  `Chia sẻ kết quả bài tập, dữ liệu quan sát hoặc sản phẩm học tập nhóm qua không gian số trong bài ${title}.`
- **2.3.TC1a/TC2a** (Thực hiện trách nhiệm công dân số):
  `Thể hiện trách nhiệm và ý thức công dân số khi tham gia các hoạt động học tập và đóng góp nội dung bài ${title}.`
- **2.4.TC1a/TC2a** (Hợp tác thông qua công nghệ số):
  `Phối hợp làm việc nhóm trên nền tảng số để cùng xây dựng và hoàn thiện sản phẩm học tập bài ${title}.`
- **2.5.TC1a/TC2a** (Quy tắc ứng xử trên mạng - Netiquette):
  `Thực hiện quy tắc giao tiếp lịch sự, tôn trọng ý kiến thành viên khi thảo luận trực tuyến bài ${title}.`
- **2.6.TC1a/TC2a** (Quản lý danh tính số):
  `Có ý thức bảo vệ danh tính số và hình ảnh cá nhân khi tham gia học tập số bài ${title}.`
- **3.1.TC1a/TC2a** (Phát triển nội dung số):
  `Sử dụng công cụ số (sơ đồ tư duy, bài trình chiếu, bảng biểu số) để thiết kế và trình bày sản phẩm bài ${title}.`
- **3.2.TC1a/TC2a** (Tích hợp và tạo lại nội dung số):
  `Kết hợp, chỉnh sửa và tái cấu trúc các nguồn học liệu số (chữ, hình ảnh, âm thanh) thành sản phẩm mới bài ${title}.`
- **3.3.TC1a/TC2a** (Thực thi bản quyền và giấy phép):
  `Trích dẫn rõ ràng nguồn gốc học liệu số, hình ảnh và tư liệu khai thác phục vụ bài ${title}, tôn trọng bản quyền.`
- **3.4.TC1a/TC2a** (Lập trình / Tự động hóa):
  `Thiết kế thuật toán, viết mã lệnh hoặc sử dụng công cụ mô phỏng số giải quyết nhiệm vụ bài ${title}.`
- **4.1.TC1a/TC2a** (Bảo vệ thiết bị số):
  `Tuân thủ quy trình vận hành an toàn, bảo vệ thiết bị số và phòng chống mã độc khi học bài ${title}.`
- **4.2.TC1a/TC2a** (Bảo vệ dữ liệu cá nhân & quyền riêng tư):
  `Bảo mật tài khoản học tập, không chia sẻ thông tin cá nhân của bản thân và bạn học khi học bài ${title}.`
- **4.3.TC1a/TC2a** (Bảo vệ sức khỏe và an sinh số):
  `Thực hiện quy tắc an toàn thị giác (20-20-20), điều chỉnh tư thế và ánh sáng hợp lý khi học tập với thiết bị số bài ${title}.`
- **4.4.TC1a/TC2a** (Bảo vệ môi trường công nghệ):
  `Có ý thức tiết kiệm năng lượng khi sử dụng thiết bị số và hiểu tác động môi trường của thiết bị công nghệ bài ${title}.`
- **5.1.TC1a/TC2a** (Giải quyết vấn đề kỹ thuật):
  `Nhận biết, chẩn đoán và xử lý các sự cố kỹ thuật thông thường (lỗi nhập liệu, lỗi kết nối, hiển thị lỗi) khi học bài ${title}.`
- **5.2.TC1a/TC2a** (Xác định nhu cầu và giải pháp công nghệ):
  `Lựa chọn công cụ số, phần mềm chuyên dụng hoặc nguồn học liệu phù hợp nhất để giải quyết nhiệm vụ bài ${title}.`
- **5.3.TC1a/TC2a** (Sử dụng sáng tạo công nghệ số):
  `Vận dụng linh hoạt và sáng tạo công cụ số chuyên ngành (${kit.tool}) để mô phỏng, trực quan hóa hoặc tạo sản phẩm đặc thù bài ${title}.`
- **5.4.TC1a/TC2a** (Xác định vấn đề cần cải thiện năng lực số):
  `Tự đánh giá mức độ thành thạo công nghệ của bản thân qua bài ${title} và chủ động học hỏi các thao tác số còn hạn chế.`

### 2.3. Ma trận Mô tả AI Độc lập theo Từng Miền và Từng Mã (QĐ 2422/QĐ-BGDĐT)
Thay thế cơ chế gộp chung bằng hệ thống phân giải chi tiết theo nhóm mã AI:

1. **Nhóm mã A1 (Con người làm chủ, AI là công cụ hỗ trợ)** (ví dụ `6.A1.1`, `6.A1.2`, `6.A1.3`, `7.A1.1`, `8.A1.1`, `9.A1.1`):
   - Mô tả: `"Sử dụng trợ lý AI gợi ý cách tiếp cận bài ${title}; học sinh nhận thức AI chỉ là công cụ hỗ trợ, đối chiếu SGK và con người giữ quyền quyết định cuối cùng về kết quả."`
2. **Nhóm mã A3 (Quyền tự chủ & Dữ liệu cá nhân)** (ví dụ `6.A3.3`, `6.A3.4`, `7.A3.1`, `8.A2.1`, `8.A3.1`):
   - Mô tả: `"Nhận biết việc bảo vệ dữ liệu cá nhân, quyền riêng tư và không cung cấp thông tin nhạy cảm khi tương tác với các hệ thống AI trong bài ${title}."`
3. **Nhóm mã B1 (Mặt tích cực, hạn chế & Nhận diện rủi ro AI)** (ví dụ `6.B1.1`, `8.B1.1`):
   - Mô tả: `"Nhận biết ưu điểm và giới hạn của công cụ AI; cảnh giác với các rủi ro thuật toán thiên vị hoặc thông tin không chính xác do AI đưa ra trong bài ${title}."`
4. **Nhóm mã B2 (An toàn, Minh bạch & Kiểm chứng Deepfake/Giả mạo)** (ví dụ `6.B2.1`, `7.B2.1`, `8.B2.1`, `9.B2.1`, `9.B2.3`):
   - `6.B2.1`, `7.B2.1`: `"Đặt câu hỏi kiểm tra tính an toàn, minh bạch của công cụ AI hỗ trợ bài ${title}; đối chiếu với chuẩn mực đạo đức học đường."`
   - `9.B2.1`: `"Ứng dụng công cụ AI hỗ trợ bài ${title}, học sinh khai báo việc sử dụng AI, tự kiểm soát và chịu trách nhiệm giải trình về sản phẩm học tập."`
   - `9.B2.3`, `8.B1.1`: `"Phân tích các dấu hiệu của nội dung/thông tin giả mạo do AI tạo ra liên quan đến bài ${title}; kiểm chứng qua các nguồn chính thống và đề xuất cách ứng phó."`
5. **Nhóm mã B3 (Khai báo trung thực & Đạo đức AI)** (ví dụ `7.B3.1`, `8.B3.1`, `9.B3.1`):
   - Mô tả: `"Khai báo trung thực và minh bạch phần nội dung có sự trợ giúp của AI trong sản phẩm học tập bài ${title}; tuân thủ liêm chính học thuật."`
6. **Nhóm mã C (Nguyên lý, Dữ liệu huấn luyện & Thuật toán AI)** (ví dụ `6.C1.1`, `7.C4.1`, `7.C5.1`, `8.C1.1`, `9.C4.1`):
   - Mô tả: `"Khám phá cách AI thu thập, phân tích dữ liệu và nhận dạng thông tin trong bài ${title}; thử nghiệm cải thiện độ chính xác của câu lệnh (prompt) hoặc dữ liệu đầu vào."`
7. **Nhóm mã D (Thiết kế & Đánh giá Giải pháp AI)** (ví dụ `6.D1.1`, `7.D1.1`, `8.D1.1`, `9.D1.1`, `9.D2.1`):
   - Mô tả: `"Đánh giá tính chính xác, tính tối ưu và độ tin cậy của sản phẩm do AI gợi ý trong bài ${title}; đề xuất cách điều chỉnh hoặc cải tiến giải pháp."`

### 2.4. Công cụ NLS Chuyên biệt cho Từng Môn Học trong `nlsSubjectToolkit`
Cập nhật và hoàn thiện `nlsSubjectToolkit(subject)` để hỗ trợ đầy đủ 17 môn THCS:
- **Vật lí**: `tool: 'cảm biến đo số, video thí nghiệm mô phỏng (PhET) hoặc phần mềm đồ thị động lực học'`, `practice: 'thu thập số liệu thực nghiệm, phân tích quy luật vật lí và mô phỏng hiện tượng'`.
- **Hoá học**: `tool: 'bảng tuần hoàn tương tác số (Ptable), phần mềm mô phỏng phân tử 3D hoặc video phản ứng hoá học'`, `practice: 'khám phá cấu trúc chất, cân bằng phản ứng và phân tích hiện tượng'`.
- **Sinh học**: `tool: 'kính hiển vi kỹ thuật số, tranh ảnh/video sinh học số hoặc mô hình giải phẫu 3D'`, `practice: 'quan sát cấu tạo sinh vật, phân loại và phân tích quá trình sống'`.
- **Lịch sử**: `tool: 'bản đồ/lược đồ lịch sử số, bảo tàng ảo 3D hoặc kho tư liệu số lịch sử chính thống'`, `practice: 'khai thác tư liệu, đối chiếu nguồn sử liệu và tái hiện bối cảnh lịch sử'`.
- **Địa lí**: `tool: 'Google Earth, bản đồ số, hệ thống GIS hoặc biểu đồ địa lí tương tác'`, `practice: 'định vị không gian, phân tích số liệu và giải thích quy luật địa lí'`.
- **Ngữ văn**: `tool: 'học liệu số văn học, từ điển số hoặc phần mềm sơ đồ tư duy (Canva/Mindmap)'`, `practice: 'khai thác văn bản số, hệ thống hóa ý tưởng và trình bày sản phẩm sáng tạo'`.
- **Toán học**: `tool: 'máy tính cầm tay, phần mềm hình học động GeoGebra hoặc bảng tính điện tử'`, `practice: 'tính toán, dựng hình trực quan, vẽ đồ thị hoặc xử lý số liệu'`.
- **Khoa học tự nhiên**: `tool: 'video thí nghiệm mô phỏng, mô hình 3D tương tác hoặc bảng số liệu đo đạc'`, `practice: 'quan sát hiện tượng, thu thập dữ liệu thực nghiệm và giải thích'`.
- **Tin học**: `tool: 'môi trường lập trình, phần mềm ứng dụng hoặc công cụ quản trị dữ liệu số'`, `practice: 'thực hành kỹ năng số, thiết kế thuật toán và kiểm thử sản phẩm'`.
- **Giáo dục công dân**: `tool: 'học liệu số pháp luật, video tình huống thực tế hoặc diễn đàn trao đổi số'`, `practice: 'tìm hiểu chuẩn mực đạo đức, pháp luật và rèn luyện hành vi ứng xử số'`.
- **Ngoại ngữ (Tiếng Anh)**: `tool: 'từ điển số, phần mềm phát âm chuẩn hoặc công cụ luyện nghe nói tương tác'`, `practice: 'luyện phát âm, tra cứu từ vựng và giao tiếp trong môi trường số'`.
- **Công nghệ**: `tool: 'phần mềm vẽ kỹ thuật số, video mô phỏng quy trình công nghệ hoặc tài liệu kỹ thuật số'`, `practice: 'đọc bản vẽ, mô phỏng quy trình và hoàn thiện sản phẩm kỹ thuật'`.
- **Âm nhạc / Mĩ thuật**: `tool: 'phần mềm xử lý âm thanh/nhạc cụ số, phần mềm đồ họa hoặc bảo tàng mỹ thuật số'`, `practice: 'sáng tạo giai điệu, thiết kế đồ họa và thưởng thức nghệ thuật số'`.
- **Giáo dục thể chất / HĐTN-HN**: `tool: 'video hướng dẫn kỹ thuật vận động, bảng theo dõi thể lực số hoặc nhật ký trải nghiệm số'`, `practice: 'tự đánh giá thể lực, lập kế hoạch hoạt động và chia sẻ kết quả'`.

---

## 3. Danh sách File Cần Chỉnh Sửa (Scope of Changes for Coder)

1. `canvas_xaydungphuluc.html`:
   - Hàm `subjectPedagogyGroup(subject)`: Bổ sung nhận diện riêng biệt cho các môn độc lập (`vatli`, `hoahoc`, `sinhhoc`, `lichsu`, `diali`, `nguvan`, `gdcd`, `tinhoc`, `congnghe`, `tienganh`, `amnhac`, `mithuat`, `gdtc`, `hdtn-hn`).
   - Hàm `nlsSubjectToolkit(subject)`: Cập nhật đầy đủ công cụ và hoạt động đặc trưng cho từng môn.
   - Hàm `lessonAppliedNlsDescription(code, label, lesson)`:
     + Khắc phục `isActualMath`: chỉ kích hoạt nhánh toán học khi môn học là Toán.
     + Sửa các regex bắt từ khóa phân môn toán học chặt chẽ có ranh giới từ `\b`, loại bỏ bắt nhầm các từ ngữ tiếng Việt thông dụng.
     + Bổ sung đầy đủ mô tả độc lập cho từng mã NLS: `1.1`, `1.2`, `1.3`, `2.1` -> `2.6`, `3.1` -> `3.4`, `4.1` -> `4.4`, `5.1` -> `5.4`.
   - Hàm `lessonAppliedNlsFallback(code, lesson, subject)`:
     + Chấm dứt việc gộp chung 5.1, 5.2, 5.3, 5.4 thành 1 câu.
     + Tách biệt rõ ràng từng mã NLS thành phần với mô tả sư phạm cụ thể, kết hợp linh hoạt với `kit.tool` và `kit.practice` của môn học.
   - Hàm `lessonAppliedAiDescription(code, label, lesson)`:
     + Tách biệt mô tả theo từng nhóm mã AI (`A1`, `A3`, `B1`, `B2`, `B3`, `C`, `D`) thay vì chỉ phụ thuộc vào môn/dạng toán.
     + Đảm bảo mã `7.B3.1` luôn có nội hàm *khai báo trung thực*, mã `8.B1.1` & `9.B2.3` luôn có nội hàm *nhận diện rủi ro/deepfake/giả mạo*, mã `6.A1.1` luôn có nội hàm *con người quyết định cuối cùng*.
   - Hàm `lessonAppliedAiFallback(code, lesson, subject)`:
     + Phân giải theo mã AI cụ thể kết hợp đặc trưng môn học, chấm dứt việc toàn bộ mã Miền B trả về 1 câu duy nhất.
2. `xaydungphuluc.html`:
   - Đồng bộ toàn bộ các cập nhật trên để đảm bảo tính nhất quán tuyệt đối giữa giao diện Canvas và giao diện Kế hoạch giáo dục truyền thống.

---

## 4. Tiêu chí Nghiệm thu & Kế hoạch Kiểm thử (Verification Plan)

### Automated Tests
1. **Kiểm tra không trùng mô tả giữa các mã NLS khác chức năng trong cùng 1 bài**:
   - Khi chọn đồng thời cặp mã `(5.2.TC1a, 5.3.TC1a)` hoặc `(1.1.TC1a, 1.3.TC1a)` hoặc `(2.1.TC1a, 2.4.TC1a)`: Hai dòng mô tả sinh ra phải hoàn toàn khác biệt về nội hàm.
2. **Kiểm tra không trùng mô tả giữa các mã AI khác chức năng trong cùng 1 bài**:
   - Khi chọn đồng thời `7.B3.1` (Khai báo trung thực) và `7.B2.1` (Tiêu chí an toàn) trên cùng một bài học bất kỳ: Hai dòng mô tả sinh ra phải thể hiện đúng 2 mục tiêu khác nhau.
3. **Kiểm tra 0 bài học phi-Toán bị gán mô tả Toán học (Zero False Positives)**:
   - Chạy kiểm thử tự động quét toàn bộ hơn 1.000 bài học của 16 môn phi-Toán (Vật lí, Hoá học, Sinh học, Lịch sử, Địa lí, Ngữ văn, GDCD, Tin học...):
     + **0 bài học** xuất hiện từ khóa toán học: `GeoGebra`, `máy tính cầm tay`, `giải hệ phương trình`, `phương pháp thế`, `cộng đại số`, `vẽ thêm yếu tố phụ`, `nghiệm hình học`, `tia số/trục số`.
     + Các bài đặc thù như *Nguồn gốc loài người (Lịch sử 6)*, *Học tập tự giác, tích cực (GDCD 7)*, *Trải nghiệm để trưởng thành (Ngữ văn 7)*, *Đô thị: Lịch sử và hiện tại (Lịch sử/Địa lí)*, *Phương trình hoá học (Hoá học 8)*, *Phản xạ toàn phần (Vật lí 9)* phải mang 100% màu sắc và công cụ của môn học đó.
4. **Không hồi quy hợp đồng kiểm thử cũ**:
   - `tests/canvas-xaydungphuluc-smoke.js`: PASSED 100%.
   - `tests/xaydungphuluc-smoke.js`: PASSED 100%.
   - `tests/sgk-knowledge-smoke.js`: PASSED 100%.
   - `scratch/test_strict_permissions.py`: PASSED 100%.
