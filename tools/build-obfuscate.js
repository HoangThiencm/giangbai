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
        return;
    }

    const obfuscator = loadObfuscator(args.fallbackOnly);
    const mode = obfuscator ? 'javascript-obfuscator' : 'fallback';
    console.log('Obfuscate mode: ' + mode + (args.inPlace ? ' (in-place)' : ' -> ' + args.outDir));

    if (!args.inPlace) {
        fs.rmSync(args.outDir, { recursive: true, force: true });
        fs.mkdirSync(args.outDir, { recursive: true });
    }

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

    console.log('DONE ' + changed + ' file(s)');
}

if (require.main === module) {
    main();
}

module.exports = {
    collectJsFiles,
    shouldSkipFile,
    transformSource,
    wrapBase64Iife,
    parseArgs
};
