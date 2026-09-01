# VERIFY

## Kết luận
PASS

## Phạm vi đã nghiệm thu
- [x] PPCT Mục 3 có nút thêm bài học, thêm tiêu đề, chèn dòng dưới từng hàng, xóa từng hàng, di chuyển `▲`/`▼` và kéo-thả.
- [x] `insertPpctRowAt`, `deletePpctRowAt` và `reorderPpctRow` đều gọi `recalculatePpctSequences`; Tiết CT được đánh liên tục, Tuần được phân bổ theo định mức môn học. Dòng tiêu đề không tiêu thụ tiết.
- [x] Chèn/xóa/di chuyển đồng bộ `sourcePpctTable`, `sourcePpctRows`, Phụ lục 1/3, preview và lựa chọn AI. Xóa yêu cầu xác nhận trước khi thực hiện.
- [x] YCCĐ tách từng ý; NLS và AI hiển thị từng dòng, vẫn giữ NLS khi chọn AI và không lặp phạm vi `Áp dụng: tiết ...`.
- [x] Tiết CT nhiều tiết hiển thị xuống dòng, Tuần trùng được khử; DOCX vẫn A4 ngang, Times New Roman 13pt, dãn dòng 1.3 và bảng rộng 100%.

## Kiểm tra đã chạy
1. `node tests/xaydungphuluc-smoke.js` — PASS
   - Bao phủ chèn bài mặc định/tiêu đề, xóa, tính lại luỹ kế, đồng bộ bảng nguồn và ánh xạ lại lựa chọn AI.
2. `node tests/xaydungphuluc-integration-smoke.js` — PASS
3. `git diff --check` — PASS

## Bug
- Không phát hiện lỗi trong phạm vi kế hoạch đã duyệt.
