# PLAN: Nâng cấp chất lượng Sư phạm, Phân loại Ví dụ & Chuẩn hóa 5 câu Tự luận trong soanbaigemini.html

Trạng thái: KẾ HOẠCH ĐÃ DUYỆT

## Hiện trạng

1. **Phần VÍ DỤ sơ sài**: Chưa bao quát hết các dạng toán trong ảnh SGK; thiếu phương pháp giải chi tiết từng bước cho từng dạng.
2. **BÀI TẬP TỰ LUẬN NGẮN thiếu số lượng**: Chưa đảm bảo chuẩn tối thiểu 5 câu phân hóa từ Nhận biết đến Vận dụng; validator chưa chặn lỗi thiếu số lượng câu.
3. **Bài tập thiếu tính sư phạm và bám sát kiểm tra đánh giá**: Bài tập sinh ngẫu nhiên, chưa gắn chặt với Mục tiêu / Yêu cầu cần đạt (YCCĐ) và Ma trận kỹ năng của bài học GDPT 2018.

## Phạm vi

1. Nâng cấp Prompt phần VÍ DỤ (`buildRemainingSectionsPrompt`): quét toàn bộ SGK, 3–5 dạng, mỗi dạng có tên / phương pháp / ví dụ mẫu 2 bài lời giải từng bước.
2. Chuẩn hóa 5 câu BÀI TẬP TỰ LUẬN NGẮN phân hóa 4 mức độ; validator lỗi đỏ nếu `< 5`; `buildFormatRepairPrompt` sinh bù đủ 5 câu.
3. Thắt chặt gợi ý sư phạm và bám sát KỸ NĂNG CẦN ĐẠT; số liệu thực tế.
4. Cập nhật `tests/soanbaigemini-plan-smoke.js`.

## Ngoài phạm vi

- Không đổi format cấu trúc JSON đầu ra (`lesson-import-v1`).
- Không đổi giao diện tổng thể của Canvas.

## File dự kiến tác động

- `backupcode viettailieu/soanbaigemini.html`
- `tests/soanbaigemini-plan-smoke.js`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/PLAN.md`

## Các bước thực hiện

1. Cập nhật `buildRemainingSectionsPrompt()` và `CANVAS_BUILTIN_FORMAT_CONTRACT`.
2. Cập nhật `getLessonValidationState()` và `buildFormatRepairPrompt()`.
3. Chạy `node tests/soanbaigemini-plan-smoke.js`.
4. Ghi `docs/handoff/IMPLEMENT.md`.

## Rủi ro

- AI sinh 5 câu tự luận đôi khi trả về câu hỏi yêu cầu chữ thay vì số.
  - *Giải pháp*: Giữ nguyên bộ lọc `isLotrinhEssayNumericAnswer()`.

## Cách kiểm thử

```
node tests/soanbaigemini-plan-smoke.js
```

## Tiêu chí nghiệm thu

1. Phần Ví dụ yêu cầu phân loại đầy đủ dạng toán SGK, có phương pháp giải và lời giải từng bước.
2. Phần Tự luận ngắn luôn khóa đủ 5 câu phân hóa; validator đỏ nếu thiếu.
3. Bài tập bám kỹ năng cần đạt; gợi ý không đối phó.
4. `node tests/soanbaigemini-plan-smoke.js` pass.
