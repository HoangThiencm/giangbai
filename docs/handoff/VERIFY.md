# VERIFY

## Kết luận
PASS

## Đối chiếu scope
1. **Modal Cài đặt Model Gemini trong `phancongtochuyenmon.html`**:
   - Thêm modal `#gemini-model-modal` với danh sách lựa chọn: `gemini-2.5-flash`, `gemini-2.5-pro`, `gemini-1.5-flash`, `gemini-3.7-flash`, `gemini-3-flash-preview` và hỗ trợ ô nhập model tùy chỉnh (`cfg-gemini-model-custom`). -> ĐẠT
   - Thêm nút mở modal kèm nhãn `#tt-active-model-label` ngay trên thẻ Nhập ảnh Thời khóa biểu (cạnh nút Khung tiết). -> ĐẠT
   - Hàm `getTimetableGeminiModel()` đọc theo thứ tự ưu tiên: `phancong_gemini_model` -> `gemini_model` -> `state.info.gemini_model` -> mặc định `gemini-2.5-flash`. -> ĐẠT
   - Hàm `saveGeminiModelConfig()` lưu vào cả hai khóa `localStorage`, cập nhật nhãn giao diện và hiển thị thông báo toast. -> ĐẠT
   - Hàm `scanTimetableWithAI()` lấy model động từ `getTimetableGeminiModel()`, không còn bị hardcode. -> ĐẠT
   - Hàm `renderTimetableView()` tự động cập nhật nhãn model đang kích hoạt khi chuyển sang tab TKB. -> ĐẠT

2. **Chống trùng lặp & Đa dạng hóa câu hỏi trong `taobaitap.html`**:
   - `GeminiModule.callGeminiParts` đã tiếp nhận `options.generationConfig` và gửi kèm trong payload gọi Gemini API. -> ĐẠT
   - `generateContent` sinh mã biến thể ngẫu nhiên (`variantNonce`), thu thập danh sách câu hỏi cũ của lần tạo trước để chỉ thị AI bắt buộc không lặp lại nội dung/ngữ cảnh cũ, đồng thời truyền `generationConfig: { temperature: 0.9, topP: 0.95 }`. -> ĐẠT

## Test đã chạy
- `node tests/timetable-render-smoke.js`: PASS
  + Xác nhận modal `#gemini-model-modal`, hàm `openGeminiModelModal`, `getTimetableGeminiModel`, `saveGeminiModelConfig`.
  + Xác nhận `scanTimetableWithAI` không còn hardcode `gemini-2.5-flash`.
  + Xác nhận đọc và ghi nhớ model đã lưu trong `localStorage`.
- `node tests/taobaitap-diversity-smoke.js`: PASS
  + Xác nhận `generationConfig` trong `callGeminiParts`.
  + Xác nhận prompt chống trùng và cú pháp Babel hợp lệ.
- `node tests/baogiang-mail-smoke.js`: PASS
- `node tests/baogiang-teacher-month-smoke.js`: PASS

## Pass / Fail từng tiêu chí
1. Thêm modal cài đặt module Gemini trong Quản lý tổ chuyên môn: PASS
2. Giao diện trực quan cho phép chuyển đổi model trước khi quét TKB: PASS
3. Động hóa model trong lệnh gọi API: PASS
4. Đa dạng hóa đề và chống trùng lặp câu hỏi từ PDF trong Tạo bài tập: PASS
5. Toàn bộ test suite liên quan: PASS

## Bug
Không phát hiện bug mới.
