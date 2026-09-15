# VERIFY: Tách Riêng Các Môn Lịch Sử, Địa Lí, Vật Lí, Hoá Học, Sinh Học & Nạp Mục Lục SGK Thống Nhất

## Kết luận
PASS

## Đối chiếu Scope & Tính năng
- [x] **Tách toàn bộ các môn Lịch sử, Địa lí, Vật lí (Lý), Hoá học (Hoá), Sinh học (Sinh):**
  - `canvas_xaydungphuluc.html` & `xaydungphuluc.html` hiển thị đầy đủ trên thanh chọn môn học:
    - **Lịch sử**: 52 tiết/năm, icon 🏛
    - **Địa lí**: 53 tiết/năm, icon 🌍
    - **Vật lí**: 47 tiết/năm, icon ⚡
    - **Hoá học**: 43 tiết/năm, icon 🧪
    - **Sinh học**: 50 tiết/năm, icon 🌱
    - **Khoa học tự nhiên**: 140 tiết/năm, icon 🔬
    - **Lịch sử và Địa lí**: 105 tiết/năm, icon 🌏
- [x] **Nạp mục lục chuẩn SGK Thống nhất (Kết nối tri thức):**
  - Đã nạp đầy đủ 100% mục lục bài học chuẩn xác, phân chia chương mục rõ ràng cho cả 4 khối (6, 7, 8, 9) vào `js/khbd-curriculum.js` và `agent-tools/thcs-toc.json`:
    - **Vật lí**: Lớp 6 (23 bài), Lớp 7 (14 bài), Lớp 8 (17 bài), Lớp 9 (16 bài).
    - **Hoá học**: Lớp 6 (9 bài), Lớp 7 (6 bài), Lớp 8 (12 bài), Lớp 9 (18 bài).
    - **Sinh học**: Lớp 6 (22 bài), Lớp 7 (22 bài), Lớp 8 (18 bài), Lớp 9 (16 bài).
    - **Lịch sử**: Lớp 6 (20 bài), Lớp 7 (20 bài), Lớp 8 (21 bài), Lớp 9 (25 bài).
    - **Địa lí**: Lớp 6 (31 bài), Lớp 7 (21 bài), Lớp 8 (14 bài), Lớp 9 (24 bài).
- [x] **Không đề cập tên bộ sách trong hệ thống:**
  - Regex phủ định `!/kntt|kết nối tri thức/i` pass trên toàn bộ cấu hình, tên môn, nhãn và danh mục.
- [x] **Đường dẫn tài nguyên ổn định:**
  - Chuyển toàn bộ CDN/remote scripts sang relative paths (`js/khbd-curriculum.js`, `css/khbd-styles.css`,...).

## Test đã chạy
1. `python verify_patch.py`:
   - `test_curriculum_js`: PASSED
   - `test_thcs_toc`: PASSED (tất cả các môn cho 4 khối 6, 7, 8, 9)
   - `test_canvas_html`: PASSED
   - `test_xaydungphuluc_html`: PASSED
   - `test_regex_logic`: PASSED
   - Kết quả: **ALL TESTS PASSED WITH 100% SUCCESS!**
2. Smoke test `tests/khbd-curriculum-thcs-smoke.js` đã mở rộng kiểm thử cả 7 môn THCS.

## Bug
Không có.
