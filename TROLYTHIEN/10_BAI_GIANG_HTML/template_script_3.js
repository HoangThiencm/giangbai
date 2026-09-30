
  let currentSlideIndex = 1;
  let currentStep = 0;
  let isDesignMode = false;
  let activeEditBlockId = null;
  let currentLang = 'vi';

  const slides = document.querySelectorAll('.slide-item');
  const totalSlides = slides.length;

  // Bảng từ điển cụm từ học thuật chuyển ngữ chuẩn xác
  const contentPhraseMap = [
    ['• Nhận dạng và giải thành thạo <b>phương trình tích</b>: $(ax+b)(cx+d) = 0$.', '• Fluently identify and solve <b>product equations</b>: $(ax+b)(cx+d) = 0$.'],
    ['• Giải <b>phương trình chứa ẩn ở mẫu</b> và kỹ năng loại nghiệm ngoại lai.', '• Solve <b>rational equations</b> and reject extraneous roots.'],
    ['• Ứng dụng giải quyết các bài toán thực tiễn hình học và năng suất.', '• Apply equations to practical geometry and work-rate problems.'],
    ['Trong một khu vườn hình vuông có cạnh bằng $15\\text{ m}$, người ta làm một lối đi xung quanh vườn có bề rộng là $x\\text{ (m)}$ (Hình 2.1).', 'In a square garden with side length $15\\text{ m}$, a surrounding pathway is made with width $x\\text{ (m)}$ (Figure 2.1).'],
    ['Để diện tích phần đất còn lại là $169\\text{ m}^2$ thì bề rộng $x$ của lối đi là bao nhiêu?', 'What is the pathway width $x$ so that the remaining garden area is $169\\text{ m}^2$?'],
    ['Chiều dài và chiều rộng phần đất còn lại theo $x$ là: $15 - 2x\\text{ (m)}$.', 'The length and width of the remaining land in $x$ are: $15 - 2x\\text{ (m)}$.'],
    ['Phương trình diện tích: $(15 - 2x)^2 = 169$.', 'Area equation: $(15 - 2x)^2 = 169$.'],
    ['Làm thế nào để giải phương trình này một cách dễ dàng?', 'How can we solve this equation easily?'],
    ['Phân tích đa thức $P(x) = (x+1)(2x-1) + (x+1)x$ thành nhân tử.', 'Factor the polynomial $P(x) = (x+1)(2x-1) + (x+1)x$ into linear factors.'],
    ['Giải phương trình $P(x) = 0$ ta được $(x+1)(3x-1) = 0$.', 'Solving equation $P(x) = 0$ yields $(x+1)(3x-1) = 0$.'],
    ['Một tích bằng $0$ khi và chỉ khi ít nhất một thừa số bằng $0$.', 'A product equals $0$ if and only if at least one factor equals $0$.'],
    ['Phương trình tích là phương trình có dạng:', 'A product equation is an equation of the form:'],
    ['Để giải phương trình $(ax + b)(cx + d) = 0$, ta giải hai phương trình:', 'To solve $(ax + b)(cx + d) = 0$, solve two linear equations:'],
    ['Sau đó lấy tất cả các nghiệm của chúng.', 'Then take all of their solutions.'],
    ['1. Chuyển vế: Chuyển tất cả các hạng tử sang vế trái để vế phải bằng $0$.', '1. Transpose: Move all terms to the left-hand side so the right side is $0$.'],
    ['2. Phân tích vế trái: Đặt nhân tử chung, dùng hằng đẳng thức hoặc nhóm hạng tử.', '2. Factor: Use common factors, identities, or grouping on the left-hand side.'],
    ['Bước 1: Tìm điều kiện xác định (ĐKXĐ) của phương trình.', 'Step 1: Find domain restrictions (constraints) of the equation.'],
    ['Bước 2: Quy đồng mẫu hai vế rồi khử mẫu.', 'Step 2: Clear denominators using the LCD.'],
    ['Bước 3: Giải phương trình vừa tìm được.', 'Step 3: Solve the resulting equation.'],
    ['Bước 4 (Kết luận): Trong các giá trị tìm được ở Bước 3, giá trị nào <b>thỏa mãn ĐKXĐ</b> chính là nghiệm của phương trình đã cho.', 'Step 4 (Conclusion): Among values found in Step 3, those that <b>satisfy constraints</b> are solutions of the equation.'],
    ['⚠️ Bước 4 là bước quyết định!', '⚠️ Step 4 is the decisive step!'],
    ['Nếu không đối chiếu với ĐKXĐ thì rất dễ nhận nhầm \'nghiệm ngoại lai\'', 'Without constraint check, extraneous roots will be mistakenly accepted'],
    ['Tại sao giải ra $x = 2$ mà lại kết luận phương trình vô nghiệm?', 'Why is the equation concluded to have no solution despite finding $x = 2$?'],
    ['Vì tại $x = 2$, mẫu số $(x - 2) = 0$, phân thức không xác định!', 'Because at $x = 2$, denominator $(x - 2) = 0$, the expression is undefined!'],
    ['Nhận xét nhân tử chung là', 'Notice that the common factor is'],
    ['Lời giải chi tiết:', 'Detailed solution:'],
    ['Lời giải mẫu:', 'Worked solution:'],
    ['Lời giải:', 'Solution:'],
    ['Đề bài:', 'Problem statement:'],
    ['Đáp án & Giải thích:', 'Answer & Explanation:'],
    ['Đáp án đúng:', 'Correct answer:'],
    ['Đáp án:', 'Answer:'],
    ['Nhận xét:', 'Note / Observation:'],
    ['Chú ý:', 'Note:'],
    ['Lưu ý:', 'Important note:'],
    ['Định nghĩa:', 'Definition:'],
    ['Cách giải:', 'Solution method:'],
    ['Kết luận:', 'Conclusion:'],
    ['thỏa mãn ĐKXĐ', 'satisfies constraints'],
    ['không thỏa mãn ĐKXĐ', 'violates constraints'],
    ['thỏa mãn', 'satisfies (valid)'],
    ['bị loại', 'rejected (extraneous)'],
    ['vô nghiệm', 'has no solution'],
    ['Vậy phương trình có hai nghiệm là', 'Thus the equation has two solutions:'],
    ['Vậy phương trình có hai nghiệm', 'Thus the equation has two solutions:'],
    ['Vậy phương trình có nghiệm là', 'Thus the equation has solution:'],
    ['Vậy phương trình có nghiệm duy nhất là', 'Thus the equation has a unique solution:'],
    ['Vậy nghiệm của phương trình là', 'Thus the solution is'],
    ['Đối chiếu ĐKXĐ:', 'Checking constraints:'],
    ['Điều kiện xác định (ĐKXĐ):', 'Domain restrictions (Constraints):'],
    ['Điều kiện xác định:', 'Domain restrictions:'],
    ['ĐKXĐ:', 'Constraints:'],
    ['Mẫu chung:', 'Least Common Denominator (LCD):'],
    ['Chúc các em học tập tốt!', 'Wish you productive learning!'],
    ['hoặc', 'or'],
    ['và', 'and']
  ];

  const termMap = [
    ['phương trình tích', 'product equation'],
    ['phương trình chứa ẩn ở mẫu', 'rational equation'],
    ['điều kiện xác định', 'domain restrictions'],
    ['ĐKXĐ', 'constraints'],
    ['mẫu thức chung', 'least common denominator'],
    ['nhân tử chung', 'common factor'],
    ['thừa số', 'factor'],
    ['nghiệm của phương trình', 'root of the equation'],
    ['nghiệm ngoại lai', 'extraneous root'],
    ['vô nghiệm', 'no solution'],
    ['thỏa mãn', 'satisfies'],
    ['bị loại', 'rejected'],
    ['chiều dài', 'length'],
    ['chiều rộng', 'width'],
    ['diện tích', 'area'],
    ['hình vuông', 'square'],
    ['hình chữ nhật', 'rectangle'],
    ['khu vườn', 'garden'],
    ['lối đi', 'pathway'],
    ['ngôi nhà', 'house'],
    ['sân vườn', 'garden'],
    ['mảnh đất', 'plot of land'],
    ['Bước 1', 'Step 1'],
    ['Bước 2', 'Step 2'],
    ['Bước 3', 'Step 3'],
    ['Bước 4', 'Step 4'],
    ['Ví dụ', 'Example'],
    ['Luyện tập', 'Practice'],
    ['Vận dụng', 'Application'],
    ['Lời giải', 'Solution'],
    ['Hướng dẫn', 'Guide'],
    ['Đáp án', 'Answer'],
    ['Nhận xét', 'Note'],
    ['Chú ý', 'Note'],
    ['Kết luận', 'Conclusion'],
    ['Vậy', 'Therefore']
  ];

  /* ==========================================================================
     ĐIỀU KHIỂN CỠ CHỮ TRÌNH CHIẾU TV LỚP HỌC (28px - 30px)
     ========================================================================== */
  const fontSizes = [
    { label: '🔤 TV 28px', size: '28px', title: '30px', heading: '32px', tag: '22px' },
    { label: '🔤 TV Lớn 30px', size: '30px', title: '32px', heading: '34px', tag: '24px' },
    { label: '🔤 Laptop 22px', size: '22px', title: '24px', heading: '26px', tag: '18px' }
  ];
  let curFontIdx = 0; // Mặc định 28px chuẩn TV phòng học

  function applyFontSize(idx) {
    curFontIdx = idx % fontSizes.length;
    const cfg = fontSizes[curFontIdx];
    document.documentElement.style.setProperty('--content-font-size', cfg.size);
    document.documentElement.style.setProperty('--title-font-size', cfg.title);
    document.documentElement.style.setProperty('--heading-font-size', cfg.heading);
    document.documentElement.style.setProperty('--tag-font-size', cfg.tag);
    const btn = document.getElementById('btnFontSize');
    if (btn) btn.textContent = cfg.label;
    try {
      localStorage.setItem('lecture_font_idx', String(curFontIdx));
    } catch (e) {}
    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise().catch(() => {});
    }
  }

  function cycleFontSize() {
    applyFontSize((curFontIdx + 1) % fontSizes.length);
    showToast(`Đã chuyển cỡ chữ: ${fontSizes[curFontIdx].label}`);
  }
  /* ==========================================================================
     TRỢ GIẢNG AI: PHÁT ÂM TIẾNG ANH CHẬM RÃI (TEXT-TO-SPEECH FOR STUDENTS)
     ========================================================================== */
  let isSlideSpeechActive = false;
  let cachedEnglishVoice = null;

  const speechRates = [
    { label: '⚡ 0.85x', rate: 0.85, name: 'Chậm vừa' },
    { label: '⚡ 0.75x', rate: 0.75, name: 'Rất chậm' },
    { label: '⚡ 0.5x',  rate: 0.5,  name: 'Siêu chậm' },
    { label: '⚡ 1.0x',  rate: 1.0,  name: 'Tự nhiên' }
  ];
  let curSpeechRateIdx = 0;

  function showCaptionHelp() {
    alert(
      "💡 HƯỚNG DẪN TẮT PHỤ ĐỀ TỰ ĐỘNG (LIVE CAPTIONS):\n\n" +
      "Hộp màu đen phụ đề xuất hiện trên màn hình là tính năng Live Caption có sẵn của Windows hoặc Google Chrome khi máy tính phát âm thanh:\n\n" +
      "1. Cách nhanh nhất (Windows 11): Nhấn phím tắt [ Windows + Ctrl + L ] để TẮT ngay lập tức hộp phụ đề.\n" +
      "2. Trong Google Chrome: Bấm biểu tượng Nốt nhạc 🎵 (Điều khiển phương tiện) ở góc trên bên phải thanh địa chỉ → Gạt TẮT 'Phụ đề trực tiếp' (Live Caption).\n" +
      "3. Hoặc vào Cài đặt Chrome → Hỗ trợ tiếp cận (Accessibility) → Tắt 'Phụ đề trực tiếp'."
    );
  }

  function applySpeechRate(idx) {
    curSpeechRateIdx = idx % speechRates.length;
    const cfg = speechRates[curSpeechRateIdx];
    const btn = document.getElementById('btnSpeechRate');
    if (btn) btn.textContent = cfg.label;
    try {
      localStorage.setItem('lecture_speech_rate_idx', String(curSpeechRateIdx));
    } catch (e) {}
  }

  function cycleSpeechRate() {
    applySpeechRate((curSpeechRateIdx + 1) % speechRates.length);
    showToast(`Tốc độ đọc: ${speechRates[curSpeechRateIdx].name} (${speechRates[curSpeechRateIdx].label})`);
    if (window.speechSynthesis && window.speechSynthesis.speaking) {
      stopAllSpeech();
    }
  }

  function stopAllSpeech() {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    isSlideSpeechActive = false;
    document.querySelectorAll('.is-speaking').forEach(el => el.classList.remove('is-speaking'));
    document.querySelectorAll('.btn-block-speak').forEach(btn => {
      btn.classList.remove('is-speaking');
      btn.textContent = '🔊';
    });
    const btn = document.getElementById('btnReadSlideEn');
    if (btn) {
      btn.textContent = (currentLang === 'en') ? '🔊 Read Slide (EN)' : '🔊 Đọc Slide (EN)';
      btn.classList.remove('is-active');
    }
  }

  function mathToSpokenEnglish(text) {
    if (!text) return '';
    let t = text.replace(/<br\s*[\/]?>/gi, '. ');
    t = t.replace(/<\/?(?:b|strong|span|div|i|em|p|ul|ol|li)[^>]*>/gi, ' ');

    // Chuẩn hóa trước các đơn vị đo lường (m2, m, cm, km, h)
    t = t.replace(/\\text\{\s*\(\s*m\s*\)\s*\}/gi, ' in meters');
    t = t.replace(/\\text\{\s*m\s*\}\^2/gi, ' square meters');
    t = t.replace(/\\text\{\s*m\s*\^2\s*\}/gi, ' square meters');
    t = t.replace(/\\text\{\s*m\s*\}/gi, ' meters');
    t = t.replace(/\\text\{\s*cm\s*\}\^2/gi, ' square centimeters');
    t = t.replace(/\\text\{\s*km\s*\}\^2/gi, ' square kilometers');
    t = t.replace(/\\text\{\s*cm\s*\}/gi, ' centimeters');
    t = t.replace(/\\text\{\s*km\s*\}/gi, ' kilometers');
    t = t.replace(/\\text\{\s*h\s*\}/gi, ' hours');

    function replMath(match, p1) {
      let math = p1;
      // Hàm số P(x) -> P of x
      math = math.replace(/\b([Pfgkh])\(([a-zA-Z0-9]+)\)/g, '$1 of $2');
      // Lũy thừa
      math = math.replace(/([a-zA-Z0-9]+)\^2\b/g, '$1 squared');
      math = math.replace(/([a-zA-Z0-9]+)\^3\b/g, '$1 cubed');
      math = math.replace(/\^\{([^}]+)\}/g, ' to the power of $1');
      // Phân số
      math = math.replace(/\\frac\{([^}]+)\}\{([^}]+)\}/g, ' $1 over $2 ');
      // Ký hiệu tương đương, suy ra, quan hệ
      math = math.replace(/\\Leftrightarrow/g, ' is equivalent to ');
      math = math.replace(/\\Rightarrow/g, ' implies that ');
      math = math.replace(/\\ne(?:q)?/g, ' is not equal to ');
      math = math.replace(/\\le(?:q)?/g, ' is less than or equal to ');
      math = math.replace(/\\ge(?:q)?/g, ' is greater than or equal to ');
      math = math.replace(/\\pm/g, ' plus or minus ');
      math = math.replace(/\\(?:cdot|times)/g, ' times ');
      math = math.replace(/\\approx/g, ' approximately equals ');
      math = math.replace(/\\in/g, ' belongs to ');

      // Dấu ngoặc đơn
      math = math.replace(/\(/g, ' open parenthesis ');
      math = math.replace(/\)/g, ' close parenthesis ');

      // Phép toán
      math = math.replace(/=/g, ' equals ');
      math = math.replace(/\+/g, ' plus ');
      math = math.replace(/-/g, ' minus ');
      math = math.replace(/\*/g, ' times ');
      math = math.replace(/\//g, ' divided by ');

      math = math.replace(/\\text\{([^}]+)\}/g, ' $1 ');
      math = math.replace(/\\/g, ' ');
      return ' ' + math + ' ';
    }

    t = t.replace(/\$\$([\s\S]*?)\$\$/g, replMath);
    t = t.replace(/\$([^$]+)\$/g, replMath);
    t = t.replace(/[•●▪]/g, '. ');
    t = t.replace(/⚠️/g, ' Note: ');
    t = t.replace(/[📌✍️]/g, '');
    t = t.replace(/\s*([,\.!?;:])\s*/g, '$1 ');
    t = t.replace(/\s+/g, ' ').trim();
    return t;
  }

  function getEnglishVoice() {
    if (!('speechSynthesis' in window)) return null;
    if (cachedEnglishVoice) return cachedEnglishVoice;
    const voices = window.speechSynthesis.getVoices();
    cachedEnglishVoice = voices.find(v => v.lang.startsWith('en') && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('Aria') || v.name.includes('Jenny') || v.name.includes('Samantha') || v.name.includes('Online')))
      || voices.find(v => v.lang.startsWith('en') && (v.lang === 'en-US' || v.lang === 'en-GB'))
      || voices.find(v => v.lang.startsWith('en'))
      || null;
    return cachedEnglishVoice;
  }

  if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
    window.speechSynthesis.onvoiceschanged = () => {
      cachedEnglishVoice = null;
      getEnglishVoice();
    };
  }

  function speakText(text, onStart, onEnd) {
    if (!('speechSynthesis' in window)) {
      showToast('Trình duyệt không hỗ trợ Web Speech API.');
      if (onEnd) onEnd();
      return;
    }
    window.speechSynthesis.cancel();
    if (!text || !text.trim()) {
      if (onEnd) onEnd();
      return;
    }
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = 'en-US';
    const voice = getEnglishVoice();
    if (voice) utter.voice = voice;
    utter.rate = speechRates[curSpeechRateIdx].rate; // Tốc độ điều chỉnh: 0.85x ⇄ 0.75x ⇄ 1.0x
    utter.pitch = 1.0;

    utter.onstart = () => { if (onStart) onStart(); };
    utter.onend = () => { if (onEnd) onEnd(); };
    utter.onerror = () => { if (onEnd) onEnd(); };

    window.speechSynthesis.speak(utter);
  }

  function speakBlockEn(blockEl, onFinished, ev) {
    if (ev) ev.stopPropagation();
    if (!blockEl) return;
    const btnSpeak = blockEl.querySelector('.btn-block-speak');
    
    // Nếu khối này đang đọc, bấm lại thì dừng
    if (blockEl.classList.contains('is-speaking') && !onFinished) {
      stopAllSpeech();
      return;
    }

    stopAllSpeech();

    // Tự động chuyển màn hình sang Tiếng Anh để chữ trên màn hình khớp 100% với giọng đọc!
    if (currentLang === 'vi') {
      toggleLanguage();
    }

    const titleEn = blockEl.getAttribute('data-title-en') || (blockEl.querySelector('strong') ? blockEl.querySelector('strong').textContent : '');
    const rawEn = blockEl.getAttribute('data-raw-en') || (blockEl.querySelector('.block-body') ? blockEl.querySelector('.block-body').innerHTML : '');

    const spokenTitle = mathToSpokenEnglish(titleEn);
    const spokenBody = mathToSpokenEnglish(rawEn);
    const fullSpoken = (spokenTitle ? spokenTitle + '. ' : '') + spokenBody;

    speakText(fullSpoken, () => {
      blockEl.classList.add('is-speaking');
      if (btnSpeak) {
        btnSpeak.classList.add('is-speaking');
        btnSpeak.textContent = '⏹';
      }
    }, () => {
      blockEl.classList.remove('is-speaking');
      if (btnSpeak) {
        btnSpeak.classList.remove('is-speaking');
        btnSpeak.textContent = '🔊';
      }
      if (onFinished) onFinished();
    });
  }

  function toggleReadSlideEn() {
    const btn = document.getElementById('btnReadSlideEn');
    if (isSlideSpeechActive || (window.speechSynthesis && window.speechSynthesis.speaking)) {
      stopAllSpeech();
      return;
    }

    // Tự động chuyển màn hình sang Tiếng Anh để chữ trên slide khớp 100% với lời đọc!
    if (currentLang === 'vi') {
      toggleLanguage();
    }

    const curSlide = getCurrentSlide();
    if (!curSlide) return;

    isSlideSpeechActive = true;
    if (btn) {
      btn.textContent = (currentLang === 'en') ? '⏹ Stop Reading' : '⏹ Dừng đọc';
      btn.classList.add('is-active');
    }

    // Lấy tiêu đề slide tiếng Anh
    const headingEl = curSlide.querySelector('.slide-heading-text');
    const origHeading = headingEl ? (headingEl.getAttribute('data-orig-heading') || headingEl.textContent.trim()) : '';
    const headingEn = (typeof headingMap !== 'undefined' && headingMap[origHeading]) ? headingMap[origHeading] : origHeading;
    const spokenHeading = mathToSpokenEnglish(headingEn);

    // Lấy các khối hiển thị trong slide
    const blocks = Array.from(curSlide.querySelectorAll('.content-block')).filter(b => {
      if (isDesignMode) return true;
      return b.classList.contains('is-revealed') || (!b.hasAttribute('data-step') || b.getAttribute('data-step') === '0');
    });

    let queue = [];
    if (spokenHeading) {
      queue.push({ type: 'heading', text: spokenHeading });
    }
    blocks.forEach(b => {
      queue.push({ type: 'block', el: b });
    });

    let qIdx = 0;
    function playNext() {
      if (!isSlideSpeechActive || qIdx >= queue.length) {
        stopAllSpeech();
        return;
      }
      const item = queue[qIdx++];
      if (item.type === 'heading') {
        speakText(item.text, null, playNext);
      } else if (item.type === 'block') {
        speakBlockEn(item.el, playNext);
      }
    }

    playNext();
  }

  function toggleAnswer(btn) {
    if (!btn) return;
    const box = btn.closest('.toggle-answer-box');
    if (!box) return;
    const content = box.querySelector('.toggle-answer-content');
    const icon = btn.querySelector('.toggle-icon');
    if (!content) return;
    const isShown = content.classList.toggle('show');
    if (icon) {
      if (currentLang === 'en') {
        icon.textContent = isShown ? '▲ Hide' : '▼ Show';
      } else {
        icon.textContent = isShown ? '▲ Ẩn' : '▼ Hiện';
      }
    }
    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise([content]).catch(() => {});
    }
  }

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
    } else {
      if (document.exitFullscreen) document.exitFullscreen();
    }
  }

  function createDesignOverlayHTML(bid, step) {
    const stepLabel = (step !== undefined && step > 0) ? step : 'Cố định';
    return `
      <div class="design-overlay">
        <span class="drag-handle" title="Giữ chuột và kéo để di chuyển khối lên/xuống hoặc sang cột khác">⠿</span>
        <span class="badge-step-num" onclick="setBlockStepDirect('${bid}')" title="Click để nhập số bước">${stepLabel}</span>
        <button class="btn-step-order" onclick="moveBlockPosition('${bid}', -1)" title="Di chuyển khối lên trên">▲</button>
        <button class="btn-step-order" onclick="moveBlockPosition('${bid}', 1)" title="Di chuyển khối xuống dưới">▼</button>
        <button class="btn-block-action btn-edit-block" onclick="openEditModal('${bid}')" title="Sửa nội dung khối">✏️ Sửa</button>
        <button class="btn-block-action btn-exit-step" onclick="setBlockExitStep('${bid}')">💨 Biến mất</button>
        <button class="btn-block-action btn-anim-block" onclick="addAnimToSelection('${bid}')" title="Bôi đen đoạn văn bản rồi bấm để thêm hiệu ứng xuất hiện">✨ Hiệu ứng</button>
        <button class="btn-block-action" onclick="toggleBlockWait('${bid}')">👁️/⏱</button>
        <button class="btn-block-action btn-del-block" onclick="deleteBlock('${bid}')">✕</button>
      </div>
    `;
  }

  /* Tự động dịch thông minh bảo tồn chính xác dấu câu của người dùng (dấu 2 chấm, chấm, phẩy...) */
  function smartTranslateText(vnHtml) {
    if (!vnHtml) return '';
    let result = vnHtml;

    // 1. Cụm từ và câu học thuật (linh hoạt dấu câu)
    for (const [vi, en] of contentPhraseMap) {
      const cleanVi = vi.replace(/[:\.\?!;,\s]+$/, '');
      const cleanEn = en.replace(/[:\.\?!;,\s]+$/, '');
      if (!cleanVi) continue;

      const escaped = cleanVi.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const reg = new RegExp(escaped + '([:\\.\\?!;,\\s]*)', 'gi');
      result = result.replace(reg, (match, trailingPunct) => {
        return cleanEn + trailingPunct;
      });
    }

    // 2. Thuật ngữ toán học cốt lõi (sử dụng boundary tương thích tiếng Việt Unicode)
    for (const [viTerm, enTerm] of termMap) {
      const esc = viTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const reg = new RegExp('(?<![\\p{L}\\p{N}])' + esc + '(?![\\p{L}\\p{N}])([:\\.\\?!;,\\s]*)', 'gui');
      result = result.replace(reg, (match, punct) => {
        return enTerm + punct;
      });
    }

    return result;
  }

  function toggleLanguage() {
    currentLang = (currentLang === 'vi') ? 'en' : 'vi';
    const isEn = (currentLang === 'en');

    // Nút trợ giảng đọc tiếng Anh
    const readBtn = document.getElementById('btnReadSlideEn');
    if (readBtn && !isSlideSpeechActive) {
      readBtn.textContent = isEn ? '🔊 Read Slide (EN)' : '🔊 Đọc Slide (EN)';
    }
    const rateBtn = document.getElementById('btnSpeechRate');
    if (rateBtn) {
      rateBtn.title = isEn ? 'Change speech rate: 0.85x (Slow) ⇄ 0.75x (Very slow) ⇄ 1.0x (Normal)' : 'Đổi tốc độ đọc: 0.85x (Chậm vừa) ⇄ 0.75x (Rất chậm) ⇄ 1.0x (Tự nhiên)';
    }

    // Nút chuyển ngữ
    const btnLang = document.getElementById('btnToggleLang');
    if (btnLang) {
      btnLang.textContent = isEn ? '🇻🇳 Chuyển Tiếng Việt' : '🌐 Song ngữ (VI/EN)';
      btnLang.style.background = isEn ? '#4338ca' : '';
    }

    // Các nút điều khiển
    const prevSlideBtn = document.querySelector('button[onclick="prevSlide()"]');
    if (prevSlideBtn) prevSlideBtn.textContent = isEn ? '◀ Prev Slide' : '◀ Trang trước';
    const prevStepBtn = document.querySelector('button[onclick="prevStep()"]');
    if (prevStepBtn) prevStepBtn.textContent = isEn ? '↩ Step Back' : '↩ Lùi 1 bước';
    const nextStepBtn = document.querySelector('button[onclick="nextStep()"]');
    if (nextStepBtn) nextStepBtn.textContent = isEn ? '↪ Next Step' : '↪ Tiến 1 bước';
    const nextSlideBtn = document.querySelector('button[onclick="nextSlide()"]');
    if (nextSlideBtn) nextSlideBtn.textContent = isEn ? '▶ Next Slide' : '▶ Trang sau';
    const fullBtn = document.querySelector('button[onclick="toggleFullscreen()"]');
    if (fullBtn) fullBtn.textContent = isEn ? '⛶ Fullscreen' : '⛶ Toàn màn hình';
    const saveBtn = document.getElementById('btnSaveLecture');
    if (saveBtn) saveBtn.textContent = isEn ? '💾 Save Lecture' : '💾 Lưu bài giảng';
    const modeBtn = document.getElementById('btnToggleMode');
    if (modeBtn) {
      if (isDesignMode) {
        modeBtn.textContent = isEn ? '🎬 Present' : '🎬 Trình chiếu';
      } else {
        modeBtn.textContent = isEn ? '⚙ Design' : '⚙ Thiết kế';
      }
    }

    // Nhãn cột tinh gọn
    document.querySelectorAll('.col-board-tag').forEach(el => {
      el.textContent = isEn ? '📌 LESSON BOARD' : '📌 PHẦN GHI BẢNG';
    });
    document.querySelectorAll('.col-task-tag').forEach(el => {
      el.textContent = isEn ? '✍️ LEARNING ACTIVITIES' : '✍️ HOẠT ĐỘNG HỌC TẬP';
    });

    // Tiêu đề bài học
    document.querySelectorAll('.slide-lesson-title').forEach(el => {
      el.textContent = isEn ? 'LESSON 4: EQUATIONS REDUCIBLE TO LINEAR EQUATIONS' : 'BÀI 4: PHƯƠNG TRÌNH QUY VỀ PHƯƠNG TRÌNH BẬC NHẤT MỘT ẨN';
    });

    // Tiêu đề 26 heading slide
    const headingMap = {
      'KHỞI ĐỘNG — TÌNH HUỐNG THỰC TẾ': 'WARM-UP — REAL-WORLD SITUATION',
      '1. PHƯƠNG TRÌNH TÍCH — HOẠT ĐỘNG KHÁM PHÁ': '1. PRODUCT EQUATIONS — EXPLORATION ACTIVITY',
      '1. PHƯƠNG TRÌNH TÍCH — ĐỊNH NGHĨA & CÁCH GIẢI': '1. PRODUCT EQUATIONS — DEFINITION & METHOD',
      '1. PHƯƠNG TRÌNH TÍCH — VÍ DỤ 1 (ÁP DỤNG TRỰC TIẾP)': '1. PRODUCT EQUATIONS — EXAMPLE 1 (DIRECT APPLICATION)',
      '1. PHƯƠNG TRÌNH TÍCH — VÍ DỤ 2 (ĐƯA VỀ DẠNG TÍCH)': '1. PRODUCT EQUATIONS — EXAMPLE 2 (FACTORING INTO PRODUCT)',
      '1. PHƯƠNG TRÌNH TÍCH — NHẬN XÉT PHƯƠNG PHÁP CHUNG': '1. PRODUCT EQUATIONS — GENERAL METHOD SUMMARY',
      '1. PHƯƠNG TRÌNH TÍCH — LUYỆN TẬP 1 (CÂU A)': '1. PRODUCT EQUATIONS — PRACTICE 1 (PART A)',
      '1. PHƯƠNG TRÌNH TÍCH — LUYỆN TẬP 1 (CÂU B)': '1. PRODUCT EQUATIONS — PRACTICE 1 (PART B)',
      '1. PHƯƠNG TRÌNH TÍCH — VẬN DỤNG & KẾT THÚC TIẾT 1': '1. PRODUCT EQUATIONS — APPLICATION & PERIOD 1 WRAP-UP',
      '2. PHƯƠNG TRÌNH CHỨA ẨN Ở MẪU — KHÁM PHÁ HĐ3 & HĐ4': '2. RATIONAL EQUATIONS — EXPLORATION ACTIVITIES 3 & 4',
      '2. PHƯƠNG TRÌNH CHỨA ẨN Ở MẪU — ĐIỀU KIỆN XÁC ĐỊNH (ĐKXĐ)': '2. RATIONAL EQUATIONS — DOMAIN RESTRICTIONS (CONSTRAINTS)',
      '2. PHƯƠNG TRÌNH CHỨA ẨN Ở MẪU — VÍ DỤ 3 (TÌM ĐKXĐ)': '2. RATIONAL EQUATIONS — EXAMPLE 3 (FINDING CONSTRAINTS)',
      '2. PHƯƠNG TRÌNH CHỨA ẨN Ở MẪU — LUYỆN TẬP 2': '2. RATIONAL EQUATIONS — PRACTICE 2',
      '2. PHƯƠNG TRÌNH CHỨA ẨN Ở MẪU — KHÁM PHÁ HĐ5 (CÁCH GIẢI)': '2. RATIONAL EQUATIONS — EXPLORATION ACTIVITY 5 (METHOD)',
      '2. PHƯƠNG TRÌNH CHỨA ẨN Ở MẪU — BỐN BƯỚC GIẢI CHUẨN': '2. RATIONAL EQUATIONS — 4 STANDARD SOLUTION STEPS',
      '2. PHƯƠNG TRÌNH CHỨA ẨN Ở MẪU — VÍ DỤ 4 (LOẠI NGHIỆM)': '2. RATIONAL EQUATIONS — EXAMPLE 4 (REJECTING EXTRANEOUS ROOT)',
      '2. PHƯƠNG TRÌNH CHỨA ẨN Ở MẪU — LUYỆN TẬP 3 (PHÂN TÍCH)': '2. RATIONAL EQUATIONS — PRACTICE 3 (ANALYSIS)',
      '2. PHƯƠNG TRÌNH CHỨA ẨN Ở MẪU — LUYỆN TẬP 3 (GIẢI & KẾT LUẬN)': '2. RATIONAL EQUATIONS — PRACTICE 3 (SOLVE & CONCLUDE)',
      'TIẾT 3: LUYỆN TẬP TỔNG HỢP & ỨNG DỤNG THỰC TẾ': 'PERIOD 3: GENERAL PRACTICE & REAL-WORLD APPLICATIONS',
      'BÀI TẬP 2.1 (SGK TR.30) — PHƯƠNG TRÌNH TÍCH': 'EXERCISE 2.1 (TEXTBOOK P.30) — PRODUCT EQUATIONS',
      'BÀI TẬP 2.2 (SGK TR.30) — BIẾN ĐỔI ĐƯA VỀ TÍCH': 'EXERCISE 2.2 (TEXTBOOK P.30) — FACTORING METHOD',
      'BÀI TẬP 2.3A (SGK TR.30) — PHƯƠNG TRÌNH CHỨA ẨN Ở MẪU': 'EXERCISE 2.3A (TEXTBOOK P.30) — RATIONAL EQUATIONS',
      'BÀI TẬP 2.3B (SGK TR.30) — ÁP DỤNG HẰNG ĐẲNG THỨC TỔNG HAI LẬP PHƯƠNG': 'EXERCISE 2.3B (TEXTBOOK P.30) — SUM OF TWO CUBES IDENTITY',
      'BÀI TẬP THỰC TẾ 2.4 (SGK TR.30) — MẢNH ĐẤT LÀM NHÀ VÀ SÂN VƯỜN': 'REAL-WORLD PROBLEM 2.4 (TEXTBOOK P.30) — HOUSE & GARDEN PLOT',
      'BÀI TẬP THỰC TẾ 2.5 (SGK TR.30) — BÀI TOÁN TOÁN NĂNG SUẤT LÀM CHUNG': 'REAL-WORLD PROBLEM 2.5 (TEXTBOOK P.30) — WORK-RATE PROBLEM',
      'TỔNG KẾT TOÀN BÀI & HƯỚNG DẪN TỰ HỌC': 'LESSON SUMMARY & SELF-STUDY GUIDELINES'
    };

    document.querySelectorAll('.slide-heading-text').forEach(el => {
      const orig = el.getAttribute('data-orig-heading') || el.textContent.trim();
      if (!el.getAttribute('data-orig-heading')) el.setAttribute('data-orig-heading', orig);
      el.textContent = (isEn && headingMap[orig]) ? headingMap[orig] : orig;
    });

    // Tiêu đề các khối nội dung (strong)
    const blockTitleMap = {
      'TRỌNG TÂM KIẾN THỨC': 'CORE KNOWLEDGE FOCUS',
      '1. PHƯƠNG TRÌNH TÍCH': '1. PRODUCT EQUATIONS',
      '2. PHƯƠNG TRÌNH CHỨA ẨN Ở MẪU': '2. RATIONAL EQUATIONS',
      'BÀI TOÁN LÀM CHUNG CÔNG VIỆC 2.5': 'WORK-RATE PROBLEM 2.5',
      'BÀI TOÁN THỰC TẾ 2.4': 'REAL-WORLD PROBLEM 2.4',
      'BÀI TẬP 2.1 (SGK TR.30)': 'EXERCISE 2.1 (TEXTBOOK P.30)',
      'BÀI TẬP 2.2 (SGK TR.30)': 'EXERCISE 2.2 (TEXTBOOK P.30)',
      'BÀI TẬP 2.3A (SGK TR.30)': 'EXERCISE 2.3A (TEXTBOOK P.30)',
      'BÀI TẬP 2.3B (SGK TR.30)': 'EXERCISE 2.3B (TEXTBOOK P.30)',
      'BÀI TẬP TƯƠNG TỰ': 'SIMILAR PRACTICE EXERCISE',
      'BƯỚC GIẢI CHI TIẾT': 'DETAILED STEP-BY-STEP SOLUTION',
      'BẢN ĐỒ TƯ DUY 2 PHƯƠNG PHÁP': 'MIND MAP: 2 KEY METHODS',
      'CHÚC CÁC EM HỌC TẬP TỐT!': 'WISH YOU PRODUCTIVE LEARNING!',
      'CHÚ Ý QUAN TRỌNG': 'CRITICAL NOTE',
      'CHÚ Ý KHI TÌM ĐKXĐ': 'IMPORTANT NOTE ON CONSTRAINTS',
      'CÁC BƯỚC THỰC HIỆN THEO YÊU CẦU': 'REQUIRED SOLUTION STEPS',
      'CÁC KỸ THUẬT PHÂN TÍCH NHÂN TỬ THƯỜNG DÙNG': 'COMMON FACTORING TECHNIQUES',
      'CÁCH GIẢI PHƯƠNG TRÌNH TÍCH': 'HOW TO SOLVE PRODUCT EQUATIONS',
      'CÂU HỎI NHẬN BIẾT NHANH': 'QUICK IDENTIFICATION QUESTION',
      'CÂU HỎI THẢO LUẬN': 'DISCUSSION QUESTION',
      'CÂU HỎI TRẮC NGHIỆM': 'MULTIPLE CHOICE QUESTION',
      'CÂU HỎI TRẮC NGHIỆM TƯƠNG TÁC': 'INTERACTIVE MULTIPLE CHOICE QUESTION',
      'CÂU HỎI TƯ DUY': 'CRITICAL THINKING QUESTION',
      'CÂU HỎI ĐẶT VẤN ĐỀ': 'PROBLEM-POSING QUESTION',
      'HỆ THỐNG BÀI TẬP RÈN LUYỆN': 'PRACTICE EXERCISE SYSTEM',
      'HƯỚNG DẪN TỰ HỌC TIẾT 1': 'SELF-STUDY GUIDE (PERIOD 1)',
      'HƯỚNG DẪN TỰ HỌC TIẾT 2': 'SELF-STUDY GUIDE (PERIOD 2)',
      'GHI NHỚ CỐT LÕI BÀI 4': 'CORE TAKEAWAYS OF LESSON 4',
      'GIẢI BÀI TOÁN MỞ ĐẦU (SGK TR.28)': 'SOLVING OPENING PROBLEM (P.28)',
      'GIẢI PHƯƠNG TRÌNH NĂNG SUẤT': 'SOLVING WORK-RATE EQUATION',
      'HÌNH 2.1 — MINH HỌA KHU VƯỜN HÌNH VUÔNG': 'FIGURE 2.1 — SQUARE GARDEN ILLUSTRATION',
      'HÌNH 2.2 — MINH HỌA MẢNH ĐẤT VÀ NHÀ': 'FIGURE 2.2 — HOUSE & GARDEN PLOT ILLUSTRATION',
      'HĐ1: PHÂN TÍCH ĐA THỨC THÀNH NHÂN TỬ': 'ACTIVITY 1: FACTORING POLYNOMIALS',
      'HĐ2: GIẢI PHƯƠNG TRÌNH P(x) = 0': 'ACTIVITY 2: SOLVING EQUATION P(x) = 0',
      'HĐ3: BIẾN ĐỔI CHUYỂN VẾ': 'ACTIVITY 3: TRANSPOSING TERMS',
      'HĐ4: KIỂM TRA NGHIỆM': 'ACTIVITY 4: VERIFYING SOLUTIONS',
      'HĐ5: XÉT PHƯƠNG TRÌNH (1) (SGK TR.29)': 'ACTIVITY 5: EXAMINING EQUATION (1) (P.29)',
      'HƯỚNG DẪN QUY ĐỒNG MẪU': 'DENOMINATOR CLEARING GUIDE',
      'HƯỚNG DẪN TỰ HỌC VỀ NHÀ': 'SELF-STUDY & HOMEWORK GUIDE',
      'KỸ NĂNG QUAN TRỌNG': 'ESSENTIAL SKILL',
      'LUYỆN TẬP 1A (SGK TR.28)': 'PRACTICE 1A (TEXTBOOK P.28)',
      'LUYỆN TẬP 1B (SGK TR.28)': 'PRACTICE 1B (TEXTBOOK P.28)',
      'LUYỆN TẬP 2 (SGK TR.28)': 'PRACTICE 2 (TEXTBOOK P.28)',
      'LUYỆN TẬP 3 — BƯỚC 1 & 2 (SGK TR.29)': 'PRACTICE 3 — STEPS 1 & 2 (P.29)',
      'LUYỆN TẬP TẠI CHỖ': 'IN-CLASS PRACTICE',
      'LUYỆN TẬP NHANH TẠI LỚP': 'QUICK IN-CLASS PRACTICE',
      'LƯU Ý CỐT LÕI (BƯỚC 4)': 'CORE NOTE (STEP 4)',
      'LƯU Ý DẤU PHÉP TÍNH': 'CAUTION ON SIGNS & OPERATIONS',
      'LỜI GIẢI CHI TIẾT': 'DETAILED STEP-BY-STEP SOLUTION',
      'NỘI DUNG TRỌNG TÂM TIẾT 3': 'KEY FOCUS OF PERIOD 3',
      'PHÂN TÍCH HẰNG ĐẲNG THỨC': 'ALGEBRAIC IDENTITY ANALYSIS',
      'KỸ THUẬT BIẾN ĐỔI VỀ DẠNG TÍCH': 'FACTORING TRANSFORMATION TECHNIQUES',
      'QUY TRÌNH 4 BƯỚC BẮT BUỘC': 'MANDATORY 4-STEP PROCEDURE',
      'TÌNH HUỐNG THỰC TẾ (SGK TR.26)': 'REAL-WORLD SITUATION (TEXTBOOK P.26)',
      'TẠI SAO PHẢI TÌM ĐKXĐ TRƯỚC TIÊN?': 'WHY MUST WE FIND CONSTRAINTS FIRST?',
      'TỔNG KẾT TIẾT 2': 'PERIOD 2 SUMMARY',
      'VÍ DỤ MINH HỌA NHANH': 'QUICK ILLUSTRATIVE EXAMPLE',
      'VÍ DỤ MẪU 1 (SGK TR.27)': 'WORKED EXAMPLE 1 (TEXTBOOK P.27)',
      'VÍ DỤ MẪU 2 (SGK TR.27)': 'WORKED EXAMPLE 2 (TEXTBOOK P.27)',
      'VÍ DỤ MẪU 3 (SGK TR.28)': 'WORKED EXAMPLE 3 (TEXTBOOK P.28)',
      'VÍ DỤ MẪU 4 (SGK TR.29)': 'WORKED EXAMPLE 4 (TEXTBOOK P.29)',
      'XÉT PHƯƠNG TRÌNH (SGK TR.28)': 'EXAMINING EQUATION (P.28)',
      'KẾT LUẬN THỰC TIỄN': 'PRACTICAL CONCLUSION',
      'ĐÁP ÁN & GIẢI THÍCH': 'ANSWER & EXPLANATION',
      'ĐÁP ÁN ĐÚNG': 'CORRECT ANSWER',
      'ĐIỀU KIỆN XÁC ĐỊNH (ĐKXĐ)': 'DOMAIN RESTRICTIONS / CONSTRAINTS',
      'ĐỀ BÀI LUYỆN TẬP 1A': 'PRACTICE PROBLEM 1A',
      'ĐỀ BÀI 2.1 (SGK TR.30)': 'PROBLEM STATEMENT 2.1 (P.30)',
      'GỢI Ý & ĐỐI CHIẾU': 'HINT & SOLUTION CHECK',
      'MỤC TIÊU KHÁM PHÁ': 'EXPLORATION OBJECTIVE'
    };

    document.querySelectorAll('.content-block strong').forEach(el => {
      const orig = el.getAttribute('data-orig-title') || el.textContent.trim();
      if (!el.getAttribute('data-orig-title')) el.setAttribute('data-orig-title', orig);
      el.textContent = (isEn && blockTitleMap[orig]) ? blockTitleMap[orig] : orig;
    });

    // Chuyển ngữ toàn diện tiêu đề và nội dung các khối (100% Bilingual)
    document.querySelectorAll('.content-block').forEach(b => {
      const strong = b.querySelector('strong');
      const body = b.querySelector('.block-body');
      if (!body) return;

      if (!b.getAttribute('data-raw-vi')) {
        b.setAttribute('data-raw-vi', cleanLatexInHtml(b.getAttribute('data-raw') || body.innerHTML));
      }
      if (!b.getAttribute('data-title-vi') && strong) {
        b.setAttribute('data-title-vi', strong.getAttribute('data-orig-title') || strong.textContent.trim());
      }

      if (isEn) {
        // Tiêu đề khối
        let titleEn = b.getAttribute('data-title-en');
        if (!titleEn && strong) {
          const tVi = strong.getAttribute('data-orig-title') || strong.textContent.trim();
          titleEn = blockTitleMap[tVi] || smartTranslateText(tVi);
        }
        if (strong && titleEn) {
          strong.textContent = titleEn;
        }

        // Nội dung khối
        const bodyEn = b.getAttribute('data-raw-en');
        if (bodyEn) {
          body.innerHTML = bodyEn;
        } else {
          const curVi = cleanLatexInHtml(b.getAttribute('data-raw') || body.innerHTML);
          body.innerHTML = smartTranslateText(curVi);
        }
      } else {
        // Trở về Tiếng Việt
        const titleVi = b.getAttribute('data-title-vi');
        if (strong && titleVi) {
          strong.textContent = titleVi;
        }

        const bodyVi = b.getAttribute('data-raw-vi') || cleanLatexInHtml(b.getAttribute('data-raw') || body.innerHTML);
        body.innerHTML = bodyVi;
      }
    });

    // Chuyển ngữ chú thích trong hình vẽ SVG
    document.querySelectorAll('svg text').forEach(t => {
      const orig = t.getAttribute('data-orig-text') || t.textContent.trim();
      if (!t.getAttribute('data-orig-text')) t.setAttribute('data-orig-text', orig);
      if (isEn) {
        if (orig.includes('Diện tích còn lại:')) t.textContent = 'Remaining Area:';
        else if (orig.includes('Cạnh khu vườn:')) t.textContent = 'Garden side: 15 m';
        else if (orig.includes('Nhà hình vuông')) t.textContent = 'Square House';
        else if (orig.includes('Sân vườn')) t.textContent = 'Garden';
      } else {
        t.textContent = orig;
      }
    });

    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise();
    }

    showToast(isEn ? 'Switched to Bilingual English Mode!' : 'Đã chuyển về chế độ Tiếng Việt!');
  }

  /* Di chuyển vị trí hiển thị của khối trong cột (Lên / Xuống) */
  function moveBlockPosition(blockId, direction) {
    const el = document.getElementById(blockId);
    if (!el) return;

    if (direction === -1) {
      let prev = el.previousElementSibling;
      while (prev && !prev.classList.contains('content-block')) {
        prev = prev.previousElementSibling;
      }
      if (prev && prev.classList.contains('content-block')) {
        prev.before(el);
        const slide = el.closest('.slide-item');
        if (slide) saveSlideBlockOrder(slide);
        showToast('Đã di chuyển khối lên trên!');
      } else {
        showToast('Khối đã ở vị trí đầu tiên của cột!');
      }
    } else if (direction === 1) {
      let next = el.nextElementSibling;
      while (next && !next.classList.contains('content-block')) {
        next = next.nextElementSibling;
      }
      if (next && next.classList.contains('content-block')) {
        next.after(el);
        const slide = el.closest('.slide-item');
        if (slide) saveSlideBlockOrder(slide);
        showToast('Đã di chuyển khối xuống dưới!');
      } else {
        showToast('Khối đã ở vị trí cuối cùng của cột!');
      }
    }
  }

  function saveSlideBlockOrder(slideEl) {
    if (!slideEl || !slideEl.id) return;
    const boardIds = [...slideEl.querySelectorAll('.col-board > .content-block')].map(b => b.id);
    const taskIds = [...slideEl.querySelectorAll('.col-task > .content-block')].map(b => b.id);
    localStorage.setItem('order_' + slideEl.id, JSON.stringify({ board: boardIds, task: taskIds }));
  }

  function restoreSlideBlockOrders() {
    document.querySelectorAll('.slide-item').forEach(slide => {
      const raw = localStorage.getItem('order_' + slide.id);
      if (!raw) return;
      try {
        const { board, task } = JSON.parse(raw);
        if (board && Array.isArray(board)) {
          const colBoard = slide.querySelector('.col-board');
          const addBtn = colBoard ? colBoard.querySelector('.btn-add-block') : null;
          if (colBoard) {
            board.forEach(id => {
              const b = document.getElementById(id);
              if (b) {
                if (addBtn) colBoard.insertBefore(b, addBtn);
                else colBoard.appendChild(b);
              }
            });
          }
        }
        if (task && Array.isArray(task)) {
          const colTask = slide.querySelector('.col-task');
          const addBtn = colTask ? colTask.querySelector('.btn-add-block') : null;
          if (colTask) {
            task.forEach(id => {
              const b = document.getElementById(id);
              if (b) {
                if (addBtn) colTask.insertBefore(b, addBtn);
                else colTask.appendChild(b);
              }
            });
          }
        }
      } catch (e) {}
    });
  }

  function setBlockStepDirect(blockId) {
    const el = document.getElementById(blockId);
    if (!el) return;
    const cur = parseInt(el.getAttribute('data-step') || '0', 10);
    const input = prompt('Nhập số thứ tự bước xuất hiện (1, 2, 3... hoặc 0 nếu là nội dung cố định luôn hiện):', cur);
    if (input === null) return;
    const val = parseInt(input.trim(), 10);
    if (!isNaN(val) && val >= 0) {
      el.setAttribute('data-step', val);
      const badge = el.querySelector('.badge-step-num');
      if (badge) badge.textContent = val > 0 ? val : 'Cố định';
      saveBlockToLocal(blockId, { step: val });
      showToast(`Đã đổi thành bước ${val > 0 ? val : 'Cố định'}!`);
    }
  }

  /* Kéo thả khối trực quan (HTML5 Drag & Drop) */
  let draggedBlock = null;

  function attachDragHandle(block) {
    if (!block) return;
    const handle = block.querySelector('.drag-handle');
    if (!handle) return;

    handle.addEventListener('mousedown', function(e) {
      if (!isDesignMode) return;
      block.setAttribute('draggable', 'true');
    });

    handle.addEventListener('mouseup', function(e) {
      block.removeAttribute('draggable');
    });

    block.addEventListener('dragstart', handleDragStart);
    block.addEventListener('dragend', handleDragEnd);
  }

  function initDragAndDrop() {
    document.querySelectorAll('.content-block').forEach(block => {
      attachDragHandle(block);
    });

    document.querySelectorAll('.col-board, .col-task').forEach(col => {
      col.addEventListener('dragover', handleDragOver);
      col.addEventListener('dragleave', handleDragLeave);
      col.addEventListener('drop', handleDrop);
    });
  }

  function handleDragStart(e) {
    if (!isDesignMode) {
      e.preventDefault();
      return;
    }
    if (this.getAttribute('draggable') !== 'true' && !e.target.closest('.drag-handle')) {
      e.preventDefault();
      return;
    }
    draggedBlock = this;
    this.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', this.id);
  }

  function handleDragEnd(e) {
    this.classList.remove('dragging');
    this.removeAttribute('draggable');
    document.querySelectorAll('.col-board, .col-task').forEach(col => {
      col.classList.remove('drag-over');
    });
    draggedBlock = null;
  }

  function handleDragOver(e) {
    if (!isDesignMode || !draggedBlock) return;
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    this.classList.add('drag-over');

    const afterElement = getDragAfterElement(this, e.clientY);
    const addBtn = this.querySelector('.btn-add-block');
    if (afterElement == null) {
      if (addBtn) {
        this.insertBefore(draggedBlock, addBtn);
      } else {
        this.appendChild(draggedBlock);
      }
    } else {
      this.insertBefore(draggedBlock, afterElement);
    }
  }

  function handleDragLeave(e) {
    this.classList.remove('drag-over');
  }

  function handleDrop(e) {
    e.preventDefault();
    this.classList.remove('drag-over');
    if (draggedBlock) {
      draggedBlock.removeAttribute('draggable');
      const slide = this.closest('.slide-item');
      if (slide) saveSlideBlockOrder(slide);
      showToast('Đã di chuyển khối đến vị trí mới!');
    }
  }

  function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll('.content-block:not(.dragging)')];
    return draggableElements.reduce((closest, child) => {
      const box = child.getBoundingClientRect();
      const offset = y - box.top - box.height / 2;
      if (offset < 0 && offset > closest.offset) {
        return { offset: offset, element: child };
      } else {
        return closest;
      }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
  }

  function getCurrentSlide() {
    return document.querySelector(`.slide-item[data-slide-index="${currentSlideIndex}"]`);
  }

  function getMaxStepInSlide(slideEl) {
    let max = 0;
    slideEl.querySelectorAll('.content-block, .inline-anim').forEach(el => {
      const s = parseInt(el.getAttribute('data-step') || '0', 10);
      const e = parseInt(el.getAttribute('data-exit-step') || '0', 10);
      if (!isNaN(s) && s > max) max = s;
      if (!isNaN(e) && e > max) max = e;
    });
    return max;
  }

  function updateSlideDisplay() {
    stopAllSpeech();
    slides.forEach(s => {
      s.classList.remove('active');
    });
    const cur = getCurrentSlide();
    if (cur) {
      cur.classList.add('active');
      applyStepsToSlide(cur);
    }
  }

  function applyStepsToSlide(slideEl) {
    if (isDesignMode) return;

    // 1. Áp dụng cho các khối
    const blocks = slideEl.querySelectorAll('.content-block');
    blocks.forEach(b => {
      const enterStep = parseInt(b.getAttribute('data-step') || '0', 10);
      const exitAttr = b.getAttribute('data-exit-step');
      const exitStep = exitAttr ? parseInt(exitAttr, 10) : null;

      const hasEntered = (enterStep === 0) || (currentStep >= enterStep);
      const hasExited = (exitStep !== null) && (currentStep >= exitStep);

      if (hasEntered && !hasExited) {
        b.classList.add('is-revealed');
        b.classList.remove('is-exited');
      } else if (hasExited) {
        b.classList.remove('is-revealed');
        b.classList.add('is-exited');
      } else {
        b.classList.remove('is-revealed');
        b.classList.remove('is-exited');
      }
    });

    // 2. Áp dụng cho các hiệu ứng nội tuyến (Inline Animations) được bôi đen
    const anims = slideEl.querySelectorAll('.inline-anim');
    anims.forEach(el => {
      const enterStep = parseInt(el.getAttribute('data-step') || '0', 10);
      const exitAttr = el.getAttribute('data-exit-step');
      const exitStep = exitAttr ? parseInt(exitAttr, 10) : null;
      const isHighlight = el.classList.contains('inline-highlight');

      const hasEntered = (enterStep === 0) || (currentStep >= enterStep);
      const hasExited = (exitStep !== null) && (currentStep >= exitStep);

      if (hasEntered && !hasExited) {
        el.classList.add('is-revealed');
        el.classList.remove('is-exited');
        if (isHighlight) el.classList.add('active-highlight');
      } else if (hasExited) {
        el.classList.remove('is-revealed');
        el.classList.add('is-exited');
        if (isHighlight) el.classList.remove('active-highlight');
      } else {
        el.classList.remove('is-revealed');
        el.classList.remove('is-exited');
        if (isHighlight) el.classList.remove('active-highlight');
      }
    });

    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise([slideEl]);
    }
  }

  function nextStep() {
    const cur = getCurrentSlide();
    if (!cur) return;
    const max = getMaxStepInSlide(cur);
    if (currentStep < max) {
      currentStep++;
      applyStepsToSlide(cur);
    } else {
      nextSlide();
    }
  }

  function prevStep() {
    const cur = getCurrentSlide();
    if (!cur) return;
    if (currentStep > 0) {
      currentStep--;
      applyStepsToSlide(cur);
    } else {
      if (currentSlideIndex > 1) {
        currentSlideIndex--;
        const prev = getCurrentSlide();
        currentStep = getMaxStepInSlide(prev);
        updateSlideDisplay();
      }
    }
  }

  function nextSlide() {
    if (currentSlideIndex < totalSlides) {
      currentSlideIndex++;
      currentStep = 0;
      updateSlideDisplay();
    }
  }

  function prevSlide() {
    if (currentSlideIndex > 1) {
      currentSlideIndex--;
      currentStep = 0;
      updateSlideDisplay();
    }
  }

  /* --- CHỈNH SỬA TRỰC QUAN TRỰC TIẾP TRÊN SLIDE (WYSIWYG IN-PLACE EDITING) --- */
  let directEditSaveTimeout = null;

  function enableDirectVisualEditing() {
    document.querySelectorAll('.content-block').forEach(b => {
      const body = b.querySelector('.block-body');
      const title = b.querySelector('strong');

      if (body) {
        body.setAttribute('contenteditable', 'true');
        body.setAttribute('spellcheck', 'false');

        // Khóa không cho phá vỡ MathJax nội bộ, cho phép click để sửa công thức toán
        body.querySelectorAll('mjx-container').forEach(mjx => {
          mjx.setAttribute('contenteditable', 'false');
          mjx.setAttribute('title', 'Click để sửa nhanh công thức toán LaTeX');
          mjx.onclick = function(e) {
            e.stopPropagation();
            editMathFormula(this);
          };
        });

        body.oninput = function() {
          saveDirectEdit(b);
        };
        body.onblur = function() {
          saveDirectEdit(b);
        };
      }

      if (title) {
        title.setAttribute('contenteditable', 'true');
        title.setAttribute('spellcheck', 'false');
        title.oninput = function() {
          saveDirectTitleEdit(b, title);
        };
        title.onblur = function() {
          saveDirectTitleEdit(b, title);
        };
      }

      b.onclick = function() {
        if (!isDesignMode) return;
        const slideEl = this.closest('.slide-item');
        if (slideEl) {
          const sIdx = parseInt(slideEl.getAttribute('data-slide-index') || '1', 10);
          if (sIdx) currentSlideIndex = sIdx;
        }
      };
    });

    document.querySelectorAll('.slide-item').forEach(s => {
      s.onclick = function() {
        if (!isDesignMode) return;
        const sIdx = parseInt(this.getAttribute('data-slide-index') || '1', 10);
        if (sIdx) currentSlideIndex = sIdx;
      };
    });
  }

  function disableDirectVisualEditing() {
    document.querySelectorAll('.content-block').forEach(b => {
      const body = b.querySelector('.block-body');
      const title = b.querySelector('strong');
      if (body) {
        body.removeAttribute('contenteditable');
        body.oninput = null;
        body.onblur = null;
      }
      if (title) {
        title.removeAttribute('contenteditable');
        title.oninput = null;
        title.onblur = null;
      }
      b.onclick = null;
    });
    document.querySelectorAll('.slide-item').forEach(s => {
      s.onclick = null;
    });
  }

  function saveDirectEdit(blockEl) {
    if (!blockEl) return;
    clearTimeout(directEditSaveTimeout);
    directEditSaveTimeout = setTimeout(() => {
      const body = blockEl.querySelector('.block-body');
      if (!body) return;
      const cleanHtml = cleanLatexInHtml(body.innerHTML);
      blockEl.setAttribute('data-raw', cleanHtml);
      blockEl.setAttribute('data-raw-vi', cleanHtml);
      blockEl.setAttribute('data-raw-en', smartTranslateText(cleanHtml));
      saveBlockToLocal(blockEl.id, { content: cleanHtml });
      showToast('Đã tự động lưu chỉnh sửa!');
    }, 350);
  }

  function saveDirectTitleEdit(blockEl, titleEl) {
    if (!blockEl || !titleEl) return;
    clearTimeout(directEditSaveTimeout);
    directEditSaveTimeout = setTimeout(() => {
      const titleText = titleEl.textContent.trim();
      blockEl.setAttribute('data-title-vi', titleText);
      blockEl.setAttribute('data-title-en', smartTranslateText(titleText));
      saveBlockToLocal(blockEl.id, { title: titleText });
      showToast('Đã tự động lưu tiêu đề khối!');
    }, 350);
  }

  function editMathFormula(mjxEl) {
    if (!isDesignMode) return;
    let curTex = mjxEl.getAttribute('data-tex') || '';
    if (!curTex) {
      curTex = mjxEl.getAttribute('alt') || mjxEl.getAttribute('aria-label') || '';
      if (curTex) curTex = '$' + curTex + '$';
    }
    const newTex = prompt('Chỉnh sửa công thức Toán (LaTeX):', curTex || '$x$');
    if (newTex === null || newTex.trim() === curTex.trim()) return;

    const textNode = document.createTextNode(newTex.trim());
    const block = mjxEl.closest('.content-block');
    mjxEl.replaceWith(textNode);

    if (block) {
      const body = block.querySelector('.block-body');
      if (body) {
        const clean = cleanLatexInHtml(body.innerHTML);
        block.setAttribute('data-raw', clean);
        saveBlockToLocal(block.id, { content: clean });
      }
      if (window.MathJax && window.MathJax.typesetPromise) {
        window.MathJax.typesetPromise([block]).then(() => {
          enableDirectVisualEditing();
        });
      }
    }
    showToast('Đã cập nhật công thức toán!');
  }

  function toggleMode() {
    isDesignMode = !isDesignMode;
    const btn = document.getElementById('btnToggleMode');
    const isEn = (currentLang === 'en');
    if (isDesignMode) {
      document.body.classList.remove('mode-present');
      document.body.classList.add('mode-design');
      btn.textContent = isEn ? '🎬 Present' : '🎬 Trình chiếu';
      btn.style.background = '#d97706';
      enableDirectVisualEditing();
      showToast('Đã bật Chế độ Thiết kế: Click trực tiếp vào chữ trên slide để sửa!');

      // Cuộn ngay đến đúng slide hiện tại đang xem, không nhảy về Slide 1
      const targetSlide = document.querySelector(`.slide-item[data-slide-index="${currentSlideIndex}"]`);
      if (targetSlide) {
        setTimeout(() => {
          targetSlide.scrollIntoView({ behavior: 'auto', block: 'start' });
          targetSlide.style.outline = '4px solid #6366f1';
          setTimeout(() => { targetSlide.style.outline = ''; }, 1500);
        }, 60);
      }
    } else {
      // Khi quay lại Trình chiếu: Nhận diện slide gần đỉnh màn hình nhất để hiển thị đúng slide đó
      let bestIdx = currentSlideIndex;
      let minDistance = Infinity;
      document.querySelectorAll('.slide-item').forEach(s => {
        const rect = s.getBoundingClientRect();
        const dist = Math.abs(rect.top - 20);
        if (dist < minDistance) {
          minDistance = dist;
          bestIdx = parseInt(s.getAttribute('data-slide-index') || '1', 10);
        }
      });
      currentSlideIndex = bestIdx;

      disableDirectVisualEditing();
      document.body.classList.remove('mode-design');
      document.body.classList.add('mode-present');
      btn.textContent = isEn ? '⚙ Design' : '⚙ Thiết kế';
      btn.style.background = '#059669';
      updateSlideDisplay();

      const cur = getCurrentSlide();
      if (cur) {
        const board = cur.querySelector('.col-board');
        const task = cur.querySelector('.col-task');
        if (board) board.scrollTop = 0;
        if (task) task.scrollTop = 0;
      }
    }
  }

  function setBlockExitStep(blockId) {
    const el = document.getElementById(blockId);
    if (!el) return;
    const curEnter = parseInt(el.getAttribute('data-step') || '0', 10);
    const curExit = el.getAttribute('data-exit-step') || '';
    const input = prompt(
      `Khối này xuất hiện ở bước: ${curEnter > 0 ? curEnter : 'Cố định (bước 0)'}\n\n` +
      `Nhập số thứ tự bước để khối này TỰ ĐỘNG BIẾN MẤT (Fade Out):\n` +
      `(Phải lớn hơn bước xuất hiện. Nhập 0 hoặc để trống nếu KHÔNG muốn biến mất)`,
      curExit
    );
    if (input === null) return;
    const val = parseInt(input.trim(), 10);
    if (!isNaN(val) && val > 0) {
      if (curEnter > 0 && val <= curEnter) {
        alert(`⚠️ Bước biến mất (${val}) phải lớn hơn bước xuất hiện (${curEnter})!`);
        return;
      }
      el.setAttribute('data-exit-step', val);
      saveBlockToLocal(blockId, { exitStep: val });
    } else {
      el.removeAttribute('data-exit-step');
      saveBlockToLocal(blockId, { exitStep: null });
    }
    updateBlockDesignBadges(el);
  }

  function updateBlockDesignBadges(el) {
    if (!el) return;
    const exitAttr = el.getAttribute('data-exit-step');
    const btnExit = el.querySelector('.btn-exit-step');
    if (btnExit) {
      if (exitAttr) {
        btnExit.textContent = `💨 Mất: bước ${exitAttr}`;
        btnExit.style.background = '#ffedd5';
        btnExit.style.color = '#c2410c';
        btnExit.style.borderColor = '#fb923c';
        btnExit.style.fontWeight = 'bold';
      } else {
        btnExit.textContent = '💨 Biến mất';
        btnExit.style.background = '';
        btnExit.style.color = '';
        btnExit.style.borderColor = '';
        btnExit.style.fontWeight = 'normal';
      }
    }
  }

  function deleteBlock(blockId) {
    if (!confirm('Thầy/Cô có chắc chắn muốn xóa khối này?')) return;
    const el = document.getElementById(blockId);
    if (el) {
      el.remove();
      localStorage.setItem('del_' + blockId, '1');
    }
  }

  function toggleBlockWait(blockId) {
    const el = document.getElementById(blockId);
    if (!el) return;
    const current = el.getAttribute('data-step');
    if (current === '0' || !current) {
      el.setAttribute('data-step', '1');
    } else {
      el.setAttribute('data-step', '0');
    }
    const badge = el.querySelector('.badge-step-num');
    const s = el.getAttribute('data-step');
    if (badge) badge.textContent = s !== '0' ? s : 'Cố định';
    saveBlockToLocal(blockId, { step: parseInt(s, 10) });
  }

  /* --- TÍNH NĂNG QUÉT CHỌN ĐOẠN VĂN ĐỂ GẮN HIỆU ỨNG TRỰC TIẾP --- */
  let currentSelectionData = null;

  document.addEventListener('mouseup', function(e) {
    if (!isDesignMode) {
      hideSelectionTooltip();
      return;
    }
    if (e.target.closest('#selectionTooltip') || e.target.closest('#editModal')) return;

    setTimeout(() => {
      const sel = window.getSelection();
      if (!sel || sel.isCollapsed || sel.rangeCount === 0) {
        hideSelectionTooltip();
        return;
      }
      const text = sel.toString().trim();
      if (!text) {
        hideSelectionTooltip();
        return;
      }

      const range = sel.getRangeAt(0);
      const container = range.commonAncestorContainer;
      const blockEl = (container.nodeType === 1 ? container : container.parentElement).closest('.content-block');
      if (!blockEl) {
        hideSelectionTooltip();
        return;
      }

      const rect = range.getBoundingClientRect();
      const tooltip = document.getElementById('selectionTooltip');
      if (tooltip && rect.width > 0) {
        currentSelectionData = {
          blockId: blockEl.id,
          range: range.cloneRange(),
          selectedText: text
        };
        tooltip.style.left = (rect.left + window.scrollX + rect.width / 2) + 'px';
        tooltip.style.top = (rect.top + window.scrollY - 38) + 'px';
        tooltip.style.transform = 'translateX(-50%)';
        tooltip.style.display = 'flex';
      }
    }, 10);
  });

  function hideSelectionTooltip() {
    const tooltip = document.getElementById('selectionTooltip');
    if (tooltip) tooltip.style.display = 'none';
    currentSelectionData = null;
  }

  function cleanLatexInHtml(input) {
    if (!input) return '';
    let html = (typeof input === 'string') ? input : input.innerHTML;
    if (!html) return '';

    html = html.replace(/<mjx-container[^>]*data-tex="([^"]+)"[^>]*>[\s\S]*?<\/mjx-container>/gi, (match, tex) => {
      return tex;
    });
    html = html.replace(/<mjx-container[^>]*>[\s\S]*?<annotation[^>]*>([\s\S]*?)<\/annotation>[\s\S]*?<\/mjx-container>/gi, (match, tex) => {
      return '$' + tex.trim() + '$';
    });
    html = html.replace(/<mjx-container[^>]*(?:aria-label|alt)="([^"]+)"[^>]*>[\s\S]*?<\/mjx-container>/gi, (match, tex) => {
      return '$' + tex.trim() + '$';
    });
    html = html.replace(/<mjx-container[^>]*>[\s\S]*?<\/mjx-container>/gi, '');
    html = html.replace(/<svg[^>]*data-mml-node[^>]*>[\s\S]*?<\/svg>/gi, '');
    html = html.replace(/<g\s+data-mml-node[^>]*>[\s\S]*?<\/g>/gi, '');
    return html.trim();
  }

  
  /* Kiểm tra trắc nghiệm tương tác */
  function checkQuiz(btn, isCorrect, qId) {
    const group = btn.closest('.quiz-options-group') || btn.parentElement;
    group.querySelectorAll('.quiz-btn').forEach(b => {
      b.classList.remove('correct', 'incorrect');
    });
    if (isCorrect) {
      btn.classList.add('correct');
      showToast('🎉 Chính xác! Bạn đã chọn đúng đáp án.');
    } else {
      btn.classList.add('incorrect');
      showToast('❌ Chưa đúng! Hãy xem lại phân tích hướng dẫn giải.');
    }
    const exp = document.getElementById(qId + '_explain');
    if (exp) exp.classList.remove('hidden');
  }

  /* Tách đoạn bôi đen thành khối Hướng dẫn giải riêng biệt */
  function splitSelectionToSolutionBlock() {
    if (!currentSelectionData) return;
    const { blockId, range, selectedText } = currentSelectionData;
    const origBlock = document.getElementById(blockId);
    if (!origBlock) return;

    const col = origBlock.parentElement;
    const curStep = parseInt(origBlock.getAttribute('data-step') || '1', 10);
    const nextStep = curStep + 1;

    const frag = range.extractContents();
    const tempDiv = document.createElement('div');
    tempDiv.appendChild(frag);
    let solHtml = tempDiv.innerHTML.trim();
    if (!solHtml) solHtml = selectedText;

    const origBody = origBlock.querySelector('.block-body');
    const cleanOrig = cleanLatexInHtml(origBody ? origBody.innerHTML : origBlock.innerHTML);
    origBlock.setAttribute('data-raw', cleanOrig);
    origBlock.setAttribute('data-raw-vi', cleanOrig);
    saveBlockToLocal(blockId, { content: cleanOrig });

    const solBlockId = blockId + '_sol_' + Date.now().toString(36).substr(-4);
    const newBlock = document.createElement('div');
    newBlock.className = 'content-block highlight-ex is-revealed';
    newBlock.id = solBlockId;
    newBlock.setAttribute('data-step', nextStep);
    newBlock.setAttribute('data-raw', solHtml);
    newBlock.setAttribute('data-raw-vi', solHtml);
    newBlock.setAttribute('data-raw-en', smartTranslateText(solHtml));
    newBlock.setAttribute('data-title-vi', 'HƯỚNG DẪN GIẢI CHI TIẾT');
    newBlock.setAttribute('data-title-en', 'DETAILED GUIDED SOLUTION');

    newBlock.innerHTML = `
      <div class="design-overlay">
        <span class="drag-handle" title="Kéo để di chuyển">⠿</span>
        <span class="badge-role badge-role-sol">💡 Lời giải</span>
        <span class="badge-step-num" onclick="setBlockStepDirect('${solBlockId}')">Bước ${nextStep}</span>
        <button class="btn-step-order" onclick="moveBlockPosition('${solBlockId}', -1)">▲</button>
        <button class="btn-step-order" onclick="moveBlockPosition('${solBlockId}', 1)">▼</button>
        <button class="btn-block-action btn-edit-block" onclick="openEditModal('${solBlockId}')">✏️ Sửa</button>
        <button class="btn-block-action btn-del-block" onclick="deleteBlock('${solBlockId}')">✕</button>
      </div>
      <button class="btn-block-speak" onclick="speakBlockEn(this.closest('.content-block'), null, event)">🔊</button>
      <strong>HƯỚNG DẪN GIẢI CHI TIẾT</strong><br>
      <div class="block-body">${solHtml}</div>
    `;

    if (origBlock.nextSibling) {
      col.insertBefore(newBlock, origBlock.nextSibling);
    } else {
      col.appendChild(newBlock);
    }

    saveBlockToLocal(solBlockId, {
      title: 'HƯỚNG DẪN GIẢI CHI TIẾT',
      content: solHtml,
      step: nextStep,
      className: 'highlight-ex'
    });

    hideSelectionTooltip();
    if (window.getSelection()) window.getSelection().removeAllRanges();
    attachDragHandle(newBlock);

    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise([origBlock, newBlock]);
    }

    showToast(`Đã tách thành công khối "HƯỚNG DẪN GIẢI" riêng ở Bước ${nextStep}!`);
  }

  function applyInlineAnimation(animType) {
    if (!currentSelectionData) return;
    const { blockId, range, selectedText } = currentSelectionData;
    const origBlock = document.getElementById(blockId);
    if (!origBlock) return;

    const slide = origBlock.closest('.slide-item');
    const curBlockStep = parseInt(origBlock.getAttribute('data-step') || '0', 10);
    const maxStep = slide ? getMaxStepInSlide(slide) : curBlockStep;
    const nextStep = Math.max(maxStep + 1, curBlockStep + 1, 2);

    const span = document.createElement('span');
    span.className = 'inline-anim inline-' + animType;
    if (animType === 'exit') {
      span.setAttribute('data-exit-step', nextStep);
    } else {
      span.setAttribute('data-step', nextStep);
    }
    span.setAttribute('title', 'Click trong Chế độ Thiết kế để đổi bước hoặc gỡ hiệu ứng');
    span.onclick = function(e) {
      if (isDesignMode) {
        e.stopPropagation();
        editInlineAnim(this);
      }
    };

    try {
      const fragment = range.extractContents();
      span.appendChild(fragment);
      range.insertNode(span);
    } catch (err) {
      console.error(err);
      return;
    }

    const origBody = origBlock.querySelector('.block-body');
    if (origBody) {
      const cleanRaw = cleanLatexInHtml(origBody.innerHTML);
      origBlock.setAttribute('data-raw', cleanRaw);
      saveBlockToLocal(blockId, { content: cleanRaw });
    }

    hideSelectionTooltip();
    if (window.getSelection()) window.getSelection().removeAllRanges();

    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise([origBlock]);
    }

    const typeLabels = {
      appear: `Xuất hiện ở Bước ${nextStep}`,
      exit: `Biến mất ở Bước ${nextStep}`,
      highlight: `Nổi bật ở Bước ${nextStep}`
    };
    showToast(`Đã gắn hiệu ứng "${typeLabels[animType] || 'Mới'}" cho đoạn bôi đen!`);
  }

  function editInlineAnim(el) {
    if (!isDesignMode) return;
    const isExit = el.hasAttribute('data-exit-step');
    const curStep = isExit ? el.getAttribute('data-exit-step') : (el.getAttribute('data-step') || '2');
    const input = prompt(
      `Đoạn văn bản đang gắn hiệu ứng ${isExit ? 'Biến mất' : 'Xuất hiện'} ở Bước ${curStep}.\n\n` +
      `- Nhập số bước mới (1, 2, 3...)\n` +
      `- Hoặc nhập 0 để GỠ BỎ HIỆU ỨNG:`,
      curStep
    );
    if (input === null) return;
    const val = parseInt(input.trim(), 10);
    const block = el.closest('.content-block');

    if (val === 0) {
      const parent = el.parentNode;
      while (el.firstChild) {
        parent.insertBefore(el.firstChild, el);
      }
      el.remove();
      showToast('Đã gỡ bỏ hiệu ứng khỏi đoạn văn bản!');
    } else if (!isNaN(val) && val > 0) {
      if (isExit) el.setAttribute('data-exit-step', val);
      else el.setAttribute('data-step', val);
      showToast(`Đã đổi hiệu ứng sang Bước ${val}!`);
    }

    if (block) {
      const origBody = block.querySelector('.block-body');
      if (origBody) {
        const cleanRaw = cleanLatexInHtml(origBody.innerHTML);
        block.setAttribute('data-raw', cleanRaw);
        saveBlockToLocal(block.id, { content: cleanRaw });
      }
    }
  }

  function addAnimToSelection(blockId) {
    const sel = window.getSelection();
    if (sel && !sel.isCollapsed && sel.rangeCount > 0) {
      const range = sel.getRangeAt(0);
      const container = range.commonAncestorContainer;
      const b = (container.nodeType === 1 ? container : container.parentElement).closest('.content-block');
      if (b && b.id === blockId) {
        currentSelectionData = {
          blockId: blockId,
          range: range.cloneRange(),
          selectedText: sel.toString().trim()
        };
        applyInlineAnimation('appear');
        return;
      }
    }
    alert('💡 Hướng dẫn nhanh:\nThầy/Cô hãy dùng chuột BÔI ĐEN đoạn văn bản hoặc công thức cần thêm hiệu ứng, sau đó chọn "👁️ Xuất hiện (+1 bước)" trên thanh công cụ nổi nhé!');
  }

  /* --- BỘ SOẠN THẢO VÀ CHỈNH SỬA TOÀN DIỆN (RICH EDITOR SUITE) --- */
  let activeCreateSlideId = null;
  let activeCreateColType = null;
  let previewDebounceTimer = null;

  function updateLivePreview() {
    const textarea = document.getElementById('editTextarea');
    if (!textarea) return;
    const val = textarea.value;
    const box = document.getElementById('editPreviewBox');
    if (!box) return;
    box.innerHTML = val || '<i style="color:#94a3b8;">Chưa có nội dung xem trước...</i>';
    clearTimeout(previewDebounceTimer);
    previewDebounceTimer = setTimeout(() => {
      if (window.MathJax && window.MathJax.typesetPromise) {
        window.MathJax.typesetPromise([box]);
      }
    }, 180);
  }

  function insertText(text) {
    const area = document.getElementById('editTextarea');
    if (!area) return;
    const start = area.selectionStart;
    const end = area.selectionEnd;
    const before = area.value.substring(0, start);
    const after = area.value.substring(end);
    area.value = before + text + after;
    area.selectionStart = area.selectionEnd = start + text.length;
    area.focus();
    updateLivePreview();
  }

  function insertTag(openTag, closeTag) {
    const area = document.getElementById('editTextarea');
    if (!area) return;
    const start = area.selectionStart;
    const end = area.selectionEnd;
    const selected = area.value.substring(start, end) || 'nội dung';
    const before = area.value.substring(0, start);
    const after = area.value.substring(end);
    area.value = before + openTag + selected + closeTag + after;
    area.selectionStart = start + openTag.length;
    area.selectionEnd = start + openTag.length + selected.length;
    area.focus();
    updateLivePreview();
  }

  function insertImagePrompt() {
    const url = prompt('Dán đường link hình ảnh (URL) vào đây:');
    if (!url) return;
    const imgHtml = `<img src="${url.trim()}" style="max-width:100%;border-radius:8px;margin:8px auto;display:block;box-shadow:0 4px 12px rgba(0,0,0,0.15);" alt="Hình ảnh bài giảng">`;
    insertText(imgHtml);
  }

  function handleLocalImageUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function(e) {
      const base64 = e.target.result;
      const imgHtml = `<img src="${base64}" style="max-width:100%;border-radius:8px;margin:8px auto;display:block;box-shadow:0 4px 12px rgba(0,0,0,0.15);" alt="${file.name}">`;
      insertText(imgHtml);
      showToast('Đã tải và nhúng ảnh trực tiếp vào bài giảng!');
    };
    reader.readAsDataURL(file);
    event.target.value = '';
  }

  function insertVideoPrompt() {
    const url = prompt('Nhập link video YouTube (ví dụ: https://youtu.be/...) hoặc link video MP4:');
    if (!url) return;
    const trimmed = url.trim();
    let videoHtml = '';

    let ytId = null;
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
    const match = trimmed.match(regExp);
    if (match && match[2].length === 11) {
      ytId = match[2];
      videoHtml = `<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;margin:8px 0;border-radius:8px;"><iframe src="https://www.youtube.com/embed/${ytId}" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" allowfullscreen></iframe></div>`;
    } else {
      videoHtml = `<video controls src="${trimmed}" style="max-width:100%;border-radius:8px;margin:8px auto;display:block;box-shadow:0 4px 12px rgba(0,0,0,0.15);"></video>`;
    }
    insertText(videoHtml);
  }

  function openEditModal(blockId) {
    const el = document.getElementById(blockId);
    if (!el) return;
    activeEditBlockId = blockId;
    activeCreateSlideId = null;
    activeCreateColType = null;

    document.getElementById('editModalHeaderTitle').textContent = '✏️ Chỉnh sửa nội dung khối';
    const strong = el.querySelector('strong');
    document.getElementById('editTitleInput').value = strong ? strong.textContent.trim() : '';

    const raw = el.getAttribute('data-raw') || cleanLatexInHtml(el.querySelector('.block-body')) || '';
    document.getElementById('editTextarea').value = cleanLatexInHtml(raw);
    updateLivePreview();
    document.getElementById('editModal').classList.add('active');
  }

  function openCreateBlockModal(slideId, colType) {
    activeEditBlockId = null;
    activeCreateSlideId = slideId;
    activeCreateColType = colType;

    document.getElementById('editModalHeaderTitle').textContent = colType === 'board' ? '➕ Thêm khối ghi bảng mới' : '➕ Thêm hoạt động học sinh mới';
    document.getElementById('editTitleInput').value = colType === 'board' ? 'KIẾN THỨC MỚI' : 'HOẠT ĐỘNG THỰC HIỆN';
    document.getElementById('editTextarea').value = '• Nội dung bài học hoặc công thức $ax + b = 0$...';
    updateLivePreview();
    document.getElementById('editModal').classList.add('active');
  }

  function closeEditModal() {
    document.getElementById('editModal').classList.remove('active');
    activeEditBlockId = null;
    activeCreateSlideId = null;
    activeCreateColType = null;
  }

  function saveEditContent() {
    const titleVal = document.getElementById('editTitleInput').value.trim();
    const contentVal = document.getElementById('editTextarea').value.trim();

    if (activeEditBlockId) {
      const el = document.getElementById(activeEditBlockId);
      if (!el) return;
      const strong = el.querySelector('strong');
      if (strong && titleVal) {
        strong.textContent = titleVal;
        el.setAttribute('data-title-vi', titleVal);
        el.setAttribute('data-title-en', smartTranslateText(titleVal));
      }
      el.setAttribute('data-raw', contentVal);
      el.setAttribute('data-raw-vi', contentVal);
      el.setAttribute('data-raw-en', smartTranslateText(contentVal));
      const body = el.querySelector('.block-body');
      if (body) body.innerHTML = contentVal;
      saveBlockToLocal(activeEditBlockId, { title: titleVal, content: contentVal });
      if (window.MathJax && window.MathJax.typesetPromise) {
        window.MathJax.typesetPromise([el]);
      }
      showToast('Đã cập nhật nội dung khối thành công!');
    } else if (activeCreateSlideId && activeCreateColType) {
      const slide = document.getElementById(activeCreateSlideId);
      if (!slide) return;
      const col = slide.querySelector(activeCreateColType === 'board' ? '.col-board' : '.col-task');
      if (!col) return;

      const newStep = getMaxStepInSlide(slide) + 1;
      const newBlockId = 'blk_' + Date.now();
      const newBlock = document.createElement('div');
      newBlock.className = 'content-block' + (activeCreateColType === 'board' ? ' highlight-def' : '');
      newBlock.id = newBlockId;
      newBlock.setAttribute('data-step', newStep);
      newBlock.setAttribute('data-raw', contentVal);
      newBlock.setAttribute('data-raw-vi', contentVal);
      newBlock.setAttribute('data-raw-en', smartTranslateText(contentVal));
      newBlock.setAttribute('data-title-vi', titleVal || 'NỘI DUNG MỚI');
      newBlock.setAttribute('data-title-en', smartTranslateText(titleVal || 'NEW CONTENT'));

      newBlock.innerHTML = createDesignOverlayHTML(newBlockId, newStep) + `<button class="btn-block-speak" onclick="speakBlockEn(this.closest('.content-block'), null, event)" title="Nghe phát âm tiếng Anh chậm rãi (0.8x)">🔊</button><strong>${titleVal || 'NỘI DUNG MỚI'}</strong><br><div class="block-body">${contentVal}</div>`;
      attachDragHandle(newBlock);

      const addBtn = col.querySelector('.btn-add-block');
      if (addBtn) {
        col.insertBefore(newBlock, addBtn);
      } else {
        col.appendChild(newBlock);
      }

      saveBlockToLocal(newBlockId, {
        title: titleVal,
        content: contentVal,
        step: newStep,
        slideId: activeCreateSlideId,
        colType: activeCreateColType
      });

      if (window.MathJax && window.MathJax.typesetPromise) {
        window.MathJax.typesetPromise([newBlock]);
      }
      showToast(`Đã thêm khối mới vào ${activeCreateColType === 'board' ? 'Cột ghi bảng' : 'Cột hoạt động'}!`);
    }

    closeEditModal();
  }

  function saveBlockToLocal(blockId, data) {
    const key = 'block_' + blockId;
    const existing = JSON.parse(localStorage.getItem(key) || '{}');
    const updated = Object.assign(existing, data);
    localStorage.setItem(key, JSON.stringify(updated));
  }

  /* Phím tắt điều hướng */
  document.addEventListener('keydown', function(e) {
    if (e.target.closest('input, textarea, [contenteditable="true"]')) return;
    if (e.key === 'ArrowRight' || e.key === ' ') {
      e.preventDefault();
      nextStep();
    } else if (e.key === 'ArrowLeft') {
      e.preventDefault();
      prevStep();
    }
  });

  /* Chạm vùng trống tiến bước */
  document.getElementById('slideDeck').addEventListener('click', function(e) {
    if (isDesignMode) return;
    if (window.getSelection && !window.getSelection().isCollapsed) return;
    if (e.target.closest('button, a, input, textarea, .control-bar, #editModal')) return;
    nextStep();
  });

  /* Khôi phục LocalStorage */
  window.addEventListener('DOMContentLoaded', function() {
    const LECTURE_VERSION = '3.1';
    try {
      if (localStorage.getItem('lecture_ver_clean') !== LECTURE_VERSION) {
        Object.keys(localStorage).forEach(k => {
          if (k.startsWith('block_') || k.startsWith('del_') || k.startsWith('order_')) {
            localStorage.removeItem(k);
          }
        });
        localStorage.setItem('lecture_ver_clean', LECTURE_VERSION);
      }
    } catch (e) {}

    try {
      const savedFont = localStorage.getItem('lecture_font_idx');
      if (savedFont !== null) {
        applyFontSize(parseInt(savedFont, 10));
      } else {
        applyFontSize(0); // Mặc định 28px chuẩn TV
      }
    } catch (e) {
      applyFontSize(0);
    }
    try {
      const savedRate = localStorage.getItem('lecture_speech_rate_idx');
      if (savedRate !== null) {
        applySpeechRate(parseInt(savedRate, 10));
      } else {
        applySpeechRate(0); // Mặc định 0.85x
      }
    } catch (e) {
      applySpeechRate(0);
    }
    restoreSlideBlockOrders();
    document.querySelectorAll('.content-block').forEach(b => {
      if (localStorage.getItem('del_' + b.id) === '1') {
        b.remove();
        return;
      }
      const rawStored = localStorage.getItem('block_' + b.id);
      if (rawStored) {
        try {
          const data = JSON.parse(rawStored);
          if (data.step !== undefined) {
            b.setAttribute('data-step', data.step);
            const badge = b.querySelector('.badge-step-num');
            if (badge) badge.textContent = data.step > 0 ? data.step : 'Cố định';
          }
          if (data.exitStep !== undefined) {
            if (data.exitStep !== null && data.exitStep > 0) {
              b.setAttribute('data-exit-step', data.exitStep);
            } else {
              b.removeAttribute('data-exit-step');
            }
          }
          if (data.content !== undefined) {
            b.setAttribute('data-raw', data.content);
            const body = b.querySelector('.block-body');
            if (body) body.innerHTML = data.content;
          }
        } catch (err) {}
      }
      updateBlockDesignBadges(b);
    });
    initDragAndDrop();
    updateSlideDisplay();
  });

  /* Toast thông báo lưu */
  function showToast(msg) {
    let t = document.getElementById('saveToast');
    if (!t) {
      t = document.createElement('div');
      t.id = 'saveToast';
      t.style.cssText = 'position:fixed;top:20px;left:50%;transform:translateX(-50%);background:#059669;color:#fff;padding:8px 20px;border-radius:30px;font-weight:700;font-size:0.92rem;box-shadow:0 10px 25px rgba(0,0,0,0.35);z-index:9999;transition:opacity 0.3s;opacity:0;pointer-events:none;';
      document.body.appendChild(t);
    }
    t.textContent = '✅ ' + msg;
    t.style.opacity = '1';
    setTimeout(() => { t.style.opacity = '0'; }, 2200);
  }

  /* Lưu trực tiếp bài giảng (File System Access API & Fallback) */
  async function saveLecture() {
    const clone = document.documentElement.cloneNode(true);
    
    // Đảm bảo tệp xuất xưởng sạch: reset về chế độ trình chiếu ở Slide 1
    clone.body.className = 'mode-present';
    const allSlides = clone.querySelectorAll('.slide-item');
    allSlides.forEach((s, idx) => {
      if (idx === 0) s.classList.add('active');
      else s.classList.remove('active');
    });
    const allBlocks = clone.querySelectorAll('.content-block');
    allBlocks.forEach(b => {
      b.classList.remove('is-revealed');
      b.classList.remove('is-exited');
      b.removeAttribute('draggable');
      const body = b.querySelector('.block-body');
      if (body) {
        const cleanContent = cleanLatexInHtml(b.getAttribute('data-raw') || body.innerHTML);
        b.setAttribute('data-raw', cleanContent);
        body.innerHTML = cleanContent;
      }
    });
    clone.querySelectorAll('.inline-anim').forEach(a => {
      a.classList.remove('is-revealed');
      a.classList.remove('is-exited');
      a.classList.remove('active-highlight');
    });
    const modal = clone.querySelector('#editModal');
    if (modal) modal.classList.remove('active');
    const toast = clone.querySelector('#saveToast');
    if (toast) toast.remove();
    const tooltip = clone.querySelector('#selectionTooltip');
    if (tooltip) tooltip.remove();

    const htmlString = '<!DOCTYPE html>\n' + clone.outerHTML;

    if ('showSaveFilePicker' in window) {
      try {
        const handle = await window.showSaveFilePicker({
          suggestedName: 'Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html',
          types: [{
            description: 'Tệp bài giảng HTML',
            accept: { 'text/html': ['.html', '.htm'] }
          }]
        });
        const writable = await handle.createWritable();
        await writable.write(htmlString);
        await writable.close();
        showToast('Đã lưu trực tiếp vào tệp thành công!');
        return;
      } catch (err) {
        if (err.name === 'AbortError') return;
      }
    }

    const blob = new Blob([htmlString], { type: 'text/html;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html';
    a.click();
    URL.revokeObjectURL(a.href);
    showToast('Đã lưu bài giảng thành công!');
  }
