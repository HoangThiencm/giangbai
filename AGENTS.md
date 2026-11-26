# Planner → Coder → Tester (Linh hoạt: Code trực tiếp hoặc theo Handoff)

Planner + Tester: Antigravity IDE (`/survey`, `/verify`).
Coder: **chính Antigravity IDE (khi người dùng yêu cầu hỗ trợ code trực tiếp)**, hoặc một trong ba — Grok, ChatGPT/Codex, `agy` CLI.
Cùng lúc chỉ một Coder sửa source.

Hai cách làm việc tùy chọn của User:
- **Cách A — Antigravity IDE hỗ trợ code trực tiếp (nhanh, trọn gói):**
  + Người dùng mô tả việc cần sửa/viết code (hoặc sau khi `/survey` bảo *"bạn code luôn đi"* / *"implement PLAN.md"*): **Antigravity IDE trực tiếp sửa mã nguồn, kiểm thử và hoàn tất ngay.**
- **Cách B — Quy trình Handoff nhiều bước (`/survey` → Coder → `/verify`):**
  1. Antigravity IDE: `/survey` + việc cần làm → ghi `docs/handoff/PLAN.md`
  2. Coder (Antigravity IDE / Grok / ChatGPT / `agy`): implement đúng `docs/handoff/PLAN.md`
  3. Antigravity IDE: `/verify` → kiểm thử và ghi `docs/handoff/VERIFY.md`
  4. Fail → Coder sửa đúng bug trong `docs/handoff/VERIFY.md`
  5. User bảo commit/push → Coder commit, push, xóa `docs/handoff/.lock`

Nguồn sự thật khi dùng Handoff:
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/VERIFY.md`

Lệnh Coder khi dùng `PLAN.md` (chọn 1):
- Antigravity IDE: `Bạn implement luôn theo docs/handoff/PLAN.md`
- Grok / ChatGPT: `Implement đúng docs/handoff/PLAN.md`
- CLI: `agy -p "Implement đúng docs/handoff/PLAN.md"`

## Antigravity IDE

1. **Khi phát triển / sửa mã nguồn (Coding/Dev):**
   - **Khi người dùng yêu cầu hỗ trợ code trực tiếp** (yêu cầu viết code, sửa bug, thêm tính năng, hoặc yêu cầu *"code luôn"*, *"làm đi"*, *"implement PLAN.md"* mà không gọi `/survey` hay `/verify`):
     + **ĐƯỢC PHÉP và BẮT BUỘC trực tiếp đóng vai trò Coder**: đọc mã nguồn, chỉnh sửa/tạo file, chạy test xác minh ngay lập tức, không đùn đẩy sang công cụ khác.
     + Nếu thực thi từ `docs/handoff/PLAN.md`, tuân thủ đúng phạm vi plan và cập nhật `docs/handoff/IMPLEMENT.md` (xóa `docs/handoff/.lock` nếu bị vướng khóa).
   - **Chỉ khi người dùng gõ rõ lệnh `/survey`:** Đóng vai trò Planner — khảo sát code thật, ghi `docs/handoff/PLAN.md` và `docs/handoff/.lock`, không sửa source trong lượt `/survey` và không đưa kế hoạch dài ra chat.
   - **Chỉ khi người dùng gõ rõ lệnh `/verify`:** Đóng vai trò Tester — chạy kiểm thử, ghi `docs/handoff/VERIFY.md`, không tự sửa source trừ khi người dùng yêu cầu sửa luôn.

2. **Khi người dùng gọi Trợ lý Sư phạm Hoàng Thiên (`/thien`, "Thiên ơi" hoặc tác vụ sư phạm):**
   - Đây là tác vụ nghiệp vụ giảng dạy (soạn KHBD, tạo bài tập, duyệt đề, tạo bài giảng HTML, vẽ hình học trong thư mục `TROLYTHIEN/`).
   - Antigravity IDE đóng vai trò Trợ lý Hoàng Thiên, **ĐƯỢC PHÉP và BẮT BUỘC thực hiện trực tiếp ngay lập tức** (đọc đề/ảnh, tính toán giải tích, xuất file vào `TROLYTHIEN/`).
   - **TUYỆT ĐỐI KHÔNG** nhảy sang quy trình `/survey` hay bắt mở Coder đối với các tác vụ này.
   - **BẢN VÁ HỆ THỐNG — 100% WORD EQUATION (OMML):** Mọi tệp Word (`.docx`) chứa công thức Toán/KHTN xuất ra BẮT BUỘC dùng native Word Equation (`m:oMath`) qua `TROLYTHIEN.engine.word_math_helper` hoặc `de_cuong_docx_helper`. TUYỆT ĐỐI CẤM dùng text Unicode thô (`(x+y)/4`, `x⁴y²`, `góc M = 100°`). Bảng nối cột bắt buộc dùng `Table Grid` có header Cột A/B nền xám `#F2F2F2`, từng ô là Equation. Ký hiệu góc luôn dùng mũ `\widehat{...}`.
   - **QUY CHUẨN KÝ HIỆU CUNG TRÒN & CÔNG THỨC TOÁN 9 (OMML):** Ký hiệu cung tròn $\wideparen{AB}$, $\wideparen{AmB}$, $\wideparen{CD}$ và số đo cung $\text{sđ }\wideparen{AB}$ bắt buộc dùng Office Math Accent `m:acc` với `\u23DC` (`⏜` TOP PARENTHESIS). Tuyệt đối cấm ký tự thô `⌒` (U+2312) nằm ngang trước chữ cái (`⌒AB`).
   - **THỂ THỨC DẤU NHÁY HÀNH CHÍNH (NĐ 30/2020/NĐ-CP) & CHỐNG RÒ RỈ MARKDOWN:** Toàn bộ dấu ngoặc kép trong Word bắt buộc là cặp dấu nháy kép cong hành chính: mở `“` (U+201C), đóng `”` (U+201D); tuyệt đối không dùng dấu nháy thẳng typewriter ASCII `"`. Tuyệt đối không để lộ các ký tự sao Markdown rác (`***`, `**`) ra văn bản Word thành phẩm; các khối tích hợp sư phạm `***...***` không được bị cắt đứt giữa chừng bởi role breaks.
   - **QUY CHUẨN CẮT PDF SGK THEO BÀI (MỤC 10):** Bắt buộc độc lập hóa bài "Luyện tập chung", "Bài tập cuối chương", "Hoạt động thực hành trải nghiệm" thành các file PDF riêng biệt. Tuyệt đối không gộp Luyện tập chung vào bài lý thuyết trước đó; xử lý chuẩn xác bài 1 trang (`start_page == end_page`), bảo đảm 100% không bỏ sót bài Luyện tập chung.
   - **QUY CHUẨN HEADER & FOOTER TRANG WORD (BẢNG KẺ ĐƠN XANH DƯƠNG #5B9BD5):**
     + Toàn bộ các trang Word thành phẩm bắt buộc có Header và Footer qua thuộc tính native `section.headers` và `section.footers` của Word (lặp lại chuẩn mực trên mọi trang).
     + **Header (Đầu trang):** Bảng 2 cột, viền dưới đơn màu xanh dương `#5B9BD5` (size 6), không viền khác.
       * Cột trái: `Trường THCS Trần Phú` (font Times New Roman, cỡ 11pt/size 22).
       * Cột phải: `Giáo viên: Hoàng Tấn Thiên` (font Times New Roman, cỡ 11pt/size 22, căn phải).
     + **Footer (Chân trang):** Bảng 3 cột, viền trên đơn màu xanh dương `#5B9BD5` (size 6), không viền khác.
       * Cột trái (40%): Tự động phân loại chính xác theo môn và phân môn:
         - Toán 6: `Môn: Toán – Số học 6` hoặc `Môn: Toán – Hình học 6`
         - Toán 9: `Môn: Toán – Đại số 9` hoặc `Môn: Toán – Hình học 9`
         - Tin học 6: `Môn: Tin học 6`
       * Cột giữa (25%): Đánh số trang căn giữa dạng `- Trang ` + `PageNumber.CURRENT` + `-` (ví dụ: `- Trang 38-`).
       * Cột phải (35%): `Năm học: 2026-2027` (căn phải).
   - **QUY CHUẨN LÀM SẠCH VĂN BẢN & ĐỀ THI ĐÁP ÁN:**
     + Bảng đáp án Toán: Tuyệt đối cấm xuất hiện chữ rác `phantom`, `phantomA`, `phantomB`, `phantomD`... Mọi bước tính toán tự luận viết dưới dạng đẳng thức liên hoàn sạch đẹp.
     + Đề trắc nghiệm Tin học: Tuyệt đối làm sạch các số thứ tự dòng/đoạn thừa dạng `[4]`, `[5]`, `[30]`... trước các phương án A, B, C, D.
     + Mã năng lực AI: Bắt buộc chuẩn hóa đúng khối lớp tương ứng (`6.D1.1` cho Lớp 6, `9.D1.1` cho Lớp 9).
     + Tiết kiểm tra giữa kì: Bắt buộc đối chiếu đúng Phân phối chương trình (PPCT), có kế hoạch bài dạy riêng biệt cho cả phân môn Số học / Đại số và Hình học (Toán 6 Tiết 29 Số học & Tiết 10 Hình học; Toán 9 Tiết 26 Đại số & Tiết 14 Hình học; Tin 6 Tiết 10).


## Coder

User bảo implement `PLAN.md` = đã duyệt.
Nếu bị hook chặn (`.lock`): xóa `docs/handoff/.lock`, sửa code, rồi tạo lại file đó nội dung LOCK.
Không thêm chức năng, không đổi kiến trúc, không đụng file ngoài plan.
Bắt buộc ghi `docs/handoff/IMPLEMENT.md`.
Commit/push khi user bảo: không force push, không commit `.lock`, xóa `.lock` sau khi push.
Chỉ commit khi `VERIFY.md` là PASS, trừ khi user nói rõ commit anyway.

## Cấm

- Hai Coder cùng sửa project.
- Tự mở rộng scope.
- Báo xong khi chưa ghi file handoff.
