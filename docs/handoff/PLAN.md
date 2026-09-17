# PLAN: Bổ sung 2 chế độ soạn "Soạn chi tiết" & "Soạn rút gọn" cho Canvas Soạn KHBD

## Hiện trạng
1. **Dung lượng và cấu trúc hiện tại của `canvas_soankhbd.html`**:
   - Quy trình 1-Click tự động chạy 8 bước tuần tự: I. Mục tiêu -> II. Thiết bị -> III.A Khởi động -> III.B Hình thành kiến thức (với đầy đủ các tiểu mục SGK) -> III.C Luyện tập -> III.D Vận dụng -> III.E Hồ sơ học tập & Đánh giá (Phiếu học tập in sẵn, Rubric) -> F. Hình minh họa SGK SVG.
   - Hợp đồng sư phạm hiện tại (`ACTIVITY_TABLE_CONTRACT` trong `js/khbd-prompts.js`) đặt mục tiêu độ dài 8–10 trang Word A4 (hoặc dài hơn nếu bài nhiều tiểu mục), yêu cầu kịch bản chi tiết 4 bước với câu thoại trực tiếp của GV trong ngoặc kép `"..."`, dự kiến cụ thể lỗi sai/ngộ nhận của HS, can thiệp phân hóa, bảng chốt kiến thức đầy đủ kèm ví dụ mẫu chi tiết.
2. **Vấn đề phản ánh từ người dùng**:
   - Giáo viên phản ánh giáo án sinh ra quá dài (8–12 trang), tốn thời gian sinh và quá tải khi in ấn phục vụ dạy học đại trà hàng ngày (tuần 15–20 tiết).
   - Tuy nhiên, bản soạn chi tiết vẫn rất cần thiết và chuẩn mực cho các tình huống: thanh tra chuyên môn, thao giảng dự giờ, thi Giáo viên dạy giỏi, hồ sơ chuyên đề.
3. **Đánh giá đề xuất của tác giả**:
   - Đề xuất tạo 2 lựa chọn ("1/ Soạn chi tiết (giữ nguyên, đừng đụng tới)" và "2/ Soạn rút gọn: vẫn giữ nguyên logic tích hợp nhưng rút gọn lại các hoạt động tối thiểu, dung lượng khoảng 4–6 trang A4") là **hoàn toàn chính xác, đúng nhu cầu thực tế sư phạm và an toàn kỹ thuật**:
     + Bảo toàn 100% logic đã ổn định của chế độ "Soạn chi tiết".
     + Bổ sung chế độ "Soạn rút gọn" tinh giản (khoảng 4–6 trang Word A4, tương đương 2–3 tờ giấy in 2 mặt cho 1–2 tiết dạy), giữ trọn vẹn pháp lý (CV 5512, NLS TT 02/2025, AI QĐ 2422, liên môn) nhưng tối thiểu hóa các bước và câu thoại rườm rà.

## Phạm vi
1. **Thiết kế giao diện lựa chọn chế độ soạn**:
   - Bổ sung bộ điều khiển chọn chế độ soạn trong `canvas_soankhbd.html` (và file dự phòng tương ứng nếu cần):
     + Lựa chọn 1: **Soạn chi tiết (Mặc định)** — Giữ nguyên 100% luồng 8 bước hiện nay (8–10 trang A4, đầy đủ kịch bản phân vai, phiếu học tập E, hình vẽ F).
     + Lựa chọn 2: **Soạn rút gọn** — Tiến trình tinh gọn (4–6 trang A4, chỉ 4 hoạt động cốt lõi A–D chuẩn CV 5512, bảng 2 cột súc tích, lược bỏ thoại dài dòng và phiếu phụ lục rườm rà).
   - Lưu lựa chọn vào storage (`canvasStorage` / `localStorage`) để ghi nhớ trạng thái người dùng.
2. **Kịch bản Sư phạm & Prompt cho Chế độ Rút gọn**:
   - Giữ nguyên cấu trúc tích hợp NLS (TT 02/2025/TT-BGDĐT) và AI (QĐ 2422/QĐ-BGDĐT) cùng tích hợp môn học đã tick (marker `***[NLS: ...]***`, `***[AI: ...]***` tại 1–2 vị trí then chốt).
   - Định nghĩa hợp đồng tinh gọn `ACTIVITY_TABLE_CONTRACT_COMPACT` hoặc chỉ thị rút gọn cho prompt:
     + Dung lượng định mức chuẩn: **4–6 trang Word A4** (vừa vặn in 2–3 tờ giấy A4, không quá dài cũng không quá cụt lủn).
     + Kịch bản 4 bước trực diện: Bước 1 (Giao việc ngắn gọn) -> Bước 2 (HS thực hiện cá nhân/nhóm) -> Bước 3 (Báo cáo ngắn) -> Bước 4 (GV chốt kiến thức cốt lõi).
     + Lược bớt câu thoại văn vở dài dòng, dự kiến ngộ nhận dài dòng; tập trung vào hành động cốt lõi.
     + Cột Nội dung: Ghi quy tắc, công thức LaTeX và 1 bài tập trọng tâm có giải mẫu ngắn gọn.
     + Hoạt động D tích hợp luôn 4 nhiệm vụ tự học về nhà ở Bước 4.
3. **Điều phối luồng 1-Click (`handle1ClickGenerate`)**:
   - Khi ở chế độ "Soạn rút gọn":
     + Chỉ chạy tuần tự 6 bước cốt lõi: I. Mục tiêu -> II. Thiết bị -> III.A Khởi động -> III.B Kiến thức mới -> III.C Luyện tập -> III.D Vận dụng & Tự học.
     + Không bắt buộc chạy Bước 7 (III.E Phiếu học tập) và Bước 8 (F. Hình minh họa SGK SVG), giúp hoàn thành nhanh gấp đôi và dung lượng file Word nhỏ gọn 4–6 trang.
   - Khi ở chế độ "Soạn chi tiết":
     + Chạy đầy đủ 8 bước như hiện tại, không thay đổi dù chỉ 1 dòng logic.
4. **Đồng bộ hóa với Tab soạn độc lập (Tab 2, 3, 4)**:
   - Khi người dùng bấm nút tạo riêng ở từng Tab trong chế độ rút gọn, các hàm tạo nội dung nhận biết cờ chế độ để áp dụng prompt tinh gọn tương ứng.

## Ngoài phạm vi
- Không sửa đổi hoặc xóa bỏ bất kỳ mã lệnh nào của chế độ "Soạn chi tiết".
- Không thay đổi cấu trúc dữ liệu JSON lưu trữ giáo án (`appState.content`).
- Không thay đổi các danh mục chuẩn NLS (TT 02), AI (QĐ 2422), PPCT hay SGK.
- Không xóa các DOM ID thiết yếu đã được kiểm thử trong `tests/canvas-soankhbd-smoke.js`.

## File dự kiến tác động
- `canvas_soankhbd.html` (Thanh công cụ, bộ chọn chế độ, hàm `handle1ClickGenerate`, prompt patch cho chế độ rút gọn)
- `backupcode viettailieu/canvas_soankhbd.html` (Đồng bộ bản sao lưu dự phòng Canvas)
- `js/khbd-prompts.js` (Bổ sung chỉ thị / contract chế độ rút gọn `ACTIVITY_TABLE_CONTRACT_COMPACT` định mức 4–6 trang và tham số context `isCompact`)
- `js/khbd-app.js` (Hỗ trợ cờ chế độ soạn trong `getGenerationPromptContext` và các hàm tạo hoạt động)
- `tests/canvas-soankhbd-smoke.js` (Bổ sung kiểm thử tự động cho tùy chọn 2 chế độ và luồng rút gọn)

## Các bước thực hiện
1. **Bước 1: Bổ sung cấu hình & UI Chế độ soạn trong `canvas_soankhbd.html`**:
   - Thêm dropdown / segmented control chọn "Chế độ soạn":
     - `detailed`: "📋 Soạn chi tiết (8–10 trang, chuẩn hồ sơ dự giờ/thi GVDG)"
     - `compact`: "⚡ Soạn rút gọn (4–6 trang, chuẩn lên lớp hàng ngày)"
   - Gắn sự kiện chuyển đổi, lưu giá trị vào `canvasStorage.setItem('khbd_generation_mode', mode)`.
2. **Bước 2: Xây dựng hợp đồng & Prompt tinh gọn trong `js/khbd-prompts.js`**:
   - Xây dựng chỉ thị `ACTIVITY_TABLE_CONTRACT_COMPACT`:
     - Giới hạn chuẩn 4–6 trang Word A4.
     - Lược bỏ câu thoại diễn giải dài dòng của GV; kịch bản 4 bước ngắn gọn, cô đọng.
     - Bắt buộc giữ nguyên vị trí tích hợp NLS và AI in đậm nghiêng `***[NLS: ...]***`, `***[AI: ...]***`.
   - Cập nhật `getPromptTemplate` để chèn contract phù hợp theo `context.generationMode`.
3. **Bước 3: Cập nhật điều phối 1-Click trong `canvas_soankhbd.html`**:
   - Trong `handle1ClickGenerate`:
     - Kiểm tra chế độ hiện tại.
     - Nếu `compact`: Thông báo xác nhận hiển thị rõ quy trình 6 bước (bỏ qua E và F); truyền cờ `generationMode: 'compact'` vào `executeStep`.
     - Nếu `detailed`: Giữ nguyên 100% luồng 8 bước hiện tại.
4. **Bước 4: Cập nhật đồng bộ các Tab soạn lẻ trong `js/khbd-app.js`**:
   - Đảm bảo khi tạo lẻ từng hoạt động A, B, C, D ở các tab, nếu chế độ rút gọn đang bật thì nội dung sinh ra cũng tuân theo chuẩn tinh gọn.
5. **Bước 5: Viết kiểm thử tự động**:
   - Cập nhật `tests/canvas-soankhbd-smoke.js` để kiểm tra:
     - Tồn tại điều khiển chọn chế độ soạn trên DOM.
     - Chế độ mặc định là "detailed" (không phá vỡ tính tương thích).
     - Luồng `compact` không gọi bước E/F trong 1-Click nhưng vẫn bảo toàn đầy đủ các marker tích hợp NLS/AI.
   - Chạy toàn bộ test suites đảm bảo 100% PASS.

## Rủi ro
- **Rủi ro 1: Lỗi hồi quy chế độ Soạn chi tiết**: Nếu sửa chung hàm mà không tách nhánh điều kiện rõ ràng, chế độ chi tiết có thể bị ảnh hưởng.
  - *Giải pháp*: Thiết kế nhánh điều kiện nghiêm ngặt: nếu không phải `compact` thì 100% luồng chạy như cũ.
- **Rủi ro 2: AI cắt xén mất các marker NLS/AI trong chế độ rút gọn**: Khi yêu cầu AI viết ngắn, AI có thể tự ý bỏ qua các marker năng lực số hoặc AI.
  - *Giải pháp*: Trong chỉ thị `ACTIVITY_TABLE_CONTRACT_COMPACT`, nhấn mạnh bằng điều khoản bắt buộc: "TUYỆT ĐỐI KHÔNG ĐƯỢC BỎ CÁC MARKER NLS/AI; NLS và AI bắt buộc xuất hiện tại 1–2 vị trí then chốt dù ở chế độ rút gọn".
- **Rủi ro 3: Phá vỡ các DOM ID mà test hiện tại đang kiểm tra**:
  - *Giải pháp*: Không xóa bất kỳ DOM ID nào hiện có; chỉ thêm mới phần tử chọn chế độ.

## Cách kiểm thử
- **Kiểm thử tự động**:
  - Chạy `node tests/canvas-soankhbd-smoke.js` kiểm tra cú pháp, DOM IDs, và logic 2 chế độ.
  - Chạy `node tests/khbd-4steps-workflow-smoke.js` và `node tests/docx-export-format-smoke.js`.
- **Kiểm thử thủ công trên Canvas Sandbox**:
  - Chọn bài học thử nghiệm (ví dụ môn Toán 6 hoặc Tin học 7).
  - Thử nghiệm 1: Chọn "Soạn chi tiết" -> Bấm 1-Click -> Kiểm tra đủ 8 bước, kịch bản đầy đủ, phụ lục E, hình vẽ F.
  - Thử nghiệm 2: Chọn "Soạn rút gọn" -> Bấm 1-Click -> Kiểm tra chỉ chạy 6 bước (A–D), văn phong cô đọng, có đủ marker NLS/AI, xuất Word ra 4–6 trang đẹp mắt.

## Tiêu chí nghiệm thu
1. Người dùng có thể dễ dàng chuyển đổi qua lại giữa 2 chế độ "Soạn chi tiết" và "Soạn rút gọn" ngay trên giao diện Canvas.
2. Chế độ "Soạn chi tiết" hoạt động 100% giống như hiện tại, không có bất kỳ thay đổi nào về độ dài hay các bước sinh.
3. Chế độ "Soạn rút gọn" sinh giáo án tinh gọn (4–6 trang Word), hoàn thành nhanh hơn, kịch bản sư phạm 4 bước súc tích, bỏ qua phụ lục rườm rà.
4. Logic tích hợp chuẩn pháp lý (NLS TT 02/2025, AI QĐ 2422, liên môn) được bảo toàn 100% trên cả 2 chế độ.
5. Toàn bộ test suites tự động PASS 100%.
