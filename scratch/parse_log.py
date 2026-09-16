import re, json

log_path = r"C:\Users\HoangThien\AppData\Local\Google\Chrome\User Data\Default\Local Storage\leveldb\000370.log"
with open(log_path, "rb") as f:
    raw = f.read()

print("File size:", len(raw))

# Search for keys
# Keys are ASCII / UTF-8: sodiem:<class>:<subject>:2025-2026
matches = [m.start() for m in re.finditer(b"sodiem:", raw)]
print("Found matches at:", matches)

results = {}

for m in matches:
    # Read key
    key_end = raw.find(b"\x00", m)
    if key_end == -1 or key_end - m > 100:
        key_raw = raw[m:m+50]
    else:
        key_raw = raw[m:key_end]
    key_str = key_raw.decode("utf-8", errors="ignore")
    print(f"\n--- Key: {key_str} at offset {m} ---")
    
    # In Chromium Local Storage leveldb, the value for a key is stored after the key header
    # It starts with \x00 or \x01 (version byte) and is UTF-16LE or UTF-8
    val_start = m + len(key_raw)
    # Scan forward up to 30000 bytes
    window = raw[val_start:val_start+50000]
    
    # Try decoding as UTF-16LE
    # Find { "columns"
    utf16_target = '{"columns"'.encode('utf-16le')
    pos16 = window.find(utf16_target)
    if pos16 != -1:
        # try to decode from pos16
        try:
            # find matching end of JSON
            dec = window[pos16:].decode('utf-16le', errors='ignore')
            # extract json object
            end_brace = dec.rfind('}')
            if end_brace != -1:
                json_str = dec[:end_brace+1]
                obj = json.loads(json_str)
                students = obj.get('students', [])
                scored_students = [s for s in students if any(v is not None and v != '' for v in s.get('scores', {}).values())]
                print(f"Decoded JSON successfully! Total students: {len(students)}, Scored: {len(scored_students)}")
                for s in scored_students:
                    print(f"  - {s.get('name')}: {s.get('scores')}")
                results[key_str] = obj
        except Exception as e:
            print("UTF-16LE parse error:", e)
    else:
        print("utf16_target not found in window")

with open("scratch/recovered_gradebook.json", "w", encoding="utf-8") as out:
    json.dump(results, out, ensure_ascii=False, indent=2)
print("\nSaved recovered data to scratch/recovered_gradebook.json")
