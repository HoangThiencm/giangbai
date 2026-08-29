# PLAN: Tối ưu Tốc độ Nhận diện PPCT bằng Mistral OCR & Chuẩn hóa Khung Năng lực AI trong soankhbd.html

Trạng thái: KẾ HOẠCH ĐÃ DUYỆT

## Hiện trạng

1. **Đọc PPCT rất chậm**: handleGeneratePpctAnalysis gửi toàn bộ ảnh/PDF nặng sang Gemini Multimodal thay vì dùng Mistral OCR đã có sẵn.
2. **Năng lực AI bị tự động chọn khi chưa tick & chọn quá 3 mục**.

## Phạm vi

1. handleGeneratePpctAnalysis gọi extractPpctOcrText (Mistral), parsePpctLessonDetails; Gemini chỉ khi hết key/lỗi.
2. Khi chưa tick AI: dọn sạch mã AI; không tự bật toggle. Khi tick: khóa 2–3 mục, không vượt 3.
3. Cập nhật smoke tests.

## Ngoài phạm vi

- Không thay đổi cấu trúc bảng mã chuẩn QĐ 2422.
- Không thay đổi format xuất Word.

## File dự kiến tác động

- `js/khbd-app.js`
- `js/khbd-standards.js`
- `tests/khbd-mistral-ocr-smoke.js`
- `tests/khbd-structured-candidates-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Tiêu chí nghiệm thu

1. PPCT ưu tiên Mistral OCR.
2. Chưa tick AI: không chọn mã AI.
3. Tick AI: 2–3 mục, không quá 3.
4. Smoke tests pass.
