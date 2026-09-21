# PLAN: Nâng Cấp Game Đua Vịt Hài Hước Đỉnh Cao & Sửa Lỗi Toán/Kẹt Câu

## 1. Tổng Quan Nhiệm Vụ

Bản kế hoạch này giải quyết trọn vẹn 3 yêu cầu cốt lõi:
1. **Sửa lỗi render công thức toán KaTeX** trong modal câu hỏi của `game-treasure.html`.
2. **Sửa lỗi kẹt vĩnh viễn câu 1** trong game Hứng Trứng Vàng (`game-escape.html`).
3. **Nâng cấp đột phá Game Đua Vịt** (`game-treasure.html`) từ bảng tính 2D khô khan thành **"ĐUA VỊT HÀI HƯỚC BÙNG NỔ LỚP HỌC"**: bầy vịt bơi tự do va chạm (`bumping physics`), sự kiện bất ngờ (đớp bánh mì, xoáy nước, cụ rùa đẩy), bình luận viên trực tiếp và pha quay chậm Photo Finish nghẹt thở.

---

## 2. Chi Tiết Thực Hiện Cho Coder

### PHẦN 1: Nâng Cấp Đột Phá Game Đua Vịt (`game-treasure.html`)

#### 1. Thư viện & KaTeX (`<head>`):
Bổ sung đầy đủ trong `<head>`:
```html
<link rel="stylesheet" href="vendor/katex.min.css">
<script src="vendor/katex.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
```

#### 2. Component `<MathText>`:
Định nghĩa component `MathText` chuẩn hóa công thức toán để render KaTeX sắc nét cho prompt và choices trong modal câu hỏi kiểm tra.

#### 3. Động Cơ Đua Vịt Hài Hước (Chaos River Engine trên HTML5 Canvas 60 FPS):
Xây dựng lại hàm vẽ và cập nhật vật lý cho bầy vịt trong component `River`:
- **Bầy vịt bơi đàn tự do (Flocking & Bumping Physics):**
  - Vịt không xếp hàng thẳng tắp ở làn cố định. Cả đàn 30–45 chú vịt cùng bơi trong lòng sông rộng.
  - Khi 2 chú vịt bơi sát nhau, chúng va chạm đẩy nhau nảy tưng tưng (`elastic bump`) kèm âm thanh `Boing!`, con lách trái, con vọt phải.
  - Vịt đạp chân tạo bọt nước (`wake bubbles`) nhấp nhô sống động.
- **Phụ kiện & Biểu cảm ngẫu nhiên (Duck Personalities):**
  Mỗi chú vịt được vẽ với phụ kiện ngẫu nhiên:
  - 🕶️ Kính râm cực ngầu
  - 🎓 Mũ cử nhân bác học
  - 🦩 Phao bơi hồng hạc
  - 🚀 Tên lửa gắn lưng
  - 🎀 Nơ đỏ dễ thương
  - Bảng tên học sinh bo tròn nổi bật, chữ đậm dễ đọc từ xa trên máy chiếu phòng học.
- **Sự kiện ngẫu nhiên hài hước (Random Chaos Events):**
  Trong suốt 10–14 giây đua, xuất hiện các biến số bất ngờ:
  - 🍞 **Mẩu bánh mì trôi:** Chú vịt đang dẫn đầu bỗng dừng lại 0.8 giây để đớp bánh mì, bị cả đàn ùa lên vượt qua!
  - 🌪️ **Xoáy nước mini:** Hút 1–2 chú vịt xoay tròn 360 độ rồi bắn vọt về trước!
  - 🐢 **Cụ Rùa cứu trợ:** Đội đáy sông đẩy 1 chú vịt từ bét bảng vọt thẳng vào Top 5!
  - 🚀 **Tên lửa Nitro:** Vịt bốc khói đuôi, lao vèo qua mặt cả đàn trong tiếng xả khói!
- **Thanh Bình Luận Viên Trực Tiếp (Live Ticker Commentary):**
  Dưới chân khung đua chạy chữ bình luận vui nhộn theo thời gian thực:
  - *"Vịt của bạn [Tên] đang bứt tốc như một mũi tên!"*
  - *"Ôi không! [Tên] vừa mải đớp bánh mì trôi!"*
  - *"Cụ rùa vừa giải cứu bạn [Tên] từ cuối đàn vọt lên Top 3!"*
  - *"Cuộc rượt đuổi nghẹt thở ở những mét nước cuối cùng!"*
- **Camera Động & Pha Quay Chậm Photo Finish:**
  - Camera cuộn theo tốp dẫn đầu.
  - Khi cách vạch đích 5%, tốc độ chậm lại (slow-motion) để cả lớp cùng nín thở theo dõi mỏ chú vịt nào chạm vạch ca-rô trước!

#### 4. Âm Thanh Web Audio API:
- Tiếng còi đếm ngược 3-2-1 và còi xuất phát.
- Tiếng đàn vịt kêu `quack quack` vui nhộn khi xuất phát và va chạm.
- Tiếng `Boing!` khi vịt húc vào nhau.
- Tiếng rẽ sóng nước tăng dần nhịp độ.
- Tiếng kèn chiến thắng Fanfare rộn rã khi chạm vạch đích.

#### 5. Modal Câu Hỏi Kiểm Tra Chuẩn KaTeX:
Khi giáo viên bấm "Hiện câu hỏi kiểm tra", hiển thị modal với:
- Prompt và Choices được render bằng `<MathText>` chuẩn đẹp.
- Đồng hồ đếm ngược 30s.

---

### PHẦN 2: Sửa Lỗi Kẹt Câu 1 Trong Hứng Trứng Vàng (`game-escape.html`)

#### 1. Tách riêng 2 Timer Ref:
Thay thế `const timeoutRef = useRef(null);` bằng:
```javascript
const fallTimerRef = useRef(null);
const nextTimerRef = useRef(null);
```

#### 2. Sửa `useEffect` rơi trứng:
Chỉ dọn dẹp `fallTimerRef`, tuyệt đối không xóa `nextTimerRef`:
```javascript
useEffect(() => {
    if (phase !== 'falling' || !currentQ || showInstructions || gameOver) return;
    fallTimerRef.current = setTimeout(() => {
        const nextLives = lives - 1;
        setLives(nextLives);
        setStreak(0);
        setPhase('result');
        setCaught(-1);
        setLastMsg('Trứng rơi mất! Mất 1 mạng.');
        nextTimerRef.current = setTimeout(() => goNext(nextLives), 1400);
    }, (fallDuration + 0.5) * 1000);
    return () => {
        if (fallTimerRef.current) clearTimeout(fallTimerRef.current);
    };
}, [fallKey, phase, currentQ, showInstructions, gameOver, fallDuration, lives, goNext]);
```

#### 3. Sửa `handleCatch`:
Dùng `nextTimerRef` để đặt lịch chuyển câu, không bị cleanup của `falling` xóa mất:
```javascript
const handleCatch = (choiceIdx) => {
    if (phase !== 'falling' || !currentQ) return;
    if (fallTimerRef.current) clearTimeout(fallTimerRef.current);
    if (nextTimerRef.current) clearTimeout(nextTimerRef.current);
    setPhase('result');
    setCaught(choiceIdx);
    const isCorrect = choiceIdx === currentQ.answer;

    if (isCorrect) {
        const bonus = Math.min(streak, 5) * 4;
        setScore(prev => prev + 20 + bonus);
        setStreak(prev => prev + 1);
        setCorrectTotal(prev => prev + 1);
        setLastMsg(currentQ.explanation || 'Trứng vàng! Đáp án chính xác!');
        nextTimerRef.current = setTimeout(() => goNext(lives), 1200);
    } else {
        const nextLives = lives - 1;
        setLives(nextLives);
        setStreak(0);
        setLastMsg(`Trứng thối! Đáp án đúng là ${String.fromCharCode(65 + currentQ.answer)}.`);
        nextTimerRef.current = setTimeout(() => goNext(nextLives), 1400);
    }
};
```

#### 4. Nâng cấp `goNext`:
Dùng updater function `setQIndex(prevIndex => ...)` để loại bỏ stale state closure.

---

## 3. Kế Hoạch Xác Minh (Verification Plan)
1. **Kiểm tra Đua Vịt (`game-treasure.html`):**
   - Đàn vịt bơi tự do, va chạm nảy tưng tưng, có các sự kiện đớp bánh mì, xoáy nước, cụ rùa đẩy, bình luận viên trực tiếp.
   - Vịt về đích có slow-motion Photo Finish, pháo hoa và âm thanh chiến thắng.
   - Mở modal câu hỏi kiểm tra: công thức `$A = 2x^2y \cdot (-3)xy^3$` và `$-6x^3y^4$` render KaTeX chuẩn đẹp mắt.
2. **Kiểm tra Hứng Trứng Vàng (`game-escape.html`):**
   - Chơi câu 1: dù đúng hay sai đều tự động chuyển mượt mà sang câu 2, câu 3, câu 4 cho đến khi hết bài hoặc hết mạng.
