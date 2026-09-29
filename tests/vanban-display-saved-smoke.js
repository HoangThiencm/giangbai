const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const vm = require('node:vm');

const root = path.join(__dirname, '..');
const read = name => fs.readFileSync(path.join(root, name), 'utf8');
const app = read('vanban-app.js');
const php = read('api/vanban.php');

const elements = {};
function makeEl(id) {
    return {
        id,
        value: '',
        innerHTML: '',
        textContent: '',
        className: '',
        classList: { add() {}, remove() {}, toggle() {} },
        dataset: {},
        style: {},
        addEventListener() {},
        querySelector() { return null; },
        querySelectorAll() { return []; },
    };
}

const documentMock = {
    readyState: 'loading',
    body: { classList: { add() {}, remove() {} } },
    addEventListener() {},
    createElement() { return makeEl('created'); },
    getElementById(id) { return elements[id] || null; },
};

const context = vm.createContext({
    window: { VANBAN_SECTOR: 'hanhchinh' },
    document: documentMock,
    localStorage: {
        getItem() { return null; },
        setItem() {},
        removeItem() {},
    },
    console,
    TextDecoder,
    TextEncoder,
    Uint8Array,
    setTimeout,
    clearTimeout,
});
context.globalThis = context;
context.window.document = documentMock;

const injected = app.replace(
    /\r?\n\}\)\(\);/,
    '\n    window.__vbdDisplayTest = { state, renderYears, scopedDocs };\n})();'
);
assert.notEqual(injected, app, 'không chèn được điểm kiểm thử vào vanban-app.js');
vm.runInContext(injected, context);

const api = context.window.__vbdDisplayTest;
assert.equal(typeof api.renderYears, 'function');
assert.equal(typeof api.scopedDocs, 'function');

elements.academicYearFilter = makeEl('academicYearFilter');
elements.academicYear = makeEl('academicYear');
elements.searchInput = makeEl('searchInput');
elements.statusFilter = makeEl('statusFilter');
elements.typeFilter = makeEl('typeFilter');

api.state.schoolYears = ['2025-2026', '2024-2025'];
api.state.selectedYear = '';
api.state.yearInitialized = false;
elements.academicYear.value = '';
api.renderYears();
assert.equal(api.state.selectedYear, '', 'bộ lọc năm học mặc định phải là Tất cả năm học');
assert.equal(elements.academicYearFilter.value, '');
assert.match(elements.academicYearFilter.innerHTML, /<option value="">Tất cả năm học<\/option>/);
assert.match(elements.academicYearFilter.innerHTML, /<option value="__empty__">Chưa gán năm học<\/option>/);
assert.equal(elements.academicYear.value, '2025-2026');

api.state.documents = [
    { id: 1, academic_year: '2025-2026', direction: 'incoming', title: 'Mới', document_number: '', organization: '', summary_text: '', document_type: '' },
    { id: 2, academic_year: '', direction: 'outgoing', title: 'Đi chưa năm', document_number: '', organization: '', summary_text: '', document_type: '' },
    { id: 3, academic_year: null, direction: '', title: 'Cũ direction rỗng', document_number: '', organization: '', summary_text: '', document_type: '' },
    { id: 4, academic_year: '2024-2025', direction: null, title: 'Cũ direction null', document_number: '', organization: '', summary_text: '', document_type: '' },
];
api.state.summaryDrilldown = null;
api.state.typeFilter = '';
elements.academicYearFilter.value = '';
elements.searchInput.value = '';
elements.statusFilter.value = '';
elements.typeFilter.value = '';
api.state.selectedYear = '';
api.state.activeDirection = 'incoming';

const visible = api.scopedDocs().map(doc => doc.id).sort((a, b) => a - b);
assert.deepEqual(visible, [1, 3, 4], 'Tất cả năm học phải giữ văn bản mọi năm và direction trống trên tab đến');

elements.academicYearFilter.value = '__empty__';
api.state.activeDirection = '';
const unassigned = api.scopedDocs().map(doc => doc.id).sort((a, b) => a - b);
assert.deepEqual(unassigned, [2, 3], 'Chưa gán năm học chỉ trả văn bản không có academic_year');

api.state.activeDirection = 'incoming';
const unassignedIncoming = api.scopedDocs().map(doc => doc.id);
assert.deepEqual(unassignedIncoming, [3], 'direction rỗng vẫn nằm ở tab văn bản đến');

assert.match(php, /'20260929-v2'/);
assert.match(php, /\(sector = 'hanhchinh' OR sector IS NULL OR sector = ''\)/);
assert.match(php, /in_array\(\$userRole, \['admin', 'superadmin'\], true\)/);
assert.match(php, /owner_id = 0 OR owner_id IS NULL/);

console.log('PASS: hiển thị văn bản đã lưu, bộ lọc năm học và truy vấn legacy.');
