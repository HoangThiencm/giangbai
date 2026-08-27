/**
 * js/khbd-prompts.js
 * Hệ thống Siêu Prompt Sư phạm Đa Môn Học (Lớp 1–12) chuẩn Công văn 5512/BGDĐT-GDTrH,
 * Dùng cho SGK và học liệu do giáo viên cung cấp.
 * Tích hợp Kịch bản Sư phạm Thực chiến (Actionable Classroom Script),
 * Khung Năng lực Chung theo đặc thù môn học (CT GDPT 2018 - TT 32/2018/TT-BGDĐT),
 * Khung Năng lực Đặc thù, Khung Năng lực AI (QĐ 2422/QĐ-BGDĐT) và Khung Năng lực Số (TT 02/2025/TT-BGDĐT).
 */

/**
 * Lấy danh sách Năng lực chung phù hợp nhất theo đặc thù môn học (CT GDPT 2018).
 * @param {string} subjectId - Mã môn học (toan, nguvan, khtn, vatly, hoahoc, sinhhoc, lichsudialy, gdcd, tinhoc, congnghe, tienganh, amnhac, mithuat, gdtc, hdtn-hn...)
 * @returns {Array<{name: string, guide: string}>} Danh sách năng lực chung ưu tiên kèm định hướng hành vi
 */
function getGeneralCompetenciesForSubject(subjectId) {
  const sid = String(subjectId || '').toLowerCase();
  
  if (['toan', 'khtn', 'vatly', 'hoahoc', 'sinhhoc', 'khoahoc', 'tinhoc', 'congnghe'].includes(sid)) {
    return [
      { name: 'Giải quyết vấn đề và sáng tạo', guide: 'phát hiện mâu thuẫn/quy luật từ tình huống bài học, đề xuất hướng giải quyết/mô hình hóa và tìm phương án tối ưu' },
      { name: 'Tự chủ và tự học', guide: 'tự lực thực hiện các nhiệm vụ khám phá, tính toán, kiểm tra kết quả và ghi chép hệ thống kiến thức' },
      { name: 'Giao tiếp và hợp tác', guide: 'thảo luận nhóm, sử dụng thuật ngữ/ký hiệu chuyên môn để diễn đạt cách giải và phản biện kết quả' }
    ];
  }
  
  if (['nguvan', 'tiengviet', 'tienganh', 'gdcd', 'daoduc', 'gdktpl', 'lichsu', 'dialy', 'lichsudialy', 'lichsudialy-th'].includes(sid)) {
    return [
      { name: 'Giao tiếp và hợp tác', guide: 'sử dụng ngôn ngữ mạch lạc để trình bày quan điểm, lắng nghe, phản biện và thấu cảm ý kiến trong thảo luận nhóm' },
      { name: 'Tự chủ và tự học', guide: 'chủ động đọc hiểu văn bản/tư liệu, tra cứu thông tin và tự liên hệ bài học vào thực tế bản thân' },
      { name: 'Giải quyết vấn đề và sáng tạo', guide: 'phân tích tình huống xã hội/ngữ cảnh văn bản, đề xuất cách xử lý tình huống hoặc liên hệ rút ra thông điệp mới' }
    ];
  }
  
  if (['amnhac', 'mithuat', 'gdtc', 'hdtn', 'hdtn-hn'].includes(sid)) {
    return [
      { name: 'Giải quyết vấn đề và sáng tạo', guide: 'thể hiện ý tưởng thẩm mĩ, sáng tạo sản phẩm nghệ thuật hoặc phương án vận động linh hoạt' },
      { name: 'Giao tiếp và hợp tác', guide: 'phối hợp nhịp nhàng với bạn trong các hoạt động nhóm, biểu diễn tập thể hoặc thi đua đồng đội' },
      { name: 'Tự chủ và tự học', guide: 'tự giác rèn luyện kỹ năng, tự tin thể hiện trước tập thể và biết tự đánh giá sự tiến bộ' }
    ];
  }
  
  return [
    { name: 'Tự chủ và tự học', guide: 'chủ động thực hiện nhiệm vụ học tập được giao bám sát nội dung bài' },
    { name: 'Giao tiếp và hợp tác', guide: 'tích cực trao đổi, thảo luận nhóm để hoàn thành sản phẩm học tập' },
    { name: 'Giải quyết vấn đề và sáng tạo', guide: 'vận dụng kiến thức bài học để giải quyết nhiệm vụ/bài tập thực tế' }
  ];
}

function foldCompetencyHay(value) {
  return String(value || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

function reorderGeneralCompetencies(list, context) {
  const items = Array.isArray(list) ? list.slice() : [];
  const methodHay = foldCompetencyHay([
    Array.isArray(context && context.methods) ? context.methods.join(" ") : "",
    Array.isArray(context && context.techniques) ? context.techniques.join(" ") : ""
  ].join(" "));
  const hay = methodHay.trim()
    ? methodHay
    : foldCompetencyHay(context && context.pedagogical_context);
  const talk = /thao luan|tranh bien|hop tac|trinh bay|bao cao|phan bien|khan trai|think-pair|giao tiep/;
  const make = /du an|thuc hanh|do dac|thi nghiem|mo hinh|sang tao|giai quyet/;
  const pick = name => items.find(item => item.name === name);
  if (talk.test(hay) && !make.test(hay)) {
    const first = pick("Giao tiếp và hợp tác");
    if (first) return [first, ...items.filter(item => item !== first)];
  }
  if (make.test(hay) && !talk.test(hay)) {
    const first = pick("Giải quyết vấn đề và sáng tạo");
    if (first) return [first, ...items.filter(item => item !== first)];
  }
  return items;
}

function formatGeneralCompetenciesGuide(subjectId, context) {
  const ordered = reorderGeneralCompetencies(getGeneralCompetenciesForSubject(subjectId), context);
  const top = ordered.slice(0, 2);
  const rest = ordered.slice(2);
  const lines = top.map(item => `- Ưu tiên: **${item.name}**: ${item.guide}.`);
  if (rest.length) {
    lines.push(`Năng lực còn lại (${rest.map(item => item.name).join(", ")}): chỉ chọn nếu bài thực sự thể hiện rõ; CẤM liệt kê cho đủ khung.`);
  }
  return lines.join("\n");
}

const ACTIVITY_TABLE_CONTRACT = `YÊU CẦU BẮT BUỘC: KỊCH BẢN SƯ PHẠM THỰC CHIẾN TRONG BẢNG 2 CỘT (Chuẩn CV 5512 & GDPT 2018):
- Mục a) Mục tiêu, b) Nội dung, c) Sản phẩm: dùng 3 cấp danh sách: ý lớn \`-\`, ý con \`+\`, ý chi tiết \`.\`.
- Mục d) Tổ chức thực hiện: BẮT BUỘC ĐÚNG MỘT bảng Markdown 2 cột, tiêu đề:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
- Bảng Markdown CHỈ GỒM ĐÚNG 1 HÀNG DỮ LIỆU DUY NHẤT (CẤM tách thành 4 hàng riêng).
- CỘT TRÁI — KỊCH BẢN THỰC CHIẾN PHÂN VAI RÕ RÀNG (ngăn các bước bằng <br>):
  + Đủ 4 bước chuẩn Công văn 5512:
    * + Bước 1: Chuyển giao nhiệm vụ: nêu kỹ thuật dạy học, GV nói câu lệnh trong ngoặc kép, HS tiếp nhận.
    * + Bước 2: Thực hiện nhiệm vụ: HS làm cá nhân rồi thảo luận; GV quan sát và hỗ trợ phân hóa.
    * + Bước 3: Báo cáo, thảo luận: HS báo cáo, phản biện; GV điều hành.
    * + Bước 4: Kết luận, nhận định: GV chốt kiến thức; HS ghi bài.
  + Trong từng bước, BẮT BUỘC nêu tên Kỹ thuật/Phương pháp dạy học được áp dụng và PHÂN VAI RÕ RÀNG:
    * **GV (Giáo viên):** 
      - Nói câu lệnh/câu hỏi trực tiếp trong ngoặc kép (câu lệnh giao việc rõ ràng, câu hỏi phát vấn gợi mở hoặc câu hỏi phân hóa đào sâu bản chất).
      - Hành động cụ thể: phát phiếu học tập/dụng cụ, chia nhóm, kiểm soát thời gian.
      - **BẮT BUỘC dự kiến lỗi sai điển hình / ngộ nhận** gắn đúng khái niệm, ví dụ hoặc bài tập đang dạy trong PDF/ảnh SGK (nêu thuật ngữ hoặc số bài). CẤM lỗi generic lặp lại mọi bài. Nếu nguồn không cho thấy ngộ nhận điển hình, viết một câu: "Dự kiến: nhầm [thuật ngữ X trong SGK] với [thuật ngữ Y trong SGK]". Can thiệp hỗ trợ phân hóa: hướng dẫn HS gặp khó khăn, đặt câu hỏi mở rộng cho HS khá giỏi.
    * **HS (Học sinh):** 
      - Hành động cụ thể theo 3 pha: (1) Thao tác cá nhân theo phút vào vở/nháp/phiếu -> (2) Thảo luận cặp/nhóm theo phút tạo **sản phẩm trung gian** (bảng phụ, phiếu học tập, sơ đồ tư duy, giấy A0, sticky note) -> (3) Đại diện báo cáo và phản biện trước lớp.
  + KỊCH BẢN TÍCH HỢP NĂNG LỰC SỐ (NLS) VÀ NĂNG LỰC AI (khi được bật trong bối cảnh sư phạm):
    * **Khi có NLS (TT 02/2025):** Thể hiện rõ hành động của GV (hướng dẫn công cụ số/phần mềm: GeoGebra, bảng tính điện tử, máy tính cầm tay, phần mềm mô phỏng) và HS (trực tiếp thao tác trên thiết bị, khai thác dữ liệu số) kèm marker **[NLS: {Miền/Mã} - {Hành vi/Công cụ}]** (hoặc **[NLS]**).
    * **Khi có AI (QĐ 2422):** Thể hiện rõ hành động của GV (giao câu lệnh Prompt AI cụ thể trong ngoặc kép "...", lưu ý giới hạn an toàn) và HS (thực hành chạy prompt, BẮT BUỘC có bước so sánh, đối chiếu, kiểm chứng kết quả của AI với SGK/toán học chuẩn mực để phát hiện sai lệch/ảo giác) kèm marker **[AI: {Mã} - {Câu lệnh/Kiểm chứng}]** (hoặc **[AI]**).
- CỘT PHẢI — NỘI DUNG GHI BẢNG (Kiến thức chuẩn mực chốt cho HS chép vào vở):
  + Tên mục kiến thức, định nghĩa, định lý, quy tắc, công thức LaTeX ($...$, $$...$$), chú ý quan trọng, ví dụ mẫu kèm đề bài và lời giải chi tiết từng bước. Dùng \`-\`, \`+\`, \`.\`; ngăn các dòng bằng \`<br>\`.
  + CỘT PHẢI CẤM: mô tả hành vi GV/HS, CẤM viết "GV yêu cầu", "HS thảo luận", CẤM để trống, CẤM để dấu "..." hay "[...]".
- CẤM để trống ô. Escape dấu | trong văn bản thành \\|.
- Hoạt động B: Mỗi tiểu mục/nội dung kiến thức dùng một bảng 2 cột (1 hàng) độc lập như trên.`;

const PROMPTS = {
  // SYSTEM INSTRUCTION
  SYSTEM_ROLE: `Bạn là Chuyên gia Sư phạm Cao cấp, phụ trách môn {subject} Cấp {gradeLevelName}, nắm vững:
1. Chương trình Giáo dục Phổ thông (GDPT) 2018 theo Thông tư số 32/2018/TT-BGDĐT.
2. Công văn số 5512/BGDĐT-GDTrH của Bộ Giáo dục và Đào tạo về xây dựng Kế hoạch bài dạy (Giáo án).
3. Khung Năng lực Chung (Tự chủ & tự học; Giao tiếp & hợp tác; Giải quyết vấn đề & sáng tạo) được phân bổ linh hoạt theo đặc thù môn học.
4. Khung Năng lực Đặc thù môn {subject}.
5. Khung Năng lực Trí tuệ Nhân tạo (AI) theo Quyết định số 2422/QĐ-BGDĐT (khi được chọn).
6. Khung Năng lực Số theo Thông tư số 02/2025/TT-BGDĐT (khi được chọn).
7. 5 phẩm chất chủ yếu (Yêu nước, Nhân ái, Chăm chỉ, Trung thực, Trách nhiệm) và phương pháp dạy học hòa nhập/phân hóa.

QUY TẮC BẮT BUỘC KHI XUẤT NỘI DUNG:
- Bám sát GDPT 2018 và nội dung SGK, dữ liệu bài học do giáo viên cung cấp; không tự gán nhà xuất bản hay bộ sách nếu không có trong dữ liệu.
- Kế hoạch bài dạy phải là một KỊCH BẢN LỚP HỌC THỰC CHIẾN: Giáo viên có câu thoại dẫn dắt trực tiếp trong ngoặc kép "...", hành động sư phạm rõ ràng; Học sinh có thao tác cụ thể, sản phẩm rõ nét; chỉ ra lỗi sai điển hình và cách xử lý sư phạm.
- Thiết kế mục tiêu tinh gọn cho bài dạy 1–2 tiết: chọn 1–2 năng lực chung cốt lõi phù hợp đặc thù môn học, 2–3 năng lực đặc thù nổi trội, 1–2 phẩm chất gắn liền nội dung bài.
- Sử dụng tiếng Việt chuẩn mực, sư phạm, trang trọng.
- Định dạng Markdown chuẩn, phân cấp tiêu đề #, ##, ###, #### mạch lạc.
- Công thức khoa học/toán học PHẢI dùng mã LaTeX chuẩn: trong dòng $...$, khối riêng $$...$$.
- Nội dung phải chi tiết, đầy đủ, thiết thực để giáo viên lên lớp dùng được ngay, TUYỆT ĐỐI KHÔNG viết tóm tắt qua loa, TUYỆT ĐỐI KHÔNG để dấu '...' hoặc '[...]' hoặc chữ 'tương tự'.
- TUYỆT ĐỐI KHÔNG xuất lời chào, lời chúc, lời giới thiệu, nhận xét ngoài lề hoặc code block \`\`\`markdown. Bắt đầu ngay bằng tiêu đề bài dạy.`,

  OUTPUT_CONTRACT: `HỢP ĐỒNG ĐẦU RA BẮT BUỘC:
- BẮT ĐẦU NGAY LẬP TỨC bằng tiêu đề/mục chuyên môn phù hợp (ví dụ: # I. MỤC TIÊU, # II. THIẾT BỊ, ## A. HOẠT ĐỘNG 1, v.v.).
- TUYỆT ĐỐI CẤM: lời chào hỏi, khen ngợi, giới thiệu, nhận xét ngoài lề (meta-commentary), lời chúc ở cuối bài (như "Chào thầy cô", "Dưới đây là", "Hy vọng giáo án giúp ích", "Chúc thầy cô thành công", "--- Kết thúc ---").
- TUYỆT ĐỐI CẤM dùng code block fence (\`\`\`markdown hoặc \`\`\`). Chỉ xuất Markdown thuần túy.
- TUYỆT ĐỐI CẤM để lại dấu ba chấm "..." hoặc ngoặc vuông "[...]" chưa điền. Mọi đề bài, câu hỏi, công thức, ví dụ mẫu và lời giải PHẢI ĐƯỢC VIẾT ĐẦY ĐỦ CHI TIẾT.
- Danh sách nội dung có đúng 3 cấp: ý lớn bắt đầu bằng "- ", ý con "+ ", ý chi tiết ". ". Không dùng "1.", "2." làm danh sách nội dung trừ khi là số thứ tự bài tập hoặc bước CV 5512.
- CẤM xuất HTML, thẻ span, thuộc tính style hay mã màu. Màu sắc và font chữ do ứng dụng xử lý.`,

  OUTPUT_REPAIR: `Hãy viết lại nội dung sau thành đúng Markdown của mục Kế hoạch bài dạy chuẩn CV 5512. Bắt đầu ngay bằng tiêu đề/mục chuyên môn; chỉ giữ lại nội dung giáo án. Xóa toàn bộ lời chào, khen ngợi, giới thiệu, meta commentary, lời chúc ở cuối và mọi code fence. Không thêm lời dẫn mới. Danh sách nội dung chỉ dùng "-", "+", ".". Không đổi tiêu đề mục khung như "I.", "## 1.", "a)", "Bước", "Bài".`,

  SOURCE_LOCK: `KHÓA NGUỒN BẮT BUỘC:
- Nguồn chính = văn bản SGK đã nhận diện (Mistral OCR / tóm tắt Bước 0) và/hoặc file PDF/ảnh đính kèm đúng request này.
- CHỈ dùng các trang PDF/ảnh đã chọn (hoặc đúng văn bản OCR của các trang đó). CẤM dùng trang ngoài danh sách.
- Chỉ dùng thêm: tên bài/môn/lớp giáo viên chọn, YCCĐ chính thức (TT 32/2018/TT-BGDĐT — CT GDPT 2018) và bối cảnh lớp học.
- CẤM bịa định nghĩa, định lý, công thức, số liệu, đề bài, đáp án, số trang hoặc nhiệm vụ không có trong nguồn.
- Luyện tập/vận dụng: CHỈ dùng bài, câu, hoạt động có trong PDF/ảnh/OCR đính kèm hoặc dữ liệu SGK. Phải đọc nguồn trước khi giải. Chỉ ghi "[Không có trong tài liệu đã cung cấp]" khi đã đọc kỹ nguồn mà vẫn không có bài/câu vận dụng. CẤM invent trắc nghiệm 4 lựa chọn không có trong sách, không bịa "SBT trang...".
- Mục tiêu kiến thức phải là Yêu cầu cần đạt của CT GDPT 2018 (hoặc YCCĐ in trên đầu bài SGK). Không tự chế thang Bloom ngoài nguồn.`,

  // TAB 1: TÓM TẮT SGK
  ANALYZE_TEXTBOOK: `Hãy đọc PDF/ảnh SGK đính kèm và tóm tắt có cấu trúc cho giáo viên.
Chủ đề bài học: "{topic}" (Môn học: {subject}).

XUẤT TÓM TẮT NGẮN GỌN, RÕ RÀNG:
1. **Tên bài** và mục tiêu cốt lõi (nếu nguồn có ghi).
2. **Tiểu mục kiến thức:** liệt kê tên từng tiểu mục (\`Mục 1: ...\`, \`Mục 2: ...\`); với mỗi mục chỉ nêu loại nội dung (định nghĩa / quy tắc / ví dụ / HĐ khám phá), không chép nguyên văn.
3. **Loại hoạt động/bài tập:** mở đầu, khám phá, luyện tập, vận dụng — ghi rõ số bài/câu nếu nguồn có.

CẤM trích nguyên văn toàn bộ SGK. Tóm tắt ngắn gọn, mạch lạc để giáo viên dễ đối chiếu và kiểm tra.`,

  // TAB 2: MỤC TIÊU BÀI HỌC (I. MỤC TIÊU)
  GENERATE_OBJECTIVES: `Hãy xây dựng phần **I. MỤC TIÊU** cho Kế hoạch bài dạy môn {subject} Cấp {gradeLevelName} chuẩn Công văn 5512/BGDĐT-GDTrH, bám sát CT GDPT 2018.
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
- Gợi ý Năng lực chung theo đặc thù môn {subject}:
{general_competencies_guide}

QUY TẮC MỤC TIÊU KIẾN THỨC:
- Mục ## 1. Về kiến thức PHẢI là Yêu cầu cần đạt (YCCĐ) của CT GDPT 2018 ban hành kèm Thông tư 32/2018/TT-BGDĐT cho đúng môn/lớp/bài.
- Nếu khối YCCĐ chính thức có nội dung: chọn và viết lại nguyên ý các YCCĐ khớp bài; giữ nguyên các động từ hành vi của YCCĐ.
- Nếu khối YCCĐ trống: lấy YCCĐ in trên SGK/nguồn.

QUY TẮC NĂNG LỰC CHUNG (CĂN CỨ VÀO MÔN HỌC & BÀI HỌC):
- Mục 2.a (Năng lực chung): CHỈ CHỌN 1–2 năng lực chung phù hợp nhất với bản chất môn {subject} và bài dạy này (ví dụ môn Toán/KHTN ưu tiên "Giải quyết vấn đề và sáng tạo" + "Tự chủ và tự học"; môn Ngữ văn/Ngoại ngữ/GDCD ưu tiên "Giao tiếp và hợp tác" + "Tự chủ và tự học"). CẤM rập khuôn máy móc, CẤM liệt kê cả 3.
- Mỗi năng lực chung viết đúng 1 dòng: \`- [Tên năng lực]: [mô tả hành vi cụ thể học sinh thực hiện trong bài học này]\`. CẤM nhãn Biểu hiện / Minh chứng.

QUY TẮC NĂNG LỰC ĐẶC THÙ & PHẨM CHẤT:
- Mục 2.b (Năng lực đặc thù môn học): CHỈ 2–3 năng lực đặc thù nổi trội của môn {subject} gắn với bài học. Viết mỗi mục 1 dòng.
- Mục 2.c (Năng lực số): CHỈ khi được bật; liệt kê đủ từng miền đã chọn, mỗi miền 1 dòng.
- Mục 2.d (Năng lực AI): CHỈ khi được bật; liệt kê đủ từng mã đã chọn, mỗi mã 1 dòng.
- Mục 3 (Phẩm chất): CHỈ 1–2 phẩm chất có hành vi quan sát rõ trong bài (ví dụ: Chăm chỉ, Trung thực, Trách nhiệm).

# I. MỤC TIÊU

## 1. Về kiến thức
(Các YCCĐ của bài học theo CT GDPT 2018; mỗi ý một gạch đầu dòng, giữ động từ hành vi.)

## 2. Về năng lực
### a) Năng lực chung
- [Tên năng lực chung 1 phù hợp môn {subject}]: [Mô tả hành vi cụ thể của học sinh trong bài học này]
- [Tên năng lực chung 2 nếu có]: [Mô tả hành vi cụ thể của học sinh trong bài học này]

### b) Năng lực đặc thù môn học
- [Tên năng lực đặc thù 1]: [Mô tả hành vi gắn với bài]
- [Tên năng lực đặc thù 2]: [Mô tả hành vi gắn với bài]

{digital_objectives_section}
{ai_objectives_section}

## 3. Về phẩm chất & Giáo dục hòa nhập (hòa nhập chỉ khi được bật)
- [Tên phẩm chất]: [Mô tả hành vi quan sát được của học sinh trong bài]`,

  // TAB 3: THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
  GENERATE_MATERIALS: `Hãy xây dựng phần **II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU** cho Kế hoạch bài dạy môn {subject} Cấp {gradeLevelName} chuẩn Công văn 5512 theo GDPT 2018.
- Môn học: {subject}
- Tên bài dạy: {topic}
- Dữ liệu SGK:
"""
{textbook_content}
"""

YÊU CẦU: Tạo danh mục thiết bị và học liệu thiết yếu, cụ thể cho đúng bài dạy (tối đa 2 ý lớn cho mỗi đối tượng, mỗi ý lớn tối đa 3 ý con). TUYỆT ĐỐI KHÔNG để dấu ngoặc vuông [...] hay dấu ba chấm "..."; phải điền tên đồ dùng/học liệu thực tế.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU

## 1. Đối với Giáo viên
- Kế hoạch bài dạy, SGK, bài giảng điện tử (trình chiếu các hình ảnh/video trực quan bám sát bài học).
- Phiếu học tập, bảng phụ nhóm và các dụng cụ trực quan phục vụ bài dạy.

## 2. Đối với Học sinh
- SGK, vở ghi, đồ dùng học tập thiết yếu của môn học.
- Đọc trước bài trong SGK và chuẩn bị các nhiệm vụ được giao ở tiết trước.`,

  // 1-CLICK PHẦN I + II (CORE LESSON)
  GENERATE_CORE_LESSON: `Đọc nguồn SGK (văn bản OCR/tóm tắt và PDF/ảnh nếu đính kèm) và soạn phần I + II của Kế hoạch bài dạy môn {subject} Cấp {gradeLevelName} chuẩn Công văn 5512/BGDĐT-GDTrH, bám CT GDPT 2018.
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
- Gợi ý Năng lực chung theo đặc thù môn {subject}:
{general_competencies_guide}

BẮT BUỘC xuất đúng 2 khối, mỗi khối bắt đầu bằng marker:
<<<KHBD_I>>>
(toàn bộ I. Mục tiêu)
<<<KHBD_II>>>
(toàn bộ II. Thiết bị và học liệu)

QUY TẮC MỤC TIÊU:
- Mục 1. Về kiến thức: YCCĐ chuẩn CT GDPT 2018 cho bài học.
- Mục 2.a (Năng lực chung): CHỈ 1–2 năng lực chung phù hợp đặc thù môn {subject} và bài dạy này; mỗi mục đúng 1 dòng mô tả hành vi.
- Mục 2.b (Năng lực đặc thù): 2–3 năng lực đặc thù của môn {subject}.
- Mục 2.c / 2.d (NLS / AI): Chỉ tạo mục đang bật và chỉ theo đúng miền/mã đã chọn (mỗi mục 1 dòng).
- Mục 3 (Phẩm chất): 1–2 phẩm chất gắn liền bài học.
- Mục II: Cụ thể hóa đồ dùng dạy học thực tế cho GV và HS, không để lại dấu [...] hay "...".`,

  // TAB 4.A: TIẾN TRÌNH DẠY HỌC - HOẠT ĐỘNG MỞ ĐẦU
  GENERATE_ACTIVITY_A: `Hãy biên soạn chi tiết **HOẠT ĐỘNG MỞ ĐẦU (TIẾP CẬN VẤN ĐỀ)** trong mục III. Tiến trình dạy học môn {subject} chuẩn Công văn 5512 theo GDPT 2018.
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

YÊU CẦU KỊCH BẢN THỰC CHIẾN:
${ACTIVITY_TABLE_CONTRACT}

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: MỞ ĐẦU (Khoảng 5 - 7 phút)

### a) Mục tiêu:
- Tạo tâm thế hứng thú, kích thích trí tò mò, tạo mâu thuẫn nhận thức hoặc gợi mở nhu cầu tìm hiểu kiến thức mới bám sát tình huống mở đầu của bài học trong SGK.
- Huy động kiến thức, kĩ năng nền tảng đã học có liên quan để chuẩn bị tiếp nhận bài mới.

### b) Nội dung:
- Giáo viên đưa ra tình huống thực tiễn / câu đố / trò chơi học tập / câu hỏi mở đầu từ SGK: nêu rõ nội dung cụ thể của tình huống.
- Học sinh quan sát, suy nghĩ độc lập và trao đổi để đưa ra dự đoán ban đầu.

### c) Sản phẩm:
- Câu trả lời, kết quả tính toán hoặc dự đoán ban đầu của học sinh đối với tình huống mở đầu.

### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ: (Áp dụng Kỹ thuật ...) **GV:** Trình chiếu tình huống mở đầu trong SGK và nêu câu lệnh trực tiếp: "Quan sát tình huống sau, các em hãy suy nghĩ và đưa ra dự đoán...". **HS:** Tiếp nhận nhiệm vụ, quan sát và chuẩn bị giấy nháp.<br>+ Bước 2: Thực hiện nhiệm vụ: **HS:** Suy nghĩ cá nhân (1-2 phút) ghi câu trả lời vào nháp -> Trao đổi nhanh theo cặp (1-2 phút) thống nhất ý kiến. **GV:** Bao quát lớp, phát hiện các dự đoán khác nhau hoặc ngộ nhận ban đầu của HS về vấn đề, gợi mở tư duy.<br>+ Bước 3: Báo cáo, thảo luận: **HS:** Đại diện 1-2 cặp xung phong phát biểu dự đoán; cả lớp nhận xét, lắng nghe các ý kiến khác biệt. **GV:** Điều hành thảo luận, đặt câu hỏi dẫn dắt: "Vì sao em lại đưa ra dự đoán này?".<br>+ Bước 4: Kết luận, nhận định: **GV:** Nhận xét tinh thần phát biểu, khéo léo tạo mâu thuẫn nhận thức và dẫn dắt vào bài mới: "Để kiểm chứng dự đoán trên và tìm câu trả lời chính xác, chúng ta cùng vào bài học hôm nay...". **HS:** Ghi tên bài vào vở. | **Tình huống mở đầu**<br>- Vấn đề thực tế từ SGK.<br>- Dự đoán ban đầu của học sinh.<br>. Ghi nhận vấn đề cần giải quyết trong bài học. |`,

  // TAB 4.B: TIẾN TRÌNH DẠY HỌC - HOẠT ĐỘNG HÌNH THÀNH KIẾN THỨC MỚI
  GENERATE_ACTIVITY_B: `Hãy biên soạn chi tiết toàn bộ **HOẠT ĐỘNG HÌNH THÀNH KIẾN THỨC MỚI** trong mục III. Tiến trình dạy học môn {subject} chuẩn Công văn 5512 theo GDPT 2018.
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

YÊU CẦU KỊCH BẢN THỰC CHIẾN & NGUYÊN TẮC ÁNH XẠ 1-1 BẮT BUỘC THEO TIỂU MỤC SGK:
${ACTIVITY_TABLE_CONTRACT}
- ĐẾM SỐ TIỂU MỤC KIẾN THỨC TRONG SGK: Nếu SGK có N tiểu mục (Mục 1, Mục 2... hoặc HĐ Khám phá 1, 2...), bạn BẮT BUỘC PHẢI chia Hoạt động B thành đúng N hoạt động con tương ứng 1-1:
  ### 1. Hoạt động 2.1: [Tên tiểu mục 1 trong SGK]
  ### 2. Hoạt động 2.2: [Tên tiểu mục 2 trong SGK]
  ...
  TUYỆT ĐỐI CẤM GỘP các tiểu mục thành một mục chung. TUYỆT ĐỐI CẤM BỊA THÊM hoạt động ngoài SGK.
- TỪNG HOẠT ĐỘNG NHÁNH 2.k PHẢI CÓ ĐỦ 4 PHẦN:
  #### a) Mục tiêu:
  #### b) Nội dung:
  #### c) Sản phẩm: (Ghi rõ lời giải chi tiết, công thức, định nghĩa hoàn chỉnh, không để dấu "...")
  #### d) Tổ chức thực hiện: (ĐÚNG 1 BẢNG MARKDOWN 2 CỘT, 1 HÀNG DUY NHẤT)
    * CỘT TRÁI: Kịch bản phân vai rõ ràng:
      + Nêu rõ tên Kỹ thuật dạy học (Think-Pair-Share, Khăn trải bàn, Mảnh ghép, Trạm học tập...).
      + **GV:** Nói câu lệnh trong ngoặc kép "...", hành động cụ thể, **DỰ KIẾN LỖI SAI / NGỘ NHẬN ĐIỂN HÌNH CỦA HỌC SINH ĐỐI VỚI TIỂU MỤC NÀY** và can thiệp hỗ trợ phân hóa.
      + **HS:** Làm việc cá nhân X phút -> Thảo luận nhóm Y phút tạo sản phẩm trung gian trên bảng phụ/phiếu -> Báo cáo và phản biện trước lớp.
    * CỘT PHẢI: NỘI DUNG GHI BẢNG CHỐT KIẾN THỨC CHO HS CHÉP VỞ (Định nghĩa, quy tắc, công thức LaTeX, chú ý, ví dụ mẫu kèm đề bài và lời giải chi tiết từng bước). CẤM viết hành động của GV/HS ở cột phải.

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI

### 1. Hoạt động 2.1: [Tên tiểu mục 1 trong SGK]
#### a) Mục tiêu:
- Học sinh hình thành được kiến thức, hiểu rõ bản chất và vận dụng được quy tắc/định nghĩa của tiểu mục 1.
#### b) Nội dung:
- Học sinh thực hiện hoạt động khám phá trong SGK, trả lời các câu hỏi phát vấn và làm ví dụ mẫu.
#### c) Sản phẩm:
- Kết quả câu trả lời, lời giải chi tiết cho hoạt động khám phá và ví dụ mẫu:
  + (Trình bày đầy đủ các bước giải, công thức khoa học/toán học LaTeX hoàn chỉnh).
#### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ: (Áp dụng Kỹ thuật ...) **GV:** Giao hoạt động khám phá trong SGK: "Các em có 3 phút làm việc cá nhân vào phiếu học tập và 4 phút thảo luận nhóm hoàn thành bảng phụ...". **HS:** Nhận phiếu học tập, phân công nhiệm vụ trong nhóm.<br>+ Bước 2: Thực hiện nhiệm vụ: **HS:** Làm việc cá nhân (3 phút) ghi kết quả vào nháp -> Thảo luận nhóm (4 phút) thống nhất sản phẩm trung gian lên bảng nhóm. **GV:** Di chuyển bao quát, phát hiện lỗi sai điển hình của học sinh trong bài: (chỉ rõ lỗi sai cụ thể), can thiệp hỗ trợ phân hóa (gợi ý cho nhóm gặp khó khăn, đặt câu hỏi nâng cao cho nhóm khá giỏi).<br>+ Bước 3: Báo cáo, thảo luận: **HS:** Đại diện một nhóm lên bảng trình bày sản phẩm; các nhóm khác đối chiếu, nhận xét và phản biện. **GV:** Điều hành báo cáo, đặt câu hỏi kiểm tra độ hiểu sâu: "Tại sao nhóm em lại suy ra được kết luận/công thức này?".<br>+ Bước 4: Kết luận, nhận định: **GV:** Nhận xét quá trình làm việc của các nhóm, chuẩn hóa kiến thức, giảng giải bản chất quy tắc và hướng dẫn ghi bảng. **HS:** Sửa bài vào vở, ghi nhận kiến thức chuẩn mực. | **1. [Tên kiến thức tiểu mục 1]**<br>- Định nghĩa / Khái niệm chuẩn xác.<br>- Quy tắc / Công thức: $...$<br>+ Chú ý quan trọng.<br>. Ví dụ mẫu 1: Đề bài và Lời giải chi tiết từng bước. |`,

  // TAB 4.C: TIẾN TRÌNH DẠY HỌC - HOẠT ĐỘNG LUYỆN TẬP
  GENERATE_ACTIVITY_C: `Hãy biên soạn chi tiết **HOẠT ĐỘNG LUYỆN TẬP** trong mục III. Tiến trình dạy học môn {subject} chuẩn Công văn 5512 theo GDPT 2018.
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
- CHỈ dùng bài luyện tập / câu hỏi có trong SGK hoặc dữ liệu giáo viên cung cấp. CẤM invent bài tập trắc nghiệm ngoài sách nếu nguồn không có.
- Cột TRÁI mục d): Kịch bản phân vai rõ ràng:
  + Áp dụng Kỹ thuật dạy học (ví dụ: Bài tập phân hóa 3 mức, Đánh giá đồng đẳng, Sửa lỗi theo cặp...).
  + **GV:** Nói câu giao việc trong ngoặc kép "...", di chuyển quan sát phát hiện lỗi sai tính toán/lập luận điển hình, trực tiếp hướng dẫn phân hóa.
  + **HS:** Giải bài cá nhân vào vở -> Đổi vở chấm chéo hoặc thảo luận cặp -> Lên bảng trình bày, lớp phản biện.
- Cột PHẢI mục d): Chép rõ Đề bài và Lời giải chi tiết từng bước của các bài tập trong SGK (không để dấu "...").

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (Khoảng 12 - 15 phút)

### a) Mục tiêu:
- Củng cố và khắc sâu kiến thức vừa học thông qua giải quyết các bài tập, câu hỏi cụ thể trong SGK.
- Rèn luyện kỹ năng tính toán, biến đổi, lập luận và trình bày bài giải chuẩn mực.

### b) Nội dung:
- Học sinh làm các bài tập luyện tập trong SGK: (Liệt kê rõ ràng đề bài các bài tập trong SGK).

### c) Sản phẩm:
- Lời giải chi tiết và đáp số chuẩn xác của các bài tập trong SGK.

### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ: (Áp dụng Kỹ thuật ...) **GV:** Giao bài tập trong SGK: "Các em hoàn thành các bài tập sau vào vở trong 7 phút, sau đó đổi vở kiểm tra chéo...". **HS:** Đọc kĩ đề bài, xác định công thức/quy tắc áp dụng.<br>+ Bước 2: Thực hiện nhiệm vụ: **HS:** Làm bài cá nhân vào vở (7 phút) -> Đổi vở kiểm tra chéo theo cặp (2 phút). **GV:** Quan sát, phát hiện các lỗi sai điển hình trong biến đổi/tính toán: (chỉ rõ lỗi sai thường gặp), trực tiếp hướng dẫn học sinh còn lúng túng.<br>+ Bước 3: Báo cáo, thảo luận: **HS:** 2 học sinh lên bảng trình bày lời giải; cả lớp đối chiếu bài làm, nhận xét và phát hiện các cách giải khác. **GV:** Đặt câu hỏi chất vấn: "Có lưu ý gì quan trọng khi thực hiện bước này?".<br>+ Bước 4: Kết luận, nhận định: **GV:** Chốt lời giải chuẩn xác, chỉ rõ các bẫy sai lầm cần tránh khi làm bài kiểm tra. **HS:** Chữa bài chuẩn mực vào vở ghi. | **Luyện tập**<br>- Bài 1: Đề bài và Lời giải chi tiết.<br>- Bài 2: Đề bài và Lời giải chi tiết.<br>. Lưu ý phương pháp giải chuẩn mực. |`,

  // TAB 4.D: TIẾN TRÌNH DẠY HỌC - HOẠT ĐỘNG VẬN DỤNG
  GENERATE_ACTIVITY_D: `Hãy biên soạn chi tiết **HOẠT ĐỘNG VẬN DỤNG** trong mục III. Tiến trình dạy học môn {subject} chuẩn Công văn 5512 theo GDPT 2018.
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
- CHỈ dùng bài vận dụng / tình huống thực tế có trong SGK hoặc dữ liệu giáo viên cung cấp. CẤM invent số liệu bài toán ngoài nguồn.
- Cột TRÁI mục d): Kịch bản phân vai rõ ràng:
  + Áp dụng Kỹ thuật dạy học (Dự án mini, Phân tích tình huống, Bài tập mở...).
  + **GV:** Nói câu định hướng trong ngoặc kép "...", gợi mở cách liên hệ thực tế, hướng dẫn phân hóa.
  + **HS:** Thảo luận cặp/nhóm giải quyết bài toán thực tế -> Báo cáo giải pháp, lớp phản biện tính khả thi.
- Cột PHẢI mục d): Tình huống thực tế và Lời giải mô hình hóa hoàn chỉnh.

## D. HOẠT ĐỘNG 4: VẬN DỤNG (Khoảng 5 - 8 phút hoặc giao về nhà)

### a) Mục tiêu:
- Vận dụng kiến thức, kĩ năng đã học vào giải quyết các bài toán, tình huống thực tế đời sống.
- Phát triển năng lực giải quyết vấn đề, mô hình hóa và tư duy liên hệ thực tiễn.

### b) Nội dung:
- Tình huống hoặc bài toán vận dụng thực tiễn trong SGK: (Nêu cụ thể đề bài tình huống).

### c) Sản phẩm:
- Bài giải mô hình hóa thực tế, kết quả tính toán hoặc báo cáo giải pháp của học sinh.

### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ: (Áp dụng Kỹ thuật ...) **GV:** Giao nhiệm vụ vận dụng thực tế: "Hãy vận dụng kiến thức vừa học để giải quyết bài toán thực tiễn sau...". **HS:** Tiếp nhận nhiệm vụ, phân tích số liệu thực tế.<br>+ Bước 2: Thực hiện nhiệm vụ: **HS:** Thảo luận cặp/nhóm (4 phút) mô hình hóa vấn đề và tính toán kết quả. **GV:** Quan sát, gợi mở cách chuyển đổi từ ngôn ngữ thực tế sang biểu thức chuyên môn.<br>+ Bước 3: Báo cáo, thảo luận: **HS:** Đại diện nhóm trình bày mô hình và kết quả; các nhóm khác nhận xét tính hợp lý của đáp số thực tế. **GV:** Đặt câu hỏi mở rộng liên hệ đời sống.<br>+ Bước 4: Kết luận, nhận định: **GV:** Nhận xét, đánh giá khả năng vận dụng của HS, chốt lại ý nghĩa thực tiễn của bài học. **HS:** Ghi nhận lời giải hoàn chỉnh vào vở. | **Vận dụng**<br>- Tình huống thực tế từ SGK.<br>- Mô hình hóa & Lời giải chuẩn xác.<br>. Ý nghĩa thực tiễn của bài học. |`,

  // 1-CLICK HOẠT ĐỘNG A -> D (ACTIVITIES AD)
  GENERATE_ACTIVITIES_AD: `Đọc PDF/ảnh SGK đính kèm và soạn toàn bộ hoạt động A–D môn {subject} Cấp {gradeLevelName} chuẩn Công văn 5512.
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

BẮT BUỘC xuất đúng 4 khối, mỗi khối bắt đầu bằng marker:
<<<KHBD_A>>>
(toàn bộ ## A. HOẠT ĐỘNG 1: MỞ ĐẦU)
<<<KHBD_B>>>
(toàn bộ ## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI)
<<<KHBD_C>>>
(toàn bộ ## C. HOẠT ĐỘNG 3: LUYỆN TẬP)
<<<KHBD_D>>>
(toàn bộ ## D. HOẠT ĐỘNG 4: VẬN DỤNG)

YÊU CẦU HÌNH THỨC & KỊCH BẢN THỰC CHIẾN (Áp dụng mọi pha A–D):
${ACTIVITY_TABLE_CONTRACT}

PHA A — MỞ ĐẦU:
- Đủ a) Mục tiêu, b) Nội dung, c) Sản phẩm, d) Tổ chức thực hiện (1 bảng 2 cột duy nhất).
- Bám sát tình huống mở đầu trong SGK; không bịa tình huống ngoài nguồn.
- Khi có NLS/AI: Tích hợp công cụ số hoặc câu hỏi/prompt AI mở đầu ngắn gọn (marker **[NLS: ...]** hoặc **[AI: ...]**).

PHA B — HÌNH THÀNH KIẾN THỨC:
- Đếm số tiểu mục kiến thức trong SGK: tạo đúng N hoạt động con (### 1. Hoạt động 2.1: ..., ### 2. Hoạt động 2.2: ...).
- Mỗi hoạt động con đủ #### a) b) c) d) + đúng 1 bảng 2 cột duy nhất.
- Cột Trái: Kịch bản phân vai GV (lời thoại trong "...", chỉ rõ lỗi sai điển hình) và HS (cá nhân -> nhóm -> báo cáo).
- Khi có NLS/AI: Thể hiện GV hướng dẫn công cụ số / giao prompt AI trong "...", HS thao tác và BẮT BUỘC kiểm chứng đối chiếu kết quả với SGK (marker **[NLS: ...]** hoặc **[AI: ...]**).
- Cột Phải: Nội dung ghi bảng chốt kiến thức, công thức LaTeX, ví dụ mẫu kèm đề và lời giải chi tiết. TUYỆT ĐỐI CẤM để dấu "...".

PHA C — LUYỆN TẬP:
- Chép rõ đề và giải chi tiết các bài tập có trong SGK vào Cột Phải. Cột Trái phân vai rõ ràng.
- Khi có NLS/AI: Ứng dụng phần mềm/máy tính hoặc AI để gợi ý, HS kiểm tra và đối chiếu lời giải.

PHA D — VẬN DỤNG:
- Bám sát bài vận dụng trong SGK, trình bày mô hình hóa và lời giải chuẩn.
- Khi có NLS/AI: Vận dụng công cụ số/AI giải quyết bài toán thực tế, đánh giá và kiểm chứng tính khả thi.

CẤM xuất HTML, span, style, mã màu. CẤM lời chào hỏi hay chúc mừng ở đầu/cuối bài.`,

  // TAB 4.E: ĐÁNH GIÁ
  GENERATE_ASSESSMENT: `Hãy biên soạn **E. KẾ HOẠCH KIỂM TRA - ĐÁNH GIÁ** cho Kế hoạch bài dạy môn {subject} Cấp {gradeLevelName} chuẩn CV 5512.
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

| Hoạt động học | Mục tiêu đánh giá | Phương pháp đánh giá | Công cụ đánh giá | Người đánh giá |
| :--- | :--- | :--- | :--- | :--- |
| **A. Mở đầu** | Sự hứng thú, khả năng huy động kiến thức nền | Quan sát, vấn đáp | Câu hỏi mở đầu, thái độ tham gia | Giáo viên |
| **B. Hình thành kiến thức** | Khả năng khám phá, chiếm lĩnh khái niệm, quy tắc mới | Quan sát, đánh giá sản phẩm | Phiếu học tập, câu trả lời cá nhân/nhóm | GV & Học sinh (đánh giá đồng đẳng) |
| **C. Luyện tập** | Kĩ năng tính toán, biến đổi, giải bài tập | Đánh giá qua sản phẩm viết | Vở ghi, bảng phụ, bài tập luyện tập | Giáo viên & Tự đánh giá |
| **D. Vận dụng** | Năng lực mô hình hoá, giải quyết vấn đề thực tế | Đánh giá sản phẩm/bài viết | Báo cáo bài tập vận dụng thực tiễn | Giáo viên |

## 2. Bảng Tiêu chí Đánh giá (Rubrics) Hoạt động Học tập của Học sinh

| Tiêu chí đánh giá | Mức 1: Chưa đạt (Dưới 5đ) | Mức 2: Đạt (5 - 6.5đ) | Mức 3: Khá (7 - 8.5đ) | Mức 4: Tốt (9 - 10đ) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Nắm vững kiến thức bài học** | Chưa nhớ định nghĩa, quy tắc; còn nhầm lẫn nhiều | Nhớ kiến thức cơ bản nhưng áp dụng còn lúng túng | Nắm vững kiến thức, vận dụng đúng vào các bài tập quen thuộc | Hiểu sâu sắc bản chất, giải thích mạch lạc, vận dụng linh hoạt |
| **2. Kĩ năng thực hành và lập luận** | Thực hành sai nhiều, trình bày lộn xộn, thiếu bước | Thực hành cơ bản đúng, trình bày còn sơ sài | Thực hành chuẩn xác, lập luận có căn cứ, trình bày sạch đẹp | Thực hành nhanh, lập luận chặt chẽ, tối ưu hóa giải pháp |
| **3. Tinh thần hợp tác và thảo luận** | Thụ động, không tham gia cùng nhóm | Có tham gia nhưng còn ỷ lại vào bạn khác | Tích cực trao đổi, hoàn thành tốt phần việc được phân công | Đóng vai trò nòng cốt, hỗ trợ các bạn khác, dẫn dắt nhóm |
| **4. Năng lực ứng dụng Số / AI** | Chưa biết sử dụng thiết bị/công cụ | Sử dụng công cụ số mức độ cơ bản | Sử dụng tốt công cụ số để tra cứu, hỗ trợ học tập | Sử dụng thành thạo thiết bị số, biết phản biện và kiểm chứng kết quả |

Chỉ đưa hàng Rubrics về năng lực Số/AI khi thành phần tương ứng được bật trong bối cảnh sư phạm; nếu không thì bỏ hàng này.`,

  // TAB 4.F: HỒ SƠ DẠY HỌC
  GENERATE_PORTFOLIO: `Hãy thiết kế **F. HỒ SƠ DẠY HỌC (CÁC PHIẾU HỌC TẬP)** cho Kế hoạch bài dạy môn {subject} Cấp {gradeLevelName}.
- Môn học: {subject}
- Tên bài dạy: {topic}
- Dữ liệu bài học:
"""
{objectives_content}
{activities_content}
"""

YÊU CẦU: Tạo 2 đến 3 Phiếu Học Tập (PHT) hoàn chỉnh với bảng biểu đẹp mắt và BẮT BUỘC CÓ PHẦN **HƯỚNG DẪN CHẤM VÀ ĐÁP ÁN CHI TIẾT** (Thang điểm 10). Điền đầy đủ câu hỏi và lời giải chi tiết, không để dấu "...".

# F. HỒ SƠ DẠY HỌC

## 1. PHIẾU HỌC TẬP SỐ 1 (Phục vụ Hoạt động Hình thành kiến thức)
**TRƯỜNG THCS: .......................................**  
**LỚP: .............. NHÓM: ..............................**  
**HỌ VÀ TÊN THÀNH VIÊN: .....................................................................................**  
### BÀI HỌC: {topic} (Môn {subject})

| Nhiệm vụ | Nội dung câu hỏi / Bài tập | Dự kiến kết quả của Học sinh |
| :--- | :--- | :--- |
| **Nhiệm vụ 1** | Câu hỏi khám phá 1 bám sát SGK | Lời giải chi tiết của học sinh |
| **Nhiệm vụ 2** | Câu hỏi khám phá 2 bám sát SGK | Lời giải chi tiết của học sinh |

---

## 2. PHIẾU HỌC TẬP SỐ 2 (Phục vụ Hoạt động Luyện tập & Củng cố)
[Nội dung tương tự với các bài tập rèn luyện kỹ năng...]

---

## 3. HƯỚNG DẪN CHẤM VÀ ĐÁP ÁN CHI TIẾT CÁC PHIẾU HỌC TẬP
### a) Đáp án và Thang điểm Phiếu học tập số 1 (Thang điểm 10)
- **Nhiệm vụ 1 (5.0 điểm):** Lời giải chi tiết và đáp số chuẩn mực.
- **Nhiệm vụ 2 (5.0 điểm):** Lời giải chi tiết và đáp số chuẩn mực.`,

  // TAB 4.G: HƯỚNG DẪN VỀ NHÀ
  GENERATE_HOMEWORK: `Hãy biên soạn chi tiết **G. HƯỚNG DẪN VỀ NHÀ** trong Kế hoạch bài dạy môn {subject} Cấp {gradeLevelName} chuẩn CV 5512.
- Môn học: {subject}
- Tên bài dạy: {topic}
- Nội dung bài học:
"""
{objectives_content}
{activities_content}
"""

# G. HƯỚNG DẪN VỀ NHÀ

## 1. Ôn tập và Khắc sâu kiến thức
- Học thuộc và nắm vững các định nghĩa, quy tắc, công thức trọng tâm đã học trong bài: (liệt kê vắn tắt các nội dung cốt lõi).
- Vẽ sơ đồ tư duy (Mindmap) tóm tắt toàn bộ nội dung bài học vào vở ghi.

## 2. Bài tập tự luyện tại nhà
- Hoàn thành các bài tập còn lại trong SGK và Sách bài tập môn {subject}.
- **Bài tập mở rộng / Nâng cao (Dành cho HS khá, giỏi):** Đưa ra 1 bài toán/nhiệm vụ mở rộng có tính tư duy cao kèm gợi ý ngắn gọn.

## 3. Nhiệm vụ chuẩn bị cho bài học tiếp theo
- Đọc trước bài mới trong SGK môn {subject}.
- Chuẩn bị đầy đủ dụng cụ học tập và tìm hiểu các ví dụ thực tế liên quan đến bài học tiếp theo.

## 4. Gợi ý Câu lệnh Prompt AI hỗ trợ học sinh tự học tại nhà an toàn (CHỈ tạo khi bối cảnh sư phạm bật năng lực AI)
- *Mẫu Prompt 1 (Giải thích lại khái niệm):* "Em là học sinh lớp {grade}, em chưa hiểu rõ về [khái niệm trong bài]. Bạn hãy giải thích lại bằng một ví dụ thực tế gần gũi, đơn giản nhất nhé!"
- *Mẫu Prompt 2 (Gợi ý từng bước):* "Em đang giải bài tập [nội dung bài tập]. Em chưa biết bắt đầu từ đâu, bạn hãy cho em 2 câu hỏi gợi ý để em tự tìm ra hướng giải, đừng giải hộ em nhé!"
- *Mẫu Prompt 3 (Kiểm tra lời giải):* "Đây là lời giải của em cho bài tập [nội dung]: [lời giải]. Bạn hãy nhận xét xem em đã làm đúng chưa và chỉ ra bước nào cần khắc phục nhé!"`
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
- 5 phẩm chất chủ yếu và phương pháp dạy học phân hóa, hòa nhập cho học sinh.

QUY TẮC BẮT BUỘC KHI XUẤT NỘI DUNG:
- Bám sát GDPT 2018 và nội dung bài học do giáo viên cung cấp.
- Thiết kế giáo án thành KỊCH BẢN SƯ PHẠM THỰC CHIẾN (GV có lời thoại trực tiếp trong ngoặc kép "...", hành động cụ thể, dự kiến lỗi sai điển hình; HS có thao tác cá nhân, nhóm và sản phẩm rõ ràng).
- Định dạng Markdown rõ ràng, phân cấp tiêu đề bằng #, ##, ###, #### hợp lý.
${latexRule}
- Nội dung phải chi tiết, đầy đủ, thiết thực cho giáo viên lên lớp, TUYỆT ĐỐI KHÔNG viết tóm tắt qua loa, KHÔNG để dấu '...' hoặc '[...]' hoặc từ 'tương tự'.
- TUYỆT ĐỐI KHÔNG xuất lời chào, lời dẫn chuyện, lời chúc mừng hoặc nhận xét meta ngoài lề.
- Mục tiêu kiến thức phải bám YCCĐ CT GDPT 2018 / Thông tư 32/2018/TT-BGDĐT; không tự tạo kiến thức ngoài nguồn.`;
}

/**
 * Trích xuất danh sách các tiểu mục kiến thức từ nội dung phân tích SGK (Tab 1/Bước 0).
 * @param {string} content - Nội dung phân tích SGK
 * @returns {Array<{index: number, title: string}>} Danh sách tiểu mục đã chuẩn hóa
 */
function extractTextbookSubsections(content) {
  if (!content || typeof content !== 'string') return [];
  const text = content.trim();
  if (!text) return [];

  const results = [];
  const seenTitles = new Set();

  const ignorePatterns = [
    /^tổng quan\b/i,
    /^khung kiến thức\b/i,
    /^chuỗi hoạt động\b/i,
    /^hệ thống bài tập\b/i,
    /^đề xuất của\b/i,
    /^yêu cầu cần đạt\b/i,
    /^tiến trình dạy học\b/i,
    /^thiết bị\b/i,
    /^hoạt động mở đầu\b/i,
    /^hoạt động luyện tập\b/i,
    /^hoạt động vận dụng\b/i,
    /^bài tập cuối bài\b/i,
    /^(?:định nghĩa|khái niệm|quy tắc|công thức|chú ý|ví dụ|bài tập|nhiệm vụ|bước\s*\d+|phương pháp|kỹ thuật)$/i
  ];

  function cleanTitle(raw) {
    if (!raw) return '';
    let t = raw
      .replace(/^[\s*#\-+•:|`]+/, '')
      .replace(/[\s*#\-+•:|`]+$/, '')
      .replace(/\s*\(.*?\)\s*$/, '')
      .replace(/^[*_~`]+/, '')
      .replace(/[*_~`]+$/, '')
      .trim();
    return t;
  }

  function isIgnored(title) {
    if (!title || title.length < 2) return true;
    return ignorePatterns.some(p => p.test(title));
  }

  function addSub(idx, title) {
    const cleaned = cleanTitle(title);
    if (!cleaned || isIgnored(cleaned)) return;
    const key = cleaned.toLowerCase();
    if (seenTitles.has(key)) return;
    seenTitles.add(key);
    results.push({ index: idx, title: cleaned });
  }

  // Chiến lược 1: Tìm các mẫu "Mục 1:", "Mục 2:", "Phần 1:", "Phần 2:"
  const mucRegex = /(?:^|\n)\s*(?:[-*+•]\s+)?(?:#{1,6}\s+)?(?:\*\*)?(?:Mục|Phần)\s*(\d+)[\s.:\-]+([^\r\n]+)/gi;
  let match;
  while ((match = mucRegex.exec(text)) !== null) {
    const num = parseInt(match[1], 10);
    const title = match[2];
    addSub(num, title);
  }

  if (results.length > 0) {
    return results.map((item, i) => ({ index: i + 1, title: item.title }));
  }

  // Chiến lược 2: Tìm theo "HĐ khám phá 1:", "Hoạt động khám phá 1:", "HĐ 1:", "Khám phá 1:"
  const hdRegex = /(?:^|\n)\s*(?:[-*+•]\s+)?(?:#{1,6}\s+)?(?:\*\*)?(?:Hoạt động khám phá|HĐ khám phá|Hoạt động|HĐ|Khám phá)\s*(\d+)[\s.:\-]+([^\r\n]+)/gi;
  while ((match = hdRegex.exec(text)) !== null) {
    const num = parseInt(match[1], 10);
    const title = match[2];
    addSub(num, title);
  }

  if (results.length > 0) {
    return results.map((item, i) => ({ index: i + 1, title: item.title }));
  }

  // Chiến lược 3: Tìm trong phạm vi mục 2 "Khung kiến thức trọng tâm" hoặc toàn văn
  let searchBlock = text;
  const section2Match = text.match(/2\.\s*(?:\*\*)?Khung kiến thức trọng tâm[\s\S]*?(?=(?:\n\s*(?:#{1,3}\s*)?3\.\s*(?:\*\*)?Chuỗi hoạt động|\n\s*(?:#{1,2}\s*)?[3-9]\.|$))/i);
  if (section2Match) {
    searchBlock = section2Match[0];
  }

  const numRegex = /(?:^|\n)\s*(?:[-*+•]\s+)?(?:#{1,6}\s+)?(?:\*\*)?(\d+)[\s.)\-]+(?:\*\*)?\s*([A-ZÀ-Ỹ0-9][^\r\n]+)/g;
  while ((match = numRegex.exec(searchBlock)) !== null) {
    const num = parseInt(match[1], 10);
    const title = match[2];
    if (section2Match && (num >= 1 && num <= 5) && isIgnored(title)) {
      continue;
    }
    addSub(num, title);
  }

  if (results.length > 0) {
    return results.map((item, i) => ({ index: i + 1, title: item.title }));
  }

  return [];
}

function getPromptTemplate(templateKey, context) {
  let baseTemplate = PROMPTS[templateKey];
  if (!baseTemplate) return '';

  const subjectId = context.subject || 'toan';
  const subjectName = context.subjectName || 'Toán';
  const gradeLevelName = context.gradeLevelName || 'THCS';

  const genCompsGuide = formatGeneralCompetenciesGuide(subjectId, context);

  // Insert competencies
  const competencies = context.competencies ? context.competencies.join('; ') : '';
  const digitalObjectivesSection = context.digitalCompetencyEnabled
    ? `### c) Năng lực số\n- [Tên miền đã chọn]: [Mô tả nhiệm vụ số gắn với bài]`
    : '';
  const aiObjectivesSection = context.aiCompetencyEnabled
    ? `### d) Năng lực AI\n- [Mã AI đã chọn]: [Mô tả nhiệm vụ AI gắn với bài]`
    : '';
  
  // Replace placeholders an toàn
  let result = baseTemplate
    .replace(/\{subject\}/g, subjectName)
    .replace(/\{gradeLevelName\}/g, gradeLevelName)
    .replace(/\{topic\}/g, context.topic || '')
    .replace(/\{duration\}/g, context.duration || '02 tiết (90 phút)')
    .replace(/\{textbook_content\}/g, context.textbook_content || '')
    .replace(/\{objectives_content\}/g, context.objectives_content || '')
    .replace(/\{activities_content\}/g, context.activities_content || '')
    .replace(/\{yccd_official\}/g, context.yccd_official || '')
    .replace(/\{grade\}/g, context.grade || '6')
    .replace(/\{competencies\}/g, competencies)
    .replace(/\{digital_objectives_section\}/g, digitalObjectivesSection)
    .replace(/\{ai_objectives_section\}/g, aiObjectivesSection)
    .replace(/\{general_competencies_guide\}/g, genCompsGuide);

  if (PROMPTS.SOURCE_LOCK) {
    result += `\n\n${PROMPTS.SOURCE_LOCK}`;
  }

  // Append pedagogical context if provided
  if (context.pedagogical_context) {
    result += `\n\nBỐI CẢNH SƯ PHẠM VÀ RÀNG BUỘC BẮT BUỘC:\n${context.pedagogical_context}`;
  }

  if (templateKey === 'GENERATE_OBJECTIVES' || templateKey === 'GENERATE_CORE_LESSON') {
    const integrationRules = [
      context.digitalCompetencyEnabled && 'NLS: chỉ tạo ### c) và liệt kê đủ từng miền đã chọn.',
      context.aiCompetencyEnabled && 'AI: chỉ tạo ### d) và liệt kê đủ từng mã đã chọn.'
    ].filter(Boolean).join(' ');
    result += `\n\nQUY TẮC VIẾT NĂNG LỰC / PHẨM CHẤT:
- Năng lực chung: CHỌN 1–2 năng lực phù hợp nhất với môn ${subjectName} từ danh sách gợi ý trên. Mỗi năng lực đúng 1 dòng: \`- [Tên năng lực]: [mô tả hành vi cụ thể trong bài]\`.
- CẤM nhãn Biểu hiện, Nhiệm vụ/Sản phẩm, Minh chứng. CẤM ý con bắt đầu bằng + .
- Năng lực đặc thù: 2–3 năng lực nổi trội của môn ${subjectName}. Phẩm chất: 1–2 phẩm chất.
- ${integrationRules || 'Không tạo mục NLS hoặc AI.'} Mỗi mục 1 dòng \`- Tên/Mã: mô tả ngắn gắn bài\`. CẤM tạo NLS/AI không được chọn hoặc gộp hai nhóm thành một hạn ngạch.`;
  }

  if (templateKey === 'GENERATE_ACTIVITY_B' || templateKey === 'GENERATE_ACTIVITIES_AD') {
    const rawTextbook = context.textbook_content || '';
    const subsections = extractTextbookSubsections(rawTextbook);
    if (subsections && subsections.length > 0) {
      const subListStr = subsections.map(s => `+ Tiểu mục ${s.index}: "${s.title}" -> BẮT BUỘC sinh: ### ${s.index}. Hoạt động 2.${s.index}: ${s.title}`).join('\n');
      result += `\n\nDANH SÁCH TIỂU MỤC SGK BẮT BUỘC ÁP DỤNG (ĐÚNG ${subsections.length} HOẠT ĐỘNG NHÁNH):
Từ dữ liệu SGK được cung cấp, xác định chính xác ${subsections.length} tiểu mục kiến thức sau. Bạn PHẢI tạo đúng ${subsections.length} hoạt động nhánh tương ứng 1-1, KHÔNG ĐƯỢC GỘP, KHÔNG ĐƯỢC BỎ BỚT, KHÔNG ĐƯỢC BỊA THÊM:
${subListStr}
Mỗi hoạt động 2.k trên BẮT BUỘC phải có đầy đủ 4 phần: #### a) Mục tiêu:, #### b) Nội dung:, #### c) Sản phẩm:, #### d) Tổ chức thực hiện: (với đúng 1 bảng Markdown 2 cột, 4 bước phân vai GV-HS và nội dung ghi bảng).`;
    }
  }

  if (templateKey === 'GENERATE_ACTIVITY_C' || templateKey === 'GENERATE_ACTIVITY_D') {
    if (context.textbook_content && String(context.textbook_content).trim().length > 0) {
      result += `\n\nLƯU Ý QUAN TRỌNG VỀ NGUỒN BÀI TẬP: Vì dữ liệu SGK đã được cung cấp ở trên, CẤM ghi "[Không có trong tài liệu đã cung cấp]". BẮT BUỘC phải trích xuất và giải chi tiết các bài tập có trong nguồn.`;
    }
  }

  return result;
}

if (typeof window !== 'undefined') {
  window.extractTextbookSubsections = extractTextbookSubsections;
  window.getGeneralCompetenciesForSubject = getGeneralCompetenciesForSubject;
  window.formatGeneralCompetenciesGuide = formatGeneralCompetenciesGuide;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { PROMPTS, getSystemRole, getPromptTemplate, extractTextbookSubsections, getGeneralCompetenciesForSubject, formatGeneralCompetenciesGuide };
}
