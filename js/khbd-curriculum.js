/**
 * js/khbd-curriculum.js
 * Cơ sở dữ liệu Mục lục SGK Toán THCS (Lớp 6, 7, 8, 9)
 * Chuyên biệt hóa 100% cho bộ sách: KẾT NỐI TRI THỨC VỚI CUỘC SỐNG (KNTT)
 * Tích hợp Khung Năng lực Đặc thù Toán, Khung Năng lực AI (QĐ 2422), Khung Năng lực Số (TT 02/2025).
 */

const CURRICULUM_DATA = {
  // THÔNG TIN BỘ SÁCH CỐ ĐỊNH
  book: {
    id: "kntt",
    name: "Kết Nối Tri Thức Với Cuộc Sống",
    shortName: "KNTT"
  },

  // DANH MỤC KHỐI LỚP
  grades: [
    { id: "6", name: "Toán 6 (KNTT)" },
    { id: "7", name: "Toán 7 (KNTT)" },
    { id: "8", name: "Toán 8 (KNTT)" },
    { id: "9", name: "Toán 9 (KNTT)" }
  ],

  // MỤC LỤC CHI TIẾT THEO TỪNG KHỐI LỚP (BỘ KẾT NỐI TRI THỨC VỚI CUỘC SỐNG)
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

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { CURRICULUM_DATA, getCurriculumLessons, getAllLessonsFlat };
}
