# VERIFY

## Kết luận
PASS

## Phạm vi đã nghiệm thu
- [x] `recalculatePpctSequences()` tính lại Tiết CT luỹ kế theo thứ tự PPCT, phân bổ Tuần theo định mức môn học (Toán học: 4 tiết/tuần), đồng bộ bảng nguồn và dữ liệu PPCT chuẩn.
- [x] Di chuyển bằng nút `▲`/`▼` và kéo-thả đều đi qua `reorderPpctRow()` rồi tự tính lại Tiết CT/Tuần. Nút `🔄 Tính lại Tiết CT & Tuần tự động` có mặt và gọi đúng hàm.
- [x] Ô Tiết CT và Tuần vẫn sửa trực tiếp được; dữ liệu nhập tay được chuẩn hóa trước khi một lần tính lại tự động tiếp theo được yêu cầu.
- [x] YCCĐ được tách dòng trong preview/DOCX; mã NLS và AI ở từng dòng riêng, giữ NLS khi chọn AI và không lặp phạm vi `Áp dụng: tiết ...`.
- [x] Tiết CT nhiều tiết hiển thị từng dòng, tuần trùng lặp được khử; DOCX dùng A4 ngang, Times New Roman 13pt, dãn dòng 1.3 và bảng rộng 100%.

## Kiểm tra đã chạy
1. `node tests/xaydungphuluc-smoke.js` — PASS
2. `node tests/xaydungphuluc-integration-smoke.js` — PASS
3. `git diff --check` — PASS

## Bug
- Không phát hiện lỗi trong phạm vi kế hoạch đã duyệt.
