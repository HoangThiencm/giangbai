# IMPLEMENT: Tách Riêng Các Môn Lịch Sử, Địa Lí, Vật Lí, Hoá Học, Sinh Học & Nạp Mục Lục SGK Thống Nhất

## Phạm vi đã triển khai

### 1. Dữ liệu chuẩn THCS (`js/khbd-curriculum.js` & `agent-tools/thcs-toc.json`)
- Đăng ký 5 môn học độc lập mới:
  - `{ id: 'lichsu', name: 'Lịch sử', grades: [6, 7, 8, 9] }`
  - `{ id: 'diali', name: 'Địa lí', grades: [6, 7, 8, 9] }`
  - `{ id: 'vatli', name: 'Vật lí', grades: [6, 7, 8, 9] }`
  - `{ id: 'hoahoc', name: 'Hoá học', grades: [6, 7, 8, 9] }`
  - `{ id: 'sinhhoc', name: 'Sinh học', grades: [6, 7, 8, 9] }`
- Nạp danh mục bài học chuẩn xác 100% từ SGK Thống nhất (theo đúng thứ tự chương, bài, số tiết và gợi ý mã NLS/AI):
  - **Lịch sử**: Khối 6 (20 bài), Khối 7 (20 bài), Khối 8 (21 bài), Khối 9 (25 bài).
  - **Địa lí**: Khối 6 (31 bài), Khối 7 (21 bài), Khối 8 (14 bài), Khối 9 (24 bài).
  - **Vật lí**: Khối 6 (23 bài), Khối 7 (14 bài), Khối 8 (17 bài), Khối 9 (16 bài).
  - **Hoá học**: Khối 6 (9 bài), Khối 7 (6 bài), Khối 8 (12 bài), Khối 9 (18 bài).
  - **Sinh học**: Khối 6 (22 bài), Khối 7 (22 bài), Khối 8 (18 bài), Khối 9 (16 bài).
- Duy trì song song môn ghép `khtn` (140 tiết) và `lichsudialy` (105 tiết) để bảo đảm tính tương thích ngược hoàn hảo.
- Tuân thủ quy tắc không xuất hiện nhãn tên bộ sách.

### 2. Giao diện & Công cụ Kế hoạch Giáo dục (`canvas_xaydungphuluc.html` & `xaydungphuluc.html`)
- Cấu hình số tiết trong menu môn học (`SUBJECTS`):
  - Lịch sử: 52 tiết/năm
  - Địa lí: 53 tiết/năm
  - Vật lí: 47 tiết/năm
  - Hoá học: 43 tiết/năm
  - Sinh học: 50 tiết/năm
  - Khoa học tự nhiên: 140 tiết/năm
  - Lịch sử và Địa lí: 105 tiết/năm
- Cập nhật chuẩn hóa chuỗi và nhận diện môn:
  - `getSubjectCurriculumKey()`: Phân tách rõ ràng giữa `vatli/ly`, `hoahoc/hoa`, `sinhhoc/sinh`, `lichsu`, `diali/dia ly`, `khtn`, `lichsudialy`.
  - `detectGradeAndSubjectFromFileName()`: Nhận diện chính xác tên môn từ file tải lên.
  - `getStandardSubjectYccd()`: Tạo câu YCCĐ chuẩn cho riêng từng phân môn.
  - `EQUIPMENT`: Bổ sung thiết bị dạy học chuyên biệt cho Vật lí (bộ thí nghiệm cơ-quang-điện-nhiệt, cảm biến, PhET), Hoá học (ống nghiệm, đèn cồn, bảng tuần hoàn, mô hình 3D), Sinh học (kính hiển vi, tiêu bản, mô hình giải phẫu 3D), Lịch sử và Địa lí.
  - `SUBJECT_SAMPLE_TOPICS`: Bổ sung chuyên đề/CLB ngoại khóa trải nghiệm phù hợp cho từng môn.
  - `nlsSubjectToolkit` & `lessonAppliedAiFallback`: Thiết lập công cụ số và prompt AI sư phạm riêng biệt cho từng môn.
  - `canvas_xaydungphuluc.html`: Sử dụng relative paths cho các tài nguyên để đảm bảo chạy mượt mà trên mọi môi trường.

### 3. Kiểm thử & Đảm bảo chất lượng (`tests/khbd-curriculum-thcs-smoke.js` & `verify_patch.py`)
- Mở rộng smoke test kiểm tra:
  - Sự tồn tại của toàn bộ các môn THCS trong danh sách môn học.
  - Số lượng bài học của từng khối cho từng môn đạt yêu cầu (> 5 bài).
  - Kiểm tra phủ định chuỗi tên sách (không chứa "kết nối tri thức" hay "kntt").
- Chạy toàn diện bộ kiểm thử `verify_patch.py`: 100% tests PASSED.
