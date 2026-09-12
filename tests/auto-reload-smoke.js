'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const root = path.join(__dirname, '..');
const guardPath = path.join(root, 'js', 'security-guard.js');
const workflowPath = path.join(root, '.github', 'workflows', 'ftp-deploy.yml');
const htaccessPath = path.join(root, '.htaccess');
const guardSrc = fs.readFileSync(guardPath, 'utf8');

function assert(name, condition) {
    console[condition ? 'log' : 'error']((condition ? 'OK: ' : 'FAIL: ') + name);
    if (!condition) process.exitCode = 1;
}

function flush() {
    return new Promise(resolve => setImmediate(resolve));
}

function makeSandbox(options) {
    const local = Object.assign({}, options.local);
    const session = Object.assign({}, options.session);
    const documentListeners = {};
    const windowListeners = {};
    const intervals = [];
    const reloads = [];
    let fetchCalls = 0;
    const document = {
        hidden: false,
        addEventListener(type, callback) {
            (documentListeners[type] || (documentListeners[type] = [])).push(callback);
        }
    };
    const window = {
        location: { hostname: 'hoangthiencm.id.vn', protocol: 'https:', reload(force) { reloads.push(force); } },
        localStorage: { getItem(key) { return Object.prototype.hasOwnProperty.call(local, key) ? local[key] : null; }, setItem(key, value) { local[key] = String(value); } },
        sessionStorage: { getItem(key) { return Object.prototype.hasOwnProperty.call(session, key) ? session[key] : null; }, setItem(key, value) { session[key] = String(value); } },
        addEventListener(type, callback) { (windowListeners[type] || (windowListeners[type] = [])).push(callback); },
        fetch(url, optionsArg) {
            fetchCalls += 1;
            return Promise.resolve(options.fetchResponse(url, optionsArg, fetchCalls));
        },
        console: { clear() {}, log() {}, debug() {}, info() {}, dir() {}, dirxml() {}, trace() {}, table() {}, group() {}, groupCollapsed() {}, groupEnd() {}, warn() {}, error() {} },
        navigator: { userAgent: 'test', maxTouchPoints: 0 },
        screen: { width: 1920, height: 1080 }, matchMedia() { return { matches: false }; },
        outerWidth: 1920, innerWidth: 1920, outerHeight: 1080, innerHeight: 1080
    };
    const sandbox = { window, document, localStorage: window.localStorage, sessionStorage: window.sessionStorage, navigator: window.navigator, console: window.console, Promise, Date, Number, String, Boolean, Math, Error, Function, setInterval(callback, delay) { intervals.push({ callback, delay }); return intervals.length; } };
    vm.createContext(sandbox);
    const instrumented = guardSrc.replace(/\}\)\(\);\s*$/, 'window.__autoReloadHooks = { checkAppVersionUpdate: checkAppVersionUpdate };\n})();');
    vm.runInContext(instrumented, sandbox, { filename: 'security-guard.js' });
    return { local, session, documentListeners, windowListeners, intervals, reloads, get fetchCalls() { return fetchCalls; }, hooks: window.__autoReloadHooks };
}

(async function run() {
    const manifest = version => ({ ok: true, json() { return Promise.resolve({ version }); } });
    const firstVisit = makeSandbox({ fetchResponse: () => manifest('sha-one') });
    await flush(); await flush();
    assert('first visit records server version without reload', firstVisit.local.__system_app_version__ === 'sha-one' && firstVisit.reloads.length === 0);
    assert('manifest request bypasses cache', firstVisit.fetchCalls === 1);
    assert('checks every 60 seconds and on focus/visibility', firstVisit.intervals.some(item => item.delay === 60000) && firstVisit.windowListeners.focus && firstVisit.documentListeners.visibilitychange);

    const changedVersion = makeSandbox({ local: { __system_app_version__: 'sha-one' }, fetchResponse: () => manifest('sha-two') });
    await flush(); await flush();
    assert('changed version reloads once and stores the new version', changedVersion.local.__system_app_version__ === 'sha-two' && changedVersion.reloads.length === 1);
    await changedVersion.hooks.checkAppVersionUpdate();
    assert('reload debounce prevents a second reload within 10 seconds', changedVersion.reloads.length === 1);

    const networkFailure = makeSandbox({ local: { __system_app_version__: 'sha-one' }, fetchResponse: () => Promise.reject(new Error('offline')) });
    await flush(); await flush();
    assert('network failure does not reload or interrupt the page', networkFailure.reloads.length === 0);

    const workflow = fs.readFileSync(workflowPath, 'utf8');
    const htaccess = fs.readFileSync(htaccessPath, 'utf8');
    assert('workflow writes version.json before FTP sync', /Generate version manifest[\s\S]*writeFileSync\('version\.json'/.test(workflow) && workflow.indexOf('Generate version manifest') < workflow.indexOf('Sync files to hosting'));
    assert('htaccess disables cache for HTML and JSON', /FilesMatch "\\\.\(html\|htm\|json\)\$"/.test(htaccess) && /Cache-Control "no-cache, no-store, must-revalidate, max-age=0"/.test(htaccess));

    if (process.exitCode) process.exit(process.exitCode);
    console.log('auto-reload-smoke: all checks passed');
})();
