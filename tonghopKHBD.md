# Tổng hợp hệ thống Soạn KHBD (sau đợt chỉnh 2026-08-26)

Tài liệu này mô tả **đúng những gì đã thay**, để AI khác phản biện. Không phải hướng dẫn quảng cáo.

## 1. Yêu cầu gốc

0. Giữ nguyên code không đụng tới.
1. Mục tiêu kiến thức bám CT GDPT 2018 / Thông tư 32/2018/TT-BGDĐT, không tự tạo.
2. Giáo án 2 cột, form mẫu `GIAO AN/demo.docx`.
3. Tích hợp PPDH, kỹ thuật, hoạt động đặc thù theo 3 ảnh; khi soạn chọn mục phù hợp môn/lớp.
4. Bám sát tuyệt đối nội dung giáo viên cung cấp, không tự thêm.
5. File này để phản biện.

## 2. File đã đụng / không đụng

**Đã sửa hoặc tạo**

| File | Việc |
|---|---|
| `soankhbd.html` | Tab 0: 3 panel catalog (PP / KT / HĐ); nạp `js/khbd-yccd.js` |
| `js/khbd-pedagogy-catalog.js` | Catalog đúng 3 ảnh + `isPedagogyRecommended` |
| `js/khbd-yccd.js` | **Mới.** YCCĐ Toán 6–9 nguyên văn từ `GIAO AN/yeucau.docx` |
| `js/khbd-prompts.js` | TT 32, `SOURCE_LOCK`, bảng 2 cột, bỏ lệnh invent bài tập |
| `js/khbd-app.js` | Render catalog, state, khóa nguồn, assert 1-Click, header form |
| `js/khbd-docx.js` | Header hành chính demo; bảng 2 cột hoạt động 50/50 |
| `css/khbd-styles.css` | Lưới 2 cột pedagogy, không uppercase label catalog |
| `tonghopKHBD.md` | File này |

**Không đụng**

- `GIAO AN/**` (chỉ đọc `demo.docx`, `yeucau.docx`)
- `js/khbd-gemini.js`, `js/khbd-standards.js`, `js/khbd-curriculum.js` (mục lục)
- Login, TKB, kttx, matrande, admin, API khác ngoài luồng KHBD

## 3. Form 2 cột (đã đối chiếu `demo.docx`)

File mẫu **không** dùng cột “Hoạt động của giáo viên | Hoạt động của học sinh”.

Tiêu đề cột thật:

| Hoạt động của GV và HS | Nội dung |

Triển khai:

- Markdown: đúng 4 hàng (Chuyển giao / Thực hiện / Báo cáo, thảo luận / Kết luận, nhận định).
- Cột trái: việc GV và HS. Cột phải: nhiệm vụ, câu hỏi, đáp án, kiến thức chốt **lấy từ nguồn**.
- Hoạt động B: mỗi đơn vị kiến thức một bảng riêng.
- DOCX: nếu header chứa “Hoạt động của GV” thì 2 cột 4500/4500 DXA.

Header hành chính (Tab 5 + Word): Trường, Tổ chuyên môn, Họ tên GV, Ngày soạn, Ngày dạy, KẾ HOẠCH BÀI DẠY, Tên bài soạn, Môn-Lớp, Bộ sách = “SGK do giáo viên cung cấp”, Thời lượng.

Không thêm lại tab E/F/G hay IV. Kết luận/dặn dò trong demo chưa được đưa vào UI.

## 4. Mục tiêu kiến thức / TT 32

- `GIAO AN/yeucau.docx` là YCCĐ môn **Toán lớp 6–9** (CT GDPT 2018 / TT 32).
- `getOfficialYccd({ subjectId, grade, topic, visionText })` chọn tối đa 3 khối YCCĐ khớp từ khóa bài.
- Prompt mục tiêu: chỉ viết YCCĐ đó (hoặc YCCĐ in trên SGK/Tab 1). Cấm bịa thang Bloom nếu không có trong nguồn.
- Môn khác / lớp 1–5, 10–12: **chưa có CSDL YCCĐ**. Hệ thống yêu cầu nguồn SGK/vision; nếu không có YCCĐ in trên nguồn thì ghi “Cần đối chiếu YCCĐ CT GDPT 2018 (TT 32)”.

Hạn chế parser: một số dòng bảng Word bị dính (ví dụ ghép ô “ước chung và bội chung”). Phản biện nên so mẫu YCCĐ với `yeucau.docx` gốc.

## 5. Catalog 3 ảnh

**Phương pháp dạy học hiện đại (15):** PBL, STEM/STEAM, Lớp học đảo ngược, Dạy học hợp tác, Học qua trò chơi, Dạy học phân hóa, Kỹ thuật Socratic, Bản đồ tư duy, Học tập trải nghiệm, 5W1H, Think-Pair-Share, Jigsaw, Gallery Walk, KWL, Mô hình 5E.

**Kĩ thuật dạy học tích cực theo pha**

- A Khởi động: Động não, KWL, Câu hỏi kích thích tư duy, Ô chữ/đố vui
- B Hình thành: TPS, Jigsaw, Gallery Walk, Trạm học tập, Sơ đồ tư duy, Khăn trải bàn
- C Luyện tập: Bài tập phân hóa 3 mức, Peer Assessment, Tranh luận, Case Study, Role-play
- D Vận dụng: Dự án mini, Nhật ký học tập, Exit Ticket, Bài tập mở

**Hoạt động đặc thù môn học (12, generic):** thảo luận nhóm chuyên đề; thực hành/thí nghiệm; phân tích tình huống; trò chơi khởi động; tập luyện kỹ năng theo nhóm; thi đấu nhóm; phân tích video/hình; peer coaching; trạm xoay vòng; sản phẩm/dự án mini; thuyết trình; thực hành công nghệ số.

Gợi ý môn/lớp: badge “Phù hợp môn này” (STEM/thí nghiệm → Toán-KHTN; 5E → khoa học; role-play/tranh luận → văn, ngoại ngữ, GDCD…). **Không ẩn** mục khác. **Không tự tick.**

Khi GV không chọn: prompt chỉ cho phép 1–2 mục catalog đúng nhãn, phù hợp môn/lớp; không bịa tên PPDH.

`assertPhasePedagogyOutput` chỉ bắt kỹ thuật **đã chọn của đúng pha** có mặt trong bảng d). 1-Click cũng assert + 1 lần sửa.

## 6. SOURCE_LOCK

Mọi prompt (`getPromptTemplate`) gắn `PROMPTS.SOURCE_LOCK`:

- Chỉ dùng ảnh/PDF, Tab 1, tên bài/môn/lớp, YCCĐ official, bối cảnh lớp.
- Cấm bịa định nghĩa, định lý, số liệu, đề, đáp án, số trang.
- Luyện tập/vận dụng: chỉ bài có trong nguồn; thiếu thì `[Không có trong tài liệu đã cung cấp]`.
- Đã xóa lệnh invent 4 câu TN / bài thực tiễn có số liệu ở HĐ C và D.

Chặn UI:

- Tạo I. Mục tiêu: cần ảnh/vision **hoặc** YCCĐ Toán 6–9.
- Tạo HĐ A–D và 1-Click: cần ảnh hoặc vision. Bỏ fallback “Dựa trên nội dung SGK do giáo viên cung cấp.”

## 7. Lỗ hổng còn lại (cần phản biện)

1. YCCĐ mới số hóa Toán 6–9; các môn/khối khác chưa có corpus chính thức.
2. Parser `yeucau.docx` không hoàn hảo (bảng Word bị vỡ ô).
3. Không có test tự động (Playwright/Jest) cho 1-Click hay xuất DOCX.
4. Tab E/F/G và IV demo không còn trên UI; prompt E/F/G vẫn nằm trong `khbd-prompts.js` (legacy).
5. `assertPhasePedagogyOutput` so khớp chuỗi nhãn — model đổi wording có thể fail oan hoặc lọt.
6. Gemini vẫn có thể bịa nếu bỏ qua prompt; khóa nguồn là ràng buộc mềm + chặn khi không có file nguồn.
7. Header Word và preview Markdown là hai đường; lệch format nhỏ vẫn có thể xảy ra.
8. Draft cũ lưu `methods` theo nhãn tiếng Việt 6 mục cũ / `phasePedagogy` id cũ — UI mới nhận id; lựa chọn cũ có thể không tick lại.

## 8. Checklist phản biện

- [ ] Tab 0: đủ 15 PP, 4 nhóm KT, 12 HĐ; lưới 2 cột desktop / 1 cột mobile.
- [ ] Đổi môn Ngữ văn vs Toán: badge gợi ý đổi, catalog không mất.
- [ ] Tick >6 PP, reload: không bị cắt còn 6.
- [ ] Không ảnh/vision: 1-Click và tạo HĐ bị chặn; Toán 6 “Tập hợp” vẫn tạo được mục tiêu từ YCCĐ TT 32.
- [ ] Có ảnh SGK: mục tiêu kiến thức trích YCCĐ, không bịa Bloom; HĐ C không invent TN 4 lựa chọn.
- [ ] Bảng d) đúng 2 cột demo, 4 hàng; HĐ B nhiều bảng.
- [ ] Xuất DOCX: header hành chính + bảng 2 cột không dồn 1 cột.
- [ ] Tick Think-Pair-Share ở Khởi động → bảng A chứa đúng nhãn; không nhét Jigsaw nếu không chọn.

## 9. Luồng chạy (không đổi kiến trúc)

`soankhbd.html` → curriculum → prompts → gemini → docx → standards → pedagogy-catalog → **yccd** → app.

1-Click: Vision (nếu có ảnh) → I. Mục tiêu → II. Thiết bị → A → B → C → D (assert từng pha) → Tab 5.
