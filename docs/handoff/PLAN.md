# PLAN: Khắc Phục Hiển Thị Đáp Án Tức Thì Trong Game Đua Xe & Rung Chuông Vàng

## 1. Tổng Quan Nhiệm Vụ

Người dùng phản ánh:
> *"sao các trò chơi như đua xe, rung chuông vàng khi thí sinh chọn đáp án ko thấy nó hiển thị lên mà phải xong rồi mới hiển thị"*

### Nguyên nhân kỹ thuật:
1. **Trong `game-racing.html`**:
   - Các thẻ lựa chọn đáp án A, B, C, D hiện đang là các thẻ `<div>` tĩnh không có sự kiện `onClick`.
   - Cơ chế cũ chỉ cho phép giáo viên bấm tick tổ đúng (phím 1–6) mà không hề có giao diện cho từng tổ chọn đáp án A, B, C, D; khi học sinh hô hoặc chọn đáp án thì màn hình hoàn toàn không có phản hồi trực quan nào, chỉ khi bấm "Xác nhận bứt tốc" xong mới hiện đáp án đúng màu xanh.
2. **Trong `game-bell.html`**:
   - Các lựa chọn A, B, C, D cũng là các thẻ `<div>` tĩnh, không lưu state `selectedChoice`.
   - Khi thí sinh/người chơi bấm chọn A, B, C, D lúc đang đếm ngược, giao diện không có bất kỳ hiệu ứng chọn nào (không sáng viền, không đổi màu), phải đợi đến khi hết giờ (`answer === true`) mới đổi sang màu xanh.

### Mục tiêu cần đạt:
1. **`game-racing.html`**:
   - Thêm cơ chế chọn đáp án trực tiếp cho từng tổ: Mỗi tổ có hàng nút chọn đáp án nhanh `[ A ] [ B ] [ C ] [ D ]`. Khi bấm chọn, nút của tổ đó lập tức sáng rực theo màu sắc của tổ, hiển thị rõ ràng trên màn hình máy chiếu: *Tổ 1 chọn A*, *Tổ 2 chọn C*...
   - Click trực tiếp vào thẻ đáp án A, B, C, D để gán cho tổ đang chọn hoặc hiển thị danh sách các tổ đã chọn đáp án đó.
   - Khi hết giờ / Xác nhận bứt tốc: Tự động so khớp đáp án các tổ đã chọn với đáp án đúng (`currentQ.answer`), tổ đúng tự động bứt tốc Nitro, thẻ đúng hiện Xanh lục, thẻ sai đã chọn hiện Đỏ.
2. **`game-bell.html`**:
   - Biến các thẻ A, B, C, D thành nút tương tác bấm được (`<button>` hoặc `onClick`).
   - Thêm state `selectedChoice`: Khi bấm vào lựa chọn A, B, C, D, thẻ đó lập tức **sáng viền vàng hổ phách nổi bật** (`border-amber-400 bg-amber-500/30 scale-[1.02] shadow-xl`), có icon tích chọn và phát âm thanh click xác nhận.
   - Khi hết giờ / Hiện đáp án: Nếu đáp án đã chọn đúng $\rightarrow$ Đổi sang Xanh lục chiến thắng (`bg-emerald-600`); nếu sai $\rightarrow$ Đổi sang Đỏ (`bg-rose-600`) đồng thời thẻ đúng vẫn hiện Xanh lục để cả lớp cùng đối chiếu.
3. **`tests/game-suite-smoke.js`**: Bổ sung kiểm tra đảm bảo cả 2 game đều có cơ chế chọn và phản hồi đáp án tức thời.

---

## 2. Chi Tiết Thực Hiện Cho Coder

### PHẦN 1: Nâng Cấp Tương Tác Chọn Đáp Án Trong Game Đua Xe (`game-racing.html`)

Chỉnh sửa `game-racing.html`:

#### 1. Quản lý state đáp án của từng tổ:
Thêm state `teamAnswers` (lưu đáp án từng tổ đã chọn, ví dụ `{ t1: 0, t2: 2, t3: 0 }`):
```javascript
const [teamAnswers, setTeamAnswers] = useState({});
```
Khi chuyển câu hỏi mới (trong `startLights` hoặc chuyển `qIndex`):
```javascript
setTeamAnswers({});
```

#### 2. Hàm chọn đáp án cho tổ:
```javascript
const selectTeamChoice = (teamId, choiceIdx) => {
    if (phase !== 'play') return;
    soundEngine.tick();
    setTeamAnswers(prev => {
        const next = { ...prev };
        // Nếu bấm lại chính đáp án đó thì giữ nguyên hoặc đổi
        next[teamId] = choiceIdx;
        return next;
    });
};
```

#### 3. Cập nhật giao diện câu hỏi & các lựa chọn:
- Các thẻ đáp án A, B, C, D hiển thị huy hiệu các tổ đã chọn:
```javascript
<div className="grid md:grid-cols-2 gap-3 mb-4">
    {currentQ.choices.map((choice, idx) => {
        const choosingTeams = teams.filter(t => teamAnswers[t.id] === idx);
        const isCorrect = idx === currentQ.answer;
        let cardStyle = 'border-slate-600 bg-slate-800/60 hover:border-slate-500';
        
        if (phase === 'boost') {
            if (isCorrect) cardStyle = 'border-emerald-400 bg-emerald-900/50 shadow-emerald-500/30 shadow-lg';
            else if (choosingTeams.length > 0) cardStyle = 'border-rose-500 bg-rose-950/40 opacity-75';
        } else if (choosingTeams.length > 0) {
            cardStyle = 'border-amber-400 bg-slate-800 shadow-md ring-2 ring-amber-400/50';
        }

        return (
            <div key={idx} className={`p-3.5 rounded-2xl border-2 text-left transition-all relative ${cardStyle}`}>
                <div className="flex items-start justify-between gap-2">
                    <div>
                        <span className="font-black mr-2 text-amber-300 text-lg">{String.fromCharCode(65 + idx)}.</span>
                        <span className="font-semibold text-white"><MathText text={choice} /></span>
                    </div>
                    {phase === 'boost' && isCorrect && (
                        <span className="px-2 py-0.5 rounded-full bg-emerald-500 text-slate-950 text-xs font-black shrink-0">ĐÚNG ✓</span>
                    )}
                </div>

                {/* Huy hiệu các tổ đã chọn đáp án này */}
                {choosingTeams.length > 0 && (
                    <div className="mt-2.5 pt-2 border-t border-slate-700/60 flex flex-wrap gap-1.5 items-center">
                        <span className="text-[11px] text-slate-400 font-medium">Tổ đã chọn:</span>
                        {choosingTeams.map(t => (
                            <span key={t.id} className="px-2 py-0.5 rounded-full text-xs font-bold text-white shadow-sm flex items-center gap-1 animate-pulse"
                                style={{ backgroundColor: t.color }}>
                                🏎️ {t.short}
                            </span>
                        ))}
                    </div>
                )}
            </div>
        );
    })}
</div>
```

#### 4. Bảng điều khiển chọn đáp án nhanh cho từng tổ:
Thay thế khối tick tổ cũ bằng bảng chọn đáp án trực quan của từng tổ:
```javascript
<div className="bg-slate-950/60 border border-slate-800 rounded-2xl p-3.5 mb-4">
    <div className="flex justify-between items-center mb-2.5">
        <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
            🚦 Bảng ghi nhận đáp án các tổ (Bấm A, B, C, D khi tổ giơ bảng):
        </span>
        <span className="text-xs text-amber-300 font-semibold">
            Đã chọn: {Object.keys(teamAnswers).length}/{teams.length} tổ
        </span>
    </div>
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5">
        {teams.map((t) => {
            const picked = teamAnswers[t.id];
            return (
                <div key={t.id} className="bg-slate-900 border rounded-xl p-2.5 flex items-center justify-between gap-2"
                    style={{ borderColor: picked !== undefined ? t.color : '#334155' }}>
                    <span className="text-xs font-bold truncate max-w-[90px]" style={{ color: t.color }}>
                        {t.short}:
                    </span>
                    <div className="flex gap-1">
                        {[0, 1, 2, 3].map(cIdx => {
                            if (cIdx >= currentQ.choices.length) return null;
                            const isPicked = picked === cIdx;
                            return (
                                <button key={cIdx} type="button" disabled={phase !== 'play'}
                                    onClick={() => selectTeamChoice(t.id, cIdx)}
                                    className={`w-7 h-7 rounded-lg text-xs font-black transition-all ${
                                        isPicked
                                            ? 'text-white shadow-md scale-110'
                                            : 'bg-slate-800 text-slate-300 hover:bg-slate-700 border border-slate-700'
                                    }`}
                                    style={{ backgroundColor: isPicked ? t.color : undefined }}>
                                    {String.fromCharCode(65 + cIdx)}
                                </button>
                            );
                        })}
                    </div>
                </div>
            );
        })}
    </div>
</div>
```

#### 5. Cập nhật `confirmBoost`:
Trong hàm `confirmBoost`:
Tự động xác định tổ đúng dựa trên `teamAnswers`:
```javascript
// Thay vì đọc correctTeams cũ, xác định theo đáp án đã chọn:
teams.forEach(t => {
    const chosenChoice = teamAnswers[t.id];
    const ok = (chosenChoice !== undefined && chosenChoice === currentQ.answer);
    // ... xử lý bứt tốc xe như logic hiện có ...
});
```

---

### PHẦN 2: Nâng Cấp Tương Tác Chọn Đáp Án Trong Game Rung Chuông Vàng (`game-bell.html`)

Chỉnh sửa `game-bell.html`:

#### 1. Thêm state `selectedChoice`:
```javascript
const [selectedChoice, setSelectedChoice] = useState(null);
```
Khi chuyển câu mới (`next` hoặc reset):
```javascript
setSelectedChoice(null);
```

#### 2. Hàm chọn đáp án:
```javascript
const pickChoice = (index) => {
    if (answer) return; // Đã hết giờ/công bố thì không đổi nữa
    setSelectedChoice(index);
    bellSound(); // Âm thanh click nhẹ
};
```

#### 3. Render các thẻ A, B, C, D với phản hồi tức thì:
Thay thế khối `q.choices.map`:
```javascript
<div className="grid sm:grid-cols-2 gap-3 mb-5">
    {q.choices.map((choice, i) => {
        const isSelected = selectedChoice === i;
        const isCorrect = i === q.answer;
        let cardStyle = 'bg-slate-800/80 border-slate-700 hover:border-amber-400/60 hover:bg-slate-800';

        if (answer) {
            // Khi đã hiện đáp án:
            if (isCorrect) {
                cardStyle = 'bg-emerald-600 border-emerald-300 text-white font-black shadow-lg shadow-emerald-600/40 ring-2 ring-emerald-400';
            } else if (isSelected) {
                cardStyle = 'bg-rose-900/60 border-rose-500 text-rose-200 opacity-80';
            } else {
                cardStyle = 'bg-slate-900 border-slate-800 opacity-50';
            }
        } else if (isSelected) {
            // ĐANG ĐẾM GIỜ & THÍ SINH VỪA BẤM CHỌN: Hiển thị ngay lập tức!
            cardStyle = 'bg-amber-500/30 border-amber-400 text-white font-bold ring-2 ring-amber-400 shadow-xl scale-[1.02]';
        }

        return (
            <button key={i} type="button" onClick={() => pickChoice(i)}
                className={`rounded-2xl p-4 md:p-5 border-2 text-left transition-all flex items-start justify-between gap-3 ${cardStyle}`}>
                <div className="flex items-start gap-3">
                    <span className={`w-8 h-8 rounded-xl flex items-center justify-center font-black text-sm shrink-0 ${
                        answer && isCorrect
                            ? 'bg-white text-emerald-800'
                            : isSelected
                            ? 'bg-amber-400 text-slate-950 shadow'
                            : 'bg-slate-700 text-amber-300'
                    }`}>
                        {String.fromCharCode(65 + i)}
                    </span>
                    <span className="text-base md:text-lg leading-snug pt-0.5">
                        <MathText text={choice} />
                    </span>
                </div>
                {isSelected && !answer && (
                    <span className="px-2.5 py-1 rounded-full bg-amber-400 text-slate-950 font-black text-xs shrink-0 flex items-center gap-1 animate-pulse">
                        <i className="fa-solid fa-check"></i> ĐÃ CHỌN
                    </span>
                )}
                {answer && isCorrect && (
                    <span className="px-2.5 py-1 rounded-full bg-white text-emerald-700 font-black text-xs shrink-0 flex items-center gap-1">
                        <i className="fa-solid fa-crown"></i> ĐÁP ÁN ĐÚNG
                    </span>
                )}
            </button>
        );
    })}
</div>
```

#### 4. Phản hồi kết quả sau khi hiện đáp án:
Khi `answer === true`:
Hiển thị banner trạng thái ngay dưới câu hỏi:
- Nếu `selectedChoice === q.answer`: Banner màu xanh `"🎉 CHÚC MỪNG: Thí sinh đã trả lời CHÍNH XÁC!"`.
- Nếu `selectedChoice !== null && selectedChoice !== q.answer`: Banner màu đỏ `"❌ RẤT TIẾC: Thí sinh đã chọn sai đáp án!"`.

---

### PHẦN 3: Kiểm Thử Tự Động (`tests/game-suite-smoke.js`)

Bổ sung các kiểm tra trong `tests/game-suite-smoke.js`:
```javascript
// Kiểm tra Game Đua xe có cơ chế chọn đáp án từng tổ và highlight tức thì:
assert.match(racingHtml, /teamAnswers|selectTeamChoice/, 'game-racing.html phải có cơ chế ghi nhận đáp án cho từng tổ');
assert.match(racingHtml, /choosingTeams|Tổ đã chọn/, 'game-racing.html phải hiển thị huy hiệu tổ đã chọn đáp án ngay lập tức');

// Kiểm tra Game Rung chuông vàng có state lựa chọn và phản hồi tức thì:
assert.match(bellHtml, /selectedChoice|pickChoice/, 'game-bell.html phải có state selectedChoice để ghi nhận đáp án lập tức');
assert.match(bellHtml, /ĐÃ CHỌN|isSelected/, 'game-bell.html phải hiển thị nhãn/hiệu ứng ĐÃ CHỌN khi thí sinh bấm');
```

---

## 3. Kế Hoạch Kiểm Thử & Nghiệm Thu (Verification Plan)

1. **Chạy test tự động:**
   ```powershell
   node tests/game-suite-smoke.js
   node tests/change-password-smoke.js
   node tests/canvas-tabs-permissions-smoke.js
   ```
2. **Kiểm tra trực quan trong `game-racing.html`:**
   - Mở `game-racing.html`:
   - Bấm bắt đầu đua $\rightarrow$ Trong lúc đồng hồ đang chạy, bấm nút `A`, `B`, `C` hoặc `D` của Tổ 1, Tổ 2:
   - **Kỳ vọng**: Nút lập tức sáng đèn màu của tổ, thẻ đáp án tương ứng hiển thị ngay huy hiệu `🏎️ Tổ 1`, `🏎️ Tổ 2`.
   - Bấm "Xác nhận bứt tốc" $\rightarrow$ Tổ chọn đúng bứt tốc Nitro, thẻ đúng hiện xanh, thẻ sai hiện đỏ.
3. **Kiểm tra trực quan trong `game-bell.html`:**
   - Mở `game-bell.html`:
   - Bấm "Bắt đầu đếm giờ" $\rightarrow$ Click vào lựa chọn `A` hoặc `B`:
   - **Kỳ vọng**: Lựa chọn lập tức sáng viền vàng rực rỡ, hiện huy hiệu `✓ ĐÃ CHỌN`, phát âm thanh click xác nhận.
   - Khi bấm "Hết giờ · hiện đáp án" $\rightarrow$ Hiện xanh đáp án đúng, kiểm tra đối chiếu chuẩn xác.
