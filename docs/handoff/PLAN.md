# PLAN: Tinh gọn Hoạt động E (Hướng dẫn về nhà) thành danh sách ngắn gọn, không dùng bảng 4 bước

Trạng thái: ĐÃ IMPLEMENT (chờ /verify)

## Hiện trạng
- Hiện tại, Hoạt động E (Hướng dẫn về nhà) trong `js/khbd-prompts.js` và `js/khbd-app.js` đang được thiết kế theo cấu trúc đầy đủ 4 phần (a. Mục tiêu, b. Nội dung, c. Sản phẩm, d. Tổ chức thực hiện) kèm Bảng Markdown 2 cột phân chia 4 bước (Bước 1 Chuyển giao -> Bước 2 Thực hiện -> Bước 3 Báo cáo -> Bước 4 Kết luận).
- **Vấn đề**: Đối với hoạt động hướng dẫn học sinh tự học ở nhà (thời lượng 2–3 phút), việc trình bày bảng 2 cột 4 bước gây cồng kềnh, rườm rà và trùng lặp nội dung giữa mục b) Nội dung và Cột Phải bảng d). Người dùng yêu cầu tinh gọn Hoạt động E thành định dạng danh sách 4 mục súc tích, trực diện, dễ đọc, không cần chia a) b) c) d) hay bảng 2 cột.

## Phạm vi
1. **Định dạng chuẩn mới cho Hoạt động E (Hướng dẫn về nhà)**:
   - Tiêu đề: `## E. HOẠT ĐỘNG 5: HƯỚNG DẪN VỀ NHÀ ({time_budget_E})` (hoặc `## E. HƯỚNG DẪN VỀ NHÀ ({time_budget_E})`).
   - Cấu trúc nội dung dạng danh sách phẳng gồm 4 mục cốt lõi:
     * `1. Ôn tập kiến thức: Ôn lại các định nghĩa, quy tắc, công thức trọng tâm đã học trong bài.`
     * `2. Làm bài tập: Hoàn thành các bài tập còn lại trong SGK (chưa làm/chữa ở Hoạt động C và D) và Sách bài tập (SBT) môn {subject} (kèm gợi ý/hướng dẫn phương pháp giải ngắn gọn). CẤM TUYỆT ĐỐI giao lại các bài tập đã được giải/chữa trên lớp.`
     * `3. Chuẩn bị bài mới: Đọc trước nội dung bài học tiếp theo trong SGK và chuẩn bị đồ dùng, học liệu học tập cần thiết.`
     * `4. Nhiệm vụ tìm tòi, mở rộng: {Tìm hiểu thêm ứng dụng thực tế của bài học trong các lĩnh vực khác như kinh tế, đời sống, khoa học...}`
   - Khối tích hợp AI an toàn (CHỈ xuất hiện khi giáo viên chủ động bật tích hợp AI):
     * `- Hướng dẫn Prompt AI an toàn:`
     * `+ Mẫu Prompt: "Em là học sinh lớp {grade}, em đang tự học bài {topic} và gặp khó khăn ở [nêu bài tập/khái niệm]. Bạn hãy đóng vai gia sư gợi mở, đặt cho em 2 câu hỏi định hướng để em tự tìm ra cách giải, đừng giải hộ em nhé!"`
   - Bỏ hoàn toàn các mục `### a) Mục tiêu:`, `### b) Nội dung:`, `### c) Sản phẩm:`, `### d) Tổ chức thực hiện:` và Bảng Markdown 2 cột trong Hoạt động E.

2. **Cập nhật Prompt Template (`js/khbd-prompts.js`)**:
   - `PROMPTS.GENERATE_ACTIVITY_E`: Cập nhật prompt chỉ thị rõ ràng định dạng danh sách 4 mục phẳng, cấm sinh bảng 2 cột và a) b) c) d).
   - `PROMPTS.GENERATE_ACTIVITIES_AE` (và alias `GENERATE_ACTIVITIES_AD`): Cập nhật yêu cầu cho Pha E trong luồng sinh 1-Click để đồng bộ định dạng danh sách ngắn gọn mới.

3. **Cập nhật Logic App & Validation (`js/khbd-app.js`)**:
   - `buildPhasePedagogyContext("E")`: Cập nhật prompt context đặc thù cho Pha E theo định dạng danh sách 4 mục tinh gọn.
   - `scoreKhbdActivityBlock(block)`: Điều chỉnh thang điểm cho khối E: ưu tiên khối có đủ 4 nội dung (Ôn tập, Làm bài tập, Chuẩn bị bài mới, Tìm tòi mở rộng), không trừ điểm vì thiếu a) b) c) d) hay bảng.
   - Đảm bảo các hàm render Preview KaTeX (`renderMathPreview`) và `getFullLessonPlanMarkdown` hiển thị danh sách mục 1, 2, 3, 4 đẹp mắt, rõ ràng.

4. **Cập nhật Kiểm thử (`tests/khbd-activity-e-smoke.js` và các file test liên quan)**:
   - Cập nhật các assertions trong `tests/khbd-activity-e-smoke.js` để kiểm tra đúng định dạng danh sách tinh gọn mới (có đủ 4 mục nội dung, không bắt buộc bảng 2 cột).

## Ngoài phạm vi
- Không thay đổi cấu trúc bảng 2 cột chuẩn CV 5512 của các Hoạt động A, B, C, D (vẫn giữ nguyên 4 bước và bảng 2 cột cho các hoạt động diễn ra trực tiếp tại lớp học).
- Không can thiệp vào cấu trúc xuất file Word chung (DocxGenerator tự động render heading và danh sách có thụt lề chuẩn).

## File dự kiến tác động
- `js/khbd-prompts.js`
- `js/khbd-app.js`
- `tests/khbd-activity-e-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Các bước thực hiện
1. **Bước 1: Cập nhật Prompt `GENERATE_ACTIVITY_E` và `GENERATE_ACTIVITIES_AE` trong `js/khbd-prompts.js`**:
   - Biên soạn lại mẫu prompt và contract cho Hoạt động E theo đúng ví dụ của người dùng: xuất thẳng danh sách 4 mục 1., 2., 3., 4. (kèm Mẫu Prompt AI an toàn nếu có).
2. **Bước 2: Cập nhật Logic trong `js/khbd-app.js`**:
   - Sửa `buildPhasePedagogyContext("E")` để nhất quán với prompt mới.
   - Cập nhật hàm chấm điểm khối `scoreKhbdActivityBlock` cho khối E.
3. **Bước 3: Cập nhật Unit Tests trong `tests/khbd-activity-e-smoke.js`**:
   - Điều chỉnh assertion kiểm thử định dạng mới của Hoạt động E.
4. **Bước 4: Chạy bộ kiểm thử tự động**:
   - Chạy `node tests/khbd-activity-e-smoke.js`, `node tests/khbd-4steps-workflow-smoke.js`, `node tests/khbd-docx-layout-smoke.js` để đảm bảo toàn bộ hệ thống tương thích và pass 100%.

## Rủi ro
- **Rủi ro**: Parser cắt ghép markdown trong luồng 1-Click (`clipKhbdActivityMarkdown`) có thể bị ảnh hưởng nếu marker kết thúc không rõ.
  - **Khắc phục**: Heading `## E.` và các heading tiếp theo (`## F.` / `# IV.` / `# Hình minh họa`) vẫn được giữ nguyên nên regex phân tách hoạt động hoạt động hoàn toàn chính xác.

## Cách kiểm thử
1. Kiểm tra Prompt Hoạt động E:
   - Mở Tab Hoạt động E trên `soankhbd.html` -> Bấm "Tạo Hoạt động E".
   - Kết quả sinh ra đúng định dạng danh sách:
     * `## E. HOẠT ĐỘNG 5: HƯỚNG DẪN VỀ NHÀ (2 phút)`
     * `1. Ôn tập kiến thức: ...`
     * `2. Làm bài tập: ...`
     * `3. Chuẩn bị bài mới: ...`
     * `4. Nhiệm vụ tìm tòi, mở rộng: ...`
     * `- Hướng dẫn Prompt AI an toàn:` (nếu bật AI)
     * `+ Mẫu Prompt: "..."`
2. Kiểm tra phần Preview KaTeX & Bảng biểu:
   - Giao diện hiển thị danh sách rõ ràng, không còn bảng trống hay các mục a) b) c) d) rườm rà.
3. Kiểm tra Xuất file Word (.docx):
   - Xuất giáo án và mở file .docx, Hoạt động E hiển thị dưới dạng tiêu đề và các đoạn danh sách căn lề chuẩn mực.

## Tiêu chí nghiệm thu
1. Hoạt động E được sinh ra theo đúng định dạng danh sách 4 mục tinh gọn, không chứa a) b) c) d) hay bảng 2 cột 4 bước.
2. Tích hợp Mẫu Prompt AI an toàn tự động xuất hiện chuẩn chỉnh khi bật tính năng AI.
3. Tất cả unit tests liên quan đến Hoạt động E và xuất file docx đều PASS.
