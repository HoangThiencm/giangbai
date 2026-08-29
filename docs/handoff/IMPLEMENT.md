# IMPLEMENT

Trạng thái: ĐÃ LÀM — vá VERIFY FAIL soanbaigemini: khớp 100% HINH_xx + card tạo ảnh tùy chọn

## File đã đổi

- `backupcode viettailieu/soanbaigemini.html`
- `lesson-import.js` (nhận marker `HINH_CUSTOM_xx`)
- `tests/soanbaigemini-plan-smoke.js`
- `docs/handoff/IMPLEMENT.md`

## Nội dung chính

1. **Khớp hình ảnh**
   - Prompt Bước 1 khóa mã liên tục `HINH_01`, `HINH_02`; mọi hình phải có `![Mô tả](HINH_xx)`.
   - Prompt Bước 2 tiếp nối `HINH_03`, `HINH_04`..., liệt kê đủ mã đã dùng.
   - `buildLessonImageInventory()` / `collectMarkerIdsFromLessonSources()`: marker trong bài mà thiếu DANH SÁCH HÌNH thì tự sinh prompt từ mô tả xung quanh (`autoFilled`) và **luôn hiện thẻ tạo ảnh**. Không còn chỉ hiện hint rồi ẩn khung.

2. **Card “Tạo ảnh từ Prompt / Mô tả tùy chọn”**
   - Textarea prompt, phong cách Sơ đồ/Vector SGK hoặc Ảnh thực tế.
   - Nút **Tạo ảnh ngay** → `createLessonIllustration()`.
   - Xem trước, **Tải PNG**, **Copy Data URL**, **Chèn vào bài soạn** `![Mô tả](HINH_CUSTOM_xx)`.

## Test đã chạy

```
node tests/soanbaigemini-plan-smoke.js
```

Kết quả: **pass**.
