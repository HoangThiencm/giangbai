# Cách chạy

## Cách 1: Nhờ Antigravity IDE code trực tiếp
- Yêu cầu thẳng việc cần code/sửa lỗi trong chat (không gõ `/survey`), hoặc sau khi `/survey` xong gõ: `Bạn implement luôn theo docs/handoff/PLAN.md`.

## Cách 2: Quy trình Handoff (`/survey` → Coder → `/verify`)
1. Antigravity, chat mới: `/survey` + việc cần làm
2. Mở `docs/handoff/PLAN.md` kiểm tra nội dung mới
3. Coder (chính Antigravity / Grok / ChatGPT / `agy`): `Implement đúng docs/handoff/PLAN.md`
4. Mở `docs/handoff/IMPLEMENT.md` kiểm tra
5. Antigravity, chat mới: `/verify`
6. Mở `docs/handoff/VERIFY.md`
7. FAIL → Coder: `Sửa đúng bug trong docs/handoff/VERIFY.md` rồi `/verify` lại
8. PASS + muốn lên git → Coder: `Commit, push, xóa docs/handoff/.lock`
