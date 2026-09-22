# IMPLEMENT: Tab chuyên biệt Học liệu OLM.vn

## Phạm vi đã thực hiện

- `taobaitap.html`: Chuẩn hóa `exportWordOLM` theo cú pháp mẫu OLM: tiêu đề ba phần màu xanh, `Câu n.`, đáp án đúng gạch chân ở nhãn, mệnh đề đúng/sai dùng `#`, câu trả lời ngắn dùng `[[...]]`, và lời giải `[HDG]`.
- `taobaitap.html`: Thêm state và modal **Học liệu OLM.vn (Luyện tập & Đề thi)**, thay hai nút xuất rời bằng một nút toolbar mở modal. Modal có hai hướng xuất: Word thông minh OLM và bộ đôi Đề bài/Hướng dẫn giải; đồng thời hiển thị xem trước cấu trúc OLM trước khi tải.
- `tests/taobaitap-olm-export-smoke.js`: Bổ sung kiểm tra cú pháp `#${item.text}`, nhãn mệnh đề gạch chân, dấu chấm sau số câu, hai hành động trong modal và preview.

## Kiểm thử

- PASS: `node tests/taobaitap-olm-export-smoke.js`
- PASS: `node tests/taobaitap-game-word-export-smoke.js`
- PASS: `node tests/cv7991-taobaitap-thitructuyen-sync-smoke.js`
- PASS: `node tests/taobaitap-plan-smoke.js`
- PASS: `node tests/taobaitap-presentation-smoke.js`
- PASS: `git diff --check -- taobaitap.html tests/taobaitap-olm-export-smoke.js docs/handoff/IMPLEMENT.md`
