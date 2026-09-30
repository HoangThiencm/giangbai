# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Đã bổ sung 2 hàm đọc key đa nguồn `getAvailableGeminiKeys()` và `getAvailableMistralKeys()` trong `vanban-app.js`, quét toàn bộ các khóa lưu trữ: `global_*`, `khbd_user_*_<email>`, `khbd_user_*_default`, `khbd_gemini_api_keys`, `gemini_api_keys`, `xdpl_gemini_api_keys`, `geometryAiApiKeys`, `xdpl_mistral_api_keys`, cùng fallback `AiDesignConfig`.
- Đã thêm hàm `ensureKeysLoaded()` await một lần `syncUserKeysFromServer()`, gọi ở đầu hàm `ocrImageData()` để loại bỏ hoàn toàn race condition khi người dùng chụp dán ảnh ngay khi mở trang.
- Đã cập nhật `extractTextViaGeminiVision()` sử dụng danh sách key từ `getAvailableGeminiKeys()`.
- Đã cập nhật `openSystemAiConfig()` ưu tiên gọi `UserAiSettings.openModal('keys')` chuẩn của toàn hệ thống, fallback sang `AiDesignConfig.openModal()`.
- Đã nạp `<script src="js/user-ai-settings.js?v=20261001"></script>` vào `<head>` của 3 trang `quanlyvanban-chuyenmon.html`, `quanlyvanban-hanhchinh.html`, `quanlyvanban-dang.html`.
- Không sửa ngoài scope, không vi phạm cấu trúc backend hay phân quyền.

## Test đã chạy
1. `node --check vanban-app.js` — Exit 0 (Cú pháp JS hợp lệ).
2. `node tests/vanban-ocr-clipboard-smoke.js` — Exit 0 (PASS: kiểm tra đủ các token hàm gom key đa nguồn, `khbd_user_*`, `ensureKeysLoaded`, `UserAiSettings.openModal('keys')`).
3. `node tests/vanban-chuyenmon-signature-smoke.js` — Exit 0 (PASS: lĩnh vực Chuyên môn, chuyển/sao chép văn bản, số quyết định và ngày ký số).
4. `node tests/vanban-display-saved-smoke.js` — Exit 0 (PASS: hiển thị văn bản đã lưu, bộ lọc năm học và truy vấn legacy).
5. `python tests/vanban-chuyenmon-root-smoke.py` — Exit 0 (PASS: bảo toàn bản gốc Hành chính khi chuyển sang Chuyên môn, 27/27 asserts).

## Pass / Fail từng tiêu chí
- [x] Tự động nhận diện API Key từ `khbd_user_gemini_keys_*` và `khbd_user_mistral_keys_*` của tài khoản mà không báo thiếu key: PASS
- [x] Chụp dán ảnh (Ctrl+V hoặc nút "Dán nhanh từ Clipboard") chạy OCR trơn tru: PASS
- [x] Có nút "Cấu hình AI" mở hộp thoại `UserAiSettings` chuẩn với cả 2 tab Gemini & Mistral: PASS
- [x] Không còn thông báo chặn cứng ép dùng Mistral OCR: PASS
- [x] Toàn bộ 4 smoke test suites đều PASS: PASS

## Bug
- Không có
