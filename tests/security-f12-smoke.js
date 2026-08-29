'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const vm = require('vm');
const { execFileSync } = require('child_process');

const root = path.join(__dirname, '..');
const guardPath = path.join(root, 'js', 'security-guard.js');
const toolPath = path.join(root, 'tools', 'build-obfuscate.js');
const workflowPath = path.join(root, '.github', 'workflows', 'ftp-deploy.yml');
const guardSrc = fs.readFileSync(guardPath, 'utf8');

function failCount(checks) {
    let failed = 0;
    for (const [name, ok] of checks) {
        console[ok ? 'log' : 'error']((ok ? 'OK: ' : 'FAIL: ') + name);
        if (!ok) failed += 1;
    }
    return failed;
}

try {
    new vm.Script(guardSrc, { filename: 'security-guard.js' });
    new vm.Script(fs.readFileSync(toolPath, 'utf8'), { filename: 'build-obfuscate.js' });
    console.log('OK: security-guard.js and build-obfuscate.js syntax');
} catch (err) {
    console.error('FAIL: syntax', err.message);
    process.exit(1);
}

const staticChecks = [
    ['no plaintext htcm@admin', !/['"]htcm@admin['"]/.test(guardSrc)],
    ['no plaintext hoangthien key', !/['"]hoangthien['"]/.test(guardSrc)],
    ['localhost or debug skip', /if\s*\(\s*isLocalhost\s*\|\|\s*isDebugUnlocked\s*\)/.test(guardSrc)],
    ['blocks F12', /keyCode === 123/.test(guardSrc) && /F12/.test(guardSrc)],
    ['blocks Ctrl+U', /key === 'u'/.test(guardSrc)],
    ['admin shortcut Ctrl+Alt+Shift+D', /keyCode === 68/.test(guardSrc)],
    ['keeps editable context menu', /MATH-FIELD/.test(guardSrc) && /isContentEditable/.test(guardSrc)],
    ['hashed fallback keys', /7731ce4a/.test(guardSrc) && /c3e3eb18/.test(guardSrc)],
    ['DevTools lock overlay', /__gb_devtools_lock__/.test(guardSrc) && /showLockOverlay/.test(guardSrc)]
];

let failed = failCount(staticChecks);

function makeSandbox(options) {
    const listeners = { document: {}, window: {} };
    const sessionStore = Object.assign({}, options.session || {});
    const localStore = Object.assign({}, options.local || {});
    const createdEls = [];
    const documentElement = { style: { overflow: '' } };
    const body = {
        appendChild(el) {
            this.child = el;
            return el;
        }
    };
    const document = {
        body,
        documentElement,
        createdEls,
        addEventListener(type, fn) {
            listeners.document[type] = listeners.document[type] || [];
            listeners.document[type].push(fn);
        },
        getElementById(id) {
            for (let i = 0; i < createdEls.length; i++) {
                if (createdEls[i].id === id) return createdEls[i];
            }
            return null;
        },
        createElement(tag) {
            const el = {
                tagName: String(tag || 'DIV').toUpperCase(),
                id: '',
                style: { display: '' },
                textContent: '',
                setAttribute() {},
                parentNode: null
            };
            createdEls.push(el);
            return el;
        }
    };
    const windowObj = {
        location: {
            hostname: options.hostname || 'hoangthiencm.id.vn',
            protocol: options.protocol || 'https:',
            reload() { windowObj.__reloaded = true; }
        },
        sessionStorage: {
            getItem(key) { return Object.prototype.hasOwnProperty.call(sessionStore, key) ? sessionStore[key] : null; },
            setItem(key, value) { sessionStore[key] = String(value); }
        },
        localStorage: {
            getItem(key) { return Object.prototype.hasOwnProperty.call(localStore, key) ? localStore[key] : null; },
            setItem(key, value) { localStore[key] = String(value); }
        },
        addEventListener(type, fn) {
            listeners.window[type] = listeners.window[type] || [];
            listeners.window[type].push(fn);
        },
        console: {
            log() {}, debug() {}, info() {}, dir() {}, dirxml() {}, trace() {},
            table() {}, group() {}, groupCollapsed() {}, groupEnd() {},
            clear() {}, error() {}, warn() {}
        },
        outerWidth: 1920,
        innerWidth: 1920,
        outerHeight: 1080,
        innerHeight: 1080,
        __reloaded: false
    };
    const sandbox = {
        window: windowObj,
        document,
        sessionStorage: windowObj.sessionStorage,
        localStorage: windowObj.localStorage,
        console: windowObj.console,
        performance: { now() { return 0; } },
        Function,
        Object,
        Error,
        Date,
        Math,
        String,
        Boolean,
        setInterval() { return 1; },
        prompt: options.prompt || function () { return null; },
        alert: options.alert || function () {},
        listeners,
        sessionStore
    };
    vm.createContext(sandbox);
    vm.runInContext(guardSrc, sandbox, { filename: 'security-guard.js' });
    return sandbox;
}

function fire(list, event) {
    (list || []).forEach(function (fn) { fn(event); });
}

function keyEvent(partial) {
    const prevented = { value: false };
    return Object.assign({
        keyCode: 0,
        which: 0,
        key: '',
        code: '',
        ctrlKey: false,
        metaKey: false,
        shiftKey: false,
        altKey: false,
        target: { tagName: 'DIV', isContentEditable: false },
        preventDefault() { prevented.value = true; },
        stopPropagation() {},
        prevented
    }, partial);
}

(function testLocalhostSkip() {
    const box = makeSandbox({ hostname: 'localhost', protocol: 'http:' });
    const ok = !box.listeners.document.keydown && !box.listeners.document.contextmenu;
    console[ok ? 'log' : 'error']((ok ? 'OK: ' : 'FAIL: ') + 'localhost skips protection');
    if (!ok) failed += 1;
})();

(function testProductionBlocks() {
    const box = makeSandbox({});
    const f12 = keyEvent({ keyCode: 123, which: 123, key: 'F12', code: 'F12' });
    fire(box.listeners.document.keydown, f12);
    const viewSource = keyEvent({ keyCode: 85, key: 'u', ctrlKey: true });
    fire(box.listeners.document.keydown, viewSource);
    const inspect = keyEvent({ keyCode: 73, key: 'i', ctrlKey: true, shiftKey: true });
    fire(box.listeners.document.keydown, inspect);
    const menu = keyEvent({});
    fire(box.listeners.document.contextmenu, menu);
    const inputMenu = keyEvent({ target: { tagName: 'INPUT', isContentEditable: false } });
    fire(box.listeners.document.contextmenu, inputMenu);
    const saveInInput = keyEvent({
        keyCode: 83,
        key: 's',
        ctrlKey: true,
        target: { tagName: 'TEXTAREA', isContentEditable: false }
    });
    fire(box.listeners.document.keydown, saveInInput);

    const checks = [
        ['F12 blocked in production', f12.prevented.value],
        ['Ctrl+U blocked', viewSource.prevented.value],
        ['Ctrl+Shift+I blocked', inspect.prevented.value],
        ['context menu blocked on DIV', menu.prevented.value],
        ['context menu allowed on INPUT', !inputMenu.prevented.value],
        ['Ctrl+S allowed in textarea', !saveInInput.prevented.value]
    ];
    failed += failCount(checks);
})();

(function testLockOverlayOnDevToolsSize() {
    const box = makeSandbox({});
    box.window.outerWidth = 1920;
    box.window.innerWidth = 800;
    fire(box.listeners.window.resize, {});
    const overlay = box.document.getElementById('__gb_devtools_lock__');
    const ok = Boolean(overlay && overlay.style.display === 'flex' && /DevTools/.test(overlay.textContent || ''));
    console[ok ? 'log' : 'error']((ok ? 'OK: ' : 'FAIL: ') + 'overlay locks screen when DevTools size detected');
    if (!ok) failed += 1;
})();

(function testNoOverlayOnLocalhost() {
    const box = makeSandbox({ hostname: 'localhost', protocol: 'http:' });
    const ok = box.document.createdEls.length === 0;
    console[ok ? 'log' : 'error']((ok ? 'OK: ' : 'FAIL: ') + 'localhost does not create lock overlay');
    if (!ok) failed += 1;
})();

(function testDebugUnlock() {
    let prompted = false;
    const box = makeSandbox({
        prompt() {
            prompted = true;
            return 'hoangthien';
        }
    });
    const unlock = keyEvent({ keyCode: 68, key: 'd', ctrlKey: true, altKey: true, shiftKey: true });
    fire(box.listeners.document.keydown, unlock);
    const ok = prompted && box.sessionStore.__system_debug_unlocked__ === 'true' && box.window.__reloaded;
    console[ok ? 'log' : 'error']((ok ? 'OK: ' : 'FAIL: ') + 'hashed admin key still unlocks debug');
    if (!ok) failed += 1;
})();

(function testDebugSessionSkip() {
    const box = makeSandbox({
        session: { __system_debug_unlocked__: 'true' }
    });
    const ok = !box.listeners.document.keydown;
    console[ok ? 'log' : 'error']((ok ? 'OK: ' : 'FAIL: ') + 'unlocked session skips protection');
    if (!ok) failed += 1;
})();

const obfuscatorSrc = fs.readFileSync(toolPath, 'utf8');
failed += failCount([
    ['stringArrayThreshold 1', /stringArrayThreshold:\s*1\b/.test(obfuscatorSrc)],
    ['transformObjectKeys true', /transformObjectKeys:\s*true/.test(obfuscatorSrc)],
    ['debugProtection true', /debugProtection:\s*true/.test(obfuscatorSrc)],
    ['debugProtectionInterval 1500', /debugProtectionInterval:\s*1500/.test(obfuscatorSrc)],
    ['selfDefending true for all files', /selfDefending:\s*true/.test(obfuscatorSrc) && !/selfDefending:\s*isGuard/.test(obfuscatorSrc)]
]);

const workflow = fs.readFileSync(workflowPath, 'utf8');
failed += failCount([
    ['workflow installs javascript-obfuscator', /javascript-obfuscator@4/.test(workflow)],
    ['workflow runs build-obfuscate --in-place', /node tools\/build-obfuscate\.js --in-place/.test(workflow)],
    ['workflow still excludes tools/**', /tools\/\*\*/.test(workflow)]
]);

const dryRun = execFileSync(process.execPath, [toolPath, '--dry-run'], {
    cwd: root,
    encoding: 'utf8'
});
failed += failCount([
    ['dry-run lists security-guard.js', /js\/security-guard\.js/.test(dryRun)],
    ['dry-run lists access-control.js', /^access-control\.js$/m.test(dryRun)],
    ['dry-run skips vendor min.js', !/vendor\/katex\.min\.js/.test(dryRun)],
    ['dry-run skips tools', !/tools\/build-obfuscate\.js/.test(dryRun) && !/tools\/obfuscate\.js/.test(dryRun)],
    ['dry-run skips tests', !/tests\//.test(dryRun)]
]);

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'gb-obf-'));
try {
    fs.copyFileSync(guardPath, path.join(tmp, 'security-guard.js'));
    execFileSync(process.execPath, [toolPath, '--in-place', '--fallback-only', '--root', tmp], {
        cwd: root,
        encoding: 'utf8'
    });
    const obfuscated = fs.readFileSync(path.join(tmp, 'security-guard.js'), 'utf8');
    const originalStill = fs.readFileSync(guardPath, 'utf8');
    failed += failCount([
        ['fallback wrap hides source comments', !obfuscated.includes('Security Guard - Module')],
        ['fallback wrap is not plaintext copy', obfuscated !== originalStill],
        ['in-place on temp does not mutate repo source', originalStill === guardSrc]
    ]);
} finally {
    fs.rmSync(tmp, { recursive: true, force: true });
}

failed += failCount([
    ['bundler scans HTML script tags', /findLocalScriptGroups/.test(obfuscatorSrc) && /applyBundles/.test(obfuscatorSrc)],
    ['dry-run plans soankhbd bundle', /BUNDLE soankhbd\.html -> js\/soankhbd\.bundle\.js/.test(dryRun)],
    ['soankhbd bundle lists khbd-app.js', /BUNDLE soankhbd\.html[\s\S]*js\/khbd-app\.js/.test(dryRun)],
    ['soankhbd bundle lists ai-design-config.js', /BUNDLE soankhbd\.html[\s\S]*ai-design-config\.js/.test(dryRun)],
    ['dry-run does not bundle vendor or CDN', !/BUNDLE[^\n]*vendor\//.test(dryRun) && !/cdn\.tailwindcss\.com/.test(dryRun)]
]);

const bundleTmp = fs.mkdtempSync(path.join(os.tmpdir(), 'gb-bundle-'));
try {
    fs.mkdirSync(path.join(bundleTmp, 'js'));
    fs.mkdirSync(path.join(bundleTmp, 'vendor'));
    fs.writeFileSync(path.join(bundleTmp, 'first.js'), 'window.FirstFlag = 1;\n', 'utf8');
    fs.writeFileSync(path.join(bundleTmp, 'second.js'), 'window.SecondFlag = window.FirstFlag + 1;\n', 'utf8');
    fs.writeFileSync(path.join(bundleTmp, 'vendor', 'katex.min.js'), 'window.VendorFlag = 9;\n', 'utf8');
    fs.writeFileSync(path.join(bundleTmp, 'page.html'), [
        '<!DOCTYPE html>',
        '<html><body>',
        '<script src="https://cdn.example.com/tailwind.js"></script>',
        '<script src="first.js"></script>',
        '<script src="second.js"></script>',
        '<script src="vendor/katex.min.js"></script>',
        '</body></html>',
        ''
    ].join('\n'), 'utf8');
    execFileSync(process.execPath, [toolPath, '--in-place', '--fallback-only', '--root', bundleTmp], {
        cwd: root,
        encoding: 'utf8'
    });
    const bundledHtml = fs.readFileSync(path.join(bundleTmp, 'page.html'), 'utf8');
    const bundleFile = path.join(bundleTmp, 'js', 'page.bundle.js');
    const bundleCode = fs.existsSync(bundleFile) ? fs.readFileSync(bundleFile, 'utf8') : '';
    const scriptSrcs = [...bundledHtml.matchAll(/<script\b[^>]*\bsrc=["']([^"']+)["']/gi)].map(m => m[1]);
    failed += failCount([
        ['sample HTML writes js/page.bundle.js', fs.existsSync(bundleFile)],
        ['sample HTML has single local bundle src', scriptSrcs.filter(s => s.endsWith('page.bundle.js')).length === 1],
        ['sample HTML dropped first.js/second.js src', !scriptSrcs.some(s => /(^|\/)first\.js$/.test(s) || /(^|\/)second\.js$/.test(s))],
        ['sample HTML keeps CDN script', scriptSrcs.some(s => s.indexOf('cdn.example.com') !== -1)],
        ['sample HTML keeps vendor min.js', scriptSrcs.some(s => s.indexOf('vendor/katex.min.js') !== -1)],
        ['bundle preserves first then second', /FirstFlag[\s\S]*SecondFlag/.test(bundleCode)],
        ['CDN stays before bundle', bundledHtml.indexOf('cdn.example.com') < bundledHtml.indexOf('page.bundle.js')],
        ['vendor stays after bundle', bundledHtml.indexOf('page.bundle.js') < bundledHtml.indexOf('vendor/katex.min.js')]
    ]);
} finally {
    fs.rmSync(bundleTmp, { recursive: true, force: true });
}

if (failed) {
    console.error('FAILED checks:', failed);
    process.exit(1);
}
console.log('security-f12-smoke: all checks passed');
