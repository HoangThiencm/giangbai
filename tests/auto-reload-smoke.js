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

function makeSandbox() {
    const local = {};
    const session = {};
    const documentListeners = {};
    const windowListeners = {};
    const intervals = [];
    const reloads = [];
    let fetchCalls = 0;
    const fetchUrls = [];
    const document = {
        hidden: false,
        addEventListener(type, callback) {
            (documentListeners[type] || (documentListeners[type] = [])).push(callback);
        },
        getElementById() { return null; }
    };
    const window = {
        location: { hostname: 'hoangthiencm.id.vn', protocol: 'https:', reload(force) { reloads.push(force); } },
        localStorage: { getItem(key) { return Object.prototype.hasOwnProperty.call(local, key) ? local[key] : null; }, setItem(key, value) { local[key] = String(value); } },
        sessionStorage: { getItem(key) { return Object.prototype.hasOwnProperty.call(session, key) ? session[key] : null; }, setItem(key, value) { session[key] = String(value); } },
        addEventListener(type, callback) { (windowListeners[type] || (windowListeners[type] = [])).push(callback); },
        fetch(url) {
            fetchCalls += 1;
            fetchUrls.push(url);
            return Promise.resolve({ ok: true, json() { return Promise.resolve({ version: 'sha-one' }); } });
        },
        console: { clear() {}, log() {}, debug() {}, info() {}, dir() {}, dirxml() {}, trace() {}, table() {}, group() {}, groupCollapsed() {}, groupEnd() {}, warn() {}, error() {} },
        navigator: { userAgent: 'test', maxTouchPoints: 0 },
        screen: { width: 1920, height: 1080 }, matchMedia() { return { matches: false }; },
        outerWidth: 1920, innerWidth: 1920, outerHeight: 1080, innerHeight: 1080
    };
    const sandbox = { window, document, localStorage: window.localStorage, sessionStorage: window.sessionStorage, navigator: window.navigator, console: window.console, Promise, Date, Number, String, Boolean, Math, Error, Function, setInterval(callback, delay) { intervals.push({ callback, delay }); return intervals.length; } };
    vm.createContext(sandbox);
    vm.runInContext(guardSrc, sandbox, { filename: 'security-guard.js' });
    return { documentListeners, windowListeners, intervals, reloads, fetchUrls, get fetchCalls() { return fetchCalls; } };
}

(async function run() {
    assert('security-guard.js does not define initAutoUpdateChecker', !/\binitAutoUpdateChecker\b/.test(guardSrc));
    assert('security-guard.js does not define checkAppVersionUpdate', !/\bcheckAppVersionUpdate\b/.test(guardSrc));
    assert('security-guard.js does not fetch version.json', !/version\.json/.test(guardSrc) && !/\bfetch\s*\(/.test(guardSrc));

    const autoReloadCall = /window\.location\.reload/.test(guardSrc) &&
        !/Nhập mã xác thực Admin để mở khóa DevTools[\s\S]*window\.location\.reload\(\);/.test(guardSrc);
    assert('security-guard.js does not auto-call window.location.reload()', !autoReloadCall);

    const sandbox = makeSandbox();
    await flush();
    await flush();

    if (sandbox.windowListeners.focus) {
        sandbox.windowListeners.focus.forEach(callback => callback());
    }
    if (sandbox.documentListeners.visibilitychange) {
        sandbox.documentListeners.visibilitychange.forEach(callback => callback());
    }
    await flush();
    await flush();

    assert('loading security-guard.js does not reload the page', sandbox.reloads.length === 0);
    assert('loading security-guard.js does not fetch a version manifest', sandbox.fetchCalls === 0 && sandbox.fetchUrls.every(url => String(url).indexOf('version.json') === -1));
    assert('no 60-second auto-update interval is registered', !sandbox.intervals.some(item => item.delay === 60000));
    assert('focus and visibilitychange do not trigger a reload', sandbox.reloads.length === 0);

    const workflow = fs.readFileSync(workflowPath, 'utf8');
    const htaccess = fs.readFileSync(htaccessPath, 'utf8');
    assert('workflow writes version.json before FTP sync', /Generate version manifest[\s\S]*writeFileSync\('version\.json'/.test(workflow) && workflow.indexOf('Generate version manifest') < workflow.indexOf('Sync files to hosting'));
    assert('htaccess disables cache for HTML and JSON', /FilesMatch "\\\.\(html\|htm\|json\)\$"/.test(htaccess) && /Cache-Control "no-cache, no-store, must-revalidate, max-age=0"/.test(htaccess));

    if (process.exitCode) process.exit(process.exitCode);
    console.log('auto-reload-smoke: all checks passed');
})();
