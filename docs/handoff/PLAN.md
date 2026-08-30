# PLAN: Khắc phục hiện tượng nhảy lựa chọn 2 lần và trùng lặp thông báo khi Đề xuất PPDH, Năng lực số & Khung AI

## Hiện trạng
1. **Hiện tượng nhảy lựa chọn 2 lần (Flash of Interim Defaults) & Bắn nhiều Toast chồng lặp**:
   - Khi người dùng bấm nút "Đề xuất PPDH & NLS" (Bước 3 / Subtab 3) hoặc kích hoạt "Khung Năng lực AI" (Bước 4 / Subtab 4), hệ thống hiện đang chạy một quy trình 2 giai đoạn không đồng bộ:
     * **Giai đoạn 1 (Ngay tức thì)**: Hệ thống lập tức gán các giá trị mặc định/heuristic ban đầu (như PBL, STEM/STEAM) và bắn Toast #1 màu xanh lam (*"Đã đề xuất PPDH/kỹ thuật theo nội dung SGK..."*), làm người dùng nhìn thấy các ô checkbox được tick ngay lập tức.
     * **Giai đoạn 2 (Sau 2–4 giây)**: Hàm AI `requestStructuredIntegrationCandidates` chạy ngầm gọi Gemini trả về kết quả phân tích sâu. Khi nhận được phản hồi, hệ thống tự động ghi đè lại các checkbox đã chọn và bắn tiếp Toast #2 màu xanh lá (*"Đã đề xuất PPDH, kỹ thuật dạy học 4 pha và 2–3 mục Năng lực số (NLS)..."*).
   - Hiện tượng tương tự cũng xảy ra tại **Khung Năng lực AI (QĐ 2422)** khi bật toggle AI: hệ thống tick ngay các mục fallback theo lớp rồi sau đó mới ghi đè bằng kết quả Gemini.
   - **Hậu quả**:
     * Người dùng thấy Toast #1 và các checkbox đã tick nên lầm tưởng hệ thống đã hoàn thành đề xuất, do đó bỏ qua hoặc chuyển sang bước khác để soạn bài.
     * Vài giây sau, hệ thống âm thầm ghi đè lại các lựa chọn khác hoặc nếu người dùng đã tự tay chỉnh sửa thì bị mất/thay đổi lựa chọn, gây hoang mang, cảm giác giật lag và sai lệch bối cảnh dạy học khi tạo giáo án.

## Phạm vi
1. **Đồng bộ hóa luồng Đề xuất Bước 3 (PPDH & NLS) và Bước 4 (Năng lực AI) (`js/khbd-app.js`)**:
   - **Trạng thái Chờ xử lý rõ ràng (Loading State)**:
     * Khi người dùng bấm nút "Đề xuất PPDH & NLS" hoặc bật đề xuất: Nút bấm hiển thị trạng thái đang xử lý (ví dụ: `⏳ Đang phân tích SGK & đề xuất...`), vô hiệu hóa nút bấm tạm thời để tránh người dùng bấm liên tục nhiều lần.
     * Có thể hiển thị chỉ báo tải nhẹ / skeleton trên panel danh mục để người dùng biết hệ thống đang phân tích.
   - **Tắt toàn bộ Toast trung gian & Chỉ cập nhật giao diện một lần duy nhất (Atomic UI Update)**:
     * Chạy các hàm heuristic và API AI ở chế độ im lặng (`silent: true`).
     * Sau khi AI phân tích xong (hoặc fallback nếu offline/timeout): Cập nhật trạng thái và render lại các checkbox trên giao diện **MỘT LẦN DUY NHẤT**.
     * Chỉ hiển thị **DUY NHẤT MỘT THÔNG BÁO HOÀN TẤT** (Toast xanh lá): *"✅ Đã đề xuất PPDH, kỹ thuật dạy học 4 pha và Năng lực số (NLS) bám sát nội dung SGK."* (loại bỏ hoàn toàn Toast #1 trung gian).
   - **Đồng bộ hóa cho Khung Năng lực AI (QĐ 2422)**:
     * Khi người dùng bật toggle AI hoặc bấm "Đề xuất Năng lực AI": Hiển thị trạng thái đang phân tích, chờ AI phản hồi rồi mới tick chọn và hiển thị 1 thông báo duy nhất.
   - **Bảo toàn lựa chọn thủ công của giáo viên**:
     * Nếu người dùng đã tự tay tick chọn hoặc bỏ chọn một mục (không còn cờ `autoSuggested`), hệ thống tôn trọng và không tự ý ghi đè/xóa bỏ mục đó trừ khi người dùng chủ động bấm nút "Đề xuất lại".

2. **Xây dựng bộ kiểm thử tự động (`tests/khbd-recommendation-flow-smoke.js`)**:
   - Viết bài kiểm thử tự động kiểm tra luồng đề xuất:
     * Xác nhận nút bấm có trạng thái loading trong khi xử lý.
     * Xác nhận không còn tình trạng bắn 2 thông báo toast nối tiếp nhau.
     * Xác nhận giao diện chỉ cập nhật 1 lần với kết quả cuối cùng hoàn chỉnh.

## Ngoài phạm vi
- Không thay đổi danh mục chuẩn PPDH, Thông tư 02 (NLS) hay Quyết định 2422 (Năng lực AI).
- Không thay đổi thuật toán phân tích sư phạm trong `khbd-pedagogy-catalog.js`.

## File dự kiến tác động
- `js/khbd-app.js`
- `tests/khbd-recommendation-flow-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Các bước thực hiện
1. **Bước 1: Tinh chỉnh `triggerStep3PedagogyAndDigitalRecommendations` trong `js/khbd-app.js`**:
   - Thêm cơ chế quản lý trạng thái loading trên nút bấm (`btnStep3Recommend`, `btnStep3PedagogyDigital`, `btnSuggestPedagogyStandards`).
   - Chạy `ensurePedagogyFromLesson({ force: true, silent: true })` và `requestStructuredIntegrationCandidates("digital", { silent: true })`.
   - Cập nhật DOM và hiển thị duy nhất 1 toast thông báo thành công khi toàn bộ quá trình hoàn tất.
2. **Bước 2: Tinh chỉnh luồng kích hoạt Năng lực AI trong `js/khbd-app.js`**:
   - Khi bật toggle AI hoặc bấm đề xuất AI, chạy với `silent: true`, cập nhật UI 1 lần và bắn 1 toast duy nhất.
3. **Bước 3: Viết bài test tự động `tests/khbd-recommendation-flow-smoke.js`**:
   - Kiểm tra luồng đề xuất Bước 3 và Bước 4 không bắn toast trùng lặp và cập nhật trạng thái an toàn.
4. **Bước 4: Chạy toàn bộ test suites**:
   - Xác nhận tất cả bài kiểm thử đều PASS 100%.

## Rủi ro
- **Rủi ro**: Nếu kết nối mạng chậm hoặc API Gemini bị lỗi, nút bấm có thể bị treo ở trạng thái loading.
  - **Khắc phục**: Đặt khối `try...finally` đảm bảo luôn khôi phục lại trạng thái bình thường của nút bấm và fallback về danh mục cục bộ trong mọi trường hợp.

## Cách kiểm thử
1. **Kiểm thử tự động qua Node.js**:
   - Chạy `node tests/khbd-recommendation-flow-smoke.js`: Kiểm tra hàm đề xuất thực hiện cập nhật atomic và chỉ phát 1 thông báo hoàn tất.
2. **Kiểm thử thủ công trên giao diện `soankhbd.html`**:
   - Đọc nội dung SGK ở Bước 1.
   - Bấm vào mục **3. PPDH, Năng lực số & Môn** (hoặc bấm nút "⚡ Đề xuất PPDH & NLS"):
     * Nút bấm hiện trạng thái `⏳ Đang phân tích...`.
     * Khi hoàn tất, các checkbox hiện ra ngay kết quả chuẩn xác cuối cùng và chỉ xuất hiện duy nhất 1 thông báo hoàn tất màu xanh lá.
     * Hoàn toàn không còn hiện tượng hiển thị kết quả mặc định trước rồi vài giây sau tự nhảy đổi sang kết quả khác.
   - Chuyển sang mục **4. Năng lực AI (QĐ 2422)** và bật toggle AI: Kết quả được áp dụng mượt mà, đồng nhất 1 lần.

## Tiêu chí nghiệm thu
1. Quá trình đề xuất PPDH, NLS (Bước 3) và Năng lực AI (Bước 4) diễn ra mượt mà, có trạng thái loading rõ ràng trên nút bấm.
2. Loại bỏ triệt để hiện tượng "chớp" giao diện (hiện lựa chọn tạm thời rồi vài giây sau tự động nhảy đổi sang lựa chọn khác).
3. Chỉ xuất hiện duy nhất 1 thông báo Toast xác nhận hoàn tất, không bị bắn 2–3 thông báo chồng lặp.
4. Toàn bộ các bài kiểm thử liên quan đều PASS 100%.

