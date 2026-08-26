/* Catalog chỉ gồm mục đã đối chiếu văn bản gốc. NLS: 6 miền TT 02/2025, không bịa mã thành phần. AI: 4 mã đã rà QĐ 2422. */
const KHBD_STANDARDS = {
  digital: {
    framework: "Thông tư 02/2025/TT-BGDĐT", date: "24/01/2025", source: "02-bgddt.pdf; hướng dẫn 23456bgddthuong-dan-trien-khai-thuc-hien_219202522.pdf",
    minSelect: 2, maxSelect: 3,
    entries: [
      "Khai thác dữ liệu và thông tin", "Giao tiếp và hợp tác trong môi trường số", "Sáng tạo nội dung số", "An toàn", "Giải quyết vấn đề", "Ứng dụng trí tuệ nhân tạo"
    ].map((label, index) => ({ id: `tt02-domain-${index + 1}`, label, kind: "Miền năng lực số", grades: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] }))
  },
  ai: {
    framework: "Khung nội dung giáo dục trí tuệ nhân tạo cho học sinh phổ thông", date: "18/08/2026", source: "Quyết định 2422/QĐ-BGDĐT, 260818-QD2422-KhungAI.pdf",
    minSelect: 2, maxSelect: 3,
    entries: [
      { id: "qd2422-6-a13", code: "6.A1.3", grades: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], label: "Thực hiện được việc kiểm tra lại một kết quả do AI đưa ra trước khi sử dụng, thể hiện thói quen con người quyết định cuối cùng." },
      { id: "qd2422-7-a12", code: "7.A1.2", grades: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], label: "Nêu được ví dụ hậu quả có thể xảy ra khi không có sự xác thực của con người về độ chính xác của kết quả do AI đưa ra." },
      { id: "qd2422-8-a12", code: "8.A1.2", grades: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], label: "Nêu được những rủi ro của việc lạm dụng các công cụ AI tạo sinh và sự cần thiết của việc kiểm chứng nguồn thông tin khi sử dụng AI tạo sinh trong học tập." },
      { id: "qd2422-9-b21", code: "9.B2.1", grades: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], label: "Trình bày được vai trò của người dùng trong việc kiểm soát và chịu trách nhiệm đối với kết quả cuối cùng do AI tạo ra; khai báo được việc sử dụng AI trong sản phẩm học tập." }
    ]
  }
};

function foldStandardText(value) {
  return String(value || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, " ").replace(/[^a-z0-9]+/g, " ").trim();
}

function standardToRecord(kind, entry, grade, autoSuggested) {
  const catalog = KHBD_STANDARDS[kind];
  return {
    framework: catalog.framework,
    source: catalog.source,
    date: catalog.date,
    catalogId: entry.id,
    officialCode: entry.code || null,
    officialLabel: entry.label,
    grade: Number(grade),
    level: kind === "digital" ? (Number(grade) <= 7 ? 3 : 4) : null,
    loci: ["Mục tiêu", "Hoạt động", "Sản phẩm"],
    autoSuggested: Boolean(autoSuggested)
  };
}

function scoreOfficialStandard(kind, entry, ctx) {
  const hay = foldStandardText([ctx.topic, ctx.vision, ctx.subjectName, ...(ctx.methods || []), ...(ctx.activities || []), ctx.specialRequirements].join(" "));
  const facilities = ctx.facilities || {};
  const hasTech = Boolean(facilities.internet || facilities.devices);
  const grouping = foldStandardText(ctx.grouping || "");
  let score = 1;
  if (kind === "digital") {
    if (entry.id === "tt02-domain-1") {
      if (/so lieu|thong ke|bieu do|bang bieu|du lieu|thong tin|thu thap|do dac/.test(hay)) score += 5;
      score += 2;
    } else if (entry.id === "tt02-domain-2") {
      if (!hasTech) score -= 4;
      if (/nhom|hop tac|chia se|thao luan|padlet|trinh bay/.test(hay) || /nhom/.test(grouping)) score += 4;
    } else if (entry.id === "tt02-domain-3") {
      if (!hasTech && !facilities.projector) score -= 3;
      if (/san pham|poster|video|thuyet trinh|thiet ke|sang tao|canva/.test(hay)) score += 4;
    } else if (entry.id === "tt02-domain-4") {
      if (hasTech || ctx.aiOn) score += 4;
      if (/an toan|rieng tu|mang|chia se|thong tin ca nhan/.test(hay)) score += 3;
      score += 1;
    } else if (entry.id === "tt02-domain-5") {
      if (/van de|du an|thuc tien|giai quyet|van dung/.test(hay)) score += 4;
      score += 2;
    } else if (entry.id === "tt02-domain-6") {
      if (ctx.aiOn) score += 5;
      if (!hasTech && !ctx.aiOn) score -= 3;
      if (/\bai\b|chatbot|gemini|tri tue nhan tao/.test(hay)) score += 4;
    }
  } else if (kind === "ai") {
    if (entry.id === "qd2422-6-a13") score += 4;
    if (entry.id === "qd2422-8-a12" && (ctx.aiOn || /tao sinh|chatbot|tra cuu|kiem chung/.test(hay))) score += 4;
    if (entry.id === "qd2422-9-b21" && (/san pham|thuyet trinh|bao cao|khai bao/.test(hay) || ctx.subjectId === "nguvan")) score += 3;
    if (entry.id === "qd2422-7-a12") score += 2;
    if (!hasTech) score -= 1;
  }
  return score;
}

function recommendOfficialStandards(kind, ctx) {
  const catalog = KHBD_STANDARDS[kind];
  if (!catalog) return [];
  const grade = Number(ctx.grade) || 6;
  const min = catalog.minSelect || 2;
  const max = catalog.maxSelect || 3;
  const ranked = catalog.entries
    .filter(entry => !entry.grades || entry.grades.includes(grade))
    .map(entry => ({ entry, score: scoreOfficialStandard(kind, entry, ctx) }))
    .filter(row => row.score > 0)
    .sort((a, b) => b.score - a.score);
  const picked = ranked.slice(0, Math.min(max, Math.max(min, ranked.length)));
  if (picked.length < min) {
    catalog.entries.filter(entry => !picked.some(row => row.entry.id === entry.id) && (!entry.grades || entry.grades.includes(grade)))
      .slice(0, min - picked.length)
      .forEach(entry => picked.push({ entry, score: 0 }));
  }
  return picked.slice(0, max).map(row => standardToRecord(kind, row.entry, grade, true));
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = { KHBD_STANDARDS, recommendOfficialStandards, standardToRecord };
}
