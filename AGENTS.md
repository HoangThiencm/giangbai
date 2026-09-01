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

Chỉ `/survey` hoặc `/verify`. Cấm implement. Cấm sửa source.
Kế hoạch / test phải ghi file. Chat không được chứa plan hay báo cáo dài.
Nếu user gõ duyệt / làm đi / ok trong chat survey: không sửa source. Trả:
`Plan xong. Mo Coder (Grok / ChatGPT / agy): Implement dung docs/handoff/PLAN.md`

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
