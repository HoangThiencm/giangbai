import glob, os, re, json

chrome_files = glob.glob(r'C:\Users\HoangThien\AppData\Local\Google\Chrome\User Data\Default\Local Storage\leveldb\*.*')
edge_files = glob.glob(r'C:\Users\HoangThien\AppData\Local\Microsoft\Edge\User Data\Default\Local Storage\leveldb\*.*')

files = chrome_files + edge_files
print(f"Total files checked: {len(files)}")

found_entries = []

for f in files:
    if not (f.endswith('.ldb') or f.endswith('.log')):
        continue
    try:
        with open(f, 'rb') as fp:
            content = fp.read()
            if b'sodiem:' in content:
                print(f"Found 'sodiem:' in: {f}")
                # extract text chunks
                pos = 0
                while True:
                    idx = content.find(b'sodiem:', pos)
                    if idx == -1:
                        break
                    snippet = content[idx:idx+2000]
                    # Try to find json after the key
                    try:
                        text = snippet.decode('utf-8', errors='ignore')
                        print(f"Snippet at {idx}: {text[:150]}")
                    except:
                        pass
                    pos = idx + 7
            # Also search for 'KTTX' or scores pattern
            if b'KTTX' in content and b'scores' in content:
                print(f"Found 'KTTX' and 'scores' in: {f}")
                pos = 0
                while True:
                    idx = content.find(b'{"columns"', pos)
                    if idx == -1:
                        idx = content.find(b'{\"columns\"', pos)
                    if idx == -1:
                        break
                    chunk = content[idx:idx+50000]
                    text = chunk.decode('utf-8', errors='ignore')
                    # look for students
                    if '"students"' in text or '\\"students\\"' in text:
                        print(f"Possible gradebook json at {idx} (len {len(text)}):")
                        print(text[:300])
                        found_entries.append(text)
                    pos = idx + 10
    except Exception as e:
        print(f"Error reading {f}: {e}")

with open('scratch/found_sodiem_raw.txt', 'w', encoding='utf-8') as out:
    for item in found_entries:
        out.write(item + '\n' + '='*50 + '\n')
print(f"Wrote {len(found_entries)} candidates to scratch/found_sodiem_raw.txt")
