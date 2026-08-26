const KHBD_PEDAGOGY_CATALOG = {
  methods: [
    { id: "pbl", label: "Dạy học theo dự án (PBL)", description: "HS giải quyết vấn đề thực tế qua dự án" },
    { id: "steam", label: "STEM/STEAM", description: "Tích hợp Khoa học-Công nghệ-Kỹ thuật-Nghệ thuật-Toán", recommendFor: { subjects: ["toan", "khtn", "vatly", "hoahoc", "sinhhoc", "khoahoc", "tnxh", "congnghe"] } },
    { id: "flipped", label: "Lớp học đảo ngược", description: "Học lý thuyết ở nhà, thực hành trên lớp", recommendFor: { needsFacilities: ["internet", "devices"] } },
    { id: "cooperative", label: "Dạy học hợp tác", description: "HS làm việc nhóm có cấu trúc" },
    { id: "game", label: "Học qua trò chơi", description: "Gamification: điểm thưởng, bảng xếp hạng, thử thách" },
    { id: "differentiation", label: "Dạy học phân hóa", description: "Điều chỉnh nội dung theo năng lực HS" },
    { id: "socratic", label: "Kỹ thuật Socratic", description: "Câu hỏi dẫn dắt tư duy phản biện" },
    { id: "mindmap", label: "Bản đồ tư duy", description: "Sơ đồ hóa kiến thức dạng cây" },
    { id: "experiential", label: "Học tập trải nghiệm", description: "Học qua hoạt động thực hành, vận động" },
    { id: "5w1h", label: "Kỹ thuật 5W1H", description: "What, Why, When, Where, Who, How" },
    { id: "tps", label: "Think-Pair-Share", description: "Suy nghĩ cá nhân → Thảo luận cặp → Chia sẻ lớp" },
    { id: "jigsaw", label: "Jigsaw (Mảnh ghép)", description: "Chia nhóm chuyên gia → ghép lại → dạy nhau" },
    { id: "gallery", label: "Gallery Walk", description: "Trình bày sản phẩm → đi tham quan → góp ý" },
    { id: "kwl", label: "KWL", description: "Biết gì (K) → Muốn biết (W) → Đã học (L)" },
    { id: "5e", label: "Mô hình 5E", description: "Engage-Explore-Explain-Elaborate-Evaluate", recommendFor: { subjects: ["khtn", "vatly", "hoahoc", "sinhhoc", "khoahoc"] } }
  ],
  techniques: [
    { id: "brainstorm", label: "Brainstorming/Động não", phases: ["A"], description: "Nêu ý tưởng nhanh để khởi động bài học" },
    { id: "kwl-tech", label: "KWL", phases: ["A"], description: "Biết gì → Muốn biết → Đã học" },
    { id: "stim-question", label: "Câu hỏi kích thích tư duy", phases: ["A"], description: "Câu hỏi gợi mở, tạo mâu thuẫn nhận thức" },
    { id: "wordgame", label: "Trò chơi ô chữ/đố vui", phases: ["A"], description: "Khởi động bằng trò chơi ngôn ngữ" },
    { id: "tps-tech", label: "Think-Pair-Share", phases: ["B"], description: "Suy nghĩ cá nhân → thảo luận cặp → chia sẻ lớp" },
    { id: "jigsaw-tech", label: "Jigsaw/Mảnh ghép", phases: ["B"], description: "Nhóm chuyên gia rồi ghép lại, dạy nhau" },
    { id: "gallery-tech", label: "Gallery Walk", phases: ["B"], description: "Trưng bày sản phẩm, đi tham quan, góp ý" },
    { id: "station", label: "Trạm học tập/Station Rotation", phases: ["B"], description: "Luân phiên nhiệm vụ theo trạm", recommendFor: { maxClassSize: 45 } },
    { id: "mindmap-tech", label: "Sơ đồ tư duy", phases: ["B"], description: "Tổ chức kiến thức dạng cây" },
    { id: "tablecloth", label: "Khăn trải bàn", phases: ["B"], description: "Ý kiến cá nhân rồi thống nhất nhóm" },
    { id: "diff-ex", label: "Bài tập phân hóa 3 mức", phases: ["C"], description: "Nhiệm vụ theo mức sẵn sàng" },
    { id: "peer", label: "Đánh giá đồng đẳng/Peer Assessment", phases: ["C"], description: "Phản hồi theo tiêu chí" },
    { id: "debate", label: "Tranh luận có cấu trúc", phases: ["C"], description: "Lập luận có bằng chứng", recommendFor: { subjects: ["nguvan", "tiengviet", "tienganh", "gdcd", "daoduc", "gdktpl", "lichsu", "lichsudialy"] } },
    { id: "case", label: "Case Study", phases: ["C"], description: "Phân tích tình huống" },
    { id: "roleplay", label: "Role-play/Đóng vai", phases: ["C"], description: "Thực hành vai trò", recommendFor: { subjects: ["nguvan", "tiengviet", "tienganh", "gdcd", "daoduc", "gdktpl", "lichsu", "lichsudialy"] } },
    { id: "mini-project", label: "Dự án mini", phases: ["D"], description: "Sản phẩm ngắn vận dụng kiến thức" },
    { id: "journal", label: "Viết nhật ký học tập", phases: ["D"], description: "Tự phản ánh điều đã học" },
    { id: "exit", label: "Exit Ticket", phases: ["D"], description: "Ghi nhận nhanh mức độ đạt" },
    { id: "open-ex", label: "Bài tập mở", phases: ["D"], description: "Nhiều cách tiếp cận, vận dụng linh hoạt" }
  ],
  activities: [
    { id: "discuss", label: "Thảo luận nhóm chuyên đề", description: "Nhóm hoàn thành nhiệm vụ theo chủ đề" },
    { id: "experiment", label: "Thực hành/thí nghiệm trực tiếp", description: "Học qua thao tác, đo đạc, thí nghiệm", recommendFor: { subjects: ["toan", "khtn", "vatly", "hoahoc", "sinhhoc", "khoahoc", "tnxh", "congnghe"] } },
    { id: "situation", label: "Phân tích tình huống thực tế", description: "Gắn kiến thức với ngữ cảnh đời sống" },
    { id: "starter-game", label: "Trò chơi học tập khởi động", description: "Khởi động bằng trò chơi có luật" },
    { id: "skill-group", label: "Tập luyện kỹ năng theo nhóm", description: "Rèn kỹ năng đặc thù theo nhóm" },
    { id: "contest", label: "Thi đấu/thi thử giữa các nhóm", description: "Cạnh tranh lành mạnh để củng cố" },
    { id: "media", label: "Phân tích qua video/hình ảnh minh họa", description: "Khai thác học liệu trực quan" },
    { id: "peer-coach", label: "Sửa lỗi theo cặp (Peer Coaching)", description: "Bạn hỗ trợ bạn theo tiêu chí" },
    { id: "station-act", label: "Trạm học tập xoay vòng (Station Rotation)", description: "Luân phiên trạm nhiệm vụ", recommendFor: { maxClassSize: 45 } },
    { id: "product", label: "Sáng tạo sản phẩm/dự án mini", description: "Tạo sản phẩm vận dụng kiến thức" },
    { id: "present", label: "Trình bày/thuyết trình trước lớp", description: "Công bố và bảo vệ sản phẩm" },
    { id: "digital-practice", label: "Thực hành ứng dụng công nghệ số", description: "Dùng công cụ số phù hợp môn học", recommendFor: { needsFacilities: ["internet", "devices"] } }
  ]
};

KHBD_PEDAGOGY_CATALOG.mathActivities = KHBD_PEDAGOGY_CATALOG.activities;
KHBD_PEDAGOGY_CATALOG.genericActivities = KHBD_PEDAGOGY_CATALOG.activities;

function isPedagogyRecommended(item, ctx = {}) {
  if (!item || !item.recommendFor) return false;
  const rec = item.recommendFor;
  const subjectId = String(ctx.subjectId || "").toLowerCase();
  if (Array.isArray(rec.subjects) && rec.subjects.length) {
    if (!rec.subjects.includes(subjectId)) return false;
  }
  if (Array.isArray(rec.grades) && rec.grades.length === 2) {
    const grade = Number(ctx.grade);
    if (!(grade >= rec.grades[0] && grade <= rec.grades[1])) return false;
  }
  if (Array.isArray(rec.needsFacilities) && rec.needsFacilities.length) {
    const facilities = ctx.facilities && typeof ctx.facilities === "object" ? ctx.facilities : {};
    if (!rec.needsFacilities.some(key => Boolean(facilities[key]))) return false;
  }
  if (typeof rec.maxClassSize === "number" && Number(ctx.classSize) > rec.maxClassSize) return false;
  return true;
}

function foldPedagogyText(value) {
  return String(value || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^a-z0-9]+/g, " ").trim();
}

function scorePedagogyItem(item, ctx) {
  const hay = foldPedagogyText([ctx.vision, ctx.topic, ctx.subjectName].join(" "));
  const recCtx = { subjectId: ctx.subjectId, grade: ctx.grade, classSize: ctx.classSize, facilities: ctx.facilities };
  let score = isPedagogyRecommended(item, recCtx) ? 4 : 1;
  const id = item.id;
  if (/nhom|thao luan|hop tac/.test(hay) && ["cooperative", "discuss", "tps", "tps-tech", "tablecloth", "jigsaw", "jigsaw-tech"].includes(id)) score += 3;
  if (/du an|van de thuc tien|van dung|thuc tien/.test(hay) && ["pbl", "mini-project", "product", "experiential", "situation", "case", "open-ex"].includes(id)) score += 3;
  if (/do dac|thi nghiem|hinh hoc|mo hinh/.test(hay) && ["steam", "experiment", "experiential"].includes(id)) score += 3;
  if ((ctx.readiness === "Không đồng đều" || /phan hoa|muc do/.test(hay)) && ["differentiation", "diff-ex"].includes(id)) score += 3;
  if (/tro choi|khoi dong/.test(hay) && ["game", "starter-game", "wordgame"].includes(id)) score += 2;
  if (/tom tat|so do|khai niem|dinh nghia/.test(hay) && ["mindmap", "mindmap-tech", "kwl", "kwl-tech"].includes(id)) score += 2;
  if (/cau hoi|kham pha/.test(hay) && ["socratic", "stim-question", "5w1h"].includes(id)) score += 2;
  if (/tinh huong|vi du/.test(hay) && ["case", "situation", "5w1h"].includes(id)) score += 2;
  if (["khtn", "vatly", "hoahoc", "sinhhoc", "khoahoc"].includes(String(ctx.subjectId || "")) && id === "5e") score += 3;
  if (["nguvan", "tiengviet", "tienganh", "gdcd", "daoduc"].includes(String(ctx.subjectId || "")) && ["debate", "roleplay"].includes(id)) score += 3;
  if (["tps", "tps-tech", "stim-question", "exit", "skill-group", "present"].includes(id)) score += 1;
  if (item.recommendFor && item.recommendFor.needsFacilities) {
    const facilities = ctx.facilities || {};
    if (!item.recommendFor.needsFacilities.some(key => facilities[key])) score = 0;
  }
  if (item.recommendFor && typeof item.recommendFor.maxClassSize === "number" && Number(ctx.classSize) > item.recommendFor.maxClassSize) score -= 3;
  return score;
}

function pickTopPedagogy(list, ctx, n) {
  return (list || [])
    .map(item => ({ item, score: scorePedagogyItem(item, ctx) }))
    .filter(row => row.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, n)
    .map(row => row.item.id);
}

function recommendPedagogyFromLesson(ctx) {
  const catalog = KHBD_PEDAGOGY_CATALOG;
  const techniques = { A: [], B: [], C: [], D: [] };
  ["A", "B", "C", "D"].forEach(phase => {
    techniques[phase] = pickTopPedagogy(catalog.techniques.filter(item => (item.phases || []).includes(phase)), ctx, 1);
  });
  return {
    methods: pickTopPedagogy(catalog.methods, ctx, 2),
    techniques,
    activities: pickTopPedagogy(catalog.activities, ctx, 2)
  };
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = { KHBD_PEDAGOGY_CATALOG, isPedagogyRecommended, recommendPedagogyFromLesson };
}
