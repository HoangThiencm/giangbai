# Planner → Coder → Tester

Planner + Tester: Antigravity IDE (`/survey`, `/verify`).
Coder: một trong ba — Grok, ChatGPT/Codex, hoặc `agy` CLI.
Cùng lúc chỉ một Coder. Không để IDE survey và Coder cùng sửa source.

User chỉ cần:
1. Antigravity IDE, chat mới: `/survey` + việc cần làm
2. Coder: implement đúng `docs/handoff/PLAN.md`
3. Antigravity IDE, chat mới: `/verify`
4. Fail → Coder sửa đúng bug trong `docs/handoff/VERIFY.md`
5. User bảo commit/push → Coder commit, push, xóa `docs/handoff/.lock`

Nguồn sự thật (file, không phải chat):
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/VERIFY.md`

Lệnh Coder (chọn 1):
- Grok / ChatGPT: `Implement đúng docs/handoff/PLAN.md`
- CLI: `agy -p "Implement đúng docs/handoff/PLAN.md"`

## Antigravity IDE

1. **Khi phát triển / sửa mã nguồn (Coding/Dev):**
   - Chỉ `/survey` hoặc `/verify`. Cấm implement. Cấm sửa source.
   - Kế hoạch / test phải ghi file. Chat không được chứa plan hay báo cáo dài.
   - Nếu user gõ duyệt / làm đi / ok trong chat survey: không sửa source. Trả:
     `Plan xong. Mo Coder (Grok / ChatGPT / agy): Implement dung docs/handoff/PLAN.md`

2. **Khi người dùng gọi Trợ lý Sư phạm Hoàng Thiên (`/thien`, "Thiên ơi" hoặc tác vụ sư phạm):**
   - Đây là tác vụ nghiệp vụ giảng dạy (soạn KHBD, tạo bài tập, duyệt đề, tạo bài giảng HTML, vẽ hình học trong thư mục `TROLYTHIEN/`).
   - Antigravity IDE đóng vai trò Trợ lý Hoàng Thiên, **ĐƯỢC PHÉP và BẮT BUỘC thực hiện trực tiếp ngay lập tức** (đọc đề/ảnh, tính toán giải tích, xuất file vào `TROLYTHIEN/`).
   - **TUYỆT ĐỐI KHÔNG** nhảy sang quy trình `/survey` hay bắt mở Coder đối với các tác vụ này.
   - **BẢN VÁ HỆ THỐNG — 100% WORD EQUATION (OMML):** Mọi tệp Word (`.docx`) chứa công thức Toán/KHTN xuất ra BẮT BUỘC dùng native Word Equation (`m:oMath`) qua `TROLYTHIEN.engine.word_math_helper` hoặc `de_cuong_docx_helper`. TUYỆT ĐỐI CẤM dùng text Unicode thô (`(x+y)/4`, `x⁴y²`, `góc M = 100°`). Bảng nối cột bắt buộc dùng `Table Grid` có header Cột A/B nền xám `#F2F2F2`, từng ô là Equation. Ký hiệu góc luôn dùng mũ `\widehat{...}`.
   - **QUY CHUẨN KÝ HIỆU CUNG TRÒN & CÔNG THỨC TOÁN 9 (OMML):** Ký hiệu cung tròn $\wideparen{AB}$, $\wideparen{AmB}$, $\wideparen{CD}$ và số đo cung $\text{sđ }\wideparen{AB}$ bắt buộc dùng Office Math Accent `m:acc` với `\u23DC` (`⏜` TOP PARENTHESIS). Tuyệt đối cấm ký tự thô `⌒` (U+2312) nằm ngang trước chữ cái (`⌒AB`).
   - **THỂ THỨC DẤU NHÁY HÀNH CHÍNH (NĐ 30/2020/NĐ-CP) & CHỐNG RÒ RỈ MARKDOWN:** Toàn bộ dấu ngoặc kép trong Word bắt buộc là cặp dấu nháy kép cong hành chính: mở `“` (U+201C), đóng `”` (U+201D); tuyệt đối không dùng dấu nháy thẳng typewriter ASCII `"`. Tuyệt đối không để lộ các ký tự sao Markdown rác (`***`, `**`) ra văn bản Word thành phẩm; các khối tích hợp sư phạm `***...***` không được bị cắt đứt giữa chừng bởi role breaks.
   - **QUY CHUẨN CẮT PDF SGK THEO BÀI (MỤC 10):** Bắt buộc độc lập hóa bài "Luyện tập chung", "Bài tập cuối chương", "Hoạt động thực hành trải nghiệm" thành các file PDF riêng biệt. Tuyệt đối không gộp Luyện tập chung vào bài lý thuyết trước đó; xử lý chuẩn xác bài 1 trang (`start_page == end_page`), bảo đảm 100% không bỏ sót bài Luyện tập chung.


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
