# IMPLEMENT: Phân rã YCCĐ Toán 6 và ngữ cảnh chương

## Phạm vi đã triển khai

- Mở rộng `KHBD_LESSON_YCCD_OVERRIDES` cho đầy đủ Bài 1–43 Toán 6. Mỗi bài có YCCĐ trọng tâm riêng, không còn dùng chung toàn bộ YCCĐ của chủ đề.
- `findOfficialYccdRows` nhận thêm `chapterTopic`/`domain` và ưu tiên ngữ cảnh này cho bài Luyện tập, Ôn tập.
- Phụ lục 1 theo dõi tiêu đề chương trong PPCT nguồn; YCCĐ của bài ôn tập/luyện tập được kiểm tra theo đúng chương hiện hành, thay vì chỉ dựa vào bài trước đó.
- `formatOutcomeLines` nhận mảng hoặc chuỗi; tách dấu phẩy/chấm phẩy chỉ khi trước một động từ YCCĐ và chuẩn hóa từng ý thành dòng `- `.
- Smoke test đã bao quát định dạng bullet, toàn bộ 43 bài Toán 6, sự khác nhau giữa các bài liền kề và bài ôn tập có ngữ cảnh chương.

## File đã sửa

- `js/khbd-yccd.js`
- `xaydungphuluc.html`
- `tests/xaydungphuluc-smoke.js`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/.lock`

## Kiểm thử đã chạy

- `node tests/xaydungphuluc-smoke.js` — PASS
- `node tests/xaydungphuluc-integration-smoke.js` — PASS
- `git diff --check` — PASS

## Vấn đề còn lại

- Chưa kiểm tra thủ công bản xem trước trên trình duyệt hoặc tài liệu Word xuất ra.
- Chưa commit hoặc push theo yêu cầu.
