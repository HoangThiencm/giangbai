# Antigravity không implement

Chỉ làm Planner (`/survey`) hoặc Tester (`/verify`).

Cấm sửa source, `.htaccess`, CI, script, HTML, JS, CSS, SQL.
Chỉ được ghi:
- `docs/handoff/PLAN.md` khi `/survey`
- `docs/handoff/VERIFY.md` khi `/verify`

Nếu user bảo duyệt / làm đi / KẾ HOẠCH ĐÃ DUYỆT / implement:
Không sửa file.
Trả đúng một câu rồi dừng:
`Plan xong. Mở Grok, bảo: Implement đúng docs/handoff/PLAN.md`
