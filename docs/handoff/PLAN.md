# PLAN: Ngừng theo dõi và loại bỏ các file rác trong TROLYTHIEN khỏi GitHub & Hosting

## Hiện trạng
1. Thư mục `TROLYTHIEN/` chứa nhiều file dữ liệu tạm, file scan độ phân giải cao (`page_*.png` ~8MB), thư mục ảnh trích xuất (`extracted_img/`, `figures/`), file PDF (`HH.pdf`), và tài liệu DOCX (`yeucau.docx`).
2. Trong commit `d5f1699`, các file này đã bị `git add` và commit lên kho GitHub do trong `.gitignore` chưa khai báo loại trừ thư mục `TROLYTHIEN/`.
3. Mặc dù `.github/workflows/ftp-deploy.yml` đã có cấu hình `TROLYTHIEN/**` chặn đẩy lên hosting (đã kiểm chứng thực tế trả về 404), việc lưu trữ các file rác này trên GitHub làm phình to dung lượng repository và tiềm ẩn nguy cơ vô tình lọt file nhạy cảm/dữ liệu tạm lên mạng.

## Phạm vi thực hiện
1. Cấu hình `.gitignore`:
   - Bổ sung cấu hình bỏ qua thư mục `TROLYTHIEN/` (đặc biệt là các thư mục dữ liệu đầu vào và kết quả trung gian `Dau_vao/`, `Ket_qua/`).
   - Đảm bảo git không tự động stage bất kỳ file tài liệu, PDF, hình ảnh nào trong `TROLYTHIEN/` trong các lần commit sau.
2. Dọn dẹp Git Tracking:
   - Thực hiện `git rm -r --cached` đối với `TROLYTHIEN/` để hủy theo dõi trên Git nhưng **giữ nguyên toàn bộ tệp tin trên máy tính cá nhân**.
3. Củng cố workflow deploy `.github/workflows/ftp-deploy.yml`:
   - Đảm bảo mẫu loại trừ bao quát cả `TROLYTHIEN/**` và `**/TROLYTHIEN/**`.

## Ngoài phạm vi
- Không xóa bất kỳ file dữ liệu vật lý nào trong thư mục `TROLYTHIEN/` trên ổ đĩa máy tính.
- Không sửa đổi mã nguồn các công cụ nghiệp vụ hoặc giao diện web.

## File dự kiến tác động
- `.gitignore`
- `.github/workflows/ftp-deploy.yml`
- Git index (cache tracking của repo)
- `docs/handoff/IMPLEMENT.md`

## Các bước thực hiện chi tiết cho Coder
1. **Bước 1: Cập nhật `.gitignore`:**
   - Mở file `.gitignore`, thêm vào cuối:
     ```gitignore
     # Trợ lý Thiên (Dữ liệu tạm & kết quả trích xuất đề/giáo án)
     TROLYTHIEN/
     ```
2. **Bước 2: Hủy theo dõi file trong Git index:**
   - Chạy lệnh git:
     ```bash
     git rm -r --cached TROLYTHIEN/
     ```
   - Chạy `git status` để xác nhận các file chuyển sang trạng thái untracked và staged for deletion.
3. **Bước 3: Tinh chỉnh `.github/workflows/ftp-deploy.yml`:**
   - Kiểm tra danh sách `exclude`, đảm bảo có cả:
     ```yaml
            TROLYTHIEN/**
            **/TROLYTHIEN/**
     ```
4. **Bước 4: Ghi nhật ký vào `docs/handoff/IMPLEMENT.md`:**
   - Báo cáo chi tiết các thao tác đã thực hiện và trạng thái git.

## Kế hoạch kiểm thử (Verification)
1. Chạy `git status` để xác nhận:
   - Các file trong `TROLYTHIEN/` không còn nằm trong staged index để track lại.
   - Thư mục `TROLYTHIEN/` bị `.gitignore` bỏ qua hoàn toàn.
2. Kiểm tra lại hệ thống thư mục cục bộ `TROLYTHIEN/` để chắc chắn không mất file làm việc nào của người dùng.
