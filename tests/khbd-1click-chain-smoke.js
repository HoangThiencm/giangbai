'use strict';

const assert = require('assert');

console.log('================================================================');
console.log('BẮT ĐẦU KIỂM THỬ DÂY CHUYỀN TUẦN TỰ 6 BƯỚC (1-CLICK CHAIN PIPELINE)');
console.log('================================================================');

// 1. Tạo mock DOM & localStorage môi trường Node.js
function createMockDOM() {
  const store = {};
  const localStorageMock = {
    getItem: (key) => (key in store ? store[key] : null),
    setItem: (key, value) => { store[key] = String(value); },
    removeItem: (key) => { delete store[key]; },
    clear: () => { Object.keys(store).forEach(k => delete store[k]); }
  };

  const elementsById = {};
  const elementsByClass = {};

  function createElement(tag) {
    const el = {
      tagName: tag.toUpperCase(),
      id: '',
      className: '',
      value: '',
      checked: false,
      textContent: '',
      innerHTML: '',
      hidden: false,
      disabled: false,
      style: {},
      dataset: {},
      children: [],
      childNodes: [],
      classList: {
        _classes: new Set(),
        add(c) { this._classes.add(c); el.className = Array.from(this._classes).join(' '); },
        remove(c) { this._classes.delete(c); el.className = Array.from(this._classes).join(' '); },
        contains(c) { return this._classes.has(c); }
      },
      getAttribute(attr) {
        if (attr === 'class') return el.className;
        if (attr === 'id') return el.id;
        if (attr === 'value') return el.value;
        if (attr && attr.startsWith('data-')) return el.dataset[attr.slice(5)];
        return el[attr] || null;
      },
      setAttribute(attr, val) {
        if (attr === 'class') {
          el.className = val;
          el.classList._classes = new Set(val.split(/\s+/).filter(Boolean));
        } else if (attr === 'id') {
          el.id = val;
        } else if (attr && attr.startsWith('data-')) {
          el.dataset[attr.slice(5)] = val;
        } else {
          el[attr] = val;
        }
      },
      hasAttribute(attr) {
        return el.getAttribute(attr) !== null;
      },
      appendChild(child) {
        el.children.push(child);
        el.childNodes.push(child);
        return child;
      },
      append(...items) {
        items.forEach(item => el.appendChild(item));
      },
      replaceChildren(...items) {
        el.children = [];
        el.childNodes = [];
        el.innerHTML = '';
        items.forEach(item => el.appendChild(item));
      },
      addEventListener(event, handler) {},
      remove() {
        if (el.parentNode) {
          el.parentNode.children = el.parentNode.children.filter(c => c !== el);
          el.parentNode.childNodes = el.parentNode.childNodes.filter(c => c !== el);
        }
      },
      querySelectorAll(selector) {
        return mockDoc.querySelectorAll(selector, el);
      },
      closest(selector) { return null; }
    };
    return el;
  }

  function registerElement(id, classes = [], initialValue = '', initialChecked = false) {
    const el = createElement('div');
    el.id = id;
    classes.forEach(c => el.classList.add(c));
    el.value = initialValue;
    el.checked = initialChecked;
    elementsById[id] = el;
    classes.forEach(c => {
      if (!elementsByClass[c]) elementsByClass[c] = [];
      elementsByClass[c].push(el);
    });
    return el;
  }

  const mockDoc = {
    createElement,
    createTextNode(text) { return { nodeType: 3, textContent: text, nodeValue: text }; },
    createDocumentFragment() { return createElement('fragment'); },
    getElementById(id) {
      if (!elementsById[id]) {
        elementsById[id] = createElement('div');
        elementsById[id].id = id;
      }
      return elementsById[id];
    },
    querySelectorAll(selector, root) {
      if (selector.startsWith('.')) {
        const cls = selector.slice(1);
        return elementsByClass[cls] || [];
      }
      if (selector.startsWith('#')) {
        const id = selector.slice(1);
        return elementsById[id] ? [elementsById[id]] : [];
      }
      return [];
    },
    querySelector(selector) {
      const list = this.querySelectorAll(selector);
      return list && list.length ? list[0] : null;
    },
    addEventListener() {}
  };

  return { localStorageMock, mockDoc, registerElement, elementsById };
}

const dom = createMockDOM();
global.window = {
  addEventListener() {},
  confirm: () => true,
  localStorage: dom.localStorageMock,
  document: dom.mockDoc,
  lucide: { createIcons: () => {} }
};
global.document = dom.mockDoc;
global.localStorage = dom.localStorageMock;

// Đăng ký các element UI
[
  'selectGrade', 'inputSchool', 'inputGroup', 'inputTeacher', 'inputSubject',
  'inputTopicCustom', 'inputDuration', 'selectLesson', 'inputClassSize',
  'selectReadiness', 'selectGrouping', 'inputClassProfileNote', 'inputSupportNote',
  'inputSpecialRequirements', 'editorVision', 'editorObjectives', 'editorMaterials',
  'editorActivity', 'hasProjector', 'hasInternet', 'hasDevices',
  'toggleDigitalCompetency', 'toggleAiCompetency', 'toggleForeignLanguage', 'toggleInclusiveSupport',
  'selectMyDraft', 'btnImportLegacyDraft', 'fileInputImages', 'imgCountBadge',
  'imageGallery', 'fullLessonPreview', 'previewVision', 'previewObjectives',
  'previewMaterials', 'previewActivity', 'toastContainer', 'digitalStandardsPanel',
  'aiStandardsPanel', 'methodsCatalogPanel', 'techniquesCatalogPanel', 'activitiesCatalogPanel',
  'btn1ClickGenerate', 'btnCancelGeneration', 'statusFooterText'
].forEach(id => dom.registerElement(id));

// Mock global UI helpers
const progressHistory = [];
global.onProgressUpdate = (pct, msg) => {
  progressHistory.push({ pct, msg });
};
global.updateProgress = (pct, msg) => {
  progressHistory.push({ pct, msg });
};
global.hideProgress = () => {};
global.showToast = (msg, type) => {};
global.switchMainTab = (tab) => {};
global.renderMathPreview = (text, id) => {};
global.renderFullLessonPreview = () => {};
global.openModal = (id) => {};
global.closeModal = (id) => {};
global.confirm = () => true;

try {
  const curr = require('../js/khbd-curriculum.js');
  Object.assign(global, curr);
} catch (e) {}

try {
  const ped = require('../js/khbd-pedagogy-catalog.js');
  Object.assign(global, ped);
} catch (e) {}

try {
  const prm = require('../js/khbd-prompts.js');
  Object.assign(global, prm);
} catch (e) {}

try {
  const { KHBD_STANDARDS } = require('../js/khbd-standards.js');
  global.KHBD_STANDARDS = KHBD_STANDARDS;
} catch (e) {
  global.KHBD_STANDARDS = { digitalCompetencies: { domains: [] }, aiCompetencies: { domains: [] } };
}

// Mock geminiAPI
const geminiCalls = [];
const keyRotationLog = [];

global.geminiAPI = {
  apiKeys: ["AIzaSyFakeKey1", "AIzaSyFakeKey2", "AIzaSyFakeKey3"],
  mistralKeys: [],
  currentKeyIndex: 0,
  selectedModel: "gemini-3.7-flash",
  rotateKey(reason = "") {
    const prev = this.currentKeyIndex;
    this.currentKeyIndex = (this.currentKeyIndex + 1) % this.apiKeys.length;
    keyRotationLog.push({ prev, current: this.currentKeyIndex, reason });
  },
  async generateContent(prompt, media, systemRole, temperature, signal, options) {
    geminiCalls.push({ prompt, media, options });

    if (prompt.includes("HOẠT ĐỘNG HƯỚNG DẪN VỀ NHÀ**") || prompt.includes("GENERATE_ACTIVITY_E")) {
      return `## E. HOẠT ĐỘNG 5: HƯỚNG DẪN VỀ NHÀ (5 phút)
### a) Mục tiêu:
- Hệ thống hóa toàn bộ kiến thức về tam giác đều, hình vuông và định hướng tự học ở nhà.
### b) Nội dung:
- 1. Học cái gì: Ôn tập đặc điểm cạnh, góc của tam giác đều, hình vuông và vẽ sơ đồ tư duy tóm tắt vào vở.
- 2. Làm bài tập gì: Hoàn thành bài tập 3, 4 SGK trang 79 và bài 1, 2 SBT.
- 3. Bài tập mở rộng: Tìm hiểu thêm hình dạng tổ ong trong tự nhiên và giải thích vì sao tổ ong có cấu trúc lục giác đều.
- 4. Chuẩn bị bài sau: Đọc trước bài "Hình chữ nhật - Hình thoi" và chuẩn bị giấy gấp hình.
### c) Sản phẩm:
- Sơ đồ tư duy bài học trong vở ghi.
- Bài giải hoàn chỉnh các bài tập 3, 4 SGK và bài mở rộng trong vở bài tập.
### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ: **GV:** Trình chiếu slide hướng dẫn về nhà và nêu câu lệnh: "Các em về nhà hoàn thành 4 nhiệm vụ: (1) Vẽ sơ đồ tư duy, (2) Giải bài 3, 4 SGK, (3) Tìm hiểu cấu trúc tổ ong, (4) Đọc trước bài mới". **HS:** Lắng nghe và ghi chép vào sổ tay.<br>+ Bước 2: Thực hiện nhiệm vụ: **HS:** Tự giác ôn bài và giải bài tập tại nhà. **GV:** Hỗ trợ giải đáp qua nhóm học tập trực tuyến khi cần.<br>+ Bước 3: Báo cáo, thảo luận: **HS:** Nộp vở bài tập và sơ đồ tư duy vào đầu tiết học sau để cán sự lớp kiểm tra. **GV:** Đánh giá xác suất 5 học sinh.<br>+ Bước 4: Kết luận, nhận định: **GV:** Nhận xét tinh thần tự học của cả lớp và giải đáp thắc mắc bài cũ ở đầu tiết học tiếp theo. **HS:** Ghi nhận và rút kinh nghiệm. | **Hướng dẫn học ở nhà:**<br>- 1. Ôn tập kiến thức và vẽ sơ đồ tư duy.<br>- 2. Hoàn thành bài tập 3, 4 SGK trang 79 & SBT.<br>- 3. Bài tập mở rộng: Khám phá cấu trúc tổ ong.<br>- 4. Chuẩn bị bài học tiếp theo. |`;
    }

    if (prompt.includes("HOẠT ĐỘNG VẬN DỤNG**") || prompt.includes("GENERATE_ACTIVITY_D")) {
      return `## D. HOẠT ĐỘNG 4: VẬN DỤNG (10 phút)
### a) Mục tiêu:
- Vận dụng kiến thức về tam giác đều và hình vuông để thiết kế hoa văn trang trí.
### b) Nội dung:
- Bài toán vận dụng thực tế: Cắt ghép các mảnh tam giác đều để tạo thành lục giác đều trang trí khăn trải bàn.
### c) Sản phẩm:
- Sản phẩm hoa văn ghép từ 6 tam giác đều của các nhóm.
### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ: **GV:** Phát cho mỗi nhóm 6 tam giác đều giấy màu và giao việc: "Hãy ghép 6 hình tam giác này thành một hình lục giác đều hoàn chỉnh". **HS:** Nhận đồ dùng.<br>+ Bước 2: Thực hiện nhiệm vụ: **HS:** Thảo luận nhóm 4 người để sắp xếp và dán hình vào giấy A3. **GV:** Hướng dẫn nhóm gặp khó khăn.<br>+ Bước 3: Báo cáo, thảo luận: **HS:** Đại diện treo sản phẩm lên bảng phụ. **GV:** Tổ chức bình chọn mẫu trang trí đẹp nhất.<br>+ Bước 4: Kết luận, nhận định: **GV:** Chốt lại tính ứng dụng phong phú của hình học trong đời sống. **HS:** Lắng nghe và hoàn thiện sản phẩm. | **Vận dụng thực tế:**<br>- Ghép 6 tam giác đều bằng nhau tạo thành hình lục giác đều.<br>- Ứng dụng trang trí gạch lát sàn, hoa văn kiến trúc. |`;
    }

    if (prompt.includes("HOẠT ĐỘNG LUYỆN TẬP**") || prompt.includes("GENERATE_ACTIVITY_C")) {
      return `## C. HOẠT ĐỘNG 3: LUYỆN TẬP (20 phút)
### a) Mục tiêu:
- Rèn luyện kĩ năng vẽ tam giác đều và hình vuông bằng compa và thước kẻ.
### b) Nội dung:
- Giải bài tập 1 và bài tập 2 trong SGK trang 78.
### c) Sản phẩm:
- Hình vẽ tam giác đều cạnh 4cm và hình vuông cạnh 5cm trong vở bài tập.
### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ: **GV:** Giao nhiệm vụ: "Hãy vẽ tam giác đều $MNP$ có cạnh bằng $4\\text{ cm}$ bằng thước và compa". **HS:** Chuẩn bị dụng cụ.<br>+ Bước 2: Thực hiện nhiệm vụ: **HS:** Vẽ hình theo từng bước vào vở. **GV:** Quan sát uốn nắn thao tác cầm compa.<br>+ Bước 3: Báo cáo, thảo luận: **HS:** 2 học sinh lên bảng vẽ hình và trình bày cách vẽ. **GV:** Cho cả lớp nhận xét.<br>+ Bước 4: Kết luận, nhận định: **GV:** Nhận xét độ chính xác và tính thẩm mỹ của hình vẽ. **HS:** Tự chỉnh sửa hình vẽ của mình. | **Bài 1 (SGK trang 78):**<br>- Vẽ đoạn thẳng $MN = 4\\text{ cm}$.<br>- Dùng compa vẽ hai cung tròn tâm $M$ và $N$ bán kính $4\\text{ cm}$ cắt nhau tại $P$.<br>- Nối $P$ với $M$ và $N$. |`;
    }

    if (prompt.includes("HOẠT ĐỘNG HÌNH THÀNH KIẾN THỨC MỚI") || prompt.includes("GENERATE_ACTIVITY_B")) {
      return `## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (45 phút)
### 1. Hoạt động 2.1: Tam giác đều (20 phút)
#### a) Mục tiêu:
- Nhận biết các yếu tố của tam giác đều: 3 cạnh bằng nhau, 3 góc bằng nhau.
#### b) Nội dung:
- Thực hiện Hoạt động khám phá 1 trong SGK: đo độ dài 3 cạnh và 3 góc.
#### c) Sản phẩm:
- Kết quả đo đạc: $AB = BC = CA$ và $\\widehat{A} = \\widehat{B} = \\widehat{C} = 60^\\circ$.
#### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ: **GV:** Giao phiếu học tập 1: "Hãy dùng thước thẳng và thước đo góc để đo tam giác $ABC$". **HS:** Nhận phiếu học tập.<br>+ Bước 2: Thực hiện nhiệm vụ: **HS:** Làm việc cá nhân 3 phút rồi thảo luận nhóm 4 phút. **GV:** Hướng dẫn cách đặt thước đo góc chính xác.<br>+ Bước 3: Báo cáo, thảo luận: **HS:** Nhóm 1 báo cáo kết quả đo đạc. **GV:** Yêu cầu nhóm khác đối chiếu kết quả.<br>+ Bước 4: Kết luận, nhận định: **GV:** Chốt kiến thức tam giác đều có 3 cạnh bằng nhau và 3 góc bằng nhau. **HS:** Ghi định nghĩa vào vở. | **1. Tam giác đều**<br>- Tam giác đều $ABC$ có:<br>+ 3 cạnh bằng nhau: $AB = BC = CA$.<br>+ 3 góc bằng nhau: $\\widehat{A} = \\widehat{B} = \\widehat{C} = 60^\\circ$. |

### 2. Hoạt động 2.2: Hình vuông (25 phút)
#### a) Mục tiêu:
- Nhận biết các yếu tố của hình vuông: 4 cạnh bằng nhau, 4 góc vuông, 2 đường chéo bằng nhau.
#### b) Nội dung:
- Thực hiện Hoạt động khám phá 2 trong SGK: đo cạnh, góc và đường chéo hình vuông.
#### c) Sản phẩm:
- Bảng tổng hợp các tính chất của hình vuông $ABCD$.
#### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ: **GV:** Yêu cầu: "Hãy đo 4 cạnh và 2 đường chéo của hình vuông $ABCD$". **HS:** Đọc yêu cầu.<br>+ Bước 2: Thực hiện nhiệm vụ: **HS:** Thao tác đo và ghi vào vở. **GV:** Theo dõi và hỗ trợ.<br>+ Bước 3: Báo cáo, thảo luận: **HS:** Đại diện lên bảng ghi số liệu. **GV:** Khắc sâu tính chất 2 đường chéo.<br>+ Bước 4: Kết luận, nhận định: **GV:** Đánh giá sản phẩm và kết luận. **HS:** Ghi bài vào vở. | **2. Hình vuông**<br>- Hình vuông $ABCD$ có:<br>+ 4 cạnh bằng nhau: $AB = BC = CD = DA$.<br>+ 4 góc bằng nhau và bằng $90^\\circ$.<br>+ 2 đường chéo bằng nhau: $AC = BD$. |`;
    }

    if (prompt.includes("HOẠT ĐỘNG MỞ ĐẦU (TIẾP CẬN VẤN ĐỀ)") || prompt.includes("GENERATE_ACTIVITY_A")) {
      return `## A. HOẠT ĐỘNG 1: MỞ ĐẦU (10 phút)
### a) Mục tiêu:
- Tạo tâm thế hứng thú học tập cho học sinh, tiếp cận khái niệm tam giác đều.
### b) Nội dung:
- Quan sát các đồ vật trong thực tế có hình tam giác đều.
### c) Sản phẩm:
- Câu trả lời của học sinh về đặc điểm các cạnh và góc của tam giác đều.
### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ: **GV:** Chiếu hình ảnh biển báo giao thông và hỏi: "Quan sát biển báo và cho biết có điều gì đặc biệt về 3 cạnh?". **HS:** Quan sát hình ảnh.<br>+ Bước 2: Thực hiện nhiệm vụ: **HS:** Thảo luận cặp đôi trong 2 phút. **GV:** Quan sát, định hướng.<br>+ Bước 3: Báo cáo, thảo luận: **HS:** Đại diện phát biểu: "3 cạnh bằng nhau". **GV:** Mời bạn nhận xét.<br>+ Bước 4: Kết luận, nhận định: **GV:** Nhận xét và dẫn dắt vào bài mới. **HS:** Ghi bài vào vở. | **Quan sát mở đầu**<br>- Hình ảnh biển báo có 3 cạnh bằng nhau.<br>- Dẫn vào bài học mới. |`;
    }

    if (prompt.includes("soạn phần I + II") || prompt.includes("GENERATE_CORE_LESSON")) {
      return `<<<KHBD_I>>>
# I. MỤC TIÊU
## 1. Về kiến thức:
- Nhận biết và phát biểu được khái niệm tam giác đều, hình vuông, lục giác đều.
## 2. Về năng lực:
### a) Năng lực chung:
- Tự chủ và tự học: tự giác thực hiện nhiệm vụ vẽ hình.
- Giao tiếp và hợp tác: thảo luận nhóm.
### b) Năng lực đặc thù:
- Năng lực tư duy và lập luận toán học.
## 3. Về phẩm chất:
- Chăm chỉ, trung thực, trách nhiệm.
<<<KHBD_II>>>
# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
- Giáo viên: Thước kẻ, compa, êke, hình mẫu tam giác đều.
- Học sinh: Vở ghi, bút chì, thước đo độ.`;
    }

    return "Nội dung mẫu sinh ra từ AI.";
  }
};

// Nạp các hàm cần test từ js/khbd-app.js
const {
  appState,
  handle1ClickGenerate
} = require('../js/khbd-app.js');

async function run1ClickChainSmokeTest() {
  console.log('-> 1. Thiết lập cấu hình đầu vào cho appState...');
  appState.selectedGrade = '6';
  appState.subject = 'Toán';
  appState.selectedSubject = 'toan';
  appState.customTopic = 'Tam giác đều. Hình vuông. Lục giác đều';
  appState.duration = '02 tiết (90 phút)';
  appState.content.vision = `
1. **Tổng quan bài học:** Bài 3: Tam giác đều. Hình vuông. Lục giác đều (Toán 6).
2. **Khung kiến thức trọng tâm:**
- Mục 1: Tam giác đều
- Mục 2: Hình vuông
- Mục 3: Lục giác đều
3. **Chuỗi hoạt động khám phá trong SGK:**
- HĐKP 1: Quan sát tam giác đều
- HĐKP 2: Quan sát hình vuông
4. **Hệ thống bài tập:**
- Bài 1: Vẽ tam giác đều cạnh 4cm
- Bài 2: Vẽ hình vuông cạnh 5cm
`;

  // Xóa sạch nội dung cũ
  appState.content.objectives = "";
  appState.content.materials = "";
  appState.content.activities = { A: "", B: "", C: "", D: "", E: "", F: "", G: "" };

  console.log('-> 2. Thực thi handle1ClickGenerate()...');
  geminiCalls.length = 0;
  keyRotationLog.length = 0;
  progressHistory.length = 0;

  await handle1ClickGenerate();

  console.log('-> 3. Kiểm tra số lượng lệnh gọi AI và tiến trình tuần tự...');
  assert.strictEqual(geminiCalls.length, 6, `Phải có đúng 6 cuộc gọi AI tuần tự tương ứng 6 bước, thực tế nhận: ${geminiCalls.length}`);

  console.log('-> 4. Kiểm tra từng bước trong dây chuyền:');

  // Bước 1: GENERATE_CORE_LESSON (I + II)
  assert.ok(geminiCalls[0].prompt.includes("MỤC TIÊU") || geminiCalls[0].prompt.includes("GENERATE_CORE_LESSON"), "Bước 1 phải gọi prompt core lesson I & II");
  assert.ok(appState.content.objectives.includes("I. MỤC TIÊU"), "Mục tiêu I phải được nạp thành công");
  assert.ok(appState.content.materials.includes("II. THIẾT BỊ"), "Thiết bị II phải được nạp thành công");

  // Bước 2: GENERATE_ACTIVITY_A
  console.log("geminiCalls[1] prompt snippet:", geminiCalls[1]?.prompt?.slice(0, 150));
  console.log("appState.content.activities:", JSON.stringify(appState.content.activities));
  assert.ok(geminiCalls[1].prompt.includes("A. HOẠT ĐỘNG") || geminiCalls[1].prompt.includes("MỞ ĐẦU") || geminiCalls[1].prompt.includes("GENERATE_ACTIVITY_A"), "Bước 2 phải gọi prompt Hoạt động A");
  assert.ok(appState.content.activities.A.includes("HOẠT ĐỘNG 1: MỞ ĐẦU") || appState.content.activities.A.includes("A. HOẠT ĐỘNG"), "Hoạt động A phải được nạp vào appState");

  // Bước 3: GENERATE_ACTIVITY_B
  assert.ok(geminiCalls[2].prompt.includes("HÌNH THÀNH KIẾN THỨC"), "Bước 3 phải gọi prompt Hoạt động B");
  assert.ok(appState.content.activities.B.includes("Hoạt động 2.1: Tam giác đều"), "Hoạt động B phải bóc tách nhánh 2.1");
  assert.ok(appState.content.activities.B.includes("Hoạt động 2.2: Hình vuông"), "Hoạt động B phải bóc tách nhánh 2.2");

  // Bước 4: GENERATE_ACTIVITY_C
  assert.ok(geminiCalls[3].prompt.includes("LUYỆN TẬP"), "Bước 4 phải gọi prompt Hoạt động C");
  assert.ok(appState.content.activities.C.includes("C. HOẠT ĐỘNG 3: LUYỆN TẬP"), "Hoạt động C phải được nạp vào appState");

  // Bước 5: GENERATE_ACTIVITY_D
  assert.ok(geminiCalls[4].prompt.includes("VẬN DỤNG"), "Bước 5 phải gọi prompt Hoạt động D");
  assert.ok(appState.content.activities.D.includes("D. HOẠT ĐỘNG 4: VẬN DỤNG"), "Hoạt động D phải được nạp vào appState");

  // Bước 6: GENERATE_ACTIVITY_E
  assert.ok(geminiCalls[5].prompt.includes("HƯỚNG DẪN VỀ NHÀ"), "Bước 6 phải gọi prompt Hoạt động E");
  assert.ok(appState.content.activities.E.includes("E. HOẠT ĐỘNG 5: HƯỚNG DẪN VỀ NHÀ"), "Hoạt động E phải được nạp vào appState");

  console.log('-> 5. Kiểm tra cơ chế xoay vòng Key (Key Rotation)...');
  assert.strictEqual(keyRotationLog.length, 5, `Phải có đúng 5 lần xoay key giữa 6 bước, thực tế nhận: ${keyRotationLog.length}`);
  assert.strictEqual(keyRotationLog[0].reason, "Xoay key sau Bước 1");
  assert.strictEqual(keyRotationLog[1].reason, "Xoay key sau Bước 2");
  assert.strictEqual(keyRotationLog[2].reason, "Xoay key sau Bước 3");
  assert.strictEqual(keyRotationLog[3].reason, "Xoay key sau Bước 4");
  assert.strictEqual(keyRotationLog[4].reason, "Xoay key sau Bước 5");

  console.log('-> 6. Kiểm tra các mốc phần trăm thanh tiến trình...');
  console.log('progressHistory:', JSON.stringify(progressHistory));
  const percentages = progressHistory.map(p => p.pct);
  assert.ok(percentages.includes(15), "Tiến trình phải qua mốc 15% ở Bước 1");
  assert.ok(percentages.includes(30), "Tiến trình phải qua mốc 30% ở Bước 2");
  assert.ok(percentages.includes(50), "Tiến trình phải qua mốc 50% ở Bước 3");
  assert.ok(percentages.includes(68), "Tiến trình phải qua mốc 68% ở Bước 4");
  assert.ok(percentages.includes(84), "Tiến trình phải qua mốc 84% ở Bước 5");
  assert.ok(percentages.includes(95), "Tiến trình phải qua mốc 95% ở Bước 6");
  assert.ok(percentages.includes(100), "Tiến trình phải kết thúc ở 100%");

  console.log('-> 7. Kiểm tra đồng bộ vào các ô soạn thảo DOM...');
  assert.strictEqual(dom.elementsById.editorObjectives.value, appState.content.objectives, "editorObjectives phải đồng bộ");
  assert.strictEqual(dom.elementsById.editorMaterials.value, appState.content.materials, "editorMaterials phải đồng bộ");
  assert.strictEqual(dom.elementsById.editorActivity.value, appState.content.activities.A, "editorActivity phải đồng bộ");

  console.log('\n================================================================');
  console.log('🎉 TẤT CẢ CÁC BƯỚC KIỂM THỬ DÂY CHUYỀN TUẦN TỰ 6 BƯỚC ĐÃ PASS 100%!');
  console.log('================================================================\n');
}

run1ClickChainSmokeTest().catch(err => {
  console.error('❌ KIỂM THỬ THẤT BẠI:', err);
  process.exit(1);
});
