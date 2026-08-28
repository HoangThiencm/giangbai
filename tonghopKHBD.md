# Tổng hợp hệ thống Soạn KHBD (hiện trạng)

Tài liệu để AI khác phản biện. Mô tả **đúng code đang chạy**, không quảng cáo.

Ứng dụng: `soankhbd.html` + `js/khbd-*.js` + `css/khbd-styles.css`. SPA client-side, Gemini REST v1beta, bản nháp `localStorage`.

---

## 1. Mục tiêu đã chốt với người dùng

1. Mục tiêu kiến thức bám CT GDPT 2018 / Thông tư 32/2018/TT-BGDĐT, không tự bịa Bloom.
2. Form giáo án 2 cột theo `GIAO AN/demo.docx`.
3. Catalog PPDH / kỹ thuật / HĐ đặc thù theo 3 ảnh mockup; đề xuất theo bài sau khi có nội dung SGK.
4. Bám nguồn SGK giáo viên cung cấp; không invent bài tập, số liệu, số trang.
5. NLS (TT 02/2025) và AI (QĐ 2422): đề xuất 2–3 mục đúng văn bản, không bịa mã.
6. User thường **một Gemini key**; đọc SGK bằng Gemini nhưng phải tiết kiệm quota.
7. Mục tiêu năng lực: **chỉ mô tả**, không nhãn Biểu hiện / Nhiệm vụ–Sản phẩm / Minh chứng.
8. Giữ danh sách `-` / `+` và đánh số; không đổi sang Word bullet cho các ý đó.

---

## 2. File

| File | Vai trò hiện tại |
|---|---|
| `soankhbd.html` | UI; tab mặc định Bước 0 = ảnh/PDF SGK |
| `css/khbd-styles.css` | Giao diện; lưới 2 cột pedagogy |
| `js/khbd-app.js` | Controller: ảnh, 1-Click, đề xuất, khóa nguồn |
| `js/khbd-prompts.js` | Prompt + `ACTIVITY_TABLE_CONTRACT` + `SOURCE_LOCK` |
| `js/khbd-gemini.js` | Gọi Gemini, xoay key, chờ 429 |
| `js/khbd-docx.js` | Xuất Word, OMML, bảng 2 cột |
| `js/khbd-curriculum.js` | Môn 1–12; mục lục bài **chỉ Toán 6–9** |
| `js/khbd-yccd.js` | YCCĐ Toán 6–9 từ `GIAO AN/yeucau.docx` |
| `js/khbd-standards.js` | 6 miền TT 02 + 4 mã QĐ 2422; hàm đề xuất |
| `js/khbd-pedagogy-catalog.js` | Catalog 3 ảnh; đề xuất PPDH theo nội dung bài |
| `api/user_gemini_keys.php` | Lưu key theo tài khoản |
| `GIAO AN/demo.docx` | Form mẫu (chỉ đọc) |
| `GIAO AN/yeucau.docx` | Nguồn YCCĐ Toán 6–9 (chỉ đọc) |

Không đụng: `GIAO AN/js/*`, TKB, kttx, matrande, login.

---

## 3. Thứ tự tab (đã đảo)

0. **Phân tích ảnh/trang SGK** (mở đầu) — dán/PDF, Gemini đọc tối đa 4 trang đã nén.
1. **Thiết lập chung** — trường, lớp, NLS/AI, PPDH.
2. I. Mục tiêu
3. II. Thiết bị
4. III. Tiến trình A–E
5. Toàn bộ + xuất DOCX

Đề xuất NLS/AI/PPDH **chỉ sau khi** `editorVision` có ≥ ~80 ký tự (đã đọc SGK). Tick NLS/AI trước khi có nội dung: hiện panel, **không** tự tick miền.

---

## 4. Đọc SGK và quota 1 key

- Đọc SGK = **Gemini Vision** (đã bỏ Tesseract và Mistral OCR).
- Gửi tối đa **4 ảnh**, nén cạnh dài ≤ 1280px, JPEG ~0.72.
- `maxOutputTokens` lúc đọc ảnh: 4096; soạn chữ: 8192.
- 1-Click **không đọc lại** nếu đã có nội dung Tab 0.
- Các bước I–III **không gửi ảnh**.
- 1 key: nghỉ ~2,2s giữa lệnh; 429: chờ đúng số giây Google báo, hoặc xoay key nếu có nhiều key.
- Lỗi bắt nhãn PPDH **không hủy** 1-Click; vẫn lưu, cảnh báo.

Hạn mức free tier Gemini (ví dụ 20 request/ngày với một model) vẫn có thể hết nếu GV tạo nhiều lần trong ngày.

---

## 5. Form 2 cột (`demo.docx`)

**Không** dùng cột “Hoạt động của giáo viên | Hoạt động của học sinh”.

Bảng **d) Tổ chức thực hiện**:

| Hoạt động của GV và HS (cột trái) | Nội dung (cột phải) |
|---|---|
| Việc tổ chức lớp: 4 bước trong **một ô** (`+ Bước 1` … `+ Bước 4`), cách dòng `<br>` | **Chỉ kiến thức ghi bảng**: định nghĩa, quy tắc, công thức, chú ý, ví dụ. Dùng `-` / `+`. **Cấm** lặp việc GV/HS |

- Một hàng dữ liệu, không 4 hàng.
- Hoạt động B: mỗi đơn vị kiến thức một bảng như trên.
- Hoạt động E: Hướng dẫn về nhà cực kỳ ngắn gọn, chuẩn mực với đúng 4 nội dung:
  1. Ôn nội dung trọng tâm.
  2. Làm bài tập còn lại chưa làm hoặc chưa chữa trên lớp (kèm gợi ý/hướng dẫn phương pháp ngắn gọn; CẤM TUYỆT ĐỐI giao lại bài đã chữa).
  3. Chuẩn bị bài mới.
  4. Giao một nhiệm vụ tìm tòi/mở rộng nếu thật sự phù hợp.
  *Quy tắc NLS/AI:* Tuyệt đối không tự ý xuất hiện NLS/AI trong Hoạt động E; chỉ thêm khi giáo viên CHỦ ĐỘNG BẬT tích hợp, nhiệm vụ có giá trị hỗ trợ tự học thực chất, không thay thế việc tự học môn học.
- Word: cột ~4000 / 5000 DXA; mỗi dòng trong ô một đoạn; hàng nội dung được phép tách trang.

Danh sách ngoài bảng: ý lớn `- `, ý con `+ ` (giữ nguyên ký tự khi xuất Word).

Header Word: Trường, Tổ, GV, Ngày soạn/dạy, KẾ HOẠCH BÀI DẠY, Tên bài, Môn–Lớp, Bộ sách = “SGK do giáo viên cung cấp”, Thời lượng.

---

## 6. Mục tiêu

**Kiến thức:** YCCĐ TT 32. `getOfficialYccd` lọc Toán 6–9. Môn/khối khác: chỉ YCCĐ in trên SGK; thiếu thì ghi cần đối chiếu TT 32, cấm bịa Bloom.

**Năng lực / phẩm chất — chỉ mô tả một dòng:**

```
- Tự chủ và tự học: …
- Tư duy và lập luận toán học: …
```

Cấm nhãn **Biểu hiện**, **Nhiệm vụ/Sản phẩm**, **Minh chứng**. Cấm ý con `+` trong khối này.

Số lượng: chung 1–2; đặc thù 2–3; phẩm chất 1–2.

**NLS:** nếu bật, 2–3 **miền** TT 02/2025 đã chọn (6 miền catalog, không bịa mã thành phần).

**AI:** nếu bật, 2–3 **mã** QĐ 2422 đã rà: `6.A1.3`, `7.A1.2`, `8.A1.2`, `9.B2.1`. Cấm bịa mã khác.

---

## 7. Catalog PPDH (3 ảnh)

**Phương pháp (15):** PBL, STEM/STEAM, Lớp học đảo ngược, Hợp tác, Học qua trò chơi, Phân hóa, Socratic, Bản đồ tư duy, Trải nghiệm, 5W1H, Think-Pair-Share, Jigsaw, Gallery Walk, KWL, 5E.

**Kỹ thuật theo pha**

- A: Động não, KWL, Câu hỏi kích thích tư duy, Ô chữ/đố vui
- B: TPS, Jigsaw, Gallery Walk, Trạm học tập, Sơ đồ tư duy, Khăn trải bàn
- C: Bài tập phân hóa 3 mức, Peer Assessment, Tranh luận, Case Study, Role-play
- D: Dự án mini, Nhật ký học tập, Exit Ticket, Bài tập mở

**HĐ đặc thù (12):** thảo luận nhóm; thí nghiệm; tình huống; trò chơi khởi động; luyện kỹ năng nhóm; thi đấu; video/hình; peer coaching; trạm xoay vòng; sản phẩm mini; thuyết trình; công nghệ số.

Sau khi có nội dung SGK, nếu GV **không chọn**: tự đề xuất ~2 PPDH, 1 kỹ thuật/pha, 2 HĐ; badge “Đề xuất theo bài”. Đã chọn tay thì không ghi đè. Assert nhãn: khớp gần đúng; kỹ thuật tự đề xuất không làm fail 1-Click.

---

## 8. SOURCE_LOCK

Mọi prompt gắn `PROMPTS.SOURCE_LOCK`: chỉ dùng ảnh/PDF, Tab 0, tên bài/môn/lớp, YCCĐ official, bối cảnh lớp. Cấm bịa định nghĩa, số liệu, đề, đáp án, số trang. Luyện tập/vận dụng: chỉ bài có trong nguồn; thiếu thì `[Không có trong tài liệu đã cung cấp]`.

1-Click / HĐ A–E: cần ảnh hoặc nội dung đã trích. Mục tiêu: ảnh/vision hoặc YCCĐ Toán 6–9.

---

## 9. Lỗ hổng còn lại

1. YCCĐ số hóa mới Toán 6–9; môn/khối khác chưa có CSDL.
2. Parser `yeucau.docx` có chỗ dính ô Word.
3. Không có test tự động cho 1-Click / DOCX.
4. Gemini Vision 4 trang nén vẫn có thể lệch công thức/hình; free tier 20 request/ngày dễ hết.
5. Model mặc định trên UI có thể là Gemini 3.x trong khi 429 log từng gặp `gemini-2.5-flash` — phụ thuộc key/model GV chọn.
6. Bảng Markdown 1 hàng + `<br>`: nếu model vẫn xuất 4 hàng, Word vẫn ra 2 cột nhưng không đúng demo.
7. Draft cũ (PPDH id/label cũ, bảng 4 hàng) không tự chuyển form mới.
8. Tab IV / phụ lục demo chưa làm.

---

## 10. Checklist phản biện

- [ ] Tab mở đầu là Bước 0 SGK; chưa đọc SGK thì NLS/AI không tự tick.
- [ ] Đọc SGK = Gemini, tối đa 4 ảnh nén; 1-Click không đọc lại nếu đã có vision.
- [ ] 429: xoay key hoặc chờ retry; không abort cả 1-Click vì thiếu đúng chuỗi PPDH.
- [ ] Mục tiêu kiến thức: YCCĐ TT 32 / SGK, không Bloom bịa.
- [ ] Năng lực: một dòng mô tả, không Biểu hiện/Minh chứng.
- [ ] NLS 2–3 miền TT 02; AI 2–3 mã QĐ 2422; không mã lạ.
- [ ] Bảng d): 1 hàng, 2 cột; phải = ghi bảng, không lặp GV/HS.
- [ ] Hoạt động E: 4 nội dung súc tích (Ôn trọng tâm, Bài tập còn lại chưa chữa, Chuẩn bị bài mới, Tìm tòi mở rộng); NLS/AI opt-in thực chất.
- [ ] Danh sách `-` / `+` giữ nguyên khi xuất Word.
- [ ] HĐ C/D không invent TN 4 lựa chọn hay bài thực tiễn ngoài nguồn.
