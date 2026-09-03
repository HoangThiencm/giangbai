# IMPLEMENT: Khắc Phục Lỗi Render Raw Code Trên Trang SmartQuiz

**Ngày implement**: 2026-09-03
**Coder**: Grok (xAI)
**Trạng thái**: DONE — 4 smoke tests PLAN yêu cầu đều PASS

## Tóm tắt thay đổi

Kịch bản chèn `security-guard.js` đã nhét `<script src="js/security-guard.js"></script>` vào chuỗi template HTML xuất Word/Excel. Trình duyệt gặp `</script>` trong template thì đóng sớm khối `<script type="text/babel">`, nên phần còn lại bị in ra trang dưới dạng text thô.

### Bước 1: `smartquiz.html`
- Xóa thẻ script thừa trong `exportWord()` (template Word).
- Giữ `<head>` + `<meta charset='utf-8'><title>Export</title>`.
- Giữ nguyên `security-guard.js` hợp lệ ở `<head>` thật (dòng 5).

### Bước 2: `taobaitap.html` và `phancongtochuyenmon.html`
- `taobaitap.html`: xóa script thừa trong `exportWord` và `exportWordLatex`.
- `phancongtochuyenmon.html`: xóa script thừa trong `downloadExcelFile` và ghép lại chuỗi template Excel thành một dòng (tránh ngắt string nháy đơn).

### Bước 3–4: Kiểm thử
- Tạo `tests/smartquiz-smoke.js`: không còn `</script>` lồng trong khối script; Babel mở/đóng khớp; `security-guard.js` chỉ còn 1 lần ở `<head>` thật.

## Files đã sửa / tạo

| File | Thay đổi |
|------|----------|
| `smartquiz.html` | Xóa script thừa trong template `exportWord` |
| `taobaitap.html` | Xóa script thừa trong `exportWord` và `exportWordLatex` |
| `phancongtochuyenmon.html` | Xóa script thừa và nối lại template Excel |
| `tests/smartquiz-smoke.js` | Tạo mới — kiểm tra không lồng `</script>` |

Không đổi logic sinh câu hỏi, chấm điểm hay AI.

## Kết quả kiểm thử

```
smartquiz smoke: nested </script> export templates cleaned; babel scripts stay intact
user-ai-settings smoke: passed
khbd user AI keys smoke: passed
security-f12-smoke: all checks passed
```

Không chạy được kiểm thử trình duyệt end-to-end (không có browser tool trong phiên này). Mở `smartquiz.html` và thử Xuất Word thuộc bước `/verify`.
