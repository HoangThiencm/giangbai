# Planner → Coder → Tester

Nguồn sự thật:
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/VERIFY.md`

Luồng:
1. Antigravity `/survey` ghi `PLAN.md` + `docs/handoff/.lock` rồi dừng.
2. User mở Grok, bảo implement `PLAN.md`. Đó là lệnh duyệt.
3. Grok code và ghi `IMPLEMENT.md`.
4. Antigravity `/verify` ghi `VERIFY.md`. Không viết feature.
5. Fail thì Grok sửa đúng bug trong `VERIFY.md`.
6. User bảo commit/push: Coder commit, push nếu được phép, rồi xóa `docs/handoff/.lock`.

## Antigravity

Chỉ `/survey` hoặc `/verify`. Cấm implement. Cấm sửa source.
Nếu user gõ duyệt / làm đi trong chat này: không sửa file. Trả:
`Plan xong. Mở Grok, bảo: Implement đúng docs/handoff/PLAN.md`

## Coder (Grok / Codex)

Khi user bảo implement `PLAN.md` thì đó là đã duyệt.
Không thêm chức năng, không đổi kiến trúc, không đụng file ngoài plan.
Ghi `docs/handoff/IMPLEMENT.md`.

Khi user bảo commit hoặc push:
1. Chỉ commit khi `VERIFY.md` là PASS, hoặc user nói rõ commit dù chưa test xong.
2. Không force push, không xóa data.
3. Xong commit/push thì xóa file `docs/handoff/.lock`.
4. Không commit `.lock`.

## Cấm

- Planner và Coder cùng sửa project.
- Tự mở rộng scope.
- Báo xong khi chưa có bằng chứng test.
