/* Compiled from trochoi.html JSX. Do not edit by hand unless you also update the source block/history. */
const {
  useState,
  useEffect,
  useRef
} = React;

// ============ CONTENT SERVICE ============
const ContentService = {
  // Lấy API keys và module từ localStorage
  getApiKeys: () => {
    const keys = localStorage.getItem('global_gemini_keys');
    return keys ? JSON.parse(keys) : [];
  },
  getDefaultModule: () => {
    return localStorage.getItem('default_gemini_module') || 'gemini-2.5-flash';
  },
  // Generate content từ Gemini
  generate: async (gameType, params) => {
    const {
      subject,
      gradeMax,
      topic,
      difficulty,
      numQuestions
    } = params;

    // Build prompt theo game type
    const prompt = ContentService.buildPrompt(gameType, params);

    // Call Gemini API
    const apiKeys = ContentService.getApiKeys();
    if (!apiKeys.length) throw new Error("Chưa có API Keys! Vui lòng cấu hình trong trang chủ.");
    const defaultModule = ContentService.getDefaultModule();
    let finalError = "";
    const shuffledKeys = [...apiKeys].sort(() => Math.random() - 0.5);
    for (let i = 0; i < shuffledKeys.length; i++) {
      try {
        const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${defaultModule}:generateContent?key=${shuffledKeys[i]}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            contents: [{
              parts: [{
                text: prompt
              }]
            }]
          })
        });
        const data = await res.json();
        if (data.error) throw new Error(data.error.message);
        const text = data.candidates[0].content.parts[0].text;

        // Parse JSON từ response
        const content = ContentService.parseJSON(text);

        // Validate
        const validated = ContentService.validate(content, gameType, gradeMax);
        return validated;
      } catch (e) {
        finalError = e.message;
        console.error(`Key ${i + 1} lỗi:`, e.message);
      }
    }
    throw new Error(`Tất cả keys đều lỗi: ${finalError}`);
  },
  // Build prompt cho từng game type
  buildPrompt: (gameType, params) => {
    const {
      subject,
      gradeMax,
      topic,
      difficulty,
      numQuestions
    } = params;
    const basePrompt = `Bạn là trợ lý tạo nội dung trò chơi học tập.
Môn: ${subject}
Chủ đề: ${topic}
Giới hạn kiến thức: KHÔNG vượt quá chương trình lớp ${gradeMax} (không dùng kiến thức lớp cao hơn).
Độ khó: ${difficulty}
Số câu: ${numQuestions}

YÊU CẦU:
- Câu ngắn gọn, rõ ràng, không đánh đố
- Nếu có công thức toán/lý/hóa, viết bằng LaTeX trong dấu \\( \\) hoặc \\[ \\]
- Trả về DUY NHẤT JSON đúng schema, không thêm chữ nào khác

`;
    let schema = '';
    switch (gameType) {
      case 'elimination':
      case 'speedscore':
        schema = `SCHEMA:
{
  "questions": [
    {
      "id": "q1",
      "type": "mcq",
      "prompt": "Câu hỏi (có thể chứa LaTeX)",
      "choices": ["A", "B", "C", "D"],
      "answer": 0,
      "explanation": "Giải thích ngắn"
    }
  ]
}`;
        break;
      case 'unlock':
        schema = `SCHEMA:
{
  "questions": [
    {
      "id": "lock1",
      "type": "mcq",
      "prompt": "Câu hỏi trọng tâm",
      "choices": ["A", "B", "C", "D"],
      "answer": 0,
      "hint": "Gợi ý nếu sai",
      "explanation": "Giải thích"
    }
  ]
}`;
        break;
      case 'tower':
        schema = `SCHEMA:
{
  "questions": [
    {
      "id": "level1",
      "level": 1,
      "type": "mcq",
      "prompt": "Câu hỏi",
      "choices": ["A", "B", "C", "D"],
      "answer": 0,
      "explanation": "Giải thích"
    }
  ]
}
Level 1-3: dễ, 4-7: vừa, 8-10: khó`;
        break;
      case 'matching':
        schema = `SCHEMA (game ghép cặp — mỗi left khớp DUY NHẤT 1 right theo thứ tự id):
{
  "topicTitle": "Tên chủ đề ngắn",
  "codewordHint": "Gợi ý từ khóa khi ghép xong (vd: Tổng các chữ cái đầu)",
  "pairs": [
    {
      "id": 1,
      "left": "Khái niệm hoặc công thức (ngắn)",
      "right": "Định nghĩa hoặc tên tương ứng",
      "chip": "A",
      "explanation": "Giải thích ngắn khi ghép đúng"
    }
  ]
}
- Tạo đúng ${numQuestions} cặp, left/right không trùng nhau giữa các cặp
- chip: 1 chữ cái in hoa (A,B,C...) dùng ghép từ khóa bí mật theo thứ tự id`;
        break;
      case 'treasure':
        schema = `SCHEMA (game đua vịt — mỗi câu đúng giúp vịt tiến 1 bước về đích):
{
  "raceTitle": "Tên cuộc đua ngắn theo chủ đề",
  "questions": [
    {
      "id": "q1",
      "type": "mcq",
      "prompt": "Câu hỏi",
      "choices": ["A", "B", "C", "D"],
      "answer": 0,
      "explanation": "Giải thích ngắn khi trả lời"
    }
  ]
}
- Tạo đúng ${numQuestions} câu trắc nghiệm 4 đáp án`;
        break;
      case 'escape':
        schema = `SCHEMA (game hứng trứng — mỗi câu là 1 lượt, 4 trứng mang 4 đáp án):
{
  "questions": [
    {
      "id": "q1",
      "type": "mcq",
      "prompt": "Câu hỏi",
      "choices": ["A", "B", "C", "D"],
      "answer": 0,
      "explanation": "Giải thích ngắn khi hứng đúng"
    }
  ]
}
- Tạo đúng ${numQuestions} câu, đáp án ngắn gọn (vừa hiển thị trên trứng rơi)`;
        break;
      case 'teambattle':
        schema = `SCHEMA:
{
  "questions": [
    {
      "id": "q1",
      "type": "mcq",
      "prompt": "Câu hỏi",
      "choices": ["A", "B", "C", "D"],
      "answer": 0,
      "value": 10,
      "isSpecial": false
    }
  ]
}
value: 10/20/30, isSpecial: true cho câu đặc biệt`;
        break;
    }
    return basePrompt + schema;
  },
  // Parse JSON từ text
  parseJSON: text => {
    // Tìm JSON trong response
    let jsonStr = text;

    // Xóa markdown code block
    jsonStr = jsonStr.replace(/```json\n?/g, '').replace(/```\n?/g, '');

    // Tìm object/array
    const startIdx = Math.min(jsonStr.indexOf('{') >= 0 ? jsonStr.indexOf('{') : Infinity, jsonStr.indexOf('[') >= 0 ? jsonStr.indexOf('[') : Infinity);
    const endIdx = Math.max(jsonStr.lastIndexOf('}'), jsonStr.lastIndexOf(']'));
    if (startIdx !== Infinity && endIdx >= 0) {
      jsonStr = jsonStr.substring(startIdx, endIdx + 1);
    }

    // CRITICAL FIX: Xử lý backslash trong LaTeX
    // LaTeX dùng \frac, \sqrt, etc. nhưng JSON cần \\frac, \\sqrt
    // Ta cần escape các backslash TRƯỚC khi parse
    try {
      // Thử parse trực tiếp trước
      return JSON.parse(jsonStr);
    } catch (e) {
      // Nếu lỗi, có thể do backslash chưa escape
      // Tìm tất cả string trong JSON và escape backslash
      const fixed = jsonStr.replace(/"([^"]*)"/g, (match, str) => {
        // Escape backslash trong string
        const escaped = str.replace(/\\/g, '\\\\');
        return `"${escaped}"`;
      });
      try {
        return JSON.parse(fixed);
      } catch (e2) {
        // Nếu vẫn lỗi, báo lỗi gốc
        console.error("JSON parse error:", e2.message);
        console.error("Original JSON:", jsonStr);
        console.error("Fixed JSON:", fixed);
        throw new Error(`Không thể parse JSON: ${e2.message}`);
      }
    }
  },
  // Validate content
  validate: (content, gameType, gradeMax) => {
    // TODO: Thêm validation "khóa lớp" - check từ khóa nâng cao
    // Ví dụ: nếu gradeMax < 11, không được có "đạo hàm", "tích phân"

    const prohibitedKeywords = {
      9: ['đạo hàm', 'tích phân', 'lượng giác nâng cao'],
      10: ['tích phân', 'phương trình vi phân'],
      11: ['phương trình vi phân']
    };

    // Simple validation
    if (!content || (!content.questions && !content.pairs && !content.locks && !content.levels)) {
      throw new Error('Invalid content structure');
    }
    return content;
  }
};

// ============ MATH RENDERER ============
const MathText = ({
  text
}) => {
  const ref = useRef(null);
  useEffect(() => {
    if (!text || !ref.current) return;
    let processed = text.replace(/`([^`]+)`/g, '$$$1$$').replace(/\\\[(.+?)\\\]/g, '$$$$1$$').replace(/\\\((.+?)\\\)/g, '$$$1$$');
    if (processed.includes('\\') && !processed.includes('$')) {
      processed = `$${processed}$`;
    }
    const parts = processed.split(/($$[\s\S]+?$$|\$[\s\S]+?\$)/g);
    ref.current.innerHTML = "";
    parts.forEach(part => {
      if (part.startsWith('$$') && part.endsWith('$$')) {
        const span = document.createElement("span");
        try {
          katex.render(part.slice(2, -2), span, {
            throwOnError: false,
            displayMode: true
          });
        } catch {
          span.textContent = part;
        }
        ref.current.appendChild(span);
      } else if (part.startsWith("$") && part.endsWith("$")) {
        const span = document.createElement("span");
        try {
          katex.render(part.slice(1, -1), span, {
            throwOnError: false,
            displayMode: false
          });
        } catch {
          span.textContent = part;
        }
        ref.current.appendChild(span);
      } else {
        ref.current.appendChild(document.createTextNode(part));
      }
    });
  }, [text]);
  return /*#__PURE__*/React.createElement("span", {
    ref: ref
  });
};

// ============ DUCK RACE ROSTER ============
const normalizeParticipantHeader = value => String(value || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/\s+/g, ' ').trim();

const extractParticipantNamesFromRows = rows => {
  const result = [];
  if (!rows?.length) return result;
  let headerIdx = 0;
  let nameCol = -1;
  let classCol = -1;
  for (let i = 0; i < Math.min(rows.length, 15); i++) {
    const cells = (rows[i] || []).map(cell => String(cell).trim());
    const normalized = cells.map(normalizeParticipantHeader);
    const foundName = normalized.findIndex(h => h.includes('ho va ten') || h.includes('ho ten') || h === 'ten' || h === 'name' || h.includes('hoten'));
    const foundClass = normalized.findIndex(h => h.includes('lop nhom') || h.includes('lop') || h.includes('class') || h.includes('nhom'));
    if (foundName >= 0) {
      headerIdx = i;
      nameCol = foundName;
      classCol = foundClass;
      break;
    }
  }
  if (nameCol >= 0) {
    for (let i = headerIdx + 1; i < rows.length; i++) {
      const row = rows[i] || [];
      const name = String(row[nameCol] || '').trim();
      if (!name || normalizeParticipantHeader(name).startsWith('huong dan')) break;
      const className = classCol >= 0 ? String(row[classCol] || '').trim() : '';
      result.push({
        name,
        className
      });
    }
  } else {
    for (const row of rows) {
      const first = (row || []).map(cell => String(cell).trim()).find(cell => cell && cell.length >= 2 && !/^\d+$/.test(cell));
      if (first) result.push({
        name: first.replace(/^\d+[\.\)\-]\s*/, ''),
        className: ''
      });
    }
  }
  const seen = new Set();
  return result.filter(item => {
    const key = item.name.toLowerCase();
    if (!key || seen.has(key)) return false;
    seen.add(key);
    return true;
  });
};

const buildParticipantList = items => items.map((item, idx) => ({
  id: `p${idx + 1}`,
  name: typeof item === 'string' ? item : item.name,
  className: typeof item === 'string' ? '' : item.className || ''
}));

const parseManualParticipantText = text => buildParticipantList(text.split(/\r?\n/).map(line => line.trim()).filter(Boolean).map(line => ({
  name: line.replace(/^\d+[\.\)\-]\s*/, ''),
  className: ''
})));

const parseParticipantWorkbook = file => new Promise((resolve, reject) => {
  const reader = new FileReader();
  reader.onload = event => {
    try {
      if (typeof XLSX === 'undefined') throw new Error('Thư viện Excel chưa tải. Vui lòng tải lại trang.');
      const data = new Uint8Array(event.target.result);
      const workbook = XLSX.read(data, {
        type: 'array'
      });
      const sheet = workbook.Sheets[workbook.SheetNames[0]];
      const rows = XLSX.utils.sheet_to_json(sheet, {
        header: 1,
        defval: ''
      });
      resolve(buildParticipantList(extractParticipantNamesFromRows(rows)));
    } catch (error) {
      reject(error);
    }
  };
  reader.onerror = () => reject(new Error('Không đọc được file Excel.'));
  reader.readAsArrayBuffer(file);
});

const downloadDuckRaceTemplate = () => {
  if (typeof XLSX === 'undefined') {
    alert('Thư viện Excel chưa tải. Vui lòng tải lại trang.');
    return;
  }
  const rows = [['STT', 'Họ và tên', 'Lớp/Nhóm'], [1, 'Nguyễn Văn An', '6A'], [2, 'Trần Thị Bình', '6A'], [3, 'Lê Văn Cường', '6A'], [], ['Hướng dẫn: Cột Họ và tên bắt buộc. Có thể dùng file danh sách học sinh từ Admin.']];
  const ws = XLSX.utils.aoa_to_sheet(rows);
  ws['!cols'] = [{
    wch: 6
  }, {
    wch: 28
  }, {
    wch: 12
  }];
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, 'DanhSachDuaVit');
  XLSX.writeFile(wb, 'DanhSachDuaVit_Mau.xlsx');
};

// ============ MAIN APP ============
const App = () => {
  const [step, setStep] = useState('SETUP'); // SETUP, GENERATING, REVIEW, EDIT, PLAYING
  const [selectedGame, setSelectedGame] = useState(null);
  const [formData, setFormData] = useState({
    subject: 'Toán',
    gradeMax: 9,
    topic: '',
    difficulty: 'Vừa',
    numQuestions: 10
  });
  const [generatedContent, setGeneratedContent] = useState(null);
  const [loading, setLoading] = useState(false);
  const [participantMode, setParticipantMode] = useState('manual');
  const [manualParticipantText, setManualParticipantText] = useState('');
  const [participants, setParticipants] = useState([]);
  const [participantExcelHint, setParticipantExcelHint] = useState('');

  // EDIT screen states - MUST be at top level, not inside conditional!
  const [editingContent, setEditingContent] = useState(null);
  const [editingIndex, setEditingIndex] = useState(null);
  const [focusedQuestion, setFocusedQuestion] = useState(null);

  // Initialize editingContent when entering EDIT mode
  useEffect(() => {
    if (step === 'EDIT' && generatedContent && !editingContent) {
      setEditingContent(JSON.parse(JSON.stringify(generatedContent)));
    }
  }, [step, generatedContent]);

  // Check auth
  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (!token) {
      alert("Bạn chưa đăng nhập! Hệ thống sẽ chuyển về trang đăng nhập.");
      window.location.href = 'login.html';
    }
  }, []);

  // PASTE IMAGE: Handle Ctrl+V to paste image from clipboard
  useEffect(() => {
    if (step !== 'EDIT' || focusedQuestion === null || !editingContent) return;
    const handlePaste = e => {
      const items = e.clipboardData?.items;
      if (!items) return;
      for (let i = 0; i < items.length; i++) {
        if (items[i].type.indexOf('image') !== -1) {
          e.preventDefault();
          const blob = items[i].getAsFile();
          const reader = new FileReader();
          reader.onload = event => {
            const newContent = {
              ...editingContent
            };
            const questionItems = newContent.questions || newContent.pairs || newContent.locks;
            questionItems[focusedQuestion].image = event.target.result;
            setEditingContent(newContent);
          };
          reader.readAsDataURL(blob);
          break;
        }
      }
    };
    document.addEventListener('paste', handlePaste);
    return () => document.removeEventListener('paste', handlePaste);
  }, [step, focusedQuestion, editingContent]);

  // Danh sách 8 games
  const games = [{
    id: 'elimination',
    name: 'Loại Trực Tiếp',
    icon: 'fa-user-slash',
    color: 'from-red-400 to-pink-500',
    purpose: 'Kiểm tra bài cũ',
    description: 'Trả lời sai → bị loại. Ai trụ lại cuối cùng?',
    suitable: 'Kiểm tra nhanh, tạo áp lực nhẹ'
  }, {
    id: 'speedscore',
    name: 'Đúng Nhanh Ghi Điểm',
    icon: 'fa-bolt',
    color: 'from-yellow-400 to-orange-500',
    purpose: 'Khởi động',
    description: 'Trả lời đúng sớm → nhiều điểm hơn!, Chức năng đa lựa chọn, kéo thả, nối ô',
    suitable: 'Kiểm tra theo cá nhân/nhóm'
  }, {
    id: 'unlock',
    name: 'Mở Khóa Kiến Thức',
    icon: 'fa-unlock',
    color: 'from-blue-400 to-cyan-500',
    purpose: 'Dẫn vào bài mới',
    description: 'Mỗi câu đúng mở 1 ổ khóa. Mở đủ → vào bài!',
    suitable: 'Giới thiệu bài mới'
  }, {
    id: 'teambattle',
    name: 'Team Strategy Quiz',
    icon: 'fa-users',
    color: 'from-purple-400 to-pink-500',
    purpose: 'Đối kháng đội',
    description: '2-4 đội thi đấu! Hợp tác + Chiến thuật. Câu cá nhân + câu đội',
    suitable: 'Ôn tập, củng cố kiến thức'
  }, {
    id: 'tower',
    name: 'Leo Tháp Kiến Thức',
    icon: 'fa-chess-rook',
    color: 'from-purple-400 to-indigo-500',
    purpose: 'Luyện tập tăng dần',
    description: 'Đúng → lên tầng. Sai → tụt xuống. Lên đỉnh!',
    suitable: 'Luyện tập từ dễ đến khó'
  }, {
    id: 'matching',
    name: 'Giải Mã Ghép Đúng',
    icon: 'fa-puzzle-piece',
    color: 'from-green-400 to-emerald-500',
    purpose: 'Củng cố',
    description: 'Ghép khái niệm với định nghĩa, công thức với tên',
    suitable: 'Củng cố khái niệm'
  }, {
    id: 'treasure',
    name: 'Đua Vịt Kiến Thức',
    icon: 'fa-flag-checkered',
    color: 'from-cyan-400 to-blue-500',
    purpose: 'Thi đua nhóm',
    description: 'Mỗi học sinh một vịt — trả lời đúng để tiến về đích. Nhập danh sách tay hoặc Excel',
    suitable: 'Khởi động, thi đua giữa các nhóm'
  }, {
    id: 'escape',
    name: 'Hứng Trứng Vàng',
    icon: 'fa-egg',
    color: 'from-amber-400 to-yellow-500',
    purpose: 'Phản xạ nhanh',
    description: 'Trứng rơi mang đáp án — hứng đúng trứng vàng, sai là trứng thối!',
    suitable: 'Ôn tập vui, luyện phản xạ'
  }];
  const syncManualParticipants = text => {
    setManualParticipantText(text);
    setParticipants(parseManualParticipantText(text));
  };

  const handleParticipantExcel = async event => {
    const file = event.target.files?.[0];
    if (!file) return;
    try {
      const parsed = await parseParticipantWorkbook(file);
      setParticipants(parsed);
      setManualParticipantText(parsed.map(p => p.name).join('\n'));
      setParticipantExcelHint(parsed.length ? `Đã đọc ${parsed.length} học sinh từ "${file.name}".` : 'Không tìm thấy tên hợp lệ trong file.');
    } catch (error) {
      setParticipantExcelHint('');
      alert(error.message || 'Không đọc được file Excel.');
    }
    event.target.value = '';
  };

  const handleGenerateContent = async () => {
    if (!formData.topic.trim()) {
      alert('Vui lòng nhập chủ đề!');
      return;
    }
    if (selectedGame.id === 'treasure' && participants.length < 1) {
      alert('Vui lòng nhập ít nhất 1 học sinh tham gia đua vịt!');
      return;
    }
    setLoading(true);
    setStep('GENERATING');
    try {
      const content = await ContentService.generate(selectedGame.id, formData);
      setGeneratedContent(content);
      setStep('REVIEW');
    } catch (error) {
      alert('Lỗi: ' + error.message);
      setStep('SETUP');
    } finally {
      setLoading(false);
    }
  };
  const handleStartGame = () => {
    // Lưu vào localStorage để các trang game con lấy
    localStorage.setItem('gameData', JSON.stringify({
      gameType: selectedGame.id,
      content: generatedContent,
      formData: formData,
      participants: selectedGame.id === 'treasure' ? participants : undefined
    }));

    // Chuyển sang trang game tương ứng
    window.location.href = `game-${selectedGame.id}.html`;
  };

  // SETUP - Chọn game
  if (!selectedGame) {
    return /*#__PURE__*/React.createElement("div", {
      className: "max-w-7xl mx-auto p-6 fade-in"
    }, /*#__PURE__*/React.createElement("div", {
      className: "text-center mb-8"
    }, /*#__PURE__*/React.createElement("div", {
      className: "mb-4 flex flex-wrap items-center justify-center gap-3"
    }, /*#__PURE__*/React.createElement("button", {
      onClick: () => window.location.href = 'index.html',
      className: "text-gray-500 hover:text-purple-600 font-bold transition"
    }, /*#__PURE__*/React.createElement("i", {
      className: "fas fa-home mr-2"
    }), "Về trang chủ"), /*#__PURE__*/React.createElement("span", {
      className: "text-gray-300"
    }, "|"), /*#__PURE__*/React.createElement("button", {
      onClick: () => window.location.href = 'smartquiz.html',
      className: "text-gray-500 hover:text-purple-600 font-bold transition"
    }, /*#__PURE__*/React.createElement("i", {
      className: "fas fa-arrow-left mr-2"
    }), "Quay lại SmartQuiz")), /*#__PURE__*/React.createElement("h1", {
      className: "text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 mb-3"
    }, "GAME GIÁO DỤC - TRỢ LÝ DẠY HỌC"), /*#__PURE__*/React.createElement("p", {
      className: "text-xl text-gray-600"
    }, "Chọn trò chơi phù hợp với mục tiêu bài học")), /*#__PURE__*/React.createElement("div", {
      className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
    }, games.map(game => /*#__PURE__*/React.createElement("div", {
      key: game.id,
      onClick: () => !game.disabled && setSelectedGame(game),
      className: `game-card bg-white rounded-2xl shadow-lg p-6 border-2 border-transparent relative ${game.disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:border-purple-400'}`
    }, game.disabled && /*#__PURE__*/React.createElement("div", {
      className: "absolute top-3 right-3 px-3 py-1 bg-orange-500 text-white text-xs font-bold rounded-full"
    }, "Đang phát triển"), /*#__PURE__*/React.createElement("div", {
      className: `w-16 h-16 bg-gradient-to-br ${game.color} rounded-2xl flex items-center justify-center mb-4`
    }, /*#__PURE__*/React.createElement("i", {
      className: `fas ${game.icon} text-3xl text-white`
    })), /*#__PURE__*/React.createElement("h3", {
      className: "text-xl font-bold mb-2 text-gray-800"
    }, game.name), /*#__PURE__*/React.createElement("div", {
      className: "text-xs font-semibold text-purple-600 mb-2 uppercase"
    }, game.purpose), /*#__PURE__*/React.createElement("p", {
      className: "text-sm text-gray-600 mb-3"
    }, game.description), /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-gray-500 bg-gray-50 rounded-lg p-2"
    }, /*#__PURE__*/React.createElement("i", {
      className: "fas fa-check-circle text-green-500 mr-1"
    }), game.suitable)))));
  }

  // SETUP - Form nhập thông tin
  if (step === 'SETUP') {
    return /*#__PURE__*/React.createElement("div", {
      className: "max-w-3xl mx-auto p-6 fade-in"
    }, /*#__PURE__*/React.createElement("button", {
      onClick: () => setSelectedGame(null),
      className: "text-gray-500 hover:text-purple-600 font-bold transition mb-6"
    }, /*#__PURE__*/React.createElement("i", {
      className: "fas fa-arrow-left mr-2"
    }), "Chọn game khác"), /*#__PURE__*/React.createElement("div", {
      className: "bg-white rounded-3xl shadow-2xl p-8"
    }, /*#__PURE__*/React.createElement("div", {
      className: "text-center mb-6"
    }, /*#__PURE__*/React.createElement("div", {
      className: `w-20 h-20 bg-gradient-to-br ${selectedGame.color} rounded-3xl flex items-center justify-center mx-auto mb-4`
    }, /*#__PURE__*/React.createElement("i", {
      className: `fas ${selectedGame.icon} text-4xl text-white`
    })), /*#__PURE__*/React.createElement("h2", {
      className: "text-3xl font-bold text-gray-800 mb-2"
    }, selectedGame.name), /*#__PURE__*/React.createElement("p", {
      className: "text-gray-600"
    }, selectedGame.description)), /*#__PURE__*/React.createElement("div", {
      className: "space-y-4"
    }, /*#__PURE__*/React.createElement("div", {
      className: "grid grid-cols-2 gap-4"
    }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("label", {
      className: "block font-bold mb-2 text-gray-700"
    }, "Môn học"), /*#__PURE__*/React.createElement("select", {
      value: formData.subject,
      onChange: e => setFormData({
        ...formData,
        subject: e.target.value
      }),
      className: "w-full p-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 outline-none"
    }, /*#__PURE__*/React.createElement("option", null, "Toán"), /*#__PURE__*/React.createElement("option", null, "Lý"), /*#__PURE__*/React.createElement("option", null, "Hóa"), /*#__PURE__*/React.createElement("option", null, "Sinh"), /*#__PURE__*/React.createElement("option", null, "Văn"), /*#__PURE__*/React.createElement("option", null, "Anh"), /*#__PURE__*/React.createElement("option", null, "Sử"), /*#__PURE__*/React.createElement("option", null, "Địa"))), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("label", {
      className: "block font-bold mb-2 text-gray-700"
    }, "Lớp tối đa"), /*#__PURE__*/React.createElement("select", {
      value: formData.gradeMax,
      onChange: e => setFormData({
        ...formData,
        gradeMax: parseInt(e.target.value)
      }),
      className: "w-full p-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 outline-none"
    }, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].map(g => /*#__PURE__*/React.createElement("option", {
      key: g,
      value: g
    }, "Lớp ", g))))), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("label", {
      className: "block font-bold mb-2 text-gray-700"
    }, "Chủ đề"), /*#__PURE__*/React.createElement("input", {
      type: "text",
      value: formData.topic,
      onChange: e => setFormData({
        ...formData,
        topic: e.target.value
      }),
      className: "w-full p-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 outline-none",
      placeholder: "VD: Phương trình bậc 2, Định luật Ôm, Bảng tuần hoàn..."
    })), /*#__PURE__*/React.createElement("div", {
      className: "grid grid-cols-2 gap-4"
    }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("label", {
      className: "block font-bold mb-2 text-gray-700"
    }, "Độ khó"), /*#__PURE__*/React.createElement("select", {
      value: formData.difficulty,
      onChange: e => setFormData({
        ...formData,
        difficulty: e.target.value
      }),
      className: "w-full p-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 outline-none"
    }, /*#__PURE__*/React.createElement("option", null, "Dễ"), /*#__PURE__*/React.createElement("option", null, "Vừa"), /*#__PURE__*/React.createElement("option", null, "Khó"))), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("label", {
      className: "block font-bold mb-2 text-gray-700"
    }, "Số câu"), /*#__PURE__*/React.createElement("input", {
      type: "number",
      min: "5",
      max: "20",
      value: formData.numQuestions,
      onChange: e => setFormData({
        ...formData,
        numQuestions: parseInt(e.target.value)
      }),
      className: "w-full p-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 outline-none"
    }))), selectedGame.id === 'treasure' && /*#__PURE__*/React.createElement("div", {
      className: "border-2 border-cyan-200 bg-cyan-50 rounded-2xl p-5 space-y-4"
    }, /*#__PURE__*/React.createElement("div", {
      className: "flex flex-wrap items-center justify-between gap-2"
    }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h3", {
      className: "font-bold text-cyan-900 text-lg"
    }, /*#__PURE__*/React.createElement("i", {
      className: "fas fa-users mr-2"
    }), "Danh sách học sinh đua vịt"), /*#__PURE__*/React.createElement("p", {
      className: "text-sm text-cyan-800 mt-1"
    }, "Nhập tay hoặc import Excel — mỗi học sinh là một vịt trên đường đua")), /*#__PURE__*/React.createElement("button", {
      type: "button",
      onClick: downloadDuckRaceTemplate,
      className: "px-4 py-2 bg-white border border-cyan-300 text-cyan-800 rounded-lg text-sm font-bold hover:bg-cyan-100"
    }, /*#__PURE__*/React.createElement("i", {
      className: "fas fa-download mr-1"
    }), "Tải mẫu Excel")), /*#__PURE__*/React.createElement("div", {
      className: "flex gap-2"
    }, /*#__PURE__*/React.createElement("button", {
      type: "button",
      onClick: () => setParticipantMode('manual'),
      className: `px-4 py-2 rounded-lg text-sm font-bold transition ${participantMode === 'manual' ? 'bg-cyan-600 text-white' : 'bg-white text-cyan-800 border border-cyan-200'}`
    }, /*#__PURE__*/React.createElement("i", {
      className: "fas fa-keyboard mr-1"
    }), "Nhập tay"), /*#__PURE__*/React.createElement("button", {
      type: "button",
      onClick: () => setParticipantMode('excel'),
      className: `px-4 py-2 rounded-lg text-sm font-bold transition ${participantMode === 'excel' ? 'bg-cyan-600 text-white' : 'bg-white text-cyan-800 border border-cyan-200'}`
    }, /*#__PURE__*/React.createElement("i", {
      className: "fas fa-file-excel mr-1"
    }), "Import Excel")), participantMode === 'manual' ? /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("label", {
      className: "block font-bold mb-2 text-gray-700"
    }, "Mỗi dòng một học sinh"), /*#__PURE__*/React.createElement("textarea", {
      value: manualParticipantText,
      onChange: e => syncManualParticipants(e.target.value),
      className: "w-full p-3 border-2 border-gray-200 rounded-xl focus:border-cyan-500 outline-none min-h-[140px] font-mono text-sm",
      placeholder: "Nguyễn Văn An\nTrần Thị Bình\nLê Văn Cường\n..."
    }), /*#__PURE__*/React.createElement("p", {
      className: "text-xs text-gray-500 mt-2"
    }, "Gợi ý: dán danh sách từ Word/Excel hoặc gõ trực tiếp, mỗi tên một dòng.")) : /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("label", {
      className: "block font-bold mb-2 text-gray-700"
    }, "Chọn file Excel (.xlsx, .xls, .csv)"), /*#__PURE__*/React.createElement("input", {
      type: "file",
      accept: ".xlsx,.xls,.csv",
      onChange: handleParticipantExcel,
      className: "block w-full text-sm file:mr-3 file:rounded-lg file:border-0 file:bg-cyan-600 file:px-4 file:py-2 file:text-sm file:font-bold file:text-white hover:file:bg-cyan-700"
    }), /*#__PURE__*/React.createElement("p", {
      className: "text-xs text-gray-500 mt-2"
    }, "Hỗ trợ cột ", /*#__PURE__*/React.createElement("strong", null, "Họ và tên"), " / ", /*#__PURE__*/React.createElement("strong", null, "Họ tên"), " — hoặc file mẫu từ Admin."), participantExcelHint && /*#__PURE__*/React.createElement("p", {
      className: "text-sm font-semibold text-cyan-800 mt-2"
    }, participantExcelHint)), participants.length > 0 && /*#__PURE__*/React.createElement("div", {
      className: "bg-white border border-cyan-200 rounded-xl p-3"
    }, /*#__PURE__*/React.createElement("div", {
      className: "text-sm font-bold text-cyan-900 mb-2"
    }, "Đã có ", participants.length, " học sinh:"), /*#__PURE__*/React.createElement("div", {
      className: "flex flex-wrap gap-2 max-h-28 overflow-y-auto"
    }, participants.slice(0, 30).map((p, idx) => /*#__PURE__*/React.createElement("span", {
      key: p.id,
      className: "px-2 py-1 bg-cyan-100 text-cyan-900 rounded-lg text-xs font-semibold"
    }, idx + 1, ". ", p.name)), participants.length > 30 && /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-gray-500"
    }, "... và ", participants.length - 30, " học sinh nữa")))), /*#__PURE__*/React.createElement("button", {
      onClick: handleGenerateContent,
      className: "w-full py-4 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-xl font-bold text-lg hover:shadow-xl transition mt-6"
    }, /*#__PURE__*/React.createElement("i", {
      className: "fas fa-magic mr-2"
    }), "Tạo nội dung với AI"))));
  }

  // GENERATING
  if (step === 'GENERATING') {
    return /*#__PURE__*/React.createElement("div", {
      className: "max-w-2xl mx-auto p-6 fade-in"
    }, /*#__PURE__*/React.createElement("div", {
      className: "bg-white rounded-3xl shadow-2xl p-12 text-center"
    }, /*#__PURE__*/React.createElement("div", {
      className: "w-24 h-24 bg-gradient-to-br from-purple-400 to-blue-500 rounded-full flex items-center justify-center mx-auto mb-6 animate-pulse"
    }, /*#__PURE__*/React.createElement("i", {
      className: "fas fa-robot text-4xl text-white"
    })), /*#__PURE__*/React.createElement("h2", {
      className: "text-3xl font-bold mb-4 text-gray-800"
    }, "AI đang tạo nội dung..."), /*#__PURE__*/React.createElement("p", {
      className: "text-gray-600 mb-6"
    }, "Gemini đang sinh câu hỏi cho game ", /*#__PURE__*/React.createElement("span", {
      className: "font-bold text-purple-600"
    }, selectedGame.name)), /*#__PURE__*/React.createElement("div", {
      className: "w-64 h-2 bg-gray-200 rounded-full mx-auto overflow-hidden"
    }, /*#__PURE__*/React.createElement("div", {
      className: "h-full bg-gradient-to-r from-purple-500 to-blue-500 rounded-full animate-pulse"
    }))));
  }

  // REVIEW
  if (step === 'REVIEW' && generatedContent) {
    return /*#__PURE__*/React.createElement("div", {
      className: "max-w-4xl mx-auto p-6 fade-in"
    }, /*#__PURE__*/React.createElement("div", {
      className: "bg-white rounded-3xl shadow-2xl p-8"
    }, /*#__PURE__*/React.createElement("h2", {
      className: "text-3xl font-bold mb-6 text-gray-800"
    }, /*#__PURE__*/React.createElement("i", {
      className: "fas fa-eye text-purple-600 mr-3"
    }), "Xem trước nội dung"), /*#__PURE__*/React.createElement("div", {
      className: "bg-purple-50 border-2 border-purple-200 rounded-xl p-4 mb-6"
    }, /*#__PURE__*/React.createElement("div", {
      className: "grid grid-cols-2 md:grid-cols-4 gap-4 text-sm"
    }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("span", {
      className: "text-gray-600"
    }, "Môn:"), /*#__PURE__*/React.createElement("span", {
      className: "font-bold ml-2"
    }, formData.subject)), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("span", {
      className: "text-gray-600"
    }, "Lớp:"), /*#__PURE__*/React.createElement("span", {
      className: "font-bold ml-2"
    }, formData.gradeMax)), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("span", {
      className: "text-gray-600"
    }, "Độ khó:"), /*#__PURE__*/React.createElement("span", {
      className: "font-bold ml-2"
    }, formData.difficulty)), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("span", {
      className: "text-gray-600"
    }, "Số câu:"), /*#__PURE__*/React.createElement("span", {
      className: "font-bold ml-2"
    }, generatedContent.questions?.length || generatedContent.pairs?.length || generatedContent.locks?.length || 0)))), /*#__PURE__*/React.createElement("div", {
      className: "max-h-96 overflow-y-auto mb-6 space-y-4"
    }, generatedContent.questions && generatedContent.questions.slice(0, 3).map((q, idx) => /*#__PURE__*/React.createElement("div", {
      key: idx,
      className: "bg-gray-50 p-4 rounded-xl"
    }, /*#__PURE__*/React.createElement("div", {
      className: "font-bold text-gray-700 mb-2"
    }, "Câu ", idx + 1, ":"), /*#__PURE__*/React.createElement("div", {
      className: "text-gray-800"
    }, /*#__PURE__*/React.createElement(MathText, {
      text: q.prompt
    })), q.choices && /*#__PURE__*/React.createElement("div", {
      className: "mt-2 space-y-1"
    }, q.choices.map((choice, cidx) => /*#__PURE__*/React.createElement("div", {
      key: cidx,
      className: `text-sm ${q.answer === cidx ? 'text-green-600 font-bold' : 'text-gray-600'}`
    }, String.fromCharCode(65 + cidx), ". ", /*#__PURE__*/React.createElement(MathText, {
      text: choice
    })))))), generatedContent.questions && generatedContent.questions.length > 3 && /*#__PURE__*/React.createElement("div", {
      className: "text-center text-gray-500 text-sm"
    }, "... và ", generatedContent.questions.length - 3, " câu nữa"), generatedContent.pairs && generatedContent.pairs.slice(0, 4).map((pair, idx) => /*#__PURE__*/React.createElement("div", {
      key: idx,
      className: "bg-green-50 p-4 rounded-xl border border-green-200"
    }, /*#__PURE__*/React.createElement("div", {
      className: "font-bold text-gray-700 mb-2"
    }, "Cặp ", idx + 1, ":"), /*#__PURE__*/React.createElement("div", {
      className: "grid md:grid-cols-2 gap-3 text-sm"
    }, /*#__PURE__*/React.createElement("div", {
      className: "bg-white p-3 rounded-lg"
    }, /*#__PURE__*/React.createElement("span", {
      className: "text-green-700 font-semibold"
    }, "Trái: "), /*#__PURE__*/React.createElement(MathText, {
      text: pair.left
    })), /*#__PURE__*/React.createElement("div", {
      className: "bg-white p-3 rounded-lg"
    }, /*#__PURE__*/React.createElement("span", {
      className: "text-emerald-700 font-semibold"
    }, "Phải: "), /*#__PURE__*/React.createElement(MathText, {
      text: pair.right
    }))))), generatedContent.pairs && generatedContent.pairs.length > 4 && /*#__PURE__*/React.createElement("div", {
      className: "text-center text-gray-500 text-sm"
    }, "... và ", generatedContent.pairs.length - 4, " cặp nữa")), /*#__PURE__*/React.createElement("div", {
      className: "flex gap-4"
    }, /*#__PURE__*/React.createElement("button", {
      onClick: () => setStep('SETUP'),
      className: "px-6 py-3 bg-gray-500 text-white rounded-xl font-bold hover:bg-gray-600 transition"
    }, /*#__PURE__*/React.createElement("i", {
      className: "fas fa-redo mr-2"
    }), "Tạo lại"), /*#__PURE__*/React.createElement("button", {
      onClick: () => setStep('EDIT'),
      className: "flex-1 py-3 bg-blue-600 text-white rounded-xl font-bold hover:bg-blue-700 transition"
    }, /*#__PURE__*/React.createElement("i", {
      className: "fas fa-edit mr-2"
    }), "Chỉnh sửa (sửa câu, thêm ảnh)"), /*#__PURE__*/React.createElement("button", {
      onClick: handleStartGame,
      className: "flex-1 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-xl font-bold hover:shadow-xl transition"
    }, /*#__PURE__*/React.createElement("i", {
      className: "fas fa-play mr-2"
    }), "Chơi luôn"))));
  }

  // EDIT - Chỉnh sửa nội dung
  if (step === 'EDIT' && editingContent) {
    const questions = editingContent.questions || editingContent.pairs || editingContent.locks || [];
    const handleImageUpload = (qIdx, e) => {
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = event => {
        const newContent = {
          ...editingContent
        };
        const items = newContent.questions || newContent.pairs || newContent.locks;
        items[qIdx].image = event.target.result;
        setEditingContent(newContent);
      };
      reader.readAsDataURL(file);
    };
    const handleSaveEdit = (qIdx, field, value) => {
      const newContent = {
        ...editingContent
      };
      const items = newContent.questions || newContent.pairs || newContent.locks;
      items[qIdx][field] = value;
      setEditingContent(newContent);
    };
    const handleSaveChoice = (qIdx, cIdx, value) => {
      const newContent = {
        ...editingContent
      };
      const items = newContent.questions || newContent.pairs || newContent.locks;
      items[qIdx].choices[cIdx] = value;
      setEditingContent(newContent);
    };
    const handleFinishEdit = () => {
      setGeneratedContent(editingContent);
      handleStartGame(); // Lưu và chơi luôn
    };
    return /*#__PURE__*/React.createElement("div", {
      className: "max-w-6xl mx-auto p-6 fade-in"
    }, /*#__PURE__*/React.createElement("div", {
      className: "bg-white rounded-3xl shadow-2xl p-8"
    }, /*#__PURE__*/React.createElement("div", {
      className: "flex justify-between items-center mb-6"
    }, /*#__PURE__*/React.createElement("h2", {
      className: "text-3xl font-bold text-gray-800"
    }, /*#__PURE__*/React.createElement("i", {
      className: "fas fa-edit text-blue-600 mr-3"
    }), "Chỉnh sửa nội dung"), /*#__PURE__*/React.createElement("div", {
      className: "flex gap-3"
    }, /*#__PURE__*/React.createElement("button", {
      onClick: () => setStep('REVIEW'),
      className: "px-6 py-3 bg-gray-500 text-white rounded-xl font-bold hover:bg-gray-600"
    }, /*#__PURE__*/React.createElement("i", {
      className: "fas fa-arrow-left mr-2"
    }), "Quay lại"), /*#__PURE__*/React.createElement("button", {
      onClick: handleFinishEdit,
      className: "px-8 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-xl font-bold hover:shadow-xl"
    }, /*#__PURE__*/React.createElement("i", {
      className: "fas fa-save mr-2"
    }), "Lưu & Chơi"))), /*#__PURE__*/React.createElement("div", {
      className: "bg-yellow-50 border-2 border-yellow-300 rounded-xl p-4 mb-6"
    }, /*#__PURE__*/React.createElement("div", {
      className: "flex items-start gap-3"
    }, /*#__PURE__*/React.createElement("i", {
      className: "fas fa-lightbulb text-yellow-600 text-xl mt-1"
    }), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
      className: "font-bold text-yellow-800 mb-1"
    }, "Bạn có thể:"), /*#__PURE__*/React.createElement("ul", {
      className: "text-sm text-yellow-700 space-y-1"
    }, /*#__PURE__*/React.createElement("li", null, "✏️ Sửa câu hỏi, đáp án nếu AI sinh không chính xác"), /*#__PURE__*/React.createElement("li", null, "🖼️ ", /*#__PURE__*/React.createElement("strong", null, "Thêm ảnh:"), " Click \"Thêm ảnh\" hoặc ", /*#__PURE__*/React.createElement("span", {
      className: "bg-yellow-200 px-2 py-0.5 rounded font-mono"
    }, "Ctrl+V"), " paste ảnh đã chụp màn hình"), /*#__PURE__*/React.createElement("li", null, "✅ Đổi đáp án đúng bằng cách click radio button"), /*#__PURE__*/React.createElement("li", {
      className: "text-xs italic"
    }, "💡 Click vào vùng câu hỏi trước khi paste ảnh"))))), /*#__PURE__*/React.createElement("div", {
      className: "space-y-6 max-h-[600px] overflow-y-auto pr-2"
    }, questions.map((q, qIdx) => /*#__PURE__*/React.createElement("div", {
      key: qIdx,
      onClick: () => setFocusedQuestion(qIdx),
      className: `bg-gray-50 border-2 rounded-xl p-6 hover:border-blue-300 transition cursor-pointer ${focusedQuestion === qIdx ? 'border-blue-500 bg-blue-50' : 'border-gray-200'}`
    }, /*#__PURE__*/React.createElement("div", {
      className: "flex justify-between items-start mb-4"
    }, /*#__PURE__*/React.createElement("div", {
      className: "font-bold text-lg text-gray-700"
    }, "Câu ", qIdx + 1), /*#__PURE__*/React.createElement("label", {
      className: "px-4 py-2 bg-blue-500 text-white rounded-lg cursor-pointer hover:bg-blue-600 transition text-sm"
    }, /*#__PURE__*/React.createElement("i", {
      className: "fas fa-image mr-2"
    }), "Thêm ảnh", /*#__PURE__*/React.createElement("input", {
      type: "file",
      accept: "image/*",
      onChange: e => handleImageUpload(qIdx, e),
      className: "hidden"
    }))), q.image && /*#__PURE__*/React.createElement("div", {
      className: "mb-4 relative"
    }, /*#__PURE__*/React.createElement("img", {
      src: q.image,
      className: "max-w-md max-h-64 rounded-lg border-2 border-blue-300",
      alt: "Question"
    }), /*#__PURE__*/React.createElement("button", {
      onClick: () => handleSaveEdit(qIdx, 'image', null),
      className: "absolute top-2 right-2 bg-red-500 text-white rounded-full w-8 h-8 hover:bg-red-600"
    }, /*#__PURE__*/React.createElement("i", {
      className: "fas fa-times"
    }))), /*#__PURE__*/React.createElement("div", {
      className: "mb-4"
    }, /*#__PURE__*/React.createElement("label", {
      className: "block font-semibold text-gray-700 mb-2"
    }, "Câu hỏi:"), /*#__PURE__*/React.createElement("textarea", {
      value: q.prompt || q.left || '',
      onChange: e => handleSaveEdit(qIdx, q.prompt ? 'prompt' : 'left', e.target.value),
      className: "w-full p-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 outline-none min-h-[80px]"
    })), q.choices && /*#__PURE__*/React.createElement("div", {
      className: "space-y-3"
    }, /*#__PURE__*/React.createElement("label", {
      className: "block font-semibold text-gray-700"
    }, "Các đáp án:"), q.choices.map((choice, cIdx) => /*#__PURE__*/React.createElement("div", {
      key: cIdx,
      className: "flex items-center gap-3"
    }, /*#__PURE__*/React.createElement("input", {
      type: "radio",
      name: `answer-${qIdx}`,
      checked: q.answer === cIdx,
      onChange: () => handleSaveEdit(qIdx, 'answer', cIdx),
      className: "w-5 h-5 text-green-600 cursor-pointer"
    }), /*#__PURE__*/React.createElement("span", {
      className: "font-bold text-gray-600 w-8"
    }, String.fromCharCode(65 + cIdx), "."), /*#__PURE__*/React.createElement("input", {
      type: "text",
      value: choice,
      onChange: e => handleSaveChoice(qIdx, cIdx, e.target.value),
      className: `flex-1 p-2 border-2 rounded-lg outline-none ${q.answer === cIdx ? 'border-green-500 bg-green-50' : 'border-gray-300'}`
    })))), q.right && /*#__PURE__*/React.createElement("div", {
      className: "mt-4"
    }, /*#__PURE__*/React.createElement("label", {
      className: "block font-semibold text-gray-700 mb-2"
    }, "Định nghĩa/Ghép với:"), /*#__PURE__*/React.createElement("textarea", {
      value: q.right,
      onChange: e => handleSaveEdit(qIdx, 'right', e.target.value),
      className: "w-full p-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 outline-none"
    })))))));
  }
  return null;
};
ReactDOM.render(/*#__PURE__*/React.createElement(App, null), document.getElementById('root'));
