# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Đã thêm công cụ Nghiên cứu bài học vào `index.html`: `TOOL_PAGE_LINKS.nghiencuubaihoc = 'nghiencuubaihoc.html'`, thẻ `tool-tile--nghiencuubaihoc` hiển thị trên `#mainToolsGrid` với icon `fa-users-rectangle`, tiêu đề "Nghiên cứu bài học AI", nhãn "Chu trình NCBH sư phạm".
- Đã tích hợp cấu hình và phân quyền trong `admin.html`: `cfg_nghiencuubaihoc`, `CLIENT_FEATURE_CHECKS`, `USER_FEATURE_GROUPS`, `teacherFeatureGroups`.
- Đã cấp phép định tuyến trong `access-control.js` và `api/helpers.php` cùng cờ mặc định trong `global_config.json`.
- Đã xây dựng trọn vẹn `nghiencuubaihoc.html`:
  + Đủ 12 bước chu trình NCBH theo đúng tài liệu đặc tả.
  + Cấu trúc thống nhất 6 khu vực trong từng bước (Căn cứ, AI phân tích, GV cần làm, HS dự kiến làm, Cần quan sát/thu thập, Sản phẩm của bước).
  + Tách biệt 12 tác vụ AI chuyên sâu (Document Analyzer, Lesson Analyzer, Lesson Plan Reviewer, Research Question Advisor, Student Thinking Predictor, Lesson Adaptation Advisor, Observation Designer, Evidence Analyzer, Discussion Assistant, Minutes Generator, Lesson Reviser, Report Generator).
  + Thiết kế KHBD 2 lớp (Lớp 1: KHBD chuẩn CV 5512, Lớp 2: Thông tin NCBH).
  + Cơ chế AI đa tầng: đồng bộ API key từ CSDL qua `api/user_gemini_keys.php` (Gemini & Mistral AI), đọc model Gemini từ cấu hình người dùng (`default_gemini_module` / `khbd_gemini_model`), tích hợp Mistral OCR cho tài liệu scan và Mistral Chat Completion dự phòng, hỗ trợ xoay vòng key, xử lý lỗi 429/503/timeout.
  + Tích hợp Kho căn cứ chuyên môn (CV 5512, TT 32/2018, QĐ 2422 Khung AI, CV 3456 NLS, TT 38/2021, TT 14/2020).
  + Quản lý phiên hồ sơ và lưu trữ kép: API backend `api/nghiencuubaihoc.php` (bảng `nghien_cuu_bai_hoc_sessions`), tự động lưu (auto-save) và đệm vào `localStorage`.
  + Xuất Word (.docx) và đóng gói (.zip) cho trọn bộ 13 sản phẩm/biểu mẫu hồ sơ NCBH.
- Không sửa source các file ngoài phạm vi (`soankhbd.html`, `xaydungphuluc.html`, `duyetgiaoan.html`, `duyetde.html`).
- File khóa handoff `docs/handoff/.lock` được giữ nguyên vẹn.

## Test đã chạy
1. `node tests/nghiencuubaihoc-smoke.js` -> PASS
2. `node tests/xaydungphuluc-integration-smoke.js` -> PASS
3. `node tests/duyetgiaoan-integration-smoke.js` -> PASS
4. `node tests/duyetgiaoan-smoke.js` -> PASS
5. `node tests/user-ai-settings-smoke.js` -> PASS
6. `node tests/security-f12-smoke.js` -> PASS

## Pass / Fail từng tiêu chí
1. `index.html` có thẻ công cụ "Nghiên cứu bài học" trỏ đến `nghiencuubaihoc.html` và hiển thị đồng bộ: PASS
2. `admin.html` có tùy chọn cấp quyền và hiển thị trang `nghiencuubaihoc`: PASS
3. `api/nghiencuubaihoc.php` hoạt động trơn tru: tự tạo bảng `nghien_cuu_bai_hoc_sessions`, lưu và khôi phục toàn vẹn dữ liệu hồ sơ (list, get, save, delete): PASS
4. `nghiencuubaihoc.html` hiện thực hóa đầy đủ 12 bước NCBH, cấu trúc 6 khu vực thống nhất, 12 tác vụ AI chuyên biệt, mô hình KHBD 2 lớp, lưu trữ nhật ký phát triển bài học: PASS
5. Tích hợp đọc API key (Gemini & Mistral) từ CSDL qua `api/user_gemini_keys.php` và đọc model được người dùng chọn: PASS
6. Hỗ trợ xuất file Word (.docx) chuẩn thể thức và xuất .zip cho 13 sản phẩm hồ sơ NCBH: PASS
7. File kiểm thử `tests/nghiencuubaihoc-smoke.js` chạy PASS 100%: PASS
8. Không phát sinh hồi quy (regression) trên các bài kiểm thử liên quan: PASS

## Bug
Không phát hiện lỗi.