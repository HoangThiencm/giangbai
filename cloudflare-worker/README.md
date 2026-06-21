# GiangBai Workers AI (pha 1)

Worker này là AI chính cho lộ trình học: stateless, không dùng D1/KV/Vectorize và không lưu lịch sử chat. Lịch sử gần đây (nếu có) chỉ được trình duyệt gửi cùng request hiện tại.

## Cấu hình trên Cloudflare Dashboard

1. Tạo Worker và dán nội dung `worker.js` vào trình soạn thảo.
2. Trong **Settings → Bindings**, thêm **Workers AI** binding tên chính xác là `AI`.
3. Trong **Settings → Variables and Secrets**, tạo secret `APP_SHARED_SECRET` bằng một chuỗi ngẫu nhiên dài. Không đưa chuỗi này vào JavaScript hoặc `global_config.json`.
4. Tùy chọn: tạo variable `AI_MODEL`. Nếu để trống, Worker dùng `@cf/meta/llama-3.2-3b-instruct`.
5. Bấm **Deploy**. Mở URL Worker: phản hồi phải là JSON có `"ok": true`.

## Tích hợp với hosting

PHP sẽ gọi `POST {WORKER_URL}/chat` và gửi header `X-Giangbai-Worker-Secret`. URL cùng secret phải nằm trong `api/config.php` trên hosting, không nằm trong file cấu hình công khai.

Sau khi Worker đã Deploy và Binding/Secret đã tạo, tích hợp `api/ai_explain.php` để gọi Worker trước Gemini và ShopAIKey.
