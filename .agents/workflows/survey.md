---
description: Planner — ghi PLAN.md + .lock, không viết plan trong chat
---

Chỉ được ghi 2 file:
- `docs/handoff/PLAN.md` (ghi đè toàn bộ)
- `docs/handoff/.lock` (nội dung: LOCK)

Cấm sửa source. Cấm tạo file khác. Cấm đưa kế hoạch ra chat.

Làm lần lượt:
1. Đọc code thật.
2. Ghi đè `docs/handoff/PLAN.md`:

```md
# PLAN

## Hiện trạng
## Phạm vi
## Ngoài phạm vi
## File dự kiến tác động
## Các bước thực hiện
## Rủi ro
## Cách kiểm thử
## Tiêu chí nghiệm thu
```

3. Ghi `docs/handoff/.lock` nội dung LOCK.
4. Chat chỉ trình bày như sau rồi rồi dừng:
`Trình bày những gì đã khảo sát`
`Đã ghi docs/handoff/PLAN.md`
`Plan xong. Mở Grok/Chatgpt: Implement dùng docs/handoff/PLAN.md`

Chưa ghi được 2 file thì chưa được dừng.
Tin nhắn sau trong chat này cũng không được sửa source.
