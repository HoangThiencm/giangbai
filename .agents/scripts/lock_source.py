#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ALLOW = {"decision": "allow"}
DENY = {
    "decision": "deny",
    "reason": "PLAN.md da xong. IDE bi khoa ghi source. Mo Coder (Grok / ChatGPT / agy) hoac chat moi /verify.",
}

payload = json.loads(sys.stdin.read() or "{}")
tool = payload.get("toolCall") or payload
name = str(tool.get("name") or payload.get("tool_name") or "").lower()
args = tool.get("args") or payload.get("tool_input") or {}
blob = json.dumps(args, ensure_ascii=False).lower()

roots = payload.get("workspacePaths") or [Path.cwd()]
root = Path(roots[0])
lock = root / "docs" / "handoff" / ".lock"

if not lock.exists():
    print(json.dumps(ALLOW))
    sys.exit(0)

handoff_ok = "docs/handoff/" in blob or "docs\\handoff\\" in blob
if handoff_ok:
    print(json.dumps(ALLOW))
    sys.exit(0)

if "write" in name or "replace" in name:
    print(json.dumps(DENY))
    sys.exit(0)

cmd = str(args.get("command") or args.get("Command") or "")
if cmd and any(x in cmd for x in [">", "rm ", "mv ", "sed -i", "mkdir", "touch ", "chmod", "git commit", "git push"]):
    print(json.dumps(DENY))
    sys.exit(0)

print(json.dumps(ALLOW))
