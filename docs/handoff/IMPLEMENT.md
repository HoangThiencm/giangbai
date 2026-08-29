# IMPLEMENT

Trạng thái: ĐÃ LÀM — bundle JS lúc deploy để ẩn tên file trên DevTools Sources

## File đã đổi

- `tools/build-obfuscate.js`
- `tests/security-f12-smoke.js`
- `.gitignore`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

Không đụng PHP API, không gộp CDN/vendor, không sửa HTML trên git (chỉ rewrite khi `--in-place` / CI).

## Nội dung chính

`tools/build-obfuscate.js` khi ghi output (`--in-place` trên GitHub Actions):

1. Quét `.html`, chỉ nhận thẻ `<script src>` **đứng một mình trên một dòng** (tránh template export trong chuỗi JS).
2. Gộp các file JS nội bộ **liên tiếp** theo đúng thứ tự thẻ (cụm `soankhbd` 11 file → `js/soankhbd.bundle.js`).
3. Bỏ qua `http(s):`, `//`, `vendor/`, `*.min.js`, `type=module` / `text/babel`.
4. Obfuscate bundle (cùng cấu hình tối đa). Fallback không bọc `Function` cho bundle (giữ global).
5. Thay cụm thẻ bằng một dòng `<script src="js/{trang}.bundle.js"></script>`.

Cụm 1 file (ví dụ `security-guard.js` trên `<head>`) **không** kéo xuống cuối trang — tránh chạy `khbd-app.js` trước CDN/DOM.

`.gitignore`: `js/*.bundle.js` — artifact CI, không commit.

## Test đã chạy

```
node tests/security-f12-smoke.js
```

Kết quả: **pass** (cụm `soankhbd.html` → `js/soankhbd.bundle.js`; thư mục mẫu thay 2 thẻ local bằng 1 bundle, giữ CDN/vendor, thứ tự first→second).

## Vấn đề còn lại

- File JS gốc vẫn được FTP lên hosting nhưng HTML không nạp chúng, nên tab Sources không liệt kê tên thành phần. URL trực tiếp `.../js/khbd-app.js` vẫn mở được nếu biết đường dẫn.
- `thitructuyen.html` có nhiều cụm xen CDN → có thể ra `bundle-1.js`, `bundle-2.js` thay vì một file duy nhất. Tên nhạy cảm trong từng cụm vẫn biến mất.
- HTML inline / `type=text/babel` không gộp.
