# IMPLEMENT: RAG sư phạm cho YCCĐ Phụ lục 1

## Phạm vi đã triển khai

- Prompt Phụ lục 1 nay truyền toàn bộ danh sách bài học PPCT theo thứ tự, ngữ cảnh CTGDPT 2018/SGK theo từng bài, và yêu cầu AI trả đúng 1–3 YCCĐ cho từng bài theo ghép 1-kèm-1.
- `appendixOneTable` ghép kết quả AI với PPCT bằng tên chuẩn hóa hoặc số bài, chỉ dùng vị trí tương ứng khi không ghép được tên; mỗi kết quả AI chỉ được sử dụng một lần.
- `cleanAppendixOutcome` giữ kết quả AI hợp lệ, đúng ngữ nghĩa bài học. Chuỗi dự phòng khi AI thiếu hoặc sai là: CSDL CTGDPT 2018 → ngữ cảnh SGK → `generatePedagogicalOutcome`.
- Bộ ghép tên bài không còn danh sách từ khóa Toán cố định; nó dùng số bài, tên chuẩn hóa và từ khóa tổng quát, nên áp dụng cho các môn khác.
- Chuẩn hóa cột NLS/AI vẫn bảo toàn khả năng nhận mảng/object mà không hiển thị `[object Object]` trong preview hoặc Word.
- Tách Mục 4 thành ba ô `Số lớp`, `Số học sinh`, `Số giáo viên`; lưu/khôi phục bản nháp tương thích cả định dạng cũ và đưa đủ ba giá trị vào Word.
- Giữ bố cục DOCX A4 ngang với tỉ lệ cột riêng, `tableHeader: true` và `cantSplit: true`.

## File đã sửa

- `xaydungphuluc.html`
- `js/khbd-yccd.js`
- `tests/xaydungphuluc-smoke.js`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/.lock`

## Kiểm thử đã chạy

- `node tests/xaydungphuluc-smoke.js` — PASS
- `node tests/xaydungphuluc-integration-smoke.js` — PASS
- `git diff --check` — PASS

## Vấn đề còn lại

- Chưa thực hiện kiểm tra thủ công trên trình duyệt và Microsoft Word.
- Chưa commit hoặc push theo yêu cầu.
