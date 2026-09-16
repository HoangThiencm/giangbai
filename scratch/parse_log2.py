import re, json, sys

# Set stdout to utf-8
sys.stdout.reconfigure(encoding='utf-8')

log_path = r"C:\Users\HoangThien\AppData\Local\Google\Chrome\User Data\Default\Local Storage\leveldb\000370.log"
with open(log_path, "rb") as f:
    raw = f.read()

matches = [m.start() for m in re.finditer(b"sodiem:", raw)]
decoder = json.JSONDecoder()
results = {}

for m in matches:
    key_raw = raw[m:m+40]
    # find where utf16 target begins
    utf16_target = '{"columns"'.encode('utf-16le')
    pos16 = raw.find(utf16_target, m)
    if pos16 != -1 and pos16 - m < 150:
        try:
            dec = raw[pos16:].decode('utf-16le', errors='ignore')
            obj, idx = decoder.raw_decode(dec)
            # Find the actual key name
            key_name = raw[m:pos16].decode('utf-8', errors='ignore').strip()
            students = obj.get('students', [])
            scored_students = [s for s in students if any(v is not None and v != '' for v in s.get('scores', {}).values())]
            print(f"Key: {key_name} | Offset: {m} | Students: {len(students)} | Scored: {len(scored_students)}")
            for s in scored_students:
                print(f"   {s.get('name')} (SBD: {s.get('sbd')}): {s.get('scores')}")
            results[f"{key_name}_{m}"] = obj
        except Exception as e:
            print(f"Error parsing at {m}: {e}")

with open("scratch/recovered_gradebook.json", "w", encoding="utf-8") as out:
    json.dump(results, out, ensure_ascii=False, indent=2)

print("\n--- Summary of All Recovered Scores ---")
total_scored = 0
for k, v in results.items():
    sc = [s for s in v.get('students', []) if any(val is not None and val != '' for val in s.get('scores', {}).values())]
    if sc:
        print(f"\n[{k}] has {len(sc)} students with scores:")
        for s in sc:
            print(f"  - {s.get('name')}: {s.get('scores')}")
        total_scored += len(sc)

print(f"\nTotal students with recovered scores: {total_scored}")
