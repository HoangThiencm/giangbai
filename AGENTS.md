# Planner → Coder → Tester

User chỉ cần:
1. Antigravity chat mới: `/survey` + việc cần làm
2. Grok: `Implement đúng docs/handoff/PLAN.md`
3. Antigravity chat mới: `/verify`
4. Fail → Grok: `Sửa đúng bug trong docs/handoff/VERIFY.md`
5. User bảo commit/push → Coder commit, push, xóa `docs/handoff/.lock`

Nguồn sự thật (phải là file, không phải chat):
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/VERIFY.md`

## Antigravity

Chỉ `/survey` hoặc `/verify`.
Cấm implement. Cấm sửa source.
Kế hoạch / kết quả test phải ghi file. Chat không được chứa plan hay báo cáo dài.
Nếu user gõ duyệt / làm đi / ok trong chat survey: không sửa source. Trả:
`Plan xong. Mo Grok: Implement dung docs/handoff/PLAN.md`

## Coder (Grok / Codex)

User bảo implement `PLAN.md` = đã duyệt.
Không thêm chức năng, không đổi kiến trúc, không đụng file ngoài plan.
Bắt buộc ghi `docs/handoff/IMPLEMENT.md`.
Khi user bảo commit/push: commit, push nếu được phép, xóa `docs/handoff/.lock`. Không force push. Không commit `.lock`.
Chỉ commit khi `VERIFY.md` là PASS, trừ khi user nói rõ commit anyway.

## Cấm

- Planner và Coder cùng sửa project.
- Tự mở rộng scope.
- Báo xong khi chưa ghi file handoff.
