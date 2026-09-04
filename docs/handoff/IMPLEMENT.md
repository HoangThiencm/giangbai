# IMPLEMENT: Hệ thống Nghiên cứu bài học (NCBH) có hỗ trợ AI

**Ngày implement**: 2026-09-04
**Coder**: Grok (xAI)
**Trạng thái**: DONE — `tests/nghiencuubaihoc-smoke.js` PASS

## Tóm tắt

Thêm phân hệ `nghiencuubaihoc.html`: 12 bước NCBH, 6 khu vực thống nhất mỗi bước, 12 tác vụ AI riêng, KHBD 2 lớp, nhật ký quyết định GV, lưu kép CSDL + localStorage, xuất 13 sản phẩm Word/.zip.

## Files

| File | Thay đổi |
|------|----------|
| `api/nghiencuubaihoc.php` | Tạo mới — bảng `nghien_cuu_bai_hoc_sessions`, `list` / `get` / `save` / `delete` |
| `nghiencuubaihoc.html` | Tạo mới — giao diện + logic 12 bước |
| `index.html` | Thẻ công cụ + `TOOL_PAGE_LINKS.nghiencuubaihoc` |
| `admin.html` | Quyền hiển thị `cfg_nghiencuubaihoc` và danh mục công cụ GV |
| `api/helpers.php` | Catalog trang để `allowed_pages` lưu được `nghiencuubaihoc` |
| `access-control.js` | Map trang `nghiencuubaihoc.html` |
| `global_config.json` | `features.nghiencuubaihoc: true` |
| `tests/nghiencuubaihoc-smoke.js` | Tạo mới |

Không sửa `soankhbd.html`, `xaydungphuluc.html`, `duyetgiaoan.html`, `duyetde.html`, bảng `users`, Google Drive, Cloudflare Workers.

## Kết quả kiểm thử

```
node tests/nghiencuubaihoc-smoke.js
nghiencuubaihoc smoke: index/admin integration, 12 steps, 6 zones, 12 AI tasks, key sync, API schema passed
```

Cũng PASS: `xaydungphuluc-integration-smoke.js`, `duyetgiaoan-integration-smoke.js`, `security-f12-smoke.js`.

`node tests/run-all-tests.js` dừng ở các smoke KHBD sẵn có (`soankhbd.html` / `js/khbd-*.js`) — ngoài phạm vi PLAN. Module NCBH không đụng các file đó.

## Chưa kiểm thử trên trình duyệt

Phiên này không có browser tool. `/verify` cần mở `index.html` → thẻ NCBH → 12 bước, nạp key, lưu CSDL, xuất .docx.
