# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- **Khớp 100% phạm vi PLAN.md**:
  + Cơ chế liên thông Phụ lục 3 -> Phụ lục 1: Khi nạp Phụ lục 3, ứng dụng tự động sinh Phụ lục 1 chuẩn 5 cột (`STT`, `Bài học`, `Số tiết`, `Yêu cầu cần đạt`, `Mã NLS & AI`), trong đó AI tự sinh `outcomes` chuẩn GDPT 2018; đồng thời Phụ lục 3 giữ nguyên 100% các cột tiến độ và dữ liệu nguồn.
  + Cơ chế chọn 12 tiết AI trọng tâm (`AI_SELECTION_LIMIT = 12`) hoạt động chính xác trên cả bảng PPCT và dạng text/PDF.
  + Bộ lọc SGK tinh gọn (`compactSgkText`) trích xuất đúng tên bài, mục tiêu, hoạt động khám phá/vận dụng, tiết kiệm token.
  + Định dạng Word (.docx) và Web Preview tuân thủ 6 phần hành chính chuẩn mẫu `Phụ lục 1 - Lớp 6 - Toán.docx`, thể hiện đúng 2 màu: NLS Xanh (`0070C0`), NLAI Tím (`7030A0`).
  + Thanh tiến trình hiển thị mượt mà, dừng spinner và hiển thị tích xanh `✓` ở 100%, tự đóng sau 1.5s hoặc bấm `✕`.
- **Không vi phạm phạm vi**: Chỉ can thiệp đúng các file theo kế hoạch (`xaydungphuluc.html`, `tests/xaydungphuluc-smoke.js`, tài liệu handoff).

## Test đã chạy
- `node tests/xaydungphuluc-smoke.js` — **PASS** (Kiểm tra trọn vẹn: 7 cột PPCT, bảng độc lập, lọc SGK, tick 12 tiết AI, bảng 5 cột Phụ lục 1 sinh YCCĐ, màu NLS/AI và xuất Word).
- `node tests/xaydungphuluc-integration-smoke.js` — **PASS** (Kiểm tra tích hợp portal, phân quyền giáo viên, thẻ khởi chạy).
- Kiểm tra phân tích cú pháp VM JavaScript nội tuyến `xaydungphuluc.html` — **PASS**.

## Pass / Fail từng tiêu chí
1. **Liên thông Phụ lục 3 -> Phụ lục 1 tự sinh YCCĐ GDPT 2018 & bảo toàn Phụ lục 3**: PASS
2. **Khớp hình thức và cấu trúc hành chính file mẫu**: PASS
3. **Tick chọn tối đa 12 tiết AI trọng tâm**: PASS
4. **Hiển thị đúng 2 màu NLS Xanh (`0070C0`) / AI Tím (`7030A0`) trên Preview và Word**: PASS
5. **Toàn bộ smoke test tự động đều đạt 100%**: PASS

## Bug
- Không có
