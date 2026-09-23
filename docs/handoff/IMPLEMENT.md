# IMPLEMENT: Linh hoạt số câu Công văn 7991

## Cấu hình đề

- `taobaitap.html`: thêm `cv7991Config` mặc định `{ part1: 12, part2: 1, part3: 4, preset: 'standard-17' }`.
- Khi hình thức là Chuẩn Công văn 7991, ô số câu không còn bị khóa. Card hiện mẫu đề 15 phút (6 TN + 1 Đ/S + 3 TL ngắn), 45 phút (12 + 1 + 4), 60–90 phút (16 + 2 + 4) và Tùy chỉnh với 3 ô Phần I / II / III (0–40). Bấm "Chỉnh sửa số câu từng phần" chuyển sang tùy chỉnh. Tổng câu đồng bộ vào `synthCount`.
- Mẫu 45 phút vẫn gửi đúng 17 câu. Các mẫu khác dùng tổng `part1 + part2 + part3`. Nếu cả ba phần bằng 0 thì không gọi AI.

## Prompt và điểm

- `generateSynthesizedFromSource` dựng prompt theo `countPart1`, `countPart2`, `countPart3`, kể cả phần 0 câu (không sinh loại đó).
- `allocateCv7991PartScores` chia 10.0 điểm theo trọng số 1 / 4 / 1. Đề 12 + 1 + 4 vẫn ra 6.0 / 2.0 / 2.0 và 0.5 điểm mỗi câu TN hoặc TL ngắn. Phần cuối nhận phần lẻ để tổng đúng 10.0.
- Sau `normalizeQuizItems`, đề CV 7991 bị cắt đúng số câu từng phần. Thiếu câu thì báo lỗi và không ghi đè bài đang soạn.

## Xuất Word / Text

- `buildCv7991ExportHtml` và `buildCv7991ExportText` ghi điểm từng phần theo số câu thực tế. Phần không có câu thì không in. Đề chuẩn vẫn ghi 45 phút, 6.0 / 2.0 / 2.0 và thang ý Đúng/Sai cũ. Mẫu 15 phút ghi 15 phút, mẫu 22 câu ghi 90 phút, cấu hình khác ghi "theo ma trận đề".

## Kiểm thử

- PASS: `node tests/taobaitap-plan-smoke.js`
- PASS: `node tests/cv7991-taobaitap-thitructuyen-sync-smoke.js` (đề mẫu 12 + 1 + 4 vẫn xuất 6.0 / 2.0 / 2.0 và parse đủ 17 câu)
- Chưa bấm trình duyệt: không có công cụ duyệt trong phiên này.

## Việc tiếp

Antigravity IDE, chat mới: `/verify`
