# PLAN: Tích hợp Bộ Lọc Sư phạm Chống Khiên cưỡng & Ràng buộc Thực chiến (soankhbd.html)

Trạng thái: KẾ HOẠCH ĐÃ DUYỆT

## Hiện trạng
1. Đề xuất NLS/AI còn bị gán ghép khiên cưỡng do chưa phân loại theo dạng bài (Hình học, Đại số, Thống kê).
2. Chưa kiểm soát chặt chẽ thời lượng 45 phút, gây quá tải kỹ thuật dạy học nhóm trong 1 tiết.
3. Khi lớp học không có thiết bị, AI đôi khi vẫn tự sinh hoạt động tra cứu mạng/app công nghệ cao.

## Phạm vi
1. **Bộ lọc theo Phân môn & Dạng bài (Subject & Topic Classification Gate)**:
   - Trong `js/khbd-standards.js` (`scoreOfficialStandard` & `recommendOfficialStandards`):
     * **Bài Hình học & Đo đạc**: Ưu tiên trực quan hóa (thước, compa, mô hình, GeoGebra nếu có máy tính); CẤM TUYỆT ĐỐI đề xuất mã Lập trình (3.4), Bản quyền số (3.3), hoặc các mã AI không liên quan.
     * **Bài Đại số & Số học**: Ưu tiên tính toán, máy tính cầm tay, giải quyết vấn đề số học; CẤM gán ghép bảo vệ dữ liệu cá nhân hay đạo đức AI gượng ép.
     * **Bài Thống kê & Xác suất**: Ưu tiên thu thập, đánh giá và biểu diễn bảng/biểu đồ số (1.1, 1.2, 1.3).
2. **Quy tắc "Tích hợp Tự nhiên — Không Gượng ép"**:
   - Nếu bài học là lý thuyết thuần túy hoặc không có điều kiện công nghệ: Chỉ đề xuất mục tối thiểu gắn liền SGK / máy tính cầm tay, không ép học sinh dùng AI hay công nghệ phức tạp.
   - Ràng buộc Cơ sở vật chất (`Facility Gate`): Nếu `facilities.devices = false` và `facilities.internet = false` -> CẤM sinh hoạt động đòi hỏi học sinh dùng điện thoại/laptop/chatbot trong lớp.
3. **Ràng buộc Thời lượng Tiết dạy (Time-Budget Gate)**:
   - **Bài 1 tiết (45 phút)**: Khóa cứng chỉ chọn **tối đa 1 kỹ thuật dạy học tích cực nhẹ nhàng** trong pha B (Hình thành kiến thức) như *Think-Pair-Share* (3–5 phút) hoặc *Khăn trải bàn ngắn* (5 phút). CẤM kết hợp nhiều kỹ thuật nhóm phức tạp.
   - **Bài 2–3 tiết**: Mới cho phép phân bổ các kỹ thuật sâu như *Mảnh ghép*, *Trạm/Góc học tập*, *Dự án nhỏ*.
4. **Cập nhật Prompt Engineering Chống Khiên cưỡng (`js/khbd-prompts.js`)**:
   - Bổ sung chỉ dẫn cấm gán ghép khiên cưỡng vào tất cả các Prompt sinh Mục tiêu (I), Thiết bị (II), và Hoạt động (III A–D).
5. **Cập nhật Bộ kiểm thử tự động**:
   - Cập nhật `tests/khbd-pedagogy-script-smoke.js` và `tests/khbd-4steps-workflow-smoke.js`.

## Ngoài phạm vi
- Không thay đổi danh mục mã chuẩn TT 02/2025 & QĐ 2422.
- Không thay đổi định dạng xuất Word 5512.

## File dự kiến tác động
- `js/khbd-standards.js`
- `js/khbd-prompts.js`
- `js/khbd-app.js`
- `tests/khbd-4steps-workflow-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Các bước thực hiện
1. **Bước 1: Nâng cấp hàm nhận diện dạng bài & chấm điểm trong `js/khbd-standards.js`**:
   - Viết hàm `detectLessonMathBranch(topic, vision)`: Phân loại "geometry" (Hình học), "algebra" (Đại số), "statistics" (Thống kê).
   - Trong `scoreOfficialStandard`: Áp dụng điểm phạt nặng (về 0) cho các mã không phù hợp dạng bài (ví dụ phạt mã 3.4 Lập trình trong bài Hình học).
2. **Bước 2: Cài đặt Time-Budget Gate trong `js/khbd-app.js`**:
   - Trong `ensurePedagogyFromLesson`: Kiểm tra số tiết (`appState.duration`). Nếu là 1 tiết (45 phút), chỉ giữ 1 kỹ thuật nhẹ nhàng nhất cho pha B, loại bỏ việc nhồi nhét nhiều kỹ thuật.
3. **Bước 3: Tích hợp Negative Constraints vào `js/khbd-prompts.js`**:
   - Đưa chỉ dẫn cấm gượng ép công nghệ khi lớp không có thiết bị và cấm kéo dài hoạt động quá thời lượng tiết dạy vào toàn bộ prompt.
4. **Bước 4: Kiểm thử tự động**:
   - Chạy `node tests/khbd-4steps-workflow-smoke.js`.

## Tiêu chí nghiệm thu
1. Bài Hình học: Không bao giờ đề xuất mã Lập trình (3.4) hay Bản quyền số (3.3).
2. Bài 1 tiết (45 phút): Chỉ đề xuất tối đa 1 kỹ thuật dạy học nhóm nhẹ nhàng, không cháy giáo án.
3. Lớp không có thiết bị HS: Giáo án không tự bịa hoạt động học sinh dùng điện thoại/laptop trong giờ.
4. Bộ kiểm thử tự động pass 100%.
