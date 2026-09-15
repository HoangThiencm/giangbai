const app = require('../js/khbd-app.js');
const { DocxGenerator } = require('../js/khbd-docx.js');

const raw = `+ Bước 1: Chuyển giao nhiệm vụ: (Kỹ thuật 5W1H) GV: Trình chiếu H1.3 và giao nhiệm vụ: "Các em hãy xác định: Cái gì (What) là tập hợp M? Ai/Đối tượng nào (Who) là phần tử của M? Làm thế nào (How) để viết kí hiệu khi một số nằm trong M?". HS: Quan sát hình, chuẩn bị trả lời cá nhân.

+ Bước 2: Thực hiện nhiệm vụ: (Kỹ thuật Think-Pair-Share) HS: Think (1 phút): Tự viết các phần tử của M vào nháp; Pair (2 phút): Trao đổi với bạn bên cạnh về cách dùng kí hiệu \\in, \\notin. GV: Quan sát, dự kiến lỗi sai: HS viết kí hiệu ngược hoặc nhầm lẫn giữa tập hợp (chữ in hoa) và phần tử (chữ thường/số). Hỗ trợ HS phân biệt 7 \\notin M vì số 7 không có trong vòng kín của H1.3.

+ Bước 3: Báo cáo, thảo luận: HS: Đại diện cặp đôi lên bảng viết kí hiệu cho các số 4, 1, 9, 8, 7 đối với tập M. GV: "Tại sao số 7 lại dùng kí hiệu \\notin?". HS giải thích dựa trên vị trí của số 7 so với vòng biểu diễn tập hợp.

+ Bước 4: Kết luận, nhận định: GV: Chốt kiến thức về tên tập hợp (chữ in hoa) và cách dùng kí hiệu. HS: Ghi bài vào vở.`;

console.log("=== 1. formatKhbdRoleLineBreaks output ===");
const formatted = app.formatKhbdRoleLineBreaks(raw);
console.log(formatted);
