const KHBD_PEDAGOGY_CATALOG = {
  methods: [
    { id: "pbl", label: "Dạy học giải quyết vấn đề", phases: ["A","B","C","D"], description: "Xác định và giải quyết vấn đề có minh chứng." },
    { id: "cooperative", label: "Dạy học hợp tác", phases: ["A","B","C","D"], description: "Phân vai, cùng tạo sản phẩm." },
    { id: "differentiation", label: "Dạy học phân hóa", phases: ["B","C","D"], description: "Nhiệm vụ phù hợp mức sẵn sàng." },
    { id: "steam", label: "STEM/STEAM", phases: ["B","D"], description: "Thiết kế, thử nghiệm sản phẩm." }
    ,{ id:"flipped", label:"Lớp học đảo ngược", phases:["B","C"], description:"Chuẩn bị trước, học sâu trên lớp." },{ id:"game", label:"Dạy học dựa trên trò chơi", phases:["A","C"], description:"Nhiệm vụ có luật chơi." },{ id:"socratic", label:"Đối thoại Socratic", phases:["B","D"], description:"Câu hỏi gợi mở và lập luận." },{ id:"mindmap", label:"Sơ đồ tư duy", phases:["B","C"], description:"Tổ chức ý tưởng trực quan." },{id:"experiential",label:"Học tập trải nghiệm",phases:["A","D"],description:"Liên hệ tình huống thực tế."},{id:"5w1h",label:"5W1H",phases:["A","B"],description:"Khai thác vấn đề bằng câu hỏi."}
  ],
  techniques: [
    { id: "tps", label: "Think-Pair-Share", phases: ["A","B","C"], description: "Suy nghĩ cá nhân, trao đổi cặp, chia sẻ." },
    { id: "jigsaw", label: "Mảnh ghép", phases: ["B","C"], description: "Nhóm chuyên gia rồi chia sẻ." },
    { id: "gallery", label: "Gallery Walk", phases: ["B","C","D"], description: "Trưng bày, phản hồi sản phẩm." },
    { id: "exit", label: "Exit ticket", phases: ["C","D"], description: "Ghi nhận nhanh mức độ đạt." }
    ,{id:"brainstorm",label:"Động não",phases:["A","B"],description:"Nêu ý tưởng nhanh."},{id:"kwl",label:"KWL",phases:["A","B","D"],description:"Biết–Muốn biết–Đã học."},{id:"station",label:"Trạm học tập",phases:["B","C"],description:"Luân phiên nhiệm vụ."},{id:"mindmap-tech",label:"Sơ đồ tư duy",phases:["B","C"],description:"Tóm tắt mạch kiến thức."},{id:"khăn",label:"Khăn trải bàn",phases:["B","C"],description:"Ý kiến cá nhân và nhóm."},{id:"peer",label:"Đánh giá đồng đẳng",phases:["C","D"],description:"Phản hồi theo tiêu chí."},{id:"debate",label:"Tranh biện có cấu trúc",phases:["B","D"],description:"Lập luận có bằng chứng."},{id:"case",label:"Nghiên cứu tình huống",phases:["B","D"],description:"Phân tích tình huống."},{id:"roleplay",label:"Đóng vai",phases:["A","D"],description:"Thực hành vai trò."},{id:"open",label:"Bài toán/vấn đề mở",phases:["B","D"],description:"Nhiều cách tiếp cận."}
  ],
  mathActivities: [
    { id: "math-group", label: "Giải quyết vấn đề theo nhóm", phases: ["B","C","D"], description: "Nhóm lập luận và trình bày lời giải." },
    { id: "math-multiple", label: "Thảo luận nhiều cách giải", phases: ["B","C"], description: "So sánh các cách giải." },
    { id: "math-diff", label: "Bài tập phân hóa 3 mức", phases: ["C"], description: "Nhiệm vụ theo mức sẵn sàng." },
    { id: "math-game", label: "Trò chơi Toán học", phases: ["A","C"], description: "Luyện tập có luật chơi." }
    ,{id:"math-geogebra",label:"Minh họa GeoGebra/Desmos",phases:["B","C"],description:"Trực quan hóa có kiểm chứng."},{id:"math-present",label:"Trình bày lời giải",phases:["B","C"],description:"Trình bày và bảo vệ lập luận."},{id:"math-peer",label:"Đánh giá đồng đẳng",phases:["C","D"],description:"Phản hồi lời giải theo tiêu chí."},{id:"math-real",label:"Tạo bài toán thực tiễn",phases:["D"],description:"Mô hình hóa từ đời sống."}
  ]
  ,genericActivities: [
    { id: "generic-discuss", label: "Thảo luận nhóm có phân vai", phases: ["A","B","C","D"], description: "Nhóm hoàn thành nhiệm vụ và nộp minh chứng." },
    { id: "generic-product", label: "Trình bày sản phẩm và phản hồi", phases: ["B","C","D"], description: "Công bố sản phẩm, phản hồi theo tiêu chí." },
    { id: "generic-reflect", label: "Nhật ký học tập", phases: ["C","D"], description: "Tự phản ánh điều đã học và bước tiếp theo." }
  ]
};
