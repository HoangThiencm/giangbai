"use strict";

const assert = require("assert");
const fs = require("fs");
const path = require("path");

const source = fs.readFileSync(path.join(__dirname, "..", "api", "canvas_gemini.php"), "utf8");

assert.ok(source.includes("preferred_model"), "Canvas API accepts preferred_model");
assert.ok(source.includes("$body['model']"), "Canvas API remains compatible with model");
assert.ok(source.includes("'meta'"), "Canvas API returns safe route metadata");
assert.ok(source.includes("'body' => $attempt['body']"), "Canvas API preserves Gemini response body for diagnostics");
assert.ok(!source.includes("user_account"), "Canvas API does not trust client user_account");
assert.ok(!source.includes("HTTP_X_USER_ACCOUNT"), "Canvas API does not use client account headers");
assert.ok(source.includes("system_unavailable"), "Canvas API supports unauthenticated system route diagnostics");

console.log("Canvas Gemini API smoke test passed.");
