# IMPLEMENT

Đã nâng cấp bài giảng theo PLAN: bảng viết, nhảy tiết, loa song ngữ, khóa cuộn khi vẽ, cột ghi bảng và audio Hoài My.

## Đã làm

- `master_lecture_template.html` và `Bai_12_...html`:
  - `#blackboardOverlay` / `#blackboardCanvas`: phấn trắng, phấn vàng, xóa bảng, giữ Shift vẽ đường thẳng. Phím `W` hoặc `B` mở bảng, `Escape` đóng.
  - Nút `[Tiết 1]`, `[Tiết 2]`, `[Tiết 3]` gọi `jumpToPeriod` tới slide 1, 9, 16.
  - Đã bỏ nút `[💬 Tắt phụ đề]`.
  - `body.pen-mode` khóa `overflow: hidden` trên slide và hai cột.
  - `speakBlockAuto`: giao diện Việt phát `audio/slide-N.mp3` (Hoài My), giao diện Anh gọi `speakBlockEn`. Nút loa 🔊 dùng `speakBlockAuto`. `speakBlockEn` không còn tự gọi `toggleLanguage()`.
- Bài 12: các khối ví dụ, luyện tập, bài tập, phân tích đã chuyển sang cột hoạt động. Cột ghi bảng giữ định lí và công thức. Slide 2 vẫn đúng bước smoke (`s2_t1`/`s2_t2` bước 1, `s2_b1` bước 2, `s2_t3` bước 3, `s2_b2` bước 4).
- Mục 5 của `PROMPT_TAO_BAI_GIANG_HTML.md` và `.agents/rules/tao-bai-giang-html.md` có bảng viết, nút tiết, `speakBlockAuto` và khóa cuộn.
- Smoke hai file test có assertion cho bảng viết, nhảy tiết, loa song ngữ, không còn nút phụ đề.
- `export_hoaimy_audio.py` đã xuất `audio/slide-1.mp3` đến `audio/slide-26.mp3`.

## Kiểm thử

- `node tests/trolythien-template-smoke.js` — PASS
- `node tests/trolythien-bai-giang-html-smoke.js` — PASS
- Chưa mở trình duyệt. Bấm Tiết, bảng viết, Shift và loa để chat `/verify`.

## Chưa làm

- Không commit, không push.
