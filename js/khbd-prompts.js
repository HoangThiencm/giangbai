/**
 * js/khbd-prompts.js
 * Hệ thống Siêu Prompt Sư phạm Đa Môn Học (Lớp 6–9) chuẩn Công văn 5512/BGDĐT-GDTrH,
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

/**
 * Phân bổ thời lượng thông minh cho các hoạt động A, B, C, D, E
 * dựa trên tổng thời lượng (duration) của tiết dạy sao cho tổng thời gian khớp 100%.
 * @param {string} durationStr - Chuỗi thời lượng (ví dụ "02 tiết (90 phút)", "45 phút", "03 tiết (135 phút)")
 * @param {number} [subsectionCount=1] - Số tiểu mục kiến thức trong Hoạt động B (1-4)
 * @param {string|number} [grade] - Khối lớp
 * @returns {{
 *   totalMinutes: number,
 *   A: number,
 *   B: number,
 *   B_subsections: number[],
 *   C: number,
 *   D: number,
 *   E: number,
 *   formatted: {
 *     A: string,
 *     B: string,
 *     B_subsections: string[],
 *     C: string,
 *     D: string,
 *     E: string
 *   }
 * }}
 */
function calculateActivityTimeBudgets(durationStr, subsectionCount, grade) {
  const periodMinutes = Number(grade) >= 1 && Number(grade) <= 5 ? 35 : 45;
  let totalMinutes = periodMinutes * 2;
  const str = String(durationStr || "").trim();

  const minMatch = str.match(/(\d+)\s*(?:phút|p|min)/i);
  if (minMatch) {
    totalMinutes = parseInt(minMatch[1], 10);
  } else {
    const tietMatch = str.match(/(\d+)\s*tiết/i);
    if (tietMatch) {
      totalMinutes = parseInt(tietMatch[1], 10) * periodMinutes;
    } else {
      const numMatch = str.match(/^(\d+)$/);
      if (numMatch) {
        const number = parseInt(numMatch[1], 10);
        totalMinutes = number <= 20 ? number * periodMinutes : number;
      }
    }
  }

  if (isNaN(totalMinutes) || totalMinutes <= 0) {
    totalMinutes = periodMinutes * 2;
  }

  const T = totalMinutes;
  const clamp = (min, max, val) => Math.max(min, Math.min(max, val));

  let timeA = clamp(3, 10, Math.round(T * 0.08));
  let timeE = clamp(2, 5, Math.round(T * 0.04));
  let timeD = clamp(5, 25, Math.round(T * 0.12));
  let timeC = clamp(8, 50, Math.round(T * 0.25));
  let timeB = T - (timeA + timeC + timeD + timeE);

  if (timeB < 5) {
    timeB = Math.max(5, Math.round(T * 0.4));
    timeC = Math.max(5, Math.round(T * 0.25));
    timeA = Math.max(3, Math.round(T * 0.15));
    timeD = Math.max(3, Math.round(T * 0.12));
    timeE = Math.max(2, T - (timeA + timeB + timeC + timeD));
    if (timeE < 1) {
      timeE = 2;
      timeB = T - (timeA + timeC + timeD + timeE);
    }
  }

  const subCount = Math.max(1, Math.min(4, Number(subsectionCount) || 1));
  const bSubsections = [];
  const baseSub = Math.floor(timeB / subCount);
  const remSub = timeB % subCount;
  for (let i = 0; i < subCount; i++) {
    bSubsections.push(baseSub + (i < remSub ? 1 : 0));
  }

  return {
    totalMinutes: T,
    A: timeA,
    B: timeB,
    B_subsections: bSubsections,
    C: timeC,
    D: timeD,
    E: timeE,
    formatted: {
      A: `${timeA} phút`,
      B: `${timeB} phút`,
      B_subsections: bSubsections.map(m => `${m} phút`),
      C: `${timeC} phút`,
      D: `${timeD} phút`,
      E: `${timeE} phút`
    }
  };
}

const LATEX_SPACING_BAN = `- CẤM TUYỆT ĐỐI dùng chuỗi lệnh LaTeX khoảng trắng liên tiếp (\`\\quad \\quad \\quad...\`, \`\\qquad\`, \`\\hspace{...}\`, \`\\phantom{...}\`) để mô phỏng hình vẽ, giả lập trục số hoặc tạo khoảng trống làm bài.
- Đối với bài tập vẽ hình/trục số: BẮT BUỘC mô tả lời giải bằng các bước thực hiện tường minh (ví dụ: "Vẽ trục số nằm ngang, chọn điểm 0 làm gốc, chia các đoạn đơn vị bằng nhau... Điểm biểu diễn -5 nằm bên trái gốc 0 cách 5 đơn vị...") hoặc định vị hình minh họa SVG chuẩn SGK \`![caption](khbd-ill:id)\`.
- Lời giải trong cột Nội dung phải là các bước giải chi tiết hoàn chỉnh, không để khoảng trống vô nghĩa.`;

const ACTIVITY_TABLE_CONTRACT = `YÊU CẦU BẮT BUỘC: KỊCH BẢN SƯ PHẠM THỰC CHIẾN TRONG BẢNG 2 CỘT (Chuẩn CV 5512 & GDPT 2018):
- YÊU CẦU ĐỘ DÀI & VĂN PHONG SÚC TÍCH: Toàn bộ Kế hoạch bài dạy hoàn chỉnh đạt dung lượng chuẩn 8–10 trang Word A4. Hành văn sư phạm cô đọng, súc tích, trực diện vào bản chất kiến thức và hành động cốt lõi của GV/HS; TUYỆT ĐỐI KHÔNG viết văn biền ngẫu, không dùng câu thoại diễn giải lòng vòng, không lặp lại nội dung giữa các mục.
- THỜI LƯỢNG HOẠT ĐỘNG: BẮT BUỘC ghi số phút cố định cụ thể trong tiêu đề các Hoạt động (A, B, C, D, E) và từng hoạt động nhánh trong Mục B, ví dụ: \`## A. HOẠT ĐỘNG 1: MỞ ĐẦU (5 phút)\`, \`### 1. Hoạt động 2.1: [Tên mục] (15 phút)\`, \`## C. HOẠT ĐỘNG 3: LUYỆN TẬP (10 phút)\`, \`## D. HOẠT ĐỘNG 4: VẬN DỤNG (5 phút)\`, \`## E. HOẠT ĐỘNG 5: HƯỚNG DẪN VỀ NHÀ (3 phút)\`. CẤM TUYỆT ĐỐI ghi từ "Khoảng" hoặc dải thời gian dạng "X - Y phút".
- Mục a) Mục tiêu, b) Nội dung, c) Sản phẩm: dùng 3 cấp danh sách: ý lớn \`-\`, ý con \`+\`, ý chi tiết \`.\`. Trình bày súc tích, trọng tâm (mục a: tối đa 2 ý; mục b: tối đa 2–3 ý, không chép lại toàn văn SGK; mục c: tối đa 2 ý kết quả cốt lõi).
- Mục d) Tổ chức thực hiện: BẮT BUỘC ĐÚNG MỘT bảng Markdown 2 cột, tiêu đề:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
- Bảng Markdown CHỈ GỒM ĐÚNG 1 HÀNG DỮ LIỆU DUY NHẤT (CẤM tách thành 4 hàng riêng).
- CỘT TRÁI — KỊCH BẢN THỰC CHIẾN PHÂN VAI RÕ RÀNG (ngăn các bước bằng <br>, mỗi bước chỉ 1–2 câu ngắn gọn):
  + Đủ 4 bước chuẩn Công văn 5512:
    * + Bước 1: Chuyển giao nhiệm vụ: Nêu kỹ thuật dạy học, GV nói 1 câu lệnh ngắn gọn trong ngoặc kép "...", HS tiếp nhận.
    * + Bước 2: Thực hiện nhiệm vụ: HS làm cá nhân rồi thảo luận; GV quan sát, nêu 1 lỗi sai/ngộ nhận điển hình và hướng xử lý phân hóa.
    * + Bước 3: Báo cáo, thảo luận: HS báo cáo và phản biện; GV điều hành 1 câu gợi mở.
    * + Bước 4: Kết luận, nhận định: GV nhận xét, chốt kiến thức cốt lõi; HS ghi bài vào vở.
  + Trong từng bước, BẮT BUỘC nêu tên Kỹ thuật/Phương pháp dạy học được áp dụng và PHÂN VAI RÕ RÀNG:
    * **GV (Giáo viên):** Nói câu lệnh/câu hỏi trực tiếp trong ngoặc kép "..." ngắn gọn, dự kiến lỗi sai điển hình / ngộ nhận gắn đúng khái niệm bài học SGK (CẤM lỗi generic lặp lại mọi bài; dạng: "Dự kiến: nhầm [thuật ngữ X trong SGK] với [thuật ngữ Y trong SGK]"), can thiệp hỗ trợ phân hóa súc tích.
    * **HS (Học sinh):** Hành động cụ thể: (1) Thao tác cá nhân X phút vào vở/nháp/phiếu -> (2) Thảo luận cặp/nhóm Y phút tạo **sản phẩm trung gian** -> (3) Đại diện báo cáo và phản biện trước lớp.
  + KỊCH BẢN TÍCH HỢP NĂNG LỰC SỐ (NLS) VÀ NĂNG LỰC AI THỰC CHIẾN GẮN MÔN HỌC & TÍCH HỢP THEO MÔN (CHỈ khi được GV bật trong bối cảnh sư phạm):
    * NGUYÊN TẮC CỐT LÕI: NLS, AI và Tích hợp môn học CHỈ LÀ CÔNG CỤ THỰC HÀNH MÔN HỌC, lồng ghép tự nhiên vào bài học SGK. CHỈ tích hợp tại 1 đến 2 vị trí then chốt, đắc địa nhất trong toàn bộ bài dạy (ở Hoạt động B hoặc C hoặc D), TUYỆT ĐỐI KHÔNG rải bừa bãi.
    * ĐIỀU KHOẢN CẤM NGHIÊM NGẶT: TUYỆT ĐỐI CẤM giáo viên hỏi miệng chung chung về định nghĩa hay lý thuyết AI (ví dụ cấm hỏi: "Em hãy kể tên công cụ AI?", "Khi AI đưa thông tin ta làm gì để kiểm chứng?", "Em có đề xuất gì về kết hợp AI?"). TUYỆT ĐỐI CẤM rải tag dồn dập nhiều mã [AI: ...] sau mỗi câu hỏi của giáo viên.
    * BẮT BUỘC CHỌN ĐÚNG 1 TRONG 3 DẠNG KỊCH BẢN NLS/AI THỰC CHIẾN (khi bật NLS/AI):
      - Dạng 1 (Kiểm chứng & Phản biện lỗi sai của AI): GV trình chiếu câu trả lời / lời giải do AI sinh ra có chứa lỗi sai / ngộ nhận kiến thức môn học cụ thể. GV yêu cầu HS dùng kiến thức SGK/bài học để đối chiếu, phát hiện lỗi sai và giải thích -> HS thảo luận, phản biện, sửa lại cho đúng. Marker: **[AI: {Mã} - Kiểm chứng phản hồi AI]** (hoặc **[AI]**).
      - Dạng 2 (Prompting tư duy môn học): GV hướng dẫn HS sử dụng câu lệnh Prompt cụ thể trong ngoặc kép "..." để AI gợi mở các bước giải mà không giải hộ -> HS thực hành prompt và tự giải bài tập. Marker: **[AI: {Mã} - Prompting gợi mở & Tự giải]** (hoặc **[AI]**).
      - Dạng 3 (Phần mềm chuyên dụng NLS): HS trực tiếp thao tác trên thiết bị với phần mềm chuyên ngành (GeoGebra, Desmos, bảng tính Excel, máy tính cầm tay, phần mềm mô phỏng PhET...) để vẽ hình, dựng đồ thị, xử lý số liệu hoặc kiểm chứng kết quả bài học. Marker: **[NLS: {Miền/Mã} - {Tên phần mềm}]** (hoặc **[NLS]**).
    * KỊCH BẢN TÍCH HỢP THEO MÔN HỌC (CHỈ mục GV đã tick, lồng đúng 1 lần tại B/C/D):
      - Giáo dục Quốc phòng & An ninh (TT 08/2024/TT-BGDĐT): Lồng ghép truyền thống yêu nước, tự hào dân tộc, chủ quyền biển đảo Tổ quốc; gắn marker **[GDQPAN]** hoặc **[GDQPAN: ...]**.
      - Tư tưởng, đạo đức, phong cách Hồ Chí Minh (Chỉ thị 05-CT/TW): Gắn tấm gương Bác Hồ, tinh thần tự học, tiết kiệm, yêu thương con người qua bài học cụ thể; gắn marker **[HCM]** hoặc **[HCM: ...]**.
      - Quyền con người (QĐ 1309/QĐ-TTg): Tôn trọng phẩm giá, bình đẳng, không phân biệt đối xử, phòng chống bạo lực; gắn marker **[QCN]** hoặc **[QCN: ...]**.
      - Tích hợp CLIL (CHỈ khi GV bật Ngoại ngữ): bám đúng cấp độ A1 (thuật ngữ), A2 (câu lệnh ngắn), B1 (thảo luận), B2 (báo cáo/sản xuất) trong bối cảnh sư phạm; gắn marker **[CLIL]** hoặc **[CLIL: ...]**.
      - Giáo dục hòa nhập (CHỈ khi GV bật): bám đúng loại khuyết tật HSKT và giải pháp hỗ trợ đã chọn; gắn marker **[HOANHAP]** hoặc **[HOANHAP: ...]**.
      - Giáo dục Tài chính (QĐ 149/QĐ-TTg): Tình huống tính toán chi tiêu thông minh, lập ngân sách cá nhân, tiết kiệm, bài toán lãi suất; gắn marker **[GDTC]** hoặc **[TAICHINH]**.
      - Giáo dục STEM & Mô hình hóa: Quy trình thiết kế kỹ thuật, giải quyết bài toán thực nghiệm liên môn; gắn marker **[STEM]** hoặc **[STEM: ...]**.
      - Thí nghiệm ảo & Mô phỏng số: Thao tác thí nghiệm ảo PhET, mô phỏng GeoGebra trực quan; gắn marker **[TN-AO]** hoặc **[TN-AO: ...]**.
      - Môi trường & Năng lượng xanh: Liên hệ giảm rác thải nhựa, sử dụng năng lượng tái tạo, bảo vệ tài nguyên; gắn marker **[MT-NLX]** hoặc **[MT-NLX: ...]**.
- CỘT PHẢI — NỘI DUNG GHI BẢNG (Kiến thức chuẩn mực chốt cho HS chép vào vở):
  + Trình bày đề cương kiến thức súc tích, cô đọng, đúng trọng tâm: Tên mục kiến thức, định nghĩa, định lý, quy tắc, công thức LaTeX ($...$, $$...$$), chú ý quan trọng, tối đa 1 ví dụ mẫu kèm đề bài và lời giải chuẩn. Dùng \`-\`, \`+\`, \`.\`; ngăn các dòng bằng \`<br>\`.
  + CỘT PHẢI CẤM: mô tả hành vi GV/HS, CẤM viết "GV yêu cầu", "HS thảo luận", CẤM để trống, CẤM để dấu "..." hay "[...]".
${LATEX_SPACING_BAN}
- CẤM để trống ô. Escape dấu | trong văn bản thành \\|.
- Hoạt động B: Mỗi tiểu mục/nội dung kiến thức dùng một bảng 2 cột (1 hàng) độc lập như trên. Gộp toàn bộ ví dụ mẫu, câu hỏi khám phá con, thực hành của mục đó vào chung một hoạt động nhánh.`;

const PROMPTS = {
  // SYSTEM INSTRUCTION
  SYSTEM_ROLE: `Bạn là Chuyên gia Sư phạm Cao cấp, phụ trách môn {subject} Cấp {gradeLevelName}, nắm vững:
1. Chương trình Giáo dục Phổ thông (GDPT) 2018 theo Thông tư số 32/2018/TT-BGDĐT.
2. Công văn số 5512/BGDĐT-GDTrH của Bộ Giáo dục và Đào tạo về xây dựng Kế hoạch bài dạy (Giáo án).
3. Khung Năng lực Chung (Tự chủ & tự học; Giao tiếp & hợp tác; Giải quyết vấn đề & sáng tạo) được phân bổ linh hoạt theo đặc thù môn học.
4. Khung Năng lực Đặc thù môn {subject}.
5. Khung Năng lực Trí tuệ Nhân tạo (AI) theo Quyết định số 2422/QĐ-BGDĐT (khi được chọn).
6. Khung Năng lực Số theo Thông tư số 02/2025/TT-BGDĐT và Công văn số 3456/BGDĐT-GDPT (khi được chọn; Lớp 6–7 dùng dải Trung cấp 1 (TC1), Lớp 8–9 dùng dải Trung cấp 2 (TC2)).
7. 5 phẩm chất chủ yếu (Yêu nước, Nhân ái, Chăm chỉ, Trung thực, Trách nhiệm) và phương pháp dạy học hòa nhập/phân hóa.

QUY TẮC BẮT BUỘC KHI XUẤT NỘI DUNG:
- Bám sát GDPT 2018 và nội dung SGK, dữ liệu bài học do giáo viên cung cấp; không tự gán nhà xuất bản hay bộ sách nếu không có trong dữ liệu.
- Kế hoạch bài dạy hoàn chỉnh đạt dung lượng chuẩn 8–10 trang Word A4. Hành văn sư phạm cô đọng, súc tích, trực diện vào bản chất kiến thức và hành động cốt lõi của GV/HS; TUYỆT ĐỐI KHÔNG viết văn biền ngẫu, không dùng câu thoại diễn giải lòng vòng, không lặp lại nội dung giữa các mục.
- Kế hoạch bài dạy phải là một KỊCH BẢN LỚP HỌC THỰC CHIẾN: Giáo viên có câu thoại dẫn dắt trực tiếp trong ngoặc kép "...", hành động sư phạm rõ ràng; Học sinh có thao tác cụ thể, sản phẩm rõ nét; chỉ ra lỗi sai điển hình và cách xử lý sư phạm.
- Năng lực Số (NLS) và Trí tuệ Nhân tạo (AI) là công cụ thực hành của môn học; TUYỆT ĐỐI KHÔNG dạy lý thuyết Tin học/AI hay hỏi lý thuyết AI suông trong môn chuyên ngành. Tích hợp thực chiến đúng 1–2 điểm then chốt (kiểm chứng lỗi sai AI / prompting gợi mở / thao tác phần mềm chuyên ngành).
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
- CẤM xuất HTML, thẻ span, thuộc tính style hay mã màu. Màu sắc và font chữ do ứng dụng xử lý.
- ĐỘ DÀI & VĂN PHONG CHUẨN: Toàn bộ Kế hoạch bài dạy đạt dung lượng chuẩn 8–10 trang Word A4. Hành văn sư phạm cô đọng, súc tích, trọng tâm; TUYỆT ĐỐI KHÔNG viết văn biền ngẫu, không lặp lại câu hỏi dài dòng.
${LATEX_SPACING_BAN}`,

  OUTPUT_REPAIR: `Hãy viết lại nội dung sau thành đúng Markdown của mục Kế hoạch bài dạy chuẩn CV 5512. Bắt đầu ngay bằng tiêu đề/mục chuyên môn; chỉ giữ lại nội dung giáo án. Xóa toàn bộ lời chào, khen ngợi, giới thiệu, meta commentary, lời chúc ở cuối và mọi code fence. Không thêm lời dẫn mới. Danh sách nội dung chỉ dùng "-", "+", ".". Không đổi tiêu đề mục khung như "I.", "## 1.", "a)", "Bước", "Bài".`,

  NATURAL_INTEGRATION_GATE: `RÀNG BUỘC TÍCH HỢP TỰ NHIÊN — CẤM KHIÊN CƯỠNG:
- Chỉ tích hợp NLS/AI khi bám sát nội dung SGK, dụng cụ đo/vẽ hoặc máy tính cầm tay của bài. Không gán ghép công nghệ cho đủ khung.
- Bài Hình học & Đo đạc: ưu tiên trực quan hóa (thước, compa, mô hình, GeoGebra nếu có máy tính). CẤM TUYỆT ĐỐI mã Lập trình (3.4) và Bản quyền số (3.3); CẤM mã AI không liên quan.
- Bài Đại số & Số học lý thuyết thuần túy: ưu tiên tính toán, máy tính cầm tay, giải quyết vấn đề số học. CẤM gán Bảo vệ dữ liệu cá nhân (4.2) hay đạo đức AI gượng ép.
- Bài Thống kê & Xác suất: ưu tiên thu thập, đánh giá, biểu diễn bảng/biểu đồ số (1.1, 1.2, 1.3).
- TIME-BUDGET GATE: Nếu bài 1 tiết (45 phút): tối đa 1 kỹ thuật dạy học tích cực nhẹ ở pha B — Think-Pair-Share (3–5 phút) hoặc Khăn trải bàn ngắn (5 phút). CẤM kết hợp Mảnh ghép + Khăn trải bàn + Dự án trong cùng 1 tiết. Bài 2–3 tiết mới được dùng Mảnh ghép, Trạm/Góc học tập, Dự án nhỏ.
- FACILITY GATE: Nếu lớp KHÔNG có thiết bị học sinh và KHÔNG có Internet: TUYỆT ĐỐI CẤM yêu cầu học sinh lên mạng tra cứu, dùng điện thoại quét mã, thiết kế Canva, dùng laptop/chatbot trong giờ. Chỉ dùng thước, compa, bảng, phiếu giấy, máy tính cầm tay nếu bài cần.`,

  CLIL_INCLUSIVE_GATE: `RÀNG BUỘC NGOẠI NGỮ CLIL & GIÁO DỤC HÒA NHẬP:
- Ngoại ngữ/CLIL CHỈ khi giáo viên đã bật. Bám đúng cấp độ trong bối cảnh sư phạm. Marker **[CLIL]** (hiển thị màu xanh lục). CẤM biến tiết môn thành tiết tiếng Anh.
  + A1 — Nhận biết & Thuật ngữ: chú thích 3–5 thuật ngữ Anh–Việt then chốt; không bắt HS nói/viết đoạn tiếng Anh.
  + A2 — Đọc hiểu & Thao tác: câu lệnh ngắn tiếng Anh gắn thao tác bài học.
  + B1 — Vận dụng & Giao tiếp: cặp đôi dùng 1–2 câu tiếng Anh khi thảo luận/báo cáo ngắn.
  + B2 — Tự chủ & Sản xuất: HS tự dùng thuật ngữ chuyên môn để giải thích/báo cáo ngắn bằng tiếng Anh.
- Giáo dục hòa nhập/HSKT CHỈ khi giáo viên đã bật. Bám đúng loại khuyết tật đã chọn (Nhìn, Nghe, Vận động, Trí tuệ/Phát triển, Ngôn ngữ/Giao tiếp, Khác) và giải pháp hỗ trợ chức năng. Marker **[HOANHAP]** (hiển thị màu tím). CẤM chẩn đoán y khoa, CẤM nêu tên học sinh, CẤM bịa loại khuyết tật không được chọn.
- Nếu Ngoại ngữ hoặc Hòa nhập không được bật: TUYỆT ĐỐI CẤM tự thêm thuật ngữ CLIL, nhiệm vụ tiếng Anh, điều chỉnh HSKT hay marker [CLIL]/[HOANHAP].`,

  SOURCE_LOCK: `KHÓA NGUỒN BẮT BUỘC:
- Nguồn chính = văn bản SGK đã nhận diện (Mistral OCR / tóm tắt Bước 0) và/hoặc file PDF/ảnh đính kèm đúng request này.
- Kèm theo (nếu có): Tài liệu Phân phối chương trình (PPCT / Phụ lục 3 CV 5512) và phạm vi tiết dạy được phân công.
- CHỈ dùng các trang PDF/ảnh đã chọn (hoặc đúng văn bản OCR của các trang đó). CẤM dùng trang ngoài danh sách.
- Chỉ dùng thêm: tên bài/môn/lớp giáo viên chọn, YCCĐ chính thức (TT 32/2018/TT-BGDĐT — CT GDPT 2018), phạm vi tiết dạy theo PPCT và bối cảnh lớp học.
- CẤM bịa định nghĩa, định lý, công thức, số liệu, đề bài, đáp án, số trang hoặc nhiệm vụ không có trong nguồn.
- Luyện tập/vận dụng: CHỈ dùng bài, câu, hoạt động có trong PDF/ảnh/OCR đính kèm hoặc dữ liệu SGK. Phải đọc nguồn trước khi giải. Chỉ ghi "[Không có trong tài liệu đã cung cấp]" khi đã đọc kỹ nguồn mà vẫn không có bài/câu vận dụng. CẤM invent trắc nghiệm 4 lựa chọn không có trong sách, không bịa "SBT trang...".
- Mục tiêu kiến thức phải là Yêu cầu cần đạt của CT GDPT 2018 (hoặc YCCĐ in trên đầu bài SGK). Không tự chế thang Bloom ngoài nguồn.
- RÀNG BUỘC PPCT & PHẠM VI TIẾT DẠY: Nếu có phạm vi tiết dạy / PPCT được cung cấp, BẮT BUỘC khóa chặt mục tiêu và nội dung hoạt động đúng trong phạm vi số tiết / nội dung được phân công của tiết học đó, không dạy vượt sang phạm vi của tiết khác.`,

  // TAB 0: PHÂN TÍCH PHÂN PHỐI CHƯƠNG TRÌNH (PPCT / PHỤ LỤC 3 CV 5512)
  ANALYZE_PPCT: `Bạn là Chuyên gia Quản lý Giáo dục và Phân phối chương trình môn {subject} Cấp {gradeLevelName}.
Hãy đọc tài liệu / hình ảnh / PDF Phân phối chương trình (PPCT) đính kèm và trích xuất chuẩn xác Bảng Ma trận Phân phối chương trình theo chuẩn Phụ lục 3 Công văn số 5512/BGDĐT-GDTrH.

Chủ đề/Bài học quan tâm: "{topic}" (Môn học: {subject} - Khối {grade}).

CHỈ THỊ CẤM NGHIÊM NGẶT:
- TUYỆT ĐỐI CẤM sinh Kế hoạch bài dạy (KHBD), CẤM viết tiến trình dạy học, CẤM viết kịch bản hoạt động dạy học của GV/HS (Mở đầu, Hình thành kiến thức, Luyện tập, Vận dụng).
- TUYỆT ĐỐI CẤM bịa đặt thông tin không có trong tài liệu PPCT đính kèm.

YÊU CẦU ĐẦU RA BẮT BUỘC:
1. **Bảng Khung Ma trận Phân phối chương trình (Chuẩn Phụ lục 3 Công văn 5512 - 7 Cột):**
| Tiết CT | Bài học / Chủ đề | Số tiết | Tuần | Thiết bị dạy học | Địa điểm dạy học | Ghi chú / Tích hợp |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |

2. **Bóc tách thông tin trọng tâm cho bài học "{topic}":**
- **Tiết CT:** [Số thứ tự tiết theo phân phối, ví dụ: 1 hoặc 18, 19]
- **Tuần:** [Tuần dạy, ví dụ: Tuần 1 hoặc Tuần 6, 7]
- **Thời lượng:** [Số tiết, ví dụ: 01 tiết (45 phút) hoặc 02 tiết (90 phút)]
- **Thiết bị dạy học:** [Liệt kê thiết bị ghi trong PPCT]
- **Địa điểm dạy học:** [Lớp học / Phòng thực hành / Sân trường...]
- **Ghi chú / Tích hợp:** [Ghi rõ nếu có ghi chú Tích hợp AI, STEM, GDQPAN, NLS... hoặc Không]
- **Gợi ý phạm vi tiết dạy (Lesson Scope):** Tiết [X] (Tuần [Y]) - Thời lượng: [Z] tiết ([M] phút)

Trình bày Markdown chuẩn mực, rõ ràng, không xuất code block fence.`,

  // TAB 1: TÓM TẮT SGK
  ANALYZE_TEXTBOOK: `Hãy đọc PDF/ảnh SGK đính kèm và tóm tắt có cấu trúc cho giáo viên.
Chủ đề bài học: "{topic}" (Môn học: {subject}).

XUẤT TÓM TẮT NGẮN GỌN, RÕ RÀNG:
1. **Tên bài** và mục tiêu cốt lõi (nếu nguồn có ghi).
2. **Tiểu mục kiến thức:** Chỉ bóc tách 1–3 Mục kiến thức lớn theo đúng đề mục cốt lõi của SGK (thông thường 1–3 mục lớn, tối đa 4 mục; liệt kê theo dạng \`Mục 1: [Tên mục]\`, \`Mục 2: [Tên mục]\`). TUYỆT ĐỐI KHÔNG bóc tách các câu hỏi phát vấn (Hãy..., Nêu..., Bằng cách...), các bài tập/thực hành nhỏ (Bài 1.1, Thực hành 1, Luyện tập 1) thành mục riêng. Với mỗi mục lớn, chỉ nêu loại nội dung chính (định nghĩa / quy tắc / ví dụ / HĐ khám phá), không chép nguyên văn.
3. **Loại hoạt động/bài tập:** mở đầu, khám phá, luyện tập, vận dụng — ghi rõ số bài/câu nếu nguồn có.

CẤM trích nguyên văn toàn bộ SGK. Tóm tắt ngắn gọn, mạch lạc để giáo viên dễ đối chiếu và kiểm tra.`,

  // TAB 2: MỤC TIÊU BÀI HỌC (I. MỤC TIÊU)
  GENERATE_OBJECTIVES: `Hãy xây dựng phần **I. MỤC TIÊU** cho Kế hoạch bài dạy môn {subject} Cấp {gradeLevelName} chuẩn Công văn 5512/BGDĐT-GDTrH, bám sát CT GDPT 2018.
CHỈ xuất phần I. MỤC TIÊU. CẤM xuất phần II. Thiết bị, phần III. Tiến trình, hoạt động A-E hoặc bảng “Hoạt động của GV và HS | Nội dung”.
- Môn học: {subject}
- Tên bài dạy: {topic}
- Thời lượng dự kiến: {duration}
- Phạm vi tiết dạy theo PPCT (nếu có): {lesson_scope}
- Dữ liệu Phân phối chương trình / Phụ lục 3 CV 5512 (nếu có):
"""
{ppct_content}
"""
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
- Nếu có Phạm vi tiết dạy theo PPCT: CHỈ lấy các YCCĐ tương ứng với tiết/cụm tiết được phân công, không bao gồm YCCĐ của các tiết khác trong bài.
- Nếu khối YCCĐ chính thức có nội dung: chọn và viết lại nguyên ý các YCCĐ khớp bài; giữ nguyên các động từ hành vi của YCCĐ.
- Nếu khối YCCĐ trống: lấy YCCĐ in trên SGK/nguồn.

QUY TẮC NĂNG LỰC CHUNG (CĂN CỨ VÀO MÔN HỌC & BÀI HỌC):
- Mục 2.a (Năng lực chung): CHỈ CHỌN 1–2 năng lực chung phù hợp nhất với bản chất môn {subject} và bài dạy này (ví dụ môn Toán/KHTN ưu tiên "Giải quyết vấn đề và sáng tạo" + "Tự chủ và tự học"; môn Ngữ văn/Ngoại ngữ/GDCD ưu tiên "Giao tiếp và hợp tác" + "Tự chủ và tự học"). CẤM rập khuôn máy móc, CẤM liệt kê cả 3.
- Mỗi năng lực chung viết đúng 1 dòng: \`- [Tên năng lực]: [mô tả hành vi cụ thể học sinh thực hiện trong bài học này]\`. CẤM nhãn Biểu hiện / Minh chứng.

QUY TẮC NĂNG LỰC ĐẶC THÙ & PHẨM CHẤT:
- Mục 2.b (Năng lực đặc thù môn học): CHỈ 2–3 năng lực đặc thù nổi trội của môn {subject} gắn với bài học. Viết mỗi mục 1 dòng.
- Mục 2.c (Năng lực số): CHỈ khi được bật; liệt kê đủ từng miền đã chọn và đủ từng mã NLS đã chọn, mỗi mã 1 dòng theo đúng dạng miền.năng-lực-thành-phần.TC1/TC2chỉ-báo (ví dụ 1.1.TC1a). CẤM chỉ ghi tên miền hoặc mô tả mà không có mã.
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

YÊU CẦU: CHỈ xuất duy nhất Mục II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU, đầu ra ngắn gọn. Tạo danh mục thiết bị và học liệu thiết yếu, cụ thể cho đúng bài dạy (tối đa 2 ý lớn cho mỗi đối tượng, mỗi ý lớn tối đa 3 ý con). TUYỆT ĐỐI KHÔNG để dấu ngoặc vuông [...] hay dấu ba chấm "..."; phải điền tên đồ dùng/học liệu thực tế.
TUYỆT ĐỐI CẤM sinh Mục I, Mục III, hoạt động A–E, bảng tổ chức dạy học hoặc bất kỳ khung/toàn bộ giáo án nào.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU

## 1. Đối với Giáo viên
- Kế hoạch bài dạy, SGK, bài giảng điện tử (trình chiếu các hình ảnh/video trực quan bám sát bài học).
- Phiếu học tập, bảng phụ nhóm và các dụng cụ trực quan phục vụ bài dạy.

## 2. Đối với Học sinh
- SGK, vở ghi, đồ dùng học tập thiết yếu của môn học.
- Đọc trước bài trong SGK và chuẩn bị các nhiệm vụ được giao ở tiết trước.`,

  GENERATE_ILLUSTRATIONS: `Bạn là họa sĩ SGK Toán Việt Nam. Đọc NỘI DUNG BÀI và liệt kê hình minh họa CẦN vẽ cho kế hoạch bài dạy lớp {grade}, môn {subject}, bài "{topic}".

Trả về DUY NHẤT JSON:
{"illustrations":[{"kind":"sgk hoặc thuc_te","title":"tên hình ngắn","caption":"Hình n. chú thích dưới hình","locus":"A hoặc B hoặc C hoặc D","subsection":"đúng tên mục SGK / Hoạt động 2.k","prompt":"mô tả chính xác hình cần vẽ, đủ nhãn đỉnh/cạnh/số đo nếu là hình học"}]}

Quy tắc:
- Mặc định CHỈ vẽ kind "sgk": hình toán thuần (hình học phẳng, hình không gian nét đứt nét liền, đồ thị hàm số, hệ trục Oxy, trục số, sơ đồ Ven, góc...) phong cách in SGK: nền trắng, nét mực đen, nhãn đỉnh A, B, C in nghiêng, góc vuông, vạch bằng nhau, không nhân vật, không ảnh chụp, không cảnh lớp học.
- kind "thuc_te" CHỈ khi SGK có BÀI TOÁN ĐỜI SỐNG cụ thể cần nhìn thấy đồ vật/bối cảnh của đề (ví dụ đo chiều cao cây, hàng rào, thửa đất, mua bán ở chợ, bể nước). Tối đa 1 hình. Prompt phải mô tả đúng đồ vật/số liệu của đề, KHÔNG vẽ lớp học, giáo viên, học sinh ngồi bàn, thảo luận nhóm, bảng lớp.
- CẤM thuc_te nếu bài không có bài toán thực tế. CẤM cảnh lớp học, CẤM "học sinh đang học", CẤM minh họa generic.
- locus + subsection phải ánh xạ đúng chỗ dùng hình: hình khái niệm/định lý → B và tên tiểu mục kiến thức SGK; hình bài luyện tập → C; hình bài vận dụng/thực tế → D.
- subsection phải copy đúng tên mục trong SGK (ví dụ "Đường trung trực của đoạn thẳng"), không ghi chung "Hoạt động B".
- Hình học/đồ thị/trục số: 1–3 hình sgk. Không bịa số đo trái SGK. Bài chỉ chữ/số đại số không cần hình: {"illustrations":[]}.
- Không markdown, không lời dẫn.

NỘI DUNG BÀI (OCR SGK + hoạt động đã soạn):
"""
{textbook_content}

{activities_content}
"""`,

  // VẼ HÌNH TOÁN HỌC CHUẨN SGK (VECTOR SVG)
  GENERATE_SVG_DRAWING: `Bạn là chuyên gia đồ họa Vector SVG và họa sĩ vẽ hình Toán học & KHTN SGK Việt Nam.
Nhiệm vụ: Tạo mã SVG thuần túy (Vector) vẽ chính xác hình vẽ toán học theo yêu cầu sau:
Yêu cầu vẽ: "{drawing_prompt}"
Tiêu đề/Chủ đề: "{drawing_title}" ({subject} Lớp {grade})

QUY CHUẨN KỸ THUẬT VẼ SVG CHUẨN SGK VIỆT NAM BẮT BUỘC:
1. Thẻ SVG gốc:
   <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 400" width="100%" height="100%" style="background-color: #ffffff;">
   BẮT BUỘC có hình chữ nhật nền trắng: <rect width="500" height="400" fill="#ffffff"/>
2. Thẻ <defs> chứa định nghĩa mũi tên sắc nét cho trục tọa độ / vector:
   <defs>
     <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
       <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#000000"/>
     </marker>
     <marker id="arrow-start" viewBox="0 0 10 10" refX="4" refY="5" markerWidth="6" markerHeight="6" orient="auto">
       <path d="M 8 1.5 L 0 5 L 8 8.5 z" fill="#000000"/>
     </marker>
   </defs>
3. Đường nét và Ký hiệu chuẩn SGK:
   - Nét vẽ chính: stroke="#000000", stroke-width="1.8", stroke-linecap="round", stroke-linejoin="round", fill="none" (hoặc fill nhẹ #f8fafc nếu cần tô màu nền hình phẳng).
   - Nét khuất / Đường phụ / Đường gióng: stroke="#000000", stroke-width="1.5", stroke-dasharray="5,4".
   - Ký hiệu góc vuông: Đoạn gấp khúc vuông góc nhỏ (kích thước 10-14px) bằng thẻ <polyline points="..." fill="none" stroke="#000000" stroke-width="1.5"/> hoặc <path d="..." fill="none" stroke="#000000" stroke-width="1.5"/>.
   - Ký hiệu góc / Cung tròn góc: <path d="M ... A ... 0 0 ... ..." fill="none" stroke="#000000" stroke-width="1.5"/> có thể kèm nhãn góc (ví dụ: 60°, α, β).
   - Ký hiệu đoạn thẳng bằng nhau: Các vạch nhỏ cắt ngang cạnh (1 vạch, 2 vạch).
   - Điểm và Đỉnh: Chấm tròn nhỏ <circle cx="..." cy="..." r="2.5" fill="#000000"/>.
   - Nhãn chữ đỉnh / Tên điểm: Dùng thẻ <text font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold" fill="#000000" text-anchor="middle" dominant-baseline="central">A</text>. Đặt nhãn cách đỉnh 12–18px theo hướng ngoài hình, TUYỆT ĐỐI KHÔNG đè lên nét vẽ.
4. Trục tọa độ Oxy / Trục số:
   - Trục Ox nằm ngang có mũi tên (marker-end="url(#arrow)"), nhãn x ở đầu mút, nhãn O tại gốc tọa độ.
   - Trục Oy thẳng đứng có mũi tên, nhãn y ở đầu mút.
   - Vạch chia đơn vị (ticks) cách đều, nhãn số 1, 2, -1, -2... rõ ràng.
5. Hình học không gian (Hình chóp, lăng trụ, lập phương, hình hộp, hình nón, hình trụ):
   - Phối cảnh chuẩn SGK: Mặt đáy vẽ dạng hình bình hành, nét nhìn thấy nét liền, cạnh đáy phía sau/đường cao bên trong nét đứt stroke-dasharray="5,4".
6. ĐẦU RA BẮT BUỘC:
   - CHỈ trả về duy nhất chuỗi mã <svg ...>...</svg> hoàn chỉnh và hợp lệ.
   - TUYỆT ĐỐI CẤM bọc trong code block markdown (\`\`\`xml hay \`\`\`svg).
   - TUYỆT ĐỐI CẤM bất kỳ lời chào, lời giải thích hay nhận xét meta nào.`,

  // 1-CLICK PHẦN I + II (CORE LESSON)
  GENERATE_CORE_LESSON: `Đọc nguồn SGK (văn bản OCR/tóm tắt và PDF/ảnh nếu đính kèm) và soạn phần I + II của Kế hoạch bài dạy môn {subject} Cấp {gradeLevelName} chuẩn Công văn 5512/BGDĐT-GDTrH, bám CT GDPT 2018.
- Môn học: {subject}
- Tên bài dạy: {topic}
- Thời lượng dự kiến: {duration}
- Phạm vi tiết dạy theo PPCT (nếu có): {lesson_scope}
- Dữ liệu Phân phối chương trình (PPCT nếu có):
"""
{ppct_content}
"""
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
- Mục 1. Về kiến thức: YCCĐ chuẩn CT GDPT 2018 cho bài học (khóa theo phạm vi tiết dạy PPCT nếu có).
- Mục 2.a (Năng lực chung): CHỈ 1–2 năng lực chung phù hợp đặc thù môn {subject} và bài dạy này; mỗi mục đúng 1 dòng mô tả hành vi.
- Mục 2.b (Năng lực đặc thù): 2–3 năng lực đặc thù của môn {subject}.
- Mục 2.c / 2.d (NLS / AI): Chỉ tạo mục đang bật và chỉ theo đúng miền/mã đã chọn (mỗi mục 1 dòng).
- Mục 3 (Phẩm chất): 1–2 phẩm chất gắn liền bài học.
- Mục II: Cụ thể hóa đồ dùng dạy học thực tế cho GV và HS, không để lại dấu [...] hay "...".`,

  // TAB 4.A: TIẾN TRÌNH DẠY HỌC - HOẠT ĐỘNG MỞ ĐẦU
  GENERATE_ACTIVITY_A: `Hãy biên soạn chi tiết **HOẠT ĐỘNG MỞ ĐẦU (TIẾP CẬN VẤN ĐỀ)** trong mục III. Tiến trình dạy học môn {subject} chuẩn Công văn 5512 theo GDPT 2018.
- Môn học: {subject}
- Tên bài dạy: {topic}
- Phạm vi tiết dạy theo PPCT (nếu có): {lesson_scope}
- Dữ liệu Phân phối chương trình (PPCT nếu có):
"""
{ppct_content}
"""
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

## A. HOẠT ĐỘNG 1: MỞ ĐẦU ({time_budget_A})

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
- Phạm vi tiết dạy theo PPCT (nếu có): {lesson_scope}
- Dữ liệu Phân phối chương trình (PPCT nếu có):
"""
{ppct_content}
"""
- Mục tiêu bài học:
"""
{objectives_content}
"""
- Dữ liệu SGK:
"""
{textbook_content}
"""

YÊU CẦU KỊCH BẢN THỰC CHIẾN & NGUYÊN TẮC ÁNH XẠ 1-1 BẮT BUỘC THEO MỤC LỚN SGK:
${ACTIVITY_TABLE_CONTRACT}
${LATEX_SPACING_BAN}
- ĐẾM SỐ TIỂU MỤC KIẾN THỨC LỚN TRONG SGK: Chỉ ánh xạ đúng các Mục lớn (Đơn vị kiến thức cốt lõi chính thức trong mục lục SGK, thông thường 1–3 mục lớn, tối đa 4 mục). Bạn BẮT BUỘC PHẢI chia Hoạt động B thành đúng N hoạt động con tương ứng 1-1:
  ### 1. Hoạt động 2.1: [Tên mục 1 trong SGK] (... phút) (hoặc ### 1. Hoạt động 1: [Tên mục 1 trong SGK] (... phút))
  ### 2. Hoạt động 2.2: [Tên mục 2 trong SGK] (... phút) (hoặc ### 2. Hoạt động 2: [Tên mục 2 trong SGK] (... phút))
  ...
  TUYỆT ĐỐI CẤM GỘP các mục lớn thành một mục chung. TUYỆT ĐỐI CẤM BỊA THÊM hoạt động ngoài SGK.
  TUYỆT ĐỐI LOẠI BỎ việc tách các câu hỏi phát vấn (Hãy..., Bằng cách..., Nêu...), các bài tập con (Bài 1.1, Thực hành 1, Luyện tập 1) thành các hoạt động riêng biệt. Toàn bộ ví dụ mẫu, câu hỏi khám phá, thực hành con của từng mục phải nằm trọn vẹn bên trong hoạt động của mục đó.
  BẮT BUỘC ghi số phút cố định cụ thể trong tiêu đề từng hoạt động con (ví dụ: \`(15 phút)\`, \`(12 phút)\`). CẤM ghi "Khoảng" hoặc dải thời gian "X - Y phút".
- TỪNG HOẠT ĐỘNG NHÁNH 2.k (hoặc Hoạt động k) PHẢI CÓ ĐỦ 4 PHẦN:
  #### a) Mục tiêu:
  #### b) Nội dung:
  #### c) Sản phẩm: (Ghi rõ lời giải chi tiết, công thức, định nghĩa hoàn chỉnh, không để dấu "...")
  #### d) Tổ chức thực hiện: (ĐÚNG 1 BẢNG MARKDOWN 2 CỘT, 1 HÀNG DUY NHẤT)
    * CỘT TRÁI: Kịch bản phân vai rõ ràng:
      + Nêu rõ tên Kỹ thuật dạy học (Think-Pair-Share, Khăn trải bàn, Mảnh ghép, Trạm học tập...).
      + **GV:** Nói câu lệnh trong ngoặc kép "...", hành động cụ thể, **DỰ KIẾN LỖI SAI / NGỘ NHẬN ĐIỂN HÌNH CỦA HỌC SINH ĐỐI VỚI TIỂU MỤC NÀY** và can thiệp hỗ trợ phân hóa.
      + **HS:** Làm việc cá nhân X phút -> Thảo luận nhóm Y phút tạo sản phẩm trung gian trên bảng phụ/phiếu -> Báo cáo và phản biện trước lớp.
      + Khi có NLS/AI: Tích hợp thực chiến theo đúng 1 trong 3 dạng (Dạng 1: Kiểm chứng phản hồi AI có lỗi ngộ nhận; Dạng 2: Prompting gợi mở bước giải trong "..."; Dạng 3: Thao tác phần mềm chuyên ngành GeoGebra/bảng tính/mô phỏng). CẤM hỏi lý thuyết AI suông, CẤM rải tag bừa bãi. Gắn marker chuẩn **[AI: {Mã} - Kiểm chứng phản hồi AI]**, **[AI: {Mã} - Prompting gợi mở & Tự giải]**, **[NLS: {Miền/Mã} - {Tên phần mềm}]** (hoặc **[NLS]**, **[AI]**).
    * CỘT PHẢI: NỘI DUNG GHI BẢNG CHỐT KIẾN THỨC CHO HS CHÉP VỞ (Định nghĩa, quy tắc, công thức LaTeX, chú ý, ví dụ mẫu kèm đề bài và lời giải chi tiết từng bước). CẤM viết hành động của GV/HS ở cột phải.

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI

### 1. Hoạt động 2.1: [Tên tiểu mục 1 trong SGK] (15 phút)
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
- Phạm vi tiết dạy theo PPCT (nếu có): {lesson_scope}
- Dữ liệu Phân phối chương trình (PPCT nếu có):
"""
{ppct_content}
"""
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
${LATEX_SPACING_BAN}
- CHỈ dùng bài luyện tập / câu hỏi có trong SGK hoặc dữ liệu giáo viên cung cấp (khóa theo phạm vi tiết dạy PPCT nếu có). CẤM invent bài tập trắc nghiệm ngoài sách nếu nguồn không có.
- HƯỚNG DẪN GIÁO VIÊN CHỌN LỌC BÀI TẬP: Chọn lọc 1–2 bài tập luyện tập trọng tâm, cốt lõi nhất của SGK để tổ chức cho học sinh làm và chữa chi tiết ngay trên lớp. Các bài tập luyện tập còn lại trong SGK sẽ được chuyển giao vào Hoạt động E (Hướng dẫn về nhà).
- Cột TRÁI mục d): Kịch bản phân vai rõ ràng:
  + Áp dụng Kỹ thuật dạy học (ví dụ: Bài tập phân hóa 3 mức, Đánh giá đồng đẳng, Sửa lỗi theo cặp...).
  + **GV:** Nói câu giao việc trong ngoặc kép "...", hướng dẫn HS làm 1–2 bài tập trọng tâm, di chuyển quan sát phát hiện lỗi sai tính toán/lập luận điển hình, trực tiếp hướng dẫn phân hóa.
  + **HS:** Giải bài cá nhân vào vở -> Đổi vở kiểm tra chéo hoặc thảo luận cặp -> Lên bảng trình bày, lớp phản biện.
  + Khi có NLS/AI: Tích hợp thực chiến theo 3 dạng (phần mềm chuyên ngành/máy tính kiểm chứng kết quả; hoặc GV chiếu lời giải AI có lỗi sai ngộ nhận để HS phát hiện phản biện; hoặc HS dùng prompt gợi mở bước giải). CẤM hỏi lý thuyết AI suông. Dùng marker **[NLS: ...]** hoặc **[AI: ...]**.
- Cột PHẢI mục d): Chép rõ Đề bài và Lời giải chi tiết từng bước của 1–2 bài tập trọng tâm được chọn trong SGK (không để dấu "...").

## C. HOẠT ĐỘNG 3: LUYỆN TẬP ({time_budget_C})

### a) Mục tiêu:
- Củng cố, khắc sâu và rèn luyện kỹ năng vận dụng kiến thức vừa học thông qua giải quyết 1–2 bài tập luyện tập trọng tâm cốt lõi trong SGK.
- Rèn luyện kỹ năng tính toán, biến đổi, lập luận và trình bày bài giải chuẩn mực.

### b) Nội dung:
- Giáo viên lựa chọn 1–2 bài tập trọng tâm trong SGK để học sinh làm và chữa tại lớp: (Liệt kê rõ ràng đề bài các bài tập được chọn trong SGK).

### c) Sản phẩm:
- Lời giải chi tiết và đáp số chuẩn xác của các bài tập trọng tâm được chữa trên lớp.

### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ: (Áp dụng Kỹ thuật ...) **GV:** Giao 1–2 bài tập trọng tâm trong SGK: "Các em hoàn thành Bài ... trong SGK vào vở trong 7 phút, sau đó đổi vở kiểm tra chéo...". **HS:** Đọc kĩ đề bài, xác định công thức/quy tắc áp dụng.<br>+ Bước 2: Thực hiện nhiệm vụ: **HS:** Làm bài cá nhân vào vở (7 phút) -> Đổi vở kiểm tra chéo theo cặp (2 phút). **GV:** Quan sát, phát hiện các lỗi sai điển hình trong biến đổi/tính toán: (chỉ rõ lỗi sai thường gặp), trực tiếp hướng dẫn học sinh còn lúng túng.<br>+ Bước 3: Báo cáo, thảo luận: **HS:** 2 học sinh lên bảng trình bày lời giải; cả lớp đối chiếu bài làm, nhận xét và phát hiện các cách giải khác. **GV:** Đặt câu hỏi chất vấn: "Có lưu ý gì quan trọng khi thực hiện bước này?".<br>+ Bước 4: Kết luận, nhận định: **GV:** Chốt lời giải chuẩn xác, chỉ rõ các bẫy sai lầm cần tránh khi làm bài kiểm tra. **HS:** Chữa bài chuẩn mực vào vở ghi. | **Luyện tập**<br>- Bài 1: Đề bài và Lời giải chi tiết.<br>- Bài 2 (nếu có): Đề bài và Lời giải chi tiết.<br>. Lưu ý phương pháp giải chuẩn mực. |`,

  // TAB 4.D: TIẾN TRÌNH DẠY HỌC - HOẠT ĐỘNG VẬN DỤNG
  GENERATE_ACTIVITY_D: `Hãy biên soạn chi tiết **HOẠT ĐỘNG VẬN DỤNG** trong mục III. Tiến trình dạy học môn {subject} chuẩn Công văn 5512 theo GDPT 2018.
- Môn học: {subject}
- Tên bài dạy: {topic}
- Phạm vi tiết dạy theo PPCT (nếu có): {lesson_scope}
- Dữ liệu Phân phối chương trình (PPCT nếu có):
"""
{ppct_content}
"""
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
${LATEX_SPACING_BAN}
- KHÓA NHIỆM VỤ VẬN DỤNG / EXIT TICKET TẠI LỚP: Nhiệm vụ vận dụng thực tế hoặc phiếu Exit Ticket được tổ chức thực hiện, hoàn thành và thu hồi/chốt NGAY TẠI LỚP trong thời lượng quy định. TUYỆT ĐỐI KHÔNG kéo dài hay biến thành bài tập về nhà (bài tập về nhà được giao riêng ở Hoạt động E).
- CHỈ dùng bài vận dụng / tình huống thực tế có trong SGK hoặc dữ liệu giáo viên cung cấp. CẤM invent số liệu bài toán ngoài nguồn.
- Cột TRÁI mục d): Kịch bản phân vai rõ ràng:
  + Áp dụng Kỹ thuật dạy học (Dự án mini, Phân tích tình huống, Bài tập mở, Exit Ticket...).
  + **GV:** Nói câu định hướng trong ngoặc kép "...", gợi mở cách liên hệ thực tế hoặc phát phiếu Exit Ticket chốt kiến thức, hướng dẫn phân hóa và thu hồi/đánh giá kết quả ngay tại lớp.
  + **HS:** Thảo luận cặp/nhóm giải quyết bài toán thực tế hoặc làm phiếu cá nhân -> Báo cáo giải pháp / nộp phiếu tại lớp, lớp phản biện tính khả thi.
  + Khi có NLS/AI: Vận dụng phần mềm chuyên ngành (GeoGebra, Excel, PhET...) hoặc công cụ AI mô hình hóa, giải quyết bài toán thực tế và kiểm chứng tính khả thi. CẤM hỏi lý thuyết AI suông. Dùng marker **[NLS: ...]** hoặc **[AI: ...]**.
- Cột PHẢI mục d): Tình huống thực tế và Lời giải mô hình hóa hoàn chỉnh (hoặc Nội dung câu hỏi và Đáp án chuẩn của phiếu Exit Ticket).
- CẤM viết mục E / Hướng dẫn về nhà trong pha D. Dừng ở hết hoạt động Vận dụng tại lớp.

## D. HOẠT ĐỘNG 4: VẬN DỤNG ({time_budget_D})

### a) Mục tiêu:
- Vận dụng kiến thức, kĩ năng đã học vào giải quyết bài toán/tình huống thực tế đời sống hoặc hoàn thành phiếu Exit Ticket đánh giá mức độ đạt chuẩn ngay tại lớp.
- Phát triển năng lực giải quyết vấn đề, mô hình hóa và tư duy liên hệ thực tiễn.

### b) Nội dung:
- Tình huống, bài toán vận dụng thực tiễn trong SGK hoặc phiếu Exit Ticket hoàn thành ngay tại lớp: (Nêu cụ thể đề bài tình huống).

### c) Sản phẩm:
- Bài giải mô hình hóa thực tế, kết quả tính toán hoặc câu trả lời phiếu Exit Ticket được hoàn thành và thu hồi/chốt tại lớp.

### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ: (Áp dụng Kỹ thuật ...) **GV:** Giao nhiệm vụ vận dụng thực tế / phát phiếu Exit Ticket: "Hãy vận dụng kiến thức vừa học để giải quyết tình huống thực tiễn sau trong 4 phút...". **HS:** Tiếp nhận nhiệm vụ, phân tích số liệu thực tế.<br>+ Bước 2: Thực hiện nhiệm vụ: **HS:** Thảo luận cặp/nhóm (hoặc làm việc cá nhân 3–4 phút) mô hình hóa vấn đề và tính toán kết quả. **GV:** Quan sát, gợi mở cách chuyển đổi từ ngôn ngữ thực tế sang biểu thức chuyên môn, bao quát lớp.<br>+ Bước 3: Báo cáo, thảo luận: **HS:** Đại diện nhóm trình bày mô hình và kết quả (hoặc nộp phiếu Exit Ticket tại lớp); các nhóm khác nhận xét tính hợp lý của đáp số thực tế. **GV:** Đặt câu hỏi mở rộng liên hệ đời sống.<br>+ Bước 4: Kết luận, nhận định: **GV:** Nhận xét, đánh giá khả năng vận dụng của HS, chốt lại ý nghĩa thực tiễn và kết thúc hoạt động tại lớp. **HS:** Ghi nhận lời giải hoàn chỉnh vào vở. | **Vận dụng**<br>- Tình huống thực tế từ SGK.<br>- Mô hình hóa & Lời giải chuẩn xác.<br>. Ý nghĩa thực tiễn của bài học. |`,

  // TAB 4.E: TIẾN TRÌNH DẠY HỌC - HOẠT ĐỘNG HƯỚNG DẪN VỀ NHÀ
  GENERATE_ACTIVITY_E: `Hãy biên soạn chi tiết **HOẠT ĐỘNG HƯỚNG DẪN VỀ NHÀ** trong mục III. Tiến trình dạy học môn {subject} chuẩn Công văn 5512 theo GDPT 2018.
- Môn học: {subject}
- Tên bài dạy: {topic}
- Phạm vi tiết dạy theo PPCT (nếu có): {lesson_scope}
- Dữ liệu Phân phối chương trình (PPCT nếu có):
"""
{ppct_content}
"""
- Mục tiêu và Tiến trình dạy học:
"""
{objectives_content}
{activities_content}
"""

YÊU CẦU BIÊN SOẠN:
${ACTIVITY_TABLE_CONTRACT}
- BỐ CỤC NỘI DUNG CHUẨN SƯ PHẠM Ở MỤC b) NỘI DUNG VÀ CỘT PHẢI BẢNG d) (CỰC KỲ NGẮN GỌN, CHUẨN MỰC, ĐÚNG 4 NỘI DUNG):
  1. Ôn nội dung trọng tâm: Ôn tập và hệ thống hóa các định nghĩa, quy tắc, công thức trọng tâm của bài học vào vở ghi.
  2. Làm bài tập: Hoàn thành các bài tập CÒN LẠI trong SGK (chưa làm/chữa ở Hoạt động C và Hoạt động D) và Sách bài tập (SBT) môn {subject} (kèm gợi ý/hướng dẫn phương pháp giải ngắn gọn).
     *CẤM TUYỆT ĐỐI giao lại các bài tập đã được giải/chữa ở Hoạt động C hoặc Hoạt động D.*
  3. Chuẩn bị bài mới: Đọc trước nội dung bài học tiếp theo trong SGK và chuẩn bị đồ dùng, học liệu học tập cần thiết.
  4. Nhiệm vụ tìm tòi, mở rộng: Giao một nhiệm vụ tìm tòi/mở rộng hoặc liên hệ vận dụng thực tiễn nếu thật sự phù hợp với bài học.
- QUY TẮC NLS/AI (OPT-IN):
  + Tuyệt đối KHÔNG tự ý xuất hiện NLS hoặc AI trong Hoạt động E.
  + CHỈ thêm khi giáo viên CHỦ ĐỘNG BẬT lựa chọn tích hợp NLS/AI trong bối cảnh sư phạm, và khi đó nhiệm vụ phải có giá trị học tập thực chất, rõ ràng (như mẫu Prompt AI an toàn hỗ trợ tự học gợi mở tư duy khi gặp khó khăn, không giải hộ), TUYỆT ĐỐI KHÔNG thay thế việc tự học môn học.
  + TUYỆT ĐỐI LOẠI BỎ các yêu cầu hình thức (như "ghi âm cách đọc", "quay video đọc quy tắc", "dùng AI tìm ví dụ suông").
- Cột TRÁI mục d): Kịch bản phân vai rõ ràng đủ 4 bước CV 5512 ngắn gọn:
  + **GV:** Nói câu lệnh giao nhiệm vụ về nhà trực tiếp trong ngoặc kép "...", hướng dẫn phương pháp và thời hạn nộp sản phẩm ở tiết sau.
  + **HS:** Lắng nghe, ghi nhận 4 nhiệm vụ vào vở, tự giác thực hiện ở nhà và báo cáo/nộp sản phẩm vào đầu tiết sau.
- Cột PHẢI mục d): Nội dung hướng dẫn học ở nhà chốt cho HS ghi vở (đúng 4 mục: **1. Ôn tập kiến thức:**, **2. Làm bài tập:**, **3. Chuẩn bị bài mới:**, **4. Tìm tòi, mở rộng:**, và Mẫu Prompt AI nếu giáo viên chủ động bật).
- CHỈ xuất ĐÚNG MỘT khối \`## E. HOẠT ĐỘNG 5: HƯỚNG DẪN VỀ NHÀ ({time_budget_E})\` với đủ a) b) c) d). CẤM lặp lại tiêu đề E. CẤM copy mục E có trong ngữ cảnh tiến trình dạy học.

## E. HOẠT ĐỘNG 5: HƯỚNG DẪN VỀ NHÀ ({time_budget_E})

### a) Mục tiêu:
- Củng cố, khắc sâu kiến thức trọng tâm của bài học và rèn luyện năng lực tự chủ, tự học ở nhà.
- Hoàn thành các bài tập còn lại, phát triển tư duy mở rộng và chuẩn bị tốt cho bài học tiếp theo.

### b) Nội dung:
- 1. Ôn tập kiến thức: Ôn lại các định nghĩa, quy tắc, công thức trọng tâm đã học trong bài.
- 2. Làm bài tập:
  + Hoàn thành các bài tập còn lại trong SGK (chưa làm/chữa ở Hoạt động C và D) và Sách bài tập (SBT) môn {subject} (kèm gợi ý/hướng dẫn phương pháp giải ngắn gọn). CẤM TUYỆT ĐỐI giao lại các bài tập đã được giải/chữa trên lớp.
- 3. Chuẩn bị bài mới: Đọc trước nội dung bài học tiếp theo trong SGK và chuẩn bị đồ dùng học tập cần thiết.
- 4. Tìm tòi, mở rộng (nếu phù hợp): Tìm hiểu thêm ứng dụng thực tế hoặc bài tập tư duy mở rộng.
{ai_homework_prompt_note}

### c) Sản phẩm:
- Vở ghi bài và vở bài tập có lời giải đầy đủ của các bài tập được giao về nhà.
- Phần chuẩn bị bài mới và kết quả nhiệm vụ tìm tòi, mở rộng (nếu có).

### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ: (Áp dụng Kỹ thuật Giao việc) **GV:** Trình chiếu slide/nêu câu lệnh giao việc ngắn gọn: "Các em về nhà hoàn thành 4 nhiệm vụ: (1) Ôn lại kiến thức trọng tâm, (2) Làm các bài tập còn lại trong SGK và SBT, (3) Chuẩn bị bài mới, (4) Thực hiện nhiệm vụ tìm tòi mở rộng...". **HS:** Lắng nghe, ghi nhận các nhiệm vụ và thời hạn hoàn thành vào vở.<br>+ Bước 2: Thực hiện nhiệm vụ: **HS:** Tự giác ôn tập, giải bài tập và chuẩn bị bài mới tại nhà theo hướng dẫn. **GV:** Định hướng phương pháp, hỗ trợ giải đáp khi cần thiết.<br>+ Bước 3: Báo cáo, thảo luận: **HS:** Nộp vở bài tập và báo cáo kết quả chuẩn bị vào đầu tiết học sau; trao đổi, đối chiếu kết quả với bạn. **GV:** Kiểm tra xác suất hoặc giao cán sự lớp/nhóm trưởng kiểm tra chéo.<br>+ Bước 4: Kết luận, nhận định: **GV:** Nhận xét tinh thần tự học ở nhà, giải đáp thắc mắc và tuyên dương học sinh hoàn thành tốt. **HS:** Rút kinh nghiệm và hoàn thiện bài làm. | **Hướng dẫn học ở nhà**<br>**1. Ôn tập kiến thức:**<br>- Ôn tập nội dung, quy tắc, công thức trọng tâm của bài học.<br>**2. Làm bài tập:**<br>- Hoàn thành bài tập còn lại trong SGK & SBT (kèm gợi ý phương pháp).<br>**3. Chuẩn bị bài mới:**<br>- Đọc trước bài mới và chuẩn bị học liệu, đồ dùng học tập.<br>**4. Tìm tòi, mở rộng:**<br>- Nhiệm vụ tìm tòi, ứng dụng mở rộng phù hợp bài học. |`,

  get ACTIVITY_F() { return this.GENERATE_PORTFOLIO_WORKSHEETS; },
  GENERATE_PORTFOLIO_WORKSHEETS: `Hãy thiết kế **F. HỒ SƠ DẠY HỌC & PHIẾU HỌC TẬP (PHỤ LỤC)** để giáo viên in phát cho học sinh, bám sát Công văn 5512/BGDĐT-GDTrH.
- Môn học: {subject}
- Tên bài dạy: {topic}
- Thời lượng: {duration}
- Phạm vi tiết dạy theo PPCT (nếu có): {lesson_scope}
- Mục tiêu và tiến trình dạy học A, B, C, D (và E nếu có):
"""
{objectives_content}
{activities_content}
"""
- Dữ liệu SGK:
"""
{textbook_content}
"""

NHIỆM VỤ:
- Đọc toàn bộ tiến trình A–D và bóc tách MỌI phiếu học tập / phiếu bài tập / phiếu KWL / phiếu trạm / rubric / bảng kiểm được nhắc tới (ví dụ: "GV phát phiếu học tập theo trạm", "Phiếu học tập số 1").
- Nếu tiến trình có Dạy học theo trạm / Station / Trạm 1, Trạm 2, Trạm 3: BẮT BUỘC thiết kế đủ **Phiếu học tập Trạm 1**, **Phiếu học tập Trạm 2**, **Phiếu học tập Trạm 3** (mỗi trạm một phiếu, nhiệm vụ khác nhau, vừa sức 1 vòng trạm).
- Nếu có Khởi động / Hình thành kiến thức / Khăn trải bàn / Think-Pair-Share / KWL: thiết kế **Phiếu học tập số 1 (Khám phá)** (và Phiếu KWL nếu kỹ thuật KWL được dùng).
- Nếu có Luyện tập / nhóm / Mảnh ghép: thiết kế **Phiếu học tập số 2 (Luyện tập)** và **Rubric / Bảng kiểm đánh giá** (quan sát nhóm hoặc đánh giá đồng đẳng).
- Nếu tiến trình không nêu tên phiếu: vẫn tạo tối thiểu PHT số 1 (Khám phá), PHT số 2 (Luyện tập) và 1 Rubric/Bảng kiểm.
- Mỗi phiếu là MẪU IN SẴN: tiêu đề trường/lớp, nhóm/họ tên HS, bảng kẻ rõ, câu hỏi/nhiệm vụ, dòng kẻ điền kết quả. Không để dấu "..." hay "[...]". Điền nội dung bám SGK.
- Kèm **Hướng dẫn chấm / đáp án** cho từng phiếu (thang điểm 10 nếu là bài tập).
- CẤM viết lại tiến trình A–E. CẤM bịa bài tập ngoài nguồn SGK khi nguồn đã có bài.

CẤU TRÚC BẮT BUỘC:

# F. HỒ SƠ DẠY HỌC & PHIẾU HỌC TẬP (PHỤ LỤC)

## 1. PHIẾU HỌC TẬP SỐ 1 (Khám phá / Hình thành kiến thức)
**TRƯỜNG THCS: .......................................**  
**LỚP: .............. NHÓM: ..............................**  
**HỌ VÀ TÊN: .....................................................................................**  
**BÀI: {topic}**

| Nhiệm vụ | Nội dung câu hỏi / Bài tập | Chỗ HS điền kết quả |
| :--- | :--- | :--- |
| **Nhiệm vụ 1** | [Câu hỏi/bài tập cụ thể bám SGK] | ................................ |
| **Nhiệm vụ 2** | [Câu hỏi/bài tập cụ thể bám SGK] | ................................ |

*(Nhận xét của GV: ........................................................................................................)*

## 2. PHIẾU HỌC TẬP TRẠM (chỉ khi tiến trình có dạy học theo trạm — đủ Trạm 1, Trạm 2, Trạm 3)
[Mỗi trạm một phiếu in riêng, cùng khung tiêu đề trường/lớp/họ tên.]

## 3. PHIẾU HỌC TẬP SỐ 2 (Luyện tập)
[Khung tiêu đề + bảng nhiệm vụ luyện tập.]

## 4. CÔNG CỤ ĐÁNH GIÁ (Bảng kiểm / Rubric)
| Tiêu chí | Chưa đạt | Đạt | Tốt |
| :--- | :--- | :--- | :--- |
| Hoàn thành nhiệm vụ | | | |
| Trao đổi nhóm | | | |
| Chính xác kết quả | | | |

## 5. HƯỚNG DẪN CHẤM VÀ ĐÁP ÁN
### a) Đáp án Phiếu học tập số 1 (Thang điểm 10)
- Nhiệm vụ 1: [lời giải]
- Nhiệm vụ 2: [lời giải]
### b) Đáp án các phiếu còn lại
[lời giải chi tiết]`,

  // 1-CLICK HOẠT ĐỘNG A -> E (ACTIVITIES AE)
  GENERATE_ACTIVITIES_AE: `Đọc PDF/ảnh SGK đính kèm và soạn toàn bộ hoạt động A–E môn {subject} Cấp {gradeLevelName} chuẩn Công văn 5512.
- Môn học: {subject}
- Tên bài dạy: {topic}
- Thời lượng: {duration}
- Phạm vi tiết dạy theo PPCT (nếu có): {lesson_scope}
- Dữ liệu Phân phối chương trình (PPCT nếu có):
"""
{ppct_content}
"""
- Mục tiêu bài học:
"""
{objectives_content}
"""
- Dữ liệu SGK:
"""
{textbook_content}
"""

BẮT BUỘC xuất đúng 5 khối, mỗi khối bắt đầu bằng marker:
<<<KHBD_A>>>
(toàn bộ ## A. HOẠT ĐỘNG 1: MỞ ĐẦU ({time_budget_A}))
<<<KHBD_B>>>
(toàn bộ ## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI)
<<<KHBD_C>>>
(toàn bộ ## C. HOẠT ĐỘNG 3: LUYỆN TẬP ({time_budget_C}))
<<<KHBD_D>>>
(toàn bộ ## D. HOẠT ĐỘNG 4: VẬN DỤNG ({time_budget_D}))
<<<KHBD_E>>>
(toàn bộ ## E. HOẠT ĐỘNG 5: HƯỚNG DẪN VỀ NHÀ ({time_budget_E}))

YÊU CẦU HÌNH THỨC & KỊCH BẢN THỰC CHIẾN (Áp dụng mọi pha A–E):
${ACTIVITY_TABLE_CONTRACT}
- QUY TẮC THỜI LƯỢNG CỐ ĐỊNH: BẮT BUỘC đặt thời lượng cố định cụ thể bằng số phút trong tiêu đề từng hoạt động (A: {time_budget_A}, C: {time_budget_C}, D: {time_budget_D}, E: {time_budget_E}; từng hoạt động nhánh trong B: theo phân bổ tiểu mục). TUYỆT ĐỐI CẤM ghi từ "Khoảng" hoặc dải thời gian "X - Y phút".

PHA A — MỞ ĐẦU:
- Tiêu đề: \`## A. HOẠT ĐỘNG 1: MỞ ĐẦU ({time_budget_A})\`.
- Đủ a) Mục tiêu, b) Nội dung, c) Sản phẩm, d) Tổ chức thực hiện (1 bảng 2 cột duy nhất).
- Bám sát tình huống mở đầu trong SGK; không bịa tình huống ngoài nguồn.
- Khi có NLS/AI: Tích hợp công cụ số hoặc câu hỏi/prompt AI mở đầu ngắn gọn (marker **[NLS: ...]** hoặc **[AI: ...]**). CẤM hỏi lý thuyết AI suông.

PHA B — HÌNH THÀNH KIẾN THỨC:
- Đếm số mục kiến thức lớn trong SGK (chỉ 1-3 mục lớn, tối đa 4 mục): tạo đúng N hoạt động con (### 1. Hoạt động 2.1: [Tên mục 1] (... phút), ### 2. Hoạt động 2.2: [Tên mục 2] (... phút)... hoặc ### 1. Hoạt động 1: ..., ### 2. Hoạt động 2: ...).
- TUYỆT ĐỐI LOẠI BỎ việc tách câu hỏi nhỏ/bài tập con thành hoạt động riêng. Toàn bộ ví dụ, khám phá, thực hành con phải nằm trọn vẹn bên trong hoạt động của mục lớn tương ứng.
- Mỗi hoạt động con đủ #### a) b) c) d) + đúng 1 bảng 2 cột duy nhất.
- Cột Trái: Kịch bản phân vai GV (lời thoại trong "...", chỉ rõ lỗi sai điển hình) và HS (cá nhân -> nhóm -> báo cáo).
- Khi có NLS/AI: Tích hợp thực chiến theo 3 dạng (Kiểm chứng phản hồi AI có lỗi sai / Prompting gợi mở bước giải / Thao tác phần mềm GeoGebra/bảng tính/mô phỏng). CẤM hỏi lý thuyết AI suông, CẤM rải tag bừa bãi. Gắn marker **[AI: {Mã} - Kiểm chứng phản hồi AI]**, **[AI: {Mã} - Prompting gợi mở & Tự giải]**, **[NLS: {Miền/Mã} - {Tên phần mềm}]** (hoặc **[NLS: ...]**, **[AI: ...]**).
- Cột Phải: Nội dung ghi bảng chốt kiến thức, công thức LaTeX, ví dụ mẫu kèm đề và lời giải chi tiết. TUYỆT ĐỐI CẤM để dấu "...".

PHA C — LUYỆN TẬP:
- Tiêu đề: \`## C. HOẠT ĐỘNG 3: LUYỆN TẬP ({time_budget_C})\`.
- Giáo viên chọn lọc 1–2 bài tập luyện tập trọng tâm, cốt lõi trong SGK để chữa chi tiết tại lớp (các bài tập còn lại dành cho Hoạt động E). Chép rõ đề và giải chi tiết vào Cột Phải. Cột Trái phân vai rõ ràng.
- Khi có NLS/AI: Ứng dụng phần mềm chuyên dụng (GeoGebra, bảng tính) hoặc AI để gợi mở / kiểm tra đối chiếu lời giải, phản biện lỗi sai. CẤM hỏi lý thuyết AI suông.

PHA D — VẬN DỤNG:
- Tiêu đề: \`## D. HOẠT ĐỘNG 4: VẬN DỤNG ({time_budget_D})\`.
- Khóa nhiệm vụ vận dụng thực tế hoặc phiếu Exit Ticket thực hiện, thu hồi và chốt ngay tại lớp. Trình bày mô hình hóa và lời giải chuẩn. Cột Trái 4 bước.
- Khi có NLS/AI: Vận dụng công cụ số/AI chuyên ngành giải quyết bài toán thực tế, đánh giá và kiểm chứng tính khả thi. CẤM hỏi lý thuyết AI suông.

PHA E — HƯỚNG DẪN VỀ NHÀ:
- Tiêu đề: \`## E. HOẠT ĐỘNG 5: HƯỚNG DẪN VỀ NHÀ ({time_budget_E})\`.
- Đủ a) Mục tiêu, b) Nội dung (Bố cục 4 nội dung chuẩn mực: 1. Ôn nội dung trọng tâm, 2. Làm bài tập: hoàn thành các bài tập CÒN LẠI trong SGK chưa làm/chữa ở Pha C/D, bài tập SBT kèm gợi ý phương pháp - CẤM TUYỆT ĐỐI giao lại bài đã chữa ở C/D, 3. Chuẩn bị bài mới, 4. Nhiệm vụ tìm tòi/mở rộng nếu phù hợp; có thêm Mẫu Prompt AI an toàn hỗ trợ tự học CHỈ khi giáo viên chủ động bật AI), c) Sản phẩm, d) Tổ chức thực hiện (1 bảng 2 cột duy nhất, Cột Trái 4 bước giao nhiệm vụ ngắn gọn, Cột Phải đúng 4 mục nội dung).
- QUY TẮC NLS/AI: Tuyệt đối KHÔNG tự ý xuất hiện NLS hoặc AI trong Hoạt động E. Chỉ thêm khi giáo viên CHỦ ĐỘNG BẬT, và khi đó nhiệm vụ phải có giá trị học tập thực chất, rõ ràng, không thay thế việc tự học.
- LOẠI BỎ TRIỆT ĐỂ các yêu cầu hình thức (ghi âm, quay video, dùng AI tìm ví dụ suông...).

CẤM xuất HTML, span, style, mã màu. CẤM lời chào hỏi hay chúc mừng ở đầu/cuối bài.`,

  // ALIAS GENERATE_ACTIVITIES_AD -> GENERATE_ACTIVITIES_AE
  GENERATE_ACTIVITIES_AD: `Đọc PDF/ảnh SGK đính kèm và soạn toàn bộ hoạt động A–E môn {subject} Cấp {gradeLevelName} chuẩn Công văn 5512.
- Môn học: {subject}
- Tên bài dạy: {topic}
- Thời lượng: {duration}
- Phạm vi tiết dạy theo PPCT (nếu có): {lesson_scope}
- Dữ liệu Phân phối chương trình (PPCT nếu có):
"""
{ppct_content}
"""
- Mục tiêu bài học:
"""
{objectives_content}
"""
- Dữ liệu SGK:
"""
{textbook_content}
"""

BẮT BUỘC xuất đúng 5 khối, mỗi khối bắt đầu bằng marker:
<<<KHBD_A>>>
(toàn bộ ## A. HOẠT ĐỘNG 1: MỞ ĐẦU ({time_budget_A}))
<<<KHBD_B>>>
(toàn bộ ## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI)
<<<KHBD_C>>>
(toàn bộ ## C. HOẠT ĐỘNG 3: LUYỆN TẬP ({time_budget_C}))
<<<KHBD_D>>>
(toàn bộ ## D. HOẠT ĐỘNG 4: VẬN DỤNG ({time_budget_D}))
<<<KHBD_E>>>
(toàn bộ ## E. HOẠT ĐỘNG 5: HƯỚNG DẪN VỀ NHÀ ({time_budget_E}))

YÊU CẦU HÌNH THỨC & KỊCH BẢN THỰC CHIẾN (Áp dụng mọi pha A–E):
${ACTIVITY_TABLE_CONTRACT}
- QUY TẮC THỜI LƯỢNG CỐ ĐỊNH: BẮT BUỘC đặt thời lượng cố định cụ thể bằng số phút trong tiêu đề từng hoạt động (A: {time_budget_A}, C: {time_budget_C}, D: {time_budget_D}, E: {time_budget_E}; từng hoạt động nhánh trong B: theo phân bổ tiểu mục). TUYỆT ĐỐI CẤM ghi từ "Khoảng" hoặc dải thời gian "X - Y phút".

PHA A — MỞ ĐẦU:
- Tiêu đề: \`## A. HOẠT ĐỘNG 1: MỞ ĐẦU ({time_budget_A})\`.
- Đủ a) Mục tiêu, b) Nội dung, c) Sản phẩm, d) Tổ chức thực hiện (1 bảng 2 cột duy nhất).
- Bám sát tình huống mở đầu trong SGK; không bịa tình huống ngoài nguồn.
- Khi có NLS/AI: Tích hợp công cụ số hoặc câu hỏi/prompt AI mở đầu ngắn gọn (marker **[NLS: ...]** hoặc **[AI: ...]**). CẤM hỏi lý thuyết AI suông.

PHA B — HÌNH THÀNH KIẾN THỨC:
- Đếm số mục kiến thức lớn trong SGK (chỉ 1-3 mục lớn, tối đa 4 mục): tạo đúng N hoạt động con (### 1. Hoạt động 2.1: [Tên mục 1] (... phút), ### 2. Hoạt động 2.2: [Tên mục 2] (... phút)... hoặc ### 1. Hoạt động 1: ..., ### 2. Hoạt động 2: ...).
- TUYỆT ĐỐI LOẠI BỎ việc tách câu hỏi nhỏ/bài tập con thành hoạt động riêng. Toàn bộ ví dụ, khám phá, thực hành con phải nằm trọn vẹn bên trong hoạt động của mục lớn tương ứng.
- Mỗi hoạt động con đủ #### a) b) c) d) + đúng 1 bảng 2 cột duy nhất.
- Cột Trái: Kịch bản phân vai GV (lời thoại trong "...", chỉ rõ lỗi sai điển hình) và HS (cá nhân -> nhóm -> báo cáo).
- Khi có NLS/AI: Tích hợp thực chiến theo 3 dạng (Kiểm chứng phản hồi AI có lỗi sai / Prompting gợi mở bước giải / Thao tác phần mềm GeoGebra/bảng tính/mô phỏng). CẤM hỏi lý thuyết AI suông, CẤM rải tag bừa bãi. Gắn marker **[AI: {Mã} - Kiểm chứng phản hồi AI]**, **[AI: {Mã} - Prompting gợi mở & Tự giải]**, **[NLS: {Miền/Mã} - {Tên phần mềm}]** (hoặc **[NLS: ...]**, **[AI: ...]**).
- Cột Phải: Nội dung ghi bảng chốt kiến thức, công thức LaTeX, ví dụ mẫu kèm đề và lời giải chi tiết. TUYỆT ĐỐI CẤM để dấu "...".

PHA C — LUYỆN TẬP:
- Tiêu đề: \`## C. HOẠT ĐỘNG 3: LUYỆN TẬP ({time_budget_C})\`.
- Giáo viên chọn lọc 1–2 bài tập luyện tập trọng tâm, cốt lõi trong SGK để chữa chi tiết tại lớp (các bài tập còn lại dành cho Hoạt động E). Chép rõ đề và giải chi tiết vào Cột Phải. Cột Trái phân vai rõ ràng.
- Khi có NLS/AI: Ứng dụng phần mềm chuyên dụng (GeoGebra, bảng tính) hoặc AI để gợi mở / kiểm tra đối chiếu lời giải, phản biện lỗi sai. CẤM hỏi lý thuyết AI suông.

PHA D — VẬN DỤNG:
- Tiêu đề: \`## D. HOẠT ĐỘNG 4: VẬN DỤNG ({time_budget_D})\`.
- Khóa nhiệm vụ vận dụng thực tế hoặc phiếu Exit Ticket thực hiện, thu hồi và chốt ngay tại lớp. Trình bày mô hình hóa và lời giải chuẩn. Cột Trái 4 bước.
- Khi có NLS/AI: Vận dụng công cụ số/AI chuyên ngành giải quyết bài toán thực tế, đánh giá và kiểm chứng tính khả thi. CẤM hỏi lý thuyết AI suông.

PHA E — HƯỚNG DẪN VỀ NHÀ:
- Tiêu đề: \`## E. HOẠT ĐỘNG 5: HƯỚNG DẪN VỀ NHÀ ({time_budget_E})\`.
- Đủ a) Mục tiêu, b) Nội dung (Bố cục 4 nội dung chuẩn mực: 1. Ôn nội dung trọng tâm, 2. Làm bài tập: hoàn thành các bài tập CÒN LẠI trong SGK chưa làm/chữa ở Pha C/D, bài tập SBT kèm gợi ý phương pháp - CẤM TUYỆT ĐỐI giao lại bài đã chữa ở C/D, 3. Chuẩn bị bài mới, 4. Nhiệm vụ tìm tòi/mở rộng nếu phù hợp; có thêm Mẫu Prompt AI an toàn hỗ trợ tự học CHỈ khi giáo viên chủ động bật AI), c) Sản phẩm, d) Tổ chức thực hiện (1 bảng 2 cột duy nhất, Cột Trái 4 bước giao nhiệm vụ ngắn gọn, Cột Phải đúng 4 mục nội dung).
- QUY TẮC NLS/AI: Tuyệt đối KHÔNG tự ý xuất hiện NLS hoặc AI trong Hoạt động E. Chỉ thêm khi giáo viên CHỦ ĐỘNG BẬT, và khi đó nhiệm vụ phải có giá trị học tập thực chất, rõ ràng, không thay thế việc tự học.
- LOẠI BỎ TRIỆT ĐỂ các yêu cầu hình thức (ghi âm, quay video, dùng AI tìm ví dụ suông...).

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

## 1. Ôn tập nội dung trọng tâm
- Ôn tập và nắm vững các định nghĩa, quy tắc, công thức trọng tâm đã học trong bài: (liệt kê vắn tắt các nội dung cốt lõi).
- Tóm tắt và hệ thống hóa kiến thức bài học vào vở ghi.

## 2. Bài tập tự luyện tại nhà
- Hoàn thành các bài tập còn lại trong SGK (chưa làm/chữa ở Hoạt động C và D) và Sách bài tập môn {subject} (kèm gợi ý/hướng dẫn phương pháp giải ngắn gọn). CẤM TUYỆT ĐỐI giao lại các bài tập đã được giải/chữa trên lớp.

## 3. Nhiệm vụ chuẩn bị cho bài học tiếp theo
- Đọc trước bài mới trong SGK môn {subject}.
- Chuẩn bị đầy đủ dụng cụ học tập và tìm hiểu các ví dụ, hình ảnh liên quan đến bài học tiếp theo.

## 4. Nhiệm vụ tìm tòi, mở rộng (nếu phù hợp)
- Tìm hiểu ứng dụng thực tiễn hoặc thực hiện bài toán mở rộng tư duy gắn với bài học.

{ai_homework_prompt_note}`
};

function getSystemRole(subjectId, grade) {
  let subjectName = 'Toán';
  if (typeof CURRICULUM_DATA !== 'undefined' && Array.isArray(CURRICULUM_DATA.subjects)) {
    const found = CURRICULUM_DATA.subjects.find(s => s.id === subjectId || s.code === subjectId || String(s.name || '').toLowerCase() === String(subjectId || '').toLowerCase());
    if (found && found.name) subjectName = found.name;
  }
  if (!subjectName && typeof getSubjectDisplayName === 'function') {
    subjectName = getSubjectDisplayName(subjectId);
  }
  if (!subjectName) subjectName = 'Toán';
  
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
- Kế hoạch bài dạy hoàn chỉnh đạt dung lượng chuẩn 8–10 trang Word A4. Hành văn sư phạm cô đọng, súc tích, trực diện vào bản chất kiến thức và hành động cốt lõi của GV/HS; TUYỆT ĐỐI KHÔNG viết văn biền ngẫu, không dùng câu thoại diễn giải lòng vòng, không lặp lại nội dung giữa các mục.
- Thiết kế giáo án thành KỊCH BẢN SƯ PHẠM THỰC CHIẾN (GV có lời thoại trực tiếp trong ngoặc kép "...", hành động cụ thể, dự kiến lỗi sai điển hình; HS có thao tác cá nhân, nhóm và sản phẩm rõ ràng).
- NLS và AI là công cụ thực hành của môn học; TUYỆT ĐỐI KHÔNG dạy lý thuyết Tin học/AI hay hỏi lý thuyết AI suông trong giờ học chuyên môn. Tích hợp thực chiến đúng 1–2 vị trí then chốt (kiểm chứng lỗi sai AI, prompting gợi mở, thao tác phần mềm chuyên ngành).
- Định dạng Markdown rõ ràng, phân cấp tiêu đề bằng #, ##, ###, #### hợp lý.
${latexRule}
- Nội dung phải chi tiết, đầy đủ, thiết thực cho giáo viên lên lớp, TUYỆT ĐỐI KHÔNG viết tóm tắt qua loa, KHÔNG để dấu '...' hoặc '[...]' hoặc từ 'tương tự'.
- TUYỆT ĐỐI KHÔNG xuất lời chào, lời dẫn chuyện, lời chúc mừng hoặc nhận xét meta ngoài lề.
- Mục tiêu kiến thức phải bám YCCĐ CT GDPT 2018 / Thông tư 32/2018/TT-BGDĐT; không tự tạo kiến thức ngoài nguồn.`;
}

/**
 * Trích xuất danh sách các tiểu mục kiến thức lớn từ nội dung phân tích SGK (Tab 1/Bước 0).
 * @param {string} content - Nội dung phân tích SGK
 * @returns {Array<{index: number, title: string}>} Danh sách tiểu mục đã chuẩn hóa (tối đa 4 mục lớn)
 */
function extractTextbookSubsections(content) {
  if (!content || typeof content !== 'string') return [];
  const text = content.trim();
  if (!text) return [];

  const results = [];
  const seenTitles = new Set();

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
    if (!title || title.length < 3 || title.length > 100) return true;

    // 1. Loại trừ bài tập dạng số thập phân (1.1, 1.2, 1.4, 2.3...)
    if (/^\d+\.\d+/.test(title)) return true;

    // 2. Loại trừ nhãn bài tập / thực hành / ví dụ / ghi nhớ / chú ý...
    if (/^(?:Thực hành|Luyện tập|Vận dụng|Bài tập|Bài|Ví dụ|Câu hỏi|Thử thách|Trải nghiệm|Ghi nhớ|Chú ý|Nhận xét|Quy ước|Tranh luận|Em có biết)\b/i.test(title)) return true;

    // 3. Loại trừ câu lệnh / câu hỏi phát vấn (tránh bắt nhầm "Tính chất...", "Giải bài toán...")
    if (/^(?:Hãy|Nêu|Bằng cách|Cho\b|Tìm\b|Tính\s+(?!chất\b)|Chứng minh|Chỉ ra|Viết\b|Điền\b|Quan sát|Đọc\b|Xác định|Giải\s+(?!bài toán\b|tam giác\b)|Vẽ\b|Chọn\b|Thực hiện|Trả lời|Xét\b|Dựa vào|Kể\b|Phát biểu|Kiểm tra)\b/i.test(title)) return true;

    // 4. Loại trừ tiêu đề khung giáo án / cấu trúc tài liệu
    if (/^(?:Tổng quan|Khung kiến thức|Chuỗi hoạt động|Hệ thống bài tập|Đề xuất|Yêu cầu cần đạt|Tiến trình|Thiết bị|Hoạt động mở đầu|Hoạt động hình thành|Hoạt động luyện tập|Hoạt động vận dụng|Đánh giá|Hồ sơ|Hướng dẫn về nhà)\b/i.test(title)) return true;

    // 5. Loại trừ các từ đơn lẻ generic
    if (/^(?:định nghĩa|khái niệm|quy tắc|công thức|chú ý|ví dụ|bài tập|nhiệm vụ|bước\s*\d+|phương pháp|kỹ thuật)$/i.test(title)) return true;

    return false;
  }

  function addSub(idx, title) {
    const cleaned = cleanTitle(title);
    if (!cleaned || isIgnored(cleaned)) return;
    const key = cleaned.toLowerCase();
    if (seenTitles.has(key)) return;
    seenTitles.add(key);
    results.push({ index: idx, title: cleaned });
  }

  // Chiến lược 1: Ưu tiên nhận diện theo Chữ số La Mã (I., II., III., IV. hoặc # I., ## I., ### I., - I.)
  const romanRegex = /(?:^|\n)\s*(?:[-*+•]\s+)?(?:#{1,6}\s+)?(?:\*\*)?([IVXLCDM]+)[\s.:\-]+(?:\*\*)?\s*([A-ZÀ-Ỹ0-9][^\r\n]+)/g;
  let match;
  while ((match = romanRegex.exec(text)) !== null) {
    const romanStr = match[1].toUpperCase();
    const title = match[2];
    if (/^(?:I|II|III|IV|V|VI|VII|VIII|IX|X)$/.test(romanStr)) {
      addSub(results.length + 1, title);
    }
  }

  if (results.length > 0) {
    let finalRes = results.map((item, i) => ({ index: i + 1, title: item.title }));
    if (finalRes.length > 4) finalRes = finalRes.slice(0, 4);
    return finalRes;
  }

  // Chiến lược 2: Tìm các mẫu rõ ràng "Mục 1:", "Mục 2:", "Phần 1:", "Phần 2:"
  const mucRegex = /(?:^|\n)\s*(?:[-*+•]\s+)?(?:#{1,6}\s+)?(?:\*\*)?(?:Mục|Phần)\s*(\d+)[\s.:\-]+([^\r\n]+)/gi;
  while ((match = mucRegex.exec(text)) !== null) {
    const num = parseInt(match[1], 10);
    const title = match[2];
    addSub(num, title);
  }

  if (results.length > 0) {
    let finalRes = results.map((item, i) => ({ index: i + 1, title: item.title }));
    if (finalRes.length > 4) finalRes = finalRes.slice(0, 4);
    return finalRes;
  }

  // Chiến lược 3: Tìm theo "HĐ khám phá 1:", "Hoạt động khám phá 1:", "Khám phá 1:"
  const hdRegex = /(?:^|\n)\s*(?:[-*+•]\s+)?(?:#{1,6}\s+)?(?:\*\*)?(?:Hoạt động khám phá|HĐ khám phá|Khám phá)\s*(\d+)[\s.:\-]+([^\r\n]+)/gi;
  while ((match = hdRegex.exec(text)) !== null) {
    const num = parseInt(match[1], 10);
    const title = match[2];
    addSub(num, title);
  }

  if (results.length > 0) {
    let finalRes = results.map((item, i) => ({ index: i + 1, title: item.title }));
    if (finalRes.length > 4) finalRes = finalRes.slice(0, 4);
    return finalRes;
  }

  // Chiến lược 4: Tìm trong phạm vi mục 2 "Khung kiến thức trọng tâm" hoặc toàn văn theo số lớn 1. 2. 3. 4.
  let searchBlock = text;
  const section2Match = text.match(/2\.\s*(?:\*\*)?Khung kiến thức trọng tâm[\s\S]*?(?=(?:\n\s*(?:#{1,3}\s*)?3\.\s*(?:\*\*)?Chuỗi hoạt động|\n\s*(?:#{1,2}\s*)?[3-9]\.|$))/i);
  if (section2Match) {
    searchBlock = section2Match[0];
  }

  const numRegex = /(?:^|\n)\s*(?:[-*+•]\s+)?(?:#{1,6}\s+)?(?:\*\*)?(\d+)[\s.)\-]+(?:\*\*)?\s*([A-ZÀ-Ỹ0-9][^\r\n]+)/g;
  while ((match = numRegex.exec(searchBlock)) !== null) {
    const num = parseInt(match[1], 10);
    const title = match[2];
    addSub(num, title);
  }

  if (results.length > 0) {
    let finalRes = results.map((item, i) => ({ index: i + 1, title: item.title }));
    if (finalRes.length > 4) finalRes = finalRes.slice(0, 4);
    return finalRes;
  }

  return [];
}

function extractTextbookBlock(content, startPattern, endPattern) {
  const text = String(content || "");
  const start = text.search(startPattern);
  if (start < 0) return "";
  let block = text.slice(start);
  const rest = block.slice(12);
  const end = rest.search(endPattern);
  if (end >= 0) block = block.slice(0, end + 12);
  return block.replace(/\s+/g, " ").trim().slice(0, 2500);
}

function extractTextbookLessonMap(content) {
  const subsections = extractTextbookSubsections(content);
  const practice = extractTextbookBlock(
    content,
    /(?:^|\n)\s*(?:#{1,6}\s+)?(?:\*\*)?(?:Luyện tập|Bài tập)\b/i,
    /(?:^|\n)\s*(?:#{1,6}\s+)?(?:\*\*)?(?:Vận dụng|Bài toán thực tế|Hướng dẫn về nhà|Em có biết|Bạn có biết)\b/i
  );
  const application = extractTextbookBlock(
    content,
    /(?:^|\n)\s*(?:#{1,6}\s+)?(?:\*\*)?(?:Vận dụng|Bài toán thực tế)\b/i,
    /(?:^|\n)\s*(?:#{1,6}\s+)?(?:\*\*)?(?:Hướng dẫn về nhà|Em có biết|Bạn có biết|Tổng kết)\b/i
  );
  const opening = extractTextbookBlock(
    content,
    /(?:^|\n)\s*(?:#{1,6}\s+)?(?:\*\*)?(?:Mở đầu|Khởi động|Khám phá|Tình huống)\b/i,
    /(?:^|\n)\s*(?:#{1,6}\s+)?(?:\*\*)?(?:I[\.\s]|Mục\s*1|Luyện tập|Vận dụng)\b/i
  );
  return { subsections, practice, application, opening };
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
    ? `### c) Năng lực số\n- [Mã NLS đã chọn, ví dụ 1.1.TC1a]: [Mô tả nhiệm vụ số gắn với bài]`
    : '';
  const aiObjectivesSection = context.aiCompetencyEnabled
    ? `### d) Năng lực AI\n- [Mã AI đã chọn]: [Mô tả nhiệm vụ AI gắn với bài]`
    : '';
  
  const rawTextbook = context.textbook_content || '';
  const subsections = extractTextbookSubsections(rawTextbook);
  const budgets = calculateActivityTimeBudgets(context.duration, subsections.length, context.grade);
  const aiHomeworkPromptNote = context.aiCompetencyEnabled
    ? `- Hướng dẫn Prompt AI an toàn (khi giáo viên chủ động bật AI): Mẫu Prompt AI an toàn mẫu mực hỗ trợ học sinh tự học tại nhà (nhắc AI đóng vai gia sư gợi mở tư duy khi gặp khó khăn, TUYỆT ĐỐI không giải bài hộ, không thay thế việc tự học):\n  + Mẫu Prompt: "Em là học sinh lớp ${context.grade || '6'}, em đang tự học bài ${context.topic || ''} và gặp khó khăn ở [nêu bài tập/khái niệm]. Bạn hãy đóng vai gia sư gợi mở, đặt cho em 2 câu hỏi định hướng để em tự tìm ra cách giải, đừng giải hộ em nhé!"`
    : '';

  // Replace placeholders an toàn
  let result = baseTemplate
    .replace(/\{subject\}/g, subjectName)
    .replace(/\{gradeLevelName\}/g, gradeLevelName)
    .replace(/\{topic\}/g, context.topic || '')
    .replace(/\{duration\}/g, context.duration || '02 tiết (90 phút)')
    .replace(/\{lesson_scope\}/g, context.lesson_scope || '')
    .replace(/\{ppct_content\}/g, context.ppct_content || '')
    .replace(/\{textbook_content\}/g, context.textbook_content || '')
    .replace(/\{objectives_content\}/g, context.objectives_content || '')
    .replace(/\{activities_content\}/g, context.activities_content || '')
    .replace(/\{yccd_official\}/g, context.yccd_official || '')
    .replace(/\{grade\}/g, context.grade || '6')
    .replace(/\{competencies\}/g, competencies)
    .replace(/\{digital_objectives_section\}/g, digitalObjectivesSection)
    .replace(/\{ai_objectives_section\}/g, aiObjectivesSection)
    .replace(/\{general_competencies_guide\}/g, genCompsGuide)
    .replace(/\{time_budget_A\}/g, budgets.formatted.A)
    .replace(/\{time_budget_B\}/g, budgets.formatted.B)
    .replace(/\{time_budget_C\}/g, budgets.formatted.C)
    .replace(/\{time_budget_D\}/g, budgets.formatted.D)
    .replace(/\{time_budget_E\}/g, budgets.formatted.E)
    .replace(/\{ai_homework_prompt_note\}/g, aiHomeworkPromptNote)
    .replace(/\{drawing_prompt\}/g, context.drawing_prompt || '')
    .replace(/\{drawing_title\}/g, context.drawing_title || '');

  if (templateKey === 'GENERATE_SVG_DRAWING' || templateKey === 'ANALYZE_PPCT') {
    return result;
  }

  if (context.lesson_scope || context.ppct_content) {
    const scopeText = context.lesson_scope ? `\n- PHẠM VI TIẾT DẠY THEO PPCT: ${context.lesson_scope}` : '';
    const ppctText = context.ppct_content ? `\n- NỘI DUNG PPCT (PHỤ LỤC 3 CV 5512):\n"""\n${context.ppct_content}\n"""` : '';
    result += `\n\nĐỊNH HƯỚNG PHÂN PHỐI CHƯƠNG TRÌNH & PHẠM VI TIẾT HỌC:${scopeText}${ppctText}\nBẮT BUỘC: Bạn phải căn chỉnh tiến trình hoạt động, mục tiêu và lượng bài tập hoàn toàn khớp với phạm vi tiết dạy / phân phối chương trình ở trên, không soạn tràn sang nội dung của các tiết học khác.`;
  }

  if (PROMPTS.SOURCE_LOCK) {
    result += `\n\n${PROMPTS.SOURCE_LOCK}`;
  }
  if ([
    "GENERATE_OBJECTIVES",
    "GENERATE_MATERIALS",
    "GENERATE_ACTIVITY_A",
    "GENERATE_ACTIVITY_B",
    "GENERATE_ACTIVITY_C",
    "GENERATE_ACTIVITY_D",
    "GENERATE_PORTFOLIO_WORKSHEETS"
  ].includes(templateKey) && PROMPTS.NATURAL_INTEGRATION_GATE) {
    result += `\n\n${PROMPTS.NATURAL_INTEGRATION_GATE}`;
  }
  if ([
    "GENERATE_OBJECTIVES",
    "GENERATE_MATERIALS",
    "GENERATE_ACTIVITY_A",
    "GENERATE_ACTIVITY_B",
    "GENERATE_ACTIVITY_C",
    "GENERATE_ACTIVITY_D",
    "GENERATE_PORTFOLIO_WORKSHEETS"
  ].includes(templateKey) && PROMPTS.CLIL_INCLUSIVE_GATE) {
    result += `\n\n${PROMPTS.CLIL_INCLUSIVE_GATE}`;
  }
  result += `\n\nGIỚI HẠN DUNG LƯỢNG: Viết cô đọng để giáo án in Word khoảng 8–12 trang (Times New Roman 13pt). Không viết lại lý thuyết đã có ở mục trước.`;

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

  if (templateKey === 'GENERATE_ACTIVITY_B' || templateKey === 'GENERATE_ACTIVITIES_AD' || templateKey === 'GENERATE_ACTIVITIES_AE') {
    if (subsections && subsections.length > 0) {
      const subListStr = subsections.map((s, idx) => {
        const subTime = budgets.formatted.B_subsections[idx] || '15 phút';
        return `+ Tiểu mục ${s.index}: "${s.title}" -> BẮT BUỘC sinh: ### ${s.index}. Hoạt động 2.${s.index}: ${s.title} (${subTime})`;
      }).join('\n');
      result += `\n\nDANH SÁCH TIỂU MỤC SGK BẮT BUỘC ÁP DỤNG (ĐÚNG ${subsections.length} HOẠT ĐỘNG NHÁNH):
Từ dữ liệu SGK được cung cấp, xác định chính xác ${subsections.length} tiểu mục kiến thức lớn sau. Bạn PHẢI tạo đúng ${subsections.length} hoạt động nhánh tương ứng 1-1, KHÔNG ĐƯỢC GỘP, KHÔNG ĐƯỢC BỎ BỚT, KHÔNG ĐƯỢC BỊA THÊM:
${subListStr}
Mỗi hoạt động 2.k (hoặc Hoạt động k) trên BẮT BUỘC phải có thời lượng cố định cụ thể ví dụ (${budgets.formatted.B_subsections[0] || '15 phút'}), đầy đủ 4 phần: #### a) Mục tiêu:, #### b) Nội dung:, #### c) Sản phẩm:, #### d) Tổ chức thực hiện: (với đúng 1 bảng Markdown 2 cột, 4 bước phân vai GV-HS và nội dung ghi bảng). Tuyệt đối không tách câu hỏi nhỏ/bài tập con thành hoạt động riêng.`;
    }
  }

  const lessonMap = extractTextbookLessonMap(rawTextbook);

  if (templateKey === 'GENERATE_ILLUSTRATIONS') {
    if (lessonMap.subsections.length) {
      const names = lessonMap.subsections.map(s => `"${s.title}"`).join("; ");
      result += `\n\nTÊN TIỂU MỤC KIẾN THỨC SGK (dùng đúng vào trường subsection khi hình thuộc hoạt động B): ${names}`;
    }
    const realHay = `${lessonMap.application || ""} ${rawTextbook}`;
    const hasRealProblem = /bài toán thực tế|tình huống thực tế|đời sống|hàng rào|thửa đất|bể nước|đo chiều cao|đo khoảng cách|cửa hàng|siêu thị|chợ|mua bán|giá tiền/i.test(realHay);
    if (hasRealProblem) {
      result += `\n\nBài CÓ tình huống đời sống cụ thể. Cho phép tối đa 1 hình kind=thuc_te, phải vẽ đúng đồ vật/bối cảnh của đề. CẤM cảnh lớp học.`;
    } else {
      result += `\n\nBài KHÔNG có bài toán thực tế cần minh họa đời sống. CẤM kind=thuc_te. CHỈ vẽ kind=sgk nếu bài có hình học/đồ thị/trục số.`;
    }
  }

  if (templateKey === 'GENERATE_ACTIVITY_A' && lessonMap.opening) {
    result += `\n\nTÌNH HUỐNG MỞ ĐẦU TRONG SGK (bắt buộc ánh xạ, không bịa tình huống ngoài sách):\n"""\n${lessonMap.opening}\n"""`;
  }

  if (templateKey === 'GENERATE_ACTIVITY_C' || templateKey === 'GENERATE_ACTIVITY_D') {
    if (context.textbook_content && String(context.textbook_content).trim().length > 0) {
      result += `\n\nLƯU Ý QUAN TRỌNG VỀ NGUỒN BÀI TẬP: Vì dữ liệu SGK đã được cung cấp ở trên, CẤM ghi "[Không có trong tài liệu đã cung cấp]". BẮT BUỘC phải trích xuất và giải chi tiết các bài tập có trong nguồn.`;
    }
    if (templateKey === 'GENERATE_ACTIVITY_C' && lessonMap.practice) {
      result += `\n\nMỤC LUYỆN TẬP / BÀI TẬP TRONG SGK (chọn 1-2 bài tập trọng tâm để chữa trên lớp, các bài còn lại dành cho Hoạt động E - Hướng dẫn về nhà):\n"""\n${lessonMap.practice}\n"""`;
    }
    if (templateKey === 'GENERATE_ACTIVITY_D' && lessonMap.application) {
      result += `\n\nMỤC VẬN DỤNG / BÀI TOÁN THỰC TẾ TRONG SGK (thực hiện và chốt ngay tại lớp, không kéo dài sang bài tập về nhà):\n"""\n${lessonMap.application}\n"""`;
    }
  }

  if (templateKey === 'GENERATE_ACTIVITIES_AD' || templateKey === 'GENERATE_ACTIVITIES_AE') {
    if (lessonMap.practice) {
      result += `\n\nMỤC LUYỆN TẬP / BÀI TẬP TRONG SGK cho pha C (chọn 1-2 bài tập trọng tâm để chữa trên lớp, các bài còn lại dành cho pha E):\n"""\n${lessonMap.practice}\n"""`;
    }
    if (lessonMap.application) {
      result += `\n\nMỤC VẬN DỤNG / BÀI TOÁN THỰC TẾ TRONG SGK cho pha D (thực hiện và chốt ngay tại lớp):\n"""\n${lessonMap.application}\n"""`;
    }
  }

  return result;
}

if (typeof window !== 'undefined') {
  window.getSystemRole = getSystemRole;
  window.getPromptTemplate = getPromptTemplate;
  window.calculateActivityTimeBudgets = calculateActivityTimeBudgets;
  window.extractTextbookSubsections = extractTextbookSubsections;
  window.extractTextbookLessonMap = extractTextbookLessonMap;
  window.getGeneralCompetenciesForSubject = getGeneralCompetenciesForSubject;
  window.formatGeneralCompetenciesGuide = formatGeneralCompetenciesGuide;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { PROMPTS, calculateActivityTimeBudgets, getSystemRole, getPromptTemplate, extractTextbookSubsections, extractTextbookLessonMap, getGeneralCompetenciesForSubject, formatGeneralCompetenciesGuide };
}
