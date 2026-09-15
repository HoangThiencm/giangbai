/** Node 18+ smoke tests for Gemini 503/429 retry, backoff, and model fallback. */
"use strict";

function createLocalStorage() {
  const store = {};
  return {
    getItem(key) {
      return Object.prototype.hasOwnProperty.call(store, key) ? store[key] : null;
    },
    setItem(key, value) {
      store[key] = String(value);
    },
    removeItem(key) {
      delete store[key];
    }
  };
}

global.localStorage = createLocalStorage();
localStorage.setItem("khbd_user_gemini_keys_default", JSON.stringify(["AIzaSyTESTKEY1234567890"]));

const { GeminiAPIManager } = require("../js/khbd-gemini.js");

function okResponse(text = "Nội dung Gemini hợp lệ cho bài học.") {
  return {
    ok: true,
    status: 200,
    statusText: "OK",
    headers: { get: () => null },
    json: async () => ({ candidates: [{ content: { parts: [{ text }] } }] })
  };
}

function errResponse(status, message, headerMap = {}) {
  return {
    ok: false,
    status,
    statusText: "Error",
    headers: {
      get(name) {
        const key = String(name || "");
        return headerMap[key] || headerMap[key.toLowerCase()] || null;
      }
    },
    json: async () => ({ error: { message } })
  };
}

function emptyOkResponse(payload) {
  return {
    ok: true,
    status: 200,
    statusText: "OK",
    headers: { get: () => null },
    json: async () => payload
  };
}

function makeApi() {
  const api = new GeminiAPIManager();
  api.selectedModel = "gemini-3.7-flash";
  api.apiKeys = ["AIzaSyTESTKEY1234567890"];
  api.currentKeyIndex = 0;
  api._lastRequestEndedAt = 0;
  api.onStatusCallback = null;
  return api;
}

function modelFromUrl(url) {
  const match = String(url).match(/models\/([^:]+):generateContent/);
  return match ? match[1] : "";
}

let failed = 0;

function assert(cond, msg) {
  if (!cond) {
    failed += 1;
    console.error("FAIL:", msg);
  } else {
    console.log("OK:", msg);
  }
}

async function case1_retry503then200() {
  const api = makeApi();
  const calls = [];
  global.fetch = async (url) => {
    calls.push({ url, at: Date.now() });
    if (calls.length === 1) {
      return errResponse(503, "The model is overloaded. Please try again later. high demand");
    }
    return okResponse("OK after 503");
  };
  const text = await api.generateContent("prompt", [], null, 0.3, null, { _testFastRetry: true });
  assert(text === "OK after 503", "case1: generateContent succeeds after one 503");
  assert(calls.length === 2, `case1: two fetches (got ${calls.length})`);
}

async function case2_retry429then200() {
  const api = makeApi();
  const calls = [];
  const waits = [];
  api.waitForRetry = async (ms) => {
    waits.push(ms);
  };
  global.fetch = async (url) => {
    calls.push({ url, at: Date.now() });
    if (calls.length === 1) {
      return errResponse(429, "Resource exhausted. Please retry in 2s");
    }
    return okResponse("OK after 429");
  };
  const text = await api.generateContent("prompt");
  assert(text === "OK after 429", "case2: generateContent succeeds after 429");
  assert(calls.length === 2, `case2: two fetches (got ${calls.length})`);
  const retryWait = waits.find(ms => ms >= 1000);
  assert(Boolean(retryWait), `case2: waitForRetry >= 1s from 'retry in 2s' (waits=${JSON.stringify(waits)})`);
  assert(retryWait >= 2000 && retryWait <= 25000, `case2: parsed retry wait in range (got ${retryWait})`);
}

async function case3_fallbackModelOn503() {
  localStorage.setItem("default_gemini_fallback", "gemini-custom-fallback");
  const api = makeApi();
  const calls = [];
  global.fetch = async (url) => {
    calls.push({ url, at: Date.now() });
    if (calls.length === 1) {
      return errResponse(503, "The model is overloaded. Please try again later.");
    }
    return okResponse("OK on fallback model");
  };
  const text = await api.generateContent("prompt", [], null, 0.3, null, { _testFastRetry: true });
  assert(text === "OK on fallback model", "case3: succeeds after model fallback");
  assert(modelFromUrl(calls[0]?.url) === "gemini-3.7-flash", `case3: first URL uses selected model (got ${modelFromUrl(calls[0]?.url)})`);
  assert(modelFromUrl(calls[1]?.url) === "gemini-custom-fallback", `case3: second URL uses configured custom fallback (got ${modelFromUrl(calls[1]?.url)})`);
  assert(api.selectedModel === "gemini-3.7-flash", "case3: does not overwrite selectedModel");
  assert(localStorage.getItem("khbd_gemini_model") == null, "case3: does not write khbd_gemini_model");
}

async function case4_sameFallbackDoesNotSwitchModels() {
  localStorage.setItem("default_gemini_fallback", "gemini-3.7-flash");
  const api = makeApi();
  const calls = [];
  global.fetch = async (url) => {
    calls.push({ url, at: Date.now() });
    if (calls.length === 1) return errResponse(503, "The model is overloaded. Please try again later.");
    return okResponse("OK after retrying the same model");
  };
  const text = await api.generateContent("prompt", [], null, 0.3, null, { _testFastRetry: true });
  assert(text === "OK after retrying the same model", "case4: retries without a duplicate fallback model");
  assert(calls.every(call => modelFromUrl(call.url) === "gemini-3.7-flash"), "case4: fallback equal to primary never calls a second model");
}

async function case5_400noRetry() {
  localStorage.setItem("default_gemini_fallback", "gemini-2.5-flash");
  const api = makeApi();
  const calls = [];
  global.fetch = async (url) => {
    calls.push({ url, at: Date.now() });
    return errResponse(400, "Invalid argument: bad request");
  };
  let thrown = null;
  try {
    await api.generateContent("prompt", [], null, 0.3, null, { _testFastRetry: true });
  } catch (err) {
    thrown = err;
  }
  assert(Boolean(thrown), "case5: 400 throws");
  assert(/400/.test(String(thrown && thrown.message)), `case5: error mentions 400 (got ${thrown && thrown.message})`);
  assert(calls.length === 1, `case5: no retry on 400 (got ${calls.length} fetches)`);
}

async function case6_textAcrossCandidatesAndParts() {
  const api = makeApi();
  let calls = 0;
  global.fetch = async () => {
    calls += 1;
    return emptyOkResponse({
      candidates: [
        { content: { parts: [{ text: "Phần một " }] } },
        { content: { parts: [{ text: "phần hai" }] } }
      ]
    });
  };
  const text = await api.generateContent("prompt", [], null, 0.3, null, { _testFastRetry: true });
  assert(text === "Phần một phần hai", "case6: joins text across candidate parts");
  assert(calls === 1, `case6: text response makes one fetch (got ${calls})`);
}

async function case7_empty200DoesNotRetry() {
  const api = makeApi();
  let calls = 0;
  global.fetch = async () => {
    calls += 1;
    return emptyOkResponse({ candidates: [{ finishReason: "SAFETY", content: { parts: [] }, safetyRatings: [{ blocked: true }] }] });
  };
  let thrown = null;
  try { await api.generateContent("prompt", [], null, 0.3, null, { _testFastRetry: true }); } catch (err) { thrown = err; }
  assert(Boolean(thrown), "case7: empty 200 throws a diagnostic");
  assert(/finishReason=SAFETY/.test(String(thrown && thrown.message)), `case7: diagnostic includes finish reason (got ${thrown && thrown.message})`);
  assert(/safety=blocked/.test(String(thrown && thrown.message)), `case7: diagnostic includes safety state (got ${thrown && thrown.message})`);
  assert(calls === 1, `case7: empty/safety 200 does not retry or fall back (got ${calls})`);
}

async function case8_nonCanvasWithoutKeyKeepsGuard() {
  const api = makeApi();
  api.apiKeys = [];
  api.loadKeysFromLocalStorage = function () { this.apiKeys = []; };
  delete global.window;
  let calls = 0;
  global.fetch = async () => { calls += 1; return okResponse("không được gọi"); };
  let thrown = null;
  try { await api.generateContent("prompt", [], null, 0.3, null, { _testFastRetry: true }); } catch (err) { thrown = err; }
  assert(/chưa cấu hình Gemini API Key cá nhân/.test(String(thrown && thrown.message)), "case8: non-Canvas without key keeps the personal-key guard");
  assert(calls === 0, `case8: guard makes no request (got ${calls})`);
}

async function case9_canvasWithoutKeyUsesSystemEndpointOnce() {
  const api = makeApi();
  api.apiKeys = [];
  api.loadKeysFromLocalStorage = function () { this.apiKeys = []; };
  global.window = { __KHBD_CANVAS__: {
    systemGemini: true,
    geminiEndpoint: "https://hoangthiencm.id.vn/api/canvas_gemini.php",
    model: "gemini-3-flash-preview"
  } };
  const calls = [];
  global.fetch = async (url, init) => {
    calls.push({ url, init });
    return {
      ok: true, status: 200, statusText: "OK", headers: { get: () => null },
      json: async () => ({ ok: true, meta: { route: "system", model: "gemini-3-flash-preview" }, body: { candidates: [{ content: { parts: [{ text: "OCR Canvas hợp lệ" }] } }] } })
    };
  };
  const text = await api.generateContent("OCR SGK", [{ mimeType: "image/jpeg", base64: "aGVsbG8=" }], null, 0.3, null, { _testFastRetry: true });
  const sent = JSON.parse(calls[0].init.body);
  assert(text === "OCR Canvas hợp lệ", "case9: Canvas gets text from the system envelope");
  assert(calls.length === 1, `case9: Canvas OCR calls proxy exactly once (got ${calls.length})`);
  assert(calls[0].url === "https://hoangthiencm.id.vn/api/canvas_gemini.php", "case9: Canvas uses only the configured proxy endpoint");
  assert(JSON.stringify(Object.keys(sent).sort()) === JSON.stringify(["payload", "preferred_model", "timeout"]), "case9: endpoint payload contains no key or client identity");
  assert(sent.preferred_model === "gemini-3-flash-preview", "case9: Canvas sends its configured model");
  delete global.window;
}

(async () => {
  try {
    await case1_retry503then200();
    await case2_retry429then200();
    await case3_fallbackModelOn503();
    await case4_sameFallbackDoesNotSwitchModels();
    await case5_400noRetry();
    await case6_textAcrossCandidatesAndParts();
    await case7_empty200DoesNotRetry();
    await case8_nonCanvasWithoutKeyKeepsGuard();
    await case9_canvasWithoutKeyUsesSystemEndpointOnce();
  } catch (err) {
    failed += 1;
    console.error("FAIL: uncaught", err);
  }
  if (failed) {
    console.error(`\n${failed} assertion(s) failed.`);
    process.exit(1);
  }
  console.log("\nAll khbd-gemini retry smoke tests passed.");
})();
