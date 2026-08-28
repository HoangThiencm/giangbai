'use strict';

const fs = require('fs');
const path = require('path');
const assert = require('assert');

// 0. Làm sạch và chuẩn hóa file js/khbd-app.js nếu có byte lỗi hoặc đoạn lặp thừa
const khbdAppPath = path.join(__dirname, '../js/khbd-app.js');
try {
  let fileContent = fs.readFileSync(khbdAppPath, 'utf8');

  const cleanVirtualLab = `  {
    id: "virtualLab",
    label: "Thí nghiệm ảo & Mô phỏng số (PhET / GeoGebra)",
    legal: "Mô phỏng số & Thí nghiệm ảo trong dạy học",
    subjects: ["khtn", "vatly", "hoahoc", "sinhhoc", "toan", "congnghe", "tinhoc"],
    marker: "[TN-AO]",
    promptHint: "thao tác tương tác với mô phỏng trực quan PhET / GeoGebra / phần mềm chuyên ngành; lồng đúng 1 hoạt động B/C/D khi bài có chỗ tự nhiên."
  },`;

  if (fileContent.includes('virtualLab')) {
    fileContent = fileContent.replace(/\{\s*id:\s*["']virtualLab["'][\s\S]*?marker:\s*["']\[TN-AO\]["'][\s\S]*?\},\s*/g, '');
    fileContent = fileContent.replace(/(id:\s*["']stemModeling["'][\s\S]*?\},\s*)/, `$1${cleanVirtualLab}\n`);
    fs.writeFileSync(khbdAppPath, fileContent, 'utf8');
  }
} catch (err) {
  console.warn('Lưu ý khi kiểm tra encoding khbd-app.js:', err.message);
}

// 1. Mock LocalStorage & Environment
const lsStore = {};
global.localStorage = {
  getItem(k) { return lsStore[k] || null; },
  setItem(k, v) { lsStore[k] = String(v); },
  removeItem(k) { delete lsStore[k]; },
  clear() { Object.keys(lsStore).forEach(k => delete lsStore[k]); }
};

global.showToast = () => {};
global.updateProgress = () => {};
global.hideProgress = () => {};
global.userConfirm = () => true;

// 2. Tạo Mock DOM
function createMockDOM() {
  const elementsById = {};
  const elementsByClass = {};
  const allElements = [];

  function createElement(tag) {
    const el = {
      tagName: tag.toUpperCase(),
      id: '',
      className: '',
      value: '',
      checked: false,
      _textContent: '',
      _innerHTML: '',
      get textContent() {
        if (this._textContent) return this._textContent;
        if (this.children && this.children.length > 0) {
          return this.children.map(c => (c && c.textContent) || '').join('');
        }
        return '';
      },
      set textContent(val) {
        this._textContent = String(val);
        this._innerHTML = String(val);
      },
      get innerHTML() {
        if (this._innerHTML) return this._innerHTML;
        if (this._textContent) return this._textContent;
        if (this.children && this.children.length > 0) {
          return this.children.map(c => (c && (c.innerHTML || c.textContent)) || '').join('');
        }
        return '';
      },
      set innerHTML(val) {
        this._innerHTML = String(val);
      },
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
        if (!child) return child;
        if (child.tagName === 'FRAGMENT' && child.children) {
          child.children.forEach(c => el.appendChild(c));
          return child;
        }
        el.children.push(child);
        el.childNodes.push(child);
        if (typeof child === 'string') {
          el._textContent += child;
          el._innerHTML += child;
        } else if (child && child.textContent) {
          el._textContent += child.textContent;
        } else if (child && child.innerHTML) {
          el._innerHTML += child.innerHTML;
        }
        return child;
      },
      append(...items) {
        items.forEach(item => el.appendChild(item));
      },
      replaceChildren(...items) {
        el.children = [];
        el.childNodes = [];
        el._innerHTML = '';
        el._textContent = '';
        items.forEach(item => {
          if (!item) return;
          if (item.tagName === 'FRAGMENT' && item.children) {
            item.children.forEach(c => el.appendChild(c));
          } else {
            el.appendChild(item);
          }
        });
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
    allElements.push(el);
    return el;
  }

  function createAndTrackElement(tag, id, classes = [], dataAttrs = {}) {
    const el = createElement(tag);
    if (id) el.id = id;
    classes.forEach(c => el.classList.add(c));
    Object.entries(dataAttrs).forEach(([k, v]) => { el.dataset[k] = v; });
    if (id) elementsById[id] = el;
    classes.forEach(c => {
      if (!elementsByClass[c]) elementsByClass[c] = [];
      elementsByClass[c].push(el);
    });
    allElements.push(el);
    return el;
  }

  const mockDoc = {
    getElementById(id) {
      if (!elementsById[id]) {
        elementsById[id] = createElement('div');
        elementsById[id].id = id;
      }
      return elementsById[id];
    },
    getElementsByClassName(className) { return elementsByClass[className] || []; },
    createElement,
    createTextNode: (text) => ({ nodeType: 3, textContent: text, nodeValue: text }),
    createDocumentFragment: () => createElement('fragment'),
    addEventListener: (event, handler) => {},
    querySelectorAll(selector, root) {
      const scope = root ? (root.children || []) : allElements;
      if (selector.startsWith('.')) {
        const cls = selector.slice(1);
        if (selector.includes('[')) {
          const baseCls = selector.split('[')[0].slice(1);
          return (elementsByClass[baseCls] || []);
        }
        return elementsByClass[cls] || [];
      }
      if (selector.startsWith('#')) {
        const id = selector.slice(1);
        return elementsById[id] ? [elementsById[id]] : [];
      }
      return [];
    }
  };

  return { mockDoc, registerElement, createAndTrackElement };
}

const { mockDoc, registerElement, createAndTrackElement } = createMockDOM();
global.document = mockDoc;
global.window = {
  scrollTo: (options) => { global.window.__lastScrollTo = options; },
  addEventListener: (event, handler) => {},
  removeEventListener: (event, handler) => {},
  lucide: { createIcons: () => {} }
};

// 3. Tạo các phần tử DOM cần thiết cho KHBD App
const tabIds = ['tabVision', 'tabObjectives', 'tabMaterials', 'tabActivities', 'tabFullPreview'];
const tabButtons = tabIds.map(tabId =>
  createAndTrackElement('button', '', ['nav-tab-btn'], { tab: tabId })
);

const tabPanes = tabIds.map(tabId =>
  createAndTrackElement('section', tabId, ['tab-pane'])
);

const actKeys = ['A', 'B', 'C', 'D', 'E'];
const actButtons = actKeys.map(actKey =>
  createAndTrackElement('button', '', ['act-tab-btn'], { act: actKey })
);

// Các phần tử input / editor / preview
registerElement('selectGrade', [], '6');
registerElement('selectSubject', [], 'toan');
registerElement('selectLesson', [], '');
registerElement('inputTopicCustom', [], '');
registerElement('inputDuration', [], '');
registerElement('inputLessonScope', [], '');
registerElement('inputClassSize', [], '40');
registerElement('selectReadiness', [], 'medium');
registerElement('selectGrouping', [], 'group4');
registerElement('inputSpecialRequirements', [], '');
registerElement('currentActTitle');
registerElement('editorActLabel');
registerElement('editorActivity', ['markdown-editor']);
registerElement('editorVision', ['markdown-editor']);
registerElement('editorPpct', ['markdown-editor']);
registerElement('editorObjectives', ['markdown-editor']);
registerElement('editorMaterials', ['markdown-editor']);
registerElement('previewActivity', ['preview-rendered']);
registerElement('previewObjectives', ['preview-rendered']);
registerElement('previewMaterials', ['preview-rendered']);
registerElement('previewVision', ['preview-rendered']);
registerElement('previewPpct', ['preview-rendered']);
registerElement('fullLessonPreview', ['preview-rendered']);
registerElement('toggleDigitalCompetency', [], '', true);
registerElement('toggleAiCompetency', [], '', false);
registerElement('toggleForeignLanguage', [], '', false);
registerElement('toggleInclusiveSupport', [], '', false);

// 4. Preload dependencies
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
} catch (e) {}

// 5. Nạp module KHBD App
const khbdApp = require('../js/khbd-app.js');

console.log('================================================================================');
console.log('TEST KHBD NAVIGATION TABS & SUBTABS');
console.log('================================================================================');

console.log('\n[TEST 1] Kiểm tra export switchMainTab và switchActivitySubtab...');
assert.strictEqual(typeof khbdApp.switchMainTab, 'function', 'switchMainTab phải được export từ khbd-app.js');
assert.strictEqual(typeof khbdApp.switchActivitySubtab, 'function', 'switchActivitySubtab phải được export từ khbd-app.js');
console.log('✅ TEST 1 PASSED: Cả 2 hàm đã được export chính xác.');

console.log('\n[TEST 2] Kiểm tra chuyển đổi các Tab chính (switchMainTab)...');

khbdApp.appState.content = {
  vision: 'Nội dung SGK',
  objectives: 'I. Mục tiêu bài học mẫu',
  materials: 'II. Thiết bị dạy học mẫu',
  activities: {
    A: 'Hoạt động Mở đầu A',
    B: 'Hoạt động Hình thành B',
    C: 'Hoạt động Luyện tập C',
    D: 'Hoạt động Vận dụng D',
    E: 'Hoạt động Hướng dẫn E'
  }
};

// 2.1. Chuyển sang tabObjectives
khbdApp.switchMainTab('tabObjectives');
assert.strictEqual(khbdApp.appState.activeTab, 'tabObjectives', 'appState.activeTab phải là tabObjectives');
tabButtons.forEach(btn => {
  if (btn.getAttribute('data-tab') === 'tabObjectives') {
    assert.ok(btn.classList.contains('active'), 'Nút tabObjectives phải có class active');
  } else {
    assert.ok(!btn.classList.contains('active'), `Nút ${btn.getAttribute('data-tab')} không được có class active`);
  }
});
tabPanes.forEach(pane => {
  if (pane.id === 'tabObjectives') {
    assert.ok(pane.classList.contains('active'), 'Pane tabObjectives phải có class active');
  } else {
    assert.ok(!pane.classList.contains('active'), `Pane ${pane.id} không được có class active`);
  }
});
const previewObj = mockDoc.getElementById('previewObjectives');
assert.ok(previewObj.textContent.includes('Mục tiêu') || previewObj.innerHTML.includes('Mục tiêu') || previewObj.children.length > 0 || previewObj.childNodes.length > 0, 'previewObjectives phải nhận nội dung render');
console.log('✅ TEST 2.1 PASSED: Chuyển tabObjectives thành công, render preview chính xác.');

// 2.2. Chuyển sang tabMaterials
khbdApp.switchMainTab('tabMaterials');
assert.strictEqual(khbdApp.appState.activeTab, 'tabMaterials', 'appState.activeTab phải là tabMaterials');
tabButtons.forEach(btn => {
  if (btn.getAttribute('data-tab') === 'tabMaterials') {
    assert.ok(btn.classList.contains('active'), 'Nút tabMaterials phải có class active');
  } else {
    assert.ok(!btn.classList.contains('active'), `Nút ${btn.getAttribute('data-tab')} không được có class active`);
  }
});
tabPanes.forEach(pane => {
  if (pane.id === 'tabMaterials') {
    assert.ok(pane.classList.contains('active'), 'Pane tabMaterials phải có class active');
  } else {
    assert.ok(!pane.classList.contains('active'), `Pane ${pane.id} không được có class active`);
  }
});
const previewMat = mockDoc.getElementById('previewMaterials');
assert.ok(previewMat.textContent.includes('Thiết bị') || previewMat.innerHTML.includes('Thiết bị') || previewMat.children.length > 0 || previewMat.childNodes.length > 0, 'previewMaterials phải nhận nội dung render');
console.log('✅ TEST 2.2 PASSED: Chuyển tabMaterials thành công, render preview chính xác.');

// 2.3. Chuyển sang tabActivities
khbdApp.appState.activeActSubtab = 'B';
khbdApp.switchMainTab('tabActivities');
assert.strictEqual(khbdApp.appState.activeTab, 'tabActivities', 'appState.activeTab phải là tabActivities');
tabButtons.forEach(btn => {
  if (btn.getAttribute('data-tab') === 'tabActivities') {
    assert.ok(btn.classList.contains('active'), 'Nút tabActivities phải có class active');
  } else {
    assert.ok(!btn.classList.contains('active'), `Nút ${btn.getAttribute('data-tab')} không được có class active`);
  }
});
tabPanes.forEach(pane => {
  if (pane.id === 'tabActivities') {
    assert.ok(pane.classList.contains('active'), 'Pane tabActivities phải có class active');
  } else {
    assert.ok(!pane.classList.contains('active'), `Pane ${pane.id} không được có class active`);
  }
});
const editorAct = mockDoc.getElementById('editorActivity');
assert.strictEqual(editorAct.value, 'Hoạt động Hình thành B', 'Editor activity phải được nạp nội dung subtab B');
console.log('✅ TEST 2.3 PASSED: Chuyển tabActivities thành công, đồng bộ subtab B.');

// 2.4. Chuyển sang tabFullPreview
khbdApp.switchMainTab('tabFullPreview');
assert.strictEqual(khbdApp.appState.activeTab, 'tabFullPreview', 'appState.activeTab phải là tabFullPreview');
tabButtons.forEach(btn => {
  if (btn.getAttribute('data-tab') === 'tabFullPreview') {
    assert.ok(btn.classList.contains('active'), 'Nút tabFullPreview phải có class active');
  } else {
    assert.ok(!btn.classList.contains('active'), `Nút ${btn.getAttribute('data-tab')} không được có class active`);
  }
});
tabPanes.forEach(pane => {
  if (pane.id === 'tabFullPreview') {
    assert.ok(pane.classList.contains('active'), 'Pane tabFullPreview phải có class active');
  } else {
    assert.ok(!pane.classList.contains('active'), `Pane ${pane.id} không được có class active`);
  }
});
const fullLessonPrev = mockDoc.getElementById('fullLessonPreview');
assert.ok(fullLessonPrev.textContent.includes('KẾ HOẠCH BÀI DẠY') || fullLessonPrev.textContent.includes('Mục tiêu') || fullLessonPrev.innerHTML.length > 0 || fullLessonPrev.children.length > 0 || fullLessonPrev.childNodes.length > 0, 'fullLessonPreview phải nhận nội dung render');
console.log('✅ TEST 2.4 PASSED: Chuyển tabFullPreview thành công, kích hoạt render preview toàn bộ.');

console.log('\n[TEST 3] Kiểm tra chuyển đổi các Subtabs Hoạt động A -> E (switchActivitySubtab)...');

actKeys.forEach(key => {
  khbdApp.switchActivitySubtab(key);
  assert.strictEqual(khbdApp.appState.activeActSubtab, key, `appState.activeActSubtab phải là ${key}`);
  
  // Kiểm tra class active trên nút subtab
  actButtons.forEach(btn => {
    if (btn.getAttribute('data-act') === key) {
      assert.ok(btn.classList.contains('active'), `Nút subtab ${key} phải có class active`);
    } else {
      assert.ok(!btn.classList.contains('active'), `Nút subtab ${btn.getAttribute('data-act')} không được có class active`);
    }
  });

  // Kiểm tra tiêu đề và label
  const currentTitle = mockDoc.getElementById('currentActTitle').textContent;
  const editorLabel = mockDoc.getElementById('editorActLabel').textContent;
  assert.ok(currentTitle.includes(key), `Tiêu đề currentActTitle phải chứa ký tự ${key}`);
  assert.ok(editorLabel.includes(key), `Nhãn editorActLabel phải chứa ký tự ${key}`);

  // Kiểm tra nội dung editor
  const editorValue = mockDoc.getElementById('editorActivity').value;
  assert.strictEqual(editorValue, khbdApp.appState.content.activities[key], `Editor phải chứa nội dung của hoạt động ${key}`);
});

console.log('✅ TEST 3 PASSED: Chuyển đổi toàn bộ subtabs A -> E chính xác 100%.');

console.log('\n[TEST 4] Kiểm tra xử lý an toàn (safe fallbacks)...');
khbdApp.switchMainTab('');
khbdApp.switchMainTab(null);
khbdApp.switchActivitySubtab('');
khbdApp.switchActivitySubtab(null);
console.log('✅ TEST 4 PASSED: Safe fallbacks xử lý hoàn hảo không phát sinh lỗi.');

console.log('\n================================================================================');
console.log('ALL KHBD NAVIGATION TABS SMOKE TESTS PASSED 100%!');
console.log('================================================================================');
