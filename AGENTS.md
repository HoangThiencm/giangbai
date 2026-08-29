# Planner → Coder → Tester

Nguồn sự thật:
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/VERIFY.md`

Luồng:
1. Antigravity `/survey` ghi `PLAN.md` rồi dừng. Không sửa source.
2. User mở Grok, bảo implement `PLAN.md`. Đó là lệnh duyệt.
3. Grok code và ghi `IMPLEMENT.md`.
4. Antigravity `/verify` ghi `VERIFY.md`. Không viết feature.
5. Fail thì Grok sửa đúng bug trong `VERIFY.md`.
6. Pass mới push GitHub nếu user yêu cầu.

## Antigravity

Chỉ `/survey` hoặc `/verify`.
Cấm implement. Cấm sửa source.
Nếu user gõ duyệt / làm đi / KẾ HOẠCH ĐÃ DUYỆT trong chat này: không sửa file. Trả đúng một câu rồi dừng:
`Plan xong. Mở Grok, bảo: Implement đúng docs/handoff/PLAN.md`

## Coder (Grok / Codex)

Khi user bảo implement `PLAN.md` thì đó là đã duyệt.
Không thêm chức năng, không đổi kiến trúc, không đụng file ngoài plan.
Không ghi đè thay đổi sẵn có của user.
Ghi `docs/handoff/IMPLEMENT.md`: file đã đổi, nội dung chính, test đã chạy, vấn đề còn lại.

## Cấm

- Planner và Coder cùng sửa project.
- Tự mở rộng scope.
- Xóa data, reset repo, force push khi chưa được phép.
- Báo xong khi chưa có bằng chứng test.
