# IMPLEMENT: Bảng PPCT và chọn tiết AI cho Phụ lục 1/3

## Đã triển khai

- Thay toàn bộ danh sách thẻ ở Mục 3 bằng bảng cuộn ngang 8 cột: STT, Bài học, Số tiết, Tiết CT, Tuần, Thiết bị dạy học, Địa điểm và Tích hợp AI. Dòng tiêu đề PPCT nguồn được gộp đủ `colspan="8"`, in đậm/căn giữa theo kiểu bảng PPCT.
- Nạp PPCT DOCX/XLSX/PDF, bảo toàn bảng nguồn và hiển thị từng bài với Số tiết có thể sửa, metadata Tiết CT/Tuần/Thiết bị/Địa điểm và checkbox từng tiết AI hoặc chọn cả bài.
- Giới hạn, gợi ý và bỏ chọn AI hoạt động theo tối đa 12 tiết; khi giảm số tiết, checkbox thừa tự bị loại và PL1/PL3 được làm mới.
- Nhận diện số tiết từ số thường, ngoặc, `/tuần`, khoảng, danh sách `1, 2` và số đếm tiếng Việt; khi Số tiết trống, suy ra từ Tiết CT.
- Danh sách mẫu Toán 6 dùng đúng 47 bài học và số tiết không đồng đều từ `GIAO AN/XAYDUNGPHULUC/Phụ lục 1 - Lớp 6 - Toán.docx`, gồm Bài 1–4: 1 tiết, Bài 5: 2 tiết và ôn tập cuối Chương II: 5 tiết.
- Khi chưa tải PPCT, bảng Mục 3 hiển thị ngay danh sách mẫu tương ứng; ID dòng vẫn đồng nhất với ID chọn tiết AI.
- PL1 lấy Bài học/Số tiết từ PPCT và sinh Yêu cầu cần đạt; PL3 giữ nguyên bảng nguồn và chỉ nối một cột Mã NLS & AI. Preview/DOCX tách NLS xanh `0070C0`, AI tím `7030A0`.

## File thay đổi

- `xaydungphuluc.html`
- `tests/xaydungphuluc-smoke.js`
- `docs/handoff/IMPLEMENT.md`

Không sửa `docs/handoff/PLAN.md`, `docs/handoff/VERIFY.md` hoặc `docs/handoff/.lock` trong lần triển khai này.

## Kiểm thử

- `node tests/xaydungphuluc-smoke.js` — PASS (bao gồm 8 cột table view, metadata nguồn/gộp header và phân bổ Toán 6 không chia đều).
- `node tests/xaydungphuluc-integration-smoke.js` — PASS.
- `git diff --check` — PASS.
