# IMPLEMENT: Bảo mật key, nạp key tức thì và tiến trình PPCT

## Đã triển khai

- Loại bỏ hoàn toàn cơ chế đọc/ghi API key từ `localStorage` và không dùng `sessionStorage`. Gemini/Mistral key chỉ tồn tại trong RAM (`apiKeys`, `mistralKeys`) sau khi đồng bộ với `api/user_gemini_keys.php`; lưu từ modal chỉ POST lên máy chủ rồi cập nhật RAM khi thành công.
- Khi khởi động trang, ứng dụng dọn đúng các key API cũ (bao gồm biến thể `khbd_user_*_keys_*`) nhưng giữ nguyên nhận diện tài khoản, giao diện và tuỳ chọn khác. Badge key được cập nhật từ kết quả nạp máy chủ.
- Thêm `syncUserKeysPromise` cho eager load ngay lúc vào trang và `ensureKeysLoaded()` dùng chung promise đó. Luồng nhận diện PPCT luôn chờ key load hoàn tất trước khi gửi ngữ cảnh tới Gemini/Mistral, không tạo GET trùng lặp.
- Gắn tiến trình chi tiết, chỉ cho tải PPCT: 15% đọc tệp, 40% gửi ngữ cảnh, 75% AI phân tích, 90% dựng bảng 8 cột, 100% hoàn tất và tự ẩn sau 1,5 giây. Nhánh parser dự phòng và lỗi đọc tệp cũng luôn đóng tiến trình; luồng SGK không giả mạo tiến trình nhận diện PPCT.

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

- `node tests/xaydungphuluc-smoke.js` — PASS (bao gồm recognizer Giai đoạn 1, fallback parser, không persist key, dọn key legacy có chọn lọc, eager-load/await dùng chung promise, các mốc tiến trình PPCT, 8 cột table view và metadata nguồn/gộp header).
- `node tests/xaydungphuluc-integration-smoke.js` — PASS.
- `git diff --check` — PASS.

## Cập nhật triển khai: chọn model Gemini và nhận diện PPCT có cảnh báo

- Thêm bộ chọn `#selectModel` ở header với Gemini 3.7 Flash làm mặc định và đầy đủ các model trong kế hoạch. Chỉ ID model `khbd_gemini_model` được lưu trong `localStorage`; API key vẫn chỉ được đồng bộ với máy chủ và giữ trong RAM.
- `callGemini()` dùng model được chọn, gửi `thinkingConfig.thinkingBudget: 0`, có timeout, xoay vòng key khi gặp 429/403, rồi tự thử proxy `api/khbd_gemini.php` khi direct request lỗi mạng/CORS. Phản hồi proxy bọc `{ok,status,body}` được giải mã trước khi đọc Gemini body.
- Khi Gemini 3.7 Flash gặp lỗi tạm thời 5xx/quá tải/không khả dụng/timeout, hoặc 429 ở key cuối, request tự chạy lại bằng Gemini 2.5 Flash. Đây chỉ là fallback cho request đó, không đổi model đã lưu; hủy tác vụ không kích hoạt fallback.
- Trước khi nhận diện PPCT, ứng dụng nạp key và chặn rõ ràng nếu tổng Gemini/Mistral key bằng 0: log, toast, `#fileList`, modal API key và trạng thái tiến trình lỗi. Tệp rỗng/PDF scan, lỗi AI (trước parser dự phòng), và trường hợp cuối cùng không có dòng PPCT đều có log/toast/file list/status rõ ràng. Thành công hiển thị số dòng đã nhận diện.
- Mở rộng smoke test cho lưu/khôi phục model, payload thinking budget, direct request, proxy fallback và fallback 3.7 → 2.5 mà không đổi lựa chọn lưu.

## Kiểm thử cập nhật

- `node tests/xaydungphuluc-smoke.js` — PASS.
- Kiểm tra cú pháp JavaScript inline bằng Node VM — PASS.
- `git diff --check` — PASS.
