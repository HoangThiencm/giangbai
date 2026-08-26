'use strict';

const assert = require('assert');

const store = {};
global.localStorage = {
  getItem: key => (key in store ? store[key] : null),
  setItem: (key, value) => { store[key] = String(value); },
  removeItem: key => { delete store[key]; }
};
function fakeEl() {
  return {
    addEventListener() {},
    value: '',
    checked: false,
    textContent: '',
    innerHTML: '',
    style: {},
    classList: { add() {}, remove() {}, contains() { return false; } },
    querySelectorAll() { return []; },
    appendChild() {},
    append() {},
    replaceChildren() {},
    disabled: false,
    hidden: false,
    dataset: {},
    children: [],
    setAttribute() {},
    getAttribute() { return null; }
  };
}
const documentMock = {
  addEventListener() {},
  getElementById() { return fakeEl(); },
  querySelectorAll() { return []; },
  querySelector() { return fakeEl(); },
  createElement() { return fakeEl(); }
};
global.document = documentMock;
global.window = {
  addEventListener() {},
  localStorage,
  document: documentMock,
  confirm: () => true,
  lucide: { createIcons() {} }
};
global.geminiAPI = { apiKeys: [], onKeyRotatedCallback: null, onStatusCallback: null, syncKeysFromServer: async () => [] };

const {
  sanitizeLessonMarkdown,
  splitKhbdMarkdownTableRow
} = require('../js/khbd-app.js');

function testSplitTableRow() {
  const cells = splitKhbdMarkdownTableRow('| $|x|$ thuộc $A$ | $x \\in A$ |');
  assert.strictEqual(cells.length, 2, 'Không tách cột bên trong $...$');
  assert.ok(cells[0].includes('$|x|$'), 'Giữ nguyên $|x|$');
  const escaped = splitKhbdMarkdownTableRow('| a \\| b | cột 2 |');
  assert.strictEqual(escaped.length, 2, 'Tôn trọng \\|');
  assert.strictEqual(escaped[0], 'a | b');
}

function testKeepLessonLanguage() {
  const source = `# I. MỤC TIÊU
- Học sinh nêu lời chúc sức khỏe trong ngữ liệu bài Đạo đức.
- Hy vọng toán học của biến cố A.
**GV:** Trên đây là các cách xác định tập hợp.

## B. HOẠT ĐỘNG 2
Nội dung pha B còn nguyên.`;
  const out = sanitizeLessonMarkdown(source);
  assert.ok(out.includes('lời chúc sức khỏe'), 'Không xóa chữ chúc trong ngữ liệu');
  assert.ok(out.includes('Hy vọng toán học'), 'Không xóa hy vọng trong nội dung bài');
  assert.ok(out.includes('Trên đây là các cách xác định tập hợp'), 'Không cắt bài vì "trên đây là"');
  assert.ok(out.includes('Nội dung pha B còn nguyên'), 'Không nuốt các pha sau');
}

function testStripClosingBlessing() {
  const source = `# I. MỤC TIÊU
- Nhận biết tập hợp.

Chúc thầy cô soạn bài thành công!`;
  const out = sanitizeLessonMarkdown(source);
  assert.ok(out.includes('Nhận biết tập hợp'));
  assert.ok(!/Chúc thầy cô soạn bài thành công/i.test(out), 'Xóa dòng chúc đứng riêng ở cuối');
}

function testKeepPedagogyNote() {
  const source = `# I. MỤC TIÊU
*Chú ý: Tập rỗng không chứa phần tử nào.*

*Lưu ý của AI: có thể rút gọn đoạn này.*
`;
  const out = sanitizeLessonMarkdown(source);
  assert.ok(out.includes('Tập rỗng không chứa phần tử nào'), 'Giữ *Chú ý:* sư phạm');
  assert.ok(!/rút gọn đoạn này/i.test(out), 'Xóa *Lưu ý của AI*');
}

function testDoNotMergePhaseBTables() {
  const source = `### 1. Hoạt động 2.1: Tập hợp
#### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Giao HĐ 1 | Định nghĩa tập hợp |
| + Bước 2: HS thảo luận | Công thức |

### 2. Hoạt động 2.2: Phần tử
#### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Giao HĐ 2 | Phần tử thuộc tập |
`;
  const out = sanitizeLessonMarkdown(source);
  const headers = out.match(/Hoạt động của GV và HS/g) || [];
  assert.strictEqual(headers.length, 2, 'Không gộp hai bảng pha B');
  assert.ok(out.includes('Định nghĩa tập hợp'));
  assert.ok(out.includes('Phần tử thuộc tập'));
  assert.ok(/Bước 1: Giao HĐ 1[\s\S]*<br>[\s\S]*Bước 2: HS thảo luận/.test(out), 'Gộp hàng vỡ của cùng một bảng');
}

function testOpeningChitchat() {
  const out = sanitizeLessonMarkdown('Tuyệt vời!\n# I. MỤC TIÊU\n- Ý 1');
  assert.ok(out.startsWith('# I. MỤC TIÊU'), 'Cắt lời mở đầu, giữ tiêu đề');
}

testSplitTableRow();
testKeepLessonLanguage();
testStripClosingBlessing();
testKeepPedagogyNote();
testDoNotMergePhaseBTables();
testOpeningChitchat();
console.log('khbd-sanitize-smoke: passed');
