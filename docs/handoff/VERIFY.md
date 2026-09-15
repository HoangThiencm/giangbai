# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- `js/khbd-app.js`:
  + Đã bổ sung `getLessonPeriodsCount(duration, grade)` và nâng cấp `applyTimeBudgetGateToPedagogy()`:
    * Bài 1 tiết (<= 45 phút): Ép PPDH tối đa đúng 1 phương pháp chủ đạo; KTDH tối đa 1–2 kỹ thuật nhẹ (Think-Pair-Share, Khăn trải bàn rút gọn, 5W1H); loại bỏ hoàn toàn các kỹ thuật cồng kềnh (Jigsaw, Station, Gallery walk, Mini-project, PBL, STEAM).
    * Bài 2 tiết (90 phút): Giới hạn tối đa 2 PPDH; tối đa 2–3 KTDH.
    * Bài từ 3 tiết trở lên: Giới hạn tối đa 2 PPDH; tối đa 3–4 KTDH.
  + Đã bổ sung hàm `formatKhbdRoleLineBreaks(markdown)` tự động chèn `<br>- **GV:**` và `<br>- **HS:**` khi phát hiện vai trò bị viết dính liền không có ngắt dòng; tích hợp trực tiếp vào pipeline `applyActivityOutput()`.
- `js/khbd-prompts.js`:
  + Cập nhật quy tắc Cột TRÁI bảng d): Mỗi bước bắt buộc xuống dòng riêng cho Tiêu đề bước, dòng `- **GV:**` và dòng `- **HS:**` (nghiêm cấm viết dính liền GV và HS trên cùng 1 dòng).
  + Bổ sung điều khoản TIME-BUDGET GATE theo số tiết vào hợp đồng sư phạm.
- `js/khbd-docx.js`:
  + Trong `parseTableCellParagraphs()`: Tự động phát hiện và tách các dòng vai trò `GV:` / `HS:` thành các đối tượng `Paragraph` riêng biệt với thụt đầu dòng chuẩn mực (`indent: { left: 360 }`), giúp file Word xuất ra luôn hiển thị phân vai rõ ràng.
- `tests/khbd-pedagogy-rate-smoke.js`:
  + Tạo mới và kiểm thử toàn diện cả 6 nội dung: Gate 1 tiết, Gate 2 tiết, hàm `formatKhbdRoleLineBreaks`, pipeline hoạt động, Word DOCX paragraph separation và prompt contract.

## Test đã chạy
- `node tests/khbd-pedagogy-rate-smoke.js`: PASS 100%
- `node tests/canvas-soankhbd-smoke.js`: PASS 100%
- `node tests/khbd-nls-ai-bold-italic-smoke.js`: PASS 100%
- `node tests/khbd-docx-format-smoke.js`: PASS 100%
- `node tests/khbd-integrations-smoke.js`: PASS 100%
- `node tests/khbd-dynamic-integrations-smoke.js`: PASS 100%

## Pass / Fail từng tiêu chí
- Tiêu chí 1 (Bài 1 tiết chỉ đề xuất 1 PPDH + tối đa 1–2 KTDH nhẹ, chặn kỹ thuật nặng): PASS
- Tiêu chí 2 (Bài 2 tiết đề xuất tối đa 2 PPDH + 2–3 KTDH): PASS
- Tiêu chí 3 (Tự động ngắt dòng phân vai GV và HS bằng `<br>- **GV:**` và `<br>- **HS:**`): PASS
- Tiêu chí 4 (File Word .docx xuất ra tách thành các Paragraph riêng có thụt đầu dòng cho GV và HS): PASS
- Tiêu chí 5 (Toàn bộ test suites liên quan đều đạt 100%): PASS

## Bug
Không có.
