# Cách chạy

1. Antigravity, chat mới: `/survey` + việc cần làm
2. Mở `docs/handoff/PLAN.md` — có nội dung mới mới bước 3
3. Grok: `Implement đúng docs/handoff/PLAN.md`
4. Mở `docs/handoff/IMPLEMENT.md` kiểm tra
5. Antigravity, chat mới: `/verify`
6. Mở `docs/handoff/VERIFY.md`
7. FAIL → Grok: `Sửa đúng bug trong docs/handoff/VERIFY.md` rồi `/verify` lại
8. PASS + muốn lên git → Grok: `Commit, push, xóa docs/handoff/.lock`

Việc mới: Grok đã xóa `.lock` ở bước 8, hoặc tự xóa `docs/handoff/.lock` rồi làm lại từ bước 1.
