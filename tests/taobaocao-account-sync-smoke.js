'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'backupcode viettailieu', 'taobaocao.html'), 'utf8');
const php = fs.readFileSync(path.join(root, 'api', 'user_phuluc_draft.php'), 'utf8');
const globalConfig = JSON.parse(fs.readFileSync(path.join(root, 'global_config.json'), 'utf8'));

const DEFAULT_HOSTING_ENDPOINT = 'https://hoangthiencm.id.vn/api/user_phuluc_draft.php';
const REVOKED_PAT = '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';

function extractNamed(source, name) {
    const needles = [`async function ${name}(`, `function ${name}(`];
    let start = -1;
    for (const needle of needles) {
        start = source.indexOf(needle);
        if (start >= 0) break;
    }
    assert(start >= 0, `missing function ${name}`);
    const paren = source.indexOf('(', start);
    assert(paren >= 0, `missing parameter list for ${name}`);
    let parenDepth = 0;
    let afterParams = -1;
    for (let i = paren; i < source.length; i++) {
        if (source[i] === '(') parenDepth += 1;
        else if (source[i] === ')') {
            parenDepth -= 1;
            if (parenDepth === 0) {
                afterParams = i;
                break;
            }
        }
    }
    assert(afterParams >= 0, `unterminated parameter list for ${name}`);
    const brace = source.indexOf('{', afterParams);
    assert(brace >= 0, `missing body for ${name}`);
    let depth = 0;
    for (let i = brace; i < source.length; i++) {
        const ch = source[i];
        if (ch === '{') depth += 1;
        else if (ch === '}') {
            depth -= 1;
            if (depth === 0) return source.slice(start, i + 1);
        }
    }
    throw new Error(`unterminated function ${name}`);
}

function makeSandbox(options = {}) {
    const store = Object.assign({}, options.local || {});
    const fields = Object.assign({}, options.fields || {});
    const fetches = [];
    const location = {
        protocol: options.protocol || 'https:',
        hostname: options.hostname || 'abc.googleusercontent.com',
        href: options.href || 'https://abc.googleusercontent.com/canvas/taobaocao.html'
    };
    const localStorage = {
        getItem(key) {
            return Object.prototype.hasOwnProperty.call(store, key) ? store[key] : null;
        },
        setItem(key, value) {
            store[key] = String(value);
        },
        removeItem(key) {
            delete store[key];
        }
    };
    const document = {
        getElementById(id) {
            if (!Object.prototype.hasOwnProperty.call(fields, id)) return null;
            const current = fields[id];
            if (current && typeof current === 'object') return current;
            return { value: current };
        }
    };
    const fetchImpl = options.fetch || (async () => ({
        ok: true,
        status: 200,
        statusText: 'OK',
        json: async () => ({ ok: true }),
        text: async () => '{}'
    }));
    const sandbox = {
        window: { location },
        document,
        localStorage,
        URL,
        fetch: async (url, init) => {
            fetches.push({ url: String(url), init: init || {} });
            return fetchImpl(url, init);
        },
        fetches,
        store,
        fields
    };
    sandbox.window.document = document;
    sandbox.window.localStorage = localStorage;
    sandbox.window.fetch = sandbox.fetch;
    sandbox.window.URL = URL;
    vm.createContext(sandbox);
    const hostingSrc = [
        extractNamed(html, 'getAccountHostingDraftIdKey'),
        "const DEFAULT_HOSTING_ENDPOINT = 'https://hoangthiencm.id.vn/api/user_phuluc_draft.php';",
        extractNamed(html, 'persistCustomHostingUrl'),
        extractNamed(html, 'getAccountHostingEndpoint'),
        extractNamed(html, 'hostingFetchOptions'),
        extractNamed(html, 'hostingErrorMessage'),
        extractNamed(html, 'saveAccountProfileToHosting'),
        extractNamed(html, 'loadAccountProfileFromHosting')
    ].join('\n');
    vm.runInContext(hostingSrc, sandbox);
    return sandbox;
}

async function main() {
    const canvas = makeSandbox({ hostname: 'hash.googleusercontent.com', href: 'https://hash.googleusercontent.com/canvas' });
    assert.strictEqual(canvas.getAccountHostingEndpoint(), DEFAULT_HOSTING_ENDPOINT, 'Canvas must use absolute school endpoint');

    const fileProto = makeSandbox({ protocol: 'file:', hostname: '', href: 'file:///C:/taobaocao.html' });
    assert.strictEqual(fileProto.getAccountHostingEndpoint(), DEFAULT_HOSTING_ENDPOINT, 'file:// must use absolute school endpoint');

    const local = makeSandbox({ hostname: 'localhost', href: 'http://localhost:5173/taobaocao.html', protocol: 'http:' });
    assert.strictEqual(local.getAccountHostingEndpoint(), DEFAULT_HOSTING_ENDPOINT, 'localhost must use absolute school endpoint');

    const custom = makeSandbox({
        fields: { accHostingCustomUrl: 'https://truong-thcs.example.edu.vn/' },
        hostname: 'hash.googleusercontent.com'
    });
    assert.strictEqual(
        custom.getAccountHostingEndpoint(),
        'https://truong-thcs.example.edu.vn/api/user_phuluc_draft.php',
        'custom hosting URL must win'
    );

    const fromStorage = makeSandbox({
        local: { tthc_custom_hosting_url: 'https://other.example' },
        hostname: 'hash.googleusercontent.com'
    });
    assert.strictEqual(
        fromStorage.getAccountHostingEndpoint(),
        'https://other.example/api/user_phuluc_draft.php',
        'localStorage custom hosting URL must win when input is empty'
    );

    const sameOrigin = makeSandbox({
        hostname: 'school.example.edu.vn',
        href: 'https://school.example.edu.vn/backupcode%20viettailieu/taobaocao.html',
        protocol: 'https:'
    });
    assert.strictEqual(
        sameOrigin.getAccountHostingEndpoint(),
        'https://school.example.edu.vn/api/user_phuluc_draft.php',
        'same-origin http(s) host must resolve relative ../api path'
    );

    const saveSandbox = makeSandbox({
        hostname: 'hash.googleusercontent.com',
        fetch: async () => ({
            ok: true,
            status: 200,
            statusText: 'OK',
            json: async () => ({ ok: true, draft_info: { id: 17 } })
        })
    });
    await saveSandbox.saveAccountProfileToHosting('tranphu_gv1', { profile: { unit_name: 'THCS' } });
    assert.strictEqual(saveSandbox.fetches.length, 1, 'save must issue one POST');
    const saveCall = saveSandbox.fetches[0];
    assert.strictEqual(saveCall.url, DEFAULT_HOSTING_ENDPOINT);
    assert.strictEqual(saveCall.init.credentials, 'omit');
    assert.strictEqual(saveCall.init.cache, 'no-store');
    assert.strictEqual(saveCall.init.headers['X-User-Account'], 'tranphu_gv1');
    const saveBody = JSON.parse(saveCall.init.body);
    assert.strictEqual(saveBody.user_account, 'tranphu_gv1');
    assert.strictEqual(saveSandbox.store['tthc_account_profile_hosting_draft:tranphu_gv1'], '17');

    const loadSandbox = makeSandbox({
        hostname: 'hash.googleusercontent.com',
        fetch: async (url) => {
            const href = String(url);
            if (href.includes('action=list')) {
                return {
                    ok: true,
                    status: 200,
                    statusText: 'OK',
                    json: async () => ({ ok: true, drafts: [{ id: 9, title: 'Hồ sơ tổ chuyên môn' }] })
                };
            }
            return {
                ok: true,
                status: 200,
                statusText: 'OK',
                json: async () => ({ ok: true, draft: { account_profile_payload: { profile: { unit_name: 'THCS' } } } })
            };
        }
    });
    const payload = await loadSandbox.loadAccountProfileFromHosting('tranphu_gv1');
    assert.ok(payload && payload.profile, 'load must return profile payload');
    assert.ok(loadSandbox.fetches.length >= 2, 'load without cached id lists then fetches');
    for (const call of loadSandbox.fetches) {
        assert.strictEqual(call.init.credentials, 'omit', 'load fetch must omit credentials');
        assert.strictEqual(call.init.cache, 'no-store', 'load fetch must disable cache');
        assert.strictEqual(call.init.headers['X-User-Account'], 'tranphu_gv1');
    }

    assert.match(html, /Authorization:\s*`Bearer \$\{pat\}`/, 'GitHub auth header must use Bearer');
    assert.doesNotMatch(html, /Authorization:\s*`token \$\{pat\}`/, 'legacy token prefix must be removed');
    for (const name of ['githubReadJsonFile', 'githubListDirectory', 'githubWriteJsonFile']) {
        const src = extractNamed(html, name);
        assert.match(src, /githubAuthHeaders\(pat/, `${name} must send Bearer via githubAuthHeaders`);
        assert.match(src, /formatGitHubApiError/, `${name} must surface 401 Bad credentials guidance`);
    }
    assert.match(extractNamed(html, 'formatGitHubApiError'), /Xóa token đã lưu/, '401 guidance must mention clearing the saved token');

    assert.strictEqual(globalConfig.github_pat, '', 'github_pat must be emptied');
    const rawConfig = fs.readFileSync(path.join(root, 'global_config.json'), 'utf8');
    assert.ok(!rawConfig.includes(REVOKED_PAT), 'revoked PAT must not remain in global_config.json');

    assert.match(html, /id="accHostingCustomUrl"/, 'custom hosting URL input');
    assert.match(html, /onclick="testHostingConnection\(\)"/, 'test hosting button');
    assert.match(html, /onclick="testGitHubConnection\(\)"/, 'test GitHub button');
    assert.match(html, /onclick="clearGitHubPat\(\)"/, 'clear PAT button');
    assert.match(html, /🔌 Kiểm tra kết nối Hosting/, 'hosting test label');
    assert.match(html, /🔍 Kiểm tra kết nối GitHub/, 'github test label');
    assert.match(html, /Xóa token đã lưu/, 'clear PAT label');
    assert.match(html, /✦ Chế độ Gemini Canvas · Máy chủ kết nối: hoangthiencm\.id\.vn/, 'Canvas banner');
    assert.match(html, /Username \/ Tài khoản giáo viên \(trên hoangthiencm\.id\.vn\)/, 'username label');
    assert.match(html, /placeholder="Nhập username đăng nhập \(VD: tranphu_gv1\)"/, 'username placeholder');
    assert.match(html, /Contents: Read and write/, 'PAT scope hint');
    assert.match(html, /Hồ sơ đã được lưu vào bộ nhớ trình duyệt \(Local-First\)/, 'transparent local-first hosting error');
    assert.match(html, /async function testHostingConnection\(/, 'testHostingConnection exists');
    assert.match(html, /async function testGitHubConnection\(/, 'testGitHubConnection exists');
    assert.match(html, /function clearGitHubPat\(/, 'clearGitHubPat exists');
    assert.match(extractNamed(html, 'testHostingConnection'), /action=list/, 'hosting test uses action=list');
    assert.match(extractNamed(html, 'testHostingConnection'), /hostingFetchOptions/, 'hosting test omits credentials');
    assert.match(extractNamed(html, 'clearGitHubPat'), /localStorage\.removeItem\("github_pat"\)/, 'clearGitHubPat removes stored token');

    assert.match(php, /Access-Control-Allow-Origin: \*/, 'CORS Origin *');
    assert.match(php, /X-User-Account/, 'CORS allows X-User-Account');
    assert.match(
        php,
        /Tài khoản '\$account' chưa đăng ký hoặc chưa kích hoạt trên hoangthiencm\.id\.vn\./,
        '401 must name the missing/inactive account'
    );
    assert.match(
        php,
        /\$altAccount = strpos\(\$account, '@'\) !== false \? explode\('@', \$account\)\[0\] : \$account;/,
        'backend must derive username from email local-part'
    );
    assert.match(
        php,
        /SELECT id FROM users WHERE \(username = \? OR username = \?\) AND is_active = 1 LIMIT 1/,
        'backend must match both full email and username before @'
    );

    const getEmailSrc = extractNamed(html, 'getCurrentUserEmail');
    assert.match(getEmailSrc, /localStorage\.getItem\("userEmail"\)/, 'startup email reads userEmail');
    assert.match(getEmailSrc, /localStorage\.getItem\("userName"\)/, 'startup email reads userName');
    assert.match(getEmailSrc, /localStorage\.getItem\("canvas_xdpl_user"\)/, 'startup email reads canvas_xdpl_user');
    assert.match(getEmailSrc, /localStorage\.setItem\("userEmail", email\)/, 'resolved account is persisted');

    const autoSyncSrc = extractNamed(html, 'autoSyncAccountProfileOnStartup');
    assert.match(autoSyncSrc, /loadAccountSettingsFromGitHub\(false, true\)/, 'startup auto-sync must forceApply');
    assert.match(html, /await autoSyncAccountProfileOnStartup\(\)/, 'startup IIFE must call autoSyncAccountProfileOnStartup');
    assert.doesNotMatch(
        html,
        /await loadAccountSettingsFromGitHub\(false, false\)/,
        'startup must no longer load with forceApply=false'
    );

    assert.match(html, /id="headerAccountBadge"/, 'header account badge');
    assert.match(html, /id="headerAccountName"/, 'header account name');
    assert.match(html, /id="headerAccountSyncStatus"/, 'header sync status');
    assert.match(html, /🟢 Đã nạp từ Hosting/, 'hosting loaded badge copy');
    assert.match(html, /🔄 Nạp lại hồ sơ/, 'header reload button label');
    assert.match(html, /onclick="loadAccountSettingsFromGitHub\(true, true\)"/, 'header reload uses forceApply');
    assert.match(html, /id="accountSyncToast"/, 'auto-sync toast');
    assert.match(extractNamed(html, 'loadAccountProfileFromHosting'), /appendix_type === "account-profile"/, 'hosting list matches account-profile type');
    assert.match(extractNamed(html, 'loadAccountProfileFromHosting'), /title === "Hồ sơ tổ chuyên môn"/, 'hosting list still matches title');

    const applySrc = extractNamed(html, 'applyAccountProfileToSetupInputs');
    assert.match(applySrc, /unitNamePreset/, 'forceApply updates unit name');
    assert.match(applySrc, /unitParentPreset/, 'forceApply updates unit parent');
    assert.doesNotMatch(applySrc, /docSubject|docNumberPreset/, 'forceApply must not overwrite document subject/number');

    const emailStore = {};
    const emailSandbox = {
        document: { getElementById() { return null; } },
        localStorage: {
            getItem(key) { return Object.prototype.hasOwnProperty.call(emailStore, key) ? emailStore[key] : null; },
            setItem(key, value) { emailStore[key] = String(value); }
        }
    };
    vm.createContext(emailSandbox);
    vm.runInContext(getEmailSrc, emailSandbox);
    emailSandbox.localStorage.setItem('canvas_xdpl_user', 'HoangThienCM@gmail.com');
    assert.strictEqual(emailSandbox.getCurrentUserEmail(false), 'hoangthiencm@gmail.com', 'canvas_xdpl_user is used on startup');
    assert.strictEqual(emailStore.userEmail, 'hoangthiencm@gmail.com', 'resolved email is persisted to userEmail');

    console.log('taobaocao-account-sync smoke: passed');
}

main().catch((err) => {
    console.error(err && err.stack ? err.stack : err);
    process.exit(1);
});
