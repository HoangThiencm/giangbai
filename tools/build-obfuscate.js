/**
 * Làm rối JS first-party lúc deploy (không đụng vendor / tests).
 *
 *   node tools/build-obfuscate.js              # ghi vào .deploy-obfuscated/
 *   node tools/build-obfuscate.js --in-place   # ghi đè working tree (chỉ CI)
 *   node tools/build-obfuscate.js --dry-run
 *
 * Ưu tiên javascript-obfuscator nếu đã cài. Không có thì fallback:
 *   - security-guard.js: bọc Base64 (IIFE, không lộ global)
 *   - file khác: chỉ xóa comment / gọn khoảng trắng (giữ khai báo global)
 */
'use strict';

const fs = require('fs');
const path = require('path');

const SKIP_DIR_NAMES = new Set([
    'node_modules',
    '.git',
    '.github',
    '.agents',
    '.deploy-obfuscated',
    'vendor',
    'tests',
    'docs',
    'agent-tools',
    'mcps',
    'data',
    'storage',
    'api',
    'tools',
    'qlvb',
    'taovideo',
    'cloudflare-worker'
]);

const SKIP_DIR_PREFIXES = [
    'backupcode',
    'GIAO AN'
];

const SKIP_FILE_NAMES = new Set([
    'obfuscate.js',
    'build-obfuscate.js',
    'trochoi.compiled.js',
    'thoikhoabieu-worker.js'
]);

function parseArgs(argv) {
    const args = {
        inPlace: false,
        dryRun: false,
        fallbackOnly: false,
        root: process.cwd(),
        outDir: path.join(process.cwd(), '.deploy-obfuscated')
    };
    for (let i = 0; i < argv.length; i++) {
        const token = argv[i];
        if (token === '--in-place') args.inPlace = true;
        else if (token === '--dry-run') args.dryRun = true;
        else if (token === '--fallback-only') args.fallbackOnly = true;
        else if (token === '--root' && argv[i + 1]) args.root = path.resolve(argv[++i]);
        else if (token === '--out' && argv[i + 1]) args.outDir = path.resolve(argv[++i]);
        else if (token === '--help' || token === '-h') args.help = true;
    }
    return args;
}

function relPosix(root, filePath) {
    return path.relative(root, filePath).split(path.sep).join('/');
}

function shouldSkipDir(name, rel) {
    if (SKIP_DIR_NAMES.has(name)) return true;
    if (name.startsWith('.') && name !== '.') return true;
    return SKIP_DIR_PREFIXES.some(function (prefix) {
        return name === prefix || rel === prefix || rel.startsWith(prefix + '/');
    });
}

function shouldSkipFile(name, rel) {
    if (!name.endsWith('.js')) return true;
    if (name.endsWith('.min.js')) return true;
    if (name.endsWith('.bundle.js') || /\.bundle-\d+\.js$/.test(name)) return true;
    if (name.endsWith('.bak')) return true;
    if (SKIP_FILE_NAMES.has(name)) return true;
    if (rel.indexOf('/vendor/') !== -1 || rel.indexOf('vendor/') === 0) return true;
    return false;
}

function collectJsFiles(root) {
    const results = [];
    function walk(dir) {
        let entries;
        try {
            entries = fs.readdirSync(dir, { withFileTypes: true });
        } catch (err) {
            return;
        }
        for (const ent of entries) {
            const full = path.join(dir, ent.name);
            const rel = relPosix(root, full);
            if (ent.isDirectory()) {
                if (shouldSkipDir(ent.name, rel)) continue;
                walk(full);
            } else if (ent.isFile() && !shouldSkipFile(ent.name, rel)) {
                results.push(full);
            }
        }
    }
    walk(root);
    results.sort();
    return results;
}

function stripComments(code) {
    return code
        .replace(/\/\*[\s\S]*?\*\//g, '')
        .replace(/^\s*\/\/.*$/gm, '')
        .replace(/(?<=[^:\\])\/\/.*$/gm, '');
}

function compactWhitespace(code) {
    return stripComments(code)
        .replace(/[ \t]+/g, ' ')
        .replace(/\n{2,}/g, '\n')
        .trim();
}

function wrapBase64Iife(code) {
    const cleaned = compactWhitespace(code);
    const b64 = Buffer.from(cleaned, 'utf8').toString('base64');
    return '(function(_0x1a){var _0x2b=typeof atob===\'function\'?function(s){return decodeURIComponent(escape(atob(s)));}:function(s){return Buffer.from(s,\'base64\').toString(\'utf8\');};new Function(_0x2b(_0x1a))();})("' + b64 + '");';
}

function loadObfuscator(fallbackOnly) {
    if (fallbackOnly) return null;
    try {
        return require('javascript-obfuscator');
    } catch (err) {
        return null;
    }
}

function obfuscatorOptions(rel) {
    return {
        compact: true,
        controlFlowFlattening: false,
        deadCodeInjection: false,
        debugProtection: true,
        debugProtectionInterval: 1500,
        disableConsoleOutput: false,
        identifierNamesGenerator: 'hexadecimal',
        renameGlobals: false,
        selfDefending: true,
        stringArray: true,
        stringArrayEncoding: ['base64'],
        stringArrayThreshold: 1,
        transformObjectKeys: true,
        unicodeEscapeSequence: false,
        target: 'browser'
    };
}

function transformSource(code, rel, obfuscator) {
    if (obfuscator) {
        return obfuscator.obfuscate(code, obfuscatorOptions(rel)).getObfuscatedCode();
    }
    if (/(^|\/)security-guard\.js$/.test(rel)) {
        return wrapBase64Iife(code);
    }
    return compactWhitespace(code);
}

function collectHtmlFiles(root) {
    const results = [];
    function walk(dir) {
        let entries;
        try {
            entries = fs.readdirSync(dir, { withFileTypes: true });
        } catch (err) {
            return;
        }
        for (const ent of entries) {
            const full = path.join(dir, ent.name);
            const rel = relPosix(root, full);
            if (ent.isDirectory()) {
                if (shouldSkipDir(ent.name, rel)) continue;
                walk(full);
            } else if (ent.isFile() && /\.html$/i.test(ent.name) && !/\.backup/i.test(ent.name)) {
                results.push(full);
            }
        }
    }
    walk(root);
    results.sort();
    return results;
}

function pageStem(htmlRel) {
    return path.basename(htmlRel, path.extname(htmlRel)).replace(/[^A-Za-z0-9_-]+/g, '-') || 'page';
}

function getAttr(attrs, name) {
    const re = new RegExp('\\b' + name + '\\s*=\\s*["\']([^"\']+)["\']', 'i');
    const m = String(attrs || '').match(re);
    return m ? m[1] : '';
}

function parseStandaloneScriptLine(line) {
    const m = String(line || '').match(/^([ \t]*)<script\b([^>]*)>\s*<\/script>[ \t\r]*$/i);
    if (!m) return null;
    const attrs = m[2];
    if (/\btype\s*=\s*["']?(module|text\/babel)/i.test(attrs)) return null;
    const src = getAttr(attrs, 'src');
    if (!src) return null;
    return { indent: m[1], attrs: attrs, src: src };
}

function isBlankOrCommentLine(line) {
    return /^\s*(?:<!--[\s\S]*?-->\s*)*$/.test(String(line || ''));
}

function stripSrcQuery(src) {
    return String(src || '').split('#')[0].split('?')[0].trim();
}

function resolveLocalScript(src, htmlDir, root) {
    const clean = stripSrcQuery(src);
    if (!clean) return null;
    if (/^(https?:)?\/\//i.test(clean) || /^data:/i.test(clean) || /^javascript:/i.test(clean)) return null;
    const full = clean.startsWith('/')
        ? path.join(root, clean.replace(/^\/+/, ''))
        : path.resolve(htmlDir, clean);
    const rel = relPosix(root, full);
    if (!rel || rel.startsWith('..')) return null;
    const name = path.basename(full);
    if (shouldSkipFile(name, rel)) return null;
    if (!fs.existsSync(full)) return null;
    return { full: full, rel: rel };
}

function findLocalScriptGroups(html, htmlDir, root) {
    const nl = html.indexOf('\r\n') !== -1 ? '\r\n' : '\n';
    const lines = html.split(/\r?\n/);
    const groups = [];
    let current = [];

    function flush() {
        if (current.length >= 2) groups.push(current);
        current = [];
    }

    for (let i = 0; i < lines.length; i++) {
        const parsed = parseStandaloneScriptLine(lines[i]);
        const resolved = parsed ? resolveLocalScript(parsed.src, htmlDir, root) : null;
        if (parsed && resolved) {
            current.push({
                lineIndex: i,
                indent: parsed.indent,
                src: parsed.src,
                rel: resolved.rel,
                full: resolved.full
            });
            continue;
        }
        if (current.length && isBlankOrCommentLine(lines[i])) continue;
        flush();
    }
    flush();
    return { nl: nl, lines: lines, groups: groups };
}

function bundleRelForGroup(htmlRel, groupIndex, groupCount) {
    const stem = pageStem(htmlRel);
    if (groupCount === 1) return 'js/' + stem + '.bundle.js';
    return 'js/' + stem + '.bundle-' + (groupIndex + 1) + '.js';
}

function joinScripts(files) {
    return files.map(function (filePath) {
        return fs.readFileSync(filePath, 'utf8').replace(/^\uFEFF/, '');
    }).join('\n;\n');
}

function scriptSrcFromHtml(htmlRel, bundleRel) {
    const htmlDir = path.posix.dirname(String(htmlRel || '').replace(/\\/g, '/'));
    const fromDir = !htmlDir || htmlDir === '.' ? '.' : htmlDir;
    return path.posix.relative(fromDir, bundleRel.replace(/\\/g, '/')) || bundleRel;
}

function planHtmlBundles(root) {
    const plans = [];
    const htmlFiles = collectHtmlFiles(root);
    for (const htmlPath of htmlFiles) {
        const htmlRel = relPosix(root, htmlPath);
        const htmlDir = path.dirname(htmlPath);
        const html = fs.readFileSync(htmlPath, 'utf8').replace(/^\uFEFF/, '');
        const found = findLocalScriptGroups(html, htmlDir, root);
        found.groups.forEach(function (group, idx) {
            plans.push({
                htmlPath: htmlPath,
                htmlRel: htmlRel,
                bundleRel: bundleRelForGroup(htmlRel, idx, found.groups.length),
                files: group.map(function (item) { return item.rel; }),
                group: group
            });
        });
    }
    return plans;
}

function applyBundles(root, destRoot, obfuscator, dryRun) {
    const htmlFiles = collectHtmlFiles(root);
    let count = 0;
    for (const htmlPath of htmlFiles) {
        const htmlRel = relPosix(root, htmlPath);
        const htmlDir = path.dirname(htmlPath);
        const raw = fs.readFileSync(htmlPath);
        const hasBom = raw.length >= 3 && raw[0] === 0xEF && raw[1] === 0xBB && raw[2] === 0xBF;
        const html = raw.toString('utf8').replace(/^\uFEFF/, '');
        const found = findLocalScriptGroups(html, htmlDir, root);
        if (!found.groups.length) continue;

        if (dryRun) {
            found.groups.forEach(function (group, idx) {
                const bundleRel = bundleRelForGroup(htmlRel, idx, found.groups.length);
                console.log('BUNDLE ' + htmlRel + ' -> ' + bundleRel);
                group.forEach(function (item) {
                    console.log('  ' + item.rel);
                });
            });
            count += found.groups.length;
            continue;
        }

        const drop = new Set();
        found.groups.forEach(function (group, idx) {
            const bundleRel = bundleRelForGroup(htmlRel, idx, found.groups.length);
            const joined = joinScripts(group.map(function (item) { return item.full; }));
            const obfuscated = transformSource(joined, bundleRel, obfuscator);
            const bundleDest = path.join(destRoot, bundleRel.split('/').join(path.sep));
            fs.mkdirSync(path.dirname(bundleDest), { recursive: true });
            fs.writeFileSync(bundleDest, obfuscated, 'utf8');
            const src = scriptSrcFromHtml(htmlRel, bundleRel);
            const indent = group[0].indent;
            const start = group[0].lineIndex;
            const end = group[group.length - 1].lineIndex;
            found.lines[start] = indent + '<script src="' + src + '"></script>';
            for (let i = start + 1; i <= end; i++) drop.add(i);
            console.log('BUNDLE ' + htmlRel + ' -> ' + bundleRel + ' (' + group.length + ' files, ' + joined.length + ' -> ' + obfuscated.length + ')');
            count += 1;
        });

        const nextLines = found.lines.filter(function (_line, idx) { return !drop.has(idx); });
        const nextHtml = (hasBom ? '\uFEFF' : '') + nextLines.join(found.nl);
        const htmlDest = path.join(destRoot, htmlRel.split('/').join(path.sep));
        fs.mkdirSync(path.dirname(htmlDest), { recursive: true });
        fs.writeFileSync(htmlDest, nextHtml, 'utf8');
    }
    return count;
}

function main() {
    const args = parseArgs(process.argv.slice(2));
    if (args.help) {
        console.log('Sử dụng: node tools/build-obfuscate.js [--dry-run] [--in-place] [--fallback-only] [--root DIR] [--out DIR]');
        process.exit(0);
    }

    const root = args.root;
    const files = collectJsFiles(root);
    if (args.dryRun) {
        files.forEach(function (filePath) {
            console.log(relPosix(root, filePath));
        });
        console.log('TOTAL ' + files.length);
        applyBundles(root, root, null, true);
        return;
    }

    const obfuscator = loadObfuscator(args.fallbackOnly);
    const mode = obfuscator ? 'javascript-obfuscator' : 'fallback';
    const destRoot = args.inPlace ? root : args.outDir;
    console.log('Obfuscate mode: ' + mode + (args.inPlace ? ' (in-place)' : ' -> ' + args.outDir));

    if (!args.inPlace) {
        fs.rmSync(args.outDir, { recursive: true, force: true });
        fs.mkdirSync(args.outDir, { recursive: true });
    }

    const bundled = applyBundles(root, destRoot, obfuscator, false);

    let changed = 0;
    for (const filePath of files) {
        const rel = relPosix(root, filePath);
        const original = fs.readFileSync(filePath, 'utf8');
        const next = transformSource(original, rel, obfuscator);
        const dest = args.inPlace ? filePath : path.join(args.outDir, rel.split('/').join(path.sep));
        fs.mkdirSync(path.dirname(dest), { recursive: true });
        fs.writeFileSync(dest, next, 'utf8');
        changed += 1;
        console.log('OK ' + rel + ' (' + original.length + ' -> ' + next.length + ')');
    }

    console.log('DONE ' + changed + ' file(s), ' + bundled + ' bundle(s)');
}

if (require.main === module) {
    main();
}

module.exports = {
    collectJsFiles,
    collectHtmlFiles,
    shouldSkipFile,
    transformSource,
    wrapBase64Iife,
    parseArgs,
    findLocalScriptGroups,
    planHtmlBundles,
    applyBundles
};
