# IMPLEMENT: Sửa định dạng bullet và báo cáo thẩm định sư phạm

## Phạm vi đã triển khai

- Tách hiển thị văn bản thông thường và Yêu cầu cần đạt: `htmlMultiline` không tự thêm dấu `- `; `outcomeHtml` chỉ định dạng bullet cho cột Yêu cầu cần đạt; mã NLS/AI được giữ nguyên.
- Xuất DOCX dùng `cell` cho văn bản thông thường, `outcomeCell` cho YCCĐ và `integrationCell` sạch cho mã NLS/AI. Tiêu đề và các cột thường không còn bị gắn dấu gạch đầu dòng.
- Thêm thẻ thẩm định và modal báo cáo, đối chiếu sáu tiêu chí: thời lượng, YCCĐ, NLS, AI, thiết bị/địa điểm, đánh giá định kỳ; kèm căn cứ CV 5512, TT 32, CV 3456/TT 02, QĐ 2422, TT 38 và TT 14.
- Kết luận được tính từ dữ liệu thực tế. Chỉ hiện `ĐẠT CHUẨN 100%` khi toàn bộ 6/6 tiêu chí đạt; dữ liệu thiếu sẽ hiển thị yêu cầu hoàn thiện, không cam kết đạt chuẩn vô điều kiện.
- Bổ sung smoke assertions cho định dạng không-bullet của ô thường, bullet của YCCĐ, các hàm/modal thẩm định và trường hợp dữ liệu thiếu không đạt chuẩn.

## File đã sửa

- `xaydungphuluc.html`
- `tests/xaydungphuluc-smoke.js`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/.lock`

## Kiểm thử đã chạy

- `node tests/xaydungphuluc-smoke.js` — PASS
- `node tests/xaydungphuluc-integration-smoke.js` — PASS
- `git diff --check` — PASS

## Vấn đề còn lại

- Chưa kiểm tra thủ công tệp DOCX đã xuất bằng Microsoft Word.
- Chưa commit hoặc push theo yêu cầu.
