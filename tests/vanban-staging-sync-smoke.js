const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const { spawnSync } = require('node:child_process');

const root = path.join(__dirname, '..');
const read = name => fs.readFileSync(path.join(root, name), 'utf8');
const app = read('vanban-app.js');
const phpSource = read('api/vanban.php');

assert.match(phpSource, /function vbd_staging_dir\(/);
assert.match(phpSource, /function vbd_store_staging_upload\(/);
assert.match(phpSource, /function vbd_clean_orphan_staging\(/);
assert.match(phpSource, /action === 'save_upload_stage'/);
assert.match(phpSource, /action === 'sync_drive_file'/);
assert.match(phpSource, /drive_upload_file\(/);
assert.match(phpSource, /@unlink\(\$path\)/);
assert.match(app, /save_upload_stage/);
assert.match(app, /Đang lưu văn bản và tệp\.\.\./);
assert.match(app, /Đang đồng bộ \$\{name\} lên Google Drive\.\.\./);
assert.match(app, /fa-brands fa-google-drive/);
assert.doesNotMatch(app.slice(app.indexOf('async function saveDocument')), /uploadFileViaChunks\(/);

const elements = {};
function makeEl(id) {
    return {
        id,
        value: '',
        innerHTML: '',
        textContent: '',
        className: '',
        classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
        dataset: {},
        style: {},
        addEventListener() {},
        querySelector() { return null; },
        querySelectorAll() { return []; },
        appendChild() {},
        insertBefore() {},
        classListHidden: false,
    };
}

const documentMock = {
    readyState: 'loading',
    body: { classList: { add() {}, remove() {} }, appendChild() {} },
    addEventListener() {},
    createElement() { return makeEl('created'); },
    getElementById(id) { return elements[id] || null; },
};

const context = vm.createContext({
    window: { VANBAN_SECTOR: 'hanhchinh' },
    document: documentMock,
    localStorage: { getItem() { return null; }, setItem() {}, removeItem() {} },
    console,
    TextDecoder,
    TextEncoder,
    Uint8Array,
    setTimeout,
    clearTimeout,
    FormData,
    Blob,
    fetch: async () => { throw new Error('fetch chưa được gán'); },
});
context.globalThis = context;
context.window.document = documentMock;

const injected = app.replace(
    /\r?\n\}\)\(\);/,
    '\n    window.__vbdStagingTest = { state, saveDocument, splitStagingBatches, renderFileChip, syncPendingStagedFiles, driveFileId, isStagingFile };\n})();'
);
assert.notEqual(injected, app, 'không chèn được điểm kiểm thử vào vanban-app.js');
vm.runInContext(injected, context);
const api = context.window.__vbdStagingTest;
assert.equal(typeof api.splitStagingBatches, 'function');
assert.equal(typeof api.saveDocument, 'function');

const mb = 1024 * 1024;
const batches = api.splitStagingBatches([
    { name: 'a.pdf', size: 30 * mb },
    { name: 'b.pdf', size: 30 * mb },
    { name: 'c.pdf', size: 60 * mb },
    { name: 'd.pdf', size: 10 * mb },
]);
assert.equal(batches.length, 4, 'tệp vượt 50 MB phải tách đợt');
assert.equal(
    JSON.stringify(batches.map(batch => [...batch].map(file => file.name))),
    JSON.stringify([['a.pdf'], ['b.pdf'], ['c.pdf'], ['d.pdf']])
);
assert.equal(api.splitStagingBatches([{ name: 'a.pdf', size: 20 * mb }, { name: 'b.pdf', size: 20 * mb }]).length, 1);

const stagingChip = api.renderFileChip(
    { id: 1 },
    { id: 2, original_name: 'bao-cao.pdf', drive_file_id: 'staging:1:bao-cao.pdf', view_url: 'api/vanban.php?action=file&document_id=1&name=bao-cao.pdf' }
);
assert.match(stagingChip, /Đang đồng bộ Drive/);
assert.match(stagingChip, /action=file/);
assert.equal(api.driveFileId({ drive_file_id: 'staging:1:bao-cao.pdf' }), '');

const driveChip = api.renderFileChip(
    { id: 1 },
    { id: 3, original_name: 'bao-cao.pdf', drive_file_id: '1AbCDriveTestFileId', view_url: 'https://drive.google.com/file/d/1AbCDriveTestFileId/view' }
);
assert.match(driveChip, /fa-google-drive/);
assert.equal(api.driveFileId({ drive_file_id: '1AbCDriveTestFileId' }), '1AbCDriveTestFileId');

elements.uploadProgress = makeEl('uploadProgress');
elements.uploadProgressText = makeEl('uploadProgressText');
elements.uploadProgressPercent = makeEl('uploadProgressPercent');
elements.uploadProgressBar = makeEl('uploadProgressBar');

async function assertFrontendFlow() {
    const blob = new Blob(['xin chao'], { type: 'application/pdf' });
    blob.name = 'bao-cao.pdf';
    api.state.pendingUploadFiles = [blob];
    const urls = [];
    context.fetch = async (url, options) => {
        urls.push(String(url));
        assert.equal(options.method, 'POST');
        assert.ok(options.body instanceof FormData);
        return {
            ok: true,
            json: async () => ({
                ok: true,
                document: { id: 9, title: 'Van ban thu' },
                staged_files: [{
                    id: 3,
                    document_id: 9,
                    original_name: 'bao-cao.pdf',
                    drive_file_id: 'staging:9:bao-cao.pdf',
                    view_url: 'api/vanban.php?action=file&document_id=9&name=bao-cao.pdf',
                }],
            }),
        };
    };
    const saved = await api.saveDocument({ title: 'Van ban thu', academic_year: '2025-2026', report_required: false });
    assert.equal(saved.storage, 'staging');
    assert.equal(saved.message, 'Đã lưu văn bản');
    assert.equal(urls.length, 1);
    assert.match(urls[0], /action=save_upload_stage/);
    assert.equal(elements.uploadProgressText.textContent.startsWith('Đang lưu văn bản và tệp...'), true);

    api.state.documents = [{
        id: 9,
        title: 'Van ban thu',
        files: [{
            id: 3,
            document_id: 9,
            original_name: 'bao-cao.pdf',
            drive_file_id: 'staging:9:bao-cao.pdf',
            view_url: 'api/vanban.php?action=file&document_id=9&name=bao-cao.pdf',
        }],
    }];
    const syncUrls = [];
    context.fetch = async url => {
        syncUrls.push(String(url));
        return {
            ok: true,
            json: async () => ({
                ok: true,
                synced: true,
                file: {
                    id: 3,
                    document_id: 9,
                    original_name: 'bao-cao.pdf',
                    drive_file_id: '1AbCDriveTestFileId',
                    view_url: 'https://drive.google.com/file/d/1AbCDriveTestFileId/view',
                    download_url: 'https://drive.google.com/uc?export=download&id=1AbCDriveTestFileId',
                },
            }),
        };
    };
    await api.syncPendingStagedFiles(api.state.documents[0].files);
    assert.match(syncUrls[0], /action=sync_drive_file/);
    assert.equal(api.state.documents[0].files[0].drive_file_id, '1AbCDriveTestFileId');
    assert.match(api.renderFileChip(api.state.documents[0], api.state.documents[0].files[0]), /fa-google-drive/);
}

assertFrontendFlow().then(() => {
function findPhp() {
    if (process.env.PHP_BIN && fs.existsSync(process.env.PHP_BIN)) return process.env.PHP_BIN;
    const found = spawnSync('where.exe', ['php'], { encoding: 'utf8' });
    const line = String(found.stdout || '').split(/\r?\n/).map(item => item.trim()).find(Boolean);
    if (line && fs.existsSync(line)) return line;
    const candidates = [
        'C:\\xampp\\php\\php.exe',
        'C:\\php\\php.exe',
        'C:\\tools\\php\\php.exe',
    ];
    return candidates.find(candidate => fs.existsSync(candidate)) || '';
}

const phpBin = findPhp();
if (!phpBin) {
    console.error('Không tìm thấy php.exe. Đặt PHP_BIN rồi chạy lại tests/vanban-staging-sync-smoke.js');
    process.exit(1);
}

const harness = String.raw`<?php
define('VBD_SKIP_BOOT', true);
$root = $argv[1] ?? '';
$storage = $argv[2] ?? '';
if ($root === '' || $storage === '') {
    fwrite(STDERR, "Thiếu đường dẫn kiểm thử.\n");
    exit(1);
}
define('VANBAN_LOCAL_STORAGE_DIR', $storage);
require $root . '/api/vanban.php';

function fail(string $message): void {
    fwrite(STDERR, $message . "\n");
    exit(1);
}

$pdo = new PDO('sqlite:' . $storage . '/staging-smoke.sqlite');
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$pdo->exec('CREATE TABLE office_school_years (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)');
$pdo->exec('CREATE TABLE office_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER,
    academic_year TEXT,
    sector TEXT,
    direction TEXT,
    document_number TEXT,
    title TEXT,
    document_date TEXT,
    organization TEXT,
    document_type TEXT,
    summary_text TEXT,
    source_text TEXT,
    report_required INTEGER,
    report_due_at TEXT,
    report_status TEXT,
    report_note TEXT,
    reported_at TEXT,
    drive_folder_id TEXT
)');
$pdo->exec('CREATE TABLE office_document_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER,
    drive_file_id TEXT,
    original_name TEXT,
    stored_name TEXT,
    mime_type TEXT,
    size_bytes INTEGER,
    view_url TEXT,
    download_url TEXT
)');
$pdo->exec("INSERT INTO office_school_years (name) VALUES ('2025-2026')");

$user = ['id' => 1, 'role' => 'teacher', 'full_name' => 'Smoke', 'username' => 'smoke'];
$document = vbd_save_document($pdo, $user, [
    'title' => 'Van ban staging smoke',
    'academic_year' => '2025-2026',
    'sector' => 'hanhchinh',
    'direction' => 'incoming',
    'document_number' => '01/TB-SM',
    'report_required' => '0',
]);
$docId = (int)$document['id'];
if ($docId < 1) fail('Không lưu được văn bản.');

$tmp = tempnam(sys_get_temp_dir(), 'vbd');
if ($tmp === false) fail('Không tạo được tệp tạm.');
file_put_contents($tmp, "%PDF-1.4\nstaging smoke\n");
$upload = [
    'name' => 'bao-cao.pdf',
    'type' => 'application/pdf',
    'tmp_name' => $tmp,
    'error' => UPLOAD_ERR_OK,
    'size' => filesize($tmp),
];
$staged = vbd_stage_uploaded_files($pdo, $document, [$upload]);
if (count($staged) !== 1) fail('Staging không trả về đúng một tệp.');
$stagedFile = $staged[0];
$stagedPath = vbd_staging_disk_path($docId, $stagedFile['stored_name']);
if (!is_file($stagedPath) || filesize($stagedPath) < 1) fail('Tệp tạm chưa có trong staging.');
if (!str_starts_with($stagedFile['drive_file_id'], 'staging:' . $docId . ':')) fail('Marker staging không đúng.');
if (vbd_text_len($stagedFile['drive_file_id']) > 160) fail('Marker staging dài hơn VARCHAR(160).');
$longName = vbd_fit_stored_name($docId, str_repeat('A', 240) . '.pdf');
if (vbd_text_len(vbd_staging_marker($docId, $longName)) > 160) fail('Tên tệp dài không vừa cột drive_file_id.');

$pdo->prepare('UPDATE office_documents SET drive_folder_id=? WHERE id=?')->execute(['folderTest123', $docId]);
$document = vbd_document($pdo, $docId, 1, false);
$calls = 0;
$GLOBALS['vbd_drive_upload_handler'] = function (string $folderId, string $storedName, string $mime, string $path) use (&$calls, $stagedPath): array {
    $calls++;
    if ($folderId !== 'folderTest123') fail('Sync không dùng drive_folder_id đã lưu.');
    if (!is_file($path) || $path !== $stagedPath) fail('Sync không đọc đúng tệp staging.');
    return [
        'file_id' => '1AbCDriveTestFileId',
        'stored_name' => $storedName,
        'mime_type' => $mime,
        'view_url' => 'https://drive.google.com/file/d/1AbCDriveTestFileId/view',
        'download_url' => 'https://drive.google.com/uc?export=download&id=1AbCDriveTestFileId',
    ];
};

$result = vbd_sync_drive_request($pdo, $user, ['file_id' => (int)$stagedFile['id'], 'document_id' => $docId]);
if (empty($result['ok']) || empty($result['synced'])) fail('Sync không báo thành công.');
$file = $result['file'];
if (($file['drive_file_id'] ?? '') !== '1AbCDriveTestFileId') fail('MySQL chưa cập nhật ID Google Drive.');
if (!str_contains((string)($file['view_url'] ?? ''), 'https://drive.google.com/file/d/1AbCDriveTestFileId/view')) fail('Link Drive không hợp lệ.');
if (is_file($stagedPath)) fail('Tệp staging chưa bị unlink.');
$docDir = rtrim(vbd_local_storage_root(), '/\\\\') . '/staging/' . $docId;
if (is_dir($docDir)) fail('Thư mục staging của văn bản chưa được xóa.');
$bytes = 0;
$stagingRoot = rtrim(vbd_local_storage_root(), '/\\\\') . '/staging';
if (is_dir($stagingRoot)) {
    $iterator = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($stagingRoot, FilesystemIterator::SKIP_DOTS));
    foreach ($iterator as $item) {
        if ($item->isFile() && $item->getFilename() !== '.htaccess') $bytes += $item->getSize();
    }
}
if ($bytes !== 0) fail('Dung lượng staging sau sync không phải 0.');
if ($calls !== 1) fail('drive_upload_file phải được gọi đúng một lần.');

$again = vbd_sync_drive_request($pdo, $user, ['file_id' => (int)$stagedFile['id']]);
if (($again['file']['drive_file_id'] ?? '') !== '1AbCDriveTestFileId') fail('Tệp đã sync không được giữ ID Drive.');
if ($calls !== 1) fail('Tệp đã có ID Drive không được tải lên lần nữa.');

$keepDir = $stagingRoot . '/9001';
$syncedDir = $stagingRoot . '/9002';
$freshDir = $stagingRoot . '/9003';
$oldDir = $stagingRoot . '/9004';
foreach ([$keepDir, $syncedDir, $freshDir, $oldDir] as $dir) {
    if (!is_dir($dir) && !mkdir($dir, 0755, true)) fail('Không tạo được thư mục dọn rác.');
}
file_put_contents($keepDir . '/giu.txt', 'keep');
file_put_contents($syncedDir . '/da-sync.txt', 'synced');
file_put_contents($freshDir . '/moi.txt', 'fresh');
file_put_contents($oldDir . '/cu.txt', 'old');
touch($oldDir . '/cu.txt', time() - 90000);
$insert = $pdo->prepare('INSERT INTO office_document_files (document_id, drive_file_id, original_name, stored_name, mime_type, size_bytes, view_url, download_url) VALUES (?,?,?,?,?,?,?,?)');
$insert->execute([9001, 'staging:9001:giu.txt', 'giu.txt', 'giu.txt', 'text/plain', 4, '', '']);
$insert->execute([9002, '1RealDriveLeftover', 'da-sync.txt', 'da-sync.txt', 'text/plain', 6, 'https://drive.google.com/file/d/1RealDriveLeftover/view', '']);
vbd_clean_orphan_staging($pdo);
if (!is_file($keepDir . '/giu.txt')) fail('GC đã xóa tệp staging còn chờ đồng bộ.');
if (is_file($syncedDir . '/da-sync.txt')) fail('GC chưa xóa tệp đã có ID Google Drive.');
if (!is_file($freshDir . '/moi.txt')) fail('GC đã xóa tệp mồ côi chưa đủ 24 giờ.');
if (is_file($oldDir . '/cu.txt')) fail('GC chưa xóa tệp mồ côi quá 24 giờ.');
if (vbd_documents_have_drive_files([['id' => 9001]], [9001 => [['drive_file_id' => 'staging:9001:giu.txt']]])) {
    fail('Tệp staging không được tính là đã có trên Drive.');
}

echo "PASS\n";
`;

const work = fs.mkdtempSync(path.join(os.tmpdir(), 'vbd-staging-'));
const script = path.join(work, 'harness.php');
fs.writeFileSync(script, harness);
const extDir = path.join(path.dirname(phpBin), 'ext');
const args = [];
if (fs.existsSync(extDir)) {
    args.push('-d', `extension_dir=${extDir}`, '-d', 'extension=php_pdo_sqlite.dll', '-d', 'extension=php_sqlite3.dll');
}
args.push(script, root, work);
const result = spawnSync(phpBin, args, { encoding: 'utf8' });
fs.rmSync(work, { recursive: true, force: true });
if (result.status !== 0) {
    console.error(result.stdout || '');
    console.error(result.stderr || '');
    process.exit(result.status || 1);
}
if (!String(result.stdout).includes('PASS')) {
    console.error(result.stdout || '');
    console.error(result.stderr || '');
    process.exit(1);
}
console.log('PASS');
}).catch(error => {
    console.error(error);
    process.exit(1);
});
