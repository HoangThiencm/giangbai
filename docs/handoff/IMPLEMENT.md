# IMPLEMENT: CV 7991 17 câu (12 MC + 1 Đ/S 4 ý + 4 TLN) và đồng bộ Tạo bài tập ↔ Thi trực tuyến

Đã triển khai đúng `docs/handoff/PLAN.md`.

## Module 1 — `taobaitap.html`
- Nhãn `synthForm`: `⭐ Chuẩn Công văn 7991 (17 câu - 10đ: 12 TN + 1 Đ/S 4 ý + 4 TL ngắn)`.
- Chọn `cv7991` gán cứng `synthCount = 17`, khóa ô số câu.
- Prompt `generateSynthesizedFromSource` / `generateContent`: Phần II đúng 1 câu TF 4 mệnh đề `a,b,c,d` + `correct_answers`; Phần III `correctAnswer` chỉ số (`25`, `3.5`, `-4`, `1/2`).
- `normalizeQuizItems`: TF 4 ý đồng bộ `options` / `subItems` / `correct_answers`; TLN lọc `x =`, đơn vị, dấu phẩy thập phân.
- ContentEditor: 4 ô a–d kèm nút `[ĐÚNG]`/`[SAI]`. Step 2: 4 dòng mệnh đề + ô đáp án số nổi bật.

## Module 2 — Xuất Word & Text
- `exportWordCV7991` / `exportTextCV7991` dùng `buildCv7991ExportHtml` / `buildCv7991ExportText`.
- Phần I: mỗi phương án một dòng `<p class="option">` (tránh bảng 2 cột / tab).
- Phần II: đủ 4 ý `a) … [Đúng/Sai]`; thang 1 câu = 2.0đ (0.2 / 0.5 / 1.0 / 2.0).
- Phần III: `Đáp án: <số>`; thí sinh chỉ điền số.
- Cuối file: khối `BẢNG ĐÁP ÁN` (12 MC + `13. a.Đúng b.Sai …` + 4 số).

## Module 3 — `thitructuyen.html`
- `normalizeImportedQuizText`: tách `\t` và ≥2 khoảng trắng trước `A–D` / `a–d` thành dòng mới — không rơi phương án B, D.
- `parseLatexWordQuiz`: TF 4 ý + `[Đúng]/[Sai]` / answerKey; TLN chuẩn hóa số; 17 câu (12 MC + 1 TF + 4 SA) gán `exam_format = "cv7991"`.
- `matchImportedAnswerSection` ưu tiên `BẢNG ĐÁP ÁN` (không nhầm `Đáp án:` inline).

## Module 4 — Backend
Không đổi. `backend/thitructuyen.py` và `api/exam.php` đã scale đúng khi 1 câu Đ/S (`tf_scale = 2.0`).

## Module 5 — Kiểm thử
- `node tests/cv7991-taobaitap-thitructuyen-sync-smoke.js` — PASS
- `node tests/thitructuyen-cv7991-answerkey-smoke.js` — PASS (định dạng 18 câu cũ vẫn chạy)
- `node tests/taobaitap-plan-smoke.js` — PASS

Không thêm chức năng ngoài plan. Cần `/verify` trên Antigravity: tạo đề CV 7991 17 câu → xuất Word/Text → nạp Thi trực tuyến đủ 12 MC + 1 TF 4 ý + 4 TLN số.
