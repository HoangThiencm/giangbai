/* Catalog reviewed from local official sources. NLS intentionally lists only verified MIỀN, not unverified component codes. */
const KHBD_STANDARDS = {
  digital: {
    framework: "Thông tư 02/2025/TT-BGDĐT", date: "24/01/2025", source: "02-bgddt.pdf; hướng dẫn 23456bgddthuong-dan-trien-khai-thuc-hien_219202522.pdf",
    entries: [
      "Khai thác dữ liệu và thông tin", "Giao tiếp và hợp tác trong môi trường số", "Sáng tạo nội dung số", "An toàn", "Giải quyết vấn đề", "Ứng dụng trí tuệ nhân tạo"
    ].map((label, index) => ({ id: `tt02-domain-${index + 1}`, label, kind: "Miền năng lực số", grades: [6, 7, 8, 9] }))
  },
  ai: {
    framework: "Khung nội dung giáo dục trí tuệ nhân tạo cho học sinh phổ thông", date: "18/08/2026", source: "Quyết định 2422/QĐ-BGDĐT, 260818-QD2422-KhungAI.pdf",
    entries: [
      { id: "qd2422-6-a13", code: "6.A1.3", grades: [6], label: "Thực hiện được việc kiểm tra lại một kết quả do AI đưa ra trước khi sử dụng, thể hiện thói quen con người quyết định cuối cùng." },
      { id: "qd2422-7-a12", code: "7.A1.2", grades: [7], label: "Nêu được ví dụ hậu quả có thể xảy ra khi không có sự xác thực của con người về độ chính xác của kết quả do AI đưa ra." },
      { id: "qd2422-8-a12", code: "8.A1.2", grades: [8], label: "Nêu được những rủi ro của việc lạm dụng các công cụ AI tạo sinh và sự cần thiết của việc kiểm chứng nguồn thông tin khi sử dụng AI tạo sinh trong học tập." },
      { id: "qd2422-9-b21", code: "9.B2.1", grades: [9], label: "Trình bày được vai trò của người dùng trong việc kiểm soát và chịu trách nhiệm đối với kết quả cuối cùng do AI tạo ra; khai báo được việc sử dụng AI trong sản phẩm học tập." }
    ]
  }
};

if (typeof module !== "undefined" && module.exports) module.exports = { KHBD_STANDARDS };
