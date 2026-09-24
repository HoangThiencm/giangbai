# IMPLEMENT: CV 7991 tùy chỉnh số câu và gọi học sinh khi trình chiếu

## Đã làm
1. `taobaitap.html`: thêm hình thức `cv7991-custom` — "⭐ Dạng Công văn 7991 (Tùy chỉnh số câu trắc nghiệm / các phần)". Chọn hình thức này bật `preset: 'custom'` và hiện ô số câu Phần I / II / III, kèm gợi ý 6, 8, 12, 16 câu trắc nghiệm và dòng điểm `allocateCv7991PartScores`.
2. `generateSynthesizedFromSource` nhận cả `cv7991` và `cv7991-custom`: prompt, cắt đủ số câu sau khi chuẩn hóa, và `exam_format` thi trực tuyến đều dùng số câu giáo viên chỉnh.
3. Xuất Word, LaTeX, Text (builder sẵn có), OLM và PDF OLM nhận `cv7991-custom` cùng schema CV 7991. Điều kiện `synthForm === "cv7991" || dataToExport.some(isCv7991TrueFalseItem)` được giữ nguyên rồi nối thêm mode tùy chỉnh.
4. Trình chiếu trắc nghiệm và tự luận có nút "🎲 Gọi học sinh" và `StudentPickerModal`: nạp lớp từ `api/sodiem.php?action=classes` hoặc cache `sodiem:*`, quay số ~2,6 giây kèm beep/confetti, chấm 0–10, chọn cột (KTTX / Điểm miệng), lưu `api/sodiem.php?action=save` và `localStorage` key `sodiem:${lớp}:${môn}:2025-2026`. Offline hoặc chưa đăng nhập vẫn ghi máy; có ô dán danh sách thủ công.

## Kiểm tra coder
- `node tests/cv7991-taobaitap-thitructuyen-sync-smoke.js`: PASS 100%.
- `node tests/taobaitap-presentation-smoke.js`: PASS.
- `node tests/taobaitap-plan-smoke.js`: PASS.
- Parse khối `text/babel` của `taobaitap.html` bằng `@babel/parser` (JSX): không lỗi cú pháp.
- Máy không có `node` trên PATH; đã chạy bằng Node 20 portable. Không mở trình duyệt nên chưa bấm sinh đề AI hay lưu sổ điểm thật.

## Ngoài phạm vi
- Không sửa API `api/sodiem.php`, không sửa `sodiem.html`, không commit.
