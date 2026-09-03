const assert = require("assert");
const {
  isEnglishSubject,
  getSystemRole,
  getPromptTemplate,
  PROMPTS
} = require("../js/khbd-prompts.js");

assert.strictEqual(isEnglishSubject("tienganh"), true);
assert.strictEqual(isEnglishSubject("Tiếng Anh"), true);
assert.strictEqual(isEnglishSubject("english"), true);
assert.strictEqual(isEnglishSubject("toan"), false);
assert.strictEqual(isEnglishSubject("nguvan"), false);

const enRole = getSystemRole("tienganh", 7);
assert.match(enRole, /English-medium|Write the COMPLETE lesson plan in English/i);
assert.match(enRole, /Warm-up/);
assert.match(enRole, /Knowledge Formation/);
assert.match(enRole, /Teacher says/);
assert.doesNotMatch(enRole, /Sử dụng tiếng Việt chuẩn mực/);

const viRole = getSystemRole("toan", 7);
assert.match(viRole, /Chuyên gia Sư phạm/);
assert.doesNotMatch(viRole, /English-medium ELT/);

const ctx = {
  subject: "tienganh",
  subjectName: "Tiếng Anh",
  grade: "7",
  gradeLevelName: "THCS",
  topic: "Unit 1. Hobbies",
  duration: "02 tiết (90 phút)",
  textbook_content: "Listen and read. Vocabulary: hobby, football."
};

const objectives = getPromptTemplate("GENERATE_OBJECTIVES", ctx);
assert.match(objectives, /ENGLISH-MEDIUM ELT LESSON PLAN OVERRIDE/);
assert.match(objectives, /# I\. Objectives/);
assert.match(objectives, /Activity 1: Warm-up \/ Lead-in/);
assert.match(objectives, /Activity 2: Knowledge Formation/);
assert.match(objectives, /Activity 3: Practice/);
assert.match(objectives, /Activity 4: Application/);
assert.match(objectives, /Teacher says:/);

const materials = getPromptTemplate("GENERATE_MATERIALS", ctx);
assert.match(materials, /Teaching aids & Learning materials/);

const actA = getPromptTemplate("GENERATE_ACTIVITY_A", ctx);
assert.match(actA, /Warm-up \/ Lead-in/);
assert.match(actA, /100% English/);

const mathObj = getPromptTemplate("GENERATE_OBJECTIVES", {
  subject: "toan",
  subjectName: "Toán",
  grade: "7",
  topic: "Tam giác",
  duration: "01 tiết (45 phút)"
});
assert.doesNotMatch(mathObj, /ENGLISH-MEDIUM ELT LESSON PLAN OVERRIDE/);

assert.ok(PROMPTS.ENGLISH_ELT_DIRECTIVE.includes("100% English"));
assert.ok(PROMPTS.SYSTEM_ROLE.includes("Sử dụng tiếng Việt chuẩn mực"));

console.log("khbd english lesson smoke: passed");
