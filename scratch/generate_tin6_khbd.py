import os, re

with open('TROLYTHIEN/TEMP/tin6_dump.txt', 'r', encoding='utf-8') as f:
    raw = f.read()

# Extract questions
questions = []
for i in range(1, 29):
    pattern = rf'Câu {i}\.\s*(.*?)(?=Câu {i+1}\.|\n\nII\. PHẦN TỰ LUẬN|\Z)'
    m = re.search(pattern, raw, re.DOTALL)
    if m:
        q_text = m.group(1).strip()
        # Clean up line numbers like [4], [5] from docx dump
        q_text = re.sub(r'\[\d+\]\s*', '', q_text)
        # Clean up quotes
        q_text = q_text.replace('\"', '“')
        questions.append((i, q_text))

answers_mcq = ['B', 'A', 'A', 'B', 'C', 'A', 'C', 'C', 'C', 'C', 'A', 'C', 'D', 'D',
               'D', 'C', 'B', 'B', 'D', 'C', 'C', 'C', 'D', 'A', 'C', 'C', 'B', 'C']

md = []
md.append('Tiết 10 - KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ I (TIN HỌC 6)')
md.append('*Thời lượng thực hiện: 01 tiết (45 phút)*\n')
md.append('# I. MỤC TIÊU')
md.append('## 1. Về kiến thức')
md.append('- Đánh giá mức độ đạt chuẩn kiến thức, kĩ năng của học sinh sau khi học xong hai chủ đề:')
md.append('  + **Chủ đề 1: Máy tính và cộng đồng** (Bài 1. Thông tin và dữ liệu; Bài 2. Xử lí thông tin; Bài 3. Thông tin trong máy tính).')
md.append('  + **Chủ đề 2: Mạng máy tính và Internet** (Bài 4. Mạng máy tính; Bài 5. Internet).')
md.append('- Kiểm tra khả năng nhận biết, thông hiểu và vận dụng các kiến thức cốt lõi:')
md.append('  + Phân biệt được thông tin và dữ liệu; nhận biết 4 bước cơ bản của quá trình xử lí thông tin.')
md.append('  + Hiểu được bit là đơn vị nhỏ nhất biểu diễn thông tin; nắm vững và quy đổi thành thạo các đơn vị đo dung lượng thông tin (B, KB, MB, GB, TB).')
md.append('  + Nhận biết các thành phần cơ bản và lợi ích của mạng máy tính; hiểu được khái niệm và các ứng dụng thiết thực của Internet.')
md.append('  + Vận dụng kiến thức để giải bài toán thực tế về dung lượng lưu trữ (Câu 29) và mã hóa hình ảnh dạng lưới thành dãy bit (Câu 30).\n')

md.append('## 2. Về năng lực')
md.append('a) Năng lực chung:')
md.append('- **Tự chủ và tự học:** Tự giác, độc lập hoàn thành bài kiểm tra; phân bổ hợp lý thời gian 45 phút cho các phần trắc nghiệm và tự luận; tự đánh giá được mức độ hoàn thành bài của bản thân.')
md.append('- **Giải quyết vấn đề và sáng tạo:** Vận dụng linh hoạt các kiến thức biểu diễn dữ liệu và dung lượng nhớ để tính toán chính xác và mã hóa hình ảnh chính xác.\n')

md.append('b) Năng lực đặc thù môn Tin học:')
md.append('- **Năng lực C (NLc - Tổ chức lưu trữ, tìm kiếm và trao đổi thông tin):** Hiểu rõ bản chất biểu diễn dữ liệu nhị phân (dãy bit); thực hiện chuẩn xác phép chuyển đổi đơn vị dung lượng bộ nhớ từ GB sang MB để tính số lượng bản nhạc lưu trữ.')
md.append('- **Năng lực D (NLd - Ứng dụng công nghệ thông tin và truyền thông trong học và tự học):** Nhận diện chính xác vai trò, lợi ích của mạng máy tính và Internet trong học tập, giao tiếp và đời sống hàng ngày.\n')

md.append('c) Năng lực số (NLS):')
md.append('- ***5.3.TC1a: HS nắm vững nguyên lý mã hóa thông tin số; thực hành mã hóa bức tranh ma trận điểm ảnh thành chuỗi ký tự nhị phân 0 và 1 chuẩn xác.***\n')

md.append('d) Năng lực Trí tuệ Nhân tạo (AI):')
md.append('- ***6.D1.1: HS có ý thức tự lực hoàn thành bài kiểm tra, trung thực học thuật, không sử dụng tài liệu hay các công cụ hỗ trợ trí tuệ nhân tạo tra cứu trái phép trong phòng thi.***\n')

md.append('## 3. Về phẩm chất')
md.append('- **Trung thực:** Nghiêm túc, trung thực tuyệt đối trong giờ kiểm tra; không trao đổi, không quay cóp, không sử dụng tài liệu; phản ánh đúng năng lực học tập thực chất của bản thân.')
md.append('- **Trách nhiệm:** Tuân thủ nghiêm ngặt quy chế phòng thi; có ý thức giữ gìn trật tự lớp học; nộp bài đúng giờ quy định.')
md.append('- **Chăm chỉ:** Cẩn thận, tỉ mỉ khi tô đáp án trắc nghiệm và trình bày rõ ràng, mạch lạc lời giải các câu tự luận.\n')

md.append('---\n')
md.append('# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU')
md.append('## 1. Giáo viên')
md.append('- Đề kiểm tra in sẵn theo đúng số lượng học sinh lớp 6.')
md.append('- Ma trận đề thi, bản đặc tả ma trận kiểm tra giữa học kì 1.')
md.append('- Đáp án và hướng dẫn chấm biểu điểm chi tiết.')
md.append('## 2. Học sinh')
md.append('- Ôn tập kỹ toàn bộ kiến thức Chủ đề 1 và Chủ đề 2 theo đề cương ôn tập.')
md.append('- Chuẩn bị đầy đủ dụng cụ học tập: bút mực, bút chì, thước kẻ.\n')

md.append('## 3. KHUNG MA TRẬN VÀ BẢNG ĐẶC TẢ ĐỀ KIỂM TRA')
md.append('| TT | Chủ đề | Mức độ nhận thức | Tổng số câu | Tổng điểm |')
md.append('| :--- | :--- | :---: | :---: | :---: |')
md.append('| 1 | **Chủ đề 1: Máy tính và cộng đồng**<br>- Bài 1: Thông tin và dữ liệu<br>- Bài 2: Xử lí thông tin<br>- Bài 3: Thông tin trong máy tính | Nhận biết: 8 TN<br>Thông hiểu: 6 TN<br>Vận dụng: 1 TL (Câu 29)<br>Vận dụng cao: 1 TL (Câu 30) | 14 TN<br>2 TL | 6,5 điểm<br>*(3,5 đ TN + 3,0 đ TL)* |')
md.append('| 2 | **Chủ đề 2: Mạng máy tính và Internet**<br>- Bài 4: Mạng máy tính<br>- Bài 5: Internet | Nhận biết: 8 TN<br>Thông hiểu: 6 TN | 14 TN | 3,5 điểm<br>*(3,5 đ TN)* |')
md.append('|  | **TỔNG CỘNG** | **28 câu TN (7,0 đ) + 2 câu TL (3,0 đ)** | **30 câu** | **10,0 điểm (100%)** |\n')

md.append('## 4. ĐỀ KIỂM TRA CHÍNH THỨC (TRƯỜNG THCS TRẦN PHÚ)')
md.append('> **UBND XÃ XUÂN ĐÔNG - TRƯỜNG THCS TRẦN PHÚ**  ')
md.append('> **ĐỀ KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KỲ I - NĂM HỌC 2026 - 2027**  ')
md.append('> **MÔN: TIN HỌC 6**  ')
md.append('> *Thời gian làm bài: 45 phút (Không kể thời gian phát đề)*\n')

md.append('### I. PHẦN TRẮC NGHIỆM (7,0 điểm - Gồm 28 câu, mỗi câu 0,25 điểm)\n')
for idx, q_txt in questions:
    md.append(f'**Câu {idx}.** {q_txt}\n')

md.append('### II. PHẦN TỰ LUẬN (3,0 điểm)\n')
md.append('**Câu 29 (1,5 điểm).** Một thẻ nhớ $1\\text{ GB}$ chứa được khoảng bao nhiêu bản nhạc? Biết rằng mỗi bản nhạc có dung lượng khoảng $4\\text{ MB}$.\n')
md.append('**Câu 30 (1,5 điểm).** Em hãy mã hóa bức tranh chữ H dạng lưới dưới đây thành dãy bit (với quy ước ô trắng là $0$, ô đen là $1$):\n')
md.append('![Bức tranh chữ H dạng lưới](hinh_ve/tin6_gk1_cau30.png)\n')

md.append('---\n')
md.append('## 5. HƯỚNG DẪN CHẤM VÀ ĐÁP ÁN CHI TIẾT')
md.append('### I. ĐÁP ÁN PHẦN TRẮC NGHIỆM (7,0 điểm)\n')
md.append('| Câu | Đáp án | Câu | Đáp án | Câu | Đáp án | Câu | Đáp án |')
md.append('| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |')
for r in range(7):
    c1 = r + 1
    c2 = r + 8
    c3 = r + 15
    c4 = r + 22
    md.append(f'| **{c1}** | **{answers_mcq[c1-1]}** | **{c2}** | **{answers_mcq[c2-1]}** | **{c3}** | **{answers_mcq[c3-1]}** | **{c4}** | **{answers_mcq[c4-1]}** |')

md.append('\n### II. ĐÁP ÁN VÀ THANG ĐIỂM PHẦN TỰ LUẬN (3,0 điểm)\n')
md.append('| Câu | Nội dung hướng dẫn chấm | Điểm |')
md.append('| :---: | :--- | :---: |')
md.append('| **Câu 29**<br>*(1,5 đ)* | - Đổi đơn vị dung lượng: $1\\text{ GB} = 1\\,024\\text{ MB}$.<br>- Số bản nhạc có thể lưu trữ trong thẻ nhớ là:<br>$$1\\,024 : 4 = 256\\text{ (bản nhạc)}$$<br>- Đáp số: $256$ bản nhạc. | 0,75 đ<br><br>0,75 đ |')
md.append('| **Câu 30**<br>*(1,5 đ)* | - Học sinh quan sát lưới $6 \\times 9$ ô vuông, xác định quy ước mã hóa: ô trắng là $0$, ô đen là $1$.<br>- Mã hóa từng hàng từ trên xuống dưới:<br>+ Hàng 1: `000000000`<br>+ Hàng 2: `011000110`<br>+ Hàng 3: `011111110`<br>+ Hàng 4: `011111110`<br>+ Hàng 5: `011000110`<br>+ Hàng 6: `000000000`<br>*(Đúng mỗi hàng được 0,25 điểm; nếu viết thành một dãy liên tục: `000000000011000110011111110011111110011000110000000000` vẫn cho điểm tối đa).* | 0,25 đ<br><br><br>0,25 đ<br>0,25 đ<br>0,25 đ<br>0,25 đ<br>0,25 đ |')

md.append('\n---\n')
md.append('# III. TIẾN TRÌNH DẠY HỌC (TỔ CHỨC KIỂM TRA)')
md.append('## 1. Hoạt động 1: Ổn định tổ chức và giao đề kiểm tra (5 phút)')
md.append('a) **Mục tiêu:** Tạo tâm thế bình tĩnh, nghiêm túc, sẵn sàng làm bài; phổ biến quy chế thi và phát đề đến từng học sinh.')
md.append('b) **Nội dung:**')
md.append('- Kiểm tra sĩ số lớp, sắp xếp chỗ ngồi học sinh ngay ngắn, đảm bảo khoảng cách.')
md.append('- Quán triệt quy chế: Học sinh không được trao đổi, không xem tài liệu, cất toàn bộ sách vở vào ngăn bàn/túi xách.')
md.append('- Phát đề kiểm tra tận tay từng học sinh, nhắc học sinh ghi rõ Họ tên, Lớp vào giấy làm bài.')
md.append('- Cho học sinh 1 - 2 phút kiểm tra đề in rõ ràng, không rách nát, đủ 28 câu trắc nghiệm và 2 câu tự luận.')
md.append('c) **Sản phẩm:** Học sinh ổn định vị trí, có đề kiểm tra đầy đủ, sẵn sàng làm bài.')
md.append('d) **Tổ chức thực hiện:** Giáo viên chủ động điều hành, bao quát toàn bộ lớp học.\n')

md.append('## 2. Hoạt động 2: Học sinh làm bài kiểm tra (35 phút)')
md.append('a) **Mục tiêu:** Đánh giá đúng năng lực, kiến thức và phẩm chất trung thực của học sinh.')
md.append('b) **Nội dung:**')
md.append('- Học sinh tập trung làm bài độc lập, nghiêm túc, không trao đổi.')
md.append('- Học sinh đọc kĩ từng câu trắc nghiệm, suy luận và ghi kết quả vào phiếu trả lời; đối với phần tự luận, trình bày các bước tính toán và ghi dãy bit cẩn thận.')
md.append('- Giáo viên thực hiện giám sát nghiêm túc, bao quát phòng thi, theo dõi thời gian và không giải thích gì thêm về đề thi.')
md.append('c) **Sản phẩm:** Bài làm kiểm tra hoàn chỉnh trên giấy kiểm tra của từng học sinh.')
md.append('d) **Tổ chức thực hiện:** Học sinh làm bài độc lập; giáo viên nhắc nhở mốc thời gian còn 10 phút, 5 phút để học sinh rà soát bài.\n')

md.append('## 3. Hoạt động 3: Thu bài, nhận xét và dặn dò (5 phút)')
md.append('a) **Mục tiêu:** Thu đủ số lượng bài thi; nhận xét ý thức thi cử của lớp; hướng dẫn nhiệm vụ học tập bài tiếp theo.')
md.append('b) **Nội dung:**')
md.append('- Hết giờ làm bài, giáo viên yêu cầu toàn bộ học sinh dừng bút, đặt bút xuống bàn.')
md.append('- Thu bài theo từng dãy bàn, đếm đủ số bài thi khớp với sĩ số học sinh dự thi.')
md.append('- Giáo viên nhận xét nhanh về tinh thần, thái độ và ý thức chấp hành nội quy kiểm tra của lớp.')
md.append('- Dặn dò: Học sinh về nhà xem trước **Bài 6. Mạng thông tin toàn cầu (World Wide Web)**, tìm hiểu về website, địa chỉ web và trình duyệt web.')
md.append('c) **Sản phẩm:** Toàn bộ bài kiểm tra đã được thu đủ, được niêm phong/bảo quản theo quy định.')
md.append('d) **Tổ chức thực hiện:** Lớp trưởng hỗ trợ đếm bài, giáo viên ghi sổ theo dõi và nhận xét tiết học.')

out_path = 'TROLYTHIEN/TEMP/02.11_Tin6/02_KiemTraGiuaHK1_Tin6_Tiet10.md'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(md))
print('Successfully generated Tin 6 KHBD at:', out_path)
