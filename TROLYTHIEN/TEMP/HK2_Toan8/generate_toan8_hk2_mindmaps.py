# -*- coding: utf-8 -*-
"""
Script sinh 17 Sơ đồ tư duy Mindmap vector 300 DPI cho môn Toán 8 Học kì II
Thầy Hoàng Tấn Thiên - Năm học 2026 - 2027
"""

import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

output_dir = "TROLYTHIEN/TEMP/HK2_Toan8/mindmaps"
os.makedirs(output_dir, exist_ok=True)

mindmaps_data = [
    # 1. Đại số - Tiết 47
    {
        "filename": "mindmap_toan8_tiet47.png",
        "title": "SƠ ĐỒ TƯ DUY: PHÂN THỨC ĐẠI SỐ (TIẾT 47)",
        "center": "PHÂN THỨC\nĐẠI SỐ",
        "branches": [
            ("1. ĐỊNH NGHĨA", "Biểu thức dạng A/B với A, B là đa thức; B khác 0 đa thức không.\nA là tử thức, B là mẫu thức.\nĐK xác định: B khác 0."),
            ("2. HAI PHÂN THỨC BẰNG NHAU", "A/B = C/D nếu A.D = B.C\nKiểm tra tích chéo bằng nhau."),
            ("3. TÍNH CHẤT CƠ BẢN", "A/B = (A.M)/(B.M) với M khác 0.\nA/B = (A:N)/(B:N) với N là nhân tử chung.\nQuy tắc đổi dấu: A/B = -A/(-B)."),
            ("4. RÚT GỌN & QUY ĐỒNG", "Rút gọn: Phân tích tử và mẫu thành nhân tử rồi chia cho NTC.\nQuy đồng: Tìm MTC = BCNN các hệ số nhân tích lũy thừa bậc cao nhất.")
        ],
        "color": "#1E88E5"
    },
    # 2. Đại số - Tiết 53
    {
        "filename": "mindmap_toan8_tiet53.png",
        "title": "SƠ ĐỒ TƯ DUY: CÁC PHÉP TÍNH PHÂN THỨC ĐẠI SỐ (TIẾT 53)",
        "center": "PHÉP TÍNH\nPHÂN THỨC",
        "branches": [
            ("1. PHÉP CỘNG", "Cùng mẫu: Cộng tử giữ nguyên mẫu.\nKhác mẫu: Quy đồng về MTC rồi cộng tử.\nTính chất: Giao hoán, kết hợp, cộng 0."),
            ("2. PHÉP TRỪ", "A/B - C/D = A/B + (-C/D).\nPhân thức đối: -A/B = (-A)/B = A/(-B).\nQuy tắc đổi dấu khi đặt dấu ngoặc."),
            ("3. PHÉP NHÂN", "(A/B).(C/D) = (A.C)/(B.D).\nTính chất: Giao hoán, kết hợp, nhân 1, phân phối đối với phép cộng."),
            ("4. PHÉP CHIA", "Phân thức nghịch đảo của A/B là B/A (A khác 0).\n(A/B) : (C/D) = (A/B).(D/C) = (A.D)/(B.C).")
        ],
        "color": "#43A047"
    },
    # 3. Đại số - Tiết 54
    {
        "filename": "mindmap_toan8_tiet54.png",
        "title": "SƠ ĐỒ TƯ DUY: TỔNG KẾT CHƯƠNG VI - PHÂN THỨC (TIẾT 54)",
        "center": "TỔNG HỢP\nCHƯƠNG VI",
        "branches": [
            ("1. KHÁI NIỆM & TÍNH CHẤT", "Dạng A/B (B khác 0), ĐKXĐ: B khác 0.\nTính chất nhân chia cùng đa thức khác 0.\nRút gọn về phân thức tối giản."),
            ("2. BỐN PHÉP TÍNH", "Cộng, trừ: Cùng mẫu hoặc quy đồng MTC.\nNhân: Tử nhân tử, mẫu nhân mẫu.\nChia: Nhân nghịch đảo phân thức chia."),
            ("3. THỨ TỰ THỰC HIỆN", "Ngoặc tròn -> vuông -> nhọn.\nNhân chia trước, cộng trừ sau.\nTìm ĐKXĐ trước khi rút gọn biểu thức."),
            ("4. TOÁN THỰC TẾ", "Mô hình hóa năng suất: Thời gian = Khối lượng / Năng suất.\nBài toán chuyển động: Vận tốc, thời gian, quãng đường.")
        ],
        "color": "#8E24AA"
    },
    # 4. Đại số - Tiết 58
    {
        "filename": "mindmap_toan8_tiet58.png",
        "title": "SƠ ĐỒ TƯ DUY: ÔN TẬP GIỮA HỌC KÌ II - ĐẠI SỐ (TIẾT 58)",
        "center": "ÔN TẬP GIỮA HK2\nĐẠI SỐ 8",
        "branches": [
            ("1. PHÂN THỨC ĐẠI SỐ", "Rút gọn biểu thức tổng hợp P.\nTìm ĐKXĐ của biểu thức.\nTính giá trị của P khi biết x."),
            ("2. PHƯƠNG TRÌNH BẬC NHẤT", "Dạng ax + b = 0 (a khác 0).\nNghiệm duy nhất: x = -b/a.\nQuy tắc chuyển vế và nhân chia số khác 0."),
            ("3. GIẢI TOÁN BẰNG PT", "Bước 1: Chọn ẩn, đặt ĐK thích hợp.\nBước 2: Biểu diễn đại lượng chưa biết và lập PT.\nBước 3: Giải PT và đối chiếu ĐK kết luận."),
            ("4. KỸ NĂNG TRÌNH BÀY", "Tuyệt đối không kết luận tập nghiệm S = {...}.\nKhông dùng ký hiệu tương đương tùy tiện.\nKiểm tra lại nghiệm bằng máy tính cầm tay.")
        ],
        "color": "#FB8C00"
    },
    # 5. Đại số - Tiết 60
    {
        "filename": "mindmap_toan8_tiet60.png",
        "title": "SƠ ĐỒ TƯ DUY: PHƯƠNG TRÌNH BẬC NHẤT MỘT ẨN (TIẾT 60)",
        "center": "PHƯƠNG TRÌNH\nBẬC NHẤT",
        "branches": [
            ("1. ĐỊNH NGHĨA", "Phương trình dạng ax + b = 0 với a, b là số đã cho và a khác 0.\nBậc nhất một ẩn đối với biến x."),
            ("2. HAI QUY TẮC BIẾN ĐỔI", "Quy tắc chuyển vế: Đổi dấu hạng tử khi chuyển qua vế khác.\nQuy tắc nhân/chia hai vế với cùng một số khác 0."),
            ("3. CÁCH GIẢI TỔNG QUÁT", "ax + b = 0 -> ax = -b -> x = -b/a.\nKết luận: Vậy phương trình có nghiệm duy nhất x = -b/a."),
            ("4. PHƯƠNG TRÌNH QUY VỀ", "Phương trình có dấu ngoặc: Bỏ ngoặc rồi thu gọn.\nPhương trình có mẫu số: Quy đồng khử mẫu số rồi giải.")
        ],
        "color": "#D81B60"
    },
    # 6. Đại số - Tiết 67
    {
        "filename": "mindmap_toan8_tiet67.png",
        "title": "SƠ ĐỒ TƯ DUY: HÀM SỐ BẬC NHẤT VÀ ĐỒ THỊ (TIẾT 67)",
        "center": "HÀM SỐ BẬC NHẤT\ny = ax + b",
        "branches": [
            ("1. ĐỊNH NGHĨA", "Dạng y = ax + b (a khác 0).\nx là biến số, y là hàm số.\na là hệ số góc, b là tung độ gốc."),
            ("2. ĐỒ THỊ HÀM SỐ", "Đồ thị là một đường thẳng d.\nCắt trục tung tại điểm (0; b).\nCắt trục hoành tại điểm (-b/a; 0)."),
            ("3. HỆ SỐ GÓC & VỊ TRÍ", "a > 0: Góc nhọn, hàm đồng biến.\na < 0: Góc tù, hàm nghịch biến.\nSong song: a = a', b khác b'. Cắt nhau: a khác a'."),
            ("4. ỨNG DỤNG THỰC TẾ", "Mô hình hóa cước taxi, giá tiền điện thoại.\nBài toán cân bằng cung cầu và tài chính cá nhân.")
        ],
        "color": "#00ACC1"
    },
    # 7. Đại số - Tiết 68
    {
        "filename": "mindmap_toan8_tiet68.png",
        "title": "SƠ ĐỒ TƯ DUY: BÀI TẬP CUỐI CHƯƠNG VII (TIẾT 68)",
        "center": "TỔNG HỢP\nCHƯƠNG VII",
        "branches": [
            ("1. PHƯƠNG TRÌNH BẬC NHẤT", "Giải phương trình ax + b = 0.\nGiải bài toán bằng cách lập phương trình: Chuyển động, năng suất, phần trăm."),
            ("2. KHÁI NIỆM HÀM SỐ", "Bảng giá trị, đồ thị hàm số.\nĐiểm thuộc/không thuộc đồ thị: Thay tọa độ vào công thức hàm số."),
            ("3. HÀM BẬC NHẤT & ĐỒ THỊ", "Vẽ đồ thị qua 2 điểm đặc biệt (0; b) và (-b/a; 0).\nÝ nghĩa hình học của hệ số góc a."),
            ("4. VỊ TRÍ TƯƠNG ĐỐI", "Hai đường thẳng song song: a = a', b khác b'.\nHai đường thẳng trùng nhau: a = a', b = b'.\nHai đường thẳng cắt nhau: a khác a'.")
        ],
        "color": "#3949AB"
    },
    # 8. Đại số - Tiết 76
    {
        "filename": "mindmap_toan8_tiet76.png",
        "title": "SƠ ĐỒ TƯ DUY: XÁC SUẤT CỦA BIẾN CỐ (TIẾT 76)",
        "center": "XÁC SUẤT\nBIẾN CỐ",
        "branches": [
            ("1. BIẾN CỐ & KẾT QUẢ", "Biến cố chắc chắn (xác suất = 1).\nBiến cố không thể (xác suất = 0).\nBiến cố ngẫu nhiên: Kết quả có thể và kết quả thuận lợi."),
            ("2. CÔNG THỨC XÁC SUẤT", "Xác suất P(A) = k / n.\nk: Số kết quả thuận lợi cho A.\nn: Tổng số kết quả có thể (đồng khả năng)."),
            ("3. XÁC SUẤT THỰC NGHIỆM", "Tỉ số giữa số lần biến cố xuất hiện và tổng số lần thực hiện phép thử.\nKhi số lần thử n rất lớn, xác suất thực nghiệm xấp xỉ xác suất lý thuyết."),
            ("4. ỨNG DỤNG THỰC TIỄN", "Dự báo thời tiết, kiểm định chất lượng sản phẩm.\nƯớc tính tỉ lệ bảo hành và phân tích rủi ro kinh tế.")
        ],
        "color": "#7CB342"
    },
    # 9. Đại số - Tiết 77
    {
        "filename": "mindmap_toan8_tiet77.png",
        "title": "SƠ ĐỒ TƯ DUY: BÀI TẬP CUỐI CHƯƠNG VIII (TIẾT 77)",
        "center": "TỔNG HỢP\nCHƯƠNG VIII",
        "branches": [
            ("1. MÔ HÌNH XÁC SUẤT", "Liệt kê đầy đủ không gian các kết quả có thể.\nĐảm bảo tính đồng khả năng của các kết quả sơ cấp."),
            ("2. TÍNH XÁC SUẤT BẰNG TỈ SỐ", "Xác định rõ điều kiện của biến cố A.\nĐếm số phần tử thuận lợi k và tính P(A) = k/n.\nBiểu diễn dưới dạng phân số tối giản."),
            ("3. MỐI LIÊN HỆ THỰC NGHIỆM", "Thí nghiệm gieo xúc xắc, rút thẻ, quay bánh xe may mắn.\nỨng dụng phần mềm Excel mô phỏng ngẫu nhiên hàng nghìn lần."),
            ("4. TƯ DUY XÁC SUẤT", "Hình thành tư duy khoa học khách quan.\nNhận thức đúng đắn, tỉnh táo trước các trò may rủi cá cược.")
        ],
        "color": "#5E35B1"
    },
    # 10. Đại số - Tiết 79-81
    {
        "filename": "mindmap_toan8_tiet79_81.png",
        "title": "SƠ ĐỒ TƯ DUY: ÔN TẬP CUỐI HỌC KÌ II - ĐẠI SỐ & XÁC SUẤT (TIẾT 79-81)",
        "center": "ÔN TẬP CUỐI HK2\nĐẠI SỐ & XS 8",
        "branches": [
            ("1. PHÂN THỨC ĐẠI SỐ", "ĐKXĐ, rút gọn phân thức đại số.\nThực hiện dãy tính cộng, trừ, nhân, chia.\nTìm giá trị nguyên của x để biểu thức nhận giá trị nguyên."),
            ("2. PHƯƠNG TRÌNH & HÀM SỐ", "Giải phương trình đưa về dạng ax + b = 0.\nGiải bài toán bằng cách lập PT: Chuyển động, năng suất, quan hệ số.\nVẽ đồ thị hàm số y = ax + b, vị trí tương đối hai đường thẳng."),
            ("3. XÁC SUẤT BIẾN CỐ", "Tính xác suất biến cố ngẫu nhiên bằng tỉ số kết quả thuận lợi.\nƯớc lượng xác suất thực nghiệm trong bài toán chọn mẫu."),
            ("4. KỸ NĂNG LÀM BÀI", "Trình bày các bước lập luận rõ ràng, đầy đủ điều kiện nghiệm.\nKhông kết luận tập nghiệm S = {...}, cẩn trọng kiểm tra bằng MTBT.")
        ],
        "color": "#C2185B"
    },

    # 11. Hình học - Tiết 37
    {
        "filename": "mindmap_toan8_hinh_tiet37.png",
        "title": "SƠ ĐỒ TƯ DUY: TAM GIÁC ĐỒNG DẠNG (TIẾT 37)",
        "center": "TAM GIÁC\nĐỒNG DẠNG",
        "branches": [
            ("1. ĐỊNH NGHĨA", "Tam giác A'B'C' đồng dạng với tam giác ABC (kí hiệu ~).\nCác góc tương ứng bằng nhau.\nCác cạnh tương ứng tỉ lệ: A'B'/AB = B'C'/BC = C'A'/CA = k (tỉ số đồng dạng)."),
            ("2. TRƯỜNG HỢP C-C-C", "Nếu ba cạnh của tam giác này tỉ lệ với ba cạnh của tam giác kia thì hai tam giác đó đồng dạng."),
            ("3. TRƯỜNG HỢP C-G-C", "Nếu hai cạnh của tam giác này tỉ lệ với hai cạnh tam giác kia và hai góc tạo bởi các cặp cạnh đó bằng nhau thì hai tam giác đồng dạng."),
            ("4. TRƯỜNG HỢP G-G", "Nếu hai góc của tam giác này lần lượt bằng hai góc của tam giác kia thì hai tam giác đó đồng dạng (trường hợp dùng nhiều nhất).")
        ],
        "color": "#0288D1"
    },
    # 12. Hình học - Tiết 43
    {
        "filename": "mindmap_toan8_hinh_tiet43.png",
        "title": "SƠ ĐỒ TƯ DUY: ĐỊNH LÍ PYTHAGORE & HÌNH ĐỒNG DẠNG (TIẾT 43)",
        "center": "PYTHAGORE &\nTAM GIÁC VUÔNG",
        "branches": [
            ("1. ĐỊNH LÍ PYTHAGORE", "Thuận: Tam giác ABC vuông tại A -> BC^2 = AB^2 + AC^2.\nĐảo: Nếu BC^2 = AB^2 + AC^2 thì tam giác ABC vuông tại A."),
            ("2. ĐỒNG DẠNG TAM GIÁC VUÔNG", "Trường hợp một góc nhọn bằng nhau.\nTrường hợp hai cạnh góc vuông tỉ lệ.\nTrường hợp cạnh huyền và cạnh góc vuông tỉ lệ."),
            ("3. TỈ SỐ ĐỒNG DẠNG ĐẶC BIỆT", "Tỉ số hai đường cao tương ứng bằng tỉ số đồng dạng k.\nTỉ số diện tích hai tam giác đồng dạng bằng bình phương tỉ số đồng dạng k^2."),
            ("4. HÌNH ĐỒNG DẠNG TRONG THỰC TẾ", "Hình đồng dạng phối cảnh (tâm vị tự).\nẢnh chụp thu nhỏ/phóng to, bản đồ địa lý theo tỉ lệ xích.")
        ],
        "color": "#00897B"
    },
    # 13. Hình học - Tiết 44
    {
        "filename": "mindmap_toan8_hinh_tiet44.png",
        "title": "SƠ ĐỒ TƯ DUY: BÀI TẬP CUỐI CHƯƠNG IX - HÌNH HỌC (TIẾT 44)",
        "center": "TỔNG HỢP\nCHƯƠNG IX",
        "branches": [
            ("1. ĐỊNH LÍ THALES & HỆ QUẢ", "Đoạn thẳng tỉ lệ trên hai cạnh tam giác khi có đường song song.\nTính độ dài đoạn thẳng và chứng minh song song."),
            ("2. BA TRƯỜNG HỢP ĐỒNG DẠNG", "C-C-C; C-G-C; G-G.\nÁp dụng cho tam giác vuông: Góc nhọn hoặc cạnh huyền - cạnh góc vuông."),
            ("3. TÍNH CHẤT ĐƯỜNG PHÂN GIÁC", "Đường phân giác trong góc A chia cạnh đối diện thành hai đoạn tỉ lệ với hai cạnh kề: DB/DC = AB/AC."),
            ("4. ỨNG DỤNG ĐO ĐẠC THỰC TẾ", "Đo chiều cao cây, cột cờ qua bóng nắng trên mặt đất.\nĐo khoảng cách giữa hai điểm bị ngăn cách bởi hồ nước hoặc chướng ngại vật.")
        ],
        "color": "#689F38"
    },
    # 14. Hình học - Tiết 46
    {
        "filename": "mindmap_toan8_hinh_tiet46.png",
        "title": "SƠ ĐỒ TƯ DUY: ÔN TẬP GIỮA HỌC KÌ II - HÌNH HỌC (TIẾT 46)",
        "center": "ÔN TẬP GIỮA HK2\nHÌNH HỌC 8",
        "branches": [
            ("1. CHỨNG MINH ĐỒNG DẠNG", "Chọn trường hợp đồng dạng tối ưu (thường là góc - góc).\nViết đúng thứ tự các đỉnh tương ứng."),
            ("2. TÍNH ĐỘ DÀI ĐOẠN THẲNG", "Thiết lập tỉ số đồng dạng từ hai tam giác đồng dạng.\nThay số liệu và giải tìm độ dài chưa biết."),
            ("3. CHỨNG MINH HỆ THỨC HÌNH HỌC", "Chứng minh tích AB.CD = AC.BD thông qua tỉ số đồng dạng.\nChứng minh tam giác vuông nhờ định lí Pythagore đảo."),
            ("4. LƯU Ý KÍ HIỆU", "Kí hiệu góc luôn dùng \\widehat{...}.\nKhông dùng kí hiệu tương đương tùy tiện trong lập luận hình học.")
        ],
        "color": "#EF6C00"
    },
    # 15. Hình học - Tiết 52
    {
        "filename": "mindmap_toan8_hinh_tiet52.png",
        "title": "SƠ ĐỒ TƯ DUY: HÌNH CHÓP ĐỀU TRONG THỰC TIỄN (TIẾT 52)",
        "center": "HÌNH CHÓP\nĐỀU",
        "branches": [
            ("1. HÌNH CHÓP TAM GIÁC ĐỀU", "Đáy là tam giác đều.\nCác mặt bên là các tam giác cân bằng nhau có chung đỉnh S.\nĐoạn nối đỉnh với tâm đáy là đường cao h."),
            ("2. HÌNH CHÓP TỨ GIÁC ĐỀU", "Đáy là hình vuông.\nCác mặt bên là các tam giác cân bằng nhau.\nĐoạn nối đỉnh với tâm đáy vuông góc với đáy."),
            ("3. DIỆN TÍCH XUNG QUANH", "S_xq = p . d\np: Nửa chu vi đáy.\nd: Trung đoạn (chiều cao của mặt bên xuất phát từ đỉnh S)."),
            ("4. THỂ TÍCH HÌNH CHÓP ĐỀU", "V = (1/3) . S_đáy . h\nS_đáy: Diện tích mặt đáy (tam giác đều hoặc hình vuông).\nh: Chiều cao của hình chóp.")
        ],
        "color": "#546E7A"
    },
    # 16. Hình học - Tiết 53
    {
        "filename": "mindmap_toan8_hinh_tiet53.png",
        "title": "SƠ ĐỒ TƯ DUY: BÀI TẬP CUỐI CHƯƠNG X (TIẾT 53)",
        "center": "TỔNG HỢP\nCHƯƠNG X",
        "branches": [
            ("1. ĐẶC ĐIỂM HÌNH HỌC", "Phân biệt hình chóp tam giác đều và hình chóp tứ giác đều.\nNhận biết đỉnh, cạnh bên, cạnh đáy, mặt bên, mặt đáy, trung đoạn."),
            ("2. CÔNG THỨC DIỆN TÍCH", "S_xq = p . d (nửa chu vi đáy nhân trung đoạn).\nS_toan_phan = S_xq + S_day."),
            ("3. CÔNG THỨC THỂ TÍCH", "V = (1/3) . S_day . h.\nQuan hệ giữa thể tích hình chóp và hình lăng trụ cùng đáy và chiều cao."),
            ("4. BÀI TOÁN THỰC TIỄN", "Tính diện tích vải bạt may lều trại chóp tam giác đều.\nTính thể tích khối kim tự tháp, khối hộp quà lưu niệm, mái nhà.")
        ],
        "color": "#7E57C2"
    },
    # 17. Hình học - Tiết 54-55
    {
        "filename": "mindmap_toan8_hinh_tiet54_55.png",
        "title": "SƠ ĐỒ TƯ DUY: ÔN TẬP CUỐI HỌC KÌ II - HÌNH HỌC 8 (TIẾT 54, 55)",
        "center": "ÔN TẬP CUỐI HK2\nHÌNH HỌC 8",
        "branches": [
            ("1. ĐỊNH LÍ THALES & ĐỒNG DẠNG", "Định lí Thales thuận và đảo, tính chất đường phân giác.\nBa trường hợp đồng dạng của tam giác và ứng dụng vào tam giác vuông."),
            ("2. ĐỊNH LÍ PYTHAGORE", "Tam giác vuông: BC^2 = AB^2 + AC^2.\nPythagore đảo kiểm tra tính vuông góc.\nTính khoảng cách và đường chéo các hình phẳng."),
            ("3. HÌNH KHỐI TRONG THỰC TIỄN", "Hình chóp tam giác đều và hình chóp tứ giác đều.\nCông thức diện tích xung quanh S_xq = p.d và thể tích V = (1/3).S_day.h."),
            ("4. KỸ NĂNG VẼ HÌNH & LẬP LUẬN", "Dựng hình chính xác bằng thước thẳng, êke, compa.\nLập luận hình học logic, dùng đúng kí hiệu góc \\widehat{...}.")
        ],
        "color": "#D32F2F"
    }
]

for idx, item in enumerate(mindmaps_data):
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Title
    ax.text(7, 7.5, item["title"], ha='center', va='center', fontsize=15, fontweight='bold', color=item["color"])
    
    # Center box
    center_box = FancyBboxPatch((5.3, 3.2), 3.4, 1.6, boxstyle="round,pad=0.2",
                                ec=item["color"], fc=item["color"], lw=2)
    ax.add_patch(center_box)
    ax.text(7, 4.0, item["center"], ha='center', va='center', fontsize=13, fontweight='bold', color='white', multialignment='center')
    
    # 4 branches positions
    positions = [
        {"box": (0.8, 5.0), "text": (2.8, 5.85), "line_start": (5.3, 4.4), "line_end": (4.8, 5.5)},   # Top-Left
        {"box": (9.2, 5.0), "text": (11.2, 5.85), "line_start": (8.7, 4.4), "line_end": (9.2, 5.5)},  # Top-Right
        {"box": (0.8, 1.0), "text": (2.8, 1.85), "line_start": (5.3, 3.6), "line_end": (4.8, 2.5)},   # Bottom-Left
        {"box": (9.2, 1.0), "text": (11.2, 1.85), "line_start": (8.7, 3.6), "line_end": (9.2, 2.5)}   # Bottom-Right
    ]
    
    for b_idx, (b_title, b_desc) in enumerate(item["branches"]):
        pos = positions[b_idx]
        
        # Line from center to branch
        ax.annotate('', xy=pos["line_end"], xytext=pos["line_start"],
                    arrowprops=dict(arrowstyle="-|>", color=item["color"], lw=2, mutation_scale=15))
        
        # Branch box
        bbox = FancyBboxPatch(pos["box"], 4.0, 1.9, boxstyle="round,pad=0.15",
                              ec=item["color"], fc='#F8F9FA', lw=1.5)
        ax.add_patch(bbox)
        
        # Branch title & content
        ax.text(pos["text"][0], pos["text"][1] + 0.65, b_title, ha='center', va='center',
                fontsize=10.5, fontweight='bold', color=item["color"])
        ax.text(pos["text"][0], pos["text"][1] - 0.15, b_desc, ha='center', va='center',
                fontsize=8.5, color='#212121', multialignment='center', wrap=True)

    out_path = os.path.join(output_dir, item["filename"])
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"[{idx+1}/17] -> Đã tạo Mindmap: {out_path}")

print("Hoàn tất tạo 17 ảnh Mindmap vector 300 DPI môn Toán 8 HK2!")
