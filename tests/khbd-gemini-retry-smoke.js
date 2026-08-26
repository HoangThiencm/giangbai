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
  assert(modelFromUrl(calls[1]?.url) === "gemini-2.5-flash", `case3: second URL uses gemini-2.5-flash (got ${modelFromUrl(calls[1]?.url)})`);
  assert(api.selectedModel === "gemini-3.7-flash", "case3: does not overwrite selectedModel");
  assert(localStorage.getItem("khbd_gemini_model") == null, "case3: does not write khbd_gemini_model");
}

async function case4_400noRetry() {
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
  assert(Boolean(thrown), "case4: 400 throws");
  assert(/400/.test(String(thrown && thrown.message)), `case4: error mentions 400 (got ${thrown && thrown.message})`);
  assert(calls.length === 1, `case4: no retry on 400 (got ${calls.length} fetches)`);
}

(async () => {
  try {
    await case1_retry503then200();
    await case2_retry429then200();
    await case3_fallbackModelOn503();
    await case4_400noRetry();
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
