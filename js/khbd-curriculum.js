/**
 * js/khbd-curriculum.js
 * Mục lục bài học THCS (lớp 6–9) theo bộ sách chung.
 * Toán 6–9 giữ danh mục đã kiểm duyệt; các môn khác nhập từ mục lục SGK.
 * Tích hợp Khung Năng lực Đặc thù, Khung Năng lực AI (QĐ 2422), Khung Năng lực Số (TT 02/2025).
 */


const SUBJECT_COMPETENCIES = {
  toan: ['Tư duy và lập luận toán học', 'Mô hình hoá toán học', 'Giải quyết vấn đề toán học', 'Giao tiếp toán học', 'Sử dụng công cụ, phương tiện toán học'],
  nguvan: ['Năng lực ngôn ngữ (Đọc, Viết, Nói, Nghe)', 'Năng lực văn học (Cảm thụ và thưởng thức thẩm mĩ)'],
  tiengviet: ['Năng lực ngôn ngữ (Đọc, Viết, Nói, Nghe)', 'Năng lực văn học (Cảm thụ thẩm mĩ)'],
  tienganh: ['Năng lực giao tiếp (Nghe, Nói, Đọc, Viết)', 'Năng lực tiếp nhận ngôn ngữ', 'Năng lực sản sinh ngôn ngữ'],
  khtn: ['Nhận thức khoa học tự nhiên', 'Tìm hiểu tự nhiên', 'Vận dụng kiến thức, kĩ năng đã học'],
  vatly: ['Nhận thức vật lí', 'Tìm hiểu tự nhiên dưới góc độ vật lí', 'Vận dụng kiến thức, kĩ năng vật lí'],
  hoahoc: ['Nhận thức hóa học', 'Tìm hiểu tự nhiên dưới góc độ hóa học', 'Vận dụng kiến thức, kĩ năng hóa học'],
  sinhhoc: ['Nhận thức sinh học', 'Tìm hiểu tự nhiên dưới góc độ sinh học', 'Vận dụng kiến thức, kĩ năng sinh học'],
  lichsudialy: ['Nhận thức lịch sử và địa lí', 'Tìm hiểu lịch sử và địa lí', 'Vận dụng kiến thức, kĩ năng lịch sử và địa lí'],
  'lichsudialy-th': ['Nhận thức lịch sử và địa lí', 'Tìm hiểu lịch sử và địa lí', 'Vận dụng kiến thức, kĩ năng'],
  lichsu: ['Tìm hiểu lịch sử', 'Nhận thức và tư duy lịch sử', 'Vận dụng kiến thức, kĩ năng lịch sử'],
  dialy: ['Nhận thức khoa học địa lí', 'Tìm hiểu địa lí', 'Vận dụng kiến thức, kĩ năng địa lí'],
  gdcd: ['Nhận thức chuẩn mực đạo đức, pháp luật', 'Đánh giá hành vi của bản thân và người khác', 'Điều chỉnh hành vi'],
  daoduc: ['Nhận thức chuẩn mực đạo đức', 'Đánh giá hành vi', 'Điều chỉnh hành vi'],
  gdktpl: ['Nhận thức kinh tế, pháp luật', 'Tìm hiểu và tham gia hoạt động kinh tế – xã hội', 'Vận dụng kiến thức kinh tế, pháp luật'],
  tinhoc: ['Sử dụng và quản lí các phương tiện công nghệ thông tin và truyền thông', 'Ứng xử phù hợp trong môi trường số', 'Giải quyết vấn đề với sự hỗ trợ của công nghệ thông tin và truyền thông', 'Ứng dụng công nghệ thông tin và truyền thông trong học và tự học', 'Hợp tác trong môi trường số'],
  congnghe: ['Nhận thức công nghệ', 'Giao tiếp công nghệ', 'Sử dụng công nghệ', 'Đánh giá công nghệ', 'Thiết kế kĩ thuật'],
  amnhac: ['Thể hiện âm nhạc', 'Cảm thụ và hiểu biết âm nhạc', 'Ứng dụng và sáng tạo âm nhạc'],
  mithuat: ['Quan sát và nhận thức thẩm mĩ', 'Sáng tạo và ứng dụng thẩm mĩ', 'Phân tích và đánh giá thẩm mĩ'],
  gdtc: ['Chăm sóc sức khỏe', 'Vận động cơ bản', 'Hoạt động thể dục thể thao'],
  tnxh: ['Nhận thức khoa học', 'Tìm hiểu môi trường tự nhiên và xã hội xung quanh', 'Vận dụng kiến thức, kĩ năng đã học'],
  khoahoc: ['Nhận thức khoa học', 'Tìm hiểu môi trường tự nhiên', 'Vận dụng kiến thức, kĩ năng khoa học'],
  hdtn: ['Thích ứng với cuộc sống', 'Thiết kế và tổ chức hoạt động', 'Định hướng nghề nghiệp (từ THCS)'],
  'hdtn-hn': ['Thích ứng với cuộc sống', 'Thiết kế và tổ chức hoạt động', 'Định hướng nghề nghiệp'],
  gdqpan: ['Nhận thức quốc phòng và an ninh', 'Kĩ năng quân sự, an ninh cơ bản']
};

const CURRICULUM_DATA = {

  // DANH MỤC KHỐI LỚP
  version: "nxbgd-snapshot-2026-08-26", sourceUrl: "https://taphuan.nxbgd.vn/tap-huan/doc-sach/",
  grades: [
    { id: '6', name: 'Lớp 6' },
    { id: '7', name: 'Lớp 7' },
    { id: '8', name: 'Lớp 8' },
    { id: '9', name: 'Lớp 9' }
  ],
  subjects: [
    { id: 'toan', name: 'Toán', grades: [6, 7, 8, 9] },
    { id: 'nguvan', name: 'Ngữ văn', grades: [6, 7, 8, 9] },
    { id: 'khtn', name: 'Khoa học tự nhiên', grades: [6, 7, 8, 9] },
    { id: 'lichsudialy', name: 'Lịch sử và Địa lí', grades: [6, 7, 8, 9] },
    { id: 'gdcd', name: 'Giáo dục công dân', grades: [6, 7, 8, 9] },
    { id: 'tinhoc', name: 'Tin học', grades: [6, 7, 8, 9] },
    { id: 'congnghe', name: 'Công nghệ', grades: [6, 7, 8, 9] },
    { id: 'amnhac', name: 'Âm nhạc', grades: [6, 7, 8, 9] },
    { id: 'mithuat', name: 'Mĩ thuật', grades: [6, 7, 8, 9] },
    { id: 'gdtc', name: 'Giáo dục thể chất', grades: [6, 7, 8, 9] },
    { id: 'hdtn-hn', name: 'Hoạt động trải nghiệm, hướng nghiệp', grades: [6, 7, 8, 9] },
    { id: 'tienganh', name: 'Tiếng Anh', grades: [6, 7, 8, 9] }
  ],
  books: [{ id: "bo-sach-chung", grades: [6, 7, 8, 9], label: "Danh mục bài học THCS", sourceUrl: "https://taphuan.nxbgd.vn/tap-huan/doc-sach/", catalogVersion: "2026-08-26" }],

  // MỤC LỤC CHI TIẾT THEO TỪNG KHỐI LỚP
  lessons: {
    "6": [
      {
        chapter: "Chương I: Tập hợp các số tự nhiên (Tập 1)",
        items: [
          "Bài 1: Tập hợp",
          "Bài 2: Cách ghi số tự nhiên",
          "Bài 3: Thứ tự trong tập hợp các số tự nhiên",
          "Bài 4: Phép cộng và phép trừ số tự nhiên",
          "Bài 5: Phép nhân và phép chia số tự nhiên",
          "Luyện tập chung trang 21",
          "Bài 6: Lũy thừa với số mũ tự nhiên",
          "Bài 7: Thứ tự thực hiện các phép tính",
          "Luyện tập chung trang 27",
          "Bài tập cuối chương I"
        ]
      },
      {
        chapter: "Chương II: Tính chia hết trong tập hợp các số tự nhiên (Tập 1)",
        items: [
          "Bài 8: Quan hệ chia hết và tính chất",
          "Bài 9: Dấu hiệu chia hết",
          "Bài 10: Số nguyên tố",
          "Bài 11: Ước chung. Ước chung lớn nhất",
          "Bài 12: Bội chung. Bội chung nhỏ nhất",
          "Luyện tập chung trang 54",
          "Bài tập cuối chương II"
        ]
      },
      {
        chapter: "Chương III: Số nguyên (Tập 1)",
        items: [
          "Bài 13: Tập hợp các số nguyên",
          "Bài 14: Phép cộng và phép trừ số nguyên",
          "Luyện tập chung trang 69",
          "Bài 15: Quy tắc dấu ngoặc",
          "Bài 16: Phép nhân số nguyên",
          "Bài 17: Phép chia hết. Bội và ước của một số nguyên",
          "Luyện tập chung trang 78",
          "Bài tập cuối chương III"
        ]
      },
      {
        chapter: "Chương IV: Một số hình phẳng trong thực tiễn (Tập 1)",
        items: [
          "Bài 18: Tam giác đều. Hình vuông. Lục giác đều",
          "Bài 19: Hình chữ nhật. Hình thoi. Hình bình hành. Hình thang cân",
          "Bài 20: Chu vi và diện tích của một số tứ giác đã học",
          "Luyện tập chung trang 95",
          "Bài tập cuối chương IV"
        ]
      },
      {
        chapter: "Chương V: Tính đối xứng của hình phẳng trong tự nhiên (Tập 1)",
        items: [
          "Bài 21: Hình có trục đối xứng",
          "Bài 22: Hình có tâm đối xứng",
          "Luyện tập chung trang 108",
          "Bài tập cuối chương V"
        ]
      },
      {
        chapter: "Chương VI: Phân số (Tập 2)",
        items: [
          "Bài 23: Mở rộng phân số. Phân số bằng nhau",
          "Bài 24: So sánh phân số. Hỗn số dương",
          "Luyện tập chung trang 13",
          "Bài 25: Phép cộng và phép trừ phân số",
          "Bài 26: Phép nhân và phép chia phân số",
          "Luyện tập chung trang 21",
          "Bài 27: Hai bài toán về phân số",
          "Luyện tập chung trang 25",
          "Bài tập cuối chương VI"
        ]
      },
      {
        chapter: "Chương VII: Số thập phân (Tập 2)",
        items: [
          "Bài 28: Số thập phân",
          "Bài 29: Tính toán với số thập phân",
          "Luyện tập chung trang 38",
          "Bài 30: Làm tròn và ước lượng",
          "Bài 31: Một số bài toán về tỉ số và tỉ số phần trăm",
          "Luyện tập chung trang 47",
          "Bài tập cuối chương VII"
        ]
      },
      {
        chapter: "Chương VIII: Những hình hình học cơ bản (Tập 2)",
        items: [
          "Bài 32: Điểm và đường thẳng",
          "Bài 33: Điểm nằm giữa hai điểm. Tia",
          "Bài 34: Đoạn thẳng. Độ dài đoạn thẳng",
          "Bài 35: Trung điểm của đoạn thẳng",
          "Luyện tập chung trang 59",
          "Bài 36: Góc",
          "Bài 37: Số đo góc",
          "Luyện tập chung trang 66",
          "Bài tập cuối chương VIII"
        ]
      },
      {
        chapter: "Chương IX: Dữ liệu và xác suất thực nghiệm (Tập 2)",
        items: [
          "Bài 38: Dữ liệu và thu thập dữ liệu",
          "Bài 39: Bảng thống kê và biểu đồ tranh",
          "Bài 40: Biểu đồ cột",
          "Bài 41: Biểu đồ cột kép",
          "Luyện tập chung trang 87",
          "Bài 42: Kết quả có thể và sự kiện trong trò chơi, thí nghiệm",
          "Bài 43: Xác suất thực nghiệm",
          "Luyện tập chung trang 97",
          "Bài tập cuối chương IX"
        ]
      }
    ],

    "7": [
      {
        chapter: "Chương I: Số hữu tỉ (Tập 1)",
        items: [
          "Bài 1: Tập hợp các số hữu tỉ",
          "Bài 2: Cộng, trừ, nhân, chia số hữu tỉ",
          "Luyện tập chung trang 14",
          "Bài 3: Lũy thừa với số mũ tự nhiên của một số hữu tỉ",
          "Bài 4: Thứ tự thực hiện các phép tính. Quy tắc chuyển vế",
          "Luyện tập chung trang 24",
          "Bài tập cuối chương I"
        ]
      },
      {
        chapter: "Chương II: Số thực (Tập 1)",
        items: [
          "Bài 5: Làm quen với số thập phân vô hạn tuần hoàn",
          "Bài 6: Số vô tỉ. Căn bậc hai số học",
          "Bài 7: Tập hợp các số thực",
          "Luyện tập chung trang 38",
          "Bài tập cuối chương II"
        ]
      },
      {
        chapter: "Chương III: Góc và đường thẳng song song (Tập 1)",
        items: [
          "Bài 8: Góc ở vị trí đặc biệt. Tia phân giác của một góc",
          "Bài 9: Hai đường thẳng song song và dấu hiệu nhận biết",
          "Luyện tập chung trang 50",
          "Bài 10: Tiên đề Euclid. Tính chất của hai đường thẳng song song",
          "Bài 11: Định lí và chứng minh định lí",
          "Luyện tập chung trang 58",
          "Bài tập cuối chương III"
        ]
      },
      {
        chapter: "Chương IV: Tam giác bằng nhau (Tập 1)",
        items: [
          "Bài 12: Tổng các góc trong một tam giác",
          "Bài 13: Hai tam giác bằng nhau. Trường hợp bằng nhau thứ nhất của tam giác",
          "Bài 14: Trường hợp bằng nhau thứ hai và thứ ba của tam giác",
          "Luyện tập chung trang 74",
          "Bài 15: Các trường hợp bằng nhau của tam giác vuông",
          "Bài 16: Tam giác cân. Đường trung trực của đoạn thẳng",
          "Luyện tập chung trang 86",
          "Bài tập cuối chương IV"
        ]
      },
      {
        chapter: "Chương V: Thu thập và biểu diễn dữ liệu (Tập 1)",
        items: [
          "Bài 17: Thu thập và phân loại dữ liệu",
          "Bài 18: Biểu đồ hình quạt tròn",
          "Bài 19: Biểu đồ đoạn thẳng",
          "Luyện tập chung trang 107",
          "Bài tập cuối chương V"
        ]
      },
      {
        chapter: "Chương VI: Tỉ lệ thức và đại lượng tỉ lệ (Tập 2)",
        items: [
          "Bài 20: Tỉ lệ thức",
          "Bài 21: Tính chất của dãy tỉ số bằng nhau",
          "Luyện tập chung trang 11",
          "Bài 22: Đại lượng tỉ lệ thuận",
          "Bài 23: Đại lượng tỉ lệ nghịch",
          "Luyện tập chung trang 20",
          "Bài tập cuối chương VI"
        ]
      },
      {
        chapter: "Chương VII: Biểu thức đại số và đa thức một biến (Tập 2)",
        items: [
          "Bài 24: Biểu thức đại số",
          "Bài 25: Đa thức một biến",
          "Bài 26: Phép cộng và phép trừ đa thức một biến",
          "Luyện tập chung trang 37",
          "Bài 27: Phép nhân đa thức một biến",
          "Bài 28: Phép chia đa thức một biến",
          "Luyện tập chung trang 45",
          "Bài tập cuối chương VII"
        ]
      },
      {
        chapter: "Chương VIII: Làm quen với biến cố và xác suất của biến cố (Tập 2)",
        items: [
          "Bài 29: Làm quen với biến cố",
          "Bài 30: Làm quen với xác suất của biến cố",
          "Luyện tập chung trang 56",
          "Bài tập cuối chương VIII"
        ]
      },
      {
        chapter: "Chương IX: Quan hệ giữa các yếu tố trong một tam giác (Tập 2)",
        items: [
          "Bài 31: Quan hệ giữa góc và cạnh đối diện trong một tam giác",
          "Bài 32: Quan hệ giữa đường vuông góc và đường xiên",
          "Bài 33: Quan hệ giữa ba cạnh của một tam giác",
          "Luyện tập chung trang 71",
          "Bài 34: Sự đồng quy của ba đường trung tuyến, ba đường phân giác trong một tam giác",
          "Bài 35: Sự đồng quy của ba đường trung trực, ba đường cao trong một tam giác",
          "Luyện tập chung trang 83",
          "Bài tập cuối chương IX"
        ]
      },
      {
        chapter: "Chương X: Một số hình khối trong thực tiễn (Tập 2)",
        items: [
          "Bài 36: Hình hộp chữ nhật và hình lập phương",
          "Bài 37: Hình lăng trụ đứng tam giác và hình lăng trụ đứng tứ giác",
          "Luyện tập chung trang 101",
          "Bài tập cuối chương X"
        ]
      }
    ],

    "8": [
      {
        chapter: "Chương I: Đa thức (Tập 1)",
        items: [
          "Bài 1: Đơn thức",
          "Bài 2: Đa thức",
          "Bài 3: Phép cộng và phép trừ đa thức",
          "Luyện tập chung trang 17",
          "Bài 4: Phép nhân đa thức",
          "Bài 5: Phép chia đa thức cho đơn thức",
          "Luyện tập chung trang 25",
          "Bài tập cuối chương I"
        ]
      },
      {
        chapter: "Chương II: Hằng đẳng thức đáng nhớ và ứng dụng (Tập 1)",
        items: [
          "Bài 6: Hiệu hai bình phương. Bình phương của một tổng hay một hiệu",
          "Bài 7: Lập phương của một tổng. Lập phương của một hiệu",
          "Bài 8: Tổng và hiệu hai lập phương",
          "Luyện tập chung trang 40",
          "Bài 9: Phân tích đa thức thành nhân tử",
          "Luyện tập chung trang 45",
          "Bài tập cuối chương II"
        ]
      },
      {
        chapter: "Chương III: Tứ giác (Tập 1)",
        items: [
          "Bài 10: Tứ giác",
          "Bài 11: Hình thang cân",
          "Luyện tập chung trang 56",
          "Bài 12: Hình bình hành",
          "Bài 13: Hình chữ nhật",
          "Bài 14: Hình thoi và hình vuông",
          "Luyện tập chung trang 73",
          "Bài tập cuối chương III"
        ]
      },
      {
        chapter: "Chương IV: Định lí Thalès (Tập 1)",
        items: [
          "Bài 15: Định lí Thalès trong tam giác",
          "Bài 16: Đường trung bình của tam giác",
          "Bài 17: Tính chất đường phân giác của tam giác",
          "Luyện tập chung trang 91",
          "Bài tập cuối chương IV"
        ]
      },
      {
        chapter: "Chương V: Dữ liệu và biểu đồ (Tập 1)",
        items: [
          "Bài 18: Thu thập và phân loại dữ liệu",
          "Bài 19: Biểu diễn dữ liệu bằng bảng, biểu đồ",
          "Bài 20: Phân tích số liệu thống kê dựa vào biểu đồ",
          "Luyện tập chung trang 112",
          "Bài tập cuối chương V"
        ]
      },
      {
        chapter: "Chương VI: Phân thức đại số (Tập 2)",
        items: [
          "Bài 21: Phân thức đại số",
          "Bài 22: Tính chất cơ bản của phân thức đại số",
          "Luyện tập chung trang 12",
          "Bài 23: Phép cộng và phép trừ phân thức đại số",
          "Bài 24: Phép nhân và phép chia phân thức đại số",
          "Luyện tập chung trang 24",
          "Bài tập cuối chương VI"
        ]
      },
      {
        chapter: "Chương VII: Phương trình bậc nhất và hàm số bậc nhất (Tập 2)",
        items: [
          "Bài 25: Phương trình bậc nhất một ẩn",
          "Bài 26: Giải bài toán bằng cách lập phương trình",
          "Luyện tập chung trang 37",
          "Bài 27: Khái niệm hàm số và đồ thị của hàm số",
          "Bài 28: Hàm số bậc nhất y = ax + b và đồ thị",
          "Bài 29: Hệ số góc của đường thẳng",
          "Luyện tập chung trang 55",
          "Bài tập cuối chương VII"
        ]
      },
      {
        chapter: "Chương VIII: Mở đầu về tính xác suất của biến cố (Tập 2)",
        items: [
          "Bài 30: Kết quả có thể và kết quả thuận lợi",
          "Bài 31: Cách tính xác suất của biến cố bằng tỉ số",
          "Bài 32: Mối liên hệ giữa xác suất thực nghiệm với xác suất lí thuyết",
          "Luyện tập chung trang 67",
          "Bài tập cuối chương VIII"
        ]
      },
      {
        chapter: "Chương IX: Tam giác đồng dạng (Tập 2)",
        items: [
          "Bài 33: Hai tam giác đồng dạng",
          "Bài 34: Ba trường hợp đồng dạng của hai tam giác",
          "Luyện tập chung trang 86",
          "Bài 35: Định lí Pythagore và ứng dụng",
          "Bài 36: Các trường hợp đồng dạng của hai tam giác vuông",
          "Bài 37: Hình đồng dạng",
          "Luyện tập chung trang 106",
          "Bài tập cuối chương IX"
        ]
      },
      {
        chapter: "Chương X: Một số hình khối trong thực tiễn (Tập 2)",
        items: [
          "Bài 38: Hình chóp tam giác đều",
          "Bài 39: Hình chóp tứ giác đều",
          "Luyện tập chung trang 122",
          "Bài tập cuối chương X"
        ]
      }
    ],

    "9": [
      {
        chapter: "Chương I: Phương trình và hệ hai phương trình bậc nhất hai ẩn (Tập 1)",
        items: [
          "Bài 1: Khái niệm phương trình và hệ hai phương trình bậc nhất hai ẩn",
          "Bài 2: Giải hệ hai phương trình bậc nhất hai ẩn",
          "Luyện tập chung trang 19",
          "Bài 3: Giải bài toán bằng cách lập hệ phương trình",
          "Bài tập cuối chương I"
        ]
      },
      {
        chapter: "Chương II: Phương trình và bất phương trình bậc nhất một ẩn (Tập 1)",
        items: [
          "Bài 4: Phương trình quy về phương trình bậc nhất một ẩn",
          "Bài 5: Bất đẳng thức và tính chất",
          "Luyện tập chung trang 38",
          "Bài 6: Bất phương trình bậc nhất một ẩn",
          "Bài tập cuối chương II"
        ]
      },
      {
        chapter: "Chương III: Căn bậc hai và căn bậc ba (Tập 1)",
        items: [
          "Bài 7: Căn bậc hai và căn thức bậc hai",
          "Bài 8: Khai căn bậc hai với phép nhân và phép chia",
          "Luyện tập chung trang 57",
          "Bài 9: Biến đổi đơn giản và rút gọn biểu thức chứa căn thức bậc hai",
          "Bài 10: Căn bậc ba và căn thức bậc ba",
          "Luyện tập chung trang 69",
          "Bài tập cuối chương III"
        ]
      },
      {
        chapter: "Chương IV: Hệ thức lượng trong tam giác vuông (Tập 1)",
        items: [
          "Bài 11: Tỉ số lượng giác của góc nhọn",
          "Bài 12: Một số hệ thức giữa cạnh, góc trong tam giác vuông và ứng dụng",
          "Luyện tập chung trang 89",
          "Bài tập cuối chương IV"
        ]
      },
      {
        chapter: "Chương V: Đường tròn (Tập 1)",
        items: [
          "Bài 13: Mở đầu về đường tròn",
          "Bài 14: Cung và dây của một đường tròn",
          "Luyện tập chung trang 104",
          "Bài 15: Độ dài của cung tròn. Diện tích hình quạt tròn và hình vành khuyên",
          "Bài 16: Vị trí tương đối của đường thẳng và đường tròn",
          "Bài 17: Vị trí tương đối của hai đường tròn",
          "Luyện tập chung trang 119",
          "Bài tập cuối chương V"
        ]
      },
      {
        chapter: "Chương VI: Hàm số y = ax² (a ≠ 0). Phương trình bậc hai một ẩn (Tập 2)",
        items: [
          "Bài 18: Hàm số y = ax² (a ≠ 0)",
          "Bài 19: Phương trình bậc hai một ẩn",
          "Luyện tập chung trang 16",
          "Bài 20: Định lí Viète và ứng dụng",
          "Bài 21: Giải bài toán bằng cách lập phương trình",
          "Luyện tập chung trang 28",
          "Bài tập cuối chương VI"
        ]
      },
      {
        chapter: "Chương VII: Tần số và tần số tương đối (Tập 2)",
        items: [
          "Bài 22: Bảng tần số và biểu đồ tần số",
          "Bài 23: Bảng tần số tương đối và biểu đồ tần số tương đối",
          "Luyện tập chung trang 46",
          "Bài 24: Bảng tần số ghép nhóm và biểu đồ tần số ghép nhóm",
          "Luyện tập chung trang 58",
          "Bài tập cuối chương VII"
        ]
      },
      {
        chapter: "Chương VIII: Xác suất của biến cố trong một số mô hình xác suất đơn giản (Tập 2)",
        items: [
          "Bài 25: Phép thử ngẫu nhiên và không gian mẫu",
          "Bài 26: Xác suất của biến cố liên quan tới phép thử",
          "Luyện tập chung trang 73",
          "Bài tập cuối chương VIII"
        ]
      },
      {
        chapter: "Chương IX: Đường tròn ngoại tiếp và đường tròn nội tiếp (Tập 2)",
        items: [
          "Bài 27: Góc nội tiếp",
          "Bài 28: Đường tròn ngoại tiếp và đường tròn nội tiếp của một tam giác",
          "Luyện tập chung trang 92",
          "Bài 29: Tứ giác nội tiếp",
          "Bài 30: Đa giác đều",
          "Luyện tập chung trang 107",
          "Bài tập cuối chương IX"
        ]
      },
      {
        chapter: "Chương X: Một số hình khối trong thực tiễn (Tập 2)",
        items: [
          "Bài 31: Hình trụ và hình nón",
          "Bài 32: Hình cầu",
          "Luyện tập chung trang 123",
          "Bài tập cuối chương X"
        ]
      }
    ]
  },

  // KHUNG NĂNG LỰC ĐẶC THÙ MÔN TOÁN (Theo Chương trình GDPT 2018 & nanglucdacthu.txt)
  mathCompetencies: [
    {
      code: "TDLL",
      name: "Năng lực Tư duy và Lập luận Toán học",
      description: "Thực hiện được các thao tác tư duy (so sánh, phân tích, tổng hợp, trừu tượng hoá, khái quát hoá); giải thích được sự tương đồng và khác biệt; thực hiện lập luận hợp lí, nêu và trả lời câu hỏi khi giải quyết vấn đề; chứng minh được mệnh đề toán học."
    },
    {
      code: "MHH",
      name: "Năng lực Mô hình hoá Toán học",
      description: "Sử dụng được các mô hình toán học (công thức, sơ đồ, bảng biểu, hình vẽ, phương trình, hệ phương trình...) để mô tả tình huống thực tiễn; giải quyết vấn đề toán học trong mô hình thiết lập; thể hiện lời giải vào ngữ cảnh thực tiễn và kiểm chứng."
    },
    {
      code: "GQVĐ",
      name: "Năng lực Giải quyết Vấn đề Toán học",
      description: "Phát hiện được vấn đề cần giải quyết; xác định cách thức, giải pháp giải quyết vấn đề; sử dụng kiến thức, kĩ năng toán học tương thích; giải thích và đánh giá giải pháp đã thực hiện."
    },
    {
      code: "GTTH",
      name: "Năng lực Giao tiếp Toán học",
      description: "Nghe hiểu, đọc hiểu, ghi chép và trích xuất thông tin toán học cơ bản; trình bày, diễn đạt, thảo luận, phản biện ý tưởng toán học tương tác với người khác; sử dụng kết hợp ngôn ngữ toán học và ngôn ngữ tự nhiên."
    },
    {
      code: "CCPT",
      name: "Năng lực Sử dụng Công cụ, Phương tiện học Toán",
      description: "Nhận biết tên gọi, tác dụng, quy cách sử dụng công cụ (thước, compa, êke, thước đo góc, mô hình hình học...); sử dụng thành thạo máy tính cầm tay, phần mềm vẽ hình (GeoGebra, Desmos...) và phương tiện công nghệ hỗ trợ học tập."
    }
  ],

  // KHUNG NĂNG LỰC AI CẤP THCS (Theo Quyết định số 2422/QĐ-BGDĐT)
  aiCompetencies: [
    {
      code: "AI_1",
      name: "Hiểu biết và Nhận thức về AI",
      description: "Nhận biết được vai trò, ứng dụng cơ bản của AI trong học tập môn Toán và đời sống; phân biệt được giữa trí tuệ nhân tạo và các công cụ phần mềm thông thường."
    },
    {
      code: "AI_2",
      name: "Sử dụng Công cụ AI trong Học tập Toán",
      description: "Biết sử dụng công cụ AI (Gemini, ChatGPT, NotebookLM...) để tra cứu khái niệm, gợi ý hướng giải quyết bài toán, kiểm tra các bước biến đổi toán học, trực quan hóa dữ liệu."
    },
    {
      code: "AI_3",
      name: "Đánh giá, Phản biện và Kiểm chứng kết quả AI",
      description: "Có kĩ năng đối chiếu, phát hiện lỗi sai hoặc 'ảo giác' (hallucination) trong câu trả lời của AI; kiểm chứng tính chính xác của lời giải AI bằng lập luận toán học độc lập."
    },
    {
      code: "AI_4",
      name: "Đạo đức, Liêm chính và An toàn khi dùng AI",
      description: "Sử dụng AI có trách nhiệm; tuân thủ liêm chính học thuật (không sao chép nguyên văn đáp án AI mà không tư duy); bảo vệ an toàn thông tin cá nhân trên môi trường số."
    }
  ],

  // KHUNG NĂNG LỰC SỐ CẤP THCS (Theo Thông tư số 02/2025/TT-BGDĐT)
  digitalCompetencies: [
    {
      code: "DIGI_1",
      name: "Vận hành Thiết bị & Phần mềm Toán học số",
      description: "Sử dụng thành thạo máy tính cầm tay thông minh, phần mềm hình học động (GeoGebra, Cabri, Desmos), bảng tính điện tử (Excel/Sheets) để mô phỏng và tính toán."
    },
    {
      code: "DIGI_2",
      name: "Khai thác, Quản trị Dữ liệu & Thông tin số",
      description: "Tìm kiếm, chọn lọc, trích xuất và xử lý thông tin, số liệu thống kê toán học từ các nguồn Internet uy tín phục vụ bài học và dự án học tập."
    },
    {
      code: "DIGI_3",
      name: "Giao tiếp, Hợp tác trong Môi trường số",
      description: "Chia sẻ sản phẩm học tập, bài giải toán, poster toán học trên nền tảng trực tuyến (Padlet, Google Classroom, Zalo nhóm, Canva...); làm việc nhóm qua mạng."
    },
    {
      code: "DIGI_4",
      name: "An toàn số & Văn hóa ứng xử không gian mạng",
      description: "Tuân thủ quy tắc bảo mật dữ liệu học tập, tôn trọng bản quyền học liệu số, ứng xử văn minh trong tương tác học tập trực tuyến."
    }
  ],

  // 5 PHẨM CHẤT CHỦ YẾU (Theo Chương trình GDPT 2018) + GIÁO DỤC HÒA NHẬP
  qualities: [
    { code: "PC_1", name: "Yêu nước", description: "Tự hào về các thành tựu toán học và ứng dụng của toán học trong xây dựng, phát triển đất nước." },
    { code: "PC_2", name: "Nhân ái", description: "Tôn trọng sự khác biệt trong tư duy và tốc độ tiếp thu của bạn bè; sẵn sàng hỗ trợ, hợp tác giúp đỡ bạn học yếu, học sinh hòa nhập." },
    { code: "PC_3", name: "Chăm chỉ", description: "Kiên trì thực hiện nhiệm vụ học tập, vượt qua khó khăn khi giải các bài toán tư duy, tích cực tìm tòi các cách giải khác nhau." },
    { code: "PC_4", name: "Trung thực", description: "Thật thà trong học tập, tự giác làm bài, trung thực khi báo cáo kết quả và tự đánh giá sản phẩm học tập." },
    { code: "PC_5", name: "Trách nhiệm", description: "Có trách nhiệm với nhiệm vụ được phân công trong nhóm; có ý thức bảo quản đồ dùng học tập và thiết bị công nghệ." },
    { code: "PC_HOANHAP", name: "Hỗ trợ Giáo dục Hòa nhập", description: "Điều chỉnh yêu cầu cần đạt, thiết kế câu hỏi gợi mở, bố trí bạn cùng tiến hỗ trợ học sinh khuyết tật/học sinh chậm tiến độ tiếp thu bài học một cách tự tin." }
  ]
};

CURRICULUM_DATA.lessonsBySubject = {
  "nguvan": {
    "6": [
      {
        "chapter": "Ngữ văn (Tập 1)",
        "items": [
          "Bài 1: Tôi và các bạn",
          "Bài 2: Gõ cửa trái tim",
          "Bài 3: Yêu thương và chia sẻ",
          "Bài 4: Quê hương yêu dấu",
          "Bài 5: Những nẻo đường xứ sở",
          "Ôn tập học kì i"
        ]
      },
      {
        "chapter": "Ngữ văn (Tập 2)",
        "items": [
          "Bài 6: Chuyện kể về những người anh hùng",
          "Bài 7: Thế giới cổ tích",
          "Bài 8: Khác biệt và gần gũi",
          "Bài 9: Trái đất - ngôi nhà chung",
          "Bài 10: Cuốn sách tôi yêu",
          "Ôn tập học kì ii"
        ]
      }
    ],
    "7": [
      {
        "chapter": "Ngữ văn (Tập 1)",
        "items": [
          "Bài 1: Bầu trời tuổi thơ",
          "Bài 2: Khúc nhạc tâm hồn",
          "Bài 3: Cội nguồn yêu thương",
          "Bài 4: Giai điệu đất nước",
          "Bài 5: Màu sắc trăm miền",
          "Ôn tập học kì i"
        ]
      },
      {
        "chapter": "Ngữ văn (Tập 2)",
        "items": [
          "Bài 6: Bài học cuộc sống",
          "Bài 7: Thế giới viễn tưởng",
          "Bài 8: Trải nghiệm để trưởng thành",
          "Bài 9: Hòa điệu với tự nhiên",
          "Bài 10: Trang sách và cuộc sống",
          "Ôn tập học kì ii"
        ]
      }
    ],
    "8": [
      {
        "chapter": "Ngữ văn (Tập 1)",
        "items": [
          "Bài 1: Câu chuyện của lịch sử",
          "Bài 2: Vẻ đẹp cổ điển",
          "Bài 3: Lời sông núi",
          "Bài 4: Tiếng cười trào phúng trong thơ",
          "Bài 5: Những câu chuyện hài",
          "Ôn tập học kì i"
        ]
      },
      {
        "chapter": "Ngữ văn (Tập 2)",
        "items": [
          "Bài 6: Chân dung cuộc sống",
          "Bài 7: Tin yêu và ước vọng",
          "Bài 8: Nhà văn và trang viết",
          "Bài 9: Hôm nay và ngày mai",
          "Bài 10: Sách - người bạn đồng hành",
          "Ôn tập học kì ii"
        ]
      }
    ],
    "9": [
      {
        "chapter": "Ngữ văn (Tập 1)",
        "items": [
          "Bài 1: Thế giới kì ảo",
          "Bài 2: Những cung bậc tâm trạng",
          "Bài 3: Hồn nước nằm trong tiếng mẹ cha",
          "Bài 4: Khám phá vẻ đẹp văn chương",
          "Bài 5: Đối diện nỗi đau"
        ]
      },
      {
        "chapter": "Ngữ văn (Tập 2)",
        "items": [
          "Bài 6: Giải mã những bí mật",
          "Bài 7: Hồn thơ muốn điệu",
          "Bài 8: Tiếng nói của lương tri",
          "Bài 9: Đi và suy ngẫm",
          "Bài 10: Văn học - Lịch sử tâm hồn"
        ]
      }
    ]
  },
  "khtn": {
    "6": [
      {
        "chapter": "Chương I: Mở đầu về khoa học tự nhiên",
        "items": [
          "Bài 1: Giới thiệu về Khoa học tự nhiên",
          "Bài 2: An toàn trong phòng thực hành",
          "Bài 3: Sử dụng kính lúp",
          "Bài 4: Sử dụng kính hiển vi quang học",
          "Bài 5: Đo chiều dài",
          "Bài 6: Đo khối lượng",
          "Bài 7: Đo thời gian",
          "Bài 8: Đo nhiệt độ"
        ]
      },
      {
        "chapter": "Chương II: Chất quanh ta",
        "items": [
          "Bài 9: Sự đa dạng của chất",
          "Bài 10: Các thể của chất và sự chuyển thể",
          "Bài 11: Oxygen. Không khí"
        ]
      },
      {
        "chapter": "Chương III: Một số vật liệu, nguyên liệu, nhiên liệu, lương thực - thực phẩm thông dụng",
        "items": [
          "Bài 12: Một số vật liệu",
          "Bài 13: Một số nguyên liệu",
          "Bài 14: Một số nhiên liệu",
          "Bài 15: Một số lương thực, thực phẩm"
        ]
      },
      {
        "chapter": "Chương V: Hỗn hợp. tách chất ra khỏi hỗn hợp",
        "items": [
          "Bài 16: Hỗn hợp các chất",
          "Bài 17: Tách các chất khỏi hỗn hợp"
        ]
      },
      {
        "chapter": "Chương V: Tế bào",
        "items": [
          "Bài 18: Tế bào - Đơn vị cơ bản của sự sống",
          "Bài 19: Cấu tạo và chức năng các thành phần của tế bào",
          "Bài 20: Sự lớn lên và sinh sản của tế bào",
          "Bài 21: Thực hành: Quan sát và phân biệt một số tế bào"
        ]
      },
      {
        "chapter": "Chương VI: Từ tế bào đến cơ thể",
        "items": [
          "Bài 22: Cơ thể sinh vật",
          "Bài 23: Tổ chức cơ thể đa bào",
          "Bài 24: Thực hành: Quan sát và mô tả cơ thể đơn bào, cơ thể đa bào"
        ]
      },
      {
        "chapter": "Chương VII: Đa dạng thế giới sống",
        "items": [
          "Bài 25: Hệ thống phân loại sinh vật",
          "Bài 26: Khóa lưỡng phân",
          "Bài 27: Vi khuẩn",
          "Bài 28: Thực hành: Làm sữa chua và quan sát vi khuẩn",
          "Bài 29: Virus",
          "Bài 30: Nguyên sinh vật",
          "Bài 31: Thực hành: Quan sát nguyên sinh vật",
          "Bài 32: Nấm",
          "Bài 33: Thực hành: Quan sát các loại nấm",
          "Bài 34: Thực vật",
          "Bài 35: Thực hành: Quan sát và phân biệt một số nhóm thực vật",
          "Bài 36: Động vật",
          "Bài 37: Thực hành: Quan sát và nhận biết một số nhóm động vật ngoài thiên nhiên",
          "Bài 38: Đa dạng sinh học",
          "Bài 39: Tìm hiểu sinh vật ngoài thiên nhiên"
        ]
      },
      {
        "chapter": "Chương VIII: Lực trong đời sống",
        "items": [
          "Bài 40: Lực là gì?",
          "Bài 41: Biểu diễn lực",
          "Bài 42: Biến dạng của lò xo",
          "Bài 44: Lực ma sát",
          "Bài 45: Lực cản của nước"
        ]
      },
      {
        "chapter": "Chương IX: Năng lượng",
        "items": [
          "Bài 46: Năng lượng và truyền nưng lượng",
          "Bài 47: Một số dạng năng lượng",
          "Bài 48: Sự chuyển hóa năng lượng",
          "Bài 49: Năng lượng hao phí",
          "Bài 50: Năng lượng tái tạo",
          "Bài 51: Tiết kiệm năng lượng"
        ]
      },
      {
        "chapter": "Chương X: Trái đất và bầu trời",
        "items": [
          "Bài 52: Chuyển động nhìn thấy của Mặt Trời. Thiên thể",
          "Bài 52: Mặt Trăng",
          "Bài 54: Hệ Mặt Trời",
          "Bài 55: Ngân Hà"
        ]
      }
    ],
    "7": [
      {
        "chapter": "Khoa học tự nhiên",
        "items": [
          "Bài 1: Phương pháp và kĩ năng học tập môn Khoa học tự nhiên"
        ]
      },
      {
        "chapter": "Chương I: Nguyên tử sơ lược về bảng tuần hoàn các nguyên tố hoá học",
        "items": [
          "Bài 2: Nguyên tử",
          "Bài 3: Nguyên tố hoá học",
          "Bài 4: Sơ lược về bảng tuần hoàn các nguyên tố hoá học"
        ]
      },
      {
        "chapter": "Chương II: Phân tử. liên kết hóa học",
        "items": [
          "Bài 5: Phân tử – Đơn chất – Hợp chất",
          "Bài 6: Giới thiệu về liên kết hoá học",
          "Bài 7: Hoá trị và công thức hoá học"
        ]
      },
      {
        "chapter": "Chương III: Tốc độ",
        "items": [
          "Bài 8: Tốc độ chuyển động",
          "Bài 9: Đo tốc độ",
          "Bài 10: Đồ thị quãng đường – thời gian",
          "Bài 11: Thảo luận về ảnh hưởng của tốc độ trong an toàn giao thông"
        ]
      },
      {
        "chapter": "Chương IV: Âm thanh",
        "items": [
          "Bài 12: Sóng âm",
          "Bài 13: Độ to và độ cao của âm",
          "Bài 14: Phản xạ âm, chống ô nhiễm tiếng ồn"
        ]
      },
      {
        "chapter": "Chương V: Ánh sáng",
        "items": [
          "Bài 15: Năng lượng ánh sáng. Tia sáng, vùng tối",
          "Bài 16: Sự phản xạ ánh sáng",
          "Bài 17: Ảnh của vật qua gương phẳng"
        ]
      },
      {
        "chapter": "Chương VI: TỪ",
        "items": [
          "Bài 18: Nam châm",
          "Bài 19: Từ trường",
          "Bài 20: Chế tạo nam châm điện đơn giản"
        ]
      },
      {
        "chapter": "Chương VII: Trao đổi chất và chuyển hoá năng lượng ở sinh vật",
        "items": [
          "Bài 21: Khái quát về trao đổi chất và chuyển hoá năng lượng",
          "Bài 22: Quang hợp ở thực vật",
          "Bài 23: Một số yếu tố ảnh hưởng đến quang hợp",
          "Bài 24: Thực hành: Chứng minh quang hợp ở cây xanh",
          "Bài 25: Hô hấp tế bào",
          "Bài 26: Một số yếu tố ảnh hưởng đến hô hấp tế bào",
          "Bài 27: Thực hành: Hô hấp ở thực vật",
          "Bài 28: Trao đổi khí ở sinh vật",
          "Bài 29: Vai trò của nước và chất dinh dưỡng đối với sinh vật",
          "Bài 30: Trao đổi nước và chất dinh dưỡng ở thực vật",
          "Bài 31: Trao đổi nước và chất dinh dưỡng ở động vật",
          "Bài 32: Thực hành: Chứng minh thân vận chuyển nước và lá thoát hơi nước"
        ]
      },
      {
        "chapter": "Chương VIII: Cảm ứng ở sinh vật",
        "items": [
          "Bài 33: Cảm ứng ở sinh vật và tập tính ở động vật",
          "Bài 34: Vận dụng hiện tượng cảm ứng ở sinh vật vào thực tiễn",
          "Bài 35: Thực hành: Cảm ứng ở sinh vật"
        ]
      },
      {
        "chapter": "Chương IX: Sinh trưởng và phát triển ở sinh vật",
        "items": [
          "Bài 36: Khái quát về sinh trưởng và phát triển ở sinh vật",
          "Bài 37: Ứng dụng sinh trưởng và phát triển ở sinh vật vào thực tiễn",
          "Bài 38: Thực hành: Quan sát, mô tả sự sinh trưởng và phát triển ở một số sinh vật"
        ]
      },
      {
        "chapter": "Chương X: Sinh sản ở sinh vật",
        "items": [
          "Bài 39: Sinh sản vô tính ở sinh vật",
          "Bài 40: Sinh sản hữu tính ở sinh vật",
          "Bài 41: Một số yếu tố ảnh hưởng và điều hoà, điều khiển sinh sản ở sinh vật",
          "Bài 42: Cơ thể sinh vật là một thể thống nhất"
        ]
      }
    ],
    "8": [
      {
        "chapter": "Khoa học tự nhiên",
        "items": [
          "Bài 1: Sử dụng một số hoá chất, thiết bị cơ bản trong phòng thí nghiệm"
        ]
      },
      {
        "chapter": "Chương I: Phản ứng hoá học",
        "items": [
          "Bài 2: Phản ứng hoá học",
          "Bài 3: Mol và tỉ khối chất khí",
          "Bài 4: Dung dịch và nồng độ",
          "Bài 5: Định luật bảo toàn khối lượng và phương trình hoá học",
          "Bài 6: Tính theo phương trình hoá học",
          "Bài 7: Tốc độ phản ứng và chất xúc tác"
        ]
      },
      {
        "chapter": "Chương II: Một số hợp chất thông dụng",
        "items": [
          "Bài 8: Acid",
          "Bài 9: Base. Thang pH",
          "Bài 10: Oxide",
          "Bài 11: Muối",
          "Bài 12: Phân bón hoá học"
        ]
      },
      {
        "chapter": "Chương III: Khối lượng riêng và áp suất",
        "items": [
          "Bài 13: Khối lượng riêng",
          "Bài 14: Thực hành xác định khối lượng riêng",
          "Bài 15: Áp suất trên một bề mặt",
          "Bài 16: Áp suất chất lỏng. Áp suất khí quyển",
          "Bài 17: Lực đẩy Archimedes"
        ]
      },
      {
        "chapter": "Chương IV: Tác dụng làm quay của lực",
        "items": [
          "Bài 18: Tác dụng làm quay của lực. Moment lực",
          "Bài 19: Đòn bẩy và ứng dụng"
        ]
      },
      {
        "chapter": "Chương V: Điện",
        "items": [
          "Bài 20: Hiện tượng nhiễm điện do cọ xát",
          "Bài 21: Dòng điện, nguồn điện",
          "Bài 22: Mạch điện đơn giản",
          "Bài 23: Tác dụng của dòng điện",
          "Bài 24: Cường độ dòng điện và hiệu điện thế",
          "Bài 25: Thực hành đo cường độ dòng điện và hiệu điện thế"
        ]
      },
      {
        "chapter": "Chương VI: Nhiệt",
        "items": [
          "Bài 26: Năng lượng nhiệt và nội năng",
          "Bài 27: Thực hành đo năng lượng nhiệt bằng joulemeter",
          "Bài 28: Sự truyền nhiệt",
          "Bài 29: Sự nở vì nhiệt"
        ]
      },
      {
        "chapter": "Chương VII: Sinh học cơ thể người",
        "items": [
          "Bài 30: Khái quát về cơ thể người",
          "Bài 31: Hệ vận động ở người",
          "Bài 32: Dinh dưỡng và tiêu hoá ở người",
          "Bài 33: Máu và hệ tuần hoàn của cơ thể người",
          "Bài 34: Hệ hô hấp ở người",
          "Bài 35: Hệ bài tiết ở người",
          "Bài 36: Điều hoà môi trường trong của cơ thể người",
          "Bài 37: Hệ thần kinh và các giác quan ở người",
          "Bài 38: Hệ nội tiết ở người",
          "Bài 39: Da và điều hoà thân nhiệt ở người",
          "Bài 40: Sinh sản ở người"
        ]
      },
      {
        "chapter": "Chương VIII: Sinh vật và môi trường",
        "items": [
          "Bài 41: Môi trường và các nhân tố sinh thái",
          "Bài 42: Quần thể sinh vật",
          "Bài 43: Quần xã sinh vật",
          "Bài 44: Hệ sinh thái",
          "Bài 45: Sinh quyển",
          "Bài 46: Cân bằng tự nhiên",
          "Bài 47: Bảo vệ môi trường"
        ]
      }
    ],
    "9": [
      {
        "chapter": "Chương 1: Năng lượng cơ học",
        "items": [
          "Bài 2: Động năng. Thế năng",
          "Bài 3: Cơ năng",
          "Bài 4: Công và công suất"
        ]
      },
      {
        "chapter": "Chương 2: Ánh sáng",
        "items": [
          "Bài 5: Khúc xạ ánh sáng",
          "Bài 6: Phản xạ toàn phần",
          "Bài 7: Lăng kính",
          "Bài 8: Thấu kính",
          "Bài 9: Thực hành đo tiêu cự của thấu kính hội tụ",
          "Bài 10: Kính lúp. Bài tập thấu kính"
        ]
      },
      {
        "chapter": "Chương 3: Điện",
        "items": [
          "Bài 11: Điện trở. Định luật Ohm",
          "Bài 12: Đoạn mạch nối tiếp, song song",
          "Bài 13: Năng lượng của dòng điện và công suất điện"
        ]
      },
      {
        "chapter": "Chương 4: Điện từ",
        "items": [
          "Bài 14: Cảm ứng điện từ. Nguyên tắc tạo ra dòng điện xoay chiều",
          "Bài 15: Tác dụng của dòng điện xoay chiều"
        ]
      },
      {
        "chapter": "Chương 5: Năng lượng với cuộc sống",
        "items": [
          "Bài 16: Vòng năng lượng trên Trái Đất. Năng lượng hóa thạch",
          "Bài 17: Một số dạng năng lượng tái tạo"
        ]
      },
      {
        "chapter": "Chương 6: Kim loại. Sự khác nhau cơ bản giữa phi kim và kim loại",
        "items": [
          "Bài 18: Tính chất chung của kim loại",
          "Bài 19: Dãy hoạt động hóa học",
          "Bài 20: Tách kim loại và việc sử dụng hợp kim",
          "Bài 21: Sự khác nhau cơ bản giữa phi kim và kim loại"
        ]
      },
      {
        "chapter": "Chương 7: Giới thiệu hợp chất hữu cơ. Hydrocarbon và nguồn nhiên liệu",
        "items": [
          "Bài 22: Giới thiệu về hợp chất hữu cơ",
          "Bài 23: Alkane",
          "Bài 24: Alkene",
          "Bài 25: Nguồn nhiên liệu"
        ]
      },
      {
        "chapter": "Chương 8: Ethylic alcohol và Acetic acid",
        "items": [
          "Bài 26: Ethylic alcohol",
          "Bài 27: Acetic acid"
        ]
      },
      {
        "chapter": "Chương 9: Lipid. Carbohydrate. Protein. Polymer",
        "items": [
          "Bài 28: Lipid",
          "Bài 29: Carbohydrate glucose và saccharose",
          "Bài 30: Tinh bột và cellulose",
          "Bài 31: Protein",
          "Bài 32: Polymer"
        ]
      },
      {
        "chapter": "Chương 10: Khai thác tài nguyên từ vỏ Trái Đất",
        "items": [
          "Bài 33: Sơ lược về hóa học vỏ Trái Đất và khai thác tài nguyên từ vỏ Trái Đất",
          "Bài 34: Khai thác đá vôi. Công nghiệp silicate",
          "Bài 35: Khai thác nhiên liệu hóa thạch. Nguồn carbon. Chu trình carbon và sự ấm lên toàn cầu"
        ]
      },
      {
        "chapter": "Chương 11: Di truyền học Menđel. Cơ sở phân tử của hiện tượng di truyền",
        "items": [
          "Bài 36: Khái quát về di truyền học",
          "Bài 37: Các quy luật di truyền của Mendel",
          "Bài 38: Nucleic acid và gene",
          "Bài 39: Tái bản DNA và phiên mã tạo ra RNA",
          "Bài 40: Dịch mã và mối quan hệ từ gene đến tính trạng",
          "Bài 41: Đột biến gene"
        ]
      },
      {
        "chapter": "Chương 12: Di truyền nhiễm sắc thể",
        "items": [
          "Bài 42: Di truyền nhiễm sắc thể",
          "Bài 43: Nguyên phân và giảm phân",
          "Bài 44: Nhiễm sắc thể giới tính và cơ chế xác định giới tính",
          "Bài 45: Di truyền liên kết",
          "Bài 46: Đột biến nhiễm sắc thể"
        ]
      },
      {
        "chapter": "Chương 13: Di truyền học với con người và đời sống",
        "items": [
          "Bài 47: Di truyền học với con người",
          "Bài 48: Ứng dụng công nghệ di truyền vào đời sống"
        ]
      },
      {
        "chapter": "Chương 14: Tiến hóa",
        "items": [
          "Bài 49: Khái niệm tiến hóa và các hình thức chọn lọc",
          "Bài 50: Cơ chế tiến hóa",
          "Bài 51: Sự phát sinh và phát triển của sự sống trên Trái Đất"
        ]
      }
    ]
  },
  "lichsudialy": {
    "6": [
      {
        "chapter": "Chương 1: Vì sao phải học lịch sử?",
        "items": [
          "Chương 1: Vì sao phải học lịch sử?"
        ]
      },
      {
        "chapter": "Chương 2: Xã hội nguyên thủy",
        "items": [
          "Chương 2: Xã hội nguyên thủy"
        ]
      },
      {
        "chapter": "Chương 3: Xã hội cổ đại",
        "items": [
          "Chương 3: Xã hội cổ đại"
        ]
      },
      {
        "chapter": "Chương 4: Đông nam á từ những thế kỉ tiếp giáp đầu công nguyên đến thế kỉ x",
        "items": [
          "Chương 4: Đông nam á từ những thế kỉ tiếp giáp đầu công nguyên đến thế kỉ x"
        ]
      },
      {
        "chapter": "Chương 5: Việt nam từ khoảng thế kỉ vii trước công nguyên đến đầu thế kỉ x",
        "items": [
          "Chương 5: Việt nam từ khoảng thế kỉ vii trước công nguyên đến đầu thế kỉ x"
        ]
      },
      {
        "chapter": "Phần: địa lí",
        "items": [
          "Bài mở đầu"
        ]
      },
      {
        "chapter": "Chương 1: Bản đồ - phương tiện thể hiện bề mặt trái đất",
        "items": [
          "Chương 1: Bản đồ - phương tiện thể hiện bề mặt trái đất"
        ]
      },
      {
        "chapter": "Chương 2: Trái đất - hành tinh của hệ mặt trời",
        "items": [
          "Chương 2: Trái đất - hành tinh của hệ mặt trời"
        ]
      },
      {
        "chapter": "Chương 3: Cấu tạo của trái đất. vỏ trái đất",
        "items": [
          "Chương 3: Cấu tạo của trái đất. vỏ trái đất"
        ]
      },
      {
        "chapter": "Chương 4: Khí hậu và biến đổi khí hậu",
        "items": [
          "Chương 4: Khí hậu và biến đổi khí hậu"
        ]
      },
      {
        "chapter": "Chương 5: Nước trên trái đất",
        "items": [
          "Chương 5: Nước trên trái đất"
        ]
      },
      {
        "chapter": "Chương 6: Đất và sinh vật trên trái đất",
        "items": [
          "Chương 6: Đất và sinh vật trên trái đất"
        ]
      },
      {
        "chapter": "Chương 7: Con người và thiên nhiên",
        "items": [
          "Chương 7: Con người và thiên nhiên"
        ]
      }
    ],
    "7": [
      {
        "chapter": "Chương 1: Tây Âu từ thế kỉ V đến nửa đầu thế kỉ XVI",
        "items": [
          "Chương 1: Tây Âu từ thế kỉ V đến nửa đầu thế kỉ XVI"
        ]
      },
      {
        "chapter": "Chương 2: Trung Quốc và Ấn Độ thời trung đại",
        "items": [
          "Chương 2: Trung Quốc và Ấn Độ thời trung đại"
        ]
      },
      {
        "chapter": "Chương 3: Đông Nam Á từ nửa sau thế kỉ X đến nửa đầu thế kỉ XVI",
        "items": [
          "Chương 3: Đông Nam Á từ nửa sau thế kỉ X đến nửa đầu thế kỉ XVI"
        ]
      },
      {
        "chapter": "Chương 4: Đất nước dưới thời các vương triều Ngô – Đinh – Tiền Lê (939 – 1009)",
        "items": [
          "Chương 4: Đất nước dưới thời các vương triều Ngô – Đinh – Tiền Lê (939 – 1009)"
        ]
      },
      {
        "chapter": "Chương 5: Đại Việt thời Lý – Trần – Hồ (1009 – 1407)",
        "items": [
          "Chương 5: Đại Việt thời Lý – Trần – Hồ (1009 – 1407)"
        ]
      },
      {
        "chapter": "Chương 6: Khởi nghĩa Lam Sơn và Đại Việt thời Lê sơ (1418 – 1527)",
        "items": [
          "Chương 6: Khởi nghĩa Lam Sơn và Đại Việt thời Lê sơ (1418 – 1527)"
        ]
      },
      {
        "chapter": "Chương 7: Vùng đất phía Nam Việt Nam từ đầu thế kỉ X đến đầu thế kỉ XVI",
        "items": [
          "Chương 7: Vùng đất phía Nam Việt Nam từ đầu thế kỉ X đến đầu thế kỉ XVI"
        ]
      },
      {
        "chapter": "Chương 1: Châu Âu",
        "items": [
          "Chương 1: Châu Âu"
        ]
      },
      {
        "chapter": "Chương 2: Châu Á",
        "items": [
          "Chương 2: Châu Á"
        ]
      },
      {
        "chapter": "Chương 3: Châu Phi",
        "items": [
          "Chương 3: Châu Phi"
        ]
      },
      {
        "chapter": "Chương 4: Châu Mỹ",
        "items": [
          "Chương 4: Châu Mỹ"
        ]
      },
      {
        "chapter": "Chương 5: Châu Đại Dương và châu Nam Cực",
        "items": [
          "Chương 5: Châu Đại Dương và châu Nam Cực"
        ]
      },
      {
        "chapter": "Chủ đề chung 1 Các cuộc đại phát kiến địa lí",
        "items": [
          "Chủ đề chung 1 Các cuộc đại phát kiến địa lí"
        ]
      },
      {
        "chapter": "Chủ đề chung 2 Đô thị: Lịch sử và hiện tại",
        "items": [
          "Chủ đề chung 2 Đô thị: Lịch sử và hiện tại"
        ]
      }
    ],
    "8": [
      {
        "chapter": "Chương 1: Châu âu và bắc mỹ từ nửa sau thế kỉ xvi đến thế kỉ xviii",
        "items": [
          "Chương 1: Châu âu và bắc mỹ từ nửa sau thế kỉ xvi đến thế kỉ xviii"
        ]
      },
      {
        "chapter": "Chương 2: Đông nam á từ nửa sau thế kỉ xvi đến giữa thế kỉ xix",
        "items": [
          "Chương 2: Đông nam á từ nửa sau thế kỉ xvi đến giữa thế kỉ xix"
        ]
      },
      {
        "chapter": "Chương 3: Việt nam từ đầu thế kỉ xvi đến thế kỉ xviii",
        "items": [
          "Chương 3: Việt nam từ đầu thế kỉ xvi đến thế kỉ xviii"
        ]
      },
      {
        "chapter": "Chương 4: Châu âu và nước mỹ từ cuối thế kỉ xviii đến đầu thế kỉ xx",
        "items": [
          "Chương 4: Châu âu và nước mỹ từ cuối thế kỉ xviii đến đầu thế kỉ xx"
        ]
      },
      {
        "chapter": "Chương 5: Sự phát triển của khoa học, kĩ thuật, văn học, nghệ thuật trong các thế kỉ xviii - xix",
        "items": [
          "Chương 5: Sự phát triển của khoa học, kĩ thuật, văn học, nghệ thuật trong các thế kỉ xviii - xix"
        ]
      },
      {
        "chapter": "Chương 6: Châu á từ nửa sau thế kỉ xix đến đầu thế kỉ xx",
        "items": [
          "Chương 6: Châu á từ nửa sau thế kỉ xix đến đầu thế kỉ xx"
        ]
      },
      {
        "chapter": "Chương 7: Việt nam từ thế kỉ xix đến đầu thế kỉ xx",
        "items": [
          "Chương 7: Việt nam từ thế kỉ xix đến đầu thế kỉ xx"
        ]
      },
      {
        "chapter": "Chương 1: Vị trí địa lí và phạm vi lãnh thổ, địa hình và khoáng sản việt nam",
        "items": [
          "Chương 1: Vị trí địa lí và phạm vi lãnh thổ, địa hình và khoáng sản việt nam"
        ]
      },
      {
        "chapter": "Chương 2: Khí hậu và thủy văn việt nam",
        "items": [
          "Chương 2: Khí hậu và thủy văn việt nam"
        ]
      },
      {
        "chapter": "Chương 3: Thổ nhưỡng và sinh vật việt nam",
        "items": [
          "Chương 3: Thổ nhưỡng và sinh vật việt nam"
        ]
      },
      {
        "chapter": "Chương 4: Biển đảo việt nam",
        "items": [
          "Chương 4: Biển đảo việt nam"
        ]
      },
      {
        "chapter": "Chủ đề chung 1 VĂN MINH CHÂU THỔ SÔNG HỒNG VÀ SÔNG CỬU LONG",
        "items": [
          "Chủ đề chung 1 VĂN MINH CHÂU THỔ SÔNG HỒNG VÀ SÔNG CỬU LONG"
        ]
      },
      {
        "chapter": "Chủ đề chung 2 BẢO VỆ CHỦ QUYỀN, CÁC QUYỀN VÀ LỢI ÍCH HỢP PHÁP CỦA VIỆT NAM Ở BIỂN ĐÔNG",
        "items": [
          "Chủ đề chung 2 BẢO VỆ CHỦ QUYỀN, CÁC QUYỀN VÀ LỢI ÍCH HỢP PHÁP CỦA VIỆT NAM Ở BIỂN ĐÔNG"
        ]
      }
    ],
    "9": [
      {
        "chapter": "Chương 1: Thế giới từ năm 1918 đến năm 1945",
        "items": [
          "Bài 1: Nước Nga và Liên Xô từ năm 1918 đến năm 1945",
          "Bài 2: Châu Âu và nước Mỹ từ năm 1918 đến năm 1945",
          "Bài 3: Châu Á từ năm 1918 đến 1945",
          "Bài 4: Chiến tranh thế giới thứ hai (1939-1945)"
        ]
      },
      {
        "chapter": "Chương 2: Việt Nam từ năm 1918 đến năm 1945",
        "items": [
          "Bài 5: Phong trào dân tộc dân chủ trong những năm 1918-1930",
          "Bài 6: Hoạt động của Nguyễn Ái Quốc và sự thành lập Đảng Cộng sản Việt Nam",
          "Bài 7: Phong trào cách mạng Việt Nam thời kì 1930-1939",
          "Bài 8: Cách mạng tháng Tám năm 1945"
        ]
      },
      {
        "chapter": "Chương 3: Thế giới từ năm 1945 đến năm 1991",
        "items": [
          "Bài 9: Chiến tranh lạnh(1947-1989)",
          "Bài 10: Liên Xô và Đông Âu từ năm 1945 đến năm 1991",
          "Bài 11: Nước Mỹ và Tây Âu từ năm 1945 đến năm 1991",
          "Bài 12: Khu vực Mỹ La-tinh và châu Á từ năm 1945 đến năm 1991"
        ]
      },
      {
        "chapter": "Chương 4: Việt Nam từ năm 1945 đến năm 1991",
        "items": [
          "Bài 13: Việt Nam trong năm đầu sau Cách mạng tháng Tám năm 1945",
          "Bài 14: Việt Nam kháng chiến chống thực dân Pháp xâm lược giai đoạn 1946 – 1950",
          "Bài 15: Việt Nam kháng chiến chống Pháp xâm lược gai đoạn 1951-1954",
          "Bài 16: Việt Nam kháng chiến chống Mỹ, cứu nước, thống nhất đất nước giai đoạn 1954 – 1965",
          "Bài 17: Việt Nam kháng chiến chống Mỹ, cứu nước, thống nhất đất nước giai đoạn 1965 – 1975",
          "Bài 18: Việt Nam kháng chiến chống Mỹ, cứu nước, thống nhất đất nước giai đoạn 1954 – 1965"
        ]
      },
      {
        "chapter": "Chương 5: Thế giới từ năm 1991 đến nay",
        "items": [
          "Bài 19: Trật tự thế giới mới từ năm 1991 đến nay. Liên Bang Nga và nước Mỹ từ năm 1991 đến nay",
          "Bài 20: Châu Á từ năm 1991 đến nay"
        ]
      },
      {
        "chapter": "Chương 6: Việt Nam từ năm 1991 đến nay",
        "items": [
          "Bài 21: Việt Nam từ năm 1991 đến nay"
        ]
      },
      {
        "chapter": "Chương 7: Cách mạng khoa học – kĩ thuật và xu thế toàn cầu hóa",
        "items": [
          "Bài 22: Cách mạng khoa học – kĩ thuật và xu thế toàn cầu hóa"
        ]
      },
      {
        "chapter": "Chương 1: Địa lý dân cư Việt Nam",
        "items": [
          "Bài 1: Dân tộc và dân số",
          "Bài 2: Phân bố dân cư và các loại hình quần cư",
          "Bài 3: Thực hành: Tìm hiểu vấn đề việc làm ở địa phương và phân hoá thu nhập theo vùng"
        ]
      },
      {
        "chapter": "Chương 2: Địa lý các ngành kinh tế",
        "items": [
          "Bài 10: Thực hành: Tìm hiểu xu hướng phát triển ngành thương mại, du lịch",
          "Bài 4: Nông nghiệp",
          "Bài 5: Lâm nghiệp và thuỷ sản",
          "Bài 6: Thực hành: Viết báo cáo về một mô hình sản xuất nông nghiệp có hiệu quả",
          "Bài 7: Công nghiệp",
          "Bài 8: Thực hành: Xác định các trung tâm công nghiệp chính ở nước ta",
          "Bài 9: Dịch vụ"
        ]
      },
      {
        "chapter": "Chương 3: Sự phân hóa lãnh thổ",
        "items": [
          "Bài 11: Vùng trung du và miền núi Bắc Bộ",
          "Bài 12: Vùng Đồng bằng Sông Hồng",
          "Bài 13: Thực hành:Tìm hiểu về vùng kinh tế trọng điểm Bắc Bộ",
          "Bài 14: Bắc Trung Bộ",
          "Bài 15: Duyên hải Nam Trung Bộ",
          "Bài 16: Thực hành: Phân tích ảnh hưởng của hạn hán và sa mạc hóa đối với phát triển kinh tế - xã hội ở vùng khô hạn Ninh Thuận – Bình Thuậ",
          "Bài 17: Vùng Tây Nguyên",
          "Bài 18: Vùng Đông Nam Bộ",
          "Bài 19: Thực hành: Tìm hiểu về vùng kinh tế trọng điểm phía Nam",
          "Bài 20: Vùng đồng bằng sông Cửu Long",
          "Bài 21: Thực hành:Tìm hiểu về tác động của biến đổi khí hậu đối với đồng bằng sông Cửu Long",
          "Bài 22: Phát triển tổng hợp kinh tế và bảo vệ tài nguyên,môi trường biển đảo"
        ]
      },
      {
        "chapter": "Chủ đề 1: Đô thị: Lịch sử và Hiện tại",
        "items": [
          "Chủ đề 1: Đô thị: Lịch sử và Hiện tại"
        ]
      },
      {
        "chapter": "Chủ đề 2: Văn minh châu thổ sông Hồng và sông Cửu Long",
        "items": [
          "Chủ đề 2: Văn minh châu thổ sông Hồng và sông Cửu Long"
        ]
      },
      {
        "chapter": "Chủ đề 3: Bảo vệ chủ quyền,các quyền và lợi ích hợp pháp của Việt Nam ở biển Đông(2)",
        "items": [
          "Chủ đề 3: Bảo vệ chủ quyền,các quyền và lợi ích hợp pháp của Việt Nam ở biển Đông(2)"
        ]
      }
    ]
  },
  "gdcd": {
    "6": [
      {
        "chapter": "Giáo dục công dân",
        "items": [
          "Bài 1: Tự hào về truyền thống gia đình, dòng họ",
          "Bài 2: Yêu thương con người",
          "Bài 3: Siêng năng, kiên trì",
          "Bài 4: Tôn trọng sự thật",
          "Bài 5: Tự lập",
          "Bài 6: Tự nhận thức bản thân",
          "Bài 7: Ứng phó với tình huống nguy hiểm",
          "Bài 8: Tiết kiệm",
          "Bài 9: Công dân nước Cộng hòa xã hội chủ nghĩa Việt Nam",
          "Bài 10: Quyền và nghĩa vụ của công dân",
          "Bài 11: Quyền cơ bản của trẻ em",
          "Bài 12: Thực hiện quyền trẻ em"
        ]
      }
    ],
    "7": [
      {
        "chapter": "Giáo dục công dân",
        "items": [
          "Bài 1: Tự hào về truyền thống quê hương",
          "Bài 2: Quan tâm, cảm thông và chia sẻ",
          "Bài 3: Học tập tự giác, tích cực",
          "Bài 4: Giữ chữ tín",
          "Bài 5: Bảo tồn di sản văn hóa",
          "Bài 6: Ứng phó với tâm lý căng thẳng",
          "Bài 7: Phòng, chống bạo lực học đường",
          "Bài 8: Quản lí tiền",
          "Bài 9: Phòng, chống tệ nạn xã hội",
          "Bài 10: Quyền và nghĩa vụ của công dân trong gia đình"
        ]
      }
    ],
    "8": [
      {
        "chapter": "Giáo dục công dân",
        "items": [
          "Bài 1: Tự hào về truyền thống dân tộc việt nam",
          "Bài 2: Tôn trọng sự đa dạng của các dân tộc",
          "Bài 3: Lao động cần cù, sáng tạo",
          "Bài 4: Bảo vệ lẽ phải",
          "Bài 5: Bảo vệ môi trường và tài nguyên thiên nhiên",
          "Bài 6: Xác định mục tiêu cá nhân",
          "Bài 7: Phòng, chống bạo lực gia đình",
          "Bài 8: Lập kế hoạch chi tiêu",
          "Bài 9: Phòng ngừa tai nạn vũ khí, cháy, nổ và các chất độc hại",
          "Bài 10: Quyền và nghĩa vụ lao động của công dân"
        ]
      }
    ],
    "9": [
      {
        "chapter": "Giáo dục công dân",
        "items": [
          "Bài 1: Sống có lí tưởng",
          "Bài 2: Khoan dung",
          "Bài 3: Tích cực tham gia các hoạt động cộng đồng",
          "Bài 4: Khách quan và công bằng",
          "Bài 5: Bảo vệ hòa bình",
          "Bài 6: Quản lí thời gian hiệu quả",
          "Bài 7: Thích ứng với thay đổi",
          "Bài 8: Tiêu dùng thông minh",
          "Bài 9: Vi phạm pháp luật và trách nhiệm pháp lí",
          "Bài 10: Quyền tự do kinh doanh và nghĩa vụ nộp thuế"
        ]
      }
    ]
  },
  "tinhoc": {
    "6": [
      {
        "chapter": "Chủ đề 1: Máy tính và cộng đồng",
        "items": [
          "Bài 1: Thông tin và dữ liệu",
          "Bài 2: Xử lí thông tin",
          "Bài 3: Thông tin trong máy tính"
        ]
      },
      {
        "chapter": "Chủ đề 2: Mạng máy tính và Internet",
        "items": [
          "Bài 4: Mạng máy tính",
          "Bài 5: Internet"
        ]
      },
      {
        "chapter": "Chủ đề 3: Tổ chức lưu trữ, tìm kiếm và trao đổi thông tin",
        "items": [
          "Bài 6: Mạng thông tin toàn cầu",
          "Bài 7: Tìm kiếm thông tin trên Internet",
          "Bài 8: Thư điện tử"
        ]
      },
      {
        "chapter": "Chủ đề 4: Đạo đức, pháp luật và văn hóa trong môi trường số",
        "items": [
          "Bài 9: An toàn thông tin trên Internet"
        ]
      },
      {
        "chapter": "Chủ đề 5: Ứng dụng tin học",
        "items": [
          "Bài 10: Sơ đồ tư duy",
          "Bài 11: Định dạng văn bản",
          "Bài 12: Trình bày thông tin ở dạng bảng",
          "Bài 13: Thực hành: Tìm kiếm và thay thế",
          "Bài 14: Thực hành tổng hợp: Hoàn thiện hồ sơ lưu niệm"
        ]
      },
      {
        "chapter": "Chủ đề 6: Giải quyết vấn đề với sự trợ giúp của máy tính",
        "items": [
          "Bài 15: Thuật toán",
          "Bài 16: Các cấu trúc điều khiển",
          "Bài 17: Chương trình máy tính"
        ]
      }
    ],
    "7": [
      {
        "chapter": "Chủ đề 1: Máy tính và cộng đồng",
        "items": [
          "Bài 1: Thiết bị vào - ra",
          "Bài 2: Phần mềm máy tính",
          "Bài 3: Quản lí dữ liệu trong máy tính"
        ]
      },
      {
        "chapter": "Chủ đề 2: Tổ chức lưu trữ, tìm kiếm và trao đổi thông tin",
        "items": [
          "Bài 4: Mạng xã hội và một số kênh trao đổi thông tin trên Internet"
        ]
      },
      {
        "chapter": "Chủ đề 3: Đạo đức, pháp luật và văn hóa trong môi trường số",
        "items": [
          "Bài 5: Ứng xử trên mạng"
        ]
      },
      {
        "chapter": "Chủ đề 4: Ứng dụng tin học",
        "items": [
          "Bài 6: Làm quen với phần mềm bảng tính",
          "Bài 7: Tính toán tự động trên bảng tính",
          "Bài 8: Công cụ hỗ trợ tính toán",
          "Bài 9: Trình bày bẳng tính",
          "Bài 10: Hoàn thiện bảng tính",
          "Bài 11: Tạo bài trình chiếu",
          "Bài 12: Định dạng đối tượng trên trang chiếu",
          "Bài 13: Thực hành tổng hợp: Hoàn thiện bài trình chiếu"
        ]
      },
      {
        "chapter": "Chủ đề 5: Giải quyết vấn đề với sự giúp đỡ của máy tính",
        "items": [
          "Bài 14: Thuật toán tìm kiếm tuần tự",
          "Bài 15: Thuật toán tìm kiếm nhị phân",
          "Bài 16: Thuật toán sắp xếp"
        ]
      }
    ],
    "8": [
      {
        "chapter": "Chủ đề 1: Máy tính và cộng đồng",
        "items": [
          "Bài 1: Lịch sử phát triển máy tính"
        ]
      },
      {
        "chapter": "Chủ đề 2: Tổ chức lưu trữ, tìm kiếm và trao đổi thông tin",
        "items": [
          "Bài 2: Thông tin trong môi trường số",
          "Bài 3: Thông tin với giải quyết vấn đề"
        ]
      },
      {
        "chapter": "Chủ đề 3: Đạo đức, pháp luật và văn hóa trong môi trường số",
        "items": [
          "Bài 4: Sử dụng công nghệ kĩ thuật số"
        ]
      },
      {
        "chapter": "Chủ đề 4: Ứng dụng tin học",
        "items": [
          "Bài 5: Sử dụng địa chỉ tương đối, tuyệt đối trong công thức",
          "Bài 6: Sắp xếp, lọc dữ liệu",
          "Bài 7: Tạo, chỉnh sửa biểu đồ",
          "Bài 8A: Thêm hình minh họa cho văn bản",
          "Bài 9A: Trình bày văn bản",
          "Bài 10a: Trình bày trang chiếu",
          "Bài 11a: Sử dụng bản mẫu",
          "Bài 8b: Xử lí ảnh",
          "Bài 9b: Ghép ảnh",
          "Bài 10b: Xoay, cắt, thêm chữ vào ảnh",
          "Bài 11b: Tẩy, tạo hiệu ứng cho ảnh"
        ]
      },
      {
        "chapter": "Chủ đề 5: Giải quyết vấn đề với sự trợ giúp của máy tính",
        "items": [
          "Bài 12: Thuật toán, chương trình máy tính",
          "Bài 13: Cấu trúc rẽ nhánh",
          "Bài 14: Cấu trúc lặp",
          "Bài 15: Gỡ lỗi chương trình"
        ]
      },
      {
        "chapter": "Chủ đề 6: Hướng nghiệp với tin học",
        "items": [
          "Bài 16: Tin học và nghề nghiệp"
        ]
      }
    ],
    "9": [
      {
        "chapter": "Tin học",
        "items": [
          "Bài 1: Thế giới kĩ thuật số",
          "Bài 2: Thông tin trong giải quyết vấn đề",
          "Bài 4: Một số vấn đề pháp lí về sử dụng dịch vụ internet",
          "Bài 5: Tìm hiểu phần mềm mô phỏng",
          "Bài 7: Trình bày thông tin trong trao đổi và hợp tác",
          "Bài 9a: Sử dụng công cụ xác thực dữ liệu",
          "Bài 10a: Sử dụng hàm COUNTIF",
          "Bài 11a: Sử dụng hàm SUMIF",
          "Bài 12a: Sử dụng hàm IF",
          "Bài 13a: Hoàn thiện bảng tính quản lí tài chính gia đình",
          "Bài 12b: Hoàn thành việc dựng video",
          "Bài 13b: Biên tập và xuất video",
          "Bài 9b: Các chức năng chính của phần mềm làm video",
          "Bài 10b: Chuẩn bị dữ liệu và dựng video",
          "Bài 14: Giải quyết vấn đề",
          "Bài 15: Bài toán tin học",
          "Bài 17: Tin học và thế giới nghề nghiệp"
        ]
      }
    ]
  },
  "congnghe": {
    "6": [
      {
        "chapter": "Chương I: Nhà ở",
        "items": [
          "Bài 1: Khái quát về nhà ở",
          "Bài 2: Xây dựng nhà ở",
          "Bài 3: Ngôi nhà thông minh",
          "Ôn tập Chương I"
        ]
      },
      {
        "chapter": "Chương II: Bảo quản và chế biến thực phẩm",
        "items": [
          "Bài 4: Thực phẩm và dinh dưỡng",
          "Bài 5: Phương pháp bảo quản và chế biến thực phẩm",
          "Bài 6: Dự án: Bữa ăn kết nối yêu thương",
          "Ôn tập Chương II"
        ]
      },
      {
        "chapter": "Chương III: Trang phục và thời trang",
        "items": [
          "Bài 7: Trang phục trong đời sống",
          "Bài 8: Sử dụng và bảo quản trang phục",
          "Bài 9: Thời trang",
          "Ôn tập Chương III"
        ]
      },
      {
        "chapter": "Chương IV: Đồ dùng điện trong gia đình",
        "items": [
          "Bài 10: Khái quát về đồ dùng điện trong gia đình",
          "Bài 11: Đèn điện",
          "Bài 12: Nồi cơm điện",
          "Bài 13: Bếp hồng ngoại",
          "Bài 14: Dự án: An toàn và tiết kiệm điện trong gia đình",
          "Ôn tập Chương IV"
        ]
      }
    ],
    "7": [
      {
        "chapter": "Chương I: Trồng trọt",
        "items": [
          "Bài 1: Giới thiệu về trồng trọt",
          "Bài 2: Làm đất trồng cây",
          "Bài 3: Gieo trồng, chăm sóc và phòng trừ sâu, bệnh cho cây trồng",
          "Bài 4: Thu hoạch sản phẩm trồng trọt",
          "Bài 5: Nhân giống vô tính cây trồng",
          "Bài 6: Dự án trồng rau an toàn",
          "Ôn tập Chương I"
        ]
      },
      {
        "chapter": "Chương II: Lâm nghiệp",
        "items": [
          "Bài 7: Giới thiệu về rừng",
          "Bài 8: Trồng, chăm sóc và bảo vệ rừng",
          "Ôn tập Chương II"
        ]
      },
      {
        "chapter": "Chương III: Chăn nuôi",
        "items": [
          "Bài 9: Giới thiệu về chăn nuôi",
          "Bài 10: Nuôi dưỡng và chăm sóc vật nuôi",
          "Bài 11: Phòng và trị bệnh cho vật nuôi",
          "Bài 12: Chăn nuôi gà thịt trong nông hộ",
          "Bài 13: Thực hành: Lập kế hoạch nuôi vật nuôi trong gia đình",
          "Ôn tập Chương III"
        ]
      },
      {
        "chapter": "Chương IV: Thủy sản",
        "items": [
          "Bài 14: Giới thiệu về thủy sản",
          "Bài 15: Nuôi cá ao",
          "Bài 16: Thực hành: Lập kế hoạch nuôi cá cảnh",
          "Ôn tập Chương IV"
        ]
      }
    ],
    "8": [
      {
        "chapter": "Chương I: Vẽ kĩ thuật",
        "items": [
          "Bài 1: Một số tiêu chuẩn trình bày bản vẽ kĩ thuật",
          "Bài 2: Hình chiếu vuông góc",
          "Bài 3: Bản vẽ chi tiết",
          "Bài 4: Bản vẽ lắp",
          "Bài 5: Bản vẽ nhà",
          "Ôn tập Chương I"
        ]
      },
      {
        "chapter": "Chương II: Cơ khí",
        "items": [
          "Bài 6: Vật liệu cơ khí",
          "Bài 7: Truyền và biến đổi chuyển động",
          "Bài 8: Gia công cơ khí bằng tay",
          "Bài 9: Ngành nghề trong lĩnh vực cơ khí",
          "Bài 10: Dự án: Gia công chi tiết bằng dụng cụ cầm tay",
          "Ôn tập Chương II"
        ]
      },
      {
        "chapter": "Chương III: An toàn điện",
        "items": [
          "Bài 11: Tai nạn điện",
          "Bài 12: Biện pháp an toàn điện",
          "Bài 13: Sơ cứu người bị tai nạn điện",
          "Ôn tập Chương III"
        ]
      },
      {
        "chapter": "Chương IV: Kĩ thuật điện",
        "items": [
          "Bài 14: Khái quát về mạch điện",
          "Bài 15: Cảm biến và mô đun cảm biến",
          "Bài 16: Mạch điện điều khiển sử dụng mô đun cảm biến",
          "Bài 17: Ngành nghề trong lĩnh vực kĩ thuật điện",
          "Ôn tập Chương IV"
        ]
      },
      {
        "chapter": "Chương V: Thiết kế kĩ thuật",
        "items": [
          "Bài 18: Giới thiệu về thiết kế kĩ thuật",
          "Bài 19: Các bước cơ bản trong thiết kế kĩ thuật",
          "Bài 20: Dự án: Thiết kế hệ thống tưới cây tự động",
          "Ôn tập Chương V"
        ]
      }
    ],
    "9": [
      {
        "chapter": "Công nghệ",
        "items": [
          "Bài 1: Nghề nghiệp trong lĩnh vực kĩ thuật và công nghệ",
          "Bài 2: Cơ cấu hệ thống giáo dục quốc dân",
          "Bài 3: Thị trường lao động kĩ thuật, công nghệ tại Việt Nam",
          "Bài 4: Quy trình lựa chọn nghề nghiệp",
          "Bài 5: Dự án: Tự đánh giá mức độ phù hợp của bản thân với một số ngành nghề thuộc lĩnh vực kĩ thuật, công nghệ"
        ]
      },
      {
        "chapter": "Chương 1: Dinh dưỡng và thực phẩm",
        "items": [
          "Bài 1: Thành phần dinh dưỡng trong thực phẩm",
          "Bài 2: Lựa chọn và bảo quản thực phẩm",
          "Bài 3: Một số ngành nghề liên quan đến chế biến thực phẩm",
          "Ôn tập chương 1"
        ]
      },
      {
        "chapter": "Chương 2: Tổ chức và chế biến món ăn",
        "items": [
          "Bài 4: An toàn lao động và an toàn vệ sinh thực phẩm",
          "Bài 5: Dự án: Tính toán chi phí bữa ăn theo thực đơn",
          "Bài 6: Chế biến thực phẩm có sử dụng nhiệt",
          "Bài 7: Chế biến thực phẩm không sử dụng nhiệt",
          "Ôn tập chương 2",
          "Bài 1: Thiết bị đóng cắt và lấy điện trong gia đình",
          "Bài 2: Dụng cụ đo điện cơ bản",
          "Bài 3: Thiết kế mạng điện trong nhà",
          "Bài 4: Vật liệu, thiết bị và dụng cụ dùng cho lắp đặt mạng điện trong nhà",
          "Bài 5: Tính toán chi phí mạng điện trong nhà",
          "Bài 6: Thực hành: Lắp đặt mạng điện trong nhà",
          "Bài 7: Một số ngành nghề liên quan đến lắp đặt mạng điện trong nhà",
          "Bài 1: Giới thiệu chung về cây ăn quả",
          "Bài 2: Nhân giống vô tính cây ăn quả",
          "Bài 3: Kĩ thuật trồng và chăm sóc cây ăn quả có múi",
          "Bài 4: Kĩ thuật trồng và chăm sóc cây nhãn",
          "Bài 5: Kĩ thuật trồng và chăm sóc cây xoài",
          "Bài 6: Kĩ thuật trồng và chăm sóc cây sầu riêng",
          "Bài 7: Kĩ thuật trồng và chăm sóc cây chuối"
        ]
      }
    ]
  },
  "amnhac": {
    "6": [
      {
        "chapter": "Chủ đề 1: Tuổi học trò",
        "items": [
          "Hát: Bài hát Con đường học trò",
          "Nghe nhạc: Nghe bài hát Tháng năm học trò",
          "Thường thức âm nhạc: Giới thiệu đàn piano",
          "Thường thức âm nhạc: Các thuộc tính cơ bản của âm thanh có tính nhạc",
          "Vận dụng - Sáng tạo"
        ]
      },
      {
        "chapter": "Chủ đề 2: Cuộc sống tươi đẹp",
        "items": [
          "Hát: bài hát Đời sống không già vì có chúng em",
          "Nghe nhạc: Tác phẩm The Blue Danube",
          "Lý thuyết âm nhạc: Kí hiệu âm bằng hệ thống chữ cái Latin",
          "Nhạc cụ: Recorder hoặc kèn phím"
        ]
      },
      {
        "chapter": "Chủ đề 3: Nhớ ơn thầy cô",
        "items": [
          "Hát: Bài hát Thầy cô là tất cả",
          "Nghe nhạc: Nghe bài hát Nhơ ơn thầy cô",
          "Lý thuyết âm nhạc: Nhịp 4 4",
          "Thường thức âm nhạc: Giới thiệu hình thức hát bè"
        ]
      },
      {
        "chapter": "Chủ đề 4: Ước mơ hòa bình",
        "items": [
          "Hát: Bài hát Những ước mơ",
          "Nghe nhạc: Trích đoạn chương IV bản Giao hưởng số 9 của Ludwig van Beethoven",
          "Lý thuyết âm nhạc: Nhạc sĩ Văn Ký và tác phẩm Bài ca Hy vọng",
          "Ôn tập"
        ]
      },
      {
        "chapter": "Chủ đề 5: Giai điệu quê hương",
        "items": [
          "Hát: Bài hát Mưa rơi",
          "Nghe nhạc: Bản hòa tấu nhạc cụ dân tộc Mừng hội hoa bông",
          "Lý thuyết âm nhạc: Giới thiệu khèn và sáo trúc"
        ]
      },
      {
        "chapter": "Chủ đề 6: Mẹ trong trái tim em",
        "items": [
          "Hát: Bài hát Chỉ có một trên đời",
          "Thường thức âm nhạc: Nhạc sĩ Johannes Brahms và Tác phẩm Lullaby",
          "Lý thuyết âm nhạc: Giới thiệu cung và nửa cung"
        ]
      },
      {
        "chapter": "Chủ đề 7: Âm nhạc nước ngoài",
        "items": [
          "Hát: Bài hát Hãy để mặt trời luôn chiếu sáng",
          "Nghe nhạc: Nghe bài hát Auld Lang Syne",
          "Lý thuyết âm nhạc: Các bậc chuyển hóa, dấu hóa"
        ]
      },
      {
        "chapter": "Chủ đề 8: Bác hồ với thiếu nhi",
        "items": [
          "Hát: Bài hát Bác Hồ - Người cho em tất cả",
          "Nghe nhạc: Nghe bài hát Việt Nam quê hương tôi",
          "Thường thức âm nhạc: Bài hát Như có Bác trong ngày đại thắng"
        ]
      }
    ],
    "7": [
      {
        "chapter": "Chủ đề 1: Ngày khai trường",
        "items": [
          "Hát: Bài hát Khai trường",
          "Lý thuyết âm nhạc: Nhịp lấy đà",
          "Thường thức âm nhạc: Nhạc sĩ Trịnh Công Sơn và bài hát Tuổi đời mênh mông",
          "Vận dụng - Sáng tạo"
        ]
      },
      {
        "chapter": "Chủ đề 2: Môi trường xanh",
        "items": [
          "Hát: Bài hát Vì cuộc sống tươi đẹp",
          "Nghe nhạc: Tác phẩm Alouette (Tiếng chim sơn ca)",
          "Nhạc cụ: Recorder hoặc kèn phím",
          "Thường thức âm nhạc: Nhạc sĩ Hoàng Việt và ca khúc Nhạc rừng"
        ]
      },
      {
        "chapter": "Chủ đề 3: Thầy cô và mái trường",
        "items": [
          "Hát: Bài hát Nhớ ơn thầy cô",
          "Lý thuyết âm nhạc: Dấu nhắc lại, dấu quay lại, khung thay đổi",
          "Thường thức âm nhạc: Giới thiệu một số thể loại ca khúc"
        ]
      },
      {
        "chapter": "Chủ đề 4: Giai điệu quê hương",
        "items": [
          "Hát: Bài hát Lí kéo chài",
          "Lý thuyết âm nhạc: Dân ca một số vùng miền Việt Nam"
        ]
      },
      {
        "chapter": "Chủ đề 5: Nhịp điệu mùa xuân",
        "items": [
          "Hát: Bài hát Mùa xuân ơi",
          "Nghe nhạc: Bài hát Sông Đakrông mùa xuân về",
          "Thường thức âm nhạc: Giới thiệu cồng chiêng, đàn t'rưng của Tây Nguyên",
          "Lý thuyết âm nhạc: Các kí hiệu tăng trường độ"
        ]
      },
      {
        "chapter": "Chủ đề 6: Âm nhạc nước ngoài",
        "items": [
          "Hát: Bài hát Santa Lucia",
          "Lý thuyết âm nhạc: Một số kí hiệu, thuật ngữ về nhịp độ và sắc thái cường độ",
          "Thường thức âm nhạc: Giới thiệu đàn cello và contrabass"
        ]
      },
      {
        "chapter": "Chủ đề 7: Cuộc sống tươi đẹp",
        "items": [
          "Hát: Bài hát Đời cho em những nốt nhạc vui",
          "Thường thức âm nhạc: Nhạc sĩ Pyotr Ilyich Tchaikovsky và khúc nhạc Chèo thuyền"
        ]
      },
      {
        "chapter": "Chủ đề 8: Mùa hè của em",
        "items": [
          "Hát: Bài hát Mưa hè",
          "Nghe nhạc: Bài hát Hè về"
        ]
      }
    ],
    "8": [
      {
        "chapter": "Chủ đề 1: Chào năm học mới",
        "items": [
          "Bài 1:",
          "Bài 2:"
        ]
      },
      {
        "chapter": "Chủ đề 2: Tôi yêu việt nam",
        "items": [
          "Bài 3:",
          "Bài 4:"
        ]
      },
      {
        "chapter": "Chủ đề 3: Hoà ca",
        "items": [
          "Bài 5:",
          "Bài 6:"
        ]
      },
      {
        "chapter": "Chủ đề 4: Biển đảo quê hương",
        "items": [
          "Bài 7:",
          "Bài 8:"
        ]
      },
      {
        "chapter": "Chủ đề 5: Chào xuân",
        "items": [
          "Bài 9:",
          "Bài 10:"
        ]
      },
      {
        "chapter": "Chủ đề 6: Âm nhạc nước ngoài",
        "items": [
          "Bài 11:",
          "Bài 12:"
        ]
      },
      {
        "chapter": "Chủ đề 7: Giai điệu quê hương",
        "items": [
          "Bài 13:",
          "Bài 14:"
        ]
      },
      {
        "chapter": "Chủ đề 8: Nhịp điệu mùa hè",
        "items": [
          "Bài 15:",
          "Bài 16:"
        ]
      }
    ],
    "9": [
      {
        "chapter": "Âm nhạc",
        "items": [
          "Bài 1: Khái quát về kĩ thuật điện",
          "Bài 2: Một số ngành nghề thuộc lĩnh vực kĩ thuật điện",
          "Bài 3: Mạch điện xoay chiều ba pha",
          "Bài 4: Cấu trúc hệ thống điện quốc gia",
          "Bài 5: Một số phương pháp sản xuất điện năng",
          "Bài 6: Mạng điện sản xuất quy mô nhỏ",
          "Bài 7: Mạng điện hạ áp dùng trong sinh hoạt",
          "Ôn tập chủ đề 1 và chủ đề 2",
          "Bài 8: Cấu trúc hệ thống điện trong gia đình",
          "Bài 9: Sơ đồ hệ thống điện trong gia đình",
          "Ôn tập chủ đề 3",
          "Bài 11: An toàn điện",
          "Bài 12: Tiết kiệm điện năng",
          "Ôn tập chủ đề 4",
          "Bài 1: Vai trò và triển vọng của lâm nghiệp",
          "Bài 2: Đặc trưng cơ bản của sản xuất lâm nghiệp",
          "Bài 3: Sự suy thoái tài nguyên rừng",
          "Ôn tập chủ đề 1. Giới thiệu về lâm nghiệp",
          "Bài 4: Sinh trưởng và phát triển của cây rừng",
          "Bài 5: Hoạt động trồng và chăm sóc rừng",
          "Ôn tập chủ đề 2",
          "Bài 6: Ý nghĩa, nhiệm vụ của việc bảo vệ và khai thác tài nguyên rừng bền vững",
          "Bài 7: Thực trạng trồng, chăm sóc bảo vệ và khai thác rừng",
          "Bài 8: Bảo vệ và khai thác tài nguyên rừng",
          "Ôn tập Chủ đề 3",
          "Bài 9: Vai trò và triển vọng của thủy sản trong bối cảnh cuộc cách mạng công nghệ 4.0",
          "Bài 10: Các nhóm thủy sản và phương thức nuôi phổ biến",
          "Ôn tập Chủ đề 4",
          "Bài 11: Một số chỉ tiêu cơ bản của môi trường nuôi thủy sản",
          "Bài 12: Quản lí môi trường nuôi thủy sản",
          "Bài 13: Xử lí môi trường nuôi thủy sản",
          "Ôn tập chủ đề 5"
        ]
      }
    ]
  },
  "mithuat": {
    "6": [
      {
        "chapter": "Chủ đề 1: Xây dựng ý tưởng trong sáng tác mĩ thuật",
        "items": [
          "Bài 1: Một số thể loại mĩ thuật",
          "Bài 2: Xây dựng ý tưởng trong sáng tác theo chủ đề"
        ]
      },
      {
        "chapter": "Chủ đề 2: Ngôi nhà yêu thương",
        "items": [
          "Bài 3: Tạo hình ngôi nhà",
          "Bài 4: Thiết kế quà lưu niệm"
        ]
      },
      {
        "chapter": "Chủ đề 3: Hoạt động trong trường học",
        "items": [
          "Bài 5: Tạo hình hoạt động trong nhà trường",
          "Bài 6: Thiết kế đồ chơi"
        ]
      },
      {
        "chapter": "Chủ đề 4: Mĩ thuật thời tiền sử",
        "items": [
          "Bài 7: Mĩ thuật thế giới thời kì tiền sử",
          "Bài 8: Mĩ thuật Việt Nam thời kì tiền sử"
        ]
      },
      {
        "chapter": "Chủ đề 5: Trò chơi dân gian",
        "items": [
          "Bài 9: Sáng tạo mĩ thuật và trò chơi dân gian",
          "Bài 10: Thiết kế thiệp chúc mừng"
        ]
      },
      {
        "chapter": "Chủ đề 6: Sắc màu lễ hội",
        "items": [
          "Bài 11: Hòa sắc trong tranh chủ đề lễ hội",
          "Bài 12: Màu sắc lễ hội trong thiết kế lịch treo tường"
        ]
      },
      {
        "chapter": "Chủ đề 7: Cuộc sống thường ngày",
        "items": [
          "Bài 13: Sáng tạo mĩ thuật với hình ảnh trong cuộc sống",
          "Bài 14: Thiết kế thời gian biểu"
        ]
      },
      {
        "chapter": "Chủ đề 8: Mĩ thuật thời kì cổ đại",
        "items": [
          "Bài 15: Mĩ thuật thế giới thời kì cổ đại",
          "Bài 16: Mĩ thuật Việt Nam thời kì cổ đại"
        ]
      }
    ],
    "7": [
      {
        "chapter": "Chủ đề 1: Mĩ thuật thế giới thời kì trung đại",
        "items": [
          "Bài 1: Mĩ thuật tạo hình thời kì trung đại",
          "Bài 2: Mĩ thuật ứng dựng thời kì trung đại"
        ]
      },
      {
        "chapter": "Chủ đề 2: Vẻ đẹp di tích",
        "items": [
          "Bài 3: Hình ảnh di tích trong sáng tạo mĩ thuật",
          "Bài 4: Hình ảnh di tích trong thiết kế tem bưu chính"
        ]
      },
      {
        "chapter": "Chủ đề 3: Yếu tố dân tộc trong mĩ thuật",
        "items": [
          "Bài 5: Yếu tố dân tộc trong tranh của một số họa sĩ",
          "Bài 6: Thiết kế logo"
        ]
      },
      {
        "chapter": "Chủ đề 4: Vẻ đẹp trong tác phẩm hội họa",
        "items": [
          "Bài 7: Không gian trong tác phẩm hội họa thế giới thời kì trung đại",
          "Bài 8: Tranh tĩnh vật"
        ]
      },
      {
        "chapter": "Chủ đề 5: Hiện thực cuộc sống trong sáng tạo mĩ thuật",
        "items": [
          "Bài 9: Tìm hiểu nguồn sáng trong tranh",
          "Bài 10: Thiết kế tạo mẫu trang phục"
        ]
      },
      {
        "chapter": "Chủ đề 6: Tạo hình ngôi nhà trong sáng tạo mĩ thuật",
        "items": [
          "Bài 11: Tạo hình ngôi nhà từ vật liệu sẵn có",
          "Bài 12: Trang cổ động"
        ]
      },
      {
        "chapter": "Chủ đề 7: Sum họp gia đình",
        "items": [
          "Bài 13: Đề tài gia đình trong sáng tạo mĩ thuật",
          "Bài 14: Thiết kế khung ảnh từ vật liệu sẵn có"
        ]
      },
      {
        "chapter": "Chủ đề 8: Mĩ thuật Việt Nam thời kì trung đại",
        "items": [
          "Bài 15: Di sản mĩ thuật Việt Nam thời kì trung đại",
          "Bài 16: Khai thác giá trị tạo hình truyền thống trong trang trí đồ vật"
        ]
      }
    ],
    "8": [
      {
        "chapter": "Chủ đề 1: Hình tượng con người trong mĩ thuật",
        "items": [
          "Bài 1: Hình tượng con người trong sáng tạo mĩ thuật",
          "Bài 2: Một số dạng bố cục trong tranh sinh hoạt"
        ]
      },
      {
        "chapter": "Chủ đề 2: Vẻ đẹp trong nghệ thuật truyền thông",
        "items": [
          "Bài 3: Nghệ thuật truyền thống",
          "Bài 4: Thiết kế trang phục với hoa văn dân tộc thiểu số"
        ]
      },
      {
        "chapter": "Chủ đề 3: Niềm vui, hạnh phúc",
        "items": [
          "Bài 5: Tác phẩm hội họa chủ đề Niềm vui, hạnh phúc",
          "Bài 6: Thiết kế quà sinh nhật từ vật liệu sẵn có"
        ]
      },
      {
        "chapter": "Chủ đề 4: Mĩ thuật thế giới thời kì hiện đại",
        "items": [
          "Bài 7: Một số trường phái mĩ thuật phương Tây thời kì hiện đại",
          "Bài 8: Nghệ thuật trang trí đồ gia dụng"
        ]
      },
      {
        "chapter": "Chủ đề 5: Vẻ đẹp trong lao động",
        "items": [
          "Bài 9: Vẻ đẹp của người lao động trong sáng tạo mĩ thuật",
          "Bài 10: Nghệ thuật trổ giấy trong trang trí"
        ]
      },
      {
        "chapter": "Chủ đề 6: Giao thông công cộng trong sáng tạo mĩ thuật",
        "items": [
          "Bài 11: Phương tiện giao thông công cộng trong sáng tạo mĩ thuật",
          "Bài 12: Thiết kế, trang trí áo phông"
        ]
      },
      {
        "chapter": "Chủ đề 7: Mĩ thuật Việt Nam thời kì hiện đại",
        "items": [
          "Bài 13: Một số tác giả, tác phẩm mĩ thuật Việt Nam thời kì hiện đại",
          "Bài 14: Nghệ thuật thiết kế Việt Nam thời kì hiện đại"
        ]
      },
      {
        "chapter": "Chủ đề 8: Hướng nghiệp",
        "items": [
          "Bài 15: Ngành, nghề liên quan đến mĩ thuật tạo hình",
          "Bài 16: Đặc trưng của ngành, nghề liên quan đến mĩ thuật tạo hình"
        ]
      }
    ],
    "9": [
      {
        "chapter": "Mĩ thuật",
        "items": [
          "Luyện tập 1",
          "Luyện tập 2",
          "Luyện tập 3",
          "Luyện tập 4",
          "Luyện tập 5",
          "Luyện tập 6",
          "Vận dụng 1",
          "Vận dụng 2",
          "Vận dụng",
          "luyện tập 1"
        ]
      }
    ]
  },
  "gdtc": {
    "6": [
      {
        "chapter": "Phần một: Kiến thức chung",
        "items": [
          "CHỦ ĐỀ CHẾ ĐỘ DINH DƯỠNG TRONG LUYỆN TẬP THỂ DỤC THỂ THAO"
        ]
      },
      {
        "chapter": "Chủ đề 1: Chạy cự li ngắn (60 m)",
        "items": [
          "Chủ đề 1: Chạy cự li ngắn (60 m)"
        ]
      },
      {
        "chapter": "Chủ đề 2: Ném bóng",
        "items": [
          "Chủ đề 2: Ném bóng"
        ]
      },
      {
        "chapter": "Chủ đề 3: Chạy cự li trung bình",
        "items": [
          "Chủ đề 3: Chạy cự li trung bình"
        ]
      },
      {
        "chapter": "Chủ đề 4: Bài tập thể dục",
        "items": [
          "Chủ đề 4: Bài tập thể dục"
        ]
      },
      {
        "chapter": "Chủ đề 1: Cầu lông",
        "items": [
          "Chủ đề 1: Cầu lông"
        ]
      },
      {
        "chapter": "Chủ đề 2: Bóng đá",
        "items": [
          "Chủ đề 2: Bóng đá"
        ]
      },
      {
        "chapter": "Chủ đề 3: Bóng rổ",
        "items": [
          "Chủ đề 3: Bóng rổ"
        ]
      }
    ],
    "7": [
      {
        "chapter": "Phần một: Kiến thức chung",
        "items": [
          "CHỦ ĐỀ LỰA CHỌN VÀ SỬ DỤNG CÁC YẾU TỐ CỦA MÔI TRƯỜNG TỰ NHIÊN TRONG LUYỆN TẬP"
        ]
      },
      {
        "chapter": "Chủ đề 1: Chạy cự li ngắn (60m)",
        "items": [
          "Chủ đề 1: Chạy cự li ngắn (60m)"
        ]
      },
      {
        "chapter": "Chủ đề 2: Nhảu xa kiểu ngồi",
        "items": [
          "Chủ đề 2: Nhảu xa kiểu ngồi"
        ]
      },
      {
        "chapter": "Chủ đề 3: Chạy cự li trung bình",
        "items": [
          "Chủ đề 3: Chạy cự li trung bình"
        ]
      },
      {
        "chapter": "Chủ đề 4: Bài tập thể dục",
        "items": [
          "Chủ đề 4: Bài tập thể dục"
        ]
      },
      {
        "chapter": "Chủ đề 1: Cầu lông",
        "items": [
          "Chủ đề 1: Cầu lông"
        ]
      },
      {
        "chapter": "Chủ đề 3: Bóng rổ",
        "items": [
          "Chủ đề 3: Bóng rổ"
        ]
      }
    ],
    "8": [
      {
        "chapter": "Chủ đề 1: Chạy cự li ngắn (100 m)",
        "items": [
          "Chủ đề 1: Chạy cự li ngắn (100 m)"
        ]
      },
      {
        "chapter": "Chủ đề 2: Nhảy cao kiểu bước qua",
        "items": [
          "Chủ đề 2: Nhảy cao kiểu bước qua"
        ]
      },
      {
        "chapter": "Chủ đề 3: Chạy cự li trung bình",
        "items": [
          "Chủ đề 3: Chạy cự li trung bình"
        ]
      },
      {
        "chapter": "Chủ đề 4: Bài tập thể dục",
        "items": [
          "Chủ đề 4: Bài tập thể dục"
        ]
      },
      {
        "chapter": "Phần một: Kiến thức chung",
        "items": [
          "CHỦ ĐỀ SỬ DỤNG CHẾ ĐỘ DINH DƯỠNG THÍCH HỢP VỚI BẢN THÂN TRONG LUYỆN TẬP THỂ DỤC THỂ THAO"
        ]
      },
      {
        "chapter": "Chủ đề 1: Cầu lông",
        "items": [
          "Chủ đề 1: Cầu lông"
        ]
      },
      {
        "chapter": "Chủ đề 2: Bóng đá",
        "items": [
          "Chủ đề 2: Bóng đá"
        ]
      },
      {
        "chapter": "Chủ đề 3: Bóng rổ",
        "items": [
          "Chủ đề 3: Bóng rổ"
        ]
      }
    ],
    "9": [
      {
        "chapter": "Giáo dục thể chất",
        "items": [
          "Bài 1: Lợi ích của máy tính",
          "Bài 3: Sử dụng máy tính thành thạo giúp làm được nhiều viêc",
          "Bài 1: Tìm thông tin trên website",
          "Bài 2: Hợp tác, tìm kiếm và chia sẻ thông tin",
          "Bài 1: Thu thập và tìm kiếm thông tin trong giải quyết vấn đề",
          "Bài 2: Tìm kiếm tệp và thư mục",
          "Bài. Tôn trọng quyền tác giả khi sử dụng nội dung thông tin",
          "Bài 4: Định dạng kí tự",
          "Bài 1: Làm quen với phần mềm paint",
          "Bài 1: Sử dụng website youtube kids",
          "Bài 1: Nhóm lệnh bút vẽ",
          "Bài 3: Trang phục của nhân vật",
          "Bài 5: Cấu trúc tuần tự",
          "Bài 6: Cấu trúc lặp với số lần biết trước",
          "Bài 7: Cấu trúc lặp có điều kiện",
          "Bài 8: Cấu trúc lặp liên tục",
          "Bài 9: Biến và cách dùng biến",
          "Bài 10: Các phép toán số học cơ bản và phép kết hợp",
          "Bài 11: Các phép so sánh",
          "Bài 12: Cấu trúc rẽ nhánh",
          "Bài 13: Chạy thử, phát hiện và sửa lỗi chương trình"
        ]
      }
    ]
  },
  "hdtn-hn": {
    "6": [
      {
        "chapter": "Chủ đề 1: Em với nhà trường",
        "items": [
          "1. Lớp học mới của em",
          "2. Truyền thống trường em",
          "3. Điều chỉnh bản thân cho phù hợp với môi trường học tập mới",
          "4. Em và các bạn"
        ]
      },
      {
        "chapter": "Chủ đề 2: Khám phá bản thân",
        "items": [
          "1. Em đã lớn hơn",
          "2. Đức tính đặc trưng của em",
          "3. Sở thích và khả năng của em",
          "4. Những giá trị của bản thân"
        ]
      },
      {
        "chapter": "Chủ đề 3: Trách nhiệm với bản thân",
        "items": [
          "1. Tự chăm sóc bản thân",
          "2. Ứng phó với thiên tai"
        ]
      },
      {
        "chapter": "Chủ đề 4: Rèn luyện bản thân",
        "items": [
          "1. Góc học tập của em",
          "2. Sắp xếp nơi ở của em",
          "3. Giao tiếp phù hợp",
          "4. Chi tiêu hợp lí"
        ]
      },
      {
        "chapter": "Chủ đề 5: Em với gia đình",
        "items": [
          "1. Động viên, chăm sóc người trong gia đình",
          "2. Giải quyết một số vấn đề nảy sinh trong gia đình",
          "3. Em làm việc nhà"
        ]
      },
      {
        "chapter": "Chủ đề 6: Em với cộng đồng",
        "items": [
          "1. Thiết lập quan hệ với cộng đồng",
          "2. Em tham gia hoạt động thiện nguyện",
          "3. Hành vi có văn hóa nơi công cộng",
          "4. Truyền thống của em"
        ]
      },
      {
        "chapter": "Chủ đề 7: Em với thiên nhiên và môi trường",
        "items": [
          "1. Khám phá cảnh quan thiên nhiên",
          "2. Bảo tồn cảnh quan thiên nhiên",
          "3. Ứng phó với biến đổi khí hậu"
        ]
      },
      {
        "chapter": "Chủ đề 8: Khám phá thế giới nghề nghiệp",
        "items": [
          "1. Thế giới nghề nghiệp quanh ta",
          "2. Khám phá nghề truyền thống nước ta",
          "3. Trải nghiệm nghề truyền thống"
        ]
      },
      {
        "chapter": "Chủ đề 9: Hiểu bản thân - chọn đúng nghề",
        "items": [
          "1. Em với nghề truyền thống",
          "2. Em tập làm nghề truyền thống",
          "3. Trổ tài chế biến món ăn truyền thống"
        ]
      }
    ],
    "7": [
      {
        "chapter": "Chủ đề 1: Em với nhà trường",
        "items": [
          "1. phát triển mối quan hệ hoà đồng, hợp tác với thầy cô và các bạn",
          "2. tự hào truyền thống trường em"
        ]
      },
      {
        "chapter": "Chủ đề 2: Khám phá bản thân",
        "items": [
          "1. điểm mạnh, điểm hạn chế của tôi",
          "2. kiểm soát cảm xúc của bản thân"
        ]
      },
      {
        "chapter": "Chủ đề 3: Trách nhiệm với bản thân",
        "items": [
          "1. vượt qua khó khăn",
          "2. tự bảo vệ bản thân trong tình huống nguy hiểm"
        ]
      },
      {
        "chapter": "Chủ đề 4: Rèn luyện bản thân",
        "items": [
          "1. rèn luyện thói quen ngăn nắp, gọn gàng, sạch sẽ",
          "2. rèn luyện tính kiên trì, chăm chỉ",
          "3. quản lí chi tiêu"
        ]
      },
      {
        "chapter": "Chủ đề 5: Em với gia đình",
        "items": [
          "1. kĩ năng chăm sóc người thân khi mệt, ốm",
          "2. kế hoạch lao động tại gia đình",
          "3. lắng nghe tích cực ý kiến người thân trong gia đình"
        ]
      },
      {
        "chapter": "Chủ đề 6: Em với cộng đồng",
        "items": [
          "1. giao tiếp, ứng xử có văn hoá và tôn trọng sự khác biệt",
          "2. tham gia hoạt động thiện nguyện",
          "3. tự hào truyền thống quê hương"
        ]
      },
      {
        "chapter": "Chủ đề 7: Em với thiên nhiên và môi trường",
        "items": [
          "1. cảnh quan thiên nhiên quê hương tôi",
          "2. bảo vệ môi trường, giảm thiểu hiệu ứng nhà kính"
        ]
      },
      {
        "chapter": "Chủ đề 8: Khám phá thế giới nghề nghiệp",
        "items": [
          "Chủ đề 8: Khám phá thế giới nghề nghiệp"
        ]
      },
      {
        "chapter": "Chủ đề 9: Hiểu bản thân – chọn đúng nghề",
        "items": [
          "Chủ đề 9: Hiểu bản thân – chọn đúng nghề"
        ]
      }
    ],
    "8": [
      {
        "chapter": "Chủ đề 1: Em với nhà trường",
        "items": [
          "1. xây dựng và giữ gìn tình bạn",
          "2. phòng, tránh bắt nạt học đường",
          "3. xây dựng truyền thống nhà trường"
        ]
      },
      {
        "chapter": "Chủ đề 2: Khám phá bản thân",
        "items": [
          "1. tính cách và cảm xúc của tôi",
          "2. khả năng tranh biện, thương thuyết của tôi"
        ]
      },
      {
        "chapter": "Chủ đề 3: Trách nhiệm với bản thân",
        "items": [
          "1. sống có trách nhiệm",
          "2. kĩ năng từ chối"
        ]
      },
      {
        "chapter": "Chủ đề 4: Rèn luyện bản thân",
        "items": [
          "1. người tiêu dùng thông thái",
          "2. nhà kinh doanh nhỏ",
          "3. rèn luyện sự tự chủ"
        ]
      },
      {
        "chapter": "Chủ đề 5: Em với gia đình",
        "items": [
          "1. tôn trọng, thuyết phục và ứng xử để người thân hài lòng",
          "2. tiết kiệm và thực hiện công việc gia đình"
        ]
      },
      {
        "chapter": "Chủ đề 6: Em với cộng đồng",
        "items": [
          "1. tham gia các hoạt động giáo dục truyền thống và phát triển cộng đồng ở địa phương",
          "2. lập và thực hiện kế hoạch hoạt động thiện nguyện"
        ]
      },
      {
        "chapter": "Chủ đề 7: Em với thiên nhiên và môi trường",
        "items": [
          "1. cảnh quan thiên nhiên quê hương tô",
          "2. truyền thông về biện pháp đề phòng và giảm nhẹ rủi ro thiên tai ở địa phương"
        ]
      },
      {
        "chapter": "Chủ đề 8: Khám phá thế giới nghề nghiệp",
        "items": [
          "Chủ đề 8: Khám phá thế giới nghề nghiệp"
        ]
      },
      {
        "chapter": "Chủ đề 9: Hiểu bản thân – chọn đúng nghề",
        "items": [
          "1. hứng thú nghề nghiệp",
          "2. rèn luyện, học tập theo định hướng nghề nghiệp"
        ]
      }
    ],
    "9": [
      {
        "chapter": "Hoạt động trải nghiệm, hướng nghiệp",
        "items": [
          "Mục 1: Tôn trọng sự khác biệt và sống hài hòa với bạn bè, thầy cô",
          "Mục 2: Phòng chống bắt nạt học đường",
          "Mục 3: Xây dựng truyền thống nhà trường và các hoạt động lao động công ích",
          "Mục 1: Nhận diện điểm tích cực và chưa tích cực trong giao tiếp và ứng xử của bản thân",
          "Mục 2: Khám phá khả năng thích nghi của bản thân",
          "Mục 1: Trách nhiệm với nhiệm vụ được giao",
          "Mục 2: Ứng phó với căng thẳng và áp lực",
          "Mục 1: Tạo động lực cho bản thân",
          "Mục 2: Xây dựng ngân sách cá nhân hợp lý",
          "Mục 1: Tạo bầu không khí vui vẻ, yêu thương và giải quyết bất đồng trong gia đình",
          "Mục 2: Tổ chức, sắp xếp khoa học công việc gia đình",
          "Mục 3: Biện pháp phát triển kinh tế gia đình",
          "Mục 1: Xây dựng và phát triển cộng đồng",
          "Mục 2: Khảo sát thực trạng giao tiếp của học sinh trên mạng xã hội",
          "Mục 3: Truyền thông trong cộng đồng về những vấn đề học đường",
          "Mục 1: Việt Nam – tổ quốc tôi",
          "Mục 2: Phòng chống ô nhiễm và bảo vệ môi trường",
          "Mục 1: Nghề em quan tâm",
          "Mục 1: Hệ thống các cơ sở giáo dục nghề nghiệp của trung ương và địa phương",
          "Mục 2: Rèn luyện, phát triển bản thân theo yêu cầu của định hướng nghề nghiệp"
        ]
      }
    ]
  },
  "tienganh": {
    "6": [
      {
        "chapter": "Tiếng Anh (Tập 1)",
        "items": [
          "Unit 1: my new school",
          "Unit 2: my house",
          "Unit 3: my friends",
          "Review 1:",
          "Unit 4: my neighbourhood",
          "Unit 5: natural wonders of viet nam",
          "Unit 6: our tet holiday",
          "Review 2:"
        ]
      },
      {
        "chapter": "Tiếng Anh (Tập 2)",
        "items": [
          "Unit 7: television",
          "Unit 8: sports and games",
          "Unit 9: cities of the world",
          "Review 3:",
          "Unit 10: our houses in the future",
          "Unit 11: our greener world",
          "Unit 12: ROBOTS",
          "Review 4:"
        ]
      }
    ],
    "7": [
      {
        "chapter": "Tiếng Anh (Tập 1)",
        "items": [
          "Unit 1: My hobbies",
          "Unit 2: Health",
          "Unit 3: Community service",
          "Review 1:",
          "Unit 4: Music anh arts",
          "Unit 5: Vietnamese food anh drink",
          "Unit 6: The first university in Viet Nam",
          "Review 2:"
        ]
      },
      {
        "chapter": "Tiếng Anh (Tập 2)",
        "items": [
          "Unit 7: Trafic",
          "Unit 8: Films",
          "Unit 9: Festivals around the world",
          "Review 3:",
          "Unit 10: Sources of energy",
          "Unit 11: Travelling in the future",
          "Unit 12: An Overcrowded World",
          "Review 4:"
        ]
      }
    ],
    "8": [
      {
        "chapter": "Tiếng Anh (Tập 1)",
        "items": [
          "Unit 1: Leisure activities",
          "Unit 2: Life in the coutryside",
          "Unit 3: Peoples of Viet Nam",
          "Review 1:",
          "Unit 4: Our customs and traditions",
          "Unit 5: Festivals in Viet Nam",
          "Unit 6: Folk tales"
        ]
      },
      {
        "chapter": "Tiếng Anh (Tập 2)",
        "items": [
          "Unit 7: Pollution",
          "Unit 8: English speaking countries",
          "Unit 9: Natural disasters",
          "Review 3:",
          "Unit 10: Communication",
          "Unit 11: Science and Technology",
          "Unit 12: Life on other planets",
          "Review 4:"
        ]
      }
    ],
    "9": [
      {
        "chapter": "Tiếng Anh (Tập 1)",
        "items": [
          "Unit 1: local environment",
          "Unit 2: city life",
          "Unit 3: teen stress and pressure",
          "Review 1:",
          "Unit 4: life in the past",
          "Unit 5: wonders of viet nam",
          "Unit 6: viet nam: then and now",
          "Review 2:"
        ]
      },
      {
        "chapter": "Tiếng Anh (Tập 2)",
        "items": [
          "Unit 7: recipes and eating habits",
          "Unit 8: tourism",
          "Unit 9: english in the world",
          "Review 3:",
          "Unit 10: space travel",
          "Unit 11: changing roles in society",
          "Unit 12: my future career",
          "Review 4:"
        ]
      }
    ]
  }
};
CURRICULUM_DATA.lessonsBySubject.toan = CURRICULUM_DATA.lessons;

// Utility functions
function getCurriculumLessons(gradeId) {
  if (!CURRICULUM_DATA.lessons[gradeId]) {
    return [];
  }
  return CURRICULUM_DATA.lessons[gradeId];
}

function getAllLessonsFlat(gradeId) {
  const chapters = getCurriculumLessons(gradeId);
  const result = [];
  chapters.forEach(ch => {
    ch.items.forEach(item => {
      result.push({
        chapter: ch.chapter,
        lesson: item,
        fullTitle: `${item} (${ch.chapter})`
      });
    });
  });
  return result;
}

function getSubjectsForGrade(grade) {
  const g = parseInt(grade, 10);
  return CURRICULUM_DATA.subjects.filter(s => s.grades.includes(g));
}

function getLessonsForBook(subjectId, bookId, grade) {
  const g = String(grade);
  const sid = String(subjectId || '').toLowerCase();
  const bySub = CURRICULUM_DATA.lessonsBySubject?.[sid];
  if (bySub && bySub[g]) return bySub[g];
  if (sid === 'toan') return getCurriculumLessons(g);
  return [];
}

function getSubjectCompetencies(subjectId) {
  return SUBJECT_COMPETENCIES[subjectId] || [];
}

function getGradeLevel(grade) {
  const g = parseInt(grade, 10);
  if (g >= 1 && g <= 5) return 'tieu-hoc';
  if (g >= 6 && g <= 9) return 'thcs';
  if (g >= 10 && g <= 12) return 'thpt';
  return 'thcs';
}

function getGradeLevelName(grade) {
  const g = parseInt(grade, 10);
  if (g >= 1 && g <= 5) return 'Tiểu học';
  if (g >= 6 && g <= 9) return 'THCS';
  if (g >= 10 && g <= 12) return 'THPT';
  return 'THCS';
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { 
    SUBJECT_COMPETENCIES,
    CURRICULUM_DATA, 
    getCurriculumLessons, 
    getAllLessonsFlat,
    getSubjectsForGrade,
    getLessonsForBook,
    getSubjectCompetencies,
    getGradeLevel,
    getGradeLevelName,
    get lessonsBySubject() { return CURRICULUM_DATA.lessonsBySubject; }
  };
}

