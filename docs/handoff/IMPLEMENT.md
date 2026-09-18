# IMPLEMENT: Liên thông Tạo bài tập → Thi trực tuyến 1-Click & chế độ cuốn chiếu chống AI

Đã triển khai đúng `docs/handoff/PLAN.md`.

## Thay đổi

### `taobaitap.html` & `backupcode viettailieu/taobaitap.html`
- `mapToThiTrucTuyenPayload(questions, topics, synthForm)`: map `multiple-choice`→`mc`, TF CV7991→`tf` 4 ý + `correct_answers`, `short-answer`→`short_answer` (đáp án sạch).
- Payload mặc định: `duration: 15`, `exam_format` theo form, `anti_ai_one_by_one: true`, `anti_ai_watermark: true`.
- `startOnlineExam()`: ghi `localStorage.thitructuyen_pending_import`, mở `thitructuyen.html?from=taobaitap`.
- Nút **🚀 THI TRỰC TUYẾN** cạnh **DẠY NGAY** (Bước 2, mode quiz).

### `thitructuyen.html` — tiếp nhận & cấu hình
- `App` + `HybridExamCreator`: đọc pending import → nạp câu hỏi, title, duration 15, cờ anti-AI → `setStep(2)`.
- Nút chọn nhanh thời gian: 15p / 20p / 30p / 45p.
- Checkbox: chế độ cuốn chiếu + watermark bảo mật.
- Khi lưu đề: đưa cờ vào `matrixConfig` (không sửa `api/exam.php`).

### `thitructuyen.html` — làm bài học sinh
- `anti_ai_one_by_one`: chỉ 1 câu/lúc, đồng hồ từng câu `floor(duration*60/n)`, nút **Câu tiếp theo** / **Nộp bài**, không quay lại.
- Tiến trình `currentQuestionIdx` + answers lưu `localStorage` theo `examId` (F5 vẫn đúng câu).
- `anti_ai_watermark`: lớp chữ chìm xoay -25° (họ tên / SBD / lớp / thời gian).

### Tests
- Mới: `tests/taobaitap-thitructuyen-bridge-smoke.js`.

## Test đã chạy

- `node tests/taobaitap-thitructuyen-bridge-smoke.js` — PASS
- `node tests/cv7991-taobaitap-thitructuyen-sync-smoke.js` — PASS
- `node tests/taobaitap-plan-smoke.js` — PASS

Không đổi prompt AI / `api/exam.php` / logic chấm CV 7991. Cần `/verify` trên Antigravity.
