# PLAN: Khảo sát nguyên nhân không push được và Phương án xử lý xung đột Git (Merge Conflicts)

## Hiện trạng
1. **Lý do không push được**:
   - Nhánh cục bộ (`main`) và nhánh từ xa (`origin/main`) bị **phân nhánh (diverged)**:
     + Nhánh local có **1 commit mới** (`8b98de5` lúc 21:44:23) được commit tại máy.
     + Nhánh remote (`origin/main`) có **6 commit khác** (`9b5b0ce` đến `2a5aad8`) đã được đẩy lên GitHub trước đó cùng ngày.
   - Do có sự phân nhánh, GitHub Desktop đã thực hiện lệnh `Pull origin` để đồng bộ. Khi Git thực hiện thao tác kéo hợp nhất (`git merge origin/main`), cả hai bên đều sửa đổi sâu trên cùng một nhóm file lõi về Quản lý văn bản.
   - Hậu quả: Git rơi vào trạng thái xung đột tại **10 file (unmerged paths)**:
     1. `api/vanban.php` (7 conflicts)
     2. `docs/handoff/IMPLEMENT.md` (1 conflict)
     3. `docs/handoff/PLAN.md` (1 conflict)
     4. `docs/handoff/VERIFY.md` (1 conflict)
     5. `quanlyvanban-chuyenmon.html` (11 conflicts)
     6. `quanlyvanban-dang.html`
     7. `quanlyvanban-hanhchinh.html`
     8. `quanlyvanban.html`
     9. `vanban-app.js`
     10. `vanban-hub.js`
   - **Vì Git đang ở trạng thái `MERGING` dở dang với các file unmerged**, Git tuyệt đối **chặn mọi thao tác `git push`** (và cả `git pull`). Trên GitHub Desktop, nút Push bị vô hiệu hóa và hiển thị modal bắt buộc *"Resolve conflicts before Merge"*.

2. **Nội dung công việc giữa 2 bên bị đụng độ**:
   - **Nhánh Local (`8b98de5`)**:
     + Bổ sung chế độ xem công khai không cần đăng nhập cho cấp trên / khách kiểm tra (`access-control.js`, `api/vanban.php` với `vbd_optional_user`, giao diện ẩn nút thêm/sửa/xóa).
     + Nút "Lấy từ Hành chính" ở trang Chuyên môn (`quanlyvanban-chuyenmon.html`).
   - **Nhánh Remote (`origin/main`)**:
     + Đã hoàn thành các commit pipeline tự động giữ nguyên văn bản gốc tại Hành chính khi chuyển sang Chuyên môn.
     + Nhận diện chữ ký số PDF, trích xuất OCR.
     + Bổ sung các bài test tự động (`tests/vanban-chuyenmon-root-smoke.py`, `tests/vanban-chuyenmon-signature-smoke.js`, `tests/vanban-display-saved-smoke.js`, `tests/sodiem-smoke.js`).
     + Bổ sung skills và rules chuẩn hóa văn bản NĐ 30 / VPTW.

---

## Phạm vi
1. Xử lý triệt để toàn bộ xung đột trên 10 file đang bị unmerged.
2. Hợp nhất (merge) đầy đủ các cải tiến của cả 2 phía:
   - Giữ chế độ xem công khai (khách không cần đăng nhập vẫn xem và tải được văn bản/tệp) từ nhánh Local.
   - Giữ nguyên toàn bộ logic chuẩn hóa giữ bản gốc Hành chính, nhận diện ký số và bộ kiểm thử tự động từ nhánh Remote.
3. Hoàn tất commit merge để đưa Git về trạng thái sạch sẽ (`clean working directory`).
4. Đẩy thành công (`git push origin main`) toàn bộ lịch sử commit lên GitHub.

---

## Ngoài phạm vi
- Không mở rộng tính năng mới ngoài việc hòa giải xung đột của 2 nhánh.
- Tuyệt đối không dùng `git push --force` vì sẽ làm mất 6 commit quan trọng trên GitHub.
- Không sửa mã nguồn trong phiên khảo sát Antigravity IDE (tuân thủ quy tắc Planner trong `AGENTS.md`).

---

## File dự kiến tác động
1. `api/vanban.php`: Hòa giải hàm `vbd_optional_user` (cho phép xem văn bản không cần login) với các hàm xử lý chuyển/sao chép văn bản mới (`vbd_copy_local_storage`, `transfer_sector`, `copy_sector`).
2. `vanban-app.js`: Giữ chế độ Guest Mode (khách xem công khai) đồng thời tích hợp các hàm chuyển/sao chép và nhãn thông báo giữ bản gốc.
3. `quanlyvanban-chuyenmon.html`: Giữ cấu trúc hoàn chỉnh của trang Chuyên môn (bao gồm các modal, nút xem công khai và nút quản lý khi đăng nhập).
4. `quanlyvanban-hanhchinh.html`, `quanlyvanban-dang.html`, `quanlyvanban.html`: Giữ liên kết 3 phân hệ và nút đăng nhập cho khách.
5. `vanban-hub.js`: Giữ cấu hình 3 sector và thống kê chuẩn.
6. `docs/handoff/PLAN.md`, `docs/handoff/IMPLEMENT.md`, `docs/handoff/VERIFY.md`: Giải quyết conflict tài liệu handoff.

---

## Các bước thực hiện
*Dành cho Coder (Grok / ChatGPT / `agy` CLI):*

1. **Bước 1: Tiếp nhận và chuẩn bị**:
   - Xóa file `docs/handoff/.lock`.
   - Xem danh sách các file conflict bằng `git status`.

2. **Bước 2: Xử lý xung đột mã nguồn**:
   - **`api/vanban.php`**:
     + Giữ lại hàm `vbd_optional_user($pdo)` để cho phép `action=list`, `action=file`, `action=reminder_count` hoạt động khi khách chưa đăng nhập.
     + Giữ lại các hàm xử lý mới nhất từ remote: `vbd_copy_local_storage`, `vbd_copy_document_files`, logic không xóa file Google Drive dùng chung trong `vbd_delete_document_file_storage`.
     + Hỗ trợ cả 2 chiều: Action `copy_from_hanhchinh` (lấy từ Hành chính) và `transfer_sector` / `copy_sector` (đẩy sang Chuyên môn giữ bản gốc).
   - **`vanban-app.js`**:
     + Kết hợp logic kiểm tra đăng nhập / chế độ khách: Khi `is_guest === true`, ẩn các nút sửa/xóa/thêm văn bản.
     + Giữ lại các hàm xử lý nút sao chép và chuyển giao diện từ remote.
   - **`quanlyvanban-chuyenmon.html`**:
     + Loại bỏ hoàn toàn các thẻ đánh dấu conflict (`<<<<<<<`, `=======`, `>>>>>>>`).
     + Giữ giao diện hoàn chỉnh có cả thanh điều hướng 3 tab, bộ lọc và các modal.
   - **`quanlyvanban-hanhchinh.html`, `quanlyvanban-dang.html`, `quanlyvanban.html`, `vanban-hub.js`**:
     + Chọn phiên bản hợp nhất, loại bỏ conflict markers.
   - **Các file tài liệu `docs/handoff/*`**:
     + Chấp nhận nội dung kế hoạch và xác minh mới nhất, không để lại conflict markers.

3. **Bước 3: Kiểm tra chất lượng và chạy test suite**:
   - Kiểm tra cú pháp JavaScript:
     ```powershell
     node --check vanban-app.js vanban-hub.js access-control.js
     ```
   - Chạy các kịch bản smoke test:
     ```powershell
     py tests/vanban-chuyenmon-root-smoke.py
     node tests/vanban-chuyenmon-signature-smoke.js
     node tests/sodiem-smoke.js
     ```
   - Xác nhận tất cả test đạt trạng thái PASS (exit code 0).

4. **Bước 4: Hoàn thành merge và commit**:
   - Đánh dấu đã giải quyết conflict:
     ```powershell
     git add .
     ```
   - Kiểm tra `git status` đảm bảo không còn dòng `both modified` hay `unmerged`.
   - Hoàn tất merge commit:
     ```powershell
     git commit -m "Merge origin/main into main: Resolve conflicts between public guest access and root preservation"
     ```

5. **Bước 5: Ghi nhận và bàn giao**:
   - Ghi nội dung đã làm vào `docs/handoff/IMPLEMENT.md`.
   - Tạo lại file `docs/handoff/.lock` với nội dung `LOCK`.

6. **Bước 6: Xác minh và Push**:
   - Báo User mở Antigravity IDE gõ `/verify`.
   - Sau khi IDE xác nhận PASS: Coder thực hiện `git push origin main` và xóa file `docs/handoff/.lock`.

---

## Rủi ro
- Bỏ sót conflict markers (`<<<<<<< HEAD`, `=======`, `>>>>>>>`) dẫn đến lỗi cú pháp PHP hoặc JavaScript khi chạy trên trình duyệt / server.
- Ghi đè nhầm hàm xử lý file đính kèm làm mất tệp khi sao chép văn bản giữa Hành chính và Chuyên môn.
- *Biện pháp giảm thiểu*: Bắt buộc chạy `node --check` và script kiểm thử `tests/vanban-chuyenmon-root-smoke.py` trước khi commit merge.

---

## Cách kiểm thử
1. `git status`: Phải hiển thị nhánh sạch (clean working tree), không còn `Unmerged paths`.
2. Kiểm tra cú pháp: Không có lỗi SyntaxError trên các file JS.
3. Chạy `py tests/vanban-chuyenmon-root-smoke.py` → Kết quả 27/27 PASS.
4. Chạy `node tests/vanban-chuyenmon-signature-smoke.js` → PASS.
5. Thao tác `git push origin main` thành công, remote cập nhật commit mới nhất.

---

## Tiêu chí nghiệm thu
1. 10 file bị xung đột được giải quyết dứt điểm, không còn conflict marker nào trong mã nguồn.
2. Trạng thái `MERGING` kết thúc bằng một merge commit hợp lệ.
3. Tính năng xem công khai (khách) và tính năng bảo toàn bản gốc Hành chính đều hoạt động tốt.
4. `git push origin main` hoàn tất thành công lên GitHub không báo lỗi.
