/**
 * js/khbd-prompts.js
 * Hệ thống Siêu Prompt Sư phạm Môn Toán THCS chuẩn Công văn 5512/BGDĐT-GDTrH,
 * Chuyên biệt hóa cho bộ sách: KẾT NỐI TRI THỨC VỚI CUỘC SỐNG (KNTT)
 * Tích hợp Khung Năng lực Đặc thù Toán, Khung Năng lực AI (QĐ 2422/QĐ-BGDĐT)
 * và Khung Năng lực Số (TT 02/2025/TT-BGDĐT).
 */

const ACTIVITY_TABLE_CONTRACT = `YÊU CẦU HÌNH THỨC BẮT BUỘC:
- Hoạt động này luôn có đúng bốn mục: ### a) Mục tiêu, ### b) Nội dung, ### c) Sản phẩm, ### d) Tổ chức thực hiện.
- Trong mục d), xuất một bảng Markdown hai cột đúng tiêu đề: | Hoạt động của GV và HS | Nội dung |. Bảng luôn có bốn hàng theo thứ tự: **Chuyển giao nhiệm vụ**, **Thực hiện nhiệm vụ**, **Báo cáo, thảo luận**, **Kết luận, nhận định**.
- Cột trái mô tả việc của GV và HS ở từng bước. Cột phải ghi nhiệm vụ/câu hỏi cụ thể và sản phẩm hoặc đáp án chuẩn tương ứng; không để cột nào trống.
- Riêng Hoạt động B, mỗi đơn vị kiến thức có đầy đủ a, b, c, d và một bảng hai cột riêng.
- Với bảng Markdown, escape mọi dấu pipe trong nội dung hoặc LaTeX thành \\|; không chèn dấu pipe chưa escape trong ô bảng.`;

const PROMPTS = {
  // SYSTEM INSTRUCTION
  SYSTEM_ROLE: `Bạn là Chuyên gia Sư phạm Môn Toán Cấp Trung học Cơ sở (THCS) hàng đầu tại Việt Nam, đặc biệt am hiểu sâu sắc bộ sách giáo khoa "Kết Nối Tri Thức Với Cuộc Sống" (KNTT) của Nhà xuất bản Giáo dục Việt Nam, và nắm vững:
1. Chương trình Giáo dục Phổ thông (GDPT) 2018 môn Toán (Lớp 6, 7, 8, 9) theo bộ sách Kết Nối Tri Thức Với Cuộc Sống.
2. Công văn số 5512/BGDĐT-GDTrH của Bộ Giáo dục và Đào tạo về xây dựng Kế hoạch bài dạy (Giáo án).
3. Khung năng lực đặc thù môn Toán (Tư duy và lập luận toán học; Mô hình hoá toán học; Giải quyết vấn đề toán học; Giao tiếp toán học; Sử dụng công cụ, phương tiện học toán).
4. Khung năng lực Trí tuệ Nhân tạo (AI) cho học sinh THCS theo Quyết định số 2422/QĐ-BGDĐT, khi giáo viên chủ động yêu cầu tích hợp.
5. Khung năng lực Số cho người học theo Thông tư số 02/2025/TT-BGDĐT, khi giáo viên chủ động yêu cầu tích hợp.
6. 5 phẩm chất chủ yếu (Yêu nước, Nhân ái, Chăm chỉ, Trung thực, Trách nhiệm) và phương pháp dạy học hòa nhập cho học sinh khó khăn/chậm tiến độ.

QUY TẮC BẮT BUỘC KHI XUẤT NỘI DUNG:
- Bộ sách áp dụng: KẾT NỐI TRI THỨC VỚI CUỘC SỐNG.
- Sử dụng tiếng Việt chuẩn mực, sư phạm, trang trọng.
- Định dạng Markdown rõ ràng, phân cấp tiêu đề bằng #, ##, ###, #### hợp lý.
- Công thức toán học PHẢI được viết bằng mã LaTeX chuẩn: công thức trong dòng dùng $công_thức$, công thức khối dùng $$công_thức$$. Ví dụ: $x^2 + 2x + 1 = 0$, $\\frac{a}{b}$, $\\sqrt{x}$, $\\Delta = b^2 - 4ac$, $\\triangle ABC = \\triangle A'B'C'$.
- Nội dung phải chi tiết, đầy đủ, thiết thực cho giáo viên lên lớp, tuyệt đối KHÔNG viết tóm tắt qua loa, KHÔNG để dấu '...' hoặc 'tương tự'.
- Tuân thủ tuyệt đối bối cảnh và ràng buộc sư phạm được cung cấp trong từng yêu cầu; không tự bổ sung năng lực số, AI, ngoại ngữ hoặc hỗ trợ hòa nhập nếu không được chọn.`,

  OUTPUT_CONTRACT: `HỢP ĐỒNG ĐẦU RA BẮT BUỘC:
- Chỉ xuất Markdown của đúng mục Kế hoạch bài dạy đang được yêu cầu; bắt đầu ngay bằng tiêu đề/mục chuyên môn phù hợp.
- Danh sách nội dung: ý lớn PHẢI bắt đầu bằng \`- \`; ý con phải thụt đầu dòng và bắt đầu bằng \`+ \`. Không dùng \`1.\`, \`2.\`... làm danh sách nội dung; chỉ dùng số khi là cấu trúc bắt buộc như mục Công văn 5512, Bước hoặc Bài.
- CẤM lời chào, khen ngợi, giới thiệu, nhận xét quá trình, meta commentary và các câu như “Tuyệt vời”, “Xin chào”, “Dưới đây”, “Sau đây”.
- CẤM dùng code fence (\`\`\`). Không giải thích cách bạn đã soạn; không viết nội dung ngoài KHBD.`,

  OUTPUT_REPAIR: `Hãy viết lại nội dung sau thành đúng Markdown của mục Kế hoạch bài dạy. Bắt đầu ngay bằng tiêu đề/mục chuyên môn; chỉ giữ nội dung KHBD. Xóa toàn bộ lời chào, khen ngợi, giới thiệu, meta commentary và mọi code fence. Không thêm lời dẫn mới.`,

  // TAB 1: PHÂN TÍCH ẢNH SGK (VISION)
  ANALYZE_TEXTBOOK: `Bạn hãy quan sát và phân tích toàn diện các hình ảnh trang Sách Giáo Khoa (SGK) Toán - Bộ sách "Kết Nối Tri Thức Với Cuộc Sống" được cung cấp.
Chủ đề bài học: "{topic}" (Môn học: {subject}).

HÃY PHÂN TÍCH VÀ TRÍCH XUẤT NỘI DUNG VỚI CÁC MỤC SAU:
1. **Tổng quan bài học:** Tên bài, vị trí trong chương trình SGK Kết Nối Tri Thức Với Cuộc Sống, mục tiêu cần đạt cốt lõi theo SGK.
2. **Khung kiến thức trọng tâm:**
   - Các định nghĩa, khái niệm, thuật ngữ mới theo cách tiếp cận của bộ sách Kết Nối Tri Thức.
   - Các quy tắc, công thức toán học, định lí, tính chất (viết bằng LaTeX $...$).
   - Các quy ước, chú ý sư phạm quan trọng.
3. **Chuỗi hoạt động khám phá trong SGK Kết Nối Tri Thức:**
   - Hoạt động mở đầu (tình huống, hình ảnh thực tế gắn với cuộc sống).
   - Các hoạt động hình thành kiến thức (HĐ khám phá 1, HĐ 2, các câu hỏi gợi mở, ví dụ mẫu kèm lời giải).
   - Hoạt động luyện tập (các bài Luyện tập, Tranh luận, Thử thách nhỏ trong SGK).
   - Hoạt động vận dụng (các bài toán thực tế, dự án gắn kết tri thức với cuộc sống).
4. **Hệ thống bài tập cuối bài:**
   - Tóm tắt đề bài các bài tập cơ bản và nâng cao trong SGK.
5. **Đề xuất của Chuyên gia Sư phạm:**
   - Những điểm học sinh dễ mắc sai lầm, hiểu sai bản chất.
   - Cơ hội tích hợp các thành phần số/AI nếu và chỉ nếu được bật trong bối cảnh sư phạm.

Hãy trình bày rõ ràng, mạch lạc, giữ nguyên vẹn các công thức toán bằng định dạng LaTeX.`,

  // TAB 2: MỤC TIÊU BÀI HỌC (I. MỤC TIÊU)
  GENERATE_OBJECTIVES: `Hãy xây dựng phần **I. MỤC TIÊU** cho Kế hoạch bài dạy (Giáo án) môn Toán THCS chuẩn Công văn 5512/BGDĐT-GDTrH theo bộ sách **Kết Nối Tri Thức Với Cuộc Sống**.
- Môn học: {subject}
- Tên bài dạy: {topic}
- Thời lượng dự kiến: {duration}
- Bộ sách giáo khoa: Kết Nối Tri Thức Với Cuộc Sống
- Dữ liệu nội dung SGK (nếu có):
"""
{textbook_content}
"""

YÊU CẦU XÂY DỰNG ĐẦY ĐỦ 3 PHẦN THEO CẤU TRÚC SAU:
- Đọc đúng thời lượng trong BỐI CẢNH SƯ PHẠM đi kèm yêu cầu. Với bài 2 tiết hoặc thời lượng ngắn, chỉ chọn 1–2 năng lực chung và 2–3 năng lực đặc thù môn Toán nổi trội, khả thi; không liệt kê dàn trải tất cả năng lực.
- Mỗi năng lực được chọn phải nêu minh chứng cụ thể: kiến thức, nhiệm vụ học tập hoặc sản phẩm của chính bài này; không dùng mô tả chung chung.
- Năng lực số hoặc AI chỉ xuất hiện khi thành phần tương ứng được bật trong BỐI CẢNH SƯ PHẠM, và mỗi thành phần chỉ chọn một biểu hiện thực sự triển khai được. Nếu không bật, bỏ toàn bộ mục đó.
- Phẩm chất chỉ chọn những phẩm chất có hành vi quan sát được trong bài; không mặc định liệt kê đủ 5 phẩm chất. Hỗ trợ HS hòa nhập chỉ nêu khi được bật trong BỐI CẢNH SƯ PHẠM.
- Trong các danh sách dưới đây, dùng \`- \` cho ý lớn và \`  + \` cho ý con; không dùng đánh số thay cho danh sách nội dung.

# I. MỤC TIÊU

## 1. Về kiến thức
(Nêu rõ các mức độ nhận thức: Nhận biết, Thông hiểu, Vận dụng mà học sinh cần đạt được sau bài học, bám sát các khái niệm, công thức, quy tắc trong SGK Kết Nối Tri Thức Với Cuộc Sống).
- Nhận biết được...
- Hiểu và giải thích được...
- Vận dụng được... để giải các bài toán...

## 2. Về năng lực
### a) Năng lực chung
- Chỉ chọn 1–2 năng lực chung phù hợp nhất; với từng năng lực, gắn rõ nhiệm vụ hoặc sản phẩm của bài học.

### b) Năng lực đặc thù môn Toán (Gắn cụ thể với nội dung bài học)
- Chỉ chọn 2–3 năng lực đặc thù nổi trội; với từng năng lực, gắn rõ kiến thức, nhiệm vụ hoặc sản phẩm của bài học.

### c) Năng lực số (CHỈ viết khi bối cảnh sư phạm bật năng lực số; nếu không bật thì bỏ toàn bộ mục này)
- Chỉ chọn một biểu hiện năng lực số được triển khai thật sự trong nhiệm vụ hoặc sản phẩm của bài học.

### d) Năng lực AI (CHỈ viết khi bối cảnh sư phạm bật năng lực AI; nếu không bật thì bỏ toàn bộ mục này)
- Chỉ chọn một biểu hiện năng lực AI được triển khai thật sự trong nhiệm vụ hoặc sản phẩm của bài học.

## 3. Về phẩm chất & Giáo dục hòa nhập (chỉ nêu hỗ trợ HS khuyết tật/hòa nhập khi bối cảnh sư phạm bật)
- Chỉ chọn các phẩm chất có hành vi quan sát được trong nhiệm vụ/sản phẩm của bài; nêu ngắn gọn minh chứng đó.
- **Hỗ trợ học sinh giáo dục hòa nhập (nếu có):** Chỉ khi được bật, nêu điều chỉnh vừa sức và cách hỗ trợ để HS tham gia nhiệm vụ của bài.`,

  // TAB 3: THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU (II. THIẾT BỊ & HỌC LIỆU)
  GENERATE_MATERIALS: `Hãy xây dựng phần **II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU** cho Kế hoạch bài dạy môn Toán THCS chuẩn Công văn 5512 theo bộ sách **Kết Nối Tri Thức Với Cuộc Sống**.
- Môn học: {subject}
- Tên bài dạy: {topic}
- Bộ sách giáo khoa: Kết Nối Tri Thức Với Cuộc Sống
- Dữ liệu nội dung SGK (nếu có):
"""
{textbook_content}
"""

YÊU CẦU XÂY DỰNG ĐẦY ĐỦ 2 MỤC CHÍNH; chỉ thêm thiết bị số/AI khi bối cảnh sư phạm bật thành phần tương ứng:

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU

## 1. Đối với Giáo viên
- **Hồ sơ dạy học:** Kế hoạch bài dạy (Giáo án) được biên soạn chu đáo; Sách giáo khoa, Sách giáo viên môn Toán (Bộ Kết Nối Tri Thức Với Cuộc Sống).
- **Phương tiện và Đồ dùng dạy học:**
  + Máy tính, máy chiếu/Tivi thông minh phục vụ trình chiếu bài giảng điện tử (PowerPoint/Canva).
  + Thước thẳng có chia vạch, compa bảng, êke, thước đo góc chuyên dụng cho GV.
  + Các mô hình trực quan, tranh ảnh hoặc video thực tế liên quan đến bài học.
  + Hệ thống Phiếu học tập (PHT số 1, PHT số 2,...) in sẵn cho các nhóm hoặc từng học sinh.
- **Học liệu số và Ứng dụng AI (chỉ khi được bật):**
  + File mô phỏng hình học động / đồ thị hàm số trên phần mềm **GeoGebra** hoặc **Desmos**.
  + Các câu hỏi tương tác trên Quizizz, Kahoot hoặc Google Forms (nếu có).
  + Khung câu lệnh (Prompt) chuẩn bị sẵn để minh họa hoặc hướng dẫn HS tra cứu trên các công cụ AI.

## 2. Đối với Học sinh
- **Đồ dùng học tập cá nhân:**
  + Sách giáo khoa Toán (Bộ Kết Nối Tri Thức Với Cuộc Sống), vở ghi bài, vở bài tập môn Toán.
  + Thước kẻ có chia khoảng cách, compa, êke, thước đo góc, bút chì, tẩy.
  + Máy tính cầm tay (Casio fx-580VN X, Casio fx-880BTG hoặc tương đương) đã được phép mang vào phòng thi.
  + Bảng nhóm (bảng phụ), bút lông viết bảng nhóm.
- **Nhiệm vụ chuẩn bị bài trước ở nhà:**
  + Đọc trước nội dung bài mới trong SGK Kết Nối Tri Thức Với Cuộc Sống, chuẩn bị câu hỏi thắc mắc.
  + Hoàn thành nhiệm vụ tự học/khảo sát thực tế được giao từ tiết trước.`,

  // TAB 4.A: TIẾN TRÌNH DẠY HỌC - HOẠT ĐỘNG MỞ ĐẦU
  GENERATE_ACTIVITY_A: `Hãy biên soạn chi tiết **HOẠT ĐỘNG MỞ ĐẦU (TIẾP CẬN VẤN ĐỀ)** trong mục III. Tiến trình dạy học chuẩn Công văn 5512 theo bộ sách **Kết Nối Tri Thức Với Cuộc Sống**.
- Môn học: {subject}
- Tên bài dạy: {topic}
- Bộ sách giáo khoa: Kết Nối Tri Thức Với Cuộc Sống
- Mục tiêu bài học:
"""
{objectives_content}
"""
- Dữ liệu SGK:
"""
{textbook_content}
"""

YÊU CẦU BẮT BUỘC ĐỦ 4 THÀNH PHẦN THEO CV 5512:
${ACTIVITY_TABLE_CONTRACT}

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: MỞ ĐẦU (Khoảng 5 - 7 phút)

### a) Mục tiêu:
- Tạo tâm thế hứng thú, kích thích trí tò mò, tạo mâu thuẫn nhận thức hoặc nhu cầu tìm hiểu kiến thức mới của học sinh bám sát tình huống mở đầu của SGK Kết Nối Tri Thức Với Cuộc Sống.
- Huy động các kiến thức, kĩ năng đã học có liên quan đến nội dung bài mới.

### b) Nội dung:
(Mô tả chi tiết tình huống thực tiễn / câu đố / trò chơi học tập / bài toán mở đầu / hình ảnh trực quan gắn liền với cuộc sống mà GV đưa ra cho HS thực hiện).

### c) Sản phẩm:
(Mô tả cụ thể câu trả lời, kết quả dự đoán, sản phẩm tính toán ban đầu hoặc câu hỏi băn khoăn của học sinh khi đối diện tình huống).

### d) Tổ chức thực hiện:
- **Bước 1: Chuyển giao nhiệm vụ:** (GV nêu luật chơi / trình chiếu hình ảnh / phát phiếu khởi động / giao nhiệm vụ cụ thể cho cá nhân hoặc nhóm).
- **Bước 2: Thực hiện nhiệm vụ:** (HS quan sát, thảo luận, tính toán, dự đoán dưới sự bao quát của GV; GV hỗ trợ học sinh khó khăn).
- **Bước 3: Báo cáo, thảo luận:** (Đại diện 1-2 HS hoặc nhóm phát biểu câu trả lời; các HS khác lắng nghe, nhận xét, đưa ra ý kiến phản biện).
- **Bước 4: Kết luận, nhận định & Dẫn dắt vào bài mới:** (GV nhận xét tinh thần học tập, khéo léo dẫn dắt từ mâu thuẫn nhận thức/kết quả khởi động để giới thiệu vào bài học mới).`,

  // TAB 4.B: TIẾN TRÌNH DẠY HỌC - HOẠT ĐỘNG HÌNH THÀNH KIẾN THỨC MỚI
  GENERATE_ACTIVITY_B: `Hãy biên soạn chi tiết toàn bộ **HOẠT ĐỘNG HÌNH THÀNH KIẾN THỨC MỚI** trong mục III. Tiến trình dạy học chuẩn Công văn 5512 theo bộ sách **Kết Nối Tri Thức Với Cuộc Sống**.
- Môn học: {subject}
- Tên bài dạy: {topic}
- Bộ sách: Kết Nối Tri Thức Với Cuộc Sống
- Mục tiêu bài học:
"""
{objectives_content}
"""
- Dữ liệu SGK:
"""
{textbook_content}
"""

YÊU CẦU QUAN TRỌNG:
${ACTIVITY_TABLE_CONTRACT}
- Bám sát mạch kiến thức và các Hoạt động khám phá trong SGK Kết Nối Tri Thức Với Cuộc Sống.
- Chia bài học thành các đơn vị kiến thức nhỏ rõ ràng (ví dụ: Hoạt động 2.1: Khái niệm...; Hoạt động 2.2: Định lí/Tính chất...; Hoạt động 2.3: Quy tắc...).
- MỖI ĐƠN VỊ KIẾN THỨC ĐỀU PHẢI CÓ ĐẦY ĐỦ 4 THÀNH PHẦN: a) Mục tiêu, b) Nội dung, c) Sản phẩm, d) Tổ chức thực hiện (4 bước: Chuyển giao -> Thực hiện -> Báo cáo thảo luận -> Kết luận nhận định).
- Sản phẩm và Kết luận nhận định PHẢI CÓ LỜI GIẢI TOÁN HỌC CHI TIẾT, CÔNG THỨC LATEX HOÀN CHỈNH, ĐỊNH NGHĨA/ĐỊNH LÍ CHÍNH XÁC ĐỂ HS GHI VỞ.

CẤU TRÚC MẪU:

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI

### 1. Hoạt động 2.1: [Tên đơn vị kiến thức 1]
#### a) Mục tiêu:
- Học sinh hình thành được khái niệm / nhận biết được...
#### b) Nội dung:
- Học sinh thực hiện Hoạt động khám phá / Phiếu học tập số 1 / Đọc hiểu thông tin trong SGK Kết Nối Tri Thức...
#### c) Sản phẩm:
- Kết quả câu trả lời, lời giải chi tiết cho các câu hỏi khám phá:
  + (Trình bày chi tiết các phép toán, công thức LaTeX $...$).
#### d) Tổ chức thực hiện:
- **Bước 1: Chuyển giao nhiệm vụ:** (GV chia nhóm, giao PHT, đặt câu hỏi...).
- **Bước 2: Thực hiện nhiệm vụ:** (HS làm việc cá nhân kết hợp thảo luận nhóm, GV quan sát hướng dẫn).
- **Bước 3: Báo cáo, thảo luận:** (Đại diện nhóm trình bày, các nhóm khác phản biện).
- **Bước 4: Kết luận, nhận định:** (GV chuẩn hóa kiến thức, chốt nội dung trọng tâm ghi bảng: Định nghĩa, Chú ý, Ví dụ mẫu 1 có giải chi tiết).

### 2. Hoạt động 2.2: [Tên đơn vị kiến thức 2]
(Tương tự đầy đủ 4 phần a, b, c, d với các bước chi tiết và ví dụ áp dụng...)

### 3. Hoạt động 2.3: [Nếu bài có thêm đơn vị kiến thức 3...]`,

  // TAB 4.C: TIẾN TRÌNH DẠY HỌC - HOẠT ĐỘNG LUYỆN TẬP
  GENERATE_ACTIVITY_C: `Hãy biên soạn chi tiết **HOẠT ĐỘNG LUYỆN TẬP** trong mục III. Tiến trình dạy học chuẩn Công văn 5512 theo bộ sách **Kết Nối Tri Thức Với Cuộc Sống**.
- Môn học: {subject}
- Tên bài dạy: {topic}
- Bộ sách: Kết Nối Tri Thức Với Cuộc Sống
- Mục tiêu và Kiến thức trọng tâm:
"""
{objectives_content}
"""

YÊU CẦU BIÊN SOẠN:
${ACTIVITY_TABLE_CONTRACT}
- Xây dựng hệ thống bài tập luyện tập bám sát các dạng bài trong SGK Kết Nối Tri Thức Với Cuộc Sống:
  + Dạng 1: Bài tập nhận biết và thông hiểu (rèn kĩ năng tính toán, áp dụng trực tiếp công thức).
  + Dạng 2: Bài tập vận dụng / Tranh luận / Thử thách nhỏ theo phong cách KNTT.
  + Dạng 3: Bài tập trắc nghiệm khách quan củng cố nhanh (4 câu trắc nghiệm 4 lựa chọn A, B, C, D).
- TẤT CẢ CÁC BÀI TẬP ĐỀU BẮT BUỘC CÓ LỜI GIẢI CHI TIẾT TỪNG BƯỚC kèm công thức LaTeX $...$.
- Tuân thủ đủ 4 thành phần theo CV 5512: a) Mục tiêu, b) Nội dung, c) Sản phẩm, d) Tổ chức thực hiện.

CẤU TRÚC:

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (Khoảng 12 - 15 phút)

### a) Mục tiêu:
- Củng cố, khắc sâu kiến thức vừa học thông qua việc giải các bài tập cụ thể trong SGK Kết Nối Tri Thức Với Cuộc Sống.
- Rèn luyện kĩ năng tính toán, vẽ hình, biến đổi đại số, lập luận toán học và sử dụng máy tính cầm tay.

### b) Nội dung:
- **Bài tập 1 (Mức độ Nhận biết - Thông hiểu):** [Đề bài cụ thể...]
- **Bài tập 2 (Mức độ Thông hiểu - Vận dụng):** [Đề bài cụ thể...]
- **Bài tập 3 (Trắc nghiệm nhanh củng cố):** [4 câu hỏi trắc nghiệm A, B, C, D...]

### c) Sản phẩm:
(Lời giải chi tiết đầy đủ cho từng bài tập ở mục Nội dung).
- **Lời giải Bài tập 1:** (Trình bày chi tiết từng bước bằng LaTeX $...$).
- **Lời giải Bài tập 2:** (Trình bày chi tiết từng bước bằng LaTeX $...$).
- **Đáp án Bài tập 3:** (Đáp án và giải thích ngắn gọn).

### d) Tổ chức thực hiện:
- **Bước 1: Chuyển giao nhiệm vụ:** (GV giao bài tập cho cả lớp làm việc cá nhân / bắt cặp đôi).
- **Bước 2: Thực hiện nhiệm vụ:** (HS giải bài vào vở/phiếu; GV hỗ trợ học sinh còn lúng túng).
- **Bước 3: Báo cáo, thảo luận:** (Gọi HS lên bảng trình bày, cả lớp nhận xét đối chiếu bài làm).
- **Bước 4: Kết luận, nhận định:** (GV chữa bài, chỉ ra các lỗi sai thường gặp, chốt kĩ năng và phương pháp giải chuẩn).`,

  // TAB 4.D: TIẾN TRÌNH DẠY HỌC - HOẠT ĐỘNG VẬN DỤNG
  GENERATE_ACTIVITY_D: `Hãy biên soạn chi tiết **HOẠT ĐỘNG VẬN DỤNG** trong mục III. Tiến trình dạy học chuẩn Công văn 5512 theo bộ sách **Kết Nối Tri Thức Với Cuộc Sống**.
- Môn học: {subject}
- Tên bài dạy: {topic}
- Bộ sách: Kết Nối Tri Thức Với Cuộc Sống
- Mục tiêu bài học:
"""
{objectives_content}
"""

YÊU CẦU BIÊN SOẠN:
${ACTIVITY_TABLE_CONTRACT}
- Thiết kế 1 đến 2 bài toán vận dụng thực tiễn thể hiện đúng tinh thần "Kết nối tri thức với cuộc sống", gắn liền với đời sống hàng ngày của học sinh THCS (đo đạc, tài chính gia đình, kiến trúc, môi trường, số liệu thống kê...) hoặc tích hợp liên môn (Vật lý, Địa lý, Công nghệ...).
- Chỉ tích hợp hướng dẫn HS ứng dụng công cụ số/AI để kiểm chứng lời giải khi bối cảnh sư phạm bật thành phần tương ứng.
- Đầy đủ 4 thành phần a, b, c, d theo CV 5512 kèm LỜI GIẢI CHI TIẾT ĐẦY ĐỦ.

CẤU TRÚC:

## D. HOẠT ĐỘNG 4: VẬN DỤNG (Khoảng 5 - 8 phút hoặc giao về nhà)

### a) Mục tiêu:
- Giúp học sinh thấy được ý nghĩa thực tiễn của bài học, biết mô hình hoá toán học để giải quyết các vấn đề trong đời sống theo định hướng bộ sách Kết Nối Tri Thức Với Cuộc Sống.
- Phát triển năng lực giải quyết vấn đề, tư duy sáng tạo và năng lực ứng dụng công nghệ.

### b) Nội dung:
- **Tình huống thực tế:** (Mô tả bài toán thực tế sinh động, có số liệu cụ thể...).

### c) Sản phẩm:
- Lời giải bài toán thực tế hoàn chỉnh, có giải thích rõ ràng từng bước mô hình hóa toán học và đơn vị đo.

### d) Tổ chức thực hiện:
- **Bước 1: Chuyển giao nhiệm vụ:** (GV nêu tình huống, có thể giao làm nhóm tại lớp hoặc hoàn thiện thành dự án nhỏ tại nhà).
- **Bước 2: Thực hiện nhiệm vụ:** (HS phân tích đề bài, vẽ sơ đồ, thiết lập công thức/phương trình toán học).
- **Bước 3: Báo cáo, thảo luận:** (Đại diện trình bày phương án giải quyết và ý nghĩa thực tế).
- **Bước 4: Kết luận, nhận định:** (GV đánh giá, tổng kết bài học, khích lệ tinh thần vận dụng toán học vào đời sống).`,

  // TAB 4.E: KẾ HOẠCH KIỂM TRA - ĐÁNH GIÁ (MA TRẬN & RUBRICS)
  GENERATE_ASSESSMENT: `Hãy biên soạn **E. KẾ HOẠCH KIỂM TRA - ĐÁNH GIÁ** cho Kế hoạch bài dạy môn Toán THCS chuẩn CV 5512 (Bộ sách Kết Nối Tri Thức Với Cuộc Sống).
- Môn học: {subject}
- Tên bài dạy: {topic}
- Bộ sách: Kết Nối Tri Thức Với Cuộc Sống
- Mục tiêu và Tiến trình dạy học:
"""
{objectives_content}
{activities_content}
"""

YÊU CẦU XÂY DỰNG 2 BẢNG ĐÁNH GIÁ CHUYÊN NGHIỆP DƯỚI DẠNG BẢNG MARKDOWN:

# E. KẾ HOẠCH KIỂM TRA - ĐÁNH GIÁ

## 1. Bảng Ma trận Kiểm tra - Đánh giá trong Tiến trình Dạy học
(Xây dựng bảng ma trận thể hiện hình thức, phương pháp, công cụ đánh giá cho từng hoạt động từ Khởi động đến Vận dụng).

| Hoạt động học | Mục tiêu đánh giá | Phương pháp đánh giá | Công cụ đánh giá | Người đánh giá |
| :--- | :--- | :--- | :--- | :--- |
| **A. Mở đầu** | Sự hứng thú, khả năng huy động kiến thức nền | Quan sát, vấn đáp | Câu hỏi mở đầu, thái độ tham gia | Giáo viên |
| **B. Hình thành kiến thức** | Khả năng khám phá, chiếm lĩnh khái niệm, công thức mới | Quan sát, đánh giá sản phẩm | Phiếu học tập, câu trả lời cá nhân/nhóm | GV & Học sinh (đánh giá đồng đẳng) |
| **C. Luyện tập** | Kĩ năng tính toán, biến đổi, giải bài tập mẫu | Đánh giá qua sản phẩm viết | Vở ghi, bảng phụ, câu hỏi trắc nghiệm | Giáo viên & Tự đánh giá |
| **D. Vận dụng** | Năng lực mô hình hoá toán học vào thực tế | Đánh giá sản phẩm dự án/bài viết | Báo cáo bài tập vận dụng thực tiễn | Giáo viên |

## 2. Bảng Tiêu chí Đánh giá (Rubrics) Hoạt động Học tập của Học sinh
(Xây dựng Rubrics định lượng 4 mức độ: Mức 1 - Chưa đạt, Mức 2 - Đạt, Mức 3 - Khá, Mức 4 - Tốt).

| Tiêu chí đánh giá | Mức 1: Chưa đạt (Dưới 5đ) | Mức 2: Đạt (5 - 6.5đ) | Mức 3: Khá (7 - 8.5đ) | Mức 4: Tốt (9 - 10đ) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Nắm vững kiến thức toán học** | Chưa nhớ định nghĩa, công thức; còn nhầm lẫn nhiều | Nhớ định nghĩa, công thức cơ bản nhưng áp dụng còn lúng túng | Nắm vững định nghĩa, vận dụng đúng công thức vào các bài toán quen thuộc | Hiểu sâu sắc bản chất, giải thích mạch lạc, vận dụng linh hoạt |
| **2. Kĩ năng tính toán và lập luận** | Tính toán sai nhiều, trình bày lộn xộn, thiếu bước | Tính toán cơ bản đúng, trình bày còn sơ sài | Tính toán chuẩn xác, lập luận có căn cứ, trình bày sạch đẹp | Tính toán nhanh, lập luận chặt chẽ, tối ưu hóa cách giải |
| **3. Tinh thần hợp tác và thảo luận** | Thụ động, không tham gia cùng nhóm | Có tham gia nhưng còn ỷ lại vào bạn khác | Tích cực trao đổi, hoàn thành tốt phần việc được phân công | Đóng vai trò nòng cốt, hỗ trợ các bạn khác, dẫn dắt nhóm |
| **4. Năng lực ứng dụng Số / AI** | Chưa biết sử dụng máy tính/phần mềm | Sử dụng máy tính cầm tay mức độ cơ bản | Sử dụng tốt máy tính cầm tay, biết dùng GeoGebra/AI tra cứu | Sử dụng thành thạo thiết bị số, biết phản biện và kiểm chứng kết quả AI |

Chỉ đưa hàng Rubrics về năng lực Số/AI khi thành phần tương ứng được bật trong bối cảnh sư phạm; nếu không thì bỏ hàng này.`,

  // TAB 4.F: HỒ SƠ DẠY HỌC (PHIẾU HỌC TẬP CÓ ĐÁP ÁN)
  GENERATE_PORTFOLIO: `Hãy thiết kế **F. HỒ SƠ DẠY HỌC (CÁC PHIẾU HỌC TẬP)** cho Kế hoạch bài dạy môn Toán THCS (Bộ sách Kết Nối Tri Thức Với Cuộc Sống).
- Môn học: {subject}
- Tên bài dạy: {topic}
- Bộ sách: Kết Nối Tri Thức Với Cuộc Sống
- Dữ liệu bài học:
"""
{objectives_content}
{activities_content}
"""

YÊU CẦU THIẾT KẾ:
- Tạo 2 đến 3 Phiếu Học Tập (PHT) hoàn chỉnh (PHT số 1 cho hoạt động Khám phá; PHT số 2 cho Luyện tập; PHT số 3 cho Vận dụng/Phân hóa).
- Mỗi PHT phải có phần Tiêu đề (Trường, Lớp, Nhóm/Họ tên HS), các câu hỏi/nhiệm vụ rõ ràng, kẻ khung bảng biểu đẹp mắt.
- BẮT BUỘC CÓ PHẦN **HƯỚNG DẪN CHẤM VÀ ĐÁP ÁN CHI TIẾT** CHO TỪNG PHIẾU HỌC TẬP (kèm biểu điểm 10).

CẤU TRÚC:

# F. HỒ SƠ DẠY HỌC

## 1. PHIẾU HỌC TẬP SỐ 1 (Phục vụ Hoạt động Khám phá / Hình thành kiến thức)
**TRƯỜNG THCS: .......................................**  
**LỚP: .............. NHÓM: ..............................**  
**HỌ VÀ TÊN THÀNH VIÊN: .....................................................................................**  
### BÀI HỌC: {topic} (Sách Kết Nối Tri Thức Với Cuộc Sống)

| Nhiệm vụ | Nội dung câu hỏi / Bài tập | Dự kiến kết quả của Học sinh |
| :--- | :--- | :--- |
| **Nhiệm vụ 1** | [Nội dung nhiệm vụ 1...] | .............................................................. |
| **Nhiệm vụ 2** | [Nội dung nhiệm vụ 2...] | .............................................................. |
| **Nhiệm vụ 3** | [Nội dung nhiệm vụ 3...] | .............................................................. |

*(Nhận xét của Giáo viên: ........................................................................................................)*

---

## 2. PHIẾU HỌC TẬP SỐ 2 (Phục vụ Hoạt động Luyện tập & Củng cố)
[Nội dung tương tự với các bài tập rèn luyện kĩ năng tính toán...]

---

## 3. HƯỚNG DẪN CHẤM VÀ ĐÁP ÁN CHI TIẾT CÁC PHIẾU HỌC TẬP

### a) Đáp án và Thang điểm Phiếu học tập số 1 (Thang điểm 10)
- **Nhiệm vụ 1 (3.0 điểm):** Lời giải chi tiết: ... ($...$)
- **Nhiệm vụ 2 (4.0 điểm):** Lời giải chi tiết: ... ($...$)
- **Nhiệm vụ 3 (3.0 điểm):** Lời giải chi tiết: ... ($...$)

### b) Đáp án và Thang điểm Phiếu học tập số 2 (Thang điểm 10)
[Lời giải chi tiết từng bài...]`,

  // TAB 4.G: HƯỚNG DẪN VỀ NHÀ
  GENERATE_HOMEWORK: `Hãy biên soạn chi tiết **G. HƯỚNG DẪN VỀ NHÀ** trong Kế hoạch bài dạy môn Toán THCS chuẩn CV 5512 (Bộ sách Kết Nối Tri Thức Với Cuộc Sống).
- Môn học: {subject}
- Tên bài dạy: {topic}
- Bộ sách: Kết Nối Tri Thức Với Cuộc Sống
- Nội dung bài học:
"""
{objectives_content}
{activities_content}
"""

YÊU CẦU XÂY DỰNG 4 MỤC CHI TIẾT:

# G. HƯỚNG DẪN VỀ NHÀ

## 1. Ôn tập và Khắc sâu kiến thức
- Học thuộc và nắm vững các định nghĩa, quy tắc, công thức toán học đã học trong bài: (liệt kê vắn tắt các công thức trọng tâm $...$).
- Vẽ sơ đồ tư duy (Mindmap) tóm tắt toàn bộ nội dung bài học vào vở ghi.

## 2. Bài tập tự luyện tại nhà
- Hoàn thành các bài tập trong SGK Kết Nối Tri Thức Với Cuộc Sống: Bài ... trang ...
- Hoàn thành bài tập trong Sách bài tập (SBT) Toán Kết Nối Tri Thức: Bài ... trang ...
- **Bài tập mở rộng / Nâng cao (Dành cho HS khá, giỏi):** (Đưa ra 1 bài toán mở rộng có tính tư duy cao kèm gợi ý ngắn gọn).

## 3. Nhiệm vụ chuẩn bị cho bài học tiếp theo
- Đọc trước bài mới: "[Tên bài học tiếp theo theo phân phối chương trình SGK Kết Nối Tri Thức Với Cuộc Sống]".
- Chuẩn bị đầy đủ dụng cụ học tập: thước đo góc, compa, bảng nhóm... cho tiết học sau.
- Tìm hiểu các ví dụ thực tế liên quan đến bài học tiếp theo.

## 4. Gợi ý Câu lệnh Prompt AI hỗ trợ học sinh tự học tại nhà an toàn (CHỈ tạo khi bối cảnh sư phạm bật năng lực AI)
(Cung cấp 2-3 mẫu câu lệnh mẫu để HS có thể hỏi trợ lý AI như Gemini/ChatGPT/NotebookLM khi gặp khó khăn lúc tự học ở nhà, nhưng rèn luyện tính tư duy chứ không hỏi thẳng đáp án).
- *Mẫu Prompt 1 (Giải thích lại khái niệm):* "Em là học sinh lớp {grade}, em chưa hiểu rõ về [khái niệm trong bài]. Bạn hãy giải thích lại bằng một ví dụ thực tế gần gũi, đơn giản nhất nhé!"
- *Mẫu Prompt 2 (Gợi ý từng bước):* "Em đang giải bài toán [chép đề bài]. Em chưa biết bắt đầu từ đâu, bạn hãy cho em 2 câu hỏi gợi ý để em tự tìm ra hướng giải, đừng giải hộ em nhé!"
- *Mẫu Prompt 3 (Kiểm tra lời giải):* "Đây là lời giải của em cho bài toán [bài toán]: [lời giải]. Bạn hãy nhận xét xem em đã làm đúng chưa và chỉ ra bước nào cần khắc phục nhé!"`
};

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { PROMPTS };
}
