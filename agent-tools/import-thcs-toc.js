#!/usr/bin/env node
/**
 * Scrape mục lục SGK THCS (lớp 6–9) từ timdapan.com (bộ sách chung)
 * và fallback loigiaihay.com khi listing lớp 9 trống / 404.
 * Xuất agent-tools/thcs-toc.json — không ghi nhãn bộ sách lên dữ liệu bài học.
 */
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const https = require('https');
const { URL } = require('url');
const CACHE_DIR = path.join(os.tmpdir(), 'thcs-toc-cache');

const OUT_PATH = path.join(__dirname, 'thcs-toc.json');
const UA =
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36';
const DELAY_MS = 420;
const TIMEOUT_MS = 22000;

const SUBJECTS = [
  'toan',
  'nguvan',
  'khtn',
  'lichsudialy',
  'gdcd',
  'tinhoc',
  'congnghe',
  'amnhac',
  'mithuat',
  'gdtc',
  'hdtn-hn',
  'tienganh',
];
const GRADES = ['6', '7', '8', '9'];

const SUBJECT_NAMES = {
  toan: 'Toán',
  nguvan: 'Ngữ văn',
  khtn: 'Khoa học tự nhiên',
  lichsudialy: 'Lịch sử và Địa lí',
  gdcd: 'Giáo dục công dân',
  tinhoc: 'Tin học',
  congnghe: 'Công nghệ',
  amnhac: 'Âm nhạc',
  mithuat: 'Mĩ thuật',
  gdtc: 'Giáo dục thể chất',
  'hdtn-hn': 'Hoạt động trải nghiệm, hướng nghiệp',
  tienganh: 'Tiếng Anh',
};

const SKIP_SLUG_RE =
  /sach-giao-vien|sgv|bai-tap|sbt|tieng-phap|tieng-nga|tieng-trung|tieng-nhat|tieng-han|tieng-duc|sach-giao-khoa-dien-tu/;
const SKIP_TITLE_RE =
  /sách giáo viên|sách giáo viên|bài tập|sgv|sbt|tiếng pháp|tiếng nga|tiếng trung|tiếng nhật/i;
const FRONT_BACK_RE =
  /^(hướng dẫn sử dụng|lời nói đầu|phụ lục|giải thích.*thuật ngữ|bản tra cứu|bảng tra cứu|bảng phiên âm|book map|glossary|mục lục|những chữ viết tắt|một số thuật ngữ|danh sách ảnh|bản giải thích)\b/i;

const EXTRA_SLUGS = {
  6: [
    'ngu-van-6-tap-mot-2',
    'ngu-van-6-tap-hai-2',
    'khoa-hoc-tu-nhien-6',
    'lich-su-va-dia-li-6',
    'giao-duc-cong-dan-6-2',
    'tin-hoc-6',
    'cong-nghe-6-2',
    'am-nhac-6',
    'mi-thuat-6',
    'giao-duc-the-chat-6',
    'hoat-dong-trai-nghiem-huong-nghiep-6',
    'tieng-anh-6-tap-mot',
    'tieng-anh-6-tap-hai',
  ],
  7: [
    'ngu-van-7-tap-mot-2',
    'ngu-van-7-tap-hai-2',
    'ngu-van-7-tap-mot',
    'ngu-van-7-tap-hai',
    'khoa-hoc-tu-nhien-7',
    'khoa-hoc-tu-nhien-7-2',
    'lich-su-va-dia-li-7',
    'lich-su-va-dia-li-7-2',
    'giao-duc-cong-dan-7-2',
    'giao-duc-cong-dan-7',
    'tin-hoc-7',
    'tin-hoc-7-2',
    'cong-nghe-7-2',
    'cong-nghe-7',
    'am-nhac-7',
    'mi-thuat-7',
    'giao-duc-the-chat-7',
    'hoat-dong-trai-nghiem-huong-nghiep-7',
    'tieng-anh-7-tap-mot',
    'tieng-anh-7-tap-hai',
    'tieng-anh-7-global-success',
  ],
  8: [
    'ngu-van-8-tap-mot-2',
    'ngu-van-8-tap-hai-2',
    'ngu-van-8-tap-mot',
    'ngu-van-8-tap-hai',
    'khoa-hoc-tu-nhien-8',
    'khoa-hoc-tu-nhien-8-2',
    'lich-su-va-dia-li-8',
    'lich-su-va-dia-li-8-2',
    'giao-duc-cong-dan-8-2',
    'giao-duc-cong-dan-8',
    'tin-hoc-8',
    'tin-hoc-8-2',
    'cong-nghe-8-2',
    'cong-nghe-8',
    'am-nhac-8',
    'mi-thuat-8',
    'giao-duc-the-chat-8',
    'hoat-dong-trai-nghiem-huong-nghiep-8',
    'tieng-anh-8-tap-mot',
    'tieng-anh-8-tap-hai',
    'tieng-anh-8-global-success',
  ],
  9: [
    'khoa-hoc-tu-nhien-9',
    'khoa-hoc-tu-nhien-9-2',
    'lich-su-va-dia-li-9',
    'lich-su-va-dia-li-9-2',
    'tin-hoc-9',
    'tin-hoc-9-2',
    'cong-nghe-9',
    'cong-nghe-9-2',
    'am-nhac-9',
    'mi-thuat-9',
    'giao-duc-the-chat-9',
    'hoat-dong-trai-nghiem-huong-nghiep-9',
    'ngu-van-9-tap-mot-2',
    'ngu-van-9-tap-hai-2',
    'giao-duc-cong-dan-9-2',
    'tieng-anh-9-tap-mot',
    'tieng-anh-9-tap-hai',
    'tieng-anh-9-global-success',
    'cong-nghe-9-lap-dat-mang-dien-trong-nha',
    'cong-nghe-9-trong-trot',
    'cong-nghe-9-chan-nuoi',
    'cong-nghe-9-nong-nghiep',
    'cong-nghe-9-cong-nghiep',
    'cong-nghe-9-dinh-huong-nghe-nghiep',
  ],
};

const LOIGIAIHAY_FALLBACK = {
  9: {
    nguvan: 'https://loigiaihay.com/soan-van-9-ket-noi-tri-thuc-c1740.html',
    khtn: 'https://loigiaihay.com/sgk-khoa-hoc-tu-nhien-9-ket-noi-tri-thuc-c1744.html',
    lichsudialy: 'https://loigiaihay.com/sgk-lich-su-va-dia-li-9-ket-noi-tri-thuc-c1827.html',
    gdcd: 'https://loigiaihay.com/giao-duc-cong-dan-9-ket-noi-tri-thuc-c1818.html',
    tinhoc: 'https://loigiaihay.com/sgk-tin-hoc-9-ket-noi-tri-thuc-c1821.html',
    congnghe: 'https://loigiaihay.com/sgk-cong-nghe-9-ket-noi-tri-thuc-c1810.html',
    'hdtn-hn':
      'https://loigiaihay.com/sgk-hoat-dong-trai-nghiem-huong-nghiep-9-ket-noi-tri-thuc-c1862.html',
    tienganh: 'https://loigiaihay.com/tieng-anh-9-global-success-c1757.html',
    amnhac: 'https://loigiaihay.com/am-nhac-9-ket-noi-tri-thuc-c1814.html',
    mithuat: 'https://loigiaihay.com/mi-thuat-9-ket-noi-tri-thuc-c1817.html',
    gdtc: 'https://loigiaihay.com/giao-duc-the-chat-9-ket-noi-tri-thuc-c1815.html',
  },
  6: {
    lichsudialy: 'https://loigiaihay.com/sgk-lich-su-va-dia-li-6-ket-noi-tri-thuc-c1500.html',
    gdtc: 'https://loigiaihay.com/giao-duc-the-chat-6-ket-noi-tri-thuc-c1508.html',
    'hdtn-hn': 'https://loigiaihay.com/hoat-dong-trai-nghiem-huong-nghiep-6-ket-noi-tri-thuc-c1512.html',
  },
};

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function cachePath(url) {
  const safe = Buffer.from(url).toString('base64').replace(/[/+=]/g, '_');
  return path.join(CACHE_DIR, safe + '.json');
}

async function cachedFetch(url) {
  try {
    fs.mkdirSync(CACHE_DIR, { recursive: true });
    const p = cachePath(url);
    if (fs.existsSync(p)) {
      const hit = JSON.parse(fs.readFileSync(p, 'utf8'));
      if (hit && typeof hit.status === 'number') return { ...hit, cached: true };
    }
  } catch {
    /* ignore cache read */
  }
  const result = await fetchText(url);
  try {
    fs.mkdirSync(CACHE_DIR, { recursive: true });
    fs.writeFileSync(cachePath(url), JSON.stringify({ status: result.status, text: result.text }), 'utf8');
  } catch {
    /* ignore cache write */
  }
  return result;
}

function fetchText(url, timeoutMs = TIMEOUT_MS) {
  return new Promise((resolve) => {
    let settled = false;
    const done = (status, text) => {
      if (settled) return;
      settled = true;
      resolve({ status, text: text || '' });
    };
    try {
      const u = new URL(url);
      const req = https.request(
        {
          protocol: u.protocol,
          hostname: u.hostname,
          path: u.pathname + u.search,
          method: 'GET',
          headers: {
            'User-Agent': UA,
            Accept: 'text/html,application/xhtml+xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'vi,en;q=0.8',
          },
        },
        (res) => {
          const chunks = [];
          res.on('data', (c) => chunks.push(c));
          res.on('end', () => {
            const text = Buffer.concat(chunks).toString('utf8');
            const loc = res.headers.location;
            if (res.statusCode >= 300 && res.statusCode < 400 && loc) {
              const next = loc.startsWith('http') ? loc : `${u.protocol}//${u.host}${loc}`;
              fetchText(next, timeoutMs).then(resolve);
              return;
            }
            done(res.statusCode || 0, text);
          });
        }
      );
      req.setTimeout(timeoutMs, () => {
        req.destroy();
        done(0, '');
      });
      req.on('error', () => done(0, ''));
      req.end();
    } catch {
      done(0, '');
    }
  });
}

function decodeEntities(s) {
  return String(s || '')
    .replace(/&nbsp;/gi, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#39;|&apos;/g, "'")
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&#x([0-9a-f]+);/gi, (_, h) => String.fromCharCode(parseInt(h, 16)))
    .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(Number(n)));
}

function stripTags(html) {
  return decodeEntities(String(html || '').replace(/<[^>]+>/g, ' '))
    .replace(/\s+/g, ' ')
    .trim();
}

function collapseSpace(s) {
  return String(s || '')
    .replace(/\u00a0/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function isMostlyUpper(s) {
  const letters = s.replace(/[^A-Za-zÀ-ỹ]/g, '');
  if (letters.length < 4) return false;
  const upper = letters.replace(/[^A-ZÀ-Ỹ]/g, '').length;
  return upper / letters.length > 0.72;
}

function lightTitleCase(s) {
  const t = collapseSpace(s);
  if (!t) return t;
  if (!isMostlyUpper(t) && !/^[A-ZĐ]{3,}/.test(t)) return t;
  const lower = t.toLocaleLowerCase('vi');
  return lower.charAt(0).toLocaleUpperCase('vi') + lower.slice(1);
}

function romanOrNum(s) {
  return String(s || '').toUpperCase();
}

function normalizeChapter(raw, tapLabel) {
  let t = collapseSpace(raw).replace(/^[•\-\d.]+\s*/, '');
  t = t.replace(/^(CHƯƠNG|Chương|CHUONG)\s+([IVXLC]{1,6}|\d+)\b\s*[:.\-]?\s*/i, (_, __, n) => `Chương ${romanOrNum(n)}: `);
  t = t.replace(/^(Chủ đề|CHỦ ĐỀ|CHU DE)\s+(\d+|[IVX]{1,6})\b\s*[:.\-]?\s*/i, (_, __, n) => `Chủ đề ${n}: `);
  t = t.replace(/^(BÀI HỌC|Bài học)\s+(\d+|[IVX]{1,6})\b\s*[:.\-]?\s*/i, (_, __, n) => `Bài học ${n}: `);
  t = t.replace(/^(PHẦN|Phần)\s+(MỘT|HAI|BA|TƯ|NĂM|[IVX]{1,6}|\d+)\b\s*[:.\-]?\s*/i, (_, __, n) => {
    const map = { MỘT: 'một', HAI: 'hai', BA: 'ba', TƯ: 'tư', NĂM: 'năm' };
    const label = map[String(n).toUpperCase()] || romanOrNum(n);
    return `Phần ${label}: `;
  });
  if (!/^Phần\s+(một|hai|ba|tư|năm|\d|[IVX])/i.test(t)) {
    t = t.replace(/^(PHẦN|Phần)\s+/i, 'Phần: ');
  }
  t = t.replace(/^(MODULE|Module|Mô đun)\s+(\d+|[IVX]{1,6})\b\s*[:.\-]?\s*/i, (_, __, n) => `Mô đun ${n}: `);
  if (/^Chương\s/i.test(t) || /^Chủ đề\s/i.test(t) || /^Bài học\s/i.test(t) || /^Phần\s/i.test(t)) {
    const i = t.indexOf(':');
    if (i > 0) {
      const head = t.slice(0, i + 1);
      const rest = lightTitleCase(t.slice(i + 1).trim());
      t = rest ? `${head} ${rest}` : head.replace(/:$/, '');
    } else {
      t = lightTitleCase(t);
    }
  } else {
    t = lightTitleCase(t);
  }
  t = t.replace(/\s+:/g, ':').replace(/:\s*$/, (m) => m);
  if (tapLabel && !/\(\s*Tập\s+[12]\s*\)/i.test(t)) t += ` (${tapLabel})`;
  return collapseSpace(t);
}

function normalizeItem(raw) {
  let t = collapseSpace(raw);
  t = t.replace(/^\d+\.\s+(Bài\b)/i, '$1');
  t = t.replace(/\s*trang\s+\d+(?:\s*[,–-]\s*\d+)*\s*$/i, '');
  t = t.replace(/^(Bài)\s+(\d+[a-z]?)\s*[:.\-]?\s*/i, 'Bài $2: ');
  t = t.replace(/^(Unit)\s+(\d+)\s*[:.\-]?\s*/i, 'Unit $2: ');
  t = t.replace(/^(Review)\s+(\d+)\s*[:.\-]?\s*/i, 'Review $2: ');
  t = t.replace(/^(Starter unit)\s*[:.\-]?\s*/i, 'Starter unit: ');
  t = t.replace(/^(CHƯƠNG|Chương)\s+([IVXLC]{1,6}|\d+)\b\s*[:.\-]?\s*/i, (_, __, n) => `Chương ${romanOrNum(n)}: `);
  t = t.replace(/^(Chủ đề|CHỦ ĐỀ)\s+(\d+|[IVX]{1,6})\b\s*[:.\-]?\s*/i, (_, __, n) => `Chủ đề ${n}: `);
  t = t.replace(/^(BÀI MỞ ĐẦU|Bài mở đầu)\s*[:.\-]?\s*/i, 'Bài mở đầu');
  t = t.replace(/^(Mục)\s+(\d+)\s*[:.\-]?\s*/i, 'Mục $2: ');
  t = t.replace(/^(\d+)\s+(?=[A-Za-zÀ-ỹ])/, '$1. ');
  if (/^Bài\s+\d/i.test(t) || /^Chương\s/i.test(t) || /^Chủ đề\s/i.test(t)) {
    const i = t.indexOf(':');
    if (i > 0) t = t.slice(0, i + 1) + ' ' + lightTitleCase(t.slice(i + 1).trim());
  } else if (/^UNIT\s+/i.test(t) || isMostlyUpper(t)) {
    t = lightTitleCase(t);
    t = t.replace(/^(Unit)\s+(\d+)\s*[:.\-]?\s*/i, 'Unit $2: ');
  }
  return collapseSpace(t).replace(/\s+:/g, ':');
}

function isChapterLine(text, indented) {
  if (indented) return false;
  return /^(CHƯƠNG|Chương|CHỦ ĐỀ|Chủ đề|BÀI HỌC|Bài học|PHẦN|Phần|MODULE|Module|Mô đun)\b/i.test(text);
}

function isLessonLine(text) {
  return /^(Bài\s+\d|Unit\s+\d|Review\s+\d|Starter unit|Ôn tập|Luyện tập|Bài tập cuối|Progress review|Looking back|CHƯƠNG\s|Chương\s|CHỦ ĐỀ\s|Chủ đề\s|BÀI MỞ ĐẦU|Bài mở đầu|Hát\s*:|Nghe nhạc\s*:|Thường thức|Đọc nhạc\s*:|Lý thuyết|Nhạc cụ\s*:|Vận dụng|Mục\s+\d)/i.test(
    text
  ) || /^\d+\s+\S/.test(text);
}

function isNguvanSubskill(text) {
  return /^(Đọc|Viết|Việt|Nói và nghe|Củng cố|Thực hành đọc|Đọc mở rộng|Thực hành tiếng Việt)\b/i.test(text);
}

function isSkippableSub(text, indented) {
  if (FRONT_BACK_RE.test(text)) return true;
  if (/^phiếu học tập/i.test(text)) return true;
  if (isNguvanSubskill(text)) return true;
  if (indented && !isLessonLine(text) && !isChapterLine(text, false)) return true;
  return false;
}

function detectSubject(slug, title) {
  const s = `${slug} ${title}`.toLowerCase();
  const slugOnly = String(slug || '').toLowerCase();
  if (SKIP_SLUG_RE.test(slugOnly) || SKIP_TITLE_RE.test(title || '')) return null;
  if (/ngu-van|ngữ văn/.test(s)) return 'nguvan';
  if (/khoa-hoc-tu-nhien|khoa học tự nhiên/.test(s)) return 'khtn';
  if (/lich-su-va-dia|lịch sử và địa/.test(s)) return 'lichsudialy';
  if (/giao-duc-cong-dan|giáo dục công dân/.test(s)) return 'gdcd';
  if (/tin-hoc|tin học/.test(s)) return 'tinhoc';
  if (/cong-nghe|công nghệ/.test(s)) return 'congnghe';
  if (/am-nhac|âm nhạc/.test(s)) return 'amnhac';
  if (/mi-thuat|my-thuat|mĩ thuật|mỹ thuật/.test(s)) return 'mithuat';
  if (/giao-duc-the-chat|giáo dục thể chất/.test(s)) return 'gdtc';
  if (/hoat-dong-trai-nghiem|hoạt động trải nghiệm/.test(s)) return 'hdtn-hn';
  if (/tieng-anh|tiếng anh/.test(s)) return 'tienganh';
  if (/(^|[^a-z])toan([^a-z]|$)|toán/.test(s) && !/toan-roi/.test(s)) return 'toan';
  return null;
}

function detectTap(slug, title) {
  const s = `${slug} ${title}`.toLowerCase();
  if (/tap-hai|tập hai|tap-2|tập 2|tap2/.test(s)) return 'Tập 2';
  if (/tap-mot|tập một|tap-1|tập 1|tap1/.test(s)) return 'Tập 1';
  return '';
}

function isSgkTitle(title) {
  const t = String(title || '');
  if (SKIP_TITLE_RE.test(t)) return false;
  return true;
}

function looksOldCurriculum(html, slug) {
  const year = (html.match(/Năm xuất bản:\s*(\d{4})/i) || [])[1];
  const bookSet = stripTags((html.match(/Bộ sách:\s*([^<\n]+)/i) || [])[1] || '');
  const lower = bookSet.toLowerCase();
  if (/chân trời|cánh diều|cung hoc|cùng học/.test(lower)) return true;
  if (year && Number(year) <= 2019 && !/kết nối|ket noi/i.test(bookSet + html.slice(0, 4000))) return true;
  if (/ngu-van-9-tap-(mot|hai)$/.test(slug) && Number(year) <= 2020) return true;
  return false;
}

function isGlobalSuccessEnglish(html, slug, title) {
  const blob = `${slug} ${title} ${html.slice(0, 8000)}`.toLowerCase();
  return /global success|hoàng văn vân|my new school|unit 1 my new school/.test(blob);
}

function extractTocAnchors(html) {
  const h2 = html.search(/<h2[^>]*>\s*Mục lục\s*<\/h2>/i);
  if (h2 < 0) return [];
  const rest = html.slice(h2);
  const nextH2 = rest.slice(8).search(/<h2[\s>]/i);
  const block = nextH2 >= 0 ? rest.slice(0, nextH2 + 8) : rest.slice(0, 80000);
  const anchors = [];
  const re = /<a\b([^>]*)>([\s\S]*?)<\/a>/gi;
  let m;
  while ((m = re.exec(block))) {
    const attrs = m[1] || '';
    const inner = m[2] || '';
    const href = ((attrs.match(/href="([^"]+)"/i) || [])[1] || '').trim();
    if (!href || /\/open|\/download/.test(href)) continue;
    const indented = /&nbsp;|&#160;|\u00a0/.test(inner) || /^\s{2,}/.test(inner.replace(/<[^>]+>/g, ''));
    const text = stripTags(inner);
    if (text) anchors.push({ href, text, indented });
  }
  return anchors;
}

function tocFromAnchors(anchors, tapLabel, defaultChapter) {
  const chapters = [];
  let current = null;
  const ensure = (title) => {
    if (!current) {
      current = { chapter: normalizeChapter(title || defaultChapter || 'Bài học', tapLabel), items: [] };
      chapters.push(current);
    }
    return current;
  };
  const addItem = (text) => {
    ensure(defaultChapter);
    const item = normalizeItem(text);
    if (item && !current.items.includes(item)) current.items.push(item);
  };
  for (const a of anchors) {
    const text = collapseSpace(a.text);
    if (!text || FRONT_BACK_RE.test(text) || isNguvanSubskill(text) || /^phiếu học tập/i.test(text)) continue;
    if (isChapterLine(text, a.indented)) {
      current = { chapter: normalizeChapter(text, tapLabel), items: [] };
      chapters.push(current);
      continue;
    }
    if (a.indented && isLessonLine(text)) {
      addItem(text);
      continue;
    }
    if (!a.indented && isLessonLine(text)) {
      addItem(text);
    }
  }
  const filled = chapters.filter((ch) => ch.items.length);
  if (filled.length) return filled;
  const asItems = chapters.map((ch) => ch.chapter.replace(/\s*\(Tập [12]\)$/, '')).filter(Boolean);
  if (asItems.length) return [{ chapter: normalizeChapter(defaultChapter, tapLabel), items: asItems.map(normalizeItem) }];
  return [];
}

function parseTimdapanBook(html, slug, title) {
  const tap = detectTap(slug, title);
  const subject = detectSubject(slug, title);
  const defaultChapter = SUBJECT_NAMES[subject] || title || 'Bài học';
  const anchors = extractTocAnchors(html);
  let chapters = tocFromAnchors(anchors, tap, defaultChapter);
  if (!chapters.length) {
    const items = anchors
      .map((a) => collapseSpace(a.text))
      .filter((t) => t && !FRONT_BACK_RE.test(t) && isLessonLine(t))
      .map(normalizeItem);
    if (items.length) {
      chapters = [{ chapter: normalizeChapter(defaultChapter, tap), items }];
    }
  }
  return { subject, tap, chapters, itemCount: chapters.reduce((n, c) => n + c.items.length, 0) };
}

function parseListingBooks(html) {
  const found = [];
  const seen = new Set();
  const re = /<a\b[^>]*href="(\/sach-giao-khoa\/([^"\/?#]+))"[^>]*>([\s\S]*?)<\/a>/gi;
  let m;
  while ((m = re.exec(html))) {
    const slug = m[2];
    if (!slug || seen.has(slug)) continue;
    if (slug.startsWith('lop-')) continue;
    if (SKIP_SLUG_RE.test(slug)) continue;
    const inner = stripTags(m[3]);
    let title = inner;
    if (!title || title.length < 3) {
      const around = html.slice(Math.max(0, m.index - 80), m.index + m[0].length + 400);
      const h3 = around.match(/<h3[^>]*>([\s\S]*?)<\/h3>/i);
      const attr = (m[0].match(/title="([^"]+)"/i) || [])[1];
      title = stripTags((h3 && h3[1]) || attr || slug);
    }
    if (!isSgkTitle(title)) continue;
    const subject = detectSubject(slug, title);
    if (!subject) continue;
    seen.add(slug);
    found.push({ slug, title, subject, tap: detectTap(slug, title), url: `https://timdapan.com/sach-giao-khoa/${slug}` });
  }
  return found;
}

function cutLoigiaihayMain(html) {
  const start = html.search(/<h1[\s>]/i);
  const endMarkers = [/Các môn khác/i, /Danh sách bình luận/i, /Copyright/i];
  let end = html.length;
  for (const re of endMarkers) {
    const i = html.search(re);
    if (i > 0 && i < end && i > (start > 0 ? start : 0) + 200) end = i;
  }
  return html.slice(start > 0 ? start : 0, end);
}

function parseLoigiaihay(html, subjectId) {
  const main = cutLoigiaihayMain(html);
  const chapters = [];
  let current = null;
  const defaultChapter = SUBJECT_NAMES[subjectId] || 'Bài học';
  const pushChapter = (title, tapFromTitle) => {
    current = { chapter: normalizeChapter(title, tapFromTitle), items: [] };
    chapters.push(current);
  };
  const addItem = (text) => {
    const t = normalizeItem(text);
    if (!t || FRONT_BACK_RE.test(t) || /^phiếu học tập/i.test(t)) return;
    if (!current) pushChapter(defaultChapter);
    if (!current.items.includes(t)) current.items.push(t);
  };

  const headingRe = /<(h2|h3)[^>]*>([\s\S]*?)<\/\1>/gi;
  const liRe = /<li[^>]*>\s*(?:<[^>]+>\s*)*([^<]{3,220})/gi;

  const nodes = [];
  let hm;
  while ((hm = headingRe.exec(main))) {
    const text = stripTags(hm[2] || '');
    if (/^(Bài|Bài|Chương|Chủ đề|CHỦ ĐỀ|UNIT|Bài mở đầu|Mục)\b/i.test(text)) {
      nodes.push({ i: hm.index, type: 'h', text });
    }
  }
  let lm;
  while ((lm = liRe.exec(main))) {
    nodes.push({ i: lm.index, type: 'li', text: stripTags(lm[1]) });
  }
  nodes.sort((a, b) => a.i - b.i);

  let tapHint = '';
  if (/tập 1|tap 1|tập một/i.test(main.slice(0, 2500))) tapHint = 'Tập 1';
  for (const n of nodes) {
    const text = collapseSpace(n.text).replace(/^[•\-\d.]+\s*/, '');
    if (!text) continue;
    if (/các môn khác|bình luận|đề thi/i.test(text)) continue;
    if (/soạn văn 9 kết nối|tập 1|tập 2/i.test(text) && /^soạn|^giải/i.test(text)) {
      if (/tập 2/i.test(text)) tapHint = 'Tập 2';
      else if (/tập 1/i.test(text)) tapHint = 'Tập 1';
      continue;
    }
    if (n.type === 'h' && /^(Bài|Bài)\s+\d+/i.test(text) && subjectId === 'nguvan') {
      const m = text.match(/^(Bài|Bài)\s+(\d+)\s*[:.\-]?\s*(.*)$/i);
      const title = m ? `Bài ${m[2]}: ${m[3] || ''}`.trim() : text;
      if (!current || /tập 2/i.test(text) === false) {
        /* keep current tap */
      }
      if (!current || current._asNguvanItems) {
        if (!current) {
          pushChapter('Ngữ văn' + (tapHint ? '' : ''), tapHint);
          current._asNguvanItems = true;
        }
      }
      addItem(title);
      continue;
    }
    if (n.type === 'h' && isChapterLine(text, false)) {
      const tap = /tập 2/i.test(text) ? 'Tập 2' : /tập 1/i.test(text) ? 'Tập 1' : tapHint;
      pushChapter(text, tap);
      continue;
    }
    if (n.type === 'h' && /^(UNIT|Unit)\s+\d+/i.test(text)) {
      if (!current) pushChapter(defaultChapter, tapHint);
      addItem(text);
      continue;
    }
    if (n.type === 'h' && /^Bài mở đầu/i.test(text)) {
      pushChapter('Bài mở đầu', tapHint);
      continue;
    }
    if ((n.type === 'li' || n.type === 'h') && isLessonLine(text) && !isChapterLine(text, false)) addItem(text);
    else if (n.type === 'li' && /^(Bài|Bài|Unit|Mục)\b/i.test(text)) addItem(text);
  }

  if (subjectId === 'nguvan') {
    const items = [];
    const re = /\*\*\s*(Bài|Bài)\s+(\d+)\s*[.:]\s*([^*<\n]+)/gi;
    const plain = stripTags(main);
    let mm;
    const blob = main;
    const hRe = /(?:Bài|Bài)\s+(\d+)\s*[.:]\s*([^<\n]{2,80})/g;
    while ((mm = hRe.exec(blob))) {
      const label = normalizeItem(`Bài ${mm[1]}: ${stripTags(mm[2])}`);
      if (!items.includes(label) && Number(mm[1]) <= 20) items.push(label);
    }
    if (items.length >= 5) {
      const tap1 = items.filter((x) => {
        const n = Number((x.match(/Bài\s+(\d+)/) || [])[1] || 0);
        return n > 0 && n <= 5;
      });
      const tap2 = items.filter((x) => {
        const n = Number((x.match(/Bài\s+(\d+)/) || [])[1] || 0);
        return n >= 6;
      });
      const out = [];
      if (tap1.length) out.push({ chapter: normalizeChapter('Ngữ văn', 'Tập 1'), items: tap1 });
      if (tap2.length) out.push({ chapter: normalizeChapter('Ngữ văn', 'Tập 2'), items: tap2 });
      if (out.length) return out;
    }
  }

  const cleaned = chapters
    .map((ch) => {
      const { _asNguvanItems, ...rest } = ch;
      return rest;
    })
    .filter((ch) => ch.items && ch.items.length);
  if (cleaned.length) return cleaned;

  const loose = [];
  let cur = null;
  const lines = stripTags(main.replace(/<\/li>/gi, '\n').replace(/<br\s*\/?>/gi, '\n')).split(/\n+/);
  for (let line of lines) {
    line = collapseSpace(line).replace(/^[•]+\s*/, '');
    if (!line || FRONT_BACK_RE.test(line) || /các môn khác|bình luận/i.test(line)) continue;
    if (isChapterLine(line, false)) {
      cur = { chapter: normalizeChapter(line), items: [] };
      loose.push(cur);
      continue;
    }
    if (isLessonLine(line)) {
      if (!cur) {
        cur = { chapter: normalizeChapter(defaultChapter), items: [] };
        loose.push(cur);
      }
      const item = normalizeItem(line);
      if (item && !cur.items.includes(item)) cur.items.push(item);
    }
  }
  return loose.filter((ch) => ch.items.length);
}

function bookScore(book, html) {
  let score = 0;
  if (/-2$/.test(book.slug)) score += 3;
  if (book.tap) score += 2;
  if (book.subject === 'tienganh') {
    if (isGlobalSuccessEnglish(html, book.slug, book.title)) score += 20;
    if (/tap-mot|tap-hai/.test(book.slug)) score += 5;
    if (book.slug === `tieng-anh-${book.grade}` && !/tap/.test(book.slug)) score -= 8;
  }
  const n = (html.match(/Bài\s+\d+/g) || []).length + (html.match(/UNIT\s+\d+/gi) || []).length;
  score += Math.min(8, n / 4);
  return score;
}

function mergeChapters(groups) {
  const out = [];
  for (const ch of groups) {
    const prev = out.find((c) => c.chapter.toLowerCase() === ch.chapter.toLowerCase());
    if (prev) {
      for (const it of ch.items) if (!prev.items.includes(it)) prev.items.push(it);
    } else {
      out.push({ chapter: ch.chapter, items: ch.items.slice() });
    }
  }
  return out;
}

function bookQuality(r) {
  const nCh = (r.chapters || []).length;
  return nCh * 5 + (r.itemCount || 0) + (r.score || 0) / 10;
}

function pickBooksForGrade(recs) {
  const alive = recs.filter((r) => r.itemCount > 0);
  const hasTap1 = alive.some((r) => r.tap === 'Tập 1');
  const hasTap2 = alive.some((r) => r.tap === 'Tập 2');
  let pool = alive;
  if (hasTap1 && hasTap2) pool = alive.filter((r) => r.tap === 'Tập 1' || r.tap === 'Tập 2');
  const best = new Map();
  for (const r of pool) {
    const k = r.tap || '__none__';
    const prev = best.get(k);
    if (!prev || bookQuality(r) > bookQuality(prev)) best.set(k, r);
  }
  return [...best.values()];
}

function splitTopicItems(chapters) {
  const out = [];
  for (const ch of chapters) {
    const topicIdx = [];
    ch.items.forEach((it, i) => {
      if (/^(Chủ đề|Chương)\s+\S/i.test(it)) topicIdx.push(i);
    });
    if (topicIdx.length < 2) {
      out.push(ch);
      continue;
    }
    if (topicIdx[0] > 0) out.push({ chapter: ch.chapter, items: ch.items.slice(0, topicIdx[0]) });
    for (let k = 0; k < topicIdx.length; k++) {
      const i = topicIdx[k];
      const next = k + 1 < topicIdx.length ? topicIdx[k + 1] : ch.items.length;
      const title = ch.items[i];
      const items = ch.items.slice(i + 1, next);
      out.push({ chapter: title, items: items.length ? items : [title] });
    }
  }
  return out.filter((c) => c.items && c.items.length);
}

async function main() {
  const logs = [];
  const missing = [];
  const bookRecords = [];
  const byKey = new Map();

  const log = (msg) => {
    console.log(msg);
    logs.push(msg);
  };

  for (const grade of GRADES) {
    const listingUrl = `https://timdapan.com/sach-giao-khoa/lop-${grade}?book_set=ket-noi-tri-thuc-voi-cuoc-song`;
    log(`Listing ${grade}: ${listingUrl}`);
    const listing = await cachedFetch(listingUrl);
    if (!listing.cached) await sleep(DELAY_MS);
    let books = listing.status === 200 ? parseListingBooks(listing.text) : [];
    log(`  found ${books.length} SGK candidates`);

    if (grade !== 'toan') {
      const enListing = await cachedFetch(
        `https://timdapan.com/sach-giao-khoa/lop-${grade}?book_set=tieng-anh`
      );
      if (!enListing.cached) await sleep(DELAY_MS);
      if (enListing.status === 200) {
        const enBooks = parseListingBooks(enListing.text).filter((b) => b.subject === 'tienganh');
        books = books.concat(enBooks);
        log(`  english listing: ${enBooks.length}`);
      }
    }

    for (const slug of EXTRA_SLUGS[grade] || []) {
      if (!books.some((b) => b.slug === slug)) {
        books.push({
          slug,
          title: slug,
          subject: detectSubject(slug, slug),
          tap: detectTap(slug, slug),
          url: `https://timdapan.com/sach-giao-khoa/${slug}`,
        });
      }
    }
    books = books.filter((b) => b.subject);

    const fetched = [];
    for (const book of books) {
      book.grade = grade;
      log(`  fetch ${book.slug}`);
      const page = await cachedFetch(book.url);
      if (!page.cached) await sleep(DELAY_MS);
      if (page.status !== 200 || !page.text || /doesn't exist \(404\)/i.test(page.text)) {
        log(`    skip ${book.slug} status=${page.status || 'empty'}`);
        continue;
      }
      if (book.subject !== 'tienganh' && looksOldCurriculum(page.text, book.slug)) {
        log(`    skip old curriculum ${book.slug}`);
        continue;
      }
      if (book.subject === 'tienganh' && !isGlobalSuccessEnglish(page.text, book.slug, book.title)) {
        if (!/tap-mot|tap-hai|global-success/.test(book.slug)) {
          log(`    skip non-GS english ${book.slug}`);
          continue;
        }
      }
      const parsed = parseTimdapanBook(page.text, book.slug, book.title);
      if (!parsed.subject) continue;
      const rec = {
        ...book,
        subject: parsed.subject,
        tap: parsed.tap || book.tap,
        chapters: parsed.chapters,
        itemCount: parsed.itemCount,
        score: bookScore({ ...book, grade }, page.text),
        source: book.url,
      };
      fetched.push(rec);
      log(`    ${rec.subject} ${grade} ${rec.tap || ''} items=${rec.itemCount} score=${rec.score}`);
    }

    const best = new Map();
    for (const rec of fetched) {
      if (!rec.itemCount) continue;
      const k = `${rec.subject}|${grade}|${rec.tap || rec.slug}`;
      const prev = best.get(k);
      if (!prev || rec.score > prev.score || rec.itemCount > prev.itemCount) best.set(k, rec);
    }
    for (const rec of best.values()) {
      bookRecords.push(rec);
      const key = `${rec.subject}|${grade}`;
      if (!byKey.has(key)) byKey.set(key, []);
      byKey.get(key).push(rec);
    }
  }

  for (const grade of GRADES) {
    for (const subject of SUBJECTS) {
      if (subject === 'toan') continue;
      const key = `${subject}|${grade}`;
      const have = (byKey.get(key) || []).reduce((n, r) => n + r.itemCount, 0);
      const wantFallback =
        have < 8 ||
        (subject === 'congnghe' && grade === '9' && have < 20) ||
        (subject === 'hdtn-hn' && have < 10);
      if (!wantFallback) continue;
      const url = (LOIGIAIHAY_FALLBACK[grade] || {})[subject];
      if (!url) {
        if (have === 0) missing.push(`${subject} ${grade}`);
        continue;
      }
      log(`Fallback loigiaihay ${subject} ${grade}: ${url}`);
      const page = await cachedFetch(url);
      if (!page.cached) await sleep(DELAY_MS);
      if (page.status !== 200 || !page.text) {
        log(`  fallback fail status=${page.status}`);
        if (have === 0) missing.push(`${subject} ${grade}`);
        continue;
      }
      if (!/kết nối tri thức|ket noi tri thuc|global success/i.test(page.text)) {
        log(`  fallback page does not confirm book set`);
        if (have === 0) missing.push(`${subject} ${grade}`);
        continue;
      }
      const chapters = parseLoigiaihay(page.text, subject);
      const itemCount = chapters.reduce((n, c) => n + c.items.length, 0);
      log(`  fallback items=${itemCount} chapters=${chapters.length}`);
      if (!itemCount) {
        if (have === 0) missing.push(`${subject} ${grade}`);
        continue;
      }
      const rec = {
        slug: url,
        title: SUBJECT_NAMES[subject],
        subject,
        grade,
        tap: '',
        chapters,
        itemCount,
        score: 10,
        source: url,
      };
      bookRecords.push(rec);
      if (!byKey.has(key)) byKey.set(key, []);
      byKey.get(key).push(rec);
    }
  }

  const lessonsBySubject = {};
  for (const subject of SUBJECTS) {
    lessonsBySubject[subject] = {};
    for (const grade of GRADES) {
      const recs = (byKey.get(`${subject}|${grade}`) || []).slice();
      const unique = pickBooksForGrade(recs);
      unique.sort((a, b) => {
        const ta = a.tap === 'Tập 1' ? 1 : a.tap === 'Tập 2' ? 2 : 3;
        const tb = b.tap === 'Tập 1' ? 1 : b.tap === 'Tập 2' ? 2 : 3;
        return ta - tb || b.itemCount - a.itemCount;
      });
      const merged = splitTopicItems(mergeChapters(unique.flatMap((r) => r.chapters || [])));
      lessonsBySubject[subject][grade] = merged;
      const nChap = merged.length;
      const nItem = merged.reduce((n, c) => n + c.items.length, 0);
      log(`SUMMARY ${subject} ${grade}: ${nChap} chương, ${nItem} bài`);
      if (subject !== 'toan' && nItem === 0) {
        if (!missing.includes(`${subject} ${grade}`)) missing.push(`${subject} ${grade}`);
      }
    }
  }

  const out = {
    generatedAt: new Date().toISOString().slice(0, 10),
    catalogVersion: new Date().toISOString().slice(0, 10),
    sourceUrl: 'https://taphuan.nxbgd.vn/tap-huan/doc-sach/',
    missing,
    lessonsBySubject,
    books: bookRecords.map((r) => ({
      slug: r.slug,
      subject: r.subject,
      grade: r.grade,
      tap: r.tap,
      itemCount: r.itemCount,
      source: r.source,
    })),
  };
  fs.writeFileSync(OUT_PATH, JSON.stringify(out, null, 2), 'utf8');
  log(`Wrote ${OUT_PATH}`);
  if (missing.length) log(`MISSING: ${missing.join(', ')}`);
  else log('MISSING: (none)');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
