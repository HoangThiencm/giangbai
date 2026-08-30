'use strict';

const assert = require('assert');

class TextNode {
  constructor(text) { this.nodeType = 3; this.textContent = text; this.childNodes = []; }
}
class Element {
  constructor(tagName) { this.nodeType = 1; this.tagName = tagName.toUpperCase(); this.attrs = {}; this.childNodes = []; }
  appendChild(node) { this.childNodes.push(node); return node; }
  getAttribute(name) { return this.attrs[name] || null; }
  hasAttribute(name) { return Object.prototype.hasOwnProperty.call(this.attrs, name); }
  setAttribute(name, value) { this.attrs[name] = String(value); }
  get textContent() { return this.childNodes.map(node => node.textContent).join(''); }
}
class Fragment {
  constructor() { this.childNodes = []; }
  appendChild(node) { this.childNodes.push(node); return node; }
}
function parseHtml(html) {
  const root = new Element('body');
  const stack = [root];
  String(html).split(/(<[^>]+>)/).filter(Boolean).forEach(token => {
    if (!token.startsWith('<')) return stack[stack.length - 1].appendChild(new TextNode(token));
    if (/^<\//.test(token)) return stack.pop();
    const match = token.match(/^<([a-z0-9]+)([^>]*)>/i);
    if (!match) return;
    const node = new Element(match[1]);
    match[2].replace(/([\w-]+)=(?:"([^"]*)"|'([^']*)'|([^\s>]+))/g, (_, name, a, b, c) => {
      node.setAttribute(name, a || b || c || '');
      return '';
    });
    stack[stack.length - 1].appendChild(node);
    if (!/\/$/.test(token) && !['br', 'img', 'hr'].includes(match[1].toLowerCase())) stack.push(node);
  });
  return root;
}

global.Node = { TEXT_NODE: 3, ELEMENT_NODE: 1 };
global.DOMParser = class { parseFromString(html) { return { body: parseHtml(html) }; } };
global.document = {
  addEventListener() {}, querySelectorAll() { return []; }, querySelector() { return null; }, getElementById() { return null; },
  createElement(tag) { return new Element(tag); }, createTextNode(text) { return new TextNode(text); }, createDocumentFragment() { return new Fragment(); }
};
global.window = { addEventListener() {}, document: global.document, localStorage: { getItem() { return null; }, setItem() {}, removeItem() {} } };
global.localStorage = global.window.localStorage;
global.geminiAPI = { apiKeys: [], syncKeysFromServer: async () => [] };

const { sanitizePreviewHtml } = require('../js/khbd-app.js');
const clean = sanitizePreviewHtml('<ol start="2" type="A"><li value="3" type="i">Ba</li></ol><ol start="3"><li>Bốn</li></ol><ol start="4"><li>Năm</li></ol><ul type="circle"><li>Sáu</li></ul>');
const [firstOl, secondOl, thirdOl, ul] = clean.childNodes;
assert.strictEqual(firstOl.getAttribute('start'), '2');
assert.strictEqual(secondOl.getAttribute('start'), '3');
assert.strictEqual(thirdOl.getAttribute('start'), '4');
assert.strictEqual(firstOl.getAttribute('type'), 'A');
assert.strictEqual(firstOl.childNodes[0].getAttribute('value'), '3');
assert.strictEqual(firstOl.childNodes[0].getAttribute('type'), 'i');
assert.strictEqual(ul.getAttribute('type'), 'circle');
console.log('khbd-list-numbering-smoke: passed');
