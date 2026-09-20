"use strict";

const assert = require("assert");
const childProcess = require("child_process");
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const root = path.resolve(__dirname, "..");
const pages = [
  "canvas_soankhbd.html",
  path.join("backupcode viettailieu", "canvas_soankhbd.html")
];
const version = "20260916-textbook-exact-v18";

function read(rel) {
  return fs.readFileSync(path.join(root, rel), "utf8");
}

// Required asset guard must validate both files that supply and consume PROMPTS.
const requiredAssetsOutput = childProcess.execFileSync(
  process.execPath,
  [path.join(root, "tools", "check-required-assets.js")],
  { cwd: root, encoding: "utf8" }
);
assert.match(requiredAssetsOutput, /js\/khbd-prompts\.js/, "asset guard checks khbd-prompts.js");
assert.match(requiredAssetsOutput, /js\/khbd-app\.js/, "asset guard checks khbd-app.js");

const promptsSource = read("js/khbd-prompts.js");
assert.match(promptsSource, /window\.PROMPTS\s*=\s*PROMPTS/, "prompt module exports PROMPTS to window");
assert.match(promptsSource, /globalThis\.PROMPTS\s*=\s*PROMPTS/, "prompt module exports PROMPTS to globalThis");

// Execute only the defensive helpers with no lexical PROMPTS binding present.
const appSource = read("js/khbd-app.js");
const helpersStart = appSource.indexOf("function getSafePrompts()");
const helpersEnd = appSource.indexOf("function getGenerationPromptContext", helpersStart);
assert.ok(helpersStart >= 0 && helpersEnd > helpersStart, "pedagogical prompt helpers are present");
const helpersSource = appSource.slice(helpersStart, helpersEnd);
const sandbox = {
  window: {
    PROMPTS: {
      OUTPUT_CONTRACT: "WINDOW CONTRACT",
      ENGLISH_ELT_DIRECTIVE: "ENGLISH DIRECTIVE"
    }
  },
  appState: { selectedSubject: "toan" }
};
vm.createContext(sandbox);
vm.runInContext(helpersSource, sandbox);
assert.strictEqual(
  sandbox.buildPedagogicalPrompt("Prompt"),
  "Prompt\n\nWINDOW CONTRACT",
  "window fallback works when lexical PROMPTS is absent"
);

delete sandbox.window.PROMPTS;
sandbox.window.__KHBD_DEFAULT_OUTPUT_CONTRACT = "DEFAULT CONTRACT";
assert.strictEqual(
  sandbox.buildPedagogicalPrompt("Prompt"),
  "Prompt\n\nDEFAULT CONTRACT",
  "default contract works when all PROMPTS exports are absent"
);

for (const rel of pages) {
  const html = read(rel);
  assert.match(html, new RegExp("khbd-prompts\\.js\\?v=" + version), rel + " cache-busts prompt module");
  assert.match(html, new RegExp("khbd-app\\.js\\?v=" + version), rel + " cache-busts app module");
  assert.match(html, /typeof window\.PROMPTS === "undefined"/, rel + " has PROMPTS fallback guard");
  assert.match(html, /OUTPUT_CONTRACT:/, rel + " supplies OUTPUT_CONTRACT fallback");
  assert.match(html, /ENGLISH_ELT_DIRECTIVE:/, rel + " supplies English directive fallback");
  assert.match(html, /ensureKhbdPromptsFallback/, rel + " has ensureKhbdPromptsFallback CDN rescue");
  assert.match(html, /cdn\.jsdelivr\.net\/gh\/HoangThiencm\/giangbai@main\/js\/khbd-prompts\.js/, rel + " prompts fallback uses jsDelivr CDN");
  assert.match(html, /window\.PROMPTS\.GENERATE_OBJECTIVES/, rel + " prompts fallback guards GENERATE_OBJECTIVES");
}

assert.match(promptsSource, /GENERATE_OBJECTIVES:\s*`/, "PROMPTS defines GENERATE_OBJECTIVES template");
assert.match(promptsSource, /### a\) Năng lực chung/, "GENERATE_OBJECTIVES has ### a) Năng lực chung");
assert.match(promptsSource, /### b\) Năng lực đặc thù môn học/, "GENERATE_OBJECTIVES has ### b) Năng lực đặc thù môn học");
assert.match(promptsSource, /\{digital_objectives_section\}/, "GENERATE_OBJECTIVES has {digital_objectives_section}");
assert.match(promptsSource, /\{ai_objectives_section\}/, "GENERATE_OBJECTIVES has {ai_objectives_section}");

assert.match(appSource, /hasCommonCompetency/, "isOffTopicObjectivesHallucination checks Năng lực chung");
assert.match(appSource, /hasSubjectCompetency/, "isOffTopicObjectivesHallucination checks Năng lực đặc thù");
assert.match(appSource, /isIntegrationBadgeListItem/, "preview strips orphan dash before NLS/AI badge li");

console.log("canvas-prompts-integrity-smoke: OK");
