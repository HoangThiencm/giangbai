import sys

sys.stdout.reconfigure(encoding='utf-8')

TARGET_VA_3 = '''### Vá 3 — Bảng 2 cột sư phạm chuẩn CV 5512 và GDPT 2018

Trong cấu trúc hồ sơ Kế hoạch bài dạy chuẩn CV 5512 và GDPT 2018 gồm 4 bước:
1. Chuyển giao nhiệm vụ
2. Thực hiện nhiệm vụ
3. Báo cáo, thảo luận
4. Kết luận, nhận định
với sự tương tác hai chiều:
| Hoạt động của Giáo viên | Hoạt động của Học sinh |
| --- | --- |
| Việc GV giao, câu hỏi, cách tổ chức | Việc HS làm, sản phẩm, cách báo cáo |

**ĐẶC BIỆT LƯU Ý KHI LÊN SLIDE TRÌNH CHIẾU CHO HỌC SINH:**
Slide trình chiếu là công cụ trực quan giảng dạy giữa giáo viên và học sinh, **TUYỆT ĐỐI KHÔNG** đưa các bước hành chính sư phạm giáo án vào slide (CẤM ghi "Bước 1: Chuyển giao nhiệm vụ", "Bước 2: Tổ chức thực hiện", "4 BƯỚC CV 5512" lên slide chiếu, học sinh không cần học các bước hành chính này!).

Bố cục 2 cột sư phạm chuẩn trên slide chiếu:
- **Cột trái (`col-board` - Bảng ghi bài):** Lưu lại nội dung cốt lõi học sinh ghi vào vở (Tiêu đề mục, Định nghĩa, Công thức tổng quát `data-step="0"` hoặc `fixed`, Ví dụ mẫu và lời giải chuẩn).
- **Cột phải (`col-task` - Hoạt động học tập):** Không gian tương tác của học sinh (Tình huống khởi động, Hoạt động khám phá, Câu hỏi nhận biết, Bài tập luyện tập, Vận dụng, Trò chơi trắc nghiệm).'''

VA_3_CURRENT = '''### Vá 3 — Bảng 2 cột sư phạm: Bảng ghi bài & Hoạt động học tập

Slide trình chiếu là công cụ trực quan tương tác giữa giáo viên và học sinh, **TUYỆT ĐỐI KHÔNG** đưa các bước hành chính sư phạm giáo án vào slide (CẤM ghi "Bước 1: Chuyển giao nhiệm vụ", "Bước 2: Tổ chức thực hiện", "4 BƯỚC CV 5512" lên slide trình chiếu, học sinh không cần học các bước hành chính này!).

Bố cục 2 cột sư phạm chuẩn trên slide:
- **Cột trái (`col-board` - Bảng ghi bài):** Lưu lại nội dung cốt lõi học sinh ghi vào vở (Tiêu đề mục, Định nghĩa, Công thức tổng quát `data-step="0"` hoặc `fixed`, Ví dụ mẫu và lời giải chuẩn).
- **Cột phải (`col-task` - Hoạt động học tập):** Không gian tương tác của học sinh (Tình huống khởi động, Hoạt động khám phá, Câu hỏi nhận biết, Bài tập luyện tập, Vận dụng, Trò chơi trắc nghiệm).'''

for fn in ['.agents/rules/tao-bai-giang-html.md', 'TROLYTHIEN/10_BAI_GIANG_HTML/PROMPT_TAO_BAI_GIANG_HTML.md']:
    with open(fn, 'r', encoding='utf-8') as f:
        content = f.read()

    if VA_3_CURRENT in content:
        content = content.replace(VA_3_CURRENT, TARGET_VA_3)
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated Vá 3 in {fn}")
    else:
        print(f"VA_3_CURRENT not found in {fn}")
