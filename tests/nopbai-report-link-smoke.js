const fs = require('fs');
const path = require('path');
const assert = require('assert');

const root = path.join(__dirname, '..');
const api = fs.readFileSync(path.join(root, 'api', 'submissions.php'), 'utf8');
const quanly = fs.readFileSync(path.join(root, 'nopbai-quanly.html'), 'utf8');
const nopbai = fs.readFileSync(path.join(root, 'nopbai.html'), 'utf8');

function extractFunction(src, name) {
    const start = src.indexOf(`function ${name}(`);
    assert.ok(start >= 0, `${name} must exist`);
    let i = src.indexOf('{', start);
    assert.ok(i >= 0, `${name} must have a body`);
    let depth = 0;
    let end = i;
    for (; end < src.length; end++) {
        const ch = src[end];
        if (ch === '{') depth++;
        else if (ch === '}') {
            depth--;
            if (depth === 0) {
                end++;
                break;
            }
        }
    }
    return src.slice(start, end);
}

const normalize = api.slice(
    api.indexOf('function submission_normalize_form_fields'),
    api.indexOf('function submission_form_fields')
);
assert.match(normalize, /\$types\s*=\s*\[[^\]]*['"]link['"]/, 'API $types must include link');
assert.match(normalize, /\$rawUrl\s*=\s*trim\(\(string\)\(\$raw\['url'\]\s*\?\?\s*''\)\)/, 'API must normalize url');
assert.match(normalize, /\$embed\s*=\s*\$type\s*===\s*'link'\s*\?\s*\(\$raw\['embed'\]\s*\?\?\s*true\)\s*:\s*false/, 'API must default embed true for link fields');
assert.match(normalize, /'url'\s*=>\s*\$type\s*===\s*'link'\s*\?\s*substr\(\$rawUrl,\s*0,\s*500\)\s*:\s*''/, 'API must persist url only for link fields');
assert.match(normalize, /'embed'\s*=>\s*\(bool\)\$embed/, 'API must persist embed as bool');
assert.match(normalize, /preg_match\('#\^https\?:\/\/#i',\s*\$rawUrl\)/, 'API must require http/https before storing url');
assert.match(normalize, /javascript\|data\|vbscript/, 'API must reject javascript/data/vbscript URLs');

const submit = api.slice(api.indexOf("if ($method === 'POST' && $action === 'submit')"), api.indexOf('$generalFiles ='));
assert.match(submit, /\$field\['required'\]\s*&&\s*\$value\s*===\s*''/, 'submit must reject empty required report fields including link');
assert.match(submit, /\$field\['type'\]\s*===\s*'heading'\)\s*continue/, 'submit must skip heading fields only');

assert.match(quanly, /option value="link"[^>]*>Liên kết \/ Nhúng bảng tính \(Link\)/, 'quanly dropdown must include link option');
assert.match(quanly, /state\.reportFields\[\$\{i\}\]\.url=this\.value/, 'quanly must bind url input');
assert.match(quanly, /state\.reportFields\[\$\{i\}\]\.embed=this\.checked/, 'quanly must bind embed checkbox');
assert.match(quanly, /Nhúng trực tiếp vào trang nộp bài \(Iframe\)/, 'quanly must show embed checkbox label');
assert.match(quanly, /url:\s*'',\s*embed:\s*true/, 'addReportField must default url and embed');
assert.match(quanly, /function submissionParticipantUrl\(code, personCode\)/, 'quanly must define submissionParticipantUrl');
assert.match(quanly, /function copyParticipantLink\(code, personCode\)/, 'quanly must define copyParticipantLink');
assert.match(quanly, /url\.searchParams\.set\('person',\s*personCode\)/, 'participant url must set person param');
assert.match(quanly, /copyParticipantLink\('\$\{esc\(a\.public_code\)\}','\$\{esc\(p\.participant_code\)\}'\)/, 'detail table must copy personalized link');
assert.match(quanly, /Link nộp/, 'detail table must show Link nộp button');
assert.match(quanly, /\['Mã cá nhân',\s*'Đường link nộp trực tiếp',/, 'exportParticipants must add direct link column');
assert.match(quanly, /submissionParticipantUrl\(a\.public_code,\s*x\.participant_code\)/, 'CSV rows must include participant url');
assert.match(quanly, /function reportCellHtml\(value\)/, 'quanly must render clickable report links');
assert.match(quanly, /class="text-teal-700 underline font-semibold"/, 'clickable report links must use teal underline style');
assert.match(quanly, /reportCellHtml\(reportCellValue\(s,c\.key\)\)/, 'submissions table must use reportCellHtml');

assert.match(nopbai, /function formatEmbedUrl\(url\)/, 'nopbai must define formatEmbedUrl');
assert.match(nopbai, /widget=true&headers=false&chrome=false/, 'Sheets embed url must hide chrome');
assert.match(nopbai, /embedded=true/, 'Forms embed url must set embedded=true');
assert.match(nopbai, /field\.type === 'link'/, 'nopbai must render link fields');
assert.match(nopbai, /<iframe src="\$\{esc\(embedUrl\)\}"/, 'nopbai must embed iframe with escaped url');
assert.match(nopbai, /Mở tab mới/, 'nopbai must offer open-in-new-tab fallback');
assert.match(nopbai, /name="report_\$\{esc\(field\.key\)\}"/, 'link confirmation input must use report_${esc(field.key)}');
assert.match(nopbai, /Nhập dữ liệu vào bảng tính bên dưới/, 'anti-forget step 1 must exist');
assert.match(nopbai, /Nộp bài/, 'anti-forget step 2 must mention submit');
assert.match(nopbai, /height:\s*560px/, 'embed frame height must be ~550px');
assert.match(nopbai, /const tag = field\.type === 'link' \? 'div' : 'label'/, 'link cards must not wrap iframe in a label');

const formatEmbedUrl = new Function(`${extractFunction(nopbai, 'formatEmbedUrl')}; return formatEmbedUrl;`)();
assert.strictEqual(
    formatEmbedUrl('https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit'),
    'https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit?widget=true&headers=false&chrome=false'
);
assert.strictEqual(
    formatEmbedUrl('https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit#gid=0'),
    'https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit?widget=true&headers=false&chrome=false'
);
assert.strictEqual(
    formatEmbedUrl('docs.google.com/spreadsheets/d/abc-123/edit?usp=sharing'),
    'https://docs.google.com/spreadsheets/d/abc-123/edit?widget=true&headers=false&chrome=false'
);
assert.strictEqual(
    formatEmbedUrl('https://docs.google.com/forms/d/e/abc/viewform'),
    'https://docs.google.com/forms/d/e/abc/viewform?embedded=true'
);
assert.strictEqual(
    formatEmbedUrl('https://docs.google.com/forms/d/e/abc/viewform?usp=sharing'),
    'https://docs.google.com/forms/d/e/abc/viewform?usp=sharing&embedded=true'
);
assert.strictEqual(
    formatEmbedUrl('https://docs.google.com/forms/d/e/abc/viewform?embedded=true'),
    'https://docs.google.com/forms/d/e/abc/viewform?embedded=true'
);
assert.strictEqual(formatEmbedUrl('https://example.com/sheet'), 'https://example.com/sheet');
assert.strictEqual(formatEmbedUrl(''), '');

const participantUrlFn = extractFunction(quanly, 'submissionParticipantUrl');
assert.match(participantUrlFn, /searchParams\.set\('code',\s*code\)/);
assert.match(participantUrlFn, /if \(personCode\) url\.searchParams\.set\('person',\s*personCode\)/);

console.log('nopbai report link smoke: passed');
