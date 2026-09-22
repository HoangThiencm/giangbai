# IMPLEMENT: Hai hướng xuất Word để tải lên OLM.vn

Đã triển khai đúng `docs/handoff/PLAN.md`.

## File đã thay đổi

- `taobaitap.html`
  - Giữ `exportWordOLM` cho luồng Đề thi thông minh, xuất `De_Thi_OLM.docx`.
  - Bổ sung `exportOlmPdfPair` cho luồng Đề thi PDF: xuất riêng `De_Bai_OLM_PDF.docx` (không có đáp án/lời giải) và `Huong_Dan_Giai_OLM_PDF.docx` (đáp án tổng hợp cùng lời giải chi tiết).
  - Bộ đôi hỗ trợ câu nhiều lựa chọn, đúng/sai, trả lời ngắn/điền khuyết, cấu trúc CV 7991 và bài tự luận.
  - Thêm nút `Bộ đôi OLM (Đề & Giải PDF)` cạnh `Xuất Word (OLM)`.
- `tests/taobaitap-olm-export-smoke.js`
  - Kiểm tra hồi quy cả hai hàm xuất, ba tên tệp DOCX và hai nút giao diện OLM.

## Kiểm tra

- `node tests/taobaitap-olm-export-smoke.js`: PASS.
- `git diff --check -- taobaitap.html tests/taobaitap-olm-export-smoke.js docs/handoff/IMPLEMENT.md`: PASS.
