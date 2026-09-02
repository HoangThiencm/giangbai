# IMPLEMENT: Khóa phạm vi chương khi khớp YCCĐ

## Phạm vi đã triển khai

- Mở rộng nhận diện bài luyện tập/ôn tập bao gồm bài tập, bài tập cuối chương, cuối chương, thực hành và hoạt động trải nghiệm.
- Bổ sung bộ suy luận chương Toán 6 và giới hạn ứng viên YCCĐ theo sáu dải bài học của từng chương.
- Với bài ôn tập hoặc bài tập cuối chương, sinh YCCĐ tổng hợp đúng mạch chương; riêng Chương I dùng YCCĐ về tập hợp số tự nhiên, phép tính, chia hết, ước và bội.
- YCCĐ tổng hợp chỉ dùng cho ôn tập hoặc bài tập cuối chương. Với `Luyện tập chung`, hệ thống vẫn khóa trong chương nhưng ưu tiên bài/chủ đề liền trước; ví dụ sau Bài 5 chỉ trả phạm vi phép tính, không lẫn chia hết, ước hoặc bội của các bài sau.
- Fallback của Phụ lục 1 dùng cùng phân loại trên: chỉ ôn tập/bài tập cuối chương mới nhận tổng hợp Chương I; `Luyện tập chung` sau Bài 4–7 nhận nội dung phép tính khi kết quả AI bị loại.
- Phụ lục 1 giữ ngữ cảnh của mọi dòng tiêu đề chương và từ chối kết quả YCCĐ lệch mạch; fallback Chương I không thể trả về điểm, đường thẳng, góc hoặc phân số.
- Bổ sung smoke tests cho tra cứu YCCĐ và bảng Phụ lục 1 của `Bài tập cuối chương I`/`Luyện tập chung`, xác nhận không rò rỉ Hình học hoặc Phân số.

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

- Chưa thực hiện kiểm thử thủ công với PPCT thực tế có biến thể tiêu đề chương.
- Chưa commit hoặc push theo yêu cầu.
