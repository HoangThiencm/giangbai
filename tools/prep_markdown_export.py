# -*- coding: utf-8 -*-
import json
import re
import os
import subprocess

transcript_path = r'C:\Users\HoangThien\.gemini\antigravity\brain\206572b5-754e-4527-b556-144818d16115\.system_generated\logs\transcript_full.jsonl'

content = ''
with open(transcript_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if idx == 706:
            obj = json.loads(line)
            for tc in obj.get('tool_calls', []):
                if tc.get('name') == 'write_to_file':
                    content = tc.get('args', {}).get('CodeContent', '')
        elif idx in [716, 718]:
            obj = json.loads(line)
            for tc in obj.get('tool_calls', []):
                if tc.get('name') == 'replace_file_content':
                    target = tc.get('args', {}).get('TargetContent', '')
                    replacement = tc.get('args', {}).get('ReplacementContent', '')
                    content = content.replace(target, replacement)

idx1 = content.find('const BAI_01_MD')
idx2 = content.find('const BAI_02_MD')
idx3 = content.find('const BAI_03_MD')
idx4 = content.find('const BAI_04_MD')
idx_end = content.find('module.exports')

def clean_md(raw):
    s_idx = raw.find('# KẾ HOẠCH')
    if s_idx != -1:
        raw = raw[s_idx:]
    raw = re.sub(r'[\s`;]+$', '', raw)
    return raw

md1 = clean_md(content[idx1:idx2])
md2 = clean_md(content[idx2:idx3])
md3 = clean_md(content[idx3:idx4])
md4 = clean_md(content[idx4:idx_end])

def remove_inline_image_tags(text):
    lines = text.split('\n')
    cleaned_lines = []
    for l in lines:
        trimmed = l.strip()
        if re.match(r'^!\[[^\]]*\]\((?:khbd-ill:)?[^)]+\)$', trimmed):
            cleaned_lines.append(l)
            continue
        
        l = re.sub(r'-\s*Quan sát hình vẽ minh họa hệ thức lượng:\s*`?!\[.*?\]\(.*?\)[\.\s`]*', '- Quan sát hình vẽ minh họa hệ thức lượng giữa cạnh và góc trong tam giác vuông.', l)
        l = re.sub(r'-\s*Tìm hiểu khái niệm góc nâng, góc hạ qua hình vẽ minh họa:\s*`?!\[.*?\]\(.*?\)[\.\s`]*', '- Tìm hiểu khái niệm góc nâng và góc hạ trong đo đạc qua hình vẽ minh họa.', l)
        l = re.sub(r'-\s*Mô hình đo chiều cao tòa tháp/lâu đài:\s*`?!\[.*?\]\(.*?\)[\.\s`]*', '- Mô hình toán học: Đo chiều cao tòa tháp / lâu đài trong thực tế.', l)
        l = re.sub(r'-\s*Quan sát và phân tích Sơ đồ tư duy \(Mindmap\)[^:]*:\s*`?!\[.*?\]\(.*?\)[\.\s`]*', '- Quan sát và phân tích Sơ đồ tư duy (Mindmap) hệ thống kiến thức toàn bài.', l)
        l = re.sub(r'-\s*Trình chiếu và phân tích Sơ đồ tư duy:\s*`?!\[.*?\]\(.*?\)[\.\s`]*', '- Trình chiếu và phân tích Sơ đồ tư duy tổng hợp toàn bộ Chương IV.', l)
        l = re.sub(r'-\s*Quan sát hình vẽ minh họa vị trí tương đối:\s*`?!\[.*?\]\(.*?\)[\.\s`]*', '- Quan sát hình vẽ minh họa vị trí tương đối của điểm và đường tròn.', l)
        l = re.sub(r'-\s*Quan sát hình vẽ minh họa tính đối xứng:\s*`?!\[.*?\]\(.*?\)[\.\s`]*', '- Quan sát hình vẽ minh họa tính đối xứng của đường tròn: Tâm và trục đối xứng.', l)
        
        l = re.sub(r'`!\[([^\]]*)\]\((?:khbd-ill:)?[^)]+\)`', r'\1', l)
        l = re.sub(r'!\[([^\]]*)\]\((?:khbd-ill:)?[^)]+\)', r'\1', l)
        cleaned_lines.append(l)
    return '\n'.join(cleaned_lines)

md1 = remove_inline_image_tags(md1)
md2 = remove_inline_image_tags(md2)
md3 = remove_inline_image_tags(md3)
md4 = remove_inline_image_tags(md4)

# BÀI 01: H.4.11 Lâu đài AI phục dựng chuẩn xác 100%
md1 = md1.replace(
    'nhìn lên đỉnh.\n\n#### c) Sản phẩm:',
    'nhìn lên đỉnh:\n\n![Hình 4.11. Mô hình đo chiều cao tòa lâu đài bằng giác kế](khbd-ill:hinh_sgk_4_11_lau_dai)\n\n#### c) Sản phẩm:'
)
md1 = md1.replace(
    '![Mô hình toán học: Đo chiều cao tòa tháp / lâu đài](khbd-ill:hinh-bai12-do-chieu-cao-thuc-te)\n\n| Hoạt động của GV và HS |',
    '![Mô hình toán học: Đo chiều cao tòa tháp / lâu đài](khbd-ill:hinh-bai12-do-chieu-cao-thuc-te)\n\n![Hình 4.14. Mô hình chiếc thang dựa tường](khbd-ill:hinh_sgk_4_14_chiec_thang)\n\n| Hoạt động của GV và HS |'
)
md1 = md1.replace(
    '- Học sinh làm việc cá nhân và theo nhóm giải các bài tập trong SGK.\n\n#### c) Sản phẩm:',
    '- Học sinh làm việc cá nhân và theo nhóm giải các bài tập trong SGK (Bài 4.11 Hình 4.18):\n\n![Hình 4.18. Bài toán bóng cây trong nắng](khbd-ill:hinh_sgk_4_18_bong_cay)\n\n#### c) Sản phẩm:'
)
md1 = md1.replace(
    '- Phân tích và giải Bài 4.12 hoặc Bài 4.13 SGK trang 78.\n- GV giao nhiệm vụ tìm hiểu ứng dụng đo đạc thực tế tại địa phương.\n\n#### c) Sản phẩm:',
    '- Phân tích và giải Bài 4.12 hoặc Bài 4.13 SGK trang 78:\n\n![Hình 4.22. Mô hình góc nghiêng thùng xe chở rác](khbd-ill:hinh_sgk_4_22_xe_cho_rac)\n\n![Hình 4.23. Mái dốc nhà kho](khbd-ill:hinh_sgk_4_23_mai_nha_kho)\n\n- GV giao nhiệm vụ tìm hiểu ứng dụng đo đạc thực tế tại địa phương.\n\n#### c) Sản phẩm:'
)

# BÀI 02
lines2 = md2.split('\n')
new_lines2 = []
for l in lines2:
    if l.startswith('- Phân tích và giải chi tiết Ví dụ 2 SGK trang 79'):
        new_lines2.append(l)
        new_lines2.append('\n![Hình 4.26. Mặt cắt bức tường hình thang](khbd-ill:hinh_sgk_4_26_buc_tuong_hinh_thang)\n')
    elif l.startswith('- Giải Bài 4.14 SGK trang 80'):
        new_lines2.append(l)
        new_lines2.append('\n![Hình 4.25. Tam giác vuông kích thước trang sách](khbd-ill:hinh_sgk_4_25_tam_giac_vuong)\n')
    elif l.startswith('- Giải Bài 4.16 SGK trang 80'):
        new_lines2.append(l)
        new_lines2.append('\n![Hình 4.27. Đo khoảng cách khúc sông](khbd-ill:hinh_sgk_4_27_dong_song)\n')
    elif l.startswith('- Phân tích đề bài và định hướng giải Bài 4.18'):
        new_lines2.append(l)
        new_lines2.append('\n![Hình 4.29. Đo khoảng cách AB qua hồ nước](khbd-ill:hinh_sgk_4_29_ho_nuoc)\n')
        new_lines2.append('- Tìm hiểu thêm Bài 4.20 SGK trang 80 (Tàu ngầm lặn tạo với mặt nước góc 21° — Hình 4.31):\n')
        new_lines2.append('\n![Hình 4.31. Quỹ đạo lặn của tàu ngầm](khbd-ill:hinh_sgk_4_31_tau_ngam)\n')
    else:
        new_lines2.append(l)
md2 = '\n'.join(new_lines2)

# BÀI 03
lines3 = md3.split('\n')
new_lines3 = []
for l in lines3:
    if l.startswith('- Học sinh làm việc cá nhân và giơ thẻ đáp án cho 5 câu hỏi trắc nghiệm'):
        new_lines3.append(l)
        new_lines3.append('\n![Hình 4.32. Tam giác vuông ABC cho bài trắc nghiệm 4.21](khbd-ill:hinh_sgk_4_32_trac_nghiem)\n')
    elif l.startswith('- Phân tích và giải các bài tập 4.27, 4.28, 4.29'):
        new_lines3.append(l)
        new_lines3.append('\n![Hình 4.35. Mô hình túp lều hình tam giác cân](khbd-ill:hinh_sgk_4_35_tup_leu)\n')
        new_lines3.append('\n![Hình 4.36. Bài toán cây gãy dựa tường](khbd-ill:hinh_sgk_4_36_cay_gay)\n')
    elif l.startswith('- Phân tích đề bài Đố vui Bài 4.30 SGK trang 82'):
        new_lines3.append(l)
        new_lines3.append('\n![Hình 4.38. Phương pháp đo chu vi Trái Đất của Eratosthenes](khbd-ill:hinh_sgk_4_38_trai_dat)\n')
    else:
        new_lines3.append(l)
md3 = '\n'.join(new_lines3)

# BÀI 04
md4 = md4.replace(
    '![Đường tròn và vị trí tương đối của điểm](hinh-bai13-duong-tron-vi-tri-diem)',
    '![Đường tròn và vị trí tương đối của điểm](khbd-ill:hinh-bai13-duong-tron-vi-tri-diem)\n\n![Hình 5.1. Vị trí của điểm đối với đường tròn](khbd-ill:hinh_sgk_5_1_vi_tri_diem)\n\n![Hình 5.2. Đường kính AB của đường tròn](khbd-ill:hinh_sgk_5_2_duong_kinh_ab)'
)
md4 = md4.replace(
    '![Tính đối xứng của đường tròn: Tâm và trục đối xứng](hinh-bai13-tam-va-truc-doi-xung)',
    '![Tính đối xứng của đường tròn: Tâm và trục đối xứng](khbd-ill:hinh-bai13-tam-va-truc-doi-xung)\n\n![Hình 5.3. Tính đối xứng tâm của đường tròn](khbd-ill:hinh_sgk_5_3_doi_xung_tam)\n\n![Hình 5.4. Tính đối xứng trục của đường tròn](khbd-ill:hinh_sgk_5_4_doi_xung_truc)'
)

def ensure_khbd_ill(text):
    lines = text.split('\n')
    out = []
    for l in lines:
        m = re.match(r'^!\[(.*?)\]\((?:khbd-ill:)?(.*?)\)$', l.strip())
        if m:
            out.append(f'![{m.group(1)}](khbd-ill:{m.group(2)})')
        else:
            out.append(l)
    return '\n'.join(out)

def clean_activity_titles(text):
    text = re.sub(r'\(\s*Tiết\s*[\d,\s-]+[:;\-–—]?\s*(\d+\s*phút)\s*\)', r'(\1)', text, flags=re.IGNORECASE)
    text = re.sub(r'\s*\(\s*Tiết\s*[\d,\s-]+\s*\)', '', text, flags=re.IGNORECASE)
    return text

md1 = clean_activity_titles(ensure_khbd_ill(md1))
md2 = clean_activity_titles(ensure_khbd_ill(md2))
md3 = clean_activity_titles(ensure_khbd_ill(md3))
md4 = clean_activity_titles(ensure_khbd_ill(md4))

with open('tools/BAI_01.md', 'w', encoding='utf-8') as f:
    f.write(md1)
with open('tools/BAI_02.md', 'w', encoding='utf-8') as f:
    f.write(md2)
with open('tools/BAI_03.md', 'w', encoding='utf-8') as f:
    f.write(md3)
with open('tools/BAI_04.md', 'w', encoding='utf-8') as f:
    f.write(md4)

print('4 clean markdown files written.')
