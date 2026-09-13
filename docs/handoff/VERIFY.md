# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Phụ lục 1: Đã chuyển từ 6 cột sang 5 cột (`STT`, `Bài học`, `Số tiết`, `Yêu cầu cần đạt`, `Ghi chú`), gộp thành công 2 cột Biểu hiện NLS và AI thành 1 cột `Ghi chú`.
- Phụ lục 3: Đã chuyển từ 8 cột sang 7 cột (`Bài học`, `Số tiết`, `Tiết CT`, `Tuần`, `Thiết bị dạy học (*)`, `Địa điểm dạy học (**)`, `Ghi chú`), gộp thành công 2 cột Biểu hiện NLS và AI thành 1 cột `Ghi chú`.
- Quy tắc định dạng nội dung cột Ghi chú:
  + Năng lực số: Có 1 mã ghi ngang hàng `- Năng lực số: Mã: Mô tả`; từ 2 mã trở lên xuống dòng dùng ` + Mã: Mô tả`.
  + Năng lực AI: Có 1 mã ghi ngang hàng `- Năng lực AI: Mã: Mô tả (Áp dụng: tiết ...)`; từ 2 mã trở lên xuống dòng dùng ` + Mã: Mô tả (Áp dụng: tiết ...)`.
  + Khi có cả hai thì ghép cả hai khối; khi không có thì hiển thị `-`.
- Giữ nguyên 100% logic tạo/sinh dữ liệu ban đầu, bảo toàn đồng bộ từ Phụ lục 1 sang Phụ lục 3.
- Đồng bộ hoàn tất trên cả 3 file: `xaydungphuluc.html`, `canvas_xaydungphuluc.html`, `backupcode viettailieu/canvas_xaydungphuluc.html`.

## Test đã chạy
- `node tests/xaydungphuluc-smoke.js`: PASS
- `node tests/canvas-xaydungphuluc-smoke.js`: PASS
- `node tests/xaydungphuluc-math-smoke.js`: PASS
- `node tests/xaydungphuluc-integration-smoke.js`: PASS

## Pass / Fail từng tiêu chí
- Phụ lục 1 có đúng 5 cột với cột Ghi chú: PASS
- Phụ lục 3 có đúng 7 cột với cột Ghi chú: PASS
- Định dạng 1 mã ghi ngang hàng, từ 2 mã trở lên dùng dấu `+`: PASS
- Hiển thị `-` khi không có NLS lẫn AI: PASS
- Tỷ lệ độ rộng DOCX (`DOCX_WIDTHS`) chuẩn xác 100%: PASS
- Đồng bộ mã tích hợp giữa Phụ lục 1 và Phụ lục 3: PASS
- Toàn bộ 4 bộ test tự động thoát mã 0 không lỗi: PASS

## Bug
- Không có lỗi tồn đọng.
