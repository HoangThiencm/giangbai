# PLAN: Tối ưu hóa Git Tracking cho TROLYTHIEN và Master Rule Nhánh 10

## 1. Hiện trạng & Vấn đề cần xử lý
- Nhánh `10/ Tạo bài giảng HTML (từ PDF)` đã được tích hợp vào `.agents/workflows/thien.md` và `.agents/rules/tro-ly-thien.md`.
- Tuy nhiên, file `.gitignore` dòng 18 hiện đang chặn toàn bộ thư mục `TROLYTHIEN/` (`TROLYTHIEN/`).
- Hậu quả:
  + File `TROLYTHIEN/10_BAI_GIANG_HTML/PROMPT_TAO_BAI_GIANG_HTML.md` và hai file `.gitkeep` không xuất hiện trong Git (`git status` không thấy, `git ls-files` rỗng).
  + Khi người dùng commit/push lên GitHub rồi sang máy khác clone về, thư mục `TROLYTHIEN/` sẽ hoàn toàn biến mất, khiến quy trình tự động trên máy mới không tìm thấy prompt và thư mục.

---

## 2. Giải pháp tối ưu kết hợp (Optimal Combined Solution)
1. **Tinh chỉnh `.gitignore`**:
   - Không ignore thô bạo cả thư mục `TROLYTHIEN/`.
   - Chỉ ignore các file tài liệu dữ liệu nặng do người dùng ném vào (`Dau_vao/*`) hoặc kết quả sinh ra (`Ket_qua/*`), nhưng giữ lại các file `.gitkeep`, file `.md` (prompt/hướng dẫn), và file `.js` (engine).
2. **Tạo Master Rule `.agents/rules/tao-bai-giang-html.md`**:
   - Lưu trữ bản quy chuẩn Master Prompt chính thống vào thư mục `.agents/rules/` (chuẩn kiến trúc như `.agents/rules/taobaocao.md` của nhánh 8 và `.agents/rules/vietsangkien.md` của nhánh 9).
   - Thư mục `.agents/rules/` luôn được Git theo dõi 100%, đảm bảo bất kỳ máy nào clone repo về cũng có sẵn bộ quy chuẩn này vĩnh viễn.
3. **Cập nhật liên kết tham chiếu và Smoke Test**:
   - Trong `.agents/workflows/thien.md` và `.agents/rules/tro-ly-thien.md`, bổ sung tham chiếu đến `.agents/rules/tao-bai-giang-html.md`.
   - Cập nhật `tests/trolythien-bai-giang-html-smoke.js` để kiểm tra cả file rule mới và kiểm tra trạng thái ignore của Git.

---

## 3. Phạm vi & File tác động
| STT | File | Hành động | Chi tiết |
| :--- | :--- | :--- | :--- |
| 1 | `.gitignore` | Sửa đổi | Thay `TROLYTHIEN/` bằng luật chi tiết giữ lại `.gitkeep`, `*.md`, `*.js` |
| 2 | `.agents/rules/tao-bai-giang-html.md` | Tạo mới | Chứa Master Prompt và 7 điểm vá thực chiến chuẩn kiến trúc |
| 3 | `.agents/rules/tro-ly-thien.md` | Sửa đổi | Thêm liên kết tham chiếu tới `.agents/rules/tao-bai-giang-html.md` |
| 4 | `.agents/workflows/thien.md` | Sửa đổi | Thêm liên kết tham chiếu tới `.agents/rules/tao-bai-giang-html.md` |
| 5 | `tests/trolythien-bai-giang-html-smoke.js` | Sửa đổi | Kiểm tra `.agents/rules/tao-bai-giang-html.md` và kiểm tra rule gitignore |

---

## 4. Các bước thực hiện chi tiết cho Coder
*(Dành cho Coder: Grok / ChatGPT / `agy` CLI)*

### Bước 1: Chuẩn bị
- Đọc kỹ `docs/handoff/PLAN.md`.
- Xóa file `docs/handoff/.lock` nếu có.

### Bước 2: Tinh chỉnh `.gitignore`
Tại dòng 17-18 của `.gitignore`, thay thế:
```gitignore
# Trợ lý Thiên (Dữ liệu tạm & kết quả trích xuất đề/giáo án)
TROLYTHIEN/
```
Bằng:
```gitignore
# Trợ lý Thiên: Bỏ qua dữ liệu nạp vào và kết quả sinh ra, giữ lại hướng dẫn và cấu trúc thư mục
TROLYTHIEN/**/Dau_vao/*
!TROLYTHIEN/**/Dau_vao/.gitkeep
!TROLYTHIEN/**/Dau_vao/*.md
TROLYTHIEN/**/Ket_qua/*
!TROLYTHIEN/**/Ket_qua/.gitkeep
!TROLYTHIEN/**/*.md
!TROLYTHIEN/**/*.js
```

### Bước 3: Tạo file `.agents/rules/tao-bai-giang-html.md`
Sao chép toàn bộ nội dung Master Prompt từ `TROLYTHIEN/10_BAI_GIANG_HTML/PROMPT_TAO_BAI_GIANG_HTML.md` sang `.agents/rules/tao-bai-giang-html.md` với tiêu đề chuẩn:
`# QUY CHUẨN SOẠN BÀI GIẢNG HTML TRÌNH CHIẾU TƯƠNG TÁC (NHÁNH 10)`

### Bước 4: Cập nhật tham chiếu trong `tro-ly-thien.md` và `thien.md`
- Trong `.agents/workflows/thien.md` (Nhánh 10):
  Thêm dòng tham chiếu:
  `- Tuân thủ quy chuẩn riêng tại: .agents/rules/tao-bai-giang-html.md`
- Trong `.agents/rules/tro-ly-thien.md` (Mục 4 & 5):
  Bổ sung tham chiếu: `.agents/rules/tao-bai-giang-html.md`.

### Bước 5: Cập nhật và chạy Smoke test
- Sửa `tests/trolythien-bai-giang-html-smoke.js`:
  + Kiểm tra file `.agents/rules/tao-bai-giang-html.md` tồn tại và đầy đủ từ khóa.
  + Kiểm tra `TROLYTHIEN/10_BAI_GIANG_HTML/PROMPT_TAO_BAI_GIANG_HTML.md` tồn tại.
- Chạy kiểm thử:
  ```powershell
  node tests/trolythien-bai-giang-html-smoke.js
  ```
- Kiểm tra `git status`: Các file `PROMPT_TAO_BAI_GIANG_HTML.md` và `.gitkeep` phải xuất hiện trong trạng thái của Git.

### Bước 6: Hoàn tất bàn giao
- Ghi nhận vào `docs/handoff/IMPLEMENT.md`.
- Khởi tạo `docs/handoff/VERIFY.md`.

---

## 5. Tiêu chí nghiệm thu (Verify Checklist)
- [ ] File `.gitignore` cho phép Git theo dõi các file `.md`, `.js`, `.gitkeep` trong `TROLYTHIEN/`.
- [ ] `git status` nhìn thấy `TROLYTHIEN/10_BAI_GIANG_HTML/PROMPT_TAO_BAI_GIANG_HTML.md` và các file `.gitkeep`.
- [ ] File `.agents/rules/tao-bai-giang-html.md` tồn tại và đồng bộ nội dung Master Prompt.
- [ ] Thử nghiệm: File giả lập `.pdf` trong `Dau_vao/` vẫn bị `.gitignore` chặn (không lọt vào Git).
- [ ] `node tests/trolythien-bai-giang-html-smoke.js` đạt PASS (exit code 0).
