/**
 * js/khbd-prompts.js
 * Hệ thống Siêu Prompt Sư phạm Môn Toán THCS chuẩn Công văn 5512/BGDĐT-GDTrH,
 * Dùng cho SGK Toán do giáo viên cung cấp.
 * Tích hợp Khung Năng lực Đặc thù Toán, Khung Năng lực AI (QĐ 2422/QĐ-BGDĐT)
 * và Khung Năng lực Số (TT 02/2025/TT-BGDĐT).
 */

const ACTIVITY_TABLE_CONTRACT = `YÊU CẦU HÌNH THỨC BẢNG 2 CỘT (đúng mẫu demo.docx):
- Mục a), b), c) viết bằng gạch đầu dòng - và ý con + như bình thường.
- Mục d) Tổ chức thực hiện: ĐÚNG MỘT bảng Markdown 2 cột, tiêu đề:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
- Chỉ 1 hàng dữ liệu (không tách 4 hàng).
- Cột TRÁI — việc tổ chức lớp: đủ 4 bước, mỗi bước một dòng, ngăn bằng <br>
  + Bước 1: Chuyển giao nhiệm vụ: ...
  + Bước 2: Thực hiện nhiệm vụ: ...
  + Bước 3: Báo cáo, thảo luận: ...
  + Bước 4: Kết luận, nhận định: ...
- Cột PHẢI — chỉ NỘI DUNG GHI BẢNG (kiến thức chốt cho HS chép): tên mục kiến thức, định nghĩa, quy tắc, công thức LaTeX, chú ý, ví dụ mẫu. Dùng - và +. Ngăn dòng bằng <br>
- Cột phải CẤM: mô tả việc của GV/HS, CẤM lặp lại 4 bước, CẤM viết "GV yêu cầu", "HS thảo luận", thời gian, kỹ thuật tổ chức.
- Cấm để trống cột. Escape dấu | trong ô thành \\|.
- Hoạt động B: mỗi đơn vị kiến thức một bảng 2 cột (1 hàng) như trên.`;

const PROMPTS = {
  // SYSTEM INSTRUCTION
  SYSTEM_ROLE: `Bạn là Chuyên gia Sư phạm Môn Toán Cấp Trung học Cơ sở (THCS), nắm vững:
1. Chương trình Giáo dục Phổ thông (GDPT) 2018 môn Toán (Lớp 6, 7, 8, 9).
2. Công văn số 5512/BGDĐT-GDTrH của Bộ Giáo dục và Đào tạo về xây dựng Kế hoạch bài dạy (Giáo án).
3. Khung năng lực đặc thù môn Toán (Tư duy và lập luận toán học; Mô hình hoá toán học; Giải quyết vấn đề toán học; Giao tiếp toán học; Sử dụng công cụ, phương tiện học toán).
4. Khung năng lực Trí tuệ Nhân tạo (AI) cho học sinh THCS theo Quyết định số 2422/QĐ-BGDĐT, khi giáo viên chủ động yêu cầu tích hợp.
5. Khung năng lực Số cho người học theo Thông tư số 02/2025/TT-BGDĐT, khi giáo viên chủ động yêu cầu tích hợp.
6. 5 phẩm chất chủ yếu (Yêu nước, Nhân ái, Chăm chỉ, Trung thực, Trách nhiệm) và phương pháp dạy học hòa nhập cho học sinh khó khăn/chậm tiến độ.

QUY TẮC BẮT BUỘC KHI XUẤT NỘI DUNG:
- Bám sát GDPT 2018 và nội dung SGK/trang SGK, dữ liệu bài học do giáo viên cung cấp; không tự gán nhà xuất bản hay bộ sách.
- Luôn thiết kế mục tiêu bài dạy tinh gọn, thiết thực cho 1–2 tiết học (chỉ chọn 1–2 năng lực chung, 2–3 năng lực đặc thù nổi trội, 1–2 phẩm chất; tuyệt đối không liệt kê dàn trải).
- Sử dụng tiếng Việt chuẩn mực, sư phạm, trang trọng.
- Định dạng Markdown rõ ràng, phân cấp tiêu đề bằng #, ##, ###, #### hợp lý.
- Công thức toán học PHẢI được viết bằng mã LaTeX chuẩn: công thức trong dòng dùng $công_thức$, công thức khối dùng $$công_thức$$. Ví dụ: $x^2 + 2x + 1 = 0$, $\\frac{a}{b}$, $\\sqrt{x}$, $\\Delta = b^2 - 4ac$, $\\triangle ABC = \\triangle A'B'C'$.
- Nội dung phải chi tiết, đầy đủ, thiết thực cho giáo viên lên lớp, tuyệt đối KHÔNG viết tóm tắt qua loa, KHÔNG để dấu '...' hoặc 'tương tự'.
- Tuân thủ tuyệt đối bối cảnh và ràng buộc sư phạm được cung cấp trong từng yêu cầu; không tự bổ sung năng lực số, AI, ngoại ngữ hoặc hỗ trợ hòa nhập nếu không được chọn.`,

  OUTPUT_CONTRACT: `HỢP ĐỒNG ĐẦU RA BẮT BUỘC:
- Chỉ xuất Markdown của đúng mục Kế hoạch bài dạy đang được yêu cầu; bắt đầu ngay bằng tiêu đề/mục chuyên môn phù hợp.
- Danh sách nội dung có đúng ba cấp: ý lớn bắt đầu bằng \`- \`; ý con thụt đầu dòng và bắt đầu bằng \`+ \`; ý chi tiết thụt thêm một cấp và bắt đầu bằng \`• \`. Không dùng \`1.\`, \`2.\`... làm danh sách nội dung; chỉ dùng số khi là cấu trúc bắt buộc như mục Công văn 5512, Bước hoặc Bài.
- CẤM lời chào, khen ngợi, giới thiệu, nhận xét quá trình, meta commentary và các câu như “Tuyệt vời”, “Xin chào”, “Dưới đây”, “Sau đây”.
- CẤM dùng code fence (\`\`\`). Không giải thích cách bạn đã soạn; không viết nội dung ngoài KHBD.
- CẤM xuất HTML, thẻ span, thuộc tính style hay mã màu. Chỉ Markdown thuần. Màu chữ do ứng dụng xử lý.`,

  OUTPUT_REPAIR: `Hãy viết lại nội dung sau thành đúng Markdown của mục Kế hoạch bài dạy. Bắt đầu ngay bằng tiêu đề/mục chuyên môn; chỉ giữ nội dung KHBD. Xóa toàn bộ lời chào, khen ngợi, giới thiệu, meta commentary và mọi code fence. Không thêm lời dẫn mới.`,

  SOURCE_LOCK: `KHÓA NGUỒN BẮT BUỘC:
- Chỉ dùng: ảnh/PDF SGK, nội dung phân tích Tab 1, tên bài/môn/lớp giáo viên chọn, YCCĐ chính thức (TT 32/2018/TT-BGDĐT — CT GDPT 2018) nếu được cung cấp, và bối cảnh lớp.
- CẤM bịa định nghĩa, định lý, công thức, số liệu, đề bài, đáp án, số trang, hình minh họa hoặc nhiệm vụ không có trong nguồn.
- Luyện tập/vận dụng: CHỈ dùng bài, câu, hoạt động có trong nguồn đã đưa vào prompt (khối dữ liệu SGK / bài tập nguồn). Phải đọc khối đó trước khi kết luận. Chỉ ghi "[Không có trong tài liệu đã cung cấp]" khi đã đọc khối nguồn mà vẫn không có bài/câu/luyện tập/vận dụng. CẤM kết luận thiếu nguồn khi chưa đọc dữ liệu SGK. CẤM invent trắc nghiệm 4 lựa chọn, không invent bài thực tiễn có số liệu, không bịa "SBT trang …".
- Mục tiêu kiến thức phải là Yêu cầu cần đạt của CT GDPT 2018 ban hành kèm Thông tư 32/2018/TT-BGDĐT (hoặc YCCĐ in trên SGK/nguồn). Không tự tạo thang Bloom nếu không có trong nguồn.`,

  // TAB 1: PHÂN TÍCH ẢNH SGK (VISION)
  ANALYZE_TEXTBOOK: `Bạn hãy quan sát và phân tích toàn diện các hình ảnh/trang SGK Toán được giáo viên cung cấp.
Chủ đề bài học: "{topic}" (Môn học: {subject}).

HÃY PHÂN TÍCH VÀ TRÍCH XUẤT NỘI DUNG VỚI CÁC MỤC SAU:
1. **Tổng quan bài học:** Tên bài, vị trí trong chương trình và mục tiêu cần đạt cốt lõi theo SGK.
2. **Khung kiến thức trọng tâm:**
   - Các định nghĩa, khái niệm, thuật ngữ mới theo SGK cung cấp.
   - Các quy tắc, công thức toán học, định lí, tính chất (viết bằng LaTeX $...$).
   - Các quy ước, chú ý sư phạm quan trọng.
3. **Chuỗi hoạt động khám phá trong SGK:**
   - Hoạt động mở đầu (tình huống, hình ảnh thực tế gắn với cuộc sống).
   - Các hoạt động hình thành kiến thức (HĐ khám phá 1, HĐ 2, các câu hỏi gợi mở, ví dụ mẫu kèm lời giải).
   - Hoạt động luyện tập (các bài Luyện tập, Tranh luận, Thử thách nhỏ trong SGK).
   - Hoạt động vận dụng (các bài toán thực tế, dự án gắn kết tri thức với cuộc sống).
4. **Hệ thống bài tập cuối bài:**
   - Tóm tắt đề bài các bài tập cơ bản và nâng cao trong SGK.
5. **Đề xuất của Chuyên gia Sư phạm (chỉ gắn đúng nội dung đã đọc, không thêm kiến thức mới):**
   - Những điểm học sinh dễ mắc sai lầm, hiểu sai bản chất ngay trên các khái niệm/bài tập vừa trích.
   - Cơ hội tích hợp số/AI chỉ khi thành phần đó được bật trong bối cảnh sư phạm.

Hãy trình bày rõ ràng, mạch lạc, giữ nguyên vẹn các công thức toán bằng định dạng LaTeX.`,

  // TAB 2: MỤC TIÊU BÀI HỌC (I. MỤC TIÊU)
  GENERATE_OBJECTIVES: `Hãy xây dựng phần **I. MỤC TIÊU** cho Kế hoạch bài dạy chuẩn Công văn 5512/BGDĐT-GDTrH, bám CT GDPT 2018.
- Môn học: {subject}
- Tên bài dạy: {topic}
- Thời lượng dự kiến: {duration}
- Dữ liệu nội dung SGK (nếu có):
"""
{textbook_content}
"""
- YCCĐ chính thức CT GDPT 2018 / Thông tư 32/2018/TT-BGDĐT (nếu có):
"""
{yccd_official}
"""

QUY TẮC MỤC TIÊU KIẾN THỨC (KHÔNG TỰ TẠO):
- Mục ## 1. Về kiến thức PHẢI là Yêu cầu cần đạt của CT GDPT 2018 ban hành kèm Thông tư 32/2018/TT-BGDĐT cho đúng môn/lớp/bài.
- Nếu khối {yccd_official} có nội dung: chỉ chọn và viết lại nguyên ý các YCCĐ khớp bài; không thêm kiến thức ngoài danh sách.
- Nếu khối YCCĐ trống: chỉ lấy YCCĐ in trên SGK/nguồn Tab 1. Nếu nguồn không nêu YCCĐ, ghi các ý kiến thức có trong nguồn và thêm dòng "Cần đối chiếu YCCĐ CT GDPT 2018 (TT 32) cho bài này" — CẤM bịa thang Bloom Nhận biết/Thông hiểu/Vận dụng không có trong nguồn.

QUY TẮC BẮT BUỘC VỀ SỐ LƯỢNG NĂNG LỰC VÀ PHẨM CHẤT (Bài dạy 1–2 tiết):
- Mục 2.a (Năng lực chung): CHỈ 1–2 năng lực chung. CẤM liệt kê cả 3.
- Mục 2.b (Năng lực đặc thù môn học): CHỈ 2–3 năng lực đặc thù nổi trội. CẤM liệt kê hết khung.
- Mục 3 (Phẩm chất): CHỈ 1–2 phẩm chất. CẤM đủ 5 phẩm chất.
- Năng lực số: chỉ khi được bật; PHẢI liệt kê đủ từng miền đã chọn; mỗi mục 1 dòng \`- Tên miền: mô tả ngắn gắn bài\`. CẤM bỏ miền đã chọn. CẤM gộp NLS+AI thành một hạn ngạch. CẤM bịa miền ngoài danh sách.
- Năng lực AI: chỉ khi được bật; PHẢI liệt kê đủ từng mã đã chọn; mỗi mục 1 dòng \`- Mã: mô tả ngắn gắn bài\`. CẤM bỏ mã đã chọn. CẤM gộp NLS+AI thành một hạn ngạch. CẤM bịa mã ngoài danh sách.
- CẤM xuất HTML, span, style, mã màu. Chỉ Markdown.

CÁCH VIẾT NĂNG LỰC VÀ PHẨM CHẤT (BẮT BUỘC):
- Chỉ MÔ TẢ năng lực/phẩm chất bằng một dòng cho mỗi mục: \`- Tên năng lực: mô tả ngắn gắn đúng bài học.\`
- CẤM các nhãn **Biểu hiện**, **Nhiệm vụ/Sản phẩm**, **Minh chứng**. Không dùng ý con \`+ \`. Không tách thành 2–3 gạch con dưới mỗi năng lực.
- Không liệt kê hết bài tập SGK; không viết công thức/tên tập hợp rời từng dòng.

# I. MỤC TIÊU

## 1. Về kiến thức
(Viết các YCCĐ CT GDPT 2018 / TT 32 hoặc YCCĐ in trên SGK; mỗi ý một gạch đầu dòng, giữ động từ YCCĐ.)

## 2. Về năng lực
### a) Năng lực chung
- Tự chủ và tự học: ...
- Giao tiếp và hợp tác: ...

### b) Năng lực đặc thù môn học
- [Tên năng lực đặc thù]: ...

### c) Năng lực số (CHỈ khi bối cảnh bật; đúng miền TT 02 đã chọn — đủ từng miền)
- [Tên miền 1]: ...
- [Tên miền 2]: ...
- [Tên miền 3 nếu đã chọn]: ...

### d) Năng lực AI (CHỈ khi bối cảnh bật; đúng mã QĐ 2422 đã chọn — đủ từng mã)
- [Mã 1]: ...
- [Mã 2]: ...
- [Mã 3 nếu đã chọn]: ...

## 3. Về phẩm chất & Giáo dục hòa nhập (hòa nhập chỉ khi được bật)
- [Tên phẩm chất]: mô tả ngắn gắn bài.`,

  // TAB 3: THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU (II. THIẾT BỊ & HỌC LIỆU)
  GENERATE_MATERIALS: `Hãy xây dựng phần **II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU** cho Kế hoạch bài dạy môn Toán THCS chuẩn Công văn 5512 theo GDPT 2018.
- Môn học: {subject}
- Tên bài dạy: {topic}
- Dữ liệu nội dung SGK (nếu có):
"""
{textbook_content}
"""

CHỈ tạo danh mục thiết yếu, ngắn gọn để GV và HS chuẩn bị cho đúng bài: tối đa 2 ý lớn cho mỗi đối tượng, mỗi ý lớn tối đa 3 ý con. Không liệt kê nhãn hiệu, thiết bị thay thế, công cụ số/AI, hoặc học liệu không cần trực tiếp cho bài; chỉ thêm thiết bị số/AI khi bối cảnh sư phạm bật thành phần tương ứng.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU

## 1. Đối với Giáo viên
- SGK, kế hoạch bài dạy và học liệu bám sát nội dung bài.
  + [Tài liệu/hình ảnh/phiếu học tập thực sự cần dùng].
    • [Chi tiết ngắn khi cần phân biệt loại học liệu].
- Thiết bị tổ chức dạy học.
  + [Dụng cụ toán học hoặc thiết bị trình chiếu thực sự dùng trong bài].

## 2. Đối với Học sinh
- SGK, vở ghi và dụng cụ học tập thiết yếu.
  + [Dụng cụ toán học đúng nội dung bài].
- Chuẩn bị trước ở nhà (chỉ khi bài có yêu cầu).
  + [Nhiệm vụ ngắn bám SGK].

Chỉ xuất hai mục trên; thay nội dung trong ngoặc vuông bằng danh mục cụ thể, không giữ nguyên dấu ngoặc vuông.`,

  // TAB 4.A: TIẾN TRÌNH DẠY HỌC - HOẠT ĐỘNG MỞ ĐẦU
  GENERATE_ACTIVITY_A: `Hãy biên soạn chi tiết **HOẠT ĐỘNG MỞ ĐẦU (TIẾP CẬN VẤN ĐỀ)** trong mục III. Tiến trình dạy học chuẩn Công văn 5512 theo GDPT 2018.
- Môn học: {subject}
- Tên bài dạy: {topic}
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
- Tạo tâm thế hứng thú, kích thích trí tò mò, tạo mâu thuẫn nhận thức hoặc nhu cầu tìm hiểu kiến thức mới bám sát tình huống mở đầu của SGK được cung cấp.
- Huy động các kiến thức, kĩ năng đã học có liên quan đến nội dung bài mới.

### b) Nội dung:
(Mô tả chi tiết tình huống thực tiễn / câu đố / trò chơi học tập / bài toán mở đầu / hình ảnh trực quan gắn liền với cuộc sống mà GV đưa ra cho HS thực hiện).

### c) Sản phẩm:
(Mô tả cụ thể câu trả lời, kết quả dự đoán, sản phẩm tính toán ban đầu hoặc câu hỏi băn khoăn của học sinh khi đối diện tình huống).

### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ: GV giao tình huống/hình/câu hỏi đúng nguồn.<br>+ Bước 2: Thực hiện nhiệm vụ: HS quan sát, thảo luận; GV hỗ trợ.<br>+ Bước 3: Báo cáo, thảo luận: HS phát biểu; lớp nhận xét; GV chuẩn hóa.<br>+ Bước 4: Kết luận, nhận định: GV chốt và dẫn vào bài mới. | - Trong Toán học, nhóm các đối tượng xác định được gọi là tập hợp.<br>- Bài học hôm nay nghiên cứu khái niệm tập hợp. |`,

  // TAB 4.B: TIẾN TRÌNH DẠY HỌC - HOẠT ĐỘNG HÌNH THÀNH KIẾN THỨC MỚI
  GENERATE_ACTIVITY_B: `Hãy biên soạn chi tiết toàn bộ **HOẠT ĐỘNG HÌNH THÀNH KIẾN THỨC MỚI** trong mục III. Tiến trình dạy học chuẩn Công văn 5512 theo GDPT 2018.
- Môn học: {subject}
- Tên bài dạy: {topic}
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
- Bám sát mạch kiến thức và các hoạt động khám phá trong SGK, dữ liệu bài học do giáo viên cung cấp.
- Chia bài học thành các đơn vị kiến thức nhỏ rõ ràng (ví dụ: Hoạt động 2.1: Khái niệm...; Hoạt động 2.2: Định lí/Tính chất...; Hoạt động 2.3: Quy tắc...).
- MỖI ĐƠN VỊ KIẾN THỨC ĐỀU PHẢI CÓ ĐẦY ĐỦ 4 THÀNH PHẦN: a) Mục tiêu, b) Nội dung, c) Sản phẩm, d) Tổ chức thực hiện (4 bước: Chuyển giao -> Thực hiện -> Báo cáo thảo luận -> Kết luận nhận định).
- Sản phẩm và Kết luận nhận định PHẢI CÓ LỜI GIẢI TOÁN HỌC CHI TIẾT, CÔNG THỨC LATEX HOÀN CHỈNH, ĐỊNH NGHĨA/ĐỊNH LÍ CHÍNH XÁC ĐỂ HS GHI VỞ.

CẤU TRÚC MẪU:

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI

### 1. Hoạt động 2.1: [Tên đơn vị kiến thức 1]
#### a) Mục tiêu:
- Học sinh hình thành được khái niệm / nhận biết được...
#### b) Nội dung:
- Học sinh thực hiện hoạt động khám phá / đọc hiểu thông tin trong SGK.
#### c) Sản phẩm:
- Kết quả câu trả lời, lời giải chi tiết cho các câu hỏi khám phá:
  + (Trình bày chi tiết các phép toán, công thức LaTeX $...$).
#### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ: GV giao HĐ/câu hỏi khám phá đúng SGK.<br>+ Bước 2: Thực hiện nhiệm vụ: HS khám phá; GV hỗ trợ.<br>+ Bước 3: Báo cáo, thảo luận: Đại diện trình bày; lớp phản biện; GV chuẩn hóa.<br>+ Bước 4: Kết luận, nhận định: GV chốt kiến thức ghi bảng. | **1. [Tên kiến thức]**<br>- Định nghĩa: ...<br>- Ký hiệu / công thức: $...$<br>+ Chú ý: ... |

### 2. Hoạt động 2.2: [Tên đơn vị kiến thức 2]
(Tương tự đầy đủ 4 phần a, b, c, d với các bước chi tiết và ví dụ áp dụng...)

### 3. Hoạt động 2.3: [Nếu bài có thêm đơn vị kiến thức 3...]`,

  // TAB 4.C: TIẾN TRÌNH DẠY HỌC - HOẠT ĐỘNG LUYỆN TẬP
  GENERATE_ACTIVITY_C: `Hãy biên soạn chi tiết **HOẠT ĐỘNG LUYỆN TẬP** trong mục III. Tiến trình dạy học chuẩn Công văn 5512 theo GDPT 2018.
- Môn học: {subject}
- Tên bài dạy: {topic}
- Mục tiêu và Kiến thức trọng tâm:
"""
{objectives_content}
"""
- Dữ liệu SGK / bài tập nguồn:
"""
{textbook_content}
"""

YÊU CẦU BIÊN SOẠN:
${ACTIVITY_TABLE_CONTRACT}
- CHỈ dùng bài luyện tập / câu hỏi / HĐ có trong SGK hoặc dữ liệu giáo viên cung cấp. CẤM invent trắc nghiệm 4 lựa chọn, cấm bịa đề không có trong nguồn.
- Phải đọc khối dữ liệu SGK ở trên trước. Chỉ ghi "[Không có trong tài liệu đã cung cấp]" ở mục b) và c) khi khối đó không có bài/câu/luyện tập; vẫn xuất bảng d) với nhiệm vụ đối chiếu vở/SGK.
- Nếu khối dữ liệu SGK trên có “Bài”, “Luyện tập”, đề toán thì CẤM ghi "[Không có trong tài liệu đã cung cấp]"; phải chép hoặc tóm tắt đề có trong nguồn.
- Lời giải chi tiết chỉ viết khi nguồn có dữ liệu đủ để giải; không bịa số liệu.

CẤU TRÚC:

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (Khoảng 12 - 15 phút)

### a) Mục tiêu:
- Củng cố kiến thức vừa học bằng đúng các bài/câu có trong nguồn.

### b) Nội dung:
- Liệt kê nguyên đề các bài/câu luyện tập có trong nguồn (kèm số bài/trang nếu nguồn có).

### c) Sản phẩm:
- Lời giải/đáp án chỉ khi có trong nguồn hoặc suy ra trực tiếp từ kiến thức nguồn.

### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ: GV giao đúng các bài/câu có trong nguồn.<br>+ Bước 2: Thực hiện nhiệm vụ: HS làm bài; GV hỗ trợ.<br>+ Bước 3: Báo cáo, thảo luận: HS trình bày; lớp nhận xét.<br>+ Bước 4: Kết luận, nhận định: GV chốt lỗi sai và kĩ năng. | **Luyện tập**<br>- Đề bài (đúng SGK).<br>- Đáp án chốt: $...$ |`,

  // TAB 4.D: TIẾN TRÌNH DẠY HỌC - HOẠT ĐỘNG VẬN DỤNG
  GENERATE_ACTIVITY_D: `Hãy biên soạn chi tiết **HOẠT ĐỘNG VẬN DỤNG** trong mục III. Tiến trình dạy học chuẩn Công văn 5512 theo GDPT 2018.
- Môn học: {subject}
- Tên bài dạy: {topic}
- Mục tiêu bài học:
"""
{objectives_content}
"""
- Dữ liệu SGK / bài tập nguồn:
"""
{textbook_content}
"""

YÊU CẦU BIÊN SOẠN:
${ACTIVITY_TABLE_CONTRACT}
- CHỈ dùng bài vận dụng / tình huống / dự án có trong SGK hoặc dữ liệu giáo viên. CẤM invent số liệu, đề thực tiễn hay bài liên môn không có trong nguồn.
- Phải đọc khối dữ liệu SGK ở trên trước. Chỉ ghi "[Không có trong tài liệu đã cung cấp]" khi khối đó không có bài/câu/vận dụng.
- Nếu khối dữ liệu SGK trên có “Bài”, “Luyện tập”, “Vận dụng”, đề toán thì CẤM ghi "[Không có trong tài liệu đã cung cấp]"; phải chép hoặc tóm tắt đề có trong nguồn.
- Chỉ tích hợp công cụ số/AI khi bối cảnh sư phạm bật thành phần tương ứng.

CẤU TRÚC:

## D. HOẠT ĐỘNG 4: VẬN DỤNG (Khoảng 5 - 8 phút hoặc giao về nhà)

### a) Mục tiêu:
- Vận dụng đúng nội dung bài theo nhiệm vụ có trong nguồn.

### b) Nội dung:
- Tình huống/bài vận dụng nguyên văn hoặc tóm tắt sát nguồn.

### c) Sản phẩm:
- Sản phẩm/lời giải chỉ khi nguồn cho phép; không bịa số liệu.

### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ: GV giao đúng nhiệm vụ vận dụng có trong nguồn.<br>+ Bước 2: Thực hiện nhiệm vụ: HS thực hiện; GV hỗ trợ.<br>+ Bước 3: Báo cáo, thảo luận: Đại diện trình bày.<br>+ Bước 4: Kết luận, nhận định: GV chốt ý nghĩa bài học. | **Vận dụng**<br>- Đề/tình huống (đúng SGK).<br>- Kết quả/đáp án chốt ghi bảng. |`,

  // TAB 4.E: KẾ HOẠCH KIỂM TRA - ĐÁNH GIÁ (MA TRẬN & RUBRICS)
  GENERATE_ASSESSMENT: `Hãy biên soạn **E. KẾ HOẠCH KIỂM TRA - ĐÁNH GIÁ** cho Kế hoạch bài dạy môn Toán THCS chuẩn CV 5512.
- Môn học: {subject}
- Tên bài dạy: {topic}
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
  GENERATE_PORTFOLIO: `Hãy thiết kế **F. HỒ SƠ DẠY HỌC (CÁC PHIẾU HỌC TẬP)** cho Kế hoạch bài dạy môn Toán THCS.
- Môn học: {subject}
- Tên bài dạy: {topic}
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
### BÀI HỌC: {topic} (SGK Toán do giáo viên cung cấp)

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
  GENERATE_HOMEWORK: `Hãy biên soạn chi tiết **G. HƯỚNG DẪN VỀ NHÀ** trong Kế hoạch bài dạy môn Toán THCS chuẩn CV 5512.
- Môn học: {subject}
- Tên bài dạy: {topic}
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
- Hoàn thành các bài tập trong SGK Toán: Bài ... trang ...
- Hoàn thành bài tập trong Sách bài tập Toán: Bài ... trang ...
- **Bài tập mở rộng / Nâng cao (Dành cho HS khá, giỏi):** (Đưa ra 1 bài toán mở rộng có tính tư duy cao kèm gợi ý ngắn gọn).

## 3. Nhiệm vụ chuẩn bị cho bài học tiếp theo
- Đọc trước bài mới theo SGK Toán do giáo viên sử dụng.
- Chuẩn bị đầy đủ dụng cụ học tập: thước đo góc, compa, bảng nhóm... cho tiết học sau.
- Tìm hiểu các ví dụ thực tế liên quan đến bài học tiếp theo.

## 4. Gợi ý Câu lệnh Prompt AI hỗ trợ học sinh tự học tại nhà an toàn (CHỈ tạo khi bối cảnh sư phạm bật năng lực AI)
(Cung cấp 2-3 mẫu câu lệnh mẫu để HS có thể hỏi trợ lý AI như Gemini/ChatGPT/NotebookLM khi gặp khó khăn lúc tự học ở nhà, nhưng rèn luyện tính tư duy chứ không hỏi thẳng đáp án).
- *Mẫu Prompt 1 (Giải thích lại khái niệm):* "Em là học sinh lớp {grade}, em chưa hiểu rõ về [khái niệm trong bài]. Bạn hãy giải thích lại bằng một ví dụ thực tế gần gũi, đơn giản nhất nhé!"
- *Mẫu Prompt 2 (Gợi ý từng bước):* "Em đang giải bài toán [chép đề bài]. Em chưa biết bắt đầu từ đâu, bạn hãy cho em 2 câu hỏi gợi ý để em tự tìm ra hướng giải, đừng giải hộ em nhé!"
- *Mẫu Prompt 3 (Kiểm tra lời giải):* "Đây là lời giải của em cho bài toán [bài toán]: [lời giải]. Bạn hãy nhận xét xem em đã làm đúng chưa và chỉ ra bước nào cần khắc phục nhé!"`
};

function getSystemRole(subjectId, grade) {
  const subjectNameObj = (typeof CURRICULUM_DATA !== 'undefined' ? CURRICULUM_DATA.subjects.find(s => s.id === subjectId) : null) || { name: 'Môn học' };
  const subjectName = subjectNameObj.name;
  
  let gradeLevelName = 'THCS';
  let isPrimary = false;
  if (typeof getGradeLevelName !== 'undefined') {
    gradeLevelName = getGradeLevelName(grade);
    isPrimary = getGradeLevel(grade) === 'tieu-hoc';
  }
  const cvDoc = isPrimary ? 'CV 2345' : 'Công văn 5512/BGDĐT';
  
  let compList = '';
  if (typeof SUBJECT_COMPETENCIES !== 'undefined' && SUBJECT_COMPETENCIES[subjectId]) {
    compList = SUBJECT_COMPETENCIES[subjectId].join('; ');
  }
  
  const latexSubjects = ['toan', 'vatly', 'hoahoc', 'tinhoc'];
  const needsLatex = latexSubjects.includes(subjectId);
  const latexRule = needsLatex 
    ? "- Công thức, phương trình PHẢI được viết bằng mã LaTeX chuẩn: công thức trong dòng dùng $công_thức$, công thức khối dùng $$công_thức$$. Ví dụ: $x^2 + 2x + 1 = 0$, $\\frac{a}{b}$, $\\sqrt{x}$."
    : "- Trình bày văn bản thuần túy, rõ ràng. Không dùng LaTeX trừ khi thật sự cần thiết.";

  return `Bạn là Chuyên gia Sư phạm Môn ${subjectName}, Cấp ${gradeLevelName}, nắm vững:
- Chương trình GDPT 2018 (${cvDoc} cho cấp ${gradeLevelName})
- Khung Năng lực đặc thù: ${compList}
- 5 phẩm chất chủ yếu và phương pháp dạy học hòa nhập cho học sinh khó khăn/chậm tiến độ.

QUY TẮC BẮT BUỘC KHI XUẤT NỘI DUNG:
- Bám sát GDPT 2018 và nội dung bài học do giáo viên cung cấp.
- Định dạng Markdown rõ ràng, phân cấp tiêu đề bằng #, ##, ###, #### hợp lý.
${latexRule}
- Nội dung phải chi tiết, đầy đủ, thiết thực cho giáo viên lên lớp, tuyệt đối KHÔNG viết tóm tắt qua loa, KHÔNG để dấu '...' hoặc 'tương tự'.
- Tuân thủ tuyệt đối bối cảnh và ràng buộc sư phạm được cung cấp trong từng yêu cầu; không tự bổ sung năng lực số, AI, ngoại ngữ hoặc hỗ trợ hòa nhập nếu không được chọn.
- Mục tiêu kiến thức phải bám YCCĐ CT GDPT 2018 / Thông tư 32/2018/TT-BGDĐT; không tự tạo kiến thức ngoài nguồn.`;
}

function getPromptTemplate(templateKey, context) {
  // Use PROMPTS[templateKey] as base, but replace hardcoded "Toán" with subject name
  let baseTemplate = PROMPTS[templateKey];
  if (!baseTemplate) return '';

  const subjectName = context.subjectName || 'Môn học';
  const gradeLevelName = context.gradeLevelName || 'THCS';
  
  // Replace hardcoded strings to make it generic
  baseTemplate = baseTemplate
    .replace(/môn Toán THCS/g, `môn ${subjectName} ${gradeLevelName}`)
    .replace(/Môn Toán THCS/g, `Môn ${subjectName} ${gradeLevelName}`)
    .replace(/môn Toán/g, `môn ${subjectName}`)
    .replace(/Môn Toán/g, `Môn ${subjectName}`)
    .replace(/Toán học/g, `${subjectName}`)
    .replace(/toán học/g, `${subjectName}`)
    .replace(/bài toán/g, `bài tập/nhiệm vụ`)
    .replace(/SGK Toán/g, `SGK ${subjectName}`)
    .replace(/Sách bài tập Toán/g, `Sách bài tập ${subjectName}`)
    .replace(/toán/g, `bài tập`) // be careful with this, but it's ok for fallback
    .replace(/GeoGebra/g, context.subject === 'toan' ? 'GeoGebra' : 'phần mềm mô phỏng phù hợp')
    .replace(/Casio fx-580VN X/g, context.subject === 'toan' || context.subject === 'vatly' || context.subject === 'hoahoc' ? 'Máy tính cầm tay' : 'thiết bị phù hợp')
    .replace(/vẽ hình, biến đổi đại số/g, 'kĩ năng đặc thù của môn học');

  // Insert competencies
  const competencies = context.competencies ? context.competencies.join('; ') : '';
  
  // Replace placeholders
  let result = baseTemplate
    .replace(/\{subject\}/g, subjectName)
    .replace(/\{topic\}/g, context.topic || '')
    .replace(/\{duration\}/g, context.duration || '')
    .replace(/\{textbook_content\}/g, context.textbook_content || '')
    .replace(/\{objectives_content\}/g, context.objectives_content || '')
    .replace(/\{activities_content\}/g, context.activities_content || '')
    .replace(/\{yccd_official\}/g, context.yccd_official || '')
    .replace(/\{grade\}/g, context.grade || '')
    .replace(/\{competencies\}/g, competencies);

  if (PROMPTS.SOURCE_LOCK) {
    result += `\n\n${PROMPTS.SOURCE_LOCK}`;
  }

  // Append pedagogical context if provided
  if (context.pedagogical_context) {
    result += `\n\nBỐI CẢNH SƯ PHẠM VÀ RÀNG BUỘC BẮT BUỘC:\n${context.pedagogical_context}`;
  }

  if (templateKey === 'GENERATE_OBJECTIVES') {
    result += `\n\nQUY TẮC VIẾT NĂNG LỰC / PHẨM CHẤT:
- Mỗi năng lực hoặc phẩm chất chỉ MỘT dòng: \`- Tên: mô tả ngắn gắn bài.\`
- CẤM nhãn Biểu hiện, Nhiệm vụ/Sản phẩm, Minh chứng. CẤM ý con bắt đầu bằng + .
- Năng lực chung 1–2; đặc thù 2–3; phẩm chất 1–2.
- NLS phải liệt kê đủ từng miền đã chọn; AI phải liệt kê đủ từng mã đã chọn; mỗi mục 1 dòng \`- Tên/Mã: mô tả ngắn gắn bài\`. CẤM bỏ mục đã chọn. CẤM gộp NLS+AI thành một hạn ngạch.`;
  }

  return result;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { PROMPTS, getSystemRole, getPromptTemplate };
}
