# IMPLEMENT

Trạng thái: ĐÃ LÀM — PDF scan OCR + Tạo bài tập tổng hợp từ file (`taobaitap.html`)

## File đã đổi

- `backupcode viettailieu/taobaitap.html`
- `taobaitap.html`
- `tests/taobaitap-plan-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Nội dung chính

1. **Đọc PDF scan/ảnh**: `readTextFromDocumentFile` vẫn dùng `pdfjsLib.getTextContent()`. Nếu PDF có text compact dưới 50 ký tự, `readDocumentSourceWithOcrFallback` render tối đa 20 trang sang JPEG (`renderPdfPagesToImageItems`) rồi OCR bằng `extractSourceTextFromImageBatch`. `extractSourceTextFromFile` và `handleFileUpload` đều đi đường này. `addSourceFiles` hiện tiến trình khi đọc PDF.
2. **Tạo bài tập tổng hợp từ file**: `generateSynthesizedFromSource()` lấy `getSourceContext()` từ `sourceMaterials`, không cần tên chủ đề. Prompt yêu cầu quét toàn diện, bám sát 100% học liệu. Kết quả `normalizeQuizItems` (trắc nghiệm) rồi `setStep(2)`.
3. **Card UI**: Card tím **"⚡ TẠO BÀI TẬP TỔNG HỢP TỪ FILE"** với số câu 5/10/15/20 hoặc tùy chỉnh (1–50), hình thức (trắc nghiệm tổng hợp / từng loại / tự luận), mức độ (Cơ bản, Trung bình, Nâng cao, Hỗn hợp 4 mức). Nút tắt khi chưa nạp nguồn.
4. **Ngoài phạm vi giữ nguyên**: `generateContent` vẫn chặn chủ đề trống; Word và DẠY NGAY không đổi.

## Test đã chạy

```
node tests/taobaitap-plan-smoke.js
```

Kết quả: **pass** (48/48 check, gồm root + backup + ngưỡng OCR).
