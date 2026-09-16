# IMPLEMENT

## Đã thực hiện

- Cập nhật Stepper trên cả hai bản Canvas thành giao diện 3 bước: các khối logic `data-step="3"` và `data-step="4"` vẫn được giữ nguyên, nhưng hiển thị lần lượt số `2` và `3`.
- Đặt `aria-label` của Stepper là `Quy trình 3 bước soạn KHBD`; đồng bộ nhãn bước trong bản sao lưu để khớp giao diện chính.
- Nâng cache-busting của các mô-đun Canvas từ `20260916-canvas-module-v8` lên `20260916-canvas-module-v9`.
- Cập nhật hai smoke test để yêu cầu phiên bản v9 và xác nhận Stepper vừa giữ `data-step` cũ vừa hiển thị 1–2–3.

## Hosting

Tệp cục bộ `js/khbd-curriculum.js` đã được xác nhận có 173.676 byte. Không có thông tin xác thực FTP trong workspace, nên chưa thể re-upload trực tiếp lên `hoangthiencm.id.vn`; workflow `.github/workflows/ftp-deploy.yml` sẽ tải tệp này khi thay đổi được triển khai qua quy trình CI hiện có.

## Kiểm thử

- Kiểm tra tĩnh: không còn chuỗi phiên bản v8 hoặc `aria-label` 4 bước trong hai trang Canvas; diff không có lỗi khoảng trắng (`git diff --check`).
- Hai smoke test đã được gọi nhưng chưa chạy được: Windows Security chặn `node.exe` của runtime với thông báo tệp có thể là virus/PUA. Cần chạy lại sau khi runtime Node được cho phép:
  - `node tests/canvas-module-fallback-smoke.js`
  - `node tests/canvas-soankhbd-smoke.js`

Không commit. `docs/handoff/PLAN.md` không bị sửa thêm.
