# IMPLEMENT

## Đã thực hiện

- Cập nhật Stepper trên cả hai bản Canvas thành giao diện 3 bước: các khối logic `data-step="3"` và `data-step="4"` vẫn được giữ nguyên, nhưng hiển thị lần lượt số `2` và `3`.
- Đặt `aria-label` của Stepper là `Quy trình 3 bước soạn KHBD`; đồng bộ nhãn bước trong bản sao lưu để khớp giao diện chính.
- Nâng cache-busting của các mô-đun Canvas từ `20260916-canvas-module-v8` lên `20260916-canvas-module-v9`.
- Cập nhật hai smoke test để yêu cầu phiên bản v9 và xác nhận Stepper vừa giữ `data-step` cũ vừa hiển thị 1–2–3.
- Thêm comment triển khai `20260916-textbook-exact-v15` vào `js/khbd-prompts.js` để workflow FTP Deploy tải lại tệp đầy đủ lên hosting.
- Bảo vệ riêng lời gọi trong `analyzeCanvasTextbookSafely`: nếu `getSystemRole` chưa sẵn sàng, dùng `window.getSystemRole` khi có hoặc chuỗi rỗng để OCR không bị `ReferenceError`.
- Cập nhật cả hai trang Canvas dùng `khbd-prompts.js?v=20260916-textbook-exact-v15` và đặt fallback stub `window.getSystemRole` trước khi nạp `khbd-app.js`.
- Sửa lỗi từ `VERIFY.md`: đổi duy nhất `KHBD_CURRICULUM_DEPLOY_VERSION` từ `canvas-module-v8` sang `canvas-module-v9`, tạo git diff để FTP Deploy tải lại curriculum 173.676 byte.

## Hosting

Đã đổi `KHBD_CURRICULUM_DEPLOY_VERSION` trong `js/khbd-curriculum.js` từ `canvas-module-v8` sang `canvas-module-v9`. Tệp cục bộ có 173.676 byte; thay đổi này bảo đảm workflow `.github/workflows/ftp-deploy.yml` nhận diện tệp và tải lại nó lên `hoangthiencm.id.vn` khi thay đổi được commit và push theo quy trình dự án.

## Kiểm thử

- Kiểm tra tĩnh: không còn chuỗi phiên bản v8 hoặc `aria-label` 4 bước trong hai trang Canvas; diff không có lỗi khoảng trắng (`git diff --check`).
- `python C:\Users\HoangThien\.gemini\antigravity\brain\7ddd6240-4311-4b35-b755-f9a3e9f49765\scratch\test_verify.py`: PASS cho cả hai trang Canvas.
- `python C:\Users\HoangThien\.gemini\antigravity\brain\7ddd6240-4311-4b35-b755-f9a3e9f49765\scratch\verify_all.py`: ALL CHECKS PASSED sau khi đổi curriculum sang v9.
- `node tests/canvas-soankhbd-smoke.js`: không chạy được vì Windows Security chặn `node.exe` của runtime với thông báo tệp có thể là virus/PUA.

Không commit. `docs/handoff/PLAN.md` không bị sửa thêm.
