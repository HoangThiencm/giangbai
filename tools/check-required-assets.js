"use strict";

const fs = require("fs");
const path = require("path");

const required = [
  "js/khbd-curriculum.js",
  "js/khbd-standards.js",
  "js/khbd-yccd.js",
  "ai-design-config.js"
];

const root = process.cwd();
const invalid = required.filter((rel) => {
  try { return fs.statSync(path.join(root, rel)).size === 0; }
  catch (_) { return true; }
});

if (invalid.length) {
  throw new Error("Required Canvas assets missing or zero-byte: " + invalid.join(", "));
}

console.log("required-assets-integrity: OK (" + required.join(", ") + ")");
