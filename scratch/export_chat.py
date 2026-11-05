import json
import re
from pathlib import Path
from datetime import datetime

transcript_path = Path(r"C:\Users\HoangThien\.gemini\antigravity\brain\b8e055e7-7ed9-4e60-b401-2fae6f8fd5d5\.system_generated\logs\transcript_full.jsonl")
output_md = Path(r"c:\Users\HoangThien\Documents\GitHub\giangbai\dich_truyen\ta_ba_xa_la_minh_tinh\nhat_ky_cuoc_tro_chuyen_antigravity.md")

entries = []
with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            entries.append(data)
        except Exception:
            pass

print(f"Total log entries: {len(entries)}")

# Tách thành các lượt tương tác (Conversation Turns)
turns = []
current_turn = None

for entry in entries:
    step_type = entry.get("type")
    source = entry.get("source")
    content = entry.get("content") or ""
    created_at = entry.get("created_at") or ""
    tool_calls = entry.get("tool_calls") or []

    # Bỏ qua system message tự sinh
    if step_type == "USER_INPUT":
        # Làm sạch nội dung user input nếu có bọc thẻ
        # Ví dụ <USER_REQUEST> ... </USER_REQUEST> hoặc <CONTEXT_SUMMARY>
        cleaned = content
        if "<CONTEXT_SUMMARY>" in cleaned:
            # Chỉ lấy phần sau tóm tắt nếu có
            pass
        
        current_turn = {
            "time": created_at,
            "user": content,
            "assistant_steps": []
        }
        turns.append(current_turn)
    elif step_type == "PLANNER_RESPONSE":
        if current_turn is None:
            current_turn = {
                "time": created_at,
                "user": "(Phiên làm việc tự động / tiếp nối)",
                "assistant_steps": []
            }
            turns.append(current_turn)
        
        # Nếu có tin nhắn text gửi cho user
        msg_text = content.strip() if content else ""
        tools_summary = []
        for tc in tool_calls:
            fname = tc.get("function", {}).get("name") if isinstance(tc, dict) else ""
            if not fname and isinstance(tc, dict) and "name" in tc:
                fname = tc.get("name")
            tools_summary.append(fname or "tool_call")

        current_turn["assistant_steps"].append({
            "time": created_at,
            "message": msg_text,
            "tools": tools_summary
        })

print(f"Total turns: {len(turns)}")

# Xuất ra file Markdown
with open(output_md, "w", encoding="utf-8") as out:
    out.write("# NHẬT KÝ TOÀN BỘ CUỘC TRÒ CHUYỆN ANTIGRAVITY\n\n")
    out.write(f"- **Dự án:** Tiểu thuyết 《Ta Bà Xã Là Minh Tinh》 (*我老婆是大明星*)\n")
    out.write(f"- **Conversation ID:** `b8e055e7-7ed9-4e60-b401-2fae6f8fd5d5`\n")
    out.write(f"- **Thời gian xuất file:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    out.write(f"- **Số lượt trao đổi:** {len(turns)} lượt tương tác\n\n")
    out.write("---\n\n")

    for i, turn in enumerate(turns, 1):
        user_text = turn["user"]
        # Format user text gọn gàng
        match_req = re.search(r"<USER_REQUEST>(.*?)</USER_REQUEST>", user_text, re.DOTALL)
        if match_req:
            display_user = match_req.group(1).strip()
        else:
            display_user = user_text.strip()

        out.write(f"## 👤 LƯỢT {i} — Người dùng ({turn['time']})\n\n")
        out.write(f"> {display_user.replace(chr(10), chr(10) + '> ')}\n\n")

        out.write(f"### 🤖 Phản hồi của Trợ lý Antigravity\n\n")
        
        # Lọc các tin nhắn của assistant
        final_msgs = []
        tools_used = []
        for step in turn["assistant_steps"]:
            if step["tools"]:
                tools_used.extend(step["tools"])
            if step["message"]:
                final_msgs.append(step["message"])

        if tools_used:
            out.write(f"*Các thao tác kỹ thuật đã thực hiện:* `{', '.join(set(tools_used))}`\n\n")

        if final_msgs:
            for m in final_msgs:
                out.write(f"{m}\n\n")
        else:
            out.write("*(Đã xử lý các công việc ngầm: dịch chương, tạo file và kiểm tra hệ thống)*\n\n")

        out.write("---\n\n")

print(f"Exported successfully to: {output_md}")
