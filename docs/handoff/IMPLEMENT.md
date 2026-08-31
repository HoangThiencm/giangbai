# IMPLEMENT: Hai giai đoạn PPCT → Phụ lục

## Đã triển khai

- Tách rõ hai giai đoạn: lúc nạp PPCT, ứng dụng chỉ đọc văn bản và gọi recognizer trả JSON `{ppct:[{lesson,periods,tietCT,week,devices,location,isHeader}]}`; không gọi prompt sinh YCCĐ, NLS hay AI ở thời điểm tải tệp. Bảng Mục 3 được làm mới ngay sau khi hoàn tất nhận diện.
- Recognizer dùng Gemini hiện có trước, rồi tự chuyển sang Mistral nếu Gemini không phản hồi. Nếu không có key, API lỗi hoặc JSON không có dòng PPCT hợp lệ, ứng dụng giữ parser DOCX/PDF/XLSX hiện có, hiển thị cảnh báo cụ thể và vẫn cho giáo viên sửa/tick PPCT bình thường.
- Nút Sinh phụ lục là điểm bắt đầu duy nhất của Giai đoạn 2. Prompt của PL1 mới yêu cầu AI bù `Yêu cầu cần đạt`; prompt PL3 vẫn nhận PPCT nguồn và chỉ nối một cột tích hợp. Việc lọc AI theo đúng từng tiết đã tick và NLS tự động vẫn chạy lúc chuẩn hoá kết quả sinh.
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

- `node tests/xaydungphuluc-smoke.js` — PASS (bao gồm recognizer Giai đoạn 1, gọi Gemini, fallback parser, tách prompt nhận diện khỏi prompt sinh phụ lục, 8 cột table view và metadata nguồn/gộp header).
- `node tests/xaydungphuluc-integration-smoke.js` — PASS.
- `git diff --check` — PASS.
