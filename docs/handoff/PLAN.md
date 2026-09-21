# PLAN: Sửa Lỗi Render Toán Trong "Đua Vịt" & Lỗi Đứng Yên Câu 1 Trong "Hứng Trứng Vàng"

## 1. Phân Tích Nguyên Nhân Gốc Rễ (Root Cause)

### Vấn đề 1: Đua Vịt (`game-treasure.html`) chưa render công thức toán
- **Nguyên nhân:**
  1. Trong thẻ `<head>` của `game-treasure.html` **chưa nạp thư viện KaTeX** (`vendor/katex.min.css` và `vendor/katex.min.js`).
  2. File chưa định nghĩa component `<MathText>`.
  3. Trong modal hiển thị câu hỏi kiểm tra (dòng 15), prompt và choices đang xuất thô dạng `{q.prompt || q.question}` và `{x}` thay vì bọc trong `<MathText>`. Vì vậy, các công thức như `$A = 2x^2y \cdot (-3)xy^3$` và `$-6x^3y^4$` hiển thị nguyên văn chuỗi thô.

### Vấn đề 2: Hứng Trứng Vàng (`game-escape.html`) chạy câu đầu xong đứng yên
- **Nguyên nhân (Lỗi Race Condition giữa React Re-render và Timer):**
  - Trong `game-escape.html`, chỉ sử dụng duy nhất một ref `const timeoutRef = useRef(null)`.
  - Khi người chơi bắt trứng (hoặc để trứng rơi), `handleCatch` thiết lập:
    ```javascript
    timeoutRef.current = setTimeout(() => goNext(...), 1200);
    ```
  - Tuy nhiên, trong `handleCatch` cũng đồng thời gọi `setPhase('result')` và `setLives(...)`, khiến component re-render.
  - Do `phase` chuyển từ `'falling'` sang `'result'`, React lập tức kích hoạt hàm dọn dẹp (cleanup) của `useEffect` rơi trứng:
    ```javascript
    return () => { if (timeoutRef.current) clearTimeout(timeoutRef.current); };
    ```
  - **Hàm cleanup này đã vô tình xóa sạch timer `goNext`** mà `handleCatch` vừa mới đặt trước đó vài mili-giây!
  - Kết quả: Timer `goNext` bị hủy, hàm `goNext` không bao giờ được gọi $\rightarrow$ Game bị kẹt vĩnh viễn ở trạng thái `'result'` của câu 1, không chuyển sang câu 2!

---

## 2. Nhiệm Vụ Chi Tiết Của Coder

Coder sẽ sửa đổi 2 tệp: **`game-treasure.html`** và **`game-escape.html`**.

---

### PHẦN 1: Sửa `game-treasure.html` (Đua Vịt)

#### Bước 1.1: Bổ sung KaTeX vào `<head>`
Tại dòng 4 của `game-treasure.html`, thêm link CSS và script KaTeX:
```html
<link rel="stylesheet" href="vendor/katex.min.css">
<script src="vendor/katex.min.js"></script>
```

#### Bước 1.2: Bổ sung component `MathText` trong React
Thêm component `MathText` chuẩn hóa công thức toán:
```javascript
const MathText = ({ text }) => {
    const ref = useRef(null);
    useEffect(() => {
        if (!text || !ref.current) return;
        ref.current.innerHTML = '';
        let processed = String(text).trim();
        processed = processed.replace(/`([^`]+)`/g, (m, g) => `$${g}$`);
        processed = processed.replace(/\\\[([\s\S]+?)\\\]/g, (m, g) => `$$${g}$$`);
        processed = processed.replace(/\\\(([\s\S]+?)\\\)/g, (m, g) => `$${g}$`);
        if (!processed.includes('$')) {
            if (/\\(frac|sqrt|vec|cdot|times|pm|mp|le|ge|ne|neq|alpha|beta|gamma|pi|theta|Delta|[a-zA-Z]+)/.test(processed)) {
                processed = `$${processed}$`;
            } else if (/^[a-zA-Z0-9\s\+\-\*\/\=\^\_\(\)\{\}\.,<>\\]+$/.test(processed) && /[\^_\\]/.test(processed)) {
                processed = `$${processed}$`;
            }
        }
        const parts = processed.split(/(\$\$[\s\S]+?\$\$|\$[\s\S]+?\$)/g);
        parts.forEach(part => {
            if (!part) return;
            if (part.startsWith('$$') && part.endsWith('$$')) {
                const span = document.createElement('span');
                try { katex.render(part.slice(2, -2), span, { throwOnError: false, displayMode: true }); }
                catch { span.textContent = part; }
                ref.current.appendChild(span);
            } else if (part.startsWith('$') && part.endsWith('$')) {
                const span = document.createElement('span');
                try { katex.render(part.slice(1, -1), span, { throwOnError: false, displayMode: false }); }
                catch { span.textContent = part; }
                ref.current.appendChild(span);
            } else {
                ref.current.appendChild(document.createTextNode(part));
            }
        });
    }, [text]);
    return <span ref={ref} />;
};
```

#### Bước 1.3: Render `<MathText>` trong Modal Câu Hỏi Kiểm Tra
Thay thế đoạn JSX modal câu hỏi ở cuối component `App`:
```jsx
{q && (
    <div className="fixed inset-0 z-[60] shade flex items-center justify-center p-4">
        <div className="pop bg-white rounded-3xl p-7 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-4">
                <b className="text-xl text-violet-700"><i className="fas fa-edit mr-2"></i>Câu hỏi kiểm tra</b>
                <b className="text-2xl text-rose-600">⏱ {secs}s</b>
            </div>
            <div className="text-lg font-bold text-gray-800 my-4 leading-relaxed">
                <MathText text={q.prompt || q.question} />
            </div>
            <div className="space-y-2 mb-4">
                {(q.choices || []).map((x, i) => (
                    <button key={i} className="block w-full text-left p-3 border-2 border-gray-200 rounded-xl hover:border-violet-400 hover:bg-violet-50 transition">
                        <span className="font-bold text-violet-700 mr-2">{String.fromCharCode(65 + i)}.</span>
                        <MathText text={x} />
                    </button>
                ))}
            </div>
            <button className="btn w-full mt-2 bg-slate-700 text-white" onClick={() => setQ(null)}>
                Đóng câu hỏi
            </button>
        </div>
    </div>
)}
```

---

### PHẦN 2: Sửa `game-escape.html` (Hứng Trứng Vàng)

#### Bước 2.1: Tách riêng 2 Timer Ref (Tránh xung đột hủy nhầm timer)
Thay thế `const timeoutRef = useRef(null);` (dòng 154) bằng 2 ref độc lập:
```javascript
const fallTimerRef = useRef(null);
const nextTimerRef = useRef(null);
```

#### Bước 2.2: Sửa `useEffect` rơi trứng (Chỉ dọn dẹp `fallTimerRef`)
Thay thế `useEffect` từ dòng 240–252 bằng:
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

#### Bước 2.3: Sửa `handleCatch` (Sử dụng `nextTimerRef`)
Thay thế `handleCatch` (dòng 216–238) bằng:
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

#### Bước 2.4: Nâng cấp `goNext` (Tránh stale state closure)
Thay thế `goNext` (dòng 206–214) bằng:
```javascript
const goNext = useCallback((nextLives) => {
    if (nextLives <= 0) {
        setGameOver(true);
        return;
    }
    setQIndex(prevIndex => {
        if (prevIndex >= questions.length - 1) {
            setGameOver(true);
            return prevIndex;
        }
        const nextIndex = prevIndex + 1;
        resetRound(nextIndex, questions.length);
        return nextIndex;
    });
}, [questions.length, resetRound]);
```

#### Bước 2.5: Dọn dẹp cả 2 timer khi component unmount
Thay thế `useEffect` ở dòng 198–202 bằng:
```javascript
useEffect(() => {
    return () => {
        if (fallTimerRef.current) clearTimeout(fallTimerRef.current);
        if (nextTimerRef.current) clearTimeout(nextTimerRef.current);
    };
}, []);
```

---

## 3. Kế Hoạch Xác Minh (Verification Plan)
1. **Xác minh `game-treasure.html` (Đua Vịt):**
   - Mở modal "Câu hỏi kiểm tra", kiểm tra câu hỏi: `$A = 2x^2y \cdot (-3)xy^3$` và các đáp án `$-6x^3y^4$` $\rightarrow$ Hiển thị công thức toán học KaTeX sắc nét, không còn ký tự `$`.
2. **Xác minh `game-escape.html` (Hứng Trứng Vàng):**
   - Hứng đúng trứng câu 1 $\rightarrow$ Trứng nổ vàng, hiện thông báo chính xác $\rightarrow$ Sau 1.2s tự động chuyển sang câu 2, câu 3, câu 4 liên tục mượt mà.
   - Để trứng rơi mất mạng ở câu 1 $\rightarrow$ Sau 1.4s tự động chuyển tiếp sang câu 2 bình thường, không còn bị đứng yên.
