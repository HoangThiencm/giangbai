# PLAN: Tách Riêng Các Môn Lịch Sử, Địa Lí, Vật Lí, Hoá Học, Sinh Học & Nạp Mục Lục Chuẩn SGK Thống Nhất

## 1. Bối cảnh & Yêu cầu
- Tách riêng toàn bộ các phân môn độc lập trong `canvas_xaydungphuluc.html` và `xaydungphuluc.html`:
  - **Lịch sử**: 52 tiết/năm, mã `lichsu`, icon 🏛.
  - **Địa lí**: 53 tiết/năm, mã `diali`, icon 🌍.
  - **Vật lí**: 47 tiết/năm, mã `vatli`, icon ⚡.
  - **Hoá học**: 43 tiết/năm, mã `hoahoc`, icon 🧪.
  - **Sinh học**: 50 tiết/năm, mã `sinhhoc`, icon 🌱.
  - Bảo lưu tương thích ngược cho môn ghép: **Khoa học tự nhiên** (140 tiết/năm, mã `khtn`, icon 🔬) và **Lịch sử và Địa lí** (105 tiết/năm, mã `lichsudialy`, icon 🌏).
- Nạp lại 100% mục lục bài học chính xác theo Chương trình GDPT 2018 / SGK Thống nhất cho cả 4 khối 6, 7, 8, 9.
- **Ràng buộc tuyệt đối**: Không đề cập tên bộ sách ("Kết nối tri thức", "KNTT") trong nhãn hệ thống hoặc tiêu đề danh mục.
- Chuyển đường dẫn tài nguyên trong `canvas_xaydungphuluc.html` sang dạng relative path (`js/...`, `css/...`) để chạy ổn định cả trên localhost lẫn máy chủ production.

## 2. Giải pháp Kỹ thuật
1. **Dữ liệu chương trình (`js/khbd-curriculum.js` & `agent-tools/thcs-toc.json`)**:
   - Thêm định nghĩa môn `vatli`, `hoahoc`, `sinhhoc`, `lichsu`, `diali` vào `CURRICULUM_DATA.subjects`.
   - Phân rã mục lục SGK Thống nhất chuẩn xác theo từng phân môn:
     - **Vật lí**: Lớp 6 (23 bài), Lớp 7 (14 bài), Lớp 8 (17 bài), Lớp 9 (16 bài).
     - **Hoá học**: Lớp 6 (9 bài), Lớp 7 (6 bài), Lớp 8 (12 bài), Lớp 9 (18 bài).
     - **Sinh học**: Lớp 6 (22 bài), Lớp 7 (22 bài), Lớp 8 (18 bài), Lớp 9 (16 bài).
     - **Lịch sử**: Lớp 6 (20 bài), Lớp 7 (20 bài), Lớp 8 (21 bài), Lớp 9 (25 bài).
     - **Địa lí**: Lớp 6 (31 bài), Lớp 7 (21 bài), Lớp 8 (14 bài), Lớp 9 (24 bài).
   - Duy trì song song môn ghép `khtn` (140 tiết) và `lichsudialy` (105 tiết).
2. **Giao diện & Logic Nghiệp vụ (`canvas_xaydungphuluc.html` & `xaydungphuluc.html`)**:
   - Cập nhật danh mục `SUBJECTS` và `KHBD_ALL_SUBJECTS` hiển thị đầy đủ các môn trên thanh chọn môn học.
   - Hàm `getSubjectCurriculumKey()` phân tích linh hoạt các từ khóa: `vatli/ly`, `hoahoc/hoa`, `sinhhoc/sinh`, `lichsu`, `diali/dia ly`, `khtn`, `lichsudialy`.
   - Tự động nhận diện môn từ file upload (`detectGradeAndSubjectFromFileName()`).
   - Cung cấp mẫu câu YCCĐ chuẩn cho từng môn (`getStandardSubjectYccd()`).
   - Cấu hình thiết bị dạy học (`EQUIPMENT`), chủ đề trải nghiệm (`SUBJECT_SAMPLE_TOPICS`), bộ công cụ số NLS (`nlsSubjectToolkit`) và prompt AI sư phạm (`lessonAppliedAiFallback`) riêng biệt cho từng môn.
3. **Bộ kiểm thử tự động**:
   - Mở rộng smoke test kiểm tra toàn bộ 7 môn THCS, đảm bảo số bài học > 5 và không vi phạm quy tắc bản quyền thương hiệu.

## 3. Tiêu chí Nghiệm thu
- [x] Menu chọn môn học hiển thị đầy đủ: Lịch sử, Địa lí, Vật lí, Hoá học, Sinh học và các môn tổng hợp.
- [x] Nạp đầy đủ mục lục bài học chuẩn xác từ lớp 6 đến lớp 9 theo SGK Thống nhất.
- [x] Không xuất hiện chuỗi ký tự "Kết nối tri thức" hay "KNTT" trong hệ thống.
- [x] Tương thích ngược hoàn toàn với dữ liệu cũ của môn ghép `khtn` và `lichsudialy`.
- [x] Đạt 100% các bài kiểm tra logic và dữ liệu.
