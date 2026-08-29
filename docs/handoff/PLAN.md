# PLAN: Tối ưu Quy trình 4 Bước Soạn KHBD & Trải nghiệm Dán PPCT (soankhbd.html)

Trạng thái: KẾ HOẠCH ĐÃ DUYỆT

## Hiện trạng
1. Đọc SGK tự động chạy đề xuất PPDH & NLS quá sớm khi chưa có PPCT.
2. Dán PPCT (Ctrl+V) rườm rà vì phải bấm nút kích hoạt arm trước.
3. Nút đề xuất PPDH & NLS chưa được bố trí thành Bước 3 rõ ràng.
4. Năng lực AI cần đảm bảo chỉ phân tích và tick chọn khi người dùng chủ động bật.

## Phạm vi
1. **Bước 1 (Đọc SGK)**:
   - Khi bấm "Đọc sách giáo khoa" -> Mistral OCR trích xuất văn bản vào editorVision/previewVision.
   - Chưa tự động tick chọn PPDH, KTDH hay NLS.
2. **Bước 2 (Đọc PPCT & Dán nhanh Ctrl+V)**:
   - Click hoặc focus vào vùng PPCT -> Nhấn Ctrl+V dán ngay ảnh PPCT vào gallery không cần nút phụ.
   - Bấm "Đọc PPCT" -> Mistral OCR bóc tách số tiết, tuần, phạm vi bài dạy.
3. **Bước 3 (Nút AI Đề xuất PPDH, Kỹ thuật & NLS)**:
   - Thêm nút / card hành động nổi bật: "⚡ ĐỀ XUẤT PPDH, KỸ THUẬT & NĂNG LỰC SỐ (AI)".
   - Khi bấm: AI phân tích SGK + PPCT -> Tự động tick chọn PPDH, Kỹ thuật dạy học 4 pha, và 2–3 mục Năng lực số (NLS).
4. **Bước 4 (Khung Năng lực AI)**:
   - Mặc định không tick chọn Năng lực AI.
   - Khi người dùng click toggleAiCompetency -> Gemini phân tích nội dung SGK và tick chọn đúng 2–3 mục AI phù hợp nhất theo lớp (QĐ 2422).
5. **Cập nhật giao diện & Bộ kiểm thử tự động**:
   - Thêm Thanh Stepper 4 Bước trực quan trên đầu Tab 0.
   - Cập nhật tests/khbd-4steps-workflow-smoke.js.

## Ngoài phạm vi
- Không thay đổi cấu trúc bảng mã chuẩn TT 02 và QĐ 2422 trong js/khbd-standards.js.
- Không thay đổi định dạng xuất Word 5512.

## File dự kiến tác động
- `soankhbd.html`
- `js/khbd-app.js`
- `tests/khbd-4steps-workflow-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Các bước thực hiện
1. **Bước 1: Tách rời OCR SGK khỏi tự động tick chọn (js/khbd-app.js)**:
   - Trong applyTextbookOcrResult: Chỉ lưu vision text và ocrReady = true. Bỏ gọi tự động ensurePedagogyFromLesson và requestStructuredIntegrationCandidatesForEnabled.
2. **Bước 2: Nâng cấp Paste Controller cho PPCT (js/khbd-app.js & soankhbd.html)**:
   - Theo dõi activeDropzoneTarget ('sgk' hoặc 'ppct'). Khi click vào vùng PPCT, gán activeDropzoneTarget = 'ppct'.
   - Trong handleGlobalPaste: Nếu activeDropzoneTarget === 'ppct' hoặc focus trong card PPCT -> chuyển trực tiếp ảnh vào handlePpctFiles.
3. **Bước 3: Tạo Nút AI Đề xuất PPDH & NLS (soankhbd.html & js/khbd-app.js)**:
   - Bố trí Card Bước 3 rõ ràng: "⚡ ĐỀ XUẤT PHƯƠNG PHÁP, KỸ THUẬT & NĂNG LỰC SỐ".
   - Viết hàm triggerStep3PedagogyAndDigitalRecommendations(): Kích hoạt chọn PPDH, KTDH 4 pha và NLS (TT 02).
4. **Bước 4: Chuẩn hóa kích hoạt Năng lực AI (js/khbd-app.js)**:
   - Trong toggleAiCompetency: Khi checked === true -> Gọi Gemini phân tích và tick đúng 2–3 mục AI theo lớp. Khi checked === false -> Xóa sạch mã AI.
5. **Bước 5: Thêm Thanh Stepper 4 Bước trên UI (soankhbd.html)**:
   - Hiển thị 4 bước: [1. Đọc SGK] -> [2. Đọc PPCT] -> [3. Đề xuất PPDH & NLS] -> [4. Tích hợp AI & Soạn bài].
6. **Bước 6: Kiểm thử tự động**:
   - Chạy tests/khbd-4steps-workflow-smoke.js.

## Tiêu chí nghiệm thu
1. Bước 1: Đọc SGK chỉ trích xuất OCR, không tự động tick chọn sớm.
2. Bước 2: Click vào vùng PPCT -> Nhấn Ctrl+V dán ảnh trực tiếp mượt mà.
3. Bước 3: Có nút riêng để AI đề xuất PPDH, Kỹ thuật và NLS từ học liệu đã đọc.
4. Bước 4: Khung AI chỉ phân tích và chọn 2–3 mục khi người dùng click bật.
5. Kiểm thử tự động pass 100%.
