# IMPLEMENT: Bóc tách độc lập bảng PPCT, loại header hành chính, định dạng 7 cột cố định

## Phạm vi đã triển khai

- `extractDocxTables` tách từng `<table>` (mammoth HTML, regex fallback). `ingestSourceTables` phân loại độc lập:
  - Bảng hành chính (`UBND`, `CỘNG HÒA XÃ HỘI`, `TỔ TRƯỞNG`, `HIỆU TRƯỞNG`): điền trường/tổ, không đưa vào PPCT.
  - Bảng PPCT (header có `Bài học` / `Tên bài` / `Tiết CT` / `Tuần`): `sourcePpctRows`.
  - Bảng thiết bị (`Thiết bị dạy học`) → `sourceDevices`; phòng bộ môn (`Tên phòng`) → `sourceRooms`; kiểm tra (`Bài kiểm tra`) → `sourceAssessments`.
- Dòng bài học sạch (`Bài 1. Tập hợp`, …); `isHeader` cho học kỳ/chương; không nhồi quốc hiệu/tên trường vào cột Bài học.
- Preview `table.ppct-table`: `table-layout: fixed; width: 100%; word-break: break-word` và colgroup 30/7/8/7/12/11/25. Dòng chương `colspan` 7 cột.
- AI chỉ điền cột `integration`; `preserveSourceSchedule` lọc dòng hành chính nếu còn sót.
- Không sửa `PLAN.md`, `VERIFY.md` hoặc `.lock`; không commit/push.

## File thay đổi

- `xaydungphuluc.html`: parser theo từng bảng, lọc hành chính, CSS bảng 7 cột cố định, nạp thiết bị/phòng/KTĐG nguồn vào phụ lục 1.
- `tests/xaydungphuluc-smoke.js`: parse trực tiếp `GIAO AN/XAYDUNGPHULUC/Phụ lục 1 - Lớp 6 - Toán.docx`; cấm rò `TRƯỜNG THCS` / `CỘNG HÒA XÃ HỘI`; nhận `Bài 1. Tập hợp`, `Bài 2. Cách ghi số tự nhiên`.
- `docs/handoff/IMPLEMENT.md`: báo cáo triển khai này.

## Kiểm thử đã chạy

- `node tests/xaydungphuluc-smoke.js` — PASS (47 dòng PPCT từ file mẫu, 0 dòng hành chính lẫn vào).
- `node tests/xaydungphuluc-integration-smoke.js` — PASS.

Không có browser MCP trong phiên này nên chưa tải file lên giao diện và xuất Word bằng tay.

## Vấn đề còn lại

- Cần `/verify` trên trình duyệt: tải `Phụ lục 1 - Lớp 6 - Toán.docx`, sinh phụ lục, đối chiếu 7 cột và tên bài sạch, rồi mở file Word đã xuất.
