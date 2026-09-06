# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- File mới `backupcode viettailieu/canvas_xaydungphuluc.html`: Đạt. Đã tạo độc lập, kế thừa toàn diện quy trình 7 bước, cấu hình sư phạm, PPCT, SGK, OCR PDF scan fallback qua Canvas.
- Tầng kết nối AI Canvas không cần key: Đạt. Gọi `https://hoangthiencm.id.vn/api/canvas_gemini.php` với `credentials: 'omit'`, model cố định `gemini-3-flash-preview`, không có trường nhập hay lưu API key cá nhân, có `#canvasHostBanner`.
- Phụ lục 1 đầy đủ 2 cột riêng biệt `Biểu hiện năng lực số` và `Biểu hiện năng lực AI`: Đạt. Hiển thị đúng mã màu NLS `#0070C0`, AI `#7030A0`.
- Xuất DOCX và ZIP: Đạt. Định dạng A4 ngang (`width: 11906, height: 16838, orientation: PageOrientation.LANDSCAPE`), xuất DOCX đơn và xuất gói ZIP đầy đủ các tệp phụ lục.
- Bảng chỉnh sửa trực quan (contenteditable, thêm/xóa dòng) và báo cáo thẩm định sư phạm: Đạt.
- Không sửa source gốc `xaydungphuluc.html`: Đạt.

## Test đã chạy
- `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
- `node tests/xaydungphuluc-smoke.js`: PASS.
- `node tests/xaydungphuluc-integration-smoke.js`: PASS.

## Pass / Fail từng tiêu chí
- [x] Tạo tệp `backupcode viettailieu/canvas_xaydungphuluc.html`: PASS
- [x] Không lưu hay yêu cầu key cá nhân, kết nối API Canvas nội bộ với credentials: omit: PASS
- [x] Phụ lục 1 tách riêng cột Biểu hiện năng lực số và Biểu hiện năng lực AI: PASS
- [x] Xuất Word (.docx) chuẩn khổ ngang A4 (11906x16838 LANDSCAPE): PASS
- [x] Xuất ZIP trọn bộ các phụ lục: PASS
- [x] Thẩm định sư phạm và chỉnh sửa trực quan: PASS
- [x] Không ảnh hưởng mã nguồn khác: PASS

## Bug
(Không có lỗi)
