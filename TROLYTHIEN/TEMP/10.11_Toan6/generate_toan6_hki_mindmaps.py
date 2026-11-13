# -*- coding: utf-8 -*-
"""
Script sinh Sơ đồ tư duy Mindmap vector 300 DPI cho môn Toán 6 (Tuần 13 - 18)
"""
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.stdout.reconfigure(encoding='utf-8')

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Segoe UI', 'Tahoma']
plt.rcParams['axes.unicode_minus'] = False

OUT_DIR = "TROLYTHIEN/TEMP/10.11_Toan6/mindmaps"
os.makedirs(OUT_DIR, exist_ok=True)

def create_base_canvas(title, subtitle):
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
    ax.set_facecolor("#F8FAFC")
    fig.patch.set_facecolor("#F8FAFC")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    ax.text(50, 96, title, ha='center', va='center', fontsize=15, fontweight='bold', color='#1E293B')
    ax.text(50, 92.5, subtitle, ha='center', va='center', fontsize=11, fontstyle='italic', color='#475569')
    return fig, ax

def draw_tiet37():
    fig, ax = create_base_canvas("SƠ ĐỒ TƯ DUY LUYỆN TẬP CHUNG: CỘNG TRỪ SỐ NGUYÊN VÀ DẤU NGOẶC",
                                "(Môn Toán 6 - Số học - Tiết 37 - Tuần 13)")
    # Central
    c = patches.FancyBboxPatch((35, 43), 30, 14, boxstyle="round,pad=1.2,rounding_size=2", ec="#2563EB", fc="#DBEAFE", lw=2.5)
    ax.add_patch(c)
    ax.text(50, 51.5, "PHÉP CỘNG, PHÉP TRỪ", ha='center', va='center', fontsize=12, fontweight='bold', color="#1E3A8A")
    ax.text(50, 47, "& QUY TẮC DẤU NGOẶC", ha='center', va='center', fontsize=11, fontweight='bold', color="#2563EB")
    
    # 4 branches
    # B1: Cộng cùng dấu
    b1 = patches.FancyBboxPatch((4, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#0284C7", fc="#E0F2FE", lw=1.8)
    ax.add_patch(b1)
    ax.text(20, 83.5, "1. CỘNG CÙNG DẤU", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#0369A1")
    ax.text(6, 75.5, "• Cùng dương: cộng như hai số tự nhiên\n• Cùng âm: cộng hai số đối rồi đặt dấu (-)\n  Ví dụ: (-15) + (-20) = -(15 + 20) = -35\n• Kết quả luôn cùng dấu với hai số hạng", fontsize=8.8, color="#0F172A", linespacing=1.3)
    
    # B2: Cộng khác dấu
    b2 = patches.FancyBboxPatch((4, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#D97706", fc="#FEF3C7", lw=1.8)
    ax.add_patch(b2)
    ax.text(20, 29.5, "2. CỘNG KHÁC DẤU", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B45309")
    ax.text(6, 21, "• Hai số đối nhau có tổng bằng 0: a + (-a) = 0\n• Không đối nhau: lấy số lớn trừ số bé\n  rồi đặt dấu của số có số đối lớn hơn\n  Ví dụ: (-30) + 12 = -(30 - 12) = -18", fontsize=8.8, color="#0F172A", linespacing=1.3)
    
    # B3: Phép trừ số nguyên
    b3 = patches.FancyBboxPatch((64, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#7C3AED", fc="#F3E8FF", lw=1.8)
    ax.add_patch(b3)
    ax.text(80, 83.5, "3. PHÉP TRỪ SỐ NGUYÊN", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#6D28D9")
    ax.text(66, 75.5, "• Quy tắc: a - b = a + (-b)\n  (Cộng với số đối của số trừ)\n• Trừ đi số âm là cộng với số dương:\n  a - (-b) = a + b\n  Ví dụ: 5 - (-8) = 5 + 8 = 13", fontsize=8.8, color="#0F172A", linespacing=1.3)

    # B4: Quy tắc dấu ngoặc
    b4 = patches.FancyBboxPatch((64, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#059669", fc="#D1FAE5", lw=1.8)
    ax.add_patch(b4)
    ax.text(80, 29.5, "4. QUY TẮC DẤU NGOẶC", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#047857")
    ax.text(66, 21, "• Đằng trước dấu (+): Giữ nguyên dấu các số hạng\n• Đằng trước dấu (-): Đổi dấu tất cả các số hạng\n  -(a - b + c) = -a + b - c\n• Đặt dấu ngoặc hợp lý để tính nhanh", fontsize=8.8, color="#0F172A", linespacing=1.3)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "mindmap_toan6_tiet37.png"), dpi=300)
    plt.close()

def draw_tiet42():
    fig, ax = create_base_canvas("SƠ ĐỒ TƯ DUY LUYỆN TẬP CHUNG: PHÉP NHÂN VÀ PHÉP CHIA HẾT SỐ NGUYÊN",
                                "(Môn Toán 6 - Số học - Tiết 42 - Tuần 14)")
    c = patches.FancyBboxPatch((35, 43), 30, 14, boxstyle="round,pad=1.2,rounding_size=2", ec="#D97706", fc="#FEF3C7", lw=2.5)
    ax.add_patch(c)
    ax.text(50, 51.5, "PHÉP NHÂN & PHÉP CHIA", ha='center', va='center', fontsize=12, fontweight='bold', color="#B45309")
    ax.text(50, 47, "ƯỚC VÀ BỘI TRONG Z", ha='center', va='center', fontsize=11, fontweight='bold', color="#D97706")

    # B1: Quy tắc nhân
    b1 = patches.FancyBboxPatch((4, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#0284C7", fc="#E0F2FE", lw=1.8)
    ax.add_patch(b1)
    ax.text(20, 83.5, "1. QUY TẮC NHÂN HAI SỐ NGUYÊN", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#0369A1")
    ax.text(6, 75.5, "• Cùng dấu: tích mang dấu (+)\n  (+) . (+) = (+);  (-) . (-) = (+)\n• Khác dấu: tích mang dấu (-)\n  (+) . (-) = (-);  (-) . (+) = (-)\n• Tích của a với 0 bằng 0", fontsize=8.8, color="#0F172A", linespacing=1.3)

    # B2: Tính chất phép nhân
    b2 = patches.FancyBboxPatch((4, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#7C3AED", fc="#F3E8FF", lw=1.8)
    ax.add_patch(b2)
    ax.text(20, 29.5, "2. TÍNH CHẤT PHÉP NHÂN", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#6D28D9")
    ax.text(6, 21, "• Giao hoán: a . b = b . a\n• Kết hợp: (a . b) . c = a . (b . c)\n• Nhân với 1: a . 1 = a\n• Phân phối với phép cộng:\n  a . (b + c) = a . b + a . c", fontsize=8.8, color="#0F172A", linespacing=1.3)

    # B3: Phép chia hết & Quan hệ chia hết
    b3 = patches.FancyBboxPatch((64, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#059669", fc="#D1FAE5", lw=1.8)
    ax.add_patch(b3)
    ax.text(80, 83.5, "3. PHÉP CHIA HẾT TRONG Z", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#047857")
    ax.text(66, 75.5, "• Cho a, b thuộc Z (b khác 0). Nếu có q thuộc Z\n  sao cho a = b . q thì a chia hết cho b (a : b)\n• Dấu của thương:\n  Cùng dấu -> (+); Khác dấu -> (-)", fontsize=8.8, color="#0F172A", linespacing=1.3)

    # B4: Ước và Bội
    b4 = patches.FancyBboxPatch((64, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#DC2626", fc="#FEE2E2", lw=1.8)
    ax.add_patch(b4)
    ax.text(80, 29.5, "4. ƯỚC VÀ BỘI CỦA SỐ NGUYÊN", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B91C1C")
    ax.text(66, 21, "• Nếu a chia hết cho b thì a là bội của b,\n  b là ước của a\n• Nếu b là ước của a thì -b cũng là ước của a\n  Ư(6) = {1; -1; 2; -2; 3; -3; 6; -6}\n• Số 0 là bội của mọi số nguyên khác 0", fontsize=8.8, color="#0F172A", linespacing=1.3)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "mindmap_toan6_tiet42.png"), dpi=300)
    plt.close()

def draw_tiet43():
    fig, ax = create_base_canvas("SƠ ĐỒ TỔNG KẾT BÀI TẬP CUỐI CHƯƠNG III: SỐ NGUYÊN",
                                "(Môn Toán 6 - Số học - Tiết 43 - Tuần 15)")
    c = patches.FancyBboxPatch((35, 43), 30, 14, boxstyle="round,pad=1.2,rounding_size=2", ec="#7C3AED", fc="#F3E8FF", lw=2.5)
    ax.add_patch(c)
    ax.text(50, 51.5, "TỔNG KẾT CHƯƠNG III", ha='center', va='center', fontsize=12, fontweight='bold', color="#6D28D9")
    ax.text(50, 47, "TẬP HỢP SỐ NGUYÊN Z", ha='center', va='center', fontsize=11, fontweight='bold', color="#7C3AED")

    b1 = patches.FancyBboxPatch((4, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#0284C7", fc="#E0F2FE", lw=1.8)
    ax.add_patch(b1)
    ax.text(20, 83.5, "1. TẬP HỢP SỐ NGUYÊN Z", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#0369A1")
    ax.text(6, 75.5, "• Z = {..., -3, -2, -1, 0, 1, 2, 3, ...}\n• Trục số: điểm gốc 0, chiều dương (phải), âm (trái)\n• Số đối: số đối của a là -a; số đối của 0 là 0\n• So sánh: số âm < 0 < số dương", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b2 = patches.FancyBboxPatch((4, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#D97706", fc="#FEF3C7", lw=1.8)
    ax.add_patch(b2)
    ax.text(20, 29.5, "2. CỘNG VÀ TRỪ SỐ NGUYÊN", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B45309")
    ax.text(6, 21, "• Cộng cùng dấu: cộng phần đối rồi đặt dấu chung\n• Cộng khác dấu: trừ hai số đối rồi đặt dấu số lớn\n• Trừ số nguyên: a - b = a + (-b)\n• Quy tắc dấu ngoặc: trước ngoặc dấu trừ đổi dấu", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b3 = patches.FancyBboxPatch((64, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#059669", fc="#D1FAE5", lw=1.8)
    ax.add_patch(b3)
    ax.text(80, 83.5, "3. NHÂN VÀ CHIA SỐ NGUYÊN", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#047857")
    ax.text(66, 75.5, "• Cùng dấu tích/thương mang dấu (+)\n• Khác dấu tích/thương mang dấu (-)\n• Tính chất: Giao hoán, kết hợp, phân phối\n• Ước và bội: Nếu a chia hết cho b thì b là ước của a", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b4 = patches.FancyBboxPatch((64, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#DC2626", fc="#FEE2E2", lw=1.8)
    ax.add_patch(b4)
    ax.text(80, 29.5, "4. VẬN DỤNG THỰC TIỄN", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B91C1C")
    ax.text(66, 21, "• Độ cao địa lý: đỉnh núi (+), đáy biển (-)\n• Nhiệt độ: nhiệt độ âm dưới 0 độ C\n• Tài chính: tiền có (+), tiền nợ (-), lợi nhuận\n• Lịch sử: năm sau Công nguyên (+), trước CN (-)", fontsize=8.8, color="#0F172A", linespacing=1.3)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "mindmap_toan6_tiet43.png"), dpi=300)
    plt.close()

def draw_tiet44_47():
    fig, ax = create_base_canvas("SƠ ĐỒ HỆ THỐNG HÓA ÔN TẬP CUỐI HỌC KÌ I - SỐ HỌC 6",
                                "(Tổng kết Chương I: Số tự nhiên - Chương II: Tính chia hết - Chương III: Số nguyên)")
    c = patches.FancyBboxPatch((35, 43), 30, 14, boxstyle="round,pad=1.2,rounding_size=2", ec="#1E40AF", fc="#DBEAFE", lw=2.5)
    ax.add_patch(c)
    ax.text(50, 51.5, "ÔN TẬP CUỐI HỌC KÌ I", ha='center', va='center', fontsize=12, fontweight='bold', color="#1E3A8A")
    ax.text(50, 47, "PHẦN SỐ HỌC 6", ha='center', va='center', fontsize=11, fontweight='bold', color="#2563EB")

    b1 = patches.FancyBboxPatch((4, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#0284C7", fc="#E0F2FE", lw=1.8)
    ax.add_patch(b1)
    ax.text(20, 83.5, "1. TẬP HỢP SỐ TỰ NHIÊN (CHƯƠNG I)", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#0369A1")
    ax.text(6, 75.5, "• Tập hợp N và N*\n• Các phép tính +, -, x, : và lũy thừa với số mũ tự nhiên\n• Thứ tự thực hiện phép tính: ngoặc tròn -> vuông -> nhọn\n• Lũy thừa: a^m . a^n = a^(m+n); a^m : a^n = a^(m-n)", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b2 = patches.FancyBboxPatch((4, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#D97706", fc="#FEF3C7", lw=1.8)
    ax.add_patch(b2)
    ax.text(20, 29.5, "2. TÍNH CHIA HẾT TRONG N (CHƯƠNG II)", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B45309")
    ax.text(6, 21, "• Quan hệ chia hết và tính chất chia hết của một tổng\n• Dấu hiệu chia hết cho 2, 5, 3, 9\n• Số nguyên tố, hợp số, phân tích ra thừa số nguyên tố\n• ƯCLN và BCNN: thuật toán tìm qua thừa số nguyên tố", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b3 = patches.FancyBboxPatch((64, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#7C3AED", fc="#F3E8FF", lw=1.8)
    ax.add_patch(b3)
    ax.text(80, 83.5, "3. TẬP HỢP SỐ NGUYÊN (CHƯƠNG III)", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#6D28D9")
    ax.text(66, 75.5, "• Số nguyên âm, số nguyên dương, số 0\n• Trục số, số đối, so sánh hai số nguyên\n• Bốn phép tính trong Z: +, -, x, :\n• Quy tắc dấu ngoặc và tính chất đại số", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b4 = patches.FancyBboxPatch((64, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#059669", fc="#D1FAE5", lw=1.8)
    ax.add_patch(b4)
    ax.text(80, 29.5, "4. KĨ NĂNG TOÁN HỌC TRỌNG TÂM", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#047857")
    ax.text(66, 21, "• Tính hợp lý (giao hoán, kết hợp, phân phối)\n• Tìm x (bài toán tìm thành phần chưa biết)\n• Toán thực tế: chia tổ/phần thưởng, bội chung chu kỳ\n• Tính toán lãi lỗ, chênh lệch nhiệt độ, độ cao", fontsize=8.8, color="#0F172A", linespacing=1.3)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "mindmap_toan6_tiet44_47.png"), dpi=300)
    plt.close()

def draw_hinh_tiet17():
    fig, ax = create_base_canvas("SƠ ĐỒ TƯ DUY LUYỆN TẬP CHUNG: ĐỐI XỨNG TRỤC VÀ ĐỐI XỨNG TÂM",
                                "(Môn Toán 6 - Hình học trực quan - Tiết 17 - Tuần 16)")
    c = patches.FancyBboxPatch((35, 43), 30, 14, boxstyle="round,pad=1.2,rounding_size=2", ec="#059669", fc="#D1FAE5", lw=2.5)
    ax.add_patch(c)
    ax.text(50, 51.5, "TÍNH ĐỐI XỨNG CỦA HÌNH PHẲNG", ha='center', va='center', fontsize=11.5, fontweight='bold', color="#047857")
    ax.text(50, 47, "TRỤC ĐỐI XỨNG & TÂM ĐỐI XỨNG", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#059669")

    b1 = patches.FancyBboxPatch((4, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#0284C7", fc="#E0F2FE", lw=1.8)
    ax.add_patch(b1)
    ax.text(20, 83.5, "1. HÌNH CÓ TRỤC ĐỐI XỨNG", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#0369A1")
    ax.text(6, 75.5, "• Đường thẳng d chia hình thành hai phần\n  mà khi gấp theo d, hai phần trùng khít lên nhau\n• Đường tròn: vô số trục đối xứng (mọi đường kính)\n• Hình chữ nhật: 2 trục đối xứng\n• Hình vuông: 4 trục đối xứng\n• Tam giác đều: 3 trục đối xứng", fontsize=8.5, color="#0F172A", linespacing=1.3)

    b2 = patches.FancyBboxPatch((4, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#D97706", fc="#FEF3C7", lw=1.8)
    ax.add_patch(b2)
    ax.text(20, 29.5, "2. HÌNH CÓ TÂM ĐỐI XỨNG", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B45309")
    ax.text(6, 21, "• Điểm O là tâm đối xứng nếu quay hình\n  nửa vòng quanh O, hình trùng khít với chính nó\n• Hình bình hành, hình thoi, hình chữ nhật, hình vuông:\n  Giao điểm hai đường chéo là tâm đối xứng\n• Đoạn thẳng: trung điểm là tâm đối xứng\n• Đường tròn: tâm đường tròn là tâm đối xứng", fontsize=8.5, color="#0F172A", linespacing=1.3)

    b3 = patches.FancyBboxPatch((64, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#7C3AED", fc="#F3E8FF", lw=1.8)
    ax.add_patch(b3)
    ax.text(80, 83.5, "3. SO SÁNH TRỤC VÀ TÂM ĐỐI XỨNG", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#6D28D9")
    ax.text(66, 75.5, "• Tam giác đều: Có 3 trục đối xứng, KHÔNG có tâm ĐX\n• Hình thang cân: Có 1 trục đối xứng, KHÔNG có tâm ĐX\n• Hình bình hành: Có tâm đối xứng, KHÔNG có trục ĐX\n• Hình tròn, hình vuông, hình thoi, hình chữ nhật:\n  Vừa có trục đối xứng, vừa có tâm đối xứng", fontsize=8.5, color="#0F172A", linespacing=1.3)

    b4 = patches.FancyBboxPatch((64, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#DC2626", fc="#FEE2E2", lw=1.8)
    ax.add_patch(b4)
    ax.text(80, 29.5, "4. ỨNG DỤNG TRONG THỰC TIỄN", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B91C1C")
    ax.text(66, 21, "• Tự nhiên: Cánh bướm, bông hoa tuyết, lá cây\n• Kiến trúc: Chùa Một Cột, tháp Rùa, cầu Tràng Tiền\n• Đồ họa & đời sống: Biển báo giao thông, quốc kỳ,\n  hoa văn thổ cẩm, gạch lát sàn nghệ thuật", fontsize=8.5, color="#0F172A", linespacing=1.3)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "mindmap_toan6_hinh_tiet17.png"), dpi=300)
    plt.close()

def draw_hinh_tiet18():
    fig, ax = create_base_canvas("SƠ ĐỒ TỔNG KẾT BÀI TẬP CUỐI CHƯƠNG V: TÍNH ĐỐI XỨNG",
                                "(Môn Toán 6 - Hình học trực quan - Tiết 18 - Tuần 16)")
    c = patches.FancyBboxPatch((35, 43), 30, 14, boxstyle="round,pad=1.2,rounding_size=2", ec="#0284C7", fc="#E0F2FE", lw=2.5)
    ax.add_patch(c)
    ax.text(50, 51.5, "TỔNG KẾT CHƯƠNG V", ha='center', va='center', fontsize=12, fontweight='bold', color="#0369A1")
    ax.text(50, 47, "TÍNH ĐỐI XỨNG CỦA HÌNH PHẲNG", ha='center', va='center', fontsize=11, fontweight='bold', color="#0284C7")

    b1 = patches.FancyBboxPatch((4, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#059669", fc="#D1FAE5", lw=1.8)
    ax.add_patch(b1)
    ax.text(20, 83.5, "1. TRỤC ĐỐI XỨNG", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#047857")
    ax.text(6, 75.5, "• Thao tác gấp hình theo trục\n• Nhận biết trục đối xứng của các chữ cái: A, M, T, H, X\n• Trục đối xứng trong hình học phẳng cơ bản", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b2 = patches.FancyBboxPatch((4, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#D97706", fc="#FEF3C7", lw=1.8)
    ax.add_patch(b2)
    ax.text(20, 29.5, "2. TÂM ĐỐI XỨNG", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B45309")
    ax.text(6, 21, "• Thao tác quay hình nửa vòng (180 độ)\n• Nhận biết tâm đối xứng của các chữ cái: S, Z, N, H, O\n• Nhận biết tâm đối xứng của các hình trong logo, huy hiệu", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b3 = patches.FancyBboxPatch((64, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#7C3AED", fc="#F3E8FF", lw=1.8)
    ax.add_patch(b3)
    ax.text(80, 83.5, "3. BẢNG PHÂN LOẠI HÌNH ĐỐI XỨNG", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#6D28D9")
    ax.text(66, 75.5, "• Chỉ có trục đối xứng: Tam giác đều, hình thang cân\n• Chỉ có tâm đối xứng: Hình bình hành\n• Vừa có trục vừa có tâm: Hình tròn, hình chữ nhật,\n  hình thoi, hình vuông, lục giác đều", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b4 = patches.FancyBboxPatch((64, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#DC2626", fc="#FEE2E2", lw=1.8)
    ax.add_patch(b4)
    ax.text(80, 29.5, "4. VẼ HÌNH ĐỐI XỨNG", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B91C1C")
    ax.text(66, 21, "• Gấp giấy và cắt hoa văn đối xứng\n• Vẽ phần còn lại của hình qua trục đối xứng cho trước\n• Ứng dụng vẽ hình đối xứng bằng phần mềm GeoGebra", fontsize=8.8, color="#0F172A", linespacing=1.3)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "mindmap_toan6_hinh_tiet18.png"), dpi=300)
    plt.close()

def draw_hinh_tiet19():
    fig, ax = create_base_canvas("SƠ ĐỒ HỆ THỐNG HÓA ÔN TẬP CUỐI HỌC KÌ I - HÌNH HỌC 6",
                                "(Tổng kết Chương IV: Các hình phẳng trong thực tiễn & Chương V: Tính đối xứng)")
    c = patches.FancyBboxPatch((35, 43), 30, 14, boxstyle="round,pad=1.2,rounding_size=2", ec="#1E40AF", fc="#DBEAFE", lw=2.5)
    ax.add_patch(c)
    ax.text(50, 51.5, "ÔN TẬP CUỐI HỌC KÌ I", ha='center', va='center', fontsize=12, fontweight='bold', color="#1E3A8A")
    ax.text(50, 47, "PHẦN HÌNH HỌC 6", ha='center', va='center', fontsize=11, fontweight='bold', color="#2563EB")

    b1 = patches.FancyBboxPatch((4, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#0284C7", fc="#E0F2FE", lw=1.8)
    ax.add_patch(b1)
    ax.text(20, 83.5, "1. CÁC HÌNH ĐỀU & TỨ GIÁC ĐẶC BIỆT", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#0369A1")
    ax.text(6, 75.5, "• Tam giác đều, hình vuông, lục giác đều\n• Hình chữ nhật, hình thoi, hình bình hành, hình thang cân\n• Tính chất cạnh, góc, đường chéo đặc trưng từng hình", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b2 = patches.FancyBboxPatch((4, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#D97706", fc="#FEF3C7", lw=1.8)
    ax.add_patch(b2)
    ax.text(20, 29.5, "2. CÔNG THỨC CHU VI VÀ DIỆN TÍCH", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B45309")
    ax.text(6, 21, "• Hình chữ nhật: C = 2(a+b); S = a.b\n• Hình vuông: C = 4a; S = a^2\n• Hình bình hành: S = a.h; Hình thoi: S = 1/2 m.n\n• Hình thang cân: S = 1/2 (a+b).h", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b3 = patches.FancyBboxPatch((64, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#7C3AED", fc="#F3E8FF", lw=1.8)
    ax.add_patch(b3)
    ax.text(80, 83.5, "3. TÍNH ĐỐI XỨNG CỦA HÌNH PHẲNG", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#6D28D9")
    ax.text(66, 75.5, "• Hình có trục đối xứng (gấp trùng khít)\n• Hình có tâm đối xứng (quay 180 độ trùng khít)\n• Phân loại các hình phẳng theo tính chất đối xứng", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b4 = patches.FancyBboxPatch((64, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#059669", fc="#D1FAE5", lw=1.8)
    ax.add_patch(b4)
    ax.text(80, 29.5, "4. VẬN DỤNG VÀ THỰC HÀNH", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#047857")
    ax.text(66, 21, "• Tính chi phí làm sân, lát gạch, trồng cỏ, làm hàng rào\n• Vẽ hình bằng thước, compa, êke\n• Thực hành trải nghiệm STEM làm tấm thiệp đối xứng\n• Sử dụng phần mềm GeoGebra vẽ hình học", fontsize=8.8, color="#0F172A", linespacing=1.3)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "mindmap_toan6_hinh_tiet19.png"), dpi=300)
    plt.close()

if __name__ == "__main__":
    draw_tiet37()
    draw_tiet42()
    draw_tiet43()
    draw_tiet44_47()
    draw_hinh_tiet17()
    draw_hinh_tiet18()
    draw_hinh_tiet19()
    print(">>> HOÀN TẤT SINH 7 MINDMAP TOÁN 6 VECTOR 300 DPI! <<<")
