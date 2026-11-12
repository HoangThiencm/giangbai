# -*- coding: utf-8 -*-
import sys, re

ENGINE_PATH = r"c:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\engine\export_khbd_engine.js"

with open(ENGINE_PATH, 'r', encoding='utf-8') as f:
    text = f.read()

replacement = """function formatKhbdRoleLine(line) {
  let content = String(line || "").replace(/<br\\s*\\/?>/gi, "<br>");
  const isTable = /^\\s*\\|/.test(content);
  content = content.replace(/(?:<br>\\s*)?-\\s*\\*\\*(GV|HS):\\*\\*/gi, (_, role) => `§BR§§${role.toUpperCase()}§`);
  if (!isTable) {
    content = content.replace(/\\s*\\|\\s*(?:\\*\\*)?(GV|HS)\\s*:(?:\\*\\*)?/gi, (_, role) => `§BR§§${role.toUpperCase()}§`);
  }
  // Chi chuan hoa vai GV/HS khi o dau dong hoac ngay sau <br>
  content = content.replace(/(?:^|<br>)\\s*(?:-\\s*)?(?:\\*\\*)?(GV|HS)\\s*:(?:\\*\\*)?/gi, (_, role) => `§BR§§${role.toUpperCase()}§`);
  content = content.replace(/§BR§/g, "<br>- ");
  content = content.replace(/§GV§/g, "**GV:**");
  content = content.replace(/§HS§/g, "**HS:**");
  content = content.replace(/^(\\s*)(?:<br>)+/, "$1");
  if (isTable) content = content.replace(/(\\|\\s*)(?:<br>)+/g, "$1");
  return content;
}"""

pattern = r'function formatKhbdRoleLine\(line\)\s*\{[\s\S]+?return content;\s*\}'
new_text, count = re.subn(pattern, lambda m: replacement, text)

if count > 0:
    with open(ENGINE_PATH, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("SUCCESS: Patched formatKhbdRoleLine successfully.")
else:
    print("FAIL: Pattern not found.")
