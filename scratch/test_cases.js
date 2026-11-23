const { loadDocx } = require('../TROLYTHIEN/engine/export_khbd_engine');
const docx = loadDocx();
global.window = { docx: docx };
const { DocxGenerator } = require('../js/khbd-docx.js');
const gen = new DocxGenerator();

// 1. Normalize with begin and end in supportedCommands
const origNorm = gen.normalizeLatexForMath.bind(gen);
gen.normalizeLatexForMath = function(latex) {
  let s = origNorm(latex);
  s = s.replace(/\\\\begin\b/g, '\\begin').replace(/\\\\end\b/g, '\\end');
  return s;
};

// 2. buildCasesDelimiter parses each row into native math nodes!
gen.buildCasesDelimiter = function(body, mathApi, begChr = '{') {
  if (body == null || typeof mathApi.XmlComponent !== 'function' || typeof mathApi.XmlAttributeComponent !== 'function') return null;
  const cleaned = String(body)
    .replace(/\\begin\s*\{array\}\s*\{[^}]*\}/gi, '')
    .replace(/\\end\s*\{array\}/gi, '');
  const rows = cleaned
    .split(/\\\\(?:\[[^\]]*\])?\s*/)
    .map(row => row.replace(/\s*&\s*/g, ' ').trim())
    .filter(Boolean);
  if (!rows.length) return null;

  const element = name => new mathApi.XmlComponent(name);
  const attribute = value => new mathApi.XmlAttributeComponent({ 'm:val': value });
  const delimiterProperties = element('m:dPr');
  const beginning = element('m:begChr');
  beginning.root.push(attribute(begChr));
  const ending = element('m:endChr');
  ending.root.push(attribute(''));
  delimiterProperties.root.push(beginning, ending);

  const equationArray = element('m:eqArr');
  for (const row of rows) {
    const equation = element('m:e');
    const rowMath = this.createNativeMath(row);
    if (rowMath && Array.isArray(rowMath.root) && rowMath.root.length) {
      for (const child of rowMath.root) {
        equation.root.push(child);
      }
    } else {
      equation.root.push(new mathApi.MathRun(this.latexToUnicodeMath(row)));
    }
    equationArray.root.push(equation);
  }
  const base = element('m:e');
  base.root.push(equationArray);
  const delimiter = element('m:d');
  delimiter.root.push(delimiterProperties, base);
  return delimiter;
};

// 3. createCasesMath only applies when there is a SINGLE cases environment
gen.createCasesMath = function(source, mathApi) {
  const matches = source.match(/\\begin\s*\{(?:cases|aligned)\}/gi);
  if (matches && matches.length > 1) return null;

  const casesMatch = source.match(/^([\s\S]*?)\\begin\s*\{(cases|aligned)\}([\s\S]*?)\\end\s*\{\2\}\s*$/i);
  const leftBraceMatch = source.match(/^([\s\S]*?)\\left\s*\\\{([\s\S]*?)\\right\s*\.\s*$/);
  const leftBracketMatch = source.match(/^([\s\S]*?)\\left\s*\[([\s\S]*?)\\right\s*\.\s*$/);
  let body = null;
  let prefix = "";
  let begChr = "{";
  if (casesMatch) {
    prefix = casesMatch[1] || "";
    body = casesMatch[3];
  } else if (leftBraceMatch) {
    prefix = leftBraceMatch[1] || "";
    body = leftBraceMatch[2];
  } else if (leftBracketMatch) {
    prefix = leftBracketMatch[1] || "";
    body = leftBracketMatch[2];
    begChr = "[";
  }
  if (!body) return null;
  if (/\\end\s*\{(?:cases|aligned)\}/i.test(body)) return null;

  const delimiter = this.buildCasesDelimiter(body, mathApi, begChr);
  if (!delimiter) return null;
  const children = [];
  prefix = prefix.trim();
  if (prefix) children.push(new mathApi.MathRun(this.latexToUnicodeMath(prefix) + " "));
  children.push(delimiter);
  return new mathApi.Math({ children });
};

const input = '$\\begin{cases} u + v = \\frac{1}{12} \\\\ 4u + 6v = \\frac{2}{5} \\end{cases} \\Rightarrow \\begin{cases} u = \\frac{1}{20} \\\\ v = \\frac{1}{30} \\end{cases}$';
const m = gen.createNativeMath(input);
console.log('Result rootKey:', m ? m.rootKey : null);
if (m) {
  console.log('Children rootKeys:', m.root.map(c => c ? c.rootKey : null));
}

function dumpAll(obj, indent = 0) {
  if (!obj || typeof obj !== 'object') return;
  if (obj.rootKey) {
    let extra = '';
    if (obj.rootKey === 'm:t') extra = ' -> ' + JSON.stringify(obj.root);
    console.log(' '.repeat(indent) + obj.rootKey + extra);
  }
  if (Array.isArray(obj.root)) {
    obj.root.forEach(c => dumpAll(c, indent + 2));
  }
}
console.log('--- DUMP ALL ---');
dumpAll(m);
