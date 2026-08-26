const KHBD_PEDAGOGY_CATALOG = {
  methods: [
    {
      id: "pbl",
      label: "Dạy học theo dự án (PBL)",
      description: "HS giải quyết vấn đề thực tế qua dự án",
      executionScript: {
        step1: {
          gv: 'GV nêu bài toán/dự án thực tiễn: "Chúng ta sẽ cùng tìm giải pháp thực tế cho vấn đề...", giao phiếu nhiệm vụ dự án, chia nhóm 4-6 HS và quy định rõ tiêu chí sản phẩm.',
          hs: "HS lắng nghe, nhận nhiệm vụ dự án, bầu nhóm trưởng/thư ký và phân công vai trò rõ ràng trong nhóm."
        },
        step2: {
          gv: "GV quan sát, di chuyển hỗ trợ các nhóm lập kế hoạch và phân tích dữ liệu, phát hiện lỗi sai điển hình: xác định sai mục tiêu cốt lõi hoặc thu thập dữ liệu thiếu kiểm chứng; can thiệp hỗ trợ phân hóa (gợi ý chia nhỏ nhiệm vụ cho nhóm chậm, đặt câu hỏi tối ưu hóa giải pháp cho nhóm nhanh).",
          hs: "HS làm việc cá nhân (3 phút) thu thập ý tưởng -> Thảo luận nhóm (5 phút) xây dựng đề cương, phác thảo sản phẩm trung gian (bảng phân tích/sơ đồ giải pháp) trên bảng nhóm."
        },
        step3: {
          gv: 'GV điều hành phiên báo cáo dự án, chọn đại diện nhóm thuyết trình và đặt câu hỏi phản biện: "Giải pháp của nhóm em có tính khả thi và tối ưu như thế nào?".',
          hs: "Đại diện nhóm trình bày sản phẩm dự án; các nhóm khác theo dõi, nhận xét và đặt câu hỏi chất vấn dựa trên tiêu chí rubric."
        },
        step4: {
          gv: "GV nhận xét toàn diện thái độ hợp tác và chất lượng sản phẩm của các nhóm, chuẩn hóa kiến thức cốt lõi và hướng dẫn chốt nội dung bài học.",
          hs: "HS đối chiếu đánh giá của GV, hoàn thiện hồ sơ dự án và ghi nhận kiến thức trọng tâm vào vở."
        }
      }
    },
    {
      id: "steam",
      label: "STEM/STEAM",
      description: "Tích hợp Khoa học-Công nghệ-Kỹ thuật-Nghệ thuật-Toán",
      recommendFor: { subjects: ["toan", "khtn", "vatly", "hoahoc", "sinhhoc", "khoahoc", "tnxh", "congnghe"] },
      executionScript: {
        step1: {
          gv: 'GV đặt vấn đề kỹ thuật/khoa học thực tiễn: "Làm thế nào để thiết kế mô hình/tính toán giải quyết vấn đề...?", phát phiếu tiêu chí kỹ thuật và dụng cụ học tập.',
          hs: "HS tiếp nhận thử thách STEM, kiểm tra đồ dùng/học liệu và phân chia nhiệm vụ thiết kế trong nhóm."
        },
        step2: {
          gv: "GV quan sát các nhóm tính toán và thiết kế, phát hiện lỗi sai điển hình: tính toán sai thông số hình học/bỏ qua điều kiện thực tế; can thiệp hỗ trợ phân hóa (hướng dẫn nhóm gặp khó về mặt công thức, khuyến khích nhóm khá cải tiến mẫu mã/tính năng).",
          hs: "HS vẽ phác thảo thiết kế cá nhân (2 phút) -> Thảo luận nhóm (5 phút) thống nhất bản thiết kế tối ưu và tiến hành lắp ráp/thử nghiệm sản phẩm trung gian."
        },
        step3: {
          gv: 'GV tổ chức cho các nhóm vận hành thử nghiệm sản phẩm, đặt câu hỏi đào sâu: "Nguyên lý khoa học và công thức toán học nào quyết định độ chính xác của sản phẩm?".',
          hs: "Đại diện nhóm vận hành mô hình/trình bày bản vẽ trước lớp; các nhóm khác ghi chép thông số thử nghiệm và phản biện."
        },
        step4: {
          gv: "GV tổng kết đánh giá sản phẩm theo tiêu chí STEM, chốt lại quy tắc toán học/nguyên lý khoa học nền tảng để HS ghi bảng.",
          hs: "HS ghi chép công thức chuẩn hóa vào vở và rút ra bài học cải tiến sản phẩm."
        }
      }
    },
    {
      id: "flipped",
      label: "Lớp học đảo ngược",
      description: "Học lý thuyết ở nhà, thực hành trên lớp",
      recommendFor: { needsFacilities: ["internet", "devices"] },
      executionScript: {
        step1: {
          gv: 'GV kích hoạt kiến thức đã tự học ở nhà: "Qua video và tài liệu đã xem ở nhà, em đã hiểu được quy tắc nào và còn thắc mắc ở điểm nào?", phát phiếu bài tập đào sâu.',
          hs: "HS báo cáo nhanh kết quả tự học, nêu các câu hỏi băn khoăn hoặc kết quả chuẩn bị trước ở nhà."
        },
        step2: {
          gv: "GV tổ chức các nhiệm vụ giải quyết vấn đề phức tạp trên lớp, phát hiện các lỗ hổng nhận thức khi tự học; can thiệp hỗ trợ trực tiếp các HS chưa nắm chắc lý thuyết cơ bản.",
          hs: "HS làm bài tập cá nhân (3 phút) -> Thảo luận cặp/nhóm (4 phút) giải quyết các bài toán tình huống nâng cao, ghi kết quả lên bảng nhóm."
        },
        step3: {
          gv: 'GV chỉ định HS giải thích phương pháp giải, đặt câu hỏi kiểm tra độ hiểu sâu: "Tại sao em áp dụng tính chất này mà không dùng cách khác?".',
          hs: "HS trình bày lời giải chi tiết, phản biện các cách tiếp cận khác nhau của bạn cùng lớp."
        },
        step4: {
          gv: "GV hệ thống hóa toàn bộ mạch kiến thức, khắc sâu bản chất định nghĩa/quy tắc và chốt nội dung ghi bảng.",
          hs: "HS hoàn thiện vở ghi với các kiến thức và ví dụ mẫu đã được chuẩn hóa."
        }
      }
    },
    {
      id: "cooperative",
      label: "Dạy học hợp tác",
      description: "HS làm việc nhóm có cấu trúc",
      executionScript: {
        step1: {
          gv: 'GV giao nhiệm vụ có cấu trúc phụ thuộc lẫn nhau: "Mỗi thành viên trong nhóm chịu trách nhiệm một phần nhiệm vụ để cùng hoàn thành sản phẩm chung...", phát phiếu học tập nhóm.',
          hs: "HS nhận phiếu, phân chia rõ nhiệm vụ của từng cá nhân trong nhóm và chuẩn bị nháp."
        },
        step2: {
          gv: "GV di chuyển bao quát các nhóm, phát hiện lỗi sai điển hình: làm việc tách rời không phối hợp hoặc một bạn làm hộ cả nhóm; can thiệp nhắc nhở quy tắc hợp tác và hỗ trợ nhóm gặp bế tắc.",
          hs: "HS làm việc cá nhân (2 phút) ghi ý kiến vào phần việc của mình -> Thảo luận nhóm (5 phút) tổng hợp và thống nhất sản phẩm chung lên bảng phụ."
        },
        step3: {
          gv: 'GV gọi ngẫu nhiên một thành viên bất kì trong nhóm báo cáo (đảm bảo mọi HS đều nắm bài): "Em hãy giải thích cách nhóm em tìm ra kết quả này?".',
          hs: "Thành viên được chỉ định đại diện nhóm báo cáo; các nhóm khác lắng nghe, nhận xét và bổ sung."
        },
        step4: {
          gv: "GV nhận xét tinh thần hợp tác nhóm và tính chính xác của lời giải, chốt kiến thức trọng tâm lên bảng.",
          hs: "HS sửa bài vào vở và tự đánh giá mức độ đóng góp của bản thân trong nhóm."
        }
      }
    },
    {
      id: "game",
      label: "Học qua trò chơi",
      description: "Gamification: điểm thưởng, bảng xếp hạng, thử thách",
      executionScript: {
        step1: {
          gv: 'GV phổ biến tên trò chơi, luật chơi và cách tính điểm: "Chúng ta sẽ tham gia thử thách gồm các chặng câu hỏi, đội nào có câu trả lời chính xác và nhanh nhất sẽ ghi điểm...", phát dụng cụ trò chơi (bảng phụ/thẻ màu).',
          hs: "HS lắng nghe luật chơi, chuẩn bị bảng con/thẻ đáp án và sẵn sàng thi đua."
        },
        step2: {
          gv: "GV điều hành các chặng thử thách, quan sát thời gian suy nghĩ, phát hiện các lỗi sai do vội vàng hoặc nhầm lẫn khái niệm; can thiệp giải thích ngắn giữa các chặng.",
          hs: "HS suy nghĩ cá nhân -> Hội ý chớp nhoáng trong nhóm để chọn phương án tối ưu -> Giơ bảng/trả lời đáp án."
        },
        step3: {
          gv: 'GV công bố kết quả từng vòng và yêu cầu giải thích: "Vì sao đội em lại chọn phương án này? Căn cứ vào quy tắc toán học nào?".',
          hs: "Đại diện đội giải thích căn cứ logic; các đội khác đối chiếu và phản biện nếu phát hiện sai sót."
        },
        step4: {
          gv: "GV tổng kết điểm số, vinh danh đội chiến thắng, chốt lại toàn bộ kiến thức trọng tâm được lồng ghép trong trò chơi.",
          hs: "HS ghi các công thức/quy tắc cốt lõi rút ra từ trò chơi vào vở."
        }
      }
    },
    {
      id: "differentiation",
      label: "Dạy học phân hóa",
      description: "Điều chỉnh nội dung theo năng lực HS",
      executionScript: {
        step1: {
          gv: 'GV giới thiệu hệ thống nhiệm vụ theo 3 mức độ (Cơ bản - Vận dụng - Mở rộng): "Các em chủ động chọn mức độ phù hợp với năng lực hoặc hoàn thành tuần tự theo bậc thang...", phát phiếu học tập phân hóa.',
          hs: "HS nhận diện mức độ của mình, chọn nhiệm vụ xuất phát điểm phù hợp."
        },
        step2: {
          gv: "GV dành thời gian trực tiếp hướng dẫn nhóm HS cần hỗ trợ cơ bản, phát hiện lỗi sai tính toán cơ bản; đồng thời cung cấp câu hỏi mở rộng/thử thách cho nhóm HS khá giỏi.",
          hs: "HS làm việc cá nhân theo mức độ của mình (6-8 phút) -> Trao đổi nhanh với bạn cùng mức độ để hoàn thiện lời giải."
        },
        step3: {
          gv: 'GV mời đại diện các mức độ lần lượt báo cáo: từ mức cơ bản đến nâng cao để cả lớp cùng theo dõi tiến trình phát triển kiến thức.',
          hs: "HS trình bày lời giải của từng mức, lớp lắng nghe và nhận xét."
        },
        step4: {
          gv: "GV chuẩn hóa đáp án cho từng mức độ, động viên sự nỗ lực của từng đối tượng HS, chốt chuẩn kiến thức chung cần đạt.",
          hs: "HS sửa bài vào vở theo đúng mức độ đã thực hiện và ghi chú cách làm bài mức cao hơn."
        }
      }
    },
    {
      id: "socratic",
      label: "Kỹ thuật Socratic",
      description: "Câu hỏi dẫn dắt tư duy phản biện",
      executionScript: {
        step1: {
          gv: 'GV nêu câu hỏi khởi đầu tạo mâu thuẫn nhận thức: "Nếu điều kiện này thay đổi thì kết luận có còn đúng không? Vì sao?", yêu cầu HS suy ngẫm sâu.',
          hs: "HS tiếp nhận câu hỏi, tự đặt ra các giả thiết trong đầu."
        },
        step2: {
          gv: 'GV liên tục đặt chuỗi câu hỏi truy vấn sâu ("Vì sao em nghĩ vậy?", "Có trường hợp ngoại lệ nào không?"), phát hiện các ngộ nhận logic; gợi ý định hướng tư duy từng bước.',
          hs: "HS suy nghĩ độc lập -> Trả lời câu hỏi gợi mở, bóc tách dần các tầng ý nghĩa của vấn đề."
        },
        step3: {
          gv: 'GV điều phối cuộc thảo luận có định hướng, tạo cơ hội cho các ý kiến trái chiều tranh luận: "Ai có lập luận phản bác lại ý kiến của bạn vừa nêu?".',
          hs: "HS đưa ra lập luận kèm dẫn chứng toán học/khoa học xác đáng, tự điều chỉnh nhận thức khi thấy mâu thuẫn."
        },
        step4: {
          gv: "GV đúc kết từ chuỗi câu hỏi - đáp để khái quát hóa thành định nghĩa/định lý hoàn chỉnh, ghi bảng nội dung cốt lõi.",
          hs: "HS ghi nhận quy tắc/kết luận logic vừa tìm ra vào vở."
        }
      }
    },
    {
      id: "mindmap",
      label: "Bản đồ tư duy",
      description: "Sơ đồ hóa kiến thức dạng cây",
      executionScript: {
        step1: {
          gv: 'GV nêu chủ đề trung tâm và hướng dẫn nguyên tắc vẽ sơ đồ tư duy: "Từ từ khóa chính ở giữa, hãy phát triển các nhánh cấp 1, cấp 2 bằng màu sắc và biểu tượng...", phát giấy A3/A4 và bút màu.',
          hs: "HS chuẩn bị giấy vẽ, bút màu và xác định từ khóa cốt lõi của bài học."
        },
        step2: {
          gv: "GV quan sát tiến độ lập sơ đồ, phát hiện lỗi sai phân cấp nhánh hoặc dùng quá nhiều chữ dài dòng; hỗ trợ gợi ý cấu trúc phân nhánh logic.",
          hs: "HS làm việc cá nhân phác thảo các nhánh (3 phút) -> Thảo luận cặp/nhóm (4 phút) hoàn thiện sơ đồ tư duy hoàn chỉnh."
        },
        step3: {
          gv: 'GV tổ chức trưng bày sơ đồ tư duy, mời đại diện thuyết minh mạch tư duy: "Hãy giải thích mối liên hệ logic giữa các nhánh trong sơ đồ của nhóm em".',
          hs: "HS thuyết minh sơ đồ trước lớp, các nhóm khác góp ý về tính mạch lạc và chuẩn xác kiến thức."
        },
        step4: {
          gv: "GV nhận xét, chuẩn hóa khung kiến thức dạng cây trên bảng, chốt sơ đồ chuẩn mực để ghi nhớ lâu dài.",
          hs: "HS hoàn thiện sơ đồ của mình vào vở ghi bài."
        }
      }
    },
    {
      id: "experiential",
      label: "Học tập trải nghiệm",
      description: "Học qua hoạt động thực hành, vận động",
      executionScript: {
        step1: {
          gv: 'GV giao nhiệm vụ thao tác thực nghiệm: "Các em hãy trực tiếp đo đạc/cắt dán/gấp hình/thực hiện thao tác...", phát dụng cụ và phiếu ghi chép trải nghiệm.',
          hs: "HS nhận dụng cụ, kiểm tra vật liệu và nắm rõ các bước thao tác."
        },
        step2: {
          gv: "GV quan sát quá trình thao tác thực nghiệm, phát hiện sai sót trong kỹ năng đo đạc/ghi chép số liệu; hỗ trợ trực tiếp các HS gặp khó khăn thao tác.",
          hs: "HS thực hiện thao tác cá nhân/theo cặp -> Ghi chép số liệu vào phiếu trải nghiệm -> Rút ra nhận xét ban đầu."
        },
        step3: {
          gv: 'GV yêu cầu HS chia sẻ kết quả trải nghiệm: "Qua quá trình thực hành, em phát hiện ra quy luật hoặc mối liên hệ nào?".',
          hs: "HS trình bày số liệu thực tế thu được, nêu dự đoán về quy luật chung."
        },
        step4: {
          gv: "GV chuyển hóa từ trực quan sinh động sang tư duy trừu tượng, chuẩn hóa công thức/định lý toán học và chốt ghi bảng.",
          hs: "HS ghi chép định lý/công thức chuẩn mực rút ra từ thực nghiệm vào vở."
        }
      }
    },
    {
      id: "5w1h",
      label: "Kỹ thuật 5W1H",
      description: "What, Why, When, Where, Who, How",
      executionScript: {
        step1: {
          gv: 'GV nêu khái niệm/tình huống và giao bảng câu hỏi 5W1H: "Hãy phân tích toàn diện vấn đề này qua 6 góc nhìn: Là gì (What), Tại sao (Why), Khi nào (When), Ở đâu (Where), Ai (Who), Như thế nào (How)...", phát phiếu mẫu.',
          hs: "HS tiếp nhận bảng câu hỏi 5W1H và chuẩn bị giấy nháp."
        },
        step2: {
          gv: "GV theo dõi cách HS trả lời từng câu hỏi, phát hiện lỗi: bỏ sót câu hỏi bản chất 'Why' và 'How'; gợi mở tư duy đa chiều.",
          hs: "HS làm việc cá nhân trả lời từng câu (2 phút) -> Thảo luận cặp (3 phút) hoàn thiện bảng phân tích 5W1H."
        },
        step3: {
          gv: 'GV mời đại diện trình bày câu trả lời cho từng khía cạnh 5W1H, khuyến khích lớp bổ sung góc nhìn mới.',
          hs: "HS báo cáo từng phần, tranh luận để làm rõ bản chất vấn đề."
        },
        step4: {
          gv: "GV tổng kết 6 khía cạnh thành bức tranh kiến thức hoàn chỉnh, chốt định nghĩa và quy tắc trọng tâm.",
          hs: "HS ghi chép nội dung chuẩn hóa vào vở theo cấu trúc 5W1H."
        }
      }
    },
    {
      id: "tps",
      label: "Think-Pair-Share",
      description: "Suy nghĩ cá nhân → Thảo luận cặp → Chia sẻ lớp",
      executionScript: {
        step1: {
          gv: 'GV nêu câu hỏi/vấn đề tư duy: "Các em có 2 phút suy nghĩ cá nhân (Think), 3 phút thảo luận cặp (Pair) và sau đó chia sẻ trước lớp (Share)...", giao nhiệm vụ rõ ràng.',
          hs: "HS lắng nghe, nhận nhiệm vụ và chuẩn bị giấy nháp."
        },
        step2: {
          gv: "GV quản lý thời gian nghiêm ngặt theo 2 pha: (1) Think (2 phút): HS làm việc độc lập ghi ý tưởng vào nháp; (2) Pair (3 phút): HS quay sang bạn cùng bàn trao đổi, đối chiếu và thống nhất câu trả lời. GV di chuyển nghe các cặp trao đổi, phát hiện ngộ nhận điển hình: ..., gợi mở cho cặp gặp khó khăn.",
          hs: "HS làm việc độc lập ghi lời giải vào nháp -> Trao đổi với bạn cùng bàn, phân tích điểm khác nhau và thống nhất câu trả lời chung của cặp."
        },
        step3: {
          gv: 'GV gọi ngẫu nhiên đại diện các cặp báo cáo (Share): "Cặp em đã thống nhất câu trả lời thế nào? Có điểm nào ban đầu hai bạn chưa đồng ý không?".',
          hs: "Đại diện cặp trình bày câu trả lời; các cặp khác nhận xét, bổ sung cách giải khác."
        },
        step4: {
          gv: "GV nhận xét, chính xác hóa câu trả lời, phân tích các sai lầm thường gặp trong quá trình thảo luận cặp và chốt kiến thức ghi bảng.",
          hs: "HS ghi chép lời giải chuẩn mực vào vở."
        }
      }
    },
    {
      id: "jigsaw",
      label: "Jigsaw (Mảnh ghép)",
      description: "Chia nhóm chuyên gia → ghép lại → dạy nhau",
      executionScript: {
        step1: {
          gv: 'GV chia lớp thành các "Nhóm chuyên gia" để nghiên cứu từng mảng kiến thức riêng biệt (Chuyên gia 1, 2, 3...): "Mỗi nhóm chuyên gia nghiên cứu sâu phần việc của mình để chuẩn bị dạy lại cho các bạn...", phát phiếu chuyên gia.',
          hs: "HS về đúng nhóm chuyên gia, nhận phiếu nhiệm vụ và phân công đọc hiểu tài liệu."
        },
        step2: {
          gv: "Vòng 1 (Nhóm chuyên gia - 5 phút): HS nghiên cứu cá nhân -> Thảo luận trong nhóm chuyên gia để thống nhất cách giải thích cho người khác. GV đến từng nhóm kiểm tra độ chính xác. Vòng 2 (Nhóm mảnh ghép - 6 phút): HS chuyển về nhóm mảnh ghép mới (mỗi nhóm gồm đủ đại diện từ các nhóm chuyên gia), từng chuyên gia lần lượt dạy lại phần mình phụ trách cho các bạn trong nhóm.",
          hs: "HS làm việc độc lập -> Thống nhất trong nhóm chuyên gia -> Di chuyển sang nhóm mảnh ghép, tự tin giảng lại phần mình phụ trách và lắng nghe phần kiến thức của các bạn khác."
        },
        step3: {
          gv: 'GV gọi ngẫu nhiên một HS trong nhóm mảnh ghép trình bày lại phần kiến thức do bạn khác vừa dạy để kiểm tra chất lượng truyền đạt: "Em hãy trình bày lại nội dung bạn A vừa chia sẻ cho nhóm em?".',
          hs: "HS được chỉ định trình bày lại kiến thức; thành viên chuyên gia lắng nghe và bổ sung nếu bạn nói thiếu."
        },
        step4: {
          gv: "GV tổng kết toàn bộ bức tranh kiến thức từ các mảnh ghép, giải đáp thắc mắc chung và chốt nội dung chuẩn mực lên bảng.",
          hs: "HS tổng hợp toàn bộ các phần kiến thức vào vở ghi."
        }
      }
    },
    {
      id: "gallery",
      label: "Gallery Walk",
      description: "Trình bày sản phẩm → đi tham quan → góp ý",
      executionScript: {
        step1: {
          gv: 'GV giao nhiệm vụ làm sản phẩm nhóm trên giấy A0/A1: "Các nhóm có 7 phút hoàn thành sản phẩm và 5 phút tham quan phòng tranh...", phát giấy A0, bút lông và giấy ghi chú (sticky note).',
          hs: "HS phân công nhiệm vụ trong nhóm, chuẩn bị dụng cụ viết và vẽ."
        },
        step2: {
          gv: "Pha 1: Nhóm tạo sản phẩm. GV bao quát, phát hiện lỗi sai về mặt kiến thức để nhắc nhở kịp thời. Pha 2: Các nhóm dán sản phẩm quanh lớp học; các thành viên di chuyển tham quan như trong phòng tranh, đọc sản phẩm của nhóm bạn và dán sticky note nhận xét/đặt câu hỏi.",
          hs: "HS hoàn thiện sản phẩm nhóm -> Treo sản phẩm lên vị trí quy định -> Di chuyển tham quan, đọc và dán giấy ghi chú góp ý/chất vấn vào sản phẩm nhóm bạn."
        },
        step3: {
          gv: 'GV yêu cầu các nhóm quay về sản phẩm của mình, đọc các nhận xét từ sticky note và phản hồi: "Nhóm em giải thích thế nào về câu hỏi của nhóm bạn trên sticky note?".',
          hs: "Đại diện nhóm đứng trước sản phẩm giải thích, trả lời các câu hỏi thắc mắc của bạn."
        },
        step4: {
          gv: "GV nhận xét chất lượng sản phẩm, thái độ tham quan và tinh thần góp ý, đánh giá sản phẩm xuất sắc và chốt kiến thức chuẩn mực.",
          hs: "HS hoàn thiện sản phẩm theo góp ý và ghi kiến thức cốt lõi vào vở."
        }
      }
    },
    {
      id: "kwl",
      label: "KWL",
      description: "Biết gì (K) → Muốn biết (W) → Đã học (L)",
      executionScript: {
        step1: {
          gv: 'GV kẻ bảng K-W-L và phát phiếu cho HS: "Hãy ghi vào cột K những điều em ĐÃ BIẾT và cột W những điều em MUỐN BIẾT về chủ đề hôm nay...", định hướng nội dung.',
          hs: "HS nhận phiếu KWL, suy ngẫm về kiến thức nền tảng và các câu hỏi tò mò của bản thân."
        },
        step2: {
          gv: "GV quan sát HS điền cột K và W (cá nhân 2 phút -> chia sẻ cặp 2 phút), phát hiện các hiểu lầm kiến thức cũ (ở cột K) và những câu hỏi có giá trị (ở cột W). Trong tiến trình bài học, HS tiếp tục tự ghi nhận vào cột L (ĐÃ HỌC ĐƯỢC).",
          hs: "HS điền cột K và W lúc mở đầu -> Lắng nghe bài học, thực hiện nhiệm vụ và điền kết quả vào cột L."
        },
        step3: {
          gv: 'GV mời HS chia sẻ cột K và W ở đầu giờ, và chia sẻ cột L ở cuối bài: "Em đã giải đáp được những câu hỏi nào ở cột W qua bài học hôm nay?".',
          hs: "HS đối chiếu cột W và cột L, tự đánh giá mức độ đạt mục tiêu của bản thân."
        },
        step4: {
          gv: "GV chuẩn hóa toàn bộ nội dung cốt lõi ở cột L, biểu dương sự tiến bộ từ K sang L của HS và chốt nội dung ghi bảng.",
          hs: "HS lưu phiếu KWL vào hồ sơ học tập và ghi chép nội dung chuẩn mực vào vở."
        }
      }
    },
    {
      id: "5e",
      label: "Mô hình 5E",
      description: "Engage-Explore-Explain-Elaborate-Evaluate",
      recommendFor: { subjects: ["khtn", "vatly", "hoahoc", "sinhhoc", "khoahoc"] },
      executionScript: {
        step1: {
          gv: 'Gắn kết (Engage): GV nêu hiện tượng/câu hỏi kích thích: "Quan sát hiện tượng sau, em thấy có điều gì bất thường?", tạo mâu thuẫn nhận thức.',
          hs: "HS quan sát, bộc lộ hiểu biết ban đầu và đặt ra các câu hỏi tìm tòi."
        },
        step2: {
          gv: "Khám phá (Explore) & Giải thích (Explain): GV phát phiếu hướng dẫn khám phá; HS thao tác/thí nghiệm/tính toán theo nhóm tạo sản phẩm trung gian. GV di chuyển phát hiện lỗi sai, hướng dẫn HS tự rút ra kết luận và giải thích cơ chế.",
          hs: "HS làm việc nhóm thu thập số liệu -> Phân tích kết quả -> Tự xây dựng lời giải thích khoa học cho vấn đề."
        },
        step3: {
          gv: 'Áp dụng (Elaborate): GV đưa bài tập vận dụng mới đòi hỏi áp dụng quy luật vừa khám phá. Đặt câu hỏi: "Quy luật này được ứng dụng thế nào trong tình huống mới?".',
          hs: "HS làm việc cá nhân/cặp giải quyết nhiệm vụ mới, báo cáo kết quả và phản biện trước lớp."
        },
        step4: {
          gv: "Đánh giá (Evaluate): GV tổ chức đánh giá (tự đánh giá, đánh giá đồng đẳng và GV nhận xét), chốt kiến thức chuẩn xác ghi bảng.",
          hs: "HS ghi chép kiến thức khoa học chuẩn mực vào vở."
        }
      }
    }
  ],
  techniques: [
    {
      id: "brainstorm",
      label: "Brainstorming/Động não",
      phases: ["A"],
      description: "Nêu ý tưởng nhanh để khởi động bài học",
      executionScript: {
        step1: {
          gv: 'GV nêu chủ đề/từ khóa kích thích: "Trong 2 phút, các em hãy liệt kê nhanh tất cả các ý tưởng/từ khóa liên quan đến...", khuyến khích mọi ý tưởng không phán xét.',
          hs: "HS lắng nghe chủ đề, chuẩn bị nháp hoặc bảng con."
        },
        step2: {
          gv: "GV quan sát HS viết ý tưởng cá nhân (1 phút) -> Thảo luận nhanh với bạn cùng bàn (1 phút), gom nhanh các ý tưởng độc đáo và phát hiện hiểu lầm ban đầu.",
          hs: "HS viết nhanh các ý tưởng cá nhân vào nháp -> Trao đổi chớp nhoáng với bạn cùng bàn."
        },
        step3: {
          gv: 'GV gọi HS nêu nhanh ý kiến nối tiếp nhau, ghi nhận toàn bộ lên bảng: "Có bạn nào có ý tưởng khác biệt hoặc bổ sung không?".',
          hs: "HS xung phong phát biểu ngắn gọn ý tưởng của mình; lớp lắng nghe và nhận diện các mối liên hệ."
        },
        step4: {
          gv: 'GV phân loại, tổng hợp các ý tưởng trên bảng, khéo léo dẫn dắt vào bài mới: "Để kiểm chứng và hoàn thiện các ý tưởng trên, chúng ta cùng nghiên cứu bài học hôm nay...".',
          hs: "HS ghi tên bài học và định hướng khám phá vào vở."
        }
      }
    },
    {
      id: "kwl-tech",
      label: "KWL",
      phases: ["A"],
      description: "Biết gì → Muốn biết → Đã học",
      executionScript: {
        step1: {
          gv: 'GV kẻ bảng K-W-L lên bảng và phát phiếu KWL: "Hãy ghi nhanh những điều em ĐÃ BIẾT (K) và những điều em MUỐN BIẾT (W) về chủ đề...", hướng dẫn cụ thể.',
          hs: "HS tiếp nhận phiếu KWL, suy nghĩ về kiến thức nền đã có."
        },
        step2: {
          gv: "GV quan sát HS điền cột K và W (cá nhân 2 phút -> trao đổi cặp 1 phút), phát hiện các lỗ hổng kiến thức cũ và câu hỏi tò mò hay.",
          hs: "HS điền độc lập vào cột K và W trên phiếu cá nhân -> Trao đổi nhanh với bạn bên cạnh."
        },
        step3: {
          gv: 'GV mời một số HS chia sẻ điều mình đã biết và muốn biết: "Ai muốn chia sẻ câu hỏi ở cột W của mình trước lớp?".',
          hs: "HS trình bày ý kiến; lớp lắng nghe các câu hỏi hay cần giải đáp trong bài."
        },
        step4: {
          gv: 'GV ghi nhận các câu hỏi tiêu biểu lên góc bảng, tạo động lực tìm kiếm câu trả lời trong bài học: "Chúng ta sẽ cùng tìm câu trả lời cho các câu hỏi ở cột W trong suốt bài học hôm nay...".',
          hs: "HS ghi nhớ mục tiêu học tập và sẵn sàng cho các hoạt động tiếp theo."
        }
      }
    },
    {
      id: "stim-question",
      label: "Câu hỏi kích thích tư duy",
      phases: ["A"],
      description: "Câu hỏi gợi mở, tạo mâu thuẫn nhận thức",
      executionScript: {
        step1: {
          gv: 'GV đưa ra câu hỏi nghịch lý/tình huống có vấn đề: "Liệu có thể xảy ra trường hợp... không? Điều này có luôn luôn đúng không?", kích thích sự tò mò.',
          hs: "HS tiếp nhận câu hỏi, suy nghĩ độc lập tìm câu trả lời."
        },
        step2: {
          gv: "GV quan sát HS suy nghĩ và ghi dự đoán cá nhân vào nháp (2 phút), phát hiện hai luồng ý kiến trái ngược nhau trong lớp.",
          hs: "HS phân tích câu hỏi, ghi câu trả lời dự đoán và lý do ngắn gọn vào nháp."
        },
        step3: {
          gv: 'GV mời đại diện hai luồng ý kiến trái chiều tranh luận: "Em hãy bảo vệ quan điểm dự đoán của mình trước lớp?".',
          hs: "HS trình bày dự đoán, đối thoại và phản biện lẫn nhau tạo nên mâu thuẫn nhận thức sôi nổi."
        },
        step4: {
          gv: 'GV không chốt đúng sai ngay mà giữ lại mâu thuẫn để dẫn dắt: "Để biết câu trả lời chính xác, chúng ta cùng bước vào bài học hôm nay...".',
          hs: "HS ghi tên bài vào vở với tâm thế háo hức khám phá chân lý."
        }
      }
    },
    {
      id: "wordgame",
      label: "Trò chơi ô chữ/đố vui",
      phases: ["A"],
      description: "Khởi động bằng trò chơi ngôn ngữ",
      executionScript: {
        step1: {
          gv: 'GV giới thiệu luật chơi ô chữ/đố vui: "Mỗi hàng ngang tương ứng một câu hỏi gợi nhớ kiến thức cũ, từ khóa bí mật hàng dọc chính là chủ đề bài mới...", trình chiếu ô chữ.',
          hs: "HS lắng nghe luật chơi, chuẩn bị sẵn sàng xung phong trả lời."
        },
        step2: {
          gv: "GV lần lượt đọc câu hỏi gợi ý hàng ngang, quan sát độ nhạy bén của HS, phát hiện kiến thức cũ HS còn nhầm lẫn và giải thích nhanh.",
          hs: "HS suy nghĩ cá nhân (30 giây) -> Giơ tay giành quyền trả lời từng hàng ngang."
        },
        step3: {
          gv: 'GV mở từng mảnh ghép hàng ngang; mời HS đoán từ khóa hàng dọc: "Ai đã tìm ra từ khóa hàng dọc và giải thích ý nghĩa?".',
          hs: "HS trả lời từ khóa hàng dọc và nêu hiểu biết sơ bộ về từ khóa đó."
        },
        step4: {
          gv: 'GV chúc mừng HS, chốt ý nghĩa của từ khóa và dẫn nhập vào bài mới: "Từ khóa chính là nội dung trọng tâm chúng ta sẽ cùng khám phá trong bài...".',
          hs: "HS ghi tên bài học vào vở ghi."
        }
      }
    },
    {
      id: "tps-tech",
      label: "Think-Pair-Share",
      phases: ["B"],
      description: "Suy nghĩ cá nhân → thảo luận cặp → chia sẻ lớp",
      executionScript: {
        step1: {
          gv: 'GV nêu câu hỏi/nhiệm vụ khám phá: "Các em có 2 phút suy nghĩ cá nhân (Think), 3 phút thảo luận cặp (Pair) và sau đó chia sẻ trước lớp (Share)...", phát phiếu học tập nếu có.',
          hs: "HS tiếp nhận câu hỏi khám phá, chuẩn bị nháp và phiếu học tập."
        },
        step2: {
          gv: "GV kiểm soát 2 pha: (1) Think (2 phút): HS độc lập tính toán/suy nghĩ vào nháp; (2) Pair (3 phút): HS trao đổi với bạn cùng bàn so sánh kết quả. GV di chuyển nghe các cặp trao đổi, phát hiện lỗi sai điển hình: ..., gợi ý cho các cặp gặp vướng mắc.",
          hs: "HS làm việc độc lập ghi lời giải vào nháp -> Quay sang bạn cùng bàn trao đổi, giải thích cách làm và thống nhất sản phẩm trung gian của cặp."
        },
        step3: {
          gv: 'GV gọi ngẫu nhiên một số cặp báo cáo: "Cặp em đã thống nhất câu trả lời như thế nào? Có điểm nào ban đầu hai bạn bất đồng ý kiến không?".',
          hs: "Đại diện cặp trình bày câu trả lời; các cặp khác nhận xét, bổ sung cách tiếp cận khác."
        },
        step4: {
          gv: "GV nhận xét, chính xác hóa câu trả lời, phân tích bản chất toán học/khoa học và chốt nội dung ghi bảng.",
          hs: "HS hoàn thiện vở ghi với kiến thức và công thức chuẩn hóa."
        }
      }
    },
    {
      id: "jigsaw-tech",
      label: "Jigsaw/Mảnh ghép",
      phases: ["B"],
      description: "Nhóm chuyên gia rồi ghép lại, dạy nhau",
      executionScript: {
        step1: {
          gv: 'GV chia lớp thành các "Nhóm chuyên gia" để tìm hiểu các đơn vị kiến thức khác nhau (Nhóm 1: Nội dung A, Nhóm 2: Nội dung B...): "Mỗi nhóm chuyên gia hãy làm chủ nội dung của mình để lát nữa dạy lại cho bạn...", phát phiếu chuyên gia.',
          hs: "HS di chuyển về nhóm chuyên gia, nhận phiếu nhiệm vụ và phân công nghiên cứu."
        },
        step2: {
          gv: "Vòng 1 (Chuyên gia - 5 phút): HS cá nhân đọc hiểu -> Thảo luận nhóm chuyên gia thống nhất cách giải thích. GV đến từng nhóm kiểm tra độ chuẩn xác. Vòng 2 (Mảnh ghép - 6 phút): HS lập nhóm mới có đủ đại diện các chuyên gia, từng bạn lần lượt giảng lại phần của mình cho nhóm.",
          hs: "HS làm việc cá nhân -> Thống nhất trong nhóm chuyên gia -> Về nhóm mảnh ghép mới, đóng vai người dạy giảng giải kiến thức cho các bạn khác và lắng nghe các phần còn lại."
        },
        step3: {
          gv: 'GV gọi ngẫu nhiên một HS trong nhóm mảnh ghép trình bày lại phần kiến thức do bạn khác dạy: "Em hãy tóm tắt lại nội dung bạn vừa dạy cho nhóm em?".',
          hs: "HS được chỉ định trình bày lại kiến thức; chuyên gia phụ trách phần đó nhận xét xem bạn đã hiểu đúng chưa."
        },
        step4: {
          gv: "GV tổng hợp toàn bộ các đơn vị kiến thức thành bức tranh hoàn chỉnh, chuẩn hóa các định nghĩa/công thức và chốt ghi bảng.",
          hs: "HS ghi chép toàn bộ kiến thức hoàn chỉnh vào vở."
        }
      }
    },
    {
      id: "gallery-tech",
      label: "Gallery Walk",
      phases: ["B"],
      description: "Trưng bày sản phẩm, đi tham quan, góp ý",
      executionScript: {
        step1: {
          gv: 'GV giao nhiệm vụ xây dựng sản phẩm kiến thức trên giấy A0/A1: "Các nhóm có 7 phút tạo sản phẩm và 5 phút tham quan triển lãm...", phát giấy A0, bút dạ và sticky note.',
          hs: "HS nhận dụng cụ, phân công nhiệm vụ viết/vẽ sơ đồ kiến thức trong nhóm."
        },
        step2: {
          gv: "Pha 1: Nhóm thực hiện sản phẩm trung gian trên giấy A0. GV bao quát nhắc nhở lỗi sai kiến thức. Pha 2: Các nhóm dán sản phẩm quanh phòng học, HS di chuyển tham quan theo vòng tròn, đọc và dán sticky note nhận xét/chất vấn.",
          hs: "HS hoàn thành sản phẩm -> Treo lên tường lớp -> Di chuyển tham quan phòng tranh, đọc sản phẩm nhóm bạn và dán sticky note nhận xét."
        },
        step3: {
          gv: 'GV yêu cầu các nhóm quay về vị trí sản phẩm của mình, đọc các câu hỏi trên sticky note và trả lời: "Nhóm em giải thích thế nào về thắc mắc của nhóm bạn?".',
          hs: "Đại diện nhóm đứng trước sản phẩm giải thích, làm rõ các thắc mắc của bạn cùng lớp."
        },
        step4: {
          gv: "GV nhận xét chất lượng sản phẩm và tinh thần đóng góp ý kiến của các nhóm, chuẩn hóa kiến thức trọng tâm lên bảng.",
          hs: "HS sửa bài theo góp ý và chép nội dung chuẩn mực vào vở."
        }
      }
    },
    {
      id: "station",
      label: "Trạm học tập/Station Rotation",
      phases: ["B"],
      description: "Luân phiên nhiệm vụ theo trạm",
      recommendFor: { maxClassSize: 45 },
      executionScript: {
        step1: {
          gv: 'GV bố trí các trạm học tập trong lớp (Trạm 1: Khái niệm, Trạm 2: Tính chất/Quy tắc, Trạm 3: Ví dụ mẫu...), phổ biến quy tắc xoay trạm và phát Phiếu học tập theo trạm: "Mỗi nhóm có 5-7 phút tại mỗi trạm, khi có chuông báo hiệu sẽ di chuyển theo chiều kim đồng hồ...", hướng dẫn chi tiết.',
          hs: "HS nhận phiếu học tập trạm, di chuyển về trạm xuất phát được phân công."
        },
        step2: {
          gv: "Các nhóm thực hiện nhiệm vụ tại trạm (Đọc lệnh trạm -> Cá nhân làm -> Thảo luận nhóm -> Ghi phiếu). GV di chuyển giữa các trạm, phát hiện trạm học sinh gặp khó khăn nhất để kịp thời can thiệp hướng dẫn, hỗ trợ phân hóa cho nhóm chậm.",
          hs: "HS đọc lệnh tại trạm, thao tác cá nhân rồi thảo luận nhóm hoàn thành phiếu trạm; di chuyển trạm nhanh chóng khi có hiệu lệnh chuông."
        },
        step3: {
          gv: 'Sau khi hoàn thành đủ các trạm, GV gọi mỗi nhóm báo cáo kết quả của 1 trạm: "Nhóm 2 hãy trình bày kết quả khám phá tại Trạm 1; Nhóm 4 nhận xét".',
          hs: "Đại diện nhóm báo cáo kết quả trạm; các nhóm khác đối chiếu với phiếu của mình và bổ sung."
        },
        step4: {
          gv: "GV hệ thống hóa toàn bộ kiến thức thu được từ các trạm, giải đáp khó khăn chung và chốt nội dung chuẩn mực ghi bảng.",
          hs: "HS hoàn thiện phiếu trạm và ghi chép kiến thức cốt lõi vào vở."
        }
      }
    },
    {
      id: "mindmap-tech",
      label: "Sơ đồ tư duy",
      phases: ["B"],
      description: "Tổ chức kiến thức dạng cây",
      executionScript: {
        step1: {
          gv: 'GV giao nhiệm vụ sơ đồ hóa kiến thức mới: "Hãy hệ thống hóa các định nghĩa, quy tắc vừa khám phá thành sơ đồ tư duy có phân nhánh rõ ràng...", phát giấy và bút màu.',
          hs: "HS chuẩn bị giấy vẽ và bút màu, xác định từ khóa trung tâm."
        },
        step2: {
          gv: "GV quan sát HS vẽ sơ đồ, phát hiện các lỗi sai logic trong phân nhánh hoặc biểu diễn thiếu liên kết; hỗ trợ phân hóa cấu trúc cây.",
          hs: "HS làm việc cá nhân phác thảo nhánh (2 phút) -> Thảo luận cặp hoàn thiện sơ đồ tư duy hoàn chỉnh (4 phút)."
        },
        step3: {
          gv: 'GV mời 2 HS đại diện chiếu sơ đồ hoặc vẽ lên bảng, yêu cầu lớp nhận xét: "Sơ đồ của bạn đã thể hiện đủ các nhánh kiến thức chưa?".',
          hs: "HS thuyết minh sơ đồ tư duy của mình trước lớp; các bạn khác nhận xét, góp ý."
        },
        step4: {
          gv: "GV nhận xét, chuẩn hóa sơ đồ mẫu chuẩn mực trên bảng, chốt các công thức và quy tắc cốt lõi.",
          hs: "HS hoàn thiện sơ đồ tư duy vào vở ghi."
        }
      }
    },
    {
      id: "tablecloth",
      label: "Khăn trải bàn",
      phases: ["B"],
      description: "Ý kiến cá nhân rồi thống nhất nhóm",
      executionScript: {
        step1: {
          gv: 'GV phát giấy khổ lớn A0/A1 chia 4 góc và ô trung tâm: "Mỗi bạn có 3 phút ghi ý kiến độc lập vào góc của mình, sau đó nhóm có 4 phút thảo luận để thống nhất ghi vào ô giữa...", giao nhiệm vụ khám phá.',
          hs: "HS nhận giấy và bút viết, xác định góc làm việc cá nhân của mình."
        },
        step2: {
          gv: "Pha 1 (Cá nhân - 3 phút): HS suy nghĩ và viết độc lập vào góc riêng. Pha 2 (Nhóm - 4 phút): Nhóm trao đổi, lọc bỏ ý kiến sai, thống nhất câu trả lời chuẩn xác ghi vào ô trung tâm. GV quan sát, phát hiện lỗi sai/ý kiến sai điển hình: ..., gợi ý nhóm phản biện.",
          hs: "HS làm việc độc lập viết vào góc cá nhân -> Thảo luận nhóm, tranh luận và thống nhất câu trả lời tối ưu vào ô giữa khăn trải bàn."
        },
        step3: {
          gv: 'GV mời đại diện nhóm treo bảng Khăn trải bàn và báo cáo: "Vì sao nhóm em chọn câu trả lời ở ô giữa? Nhóm đã loại bỏ những ý kiến chưa đúng nào ở các góc?".',
          hs: "Đại diện nhóm trình bày nội dung ô trung tâm và giải thích quá trình thống nhất ý kiến; lớp theo dõi và phản biện."
        },
        step4: {
          gv: "GV nhận xét quá trình làm việc cá nhân và thống nhất nhóm, chốt kiến thức chuẩn mực vào cột nội dung ghi bảng.",
          hs: "HS ghi nhận kiến thức chuẩn mực vào vở."
        }
      }
    },
    {
      id: "diff-ex",
      label: "Bài tập phân hóa 3 mức",
      phases: ["C"],
      description: "Nhiệm vụ theo mức sẵn sàng",
      executionScript: {
        step1: {
          gv: 'GV giao hệ thống bài tập phân hóa 3 mức (Mức 1: Cơ bản, Mức 2: Vận dụng, Mức 3: Nâng cao): "Tất cả các em làm Mức 1, sau đó tự chọn thử thách Mức 2 hoặc 3...", quy định thời gian làm bài.',
          hs: "HS nhận đề bài, xác định mục tiêu và chọn mức độ bài tập."
        },
        step2: {
          gv: "GV di chuyển bao quát lớp, trực tiếp hướng dẫn và sửa lỗi sai cơ bản cho HS yếu (ở Mức 1); gợi ý phương pháp tư duy nâng cao cho HS khá giỏi (ở Mức 3), ghi nhận các lỗi sai điển hình: ...",
          hs: "HS giải bài tập cá nhân vào vở (8-10 phút) -> Trao đổi nhanh với bạn cùng bàn để kiểm tra chéo đáp án."
        },
        step3: {
          gv: 'GV gọi 3 HS đại diện cho 3 mức độ lên bảng trình bày: "Hãy giải thích rõ các bước biến đổi trong bài giải của em".',
          hs: "HS lên bảng trình bày bài giải; cả lớp theo dõi, nhận xét và phát hiện các cách giải ngắn gọn hơn."
        },
        step4: {
          gv: "GV nhận xét chi tiết bài giải của từng mức, chỉ rõ các lỗi sai thường gặp khi làm bài kiểm tra, chốt phương pháp giải chuẩn mực.",
          hs: "HS sửa bài vào vở theo đúng mức độ của mình và ghi chú các lưu ý quan trọng."
        }
      }
    },
    {
      id: "peer",
      label: "Đánh giá đồng đẳng/Peer Assessment",
      phases: ["C"],
      description: "Phản hồi theo tiêu chí",
      executionScript: {
        step1: {
          gv: 'GV giao bài tập luyện tập và bảng tiêu chí chấm điểm (Rubrics): "Sau khi làm xong bài trong 7 phút, các em sẽ đổi vở cho bạn cùng bàn để chấm chéo theo tiêu chí...", phổ biến thang điểm cụ thể.',
          hs: "HS nhận đề bài và tiêu chí chấm, chuẩn bị làm bài cá nhân."
        },
        step2: {
          gv: "HS làm bài cá nhân vào vở (7 phút). Sau đó đổi vở theo cặp, đối chiếu bài của bạn với đáp án/tiêu chí, dùng bút chì chấm điểm và ghi nhận xét lỗi sai (3 phút). GV quan sát, hỗ trợ giải quyết bất đồng chấm điểm giữa các cặp.",
          hs: "HS làm bài độc lập -> Đổi vở chấm chéo theo thang điểm tiêu chí -> Ghi nhận xét chi tiết vào vở bạn."
        },
        step3: {
          gv: 'GV mời một số cặp báo cáo kết quả chấm chéo: "Em đã chấm bạn bao nhiêu điểm? Bạn làm tốt ở bước nào và mắc lỗi sai ở đâu?".',
          hs: "HS giải thích kết quả chấm chéo; bạn được chấm phản hồi ý kiến."
        },
        step4: {
          gv: "GV nhận xét tinh thần chấm chéo khách quan của HS, giải đáp các thắc mắc chung và chốt đáp án chuẩn mực ghi bảng.",
          hs: "HS nhận lại vở, tự sửa lại các bước sai sót vào vở ghi."
        }
      }
    },
    {
      id: "debate",
      label: "Tranh luận có cấu trúc",
      phases: ["C"],
      description: "Lập luận có bằng chứng",
      recommendFor: { subjects: ["nguvan", "tiengviet", "tienganh", "gdcd", "daoduc", "gdktpl", "lichsu", "lichsudialy"] },
      executionScript: {
        step1: {
          gv: 'GV đưa ra bài toán/tình huống có 2 luồng quan điểm trái chiều: "Phe A bảo vệ quan điểm 1, Phe B bảo vệ quan điểm 2...", chia phe và phổ biến luật tranh luận (thời gian lập luận, phản bác, kết luận).',
          hs: "HS nhận phe tranh luận, phân công người phát ngôn và chuẩn bị luận cứ."
        },
        step2: {
          gv: "Các phe hội ý nội bộ (3 phút) chuẩn bị bằng chứng logic/toán học và dự đoán đòn phản bác. GV di chuyển lắng nghe, gợi mở cấu trúc lập luận chặt chẽ cho cả hai phe.",
          hs: "HS thảo luận trong phe, ghi các luận điểm và bằng chứng xác đáng vào giấy nháp."
        },
        step3: {
          gv: 'GV điều hành phiên tranh luận: Phe A nêu luận điểm (1.5 phút) -> Phe B chất vấn/phản bác (1.5 phút) -> Đổi ngược lại -> Tự do tranh luận (2 phút).',
          hs: "Đại diện các phe trình bày lập luận có căn cứ, chất vấn và bảo vệ quan điểm trước lớp."
        },
        step4: {
          gv: "GV nhận định phiên tranh luận, phân tích tính đúng đắn khoa học của từng quan điểm, chỉ ra các lỗi ngụy biện/lập luận thiếu căn cứ, chốt kết luận chuẩn mực.",
          hs: "HS ghi nhận kết luận logic và bài học phương pháp vào vở."
        }
      }
    },
    {
      id: "case",
      label: "Case Study",
      phases: ["C"],
      description: "Phân tích tình huống",
      executionScript: {
        step1: {
          gv: 'GV phát tài liệu tình huống thực tế (Case study): "Hãy đọc kĩ tình huống thực tế sau và trả lời các câu hỏi định hướng...", giao nhiệm vụ phân tích.',
          hs: "HS nhận tài liệu case study, đọc và gạch chân các dữ liệu quan trọng."
        },
        step2: {
          gv: "HS làm việc cá nhân phân tích tình huống (3 phút) -> Thảo luận nhóm giải quyết các câu hỏi định hướng (5 phút). GV quan sát, phát hiện các nhóm hiểu sai dữ liệu hoặc áp dụng sai công thức, can thiệp gợi mở.",
          hs: "HS phân tích số liệu cá nhân -> Thảo luận nhóm thống nhất giải pháp tối ưu cho tình huống."
        },
        step3: {
          gv: 'GV mời đại diện các nhóm trình bày giải pháp cho case study: "Dựa vào căn cứ nào mà nhóm em đưa ra quyết định/giải pháp này?".',
          hs: "Đại diện nhóm trình bày giải pháp; các nhóm khác nhận xét và chất vấn."
        },
        step4: {
          gv: "GV tổng kết case study, rút ra bài học lý thuyết gắn liền với ứng dụng đời sống, chốt công thức/quy tắc chuẩn mực.",
          hs: "HS ghi chép các bài học kinh nghiệm và kiến thức chuẩn mực vào vở."
        }
      }
    },
    {
      id: "roleplay",
      label: "Role-play/Đóng vai",
      phases: ["C"],
      description: "Thực hành vai trò",
      recommendFor: { subjects: ["nguvan", "tiengviet", "tienganh", "gdcd", "daoduc", "gdktpl", "lichsu", "lichsudialy"] },
      executionScript: {
        step1: {
          gv: 'GV giao kịch bản tình huống đóng vai: "Mỗi nhóm chuẩn bị tiểu phẩm ngắn 2 phút ứng dụng kiến thức bài học để xử lý tình huống...", phân chia vai trò.',
          hs: "HS nhận vai, tìm hiểu bối cảnh và chuẩn bị lời thoại gắn với bài học."
        },
        step2: {
          gv: "Các nhóm phân vai và tập dượt xử lý tình huống (4 phút). GV quan sát, nhắc nhở HS lồng ghép chuẩn xác các thuật ngữ và kiến thức bài học vào lời thoại.",
          hs: "HS tập đóng vai trong nhóm, chuẩn bị các lập luận và hành vi phù hợp với vai diễn."
        },
        step3: {
          gv: 'GV mời 1-2 nhóm lên thể hiện tiểu phẩm trước lớp. Các HS khác theo dõi, ghi chép lại cách xử lý tình huống của bạn.',
          hs: "HS đóng vai trước lớp; lớp theo dõi, ghi chép nhận xét."
        },
        step4: {
          gv: "GV cùng cả lớp nhận xét tính chính xác về mặt kiến thức và sự sáng tạo trong diễn xuất, chốt bài học thực tiễn.",
          hs: "HS ghi nhớ bài học và chép nội dung cốt lõi vào vở."
        }
      }
    },
    {
      id: "mini-project",
      label: "Dự án mini",
      phases: ["D"],
      description: "Sản phẩm ngắn vận dụng kiến thức",
      executionScript: {
        step1: {
          gv: 'GV giao nhiệm vụ dự án mini: "Hãy thiết kế một sản phẩm nhỏ (bảng tính chi tiêu, mô hình hình học, infographic tuyên truyền...) áp dụng kiến thức vừa học...", phát tiêu chí sản phẩm.',
          hs: "HS tiếp nhận nhiệm vụ dự án mini, tìm hiểu tiêu chí đánh giá."
        },
        step2: {
          gv: "HS làm việc cá nhân hoặc theo cặp lên ý tưởng và phác thảo đề cương sản phẩm (hoàn thành trên lớp hoặc làm tiếp ở nhà). GV hướng dẫn các bước thực hiện, gợi ý nguồn học liệu an toàn.",
          hs: "HS phác thảo ý tưởng, tính toán các thông số cần thiết cho sản phẩm mini."
        },
        step3: {
          gv: 'HS báo cáo ý tưởng sản phẩm mini trước lớp: "Sản phẩm của em giải quyết vấn đề gì trong cuộc sống và ứng dụng kiến thức nào đã học?".',
          hs: "HS trình bày ý tưởng/mẫu sản phẩm; lớp lắng nghe và góp ý hoàn thiện."
        },
        step4: {
          gv: "GV đánh giá sự sáng tạo và tính ứng dụng của sản phẩm, chốt lại giá trị thực tiễn của bài học.",
          hs: "HS ghi nhận nhiệm vụ hoàn thiện sản phẩm vào vở ghi."
        }
      }
    },
    {
      id: "journal",
      label: "Viết nhật ký học tập",
      phases: ["D"],
      description: "Tự phản ánh điều đã học",
      executionScript: {
        step1: {
          gv: 'GV nêu câu hỏi định hướng tự phản ánh: "Hôm nay em đã học được điều gì quan trọng nhất? Điều gì em còn thấy băn khoăn hoặc làm tốt nhất?", phát mẫu nhật ký học tập.',
          hs: "HS chuẩn bị sổ nhật ký học tập hoặc giấy ghi chép cá nhân."
        },
        step2: {
          gv: "HS dành 3-5 phút viết độc lập câu trả lời chân thật vào sổ nhật ký học tập. GV quan sát trong không gian yên tĩnh, tôn trọng suy nghĩ cá nhân của HS.",
          hs: "HS viết phản ánh cá nhân về quá trình học tập, nhận diện điểm mạnh và điểm cần cải thiện."
        },
        step3: {
          gv: 'GV mời 2-3 HS tình nguyện đọc to đoạn nhật ký của mình trước lớp.',
          hs: "HS chia sẻ cảm xúc và thu hoạch học tập của bản thân; lớp lắng nghe đồng cảm."
        },
        step4: {
          gv: "GV ghi nhận và động viên tinh thần tự phản ánh của HS, chốt lời dặn dò tiếp theo.",
          hs: "HS đóng sổ nhật ký và cất vào hồ sơ cá nhân."
        }
      }
    },
    {
      id: "exit",
      label: "Exit Ticket",
      phases: ["D"],
      description: "Ghi nhận nhanh mức độ đạt",
      executionScript: {
        step1: {
          gv: 'GV phát phiếu Exit Ticket (gồm 1-2 câu hỏi chốt kiến thức và tự đánh giá): "Các em hoàn thành phiếu này trong 3 phút và nộp lại cho thầy/cô trước khi rời lớp...", định hướng làm bài.',
          hs: "HS nhận phiếu Exit Ticket, chuẩn bị bút viết."
        },
        step2: {
          gv: "HS làm bài độc lập, ghi rõ họ tên và đáp án vào phiếu (3 phút). GV đứng tại cửa hoặc đi bao quát thu phiếu, quan sát nhanh tỉ lệ làm đúng.",
          hs: "HS hoàn thành phiếu Exit Ticket hoàn toàn độc lập và nộp lại cho GV."
        },
        step3: {
          gv: 'GV phản hồi nhanh tổng quan không khí làm bài của lớp: "Thầy/cô nhận thấy đa số các em đã nắm vững phần...".',
          hs: "HS lắng nghe nhận xét nhanh của GV."
        },
        step4: {
          gv: "GV dặn dò nhiệm vụ về nhà dựa trên khảo sát Exit Ticket.",
          hs: "HS rời lớp sau khi đã nộp phiếu cho GV."
        }
      }
    },
    {
      id: "open-ex",
      label: "Bài tập mở",
      phases: ["D"],
      description: "Nhiều cách tiếp cận, vận dụng linh hoạt",
      executionScript: {
        step1: {
          gv: 'GV giao bài tập mở (nhiều đáp án hoặc nhiều hướng tiếp cận): "Bài toán này không có một đáp án duy nhất, các em hãy tìm ít nhất 2 cách tiếp cận khác nhau...", giao đề.',
          hs: "HS ghi nhận đề bài, đọc và suy nghĩ các hướng tiếp cận."
        },
        step2: {
          gv: "HS suy nghĩ cá nhân tìm tòi các phương án giải độc đáo (4-5 phút). GV di chuyển gợi mở tư duy phi truyền thống, khuyến khích các ý tưởng đột phá.",
          hs: "HS tìm tòi các cách giải khác nhau, ghi vào nháp."
        },
        step3: {
          gv: 'GV mời các HS có cách giải khác nhau lên bảng trình bày: "Vì sao em lại tiếp cận theo hướng này?".',
          hs: "HS trình bày các cách tiếp cận sáng tạo; lớp thảo luận so sánh tính tối ưu."
        },
        step4: {
          gv: "GV khẳng định vẻ đẹp của tư duy đa chiều trong môn học, chốt lại các nguyên lý nền tảng.",
          hs: "HS ghi lại các cách giải hay vào vở."
        }
      }
    }
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

function getPedagogyExecutionScript(type, id) {
  if (!type || !id) return null;
  const list = KHBD_PEDAGOGY_CATALOG[type];
  if (!Array.isArray(list)) return null;
  const item = list.find(it => it.id === id);
  return item?.executionScript || null;
}

function buildDetailedPedagogyGuide(phase, context = {}) {
  const selected = context.phasePedagogy?.[phase] || {};
  const techIds = selected.techniques || [];
  const methodIds = context.methods || [];
  
  const techItems = techIds.map(id => (KHBD_PEDAGOGY_CATALOG.techniques || []).find(t => t.id === id)).filter(Boolean);
  const methodItems = methodIds.map(id => (KHBD_PEDAGOGY_CATALOG.methods || []).find(m => m.id === id)).filter(Boolean);

  const guides = [];

  if (techItems.length > 0) {
    guides.push(`\n=== KỊCH BẢN THỰC CHIẾN KỸ THUẬT DẠY HỌC (Pha ${phase}) ===`);
    techItems.forEach(item => {
      guides.push(`\n[Kỹ thuật: ${item.label}] - ${item.description || ""}`);
      if (item.executionScript) {
        const s = item.executionScript;
        if (s.step1) guides.push(`+ Bước 1 (Chuyển giao): GV: ${s.step1.gv} | HS: ${s.step1.hs}`);
        if (s.step2) guides.push(`+ Bước 2 (Thực hiện): GV: ${s.step2.gv} | HS: ${s.step2.hs}`);
        if (s.step3) guides.push(`+ Bước 3 (Báo cáo): GV: ${s.step3.gv} | HS: ${s.step3.hs}`);
        if (s.step4) guides.push(`+ Bước 4 (Kết luận): GV: ${s.step4.gv} | HS: ${s.step4.hs}`);
      }
    });
  }

  if (methodItems.length > 0) {
    guides.push(`\n=== KỊCH BẢN THỰC CHIẾN PHƯƠNG PHÁP DẠY HỌC ===`);
    methodItems.forEach(item => {
      guides.push(`\n[Phương pháp: ${item.label}] - ${item.description || ""}`);
      if (item.executionScript) {
        const s = item.executionScript;
        if (s.step1) guides.push(`+ Bước 1 (Chuyển giao): GV: ${s.step1.gv} | HS: ${s.step1.hs}`);
        if (s.step2) guides.push(`+ Bước 2 (Thực hiện): GV: ${s.step2.gv} | HS: ${s.step2.hs}`);
        if (s.step3) guides.push(`+ Bước 3 (Báo cáo): GV: ${s.step3.gv} | HS: ${s.step3.hs}`);
        if (s.step4) guides.push(`+ Bước 4 (Kết luận): GV: ${s.step4.gv} | HS: ${s.step4.hs}`);
      }
    });
  }

  return guides.join("\n");
}

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
  module.exports = {
    KHBD_PEDAGOGY_CATALOG,
    isPedagogyRecommended,
    recommendPedagogyFromLesson,
    getPedagogyExecutionScript,
    buildDetailedPedagogyGuide
  };
}

if (typeof window !== "undefined") {
  window.KHBD_PEDAGOGY_CATALOG = KHBD_PEDAGOGY_CATALOG;
  window.isPedagogyRecommended = isPedagogyRecommended;
  window.recommendPedagogyFromLesson = recommendPedagogyFromLesson;
  window.getPedagogyExecutionScript = getPedagogyExecutionScript;
  window.buildDetailedPedagogyGuide = buildDetailedPedagogyGuide;
}
