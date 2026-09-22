# IMPLEMENT: AI thẩm định mức độ nhận thức cho OLM

## Phạm vi đã thực hiện

- `taobaitap.html`: Cả ba luồng AI (tạo đề, tạo từ học liệu, trích xuất Word/PDF) nay yêu cầu mô hình tự đánh giá bản chất từng câu và trả về `level`: Nhận biết, Thông hiểu, Vận dụng hoặc Vận dụng cao.
- `taobaitap.html`: `normalizeQuizItems` chuẩn hóa nhãn AI trả về, giữ nhãn đó trong dữ liệu và dùng Nhận biết làm mặc định an toàn cho đề cũ/dữ liệu thiếu.
- `taobaitap.html`: Bước 2 hiển thị bộ chọn mức độ trên từng câu để giáo viên xem và điều chỉnh trước khi xuất OLM.
- `taobaitap.html`: `getOlmLevelTag` luôn trả về một trong `[NB]`, `[TH]`, `[VD]`, `[VDC]`; không còn xuất nhãn rỗng.
- `tests/taobaitap-olm-export-smoke.js`: Thêm kiểm thử trực tiếp bốn nhãn xuất, kiểm tra prompt/normalizer và bộ chọn trên giao diện.

## Kiểm thử

- PASS: `node tests/taobaitap-olm-export-smoke.js`
- PASS: `node tests/cv7991-taobaitap-thitructuyen-sync-smoke.js`
- PASS: `node tests/taobaitap-game-word-export-smoke.js`
- PASS: `git diff --check`
