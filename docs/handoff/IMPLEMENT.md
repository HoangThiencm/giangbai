# IMPLEMENT: Chọn model Gemini khi nhận diện Thời khóa biểu

## Đã làm
- `phancongtochuyenmon.html`: modal `#gemini-model-modal` với `gemini-2.5-flash`, `gemini-2.5-pro`, `gemini-1.5-flash`, `gemini-3.7-flash`, `gemini-3-flash-preview` và ô model tùy chỉnh.
- Tab Thời khóa biểu GV, cạnh nút Khung tiết: nút mở modal, nhãn `#tt-active-model-label` mặc định `2.5 Flash`.
- `getTimetableGeminiModel()` đọc `phancong_gemini_model`, rồi `gemini_model`, rồi `state.info.gemini_model`, mặc định `gemini-2.5-flash`.
- `saveGeminiModelConfig()` lưu cả hai khóa localStorage, cập nhật nhãn và báo `Đã lưu model AI`.
- `scanTimetableWithAI()` gửi `model: activeModel` từ `getTimetableGeminiModel()`. `renderTimetableView()` cập nhật nhãn khi mở tab.
- `tests/timetable-render-smoke.js`: có modal và các hàm; thân hàm quét TKB không còn hardcode `gemini-2.5-flash`; model đã lưu được đọc lại.

## Kiểm thử
- `node tests/timetable-render-smoke.js` → PASS.

## Chưa kiểm trên trình duyệt
- Chưa bấm mở modal, lưu model rồi xem payload `api/khbd_gemini.php`. Phần đó để `/verify`.
