# -*- coding: utf-8 -*-
"""
Script sinh 16 Sơ đồ tư duy Mindmap vector 300 DPI cho môn Toán 9 Học kì II
Thầy Hoàng Tấn Thiên - Năm học 2026 - 2027
"""

import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

output_dir = "TROLYTHIEN/TEMP/HK2_Toan9/mindmaps"
os.makedirs(output_dir, exist_ok=True)

mindmaps_data = [
    # 1. Đại số - Tiết 50
    {
        "filename": "mindmap_toan9_tiet50.png",
        "title": "SƠ ĐỒ TƯ DUY: HÀM SỐ Y = AX² & PHƯƠNG TRÌNH BẬC HAI (TIẾT 50)",
        "center": "HÀM SỐ & PT\nBẬC HAI",
        "branches": [
            ("1. HÀM SỐ y = ax² (a ≠ 0)", "Đồng biến/nghịch biến tùy dấu a và x.\nĐồ thị là Parabol đỉnh O(0; 0), trục đối xứng Oy.\na > 0: Bề lõm quay lên, y ≥ 0; a < 0: Bề lõm quay xuống, y ≤ 0."),
            ("2. ĐỊNH NGHĨA PT BẬC HAI", "Dạng chuẩn: ax² + bx + c = 0 (a ≠ 0).\nCác hệ số: a là hệ số bậc hai, b là hệ số bậc nhất, c là số hạng tự do."),
            ("3. CÔNG THỨC NGHIỆM", "Biệt thức Δ = b² - 4ac.\nΔ > 0: PT có 2 nghiệm phân biệt x1,2 = (-b ± √Δ)/(2a).\nΔ = 0: Nghiệm kép x1 = x2 = -b/(2a).\nΔ < 0: PT vô nghiệm."),
            ("4. CÔNG THỨC THU GỌN", "Khi b = 2b': Δ' = b'² - ac.\nΔ' > 0: x1,2 = (-b' ± √Δ')/a.\nΔ' = 0: x1 = x2 = -b'/a.\nΔ' < 0: Vô nghiệm.")
        ],
        "color": "#1E88E5"
    },
    # 2. Đại số - Tiết 55
    {
        "filename": "mindmap_toan9_tiet55.png",
        "title": "SƠ ĐỒ TƯ DUY: ĐỊNH LÍ VIÈTE & GIẢI TOÁN BẰNG LẬP PT (TIẾT 55)",
        "center": "ĐỊNH LÍ VIÈTE\n& LẬP PT",
        "branches": [
            ("1. ĐỊNH LÍ VIÈTE THUẬN", "Nếu PT ax² + bx + c = 0 có nghiệm thì:\nS = x1 + x2 = -b/a\nP = x1 . x2 = c/a."),
            ("2. NHẨM NGHIỆM ĐẶC BIỆT", "Nếu a + b + c = 0 thì x1 = 1, x2 = c/a.\nNếu a - b + c = 0 thì x1 = -1, x2 = -c/a.\nTìm 2 số biết tổng S và tích P: u, v là nghiệm của X² - SX + P = 0."),
            ("3. ỨNG DỤNG HỆ THỨC ĐỐI XỨNG", "x1² + x2² = S² - 2P.\n(x1 - x2)² = S² - 4P.\n1/x1 + 1/x2 = S/P.\nx1³ + x2³ = S(S² - 3P)."),
            ("4. GIẢI TOÁN BẰNG LẬP PT", "Bước 1: Chọn ẩn, đặt ĐK và đơn vị cho ẩn.\nBước 2: Biểu diễn đại lượng chưa biết theo ẩn và lập PT.\nBước 3: Giải PT và đối chiếu ĐK kết luận nghiệm.")
        ],
        "color": "#43A047"
    },
    # 3. Đại số - Tiết 56
    {
        "filename": "mindmap_toan9_tiet56.png",
        "title": "SƠ ĐỒ TƯ DUY: TỔNG KẾT CHƯƠNG VI - HÀM SỐ & PT BẬC HAI (TIẾT 56)",
        "center": "TỔNG HỢP\nCHƯƠNG VI",
        "branches": [
            ("1. HÀM SỐ y = ax²", "Tính chất biến thiên, vẽ đồ thị Parabol.\nTương giao giữa Parabol và đường thẳng d: y = mx + n (PT hoành độ giao điểm)."),
            ("2. GIẢI PHƯƠNG TRÌNH", "Phương pháp: Tách hạng tử, đặt ẩn phụ, dùng công thức nghiệm Δ và Δ'.\nPhương trình quy về bậc hai: Trùng phương, chứa ẩn ở mẫu, tích."),
            ("3. HỆ THỨC VIÈTE", "Tổng S = -b/a, Tích P = c/a.\nXét dấu các nghiệm: 2 nghiệm dương (Δ ≥ 0, S > 0, P > 0), 2 nghiệm âm, 2 nghiệm trái dấu (ac < 0)."),
            ("4. BÀI TOÁN THỰC TẾ", "Chuyển động (s = v.t), năng suất (A = N.t), hình học (diện tích, chu vi, định lí Pythagore).")
        ],
        "color": "#8E24AA"
    },
    # 4. Đại số - Tiết 57
    {
        "filename": "mindmap_toan9_tiet57.png",
        "title": "SƠ ĐỒ TƯ DUY: ÔN TẬP GIỮA HỌC KÌ II - ĐẠI SỐ 9 (TIẾT 57)",
        "center": "ÔN TẬP GIỮA HK2\nĐẠI SỐ 9",
        "branches": [
            ("1. ĐỒ THỊ PARABOL", "Lập bảng giá trị 5 điểm đối xứng qua trục Oy.\nVẽ đường cong Parabol mượt mà.\nTìm tọa độ giao điểm với đường thẳng y = kx + m."),
            ("2. CÔNG THỨC NGHIỆM", "Tính chính xác biệt thức Δ = b² - 4ac.\nKết luận nghiệm theo điều kiện dấu của Δ.\nCấm nhầm dấu trừ trong công thức x = (-b ± √Δ)/(2a)."),
            ("3. ĐỊNH LÍ VIÈTE", "Tính giá trị biểu thức đối xứng của x1, x2.\nTìm điều kiện của tham số m để PT có nghiệm thỏa mãn hệ thức cho trước."),
            ("4. LẬP PT BẬC HAI THỰC TẾ", "Toán chuyển động xuôi/ngược dòng cano.\nToán làm chung - làm riêng công việc.\nĐối chiếu điều kiện thực tế (x > 0, nguyên).")
        ],
        "color": "#D81B60"
    },
    # 5. Thống kê - Tiết 63
    {
        "filename": "mindmap_toan9_tiet63.png",
        "md_ill_id": "mindmap-toan9-tiet63",
        "title": "SƠ ĐỒ TƯ DUY: BẢNG TẦN SỐ & BIỂU ĐỒ TẦN SỐ (TIẾT 63)",
        "center": "TẦN SỐ &\nBIỂU ĐỒ",
        "branches": [
            ("1. TẦN SỐ (m)", "Số lần xuất hiện của một giá trị trong mẫu số liệu.\nTổng các tần số bằng quy mô mẫu: m1 + m2 + ... + mk = N."),
            ("2. TẦN SỐ TƯƠNG ĐỐI (f)", "Tỉ số giữa tần số m và quy mô mẫu N: f = (m/N) . 100%.\nTổng các tần số tương đối bằng 100%: f1 + f2 + ... + fk = 100%."),
            ("3. BIỂU ĐỒ TẦN SỐ", "Biểu đồ cột: Chiều cao cột thể hiện tần số m.\nBiểu đồ đoạn thẳng: Nối các đỉnh tọa độ (giá trị, tần số)."),
            ("4. BIỂU ĐỒ HÌNH QUẠT TRÒN", "Biểu diễn tần số tương đối f.\nGóc ở tâm tương ứng: n° = f . 360° / 100%.")
        ],
        "color": "#00897B"
    },
    # 6. Thống kê - Tiết 67-68
    {
        "filename": "mindmap_toan9_tiet67_68.png",
        "md_ill_id": "mindmap-toan9-tiet67-68",
        "title": "SƠ ĐỒ TƯ DUY: TỔNG KẾT CHƯƠNG VII - TẦN SỐ GHÉP NHÓM (TIẾT 67 - 68)",
        "center": "TỔNG HỢP\nCHƯƠNG VII",
        "branches": [
            ("1. DỮ LIỆU GHÉP NHÓM", "Nhóm số liệu có dạng [a; b).\nGiá trị đại diện của nhóm: c = (a + b) / 2.\nĐộ dài nhóm: l = b - a."),
            ("2. TẦN SỐ GHÉP NHÓM", "Tần số nhóm: Số lượng cá thể thuộc nhóm [a; b).\nTần số tương đối nhóm: f = (m_nhóm / N) . 100%."),
            ("3. BIỂU ĐỒ TẦN SỐ GHÉP NHÓM", "Biểu đồ cột liền kề (Histogram).\nTrục hoành: Các mút của nhóm [a; b).\nTrục tung: Tần số hoặc tần số tương đối."),
            ("4. Ý NGHĨA THỐNG KÊ", "Phân tích đặc trưng phân bố của tập dữ liệu lớn.\nĐưa ra dự báo và quyết định dựa trên dữ liệu thực tế.")
        ],
        "color": "#FB8C00"
    },
    # 7. Xác suất - Tiết 72
    {
        "filename": "mindmap_toan9_tiet72.png",
        "md_ill_id": "mindmap-toan9-tiet72",
        "title": "SƠ ĐỒ TƯ DUY: PHÉP THỬ & XÁC SUẤT CỦA BIẾN CỐ (TIẾT 72)",
        "center": "XÁC SUẤT\nBIẾN CỐ",
        "branches": [
            ("1. PHÉP THỬ NGẪU NHIÊN", "Hành động có kết quả không thể biết trước nhưng biết tập hợp tất cả kết quả có thể.\nKí hiệu không gian mẫu: Ω; số phần tử n(Ω)."),
            ("2. BIẾN CỐ", "Biến cố A là một tập con của không gian mẫu Ω.\nKết quả thuận lợi cho A: n(A)."),
            ("3. CÔNG THỨC XÁC SUẤT", "Cổ điển: P(A) = n(A) / n(Ω) (các kết quả đồng khả năng).\nTính chất: 0 ≤ P(A) ≤ 1; P(chắc chắn) = 1; P(không thể) = 0."),
            ("4. MÔ HÌNH XÁC SUẤT", "Gieo đồng xu, gieo xúc xắc, rút thẻ số, bốc thăm.\nSơ đồ hình cây biểu diễn các kết quả qua nhiều giai đoạn.")
        ],
        "color": "#5E35B1"
    },
    # 8. Xác suất - Tiết 73-74
    {
        "filename": "mindmap_toan9_tiet73_74.png",
        "md_ill_id": "mindmap-toan9-tiet73-74",
        "title": "SƠ ĐỒ TƯ DUY: TỔNG KẾT CHƯƠNG VIII - XÁC SUẤT (TIẾT 73 - 74)",
        "center": "TỔNG HỢP\nCHƯƠNG VIII",
        "branches": [
            ("1. KHÔNG GIAN MẪU Ω", "Liệt kê đầy đủ các phần tử của Ω mà không trùng lặp.\nĐếm số phần tử n(Ω) bằng quy tắc liệt kê hoặc bảng 2 chiều."),
            ("2. XÁC SUẤT BIẾN CỐ", "P(A) = n(A) / n(Ω).\nBiến cố đối: P(không A) = 1 - P(A).\nBiến cố hợp của hai biến cố xung khắc: P(A ∪ B) = P(A) + P(B)."),
            ("3. TẦN SỐ & XÁC SUẤT", "Xác suất thực nghiệm f ≈ P(A) khi số phép thử N rất lớn (Quy luật số lớn)."),
            ("4. ỨNG DỤNG THỰC TẾ", "Dự báo thời tiết, y tế, di truyền học (gene trội/lặn Mendel), kinh doanh bảo hiểm.")
        ],
        "color": "#3949AB"
    },
    # 9. Đại số & Xác suất - Tiết 76-77
    {
        "filename": "mindmap_toan9_tiet76_77.png",
        "md_ill_id": "mindmap-toan9-tiet76-77",
        "title": "SƠ ĐỒ TƯ DUY: ÔN TẬP CUỐI HỌC KÌ II - ĐẠI SỐ & THỐNG KÊ (TIẾT 76 - 77)",
        "center": "ÔN TẬP CUỐI HK2\nĐẠI SỐ 9",
        "branches": [
            ("1. HÀM SỐ & PT BẬC HAI", "Khảo sát và vẽ Parabol y = ax².\nGiải PT bằng công thức nghiệm Δ và Δ'.\nỨng dụng Viète tính giá trị biểu thức và nhẩm nghiệm."),
            ("2. LẬP PT BẬC HAI", "Giải bài toán thực tế bằng cách lập phương trình: Toán chuyển động, năng suất, hình học."),
            ("3. THỐNG KÊ DỮ LIỆU", "Lập bảng tần số, tần số tương đối (rời rạc và ghép nhóm).\nVẽ và đọc biểu đồ cột, biểu đồ đoạn thẳng, biểu đồ quạt tròn."),
            ("4. XÁC SUẤT", "Xác định không gian mẫu Ω và số kết quả thuận lợi.\nTính xác suất cổ điển P(A) = n(A) / n(Ω).")
        ],
        "color": "#C2185B"
    },
    # 10. Hình học - Tiết 35-36
    {
        "filename": "mindmap_toan9_hinh_tiet35_36.png",
        "md_ill_id": "mindmap-toan9-hinh-tiet35-36",
        "title": "SƠ ĐỒ TƯ DUY: GÓC NỘI TIẾP & ĐƯỜNG TRÒN NGOẠI TIẾP TAM GIÁC (TIẾT 35 - 36)",
        "center": "GÓC NỘI TIẾP &\nĐƯỜNG TRÒN",
        "branches": [
            ("1. GÓC NỘI TIẾP", "Góc có đỉnh nằm trên đường tròn và 2 cạnh chứa 2 dây cung.\nSố đo bằng một nửa số đo cung bị chắn: góc = 1/2 sđ cung.\nGóc nội tiếp chắn nửa đường tròn là góc vuông (90°)."),
            ("2. TÍNH CHẤT CÙNG CHẮN", "Các góc nội tiếp cùng chắn một cung (hoặc chắn các cung bằng nhau) thì bằng nhau.\nGóc nội tiếp ≤ 90° bằng một nửa góc ở tâm cùng chắn một cung."),
            ("3. ĐƯỜNG TRÒN NGOẠI TIẾP", "Đường tròn đi qua cả 3 đỉnh của tam giác.\nTâm là giao điểm 3 đường trung trực của tam giác.\nTam giác vuông: Tâm là trung điểm cạnh huyền, R = cạnh huyền / 2."),
            ("4. ĐƯỜNG TRÒN NỘI TIẾP", "Đường tròn tiếp xúc với cả 3 cạnh của tam giác.\nTâm là giao điểm 3 đường phân giác trong của tam giác.\nBán kính r = S / p (p là nửa chu vi).")
        ],
        "color": "#0288D1"
    },
    # 11. Hình học - Tiết 41-42
    {
        "filename": "mindmap_toan9_hinh_tiet41_42.png",
        "md_ill_id": "mindmap-toan9-hinh-tiet41-42",
        "title": "SƠ ĐỒ TƯ DUY: TỨ GIÁC NỘI TIẾP & ĐA GIÁC ĐỀU (TIẾT 41 - 42)",
        "center": "TỨ GIÁC NỘI TIẾP\n& ĐA GIÁC ĐỀU",
        "branches": [
            ("1. ĐỊNH NGHĨA TỨ GIÁC NỘI TIẾP", "Tứ giác có 4 đỉnh cùng nằm trên một đường tròn.\nTổng hai góc đối diện bằng 180°: góc A + góc C = 180°, góc B + góc D = 180°."),
            ("2. BỐN DẤU HIỆU NHẬN BIẾT", "Dấu hiệu 1: Tổng 2 góc đối bằng 180°.\nDấu hiệu 2: Góc ngoài tại một đỉnh bằng góc trong đỉnh đối diện.\nDấu hiệu 3: Hai đỉnh kề nhau cùng nhìn cạnh đối diện dưới 2 góc bằng nhau.\nDấu hiệu 4: Bốn đỉnh cùng cách đều một điểm O."),
            ("3. ĐA GIÁC ĐỀU", "Đa giác có tất cả các cạnh bằng nhau và tất cả các góc bằng nhau.\nSố đo mỗi góc của n-giác đều: (n - 2) . 180° / n.\nLuôn có 1 đường tròn ngoại tiếp và 1 đường tròn nội tiếp cùng tâm."),
            ("4. ỨNG DỤNG HÌNH HỌC", "Chứng minh nhiều điểm cùng thuộc một đường tròn.\nChứng minh các góc bằng nhau, các cặp đường thẳng song song hoặc vuông góc.")
        ],
        "color": "#00796B"
    },
    # 12. Hình học - Tiết 43-44
    {
        "filename": "mindmap_toan9_hinh_tiet43_44.png",
        "md_ill_id": "mindmap-toan9-hinh-tiet43-44",
        "title": "SƠ ĐỒ TƯ DUY: TỔNG KẾT CHƯƠNG IX - ĐƯỜNG TRÒN (TIẾT 43 - 44)",
        "center": "TỔNG HỢP\nCHƯƠNG IX",
        "branches": [
            ("1. GÓC VỚI ĐƯỜNG TRÒN", "Góc ở tâm (bằng sđ cung).\nGóc nội tiếp (bằng 1/2 sđ cung).\nGóc tạo bởi tia tiếp tuyến và dây cung (bằng 1/2 sđ cung).\nGóc có đỉnh ở bên trong/ngoài đường tròn."),
            ("2. TAM GIÁC & ĐƯỜNG TRÒN", "Đường tròn ngoại tiếp: Tâm là giao 3 đường trung trực.\nĐường tròn nội tiếp: Tâm là giao 3 đường phân giác."),
            ("3. TỨ GIÁC NỘI TIẾP", "Định lí thuận: Tổng 2 góc đối bằng 180°.\n4 dấu hiệu nhận biết then chốt trong giải toán hình học tuyển sinh 10."),
            ("4. ĐA GIÁC ĐỀU & HỌA TIẾT", "Tam giác đều, hình vuông, ngũ giác đều, lục giác đều.\nVẽ đa giác đều bằng thước và compa, ứng dụng kiến trúc.")
        ],
        "color": "#7B1FA2"
    },
    # 13. Hình học - Tiết 45
    {
        "filename": "mindmap_toan9_hinh_tiet45.png",
        "md_ill_id": "mindmap-toan9-hinh-tiet45",
        "title": "SƠ ĐỒ TƯ DUY: ÔN TẬP GIỮA HỌC KÌ II - HÌNH HỌC 9 (TIẾT 45)",
        "center": "ÔN TẬP GIỮA HK2\nHÌNH HỌC 9",
        "branches": [
            ("1. GÓC NỘI TIẾP", "Góc chắn nửa đường tròn bằng 90°.\nCác góc nội tiếp bằng nhau cùng chắn các cung bằng nhau."),
            ("2. CHỨNG MINH TỨ GIÁC NỘI TIẾP", "Phương pháp 1: Chứng minh tổng hai góc đối bằng 180°.\nPhương pháp 2: Chứng minh hai đỉnh kề cùng nhìn một đoạn thẳng dưới góc vuông hoặc góc bằng nhau."),
            ("3. HỆ THỨC LƯỢNG ĐƯỜNG TRÒN", "Phương tích: MA . MB = MC . MD hoặc MA . MB = MT² (với MT là tiếp tuyến)."),
            ("4. ĐƯỜNG TRÒN NGOẠI/NỘI TIẾP", "Tính bán kính R và r của tam giác đều cạnh a, tam giác vuông.")
        ],
        "color": "#E64A19"
    },
    # 14. Hình học - Tiết 53
    {
        "filename": "mindmap_toan9_hinh_tiet53.png",
        "md_ill_id": "mindmap-toan9-hinh-tiet53",
        "title": "SƠ ĐỒ TƯ DUY: HÌNH TRỤ - HÌNH NÓN - HÌNH CẦU (TIẾT 53)",
        "center": "HÌNH TRỤ - NÓN\nHÌNH CẦU",
        "branches": [
            ("1. HÌNH TRỤ", "Quay hình chữ nhật quanh 1 cạnh.\nSxq = 2πRh, Stp = 2πRh + 2πR².\nThể tích: V = πR²h."),
            ("2. HÌNH NÓN", "Quay tam giác vuông quanh 1 cạnh góc vuông.\nĐường sinh l² = h² + R².\nSxq = πRl, Stp = πRl + πR².\nThể tích: V = (1/3)πR²h."),
            ("3. HÌNH CẦU", "Quay nửa hình tròn quanh đường kính.\nDiện tích mặt cầu: S = 4πR² = πd².\nThể tích hình cầu: V = (4/3)πR³ = (1/6)πd³."),
            ("4. ỨNG DỤNG THỰC TẾ (STEM)", "Thùng chứa nước hình trụ, nón lá hình nón, quả bóng/trái đất hình cầu.\nTính vật liệu, diện tích sơn và dung tích chứa nước.")
        ],
        "color": "#0097A7"
    },
    # 15. Hình học - Tiết 54-55
    {
        "filename": "mindmap_toan9_hinh_tiet54_55.png",
        "md_ill_id": "mindmap-toan9-hinh-tiet54-55",
        "title": "SƠ ĐỒ TƯ DUY: TỔNG KẾT CHƯƠNG X - CÁC HÌNH KHỐI THỰC TIỄN (TIẾT 54 - 55)",
        "center": "TỔNG HỢP\nCHƯƠNG X",
        "branches": [
            ("1. BẢNG CÔNG THỨC DIỆN TÍCH", "Hình trụ: Sxq = 2πRh.\nHình nón: Sxq = πRl.\nHình cầu: S = 4πR²."),
            ("2. BẢNG CÔNG THỨC THỂ TÍCH", "Hình trụ: V = πR²h.\nHình nón: V = (1/3)πR²h.\nHình cầu: V = (4/3)πR³."),
            ("3. KHỐI TRÒN XOAY KẾT HỢP", "Vật thể ghép gồm hình trụ và bán cầu.\nVật thể ghép gồm hình trụ và hình nón (bút chì, tên lửa, tháp chuông)."),
            ("4. BÀI TOÁN KỸ THUẬT & ĐỜI SỐNG", "Tính dung tích bể chứa, bồn xăng dầu.\nTính lượng sơn phủ bề mặt công trình tròn xoay.")
        ],
        "color": "#5D4037"
    },
    # 16. Hình học - Tiết 56-57
    {
        "filename": "mindmap_toan9_hinh_tiet56_57.png",
        "md_ill_id": "mindmap-toan9-hinh-tiet56-57",
        "title": "SƠ ĐỒ TƯ DUY: ÔN TẬP CUỐI HỌC KÌ II - HÌNH HỌC 9 (TIẾT 56 - 57)",
        "center": "ÔN TẬP CUỐI HK2\nHÌNH HỌC 9",
        "branches": [
            ("1. GÓC VỚI ĐƯỜNG TRÒN", "Góc ở tâm, góc nội tiếp, góc tạo bởi tiếp tuyến và dây cung.\nQuan hệ giữa cung và dây, góc nội tiếp vuông."),
            ("2. TỨ GIÁC NỘI TIẾP", "Bốn dấu hiệu nhận biết kinh điển.\nKỹ năng vẽ đường tròn ngoại tiếp tứ giác và khai thác các góc bằng nhau."),
            ("3. CÁC HÌNH KHỐI KHÔNG GIAN", "Hình trụ, nón, cầu: Công thức Sxq và Thể tích V.\nBài toán thực tế tính toán lượng nguyên vật liệu."),
            ("4. DẠNG BÀI THI TUYỂN SINH 10", "Bài toán hình học phẳng tổng hợp 3 - 4 câu:\nChứng minh tứ giác nội tiếp -> Chứng minh hệ thức hình học -> Chứng minh tiếp tuyến/vuông góc/thẳng hàng.")
        ],
        "color": "#D32F2F"
    }
]

def draw_mindmap(data):
    fig, ax = plt.subplots(figsize=(13, 7.5), dpi=300)
    ax.set_facecolor("#F8F9FA")
    fig.patch.set_facecolor("#F8F9FA")
    
    # Title
    fig.text(0.5, 0.95, data["title"], ha='center', va='center', 
             fontsize=15, fontweight='bold', color='#1A237E', family='sans-serif')
    fig.text(0.5, 0.915, "Thầy Hoàng Tấn Thiên - Toán 9 Kết nối tri thức - Bản đồ tư duy chuẩn CV 5512",
             ha='center', va='center', fontsize=9.5, fontstyle='italic', color='#555555', family='sans-serif')
    
    # Center box
    center_box = FancyBboxPatch((0.40, 0.40), 0.20, 0.18,
                               boxstyle="round,pad=0.03,rounding_size=0.04",
                               facecolor=data["color"], edgecolor='#0D47A1', linewidth=2.5,
                               transform=ax.transAxes, zorder=5)
    ax.add_patch(center_box)
    ax.text(0.50, 0.49, data["center"], ha='center', va='center',
            fontsize=13, fontweight='bold', color='white', family='sans-serif', transform=ax.transAxes, zorder=6)
    
    # Coordinates of 4 branches
    branch_coords = [
        (0.04, 0.54, 0.36, 0.30, 0.40, 0.53, 0.40, 0.65), # Top-Left
        (0.60, 0.54, 0.36, 0.30, 0.60, 0.53, 0.60, 0.65), # Top-Right
        (0.04, 0.10, 0.36, 0.32, 0.40, 0.45, 0.40, 0.28), # Bottom-Left
        (0.60, 0.10, 0.36, 0.32, 0.60, 0.45, 0.60, 0.28)  # Bottom-Right
    ]
    
    border_colors = ['#1976D2', '#388E3C', '#7B1FA2', '#D32F2F']
    header_bgs = ['#E3F2FD', '#E8F5E9', '#F3E5F5', '#FFEBEE']
    
    for idx, (b_title, b_desc) in enumerate(data["branches"]):
        bx, by, bw, bh, cx, cy, tx, ty = branch_coords[idx]
        
        # Connection line
        ax.annotate('', xy=(tx, ty), xytext=(cx, cy),
                    xycoords='axes fraction', textcoords='axes fraction',
                    arrowprops=dict(arrowstyle="-|>", color=data["color"], lw=2.2,
                                   shrinkA=5, shrinkB=5, connectionstyle="arc3,rad=0.05"),
                    zorder=3)
        
        # Branch box
        box = FancyBboxPatch((bx, by), bw, bh,
                            boxstyle="round,pad=0.02,rounding_size=0.03",
                            facecolor='white', edgecolor=border_colors[idx], linewidth=1.8,
                            transform=ax.transAxes, zorder=4)
        ax.add_patch(box)
        
        # Header banner inside branch box
        h_box = FancyBboxPatch((bx + 0.005, by + bh - 0.075), bw - 0.01, 0.065,
                               boxstyle="round,pad=0.01,rounding_size=0.02",
                               facecolor=header_bgs[idx], edgecolor='none',
                               transform=ax.transAxes, zorder=4)
        ax.add_patch(h_box)
        
        ax.text(bx + 0.02, by + bh - 0.042, b_title, ha='left', va='center',
                fontsize=10.5, fontweight='bold', color=border_colors[idx],
                family='sans-serif', transform=ax.transAxes, zorder=5)
        
        # Content text
        ax.text(bx + 0.02, by + (bh - 0.08) / 2, b_desc, ha='left', va='center',
                fontsize=8.5, color='#263238', family='sans-serif',
                transform=ax.transAxes, zorder=5, linespacing=1.4)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    save_path = os.path.join(output_dir, data["filename"])
    plt.savefig(save_path, dpi=300, bbox_inches='tight', pad_inches=0.15)
    plt.close()
    print(f" -> Đã tạo Mindmap 300 DPI: {data['filename']}")

print(f"Bắt đầu sinh 16 Sơ đồ tư duy Mindmap vector 300 DPI cho Toán 9 HK2...")
for item in mindmaps_data:
    draw_mindmap(item)
print(f"Hoàn tất tạo thành công 16 Mindmaps vector 300 DPI cho Toán 9 HK2!")
