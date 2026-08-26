'use strict';

const assert = require('assert');

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
    },
    addEventListener() {}
  };

  return { localStorageMock, mockDoc, registerElement, elementsById, elementsByClass };
}

// 2. Thiết lập môi trường toàn cục cho bài test
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

// Đăng ký các element UI cần thiết
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
  'aiStandardsPanel', 'methodsCatalogPanel', 'techniquesCatalogPanel', 'activitiesCatalogPanel'
].forEach(id => dom.registerElement(id));

// Đăng ký checkbox groups
const classProfileChoices = ['Trình độ không đồng đều', 'Cần củng cố nền tảng', 'Nhiều HS khá/giỏi', 'Cần trực quan hóa'];
classProfileChoices.forEach((choice, idx) => {
  const el = dom.registerElement(`cp_choice_${idx}`, ['class-profile-choice']);
  el.value = choice;
});

const supportChoices = ['Nhiệm vụ chia nhỏ', 'Thêm thời gian', 'Học liệu trực quan/chữ lớn'];
supportChoices.forEach((choice, idx) => {
  const el = dom.registerElement(`sp_choice_${idx}`, ['support-choice']);
  el.value = choice;
});

// Load app module sau khi globals đã sẵn sàng
const {
  appState,
  handleClearAllContent,
  syncDraftDom,
  normalizeTeachingContext
} = require('../js/khbd-app.js');

function testClearAllContent() {
  console.log('==================================================');
  console.log('BẮT ĐẦU KIỂM THỬ XÓA TẤT CẢ (CLEAR ALL SMOKE TEST)');
  console.log('==================================================');

  // 1. Giả lập người dùng đã nhập đầy đủ nội dung và thiết lập bối cảnh sư phạm
  console.log('-> 1. Nạp dữ liệu giả lập vào appState và DOM...');
  appState.selectedGrade = '7';
  appState.school = 'THCS Thực Nghiệm';
  appState.group = 'Tổ Tự Nhiên';
  appState.teacher = 'Cô Nguyễn Thị B';
  appState.subject = 'Toán';
  appState.customTopic = 'Hình lăng trụ đứng tam giác';
  appState.duration = '3 tiết';

  appState.content = {
    vision: 'Nội dung phân tích SGK về lăng trụ đứng...',
    objectives: 'Mục tiêu 1: Nắm công thức diện tích xung quanh...',
    materials: 'Mô hình lăng trụ, thước kẻ...',
    activities: {
      A: 'Hoạt động mở đầu quan sát khối hộp...',
      B: 'Hoạt động hình thành kiến thức tính thể tích...',
      C: 'Luyện tập bài 1, 2 SGK...',
      D: 'Vận dụng tính thể tích hộp sữa...',
      E: 'Mở rộng 1',
      F: 'Mở rộng 2',
      G: 'Mở rộng 3'
    }
  };

  appState.images = [
    { id: 'img_1', name: 'Trang 1.jpg', size: 1024, dataUrl: 'data:image/jpeg;base64,aaa' },
    { id: 'img_2', name: 'Trang 2.jpg', size: 2048, dataUrl: 'data:image/jpeg;base64,bbb' }
  ];

  appState.teachingContext = {
    classProfileChoices: ['Trình độ không đồng đều', 'Cần trực quan hóa'],
    classProfileNote: 'Lớp 7A1 học buổi sáng',
    supportChoices: ['Nhiệm vụ chia nhỏ', 'Thêm thời gian'],
    supportNote: 'HS Nam cần hỗ trợ đọc',
    integrations: {
      digital: true,
      ai: true,
      foreignLanguage: true,
      inclusive: true
    },
    methods: ['pp-day-hoc-hop-tac'],
    techniques: ['kt-chia-se-nhom-doi'],
    subjectActivities: ['hd-thuc-hanh-do-dac'],
    standards: [
      { framework: 'Khung năng lực số (TT 02/2025)', catalogId: 'dig_1', officialLabel: '1. Sử dụng thiết bị' },
      { framework: 'Khung năng lực AI (QĐ 2422)', catalogId: 'ai_1', officialCode: '1.AI.1', officialLabel: 'Nhận biết AI' }
    ],
    phasePedagogy: { A: { techniques: ['kt-chia-se-nhom-doi'] }, B: {}, C: {}, D: {} },
    classSize: 45,
    readiness: 'Nâng cao',
    grouping: 'Nhóm 4 có phân vai',
    facilities: { projector: true, internet: true, devices: true },
    specialRequirements: 'Thực hành mô hình 3D'
  };

  // Đồng bộ lên DOM để giả lập trạng thái đang hiển thị
  syncDraftDom();
  dom.elementsById.fileInputImages.value = 'C:\\fakepath\\sgk.pdf';
  dom.elementsById.digitalStandardsPanel.innerHTML = '<p>Đang hiển thị chuẩn NLS</p>';
  dom.elementsById.aiStandardsPanel.innerHTML = '<p>Đang hiển thị chuẩn AI</p>';

  // Kiểm tra trước khi xóa: DOM và state đều có dữ liệu
  assert.strictEqual(dom.elementsById.editorVision.value, 'Nội dung phân tích SGK về lăng trụ đứng...');
  assert.strictEqual(dom.elementsById.inputClassProfileNote.value, 'Lớp 7A1 học buổi sáng');
  assert.strictEqual(dom.elementsById.hasProjector.checked, true);
  assert.strictEqual(dom.elementsById.toggleDigitalCompetency.checked, true);
  assert.strictEqual(dom.elementsById.toggleAiCompetency.checked, true);
  assert.strictEqual(dom.elementsById.toggleForeignLanguage.checked, true);
  assert.strictEqual(dom.elementsById.toggleInclusiveSupport.checked, true);
  console.log('  -> Trạng thái trước khi xóa: ĐÃ NẠP ĐẦY ĐỦ DỮ LIỆU.');

  // 2. Thử nghiệm khi người dùng HUỶ (Cancel confirm)
  console.log('-> 2. Thử nghiệm khi người dùng Cancel hộp thoại confirm...');
  global.confirm = () => false;
  handleClearAllContent();
  assert.strictEqual(appState.content.vision, 'Nội dung phân tích SGK về lăng trụ đứng...', 'Dữ liệu không được xóa khi Cancel');
  assert.strictEqual(appState.images.length, 2, 'Ảnh không được xóa khi Cancel');
  assert.strictEqual(appState.teachingContext.integrations.digital, true, 'Bối cảnh không được xóa khi Cancel');
  console.log('  -> Khi Cancel confirm: Dữ liệu được bảo toàn an toàn (PASS)');

  // 3. Thử nghiệm khi người dùng ĐỒNG Ý XÓA (Confirm = true)
  console.log('-> 3. Thực hiện XÓA TẤT CẢ khi Confirm = true...');
  global.confirm = () => true;
  handleClearAllContent();

  // 3.1. Kiểm tra State nội dung bài soạn
  console.log('  -> Kiểm tra appState.content...');
  assert.strictEqual(appState.content.vision, '', 'Vision phải rỗng');
  assert.strictEqual(appState.content.objectives, '', 'Objectives phải rỗng');
  assert.strictEqual(appState.content.materials, '', 'Materials phải rỗng');
  ['A', 'B', 'C', 'D', 'E', 'F', 'G'].forEach(k => {
    assert.strictEqual(appState.content.activities[k], '', `Activity ${k} phải rỗng`);
  });

  // 3.2. Kiểm tra State ảnh SGK
  console.log('  -> Kiểm tra appState.images...');
  assert.deepStrictEqual(appState.images, [], 'Danh sách ảnh SGK phải là mảng rỗng []');

  // 3.3. Kiểm tra State bối cảnh sư phạm (Teaching Context)
  console.log('  -> Kiểm tra appState.teachingContext...');
  assert.deepStrictEqual(appState.teachingContext.classProfileChoices, []);
  assert.strictEqual(appState.teachingContext.classProfileNote, '');
  assert.deepStrictEqual(appState.teachingContext.supportChoices, []);
  assert.strictEqual(appState.teachingContext.supportNote, '');
  assert.deepStrictEqual(appState.teachingContext.integrations, {
    digital: false,
    ai: false,
    foreignLanguage: false,
    inclusive: false
  }, '4 Tích hợp phải đều là false');
  assert.deepStrictEqual(appState.teachingContext.methods, []);
  assert.deepStrictEqual(appState.teachingContext.techniques, []);
  assert.deepStrictEqual(appState.teachingContext.subjectActivities, []);
  assert.deepStrictEqual(appState.teachingContext.standards, []);
  assert.strictEqual(appState.teachingContext.specialRequirements, '');
  assert.deepStrictEqual(appState.teachingContext.facilities, {
    projector: false,
    internet: false,
    devices: false
  });

  // 3.4. Kiểm tra DOM Inputs & Textareas
  console.log('  -> Kiểm tra đồng bộ các Editor textareas trên DOM...');
  assert.strictEqual(dom.elementsById.editorVision.value, '');
  assert.strictEqual(dom.elementsById.editorObjectives.value, '');
  assert.strictEqual(dom.elementsById.editorMaterials.value, '');
  assert.strictEqual(dom.elementsById.editorActivity.value, '');

  console.log('  -> Kiểm tra đồng bộ ghi chú bối cảnh trên DOM...');
  assert.strictEqual(dom.elementsById.inputClassProfileNote.value, '');
  assert.strictEqual(dom.elementsById.inputSupportNote.value, '');
  assert.strictEqual(dom.elementsById.inputSpecialRequirements.value, '');

  // 3.5. Kiểm tra DOM Checkboxes & Switches
  console.log('  -> Kiểm tra đồng bộ các Checkboxes trên DOM...');
  assert.strictEqual(dom.elementsById.hasProjector.checked, false);
  assert.strictEqual(dom.elementsById.hasInternet.checked, false);
  assert.strictEqual(dom.elementsById.hasDevices.checked, false);
  assert.strictEqual(dom.elementsById.toggleDigitalCompetency.checked, false);
  assert.strictEqual(dom.elementsById.toggleAiCompetency.checked, false);
  assert.strictEqual(dom.elementsById.toggleForeignLanguage.checked, false);
  assert.strictEqual(dom.elementsById.toggleInclusiveSupport.checked, false);

  (dom.elementsByClass['class-profile-choice'] || []).forEach(input => {
    assert.strictEqual(input.checked, false, `Checkbox đặc điểm lớp ${input.value} phải unchecked`);
  });
  (dom.elementsByClass['support-choice'] || []).forEach(input => {
    assert.strictEqual(input.checked, false, `Checkbox hỗ trợ chức năng ${input.value} phải unchecked`);
  });

  // 3.6. Kiểm tra Panels Chuẩn NLS/AI
  console.log('  -> Kiểm tra dọn sạch panel NLS & AI...');
  assert.strictEqual(dom.elementsById.digitalStandardsPanel.hidden, true);
  assert.strictEqual(dom.elementsById.digitalStandardsPanel.innerHTML, '');
  assert.strictEqual(dom.elementsById.aiStandardsPanel.hidden, true);
  assert.strictEqual(dom.elementsById.aiStandardsPanel.innerHTML, '');

  // 3.7. Kiểm tra file input
  console.log('  -> Kiểm tra fileInputImages...');
  assert.strictEqual(dom.elementsById.fileInputImages.value, '');

  // 3.8. Kiểm tra Badge đếm ảnh
  assert.strictEqual(dom.elementsById.imgCountBadge.textContent, '0 ảnh');

  // 3.9. Kiểm tra lưu vào LocalStorage
  console.log('  -> Kiểm tra lưu trữ sạch vào LocalStorage...');
  const activeDraftId = dom.localStorageMock.getItem('khbd_drafts_v2:anonymous:active');
  assert.ok(activeDraftId, 'Phải có active draft key');
  const savedJson = dom.localStorageMock.getItem(`khbd_drafts_v2:anonymous:${activeDraftId}`);
  assert.ok(savedJson, 'Bản nháp đã lưu trong LocalStorage phải tồn tại');
  const savedState = JSON.parse(savedJson);
  assert.strictEqual(savedState.content.vision, '');
  assert.strictEqual(savedState.content.objectives, '');
  assert.strictEqual(savedState.teachingContext.integrations.digital, false);
  assert.strictEqual(savedState.teachingContext.integrations.ai, false);
  assert.deepStrictEqual(savedState.teachingContext.standards, []);

  console.log('==================================================');
  console.log('TẤT CẢ KIỂM THỬ XÓA TẤT CẢ ĐỀU ĐẠT CHUẨN XÁC 100% (PASS)!');
  console.log('==================================================');
}

testClearAllContent();
