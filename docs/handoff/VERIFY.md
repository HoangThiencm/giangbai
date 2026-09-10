# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- **Tôn trọng lựa chọn model trực tiếp (Direct Model Selection)**:
  - `app.js`: Hàm `resolveDrawingRequestModel()` đã được sửa để khi `#ai-model-select` có giá trị cụ thể (khác `FOLLOW_SYSTEM_MODEL`), hệ thống trả về đúng 100% model người dùng đã chọn (ví dụ: `gemini-2.5-flash`), không bị `DEPRECATED_DRAWING_MODELS` ghi đè về `gemini-3.7-flash`.
  - Mảng `DEPRECATED_DRAWING_MODELS` chỉ còn chứa các mã model thực sự đã bị Google khai tử (`gemini-1.5-flash`, `gemini-1.0-pro`).
  - Dòng trạng thái `analysisOutput` hiển thị chuẩn xác: `AI đang phân tích bằng Gemini · gemini-2.5-flash...`.
- **Tối ưu hóa độ trễ & Tốc độ gọi AI**:
  - `api/vehinh_ai.php`:
    + Timeout cURL trong `vehinh_post_json` giảm từ 90s xuống **30 giây**.
    + Danh sách ứng viên `$modelCandidates` rút gọn tối đa **2–3 model** (Model người dùng chọn → Fallback người dùng chọn → Tối đa 1 safe fallback `gemini-3.6-flash`), không còn duyệt toàn bộ 7 model.
    + Bổ sung cơ chế Fast-fail (ngắt nhanh): Khi gặp lỗi cấp Model (HTTP 400, 404, hoặc `"no longer available"` / `"not supported"`), backend lập tức ngắt vòng lặp key để chuyển sang model kế tiếp trong 1–2 giây, không thử lại các key khác với model lỗi.
    + `maxOutputTokens` tối ưu về **8192**.
  - `app.js`: `waitForAiThrottle` giảm ngưỡng xuống 1000ms, không còn delay nhân tạo 2–3s trước mỗi lượt vẽ.

## Test đã chạy
1. `node tests/game-quiz-importer-smoke.js`:
   - Kiểm tra khi chọn `gemini-2.5-flash`, `resolveDrawingRequestModel` trả về đúng `'gemini-2.5-flash'`: PASS.
   - Kiểm tra timeout cURL 30s và candidate list rút gọn: PASS.
   - Kiểm tra Fast-fail khi gặp 400/404: PASS.
2. `node tests/run-all-tests.js`:
   - Toàn bộ **66/66 test suites** đều vượt qua thành công 100% (PASS).

## Pass / Fail từng tiêu chí
1. Chọn trực tiếp model (như Gemini 2.5 Flash) được hệ thống tôn trọng 100%, gửi đúng lên API và hiển thị đúng trên giao diện: **PASS**
2. Khắc phục triệt để tình trạng "chạy rất lâu": timeout giảm còn 30s, candidate giới hạn 2-3 model, fast-fail ngắt nhanh khi model lỗi: **PASS**
3. Toàn bộ 66/66 test suites trong hệ thống đều PASS 100%: **PASS**

## Bug
- Không có (None).
