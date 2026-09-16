import glob, os, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')

all_files = glob.glob(r'C:\Users\HoangThien\AppData\Local\Google\Chrome\User Data\Default\Local Storage\leveldb\*.*') + \
            glob.glob(r'C:\Users\HoangThien\AppData\Local\Microsoft\Edge\User Data\Default\Local Storage\leveldb\*.*')

decoder = json.JSONDecoder()
scored_found = []

for filepath in all_files:
    if not (filepath.endswith('.ldb') or filepath.endswith('.log')):
        continue
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        
        # Search for "scores" followed by non-empty object
        # In utf-16le: "scores":{"KTTX
        # In utf-8: "scores":{"KTTX
        
        # Check utf-16le
        matches16 = [m.start() for m in re.finditer('{"columns"'.encode('utf-16le'), data)]
        for m in matches16:
            try:
                dec = data[m:].decode('utf-16le', errors='ignore')
                obj, _ = decoder.raw_decode(dec)
                students = obj.get('students', [])
                sc = [s for s in students if any(v is not None and v != '' for v in s.get('scores', {}).values())]
                if sc:
                    print(f"FOUND IN {filepath} (UTF-16LE at {m}): {len(sc)} scored students!")
                    for s in sc:
                        print(f"   {s.get('name')}: {s.get('scores')}")
                    scored_found.append((filepath, m, obj))
            except Exception as e:
                pass

        # Check utf-8
        matches8 = [m.start() for m in re.finditer(b'{"columns"', data)]
        for m in matches8:
            try:
                dec = data[m:].decode('utf-8', errors='ignore')
                obj, _ = decoder.raw_decode(dec)
                students = obj.get('students', [])
                sc = [s for s in students if any(v is not None and v != '' for v in s.get('scores', {}).values())]
                if sc:
                    print(f"FOUND IN {filepath} (UTF-8 at {m}): {len(sc)} scored students!")
                    for s in sc:
                        print(f"   {s.get('name')}: {s.get('scores')}")
                    scored_found.append((filepath, m, obj))
            except Exception as e:
                pass

    except Exception as e:
        print(f"Err reading {filepath}: {e}")

print(f"\nTotal scored objects found across all files: {len(scored_found)}")
