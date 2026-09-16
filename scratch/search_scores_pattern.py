import glob, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

all_files = glob.glob(r'C:\Users\HoangThien\AppData\Local\Google\Chrome\User Data\Default\Local Storage\leveldb\*.*') + \
            glob.glob(r'C:\Users\HoangThien\AppData\Local\Microsoft\Edge\User Data\Default\Local Storage\leveldb\*.*')

for filepath in all_files:
    if not (filepath.endswith('.ldb') or filepath.endswith('.log')):
        continue
    with open(filepath, 'rb') as f:
        data = f.read()

    # Search for non-empty scores in utf-8: "scores": { "
    m8 = list(re.finditer(b'"scores"\\s*:\\s*\\{\\s*"', data))
    if m8:
        print(f"[UTF-8] Found non-empty scores in {filepath}: {len(m8)} matches")
        for m in m8:
            print("  ", data[m.start():m.start()+200])

    # Search in utf-16le:
    pat16 = '"scores"'.encode('utf-16le') + b'\\s*:\\s*\\{\\s*"'.replace(b'\\s', b'\\s\x00')
    # Or simply:
    m16 = list(re.finditer('"scores":{"'.encode('utf-16le'), data)) + list(re.finditer('"scores": {"'.encode('utf-16le'), data))
    if m16:
        print(f"[UTF-16] Found non-empty scores in {filepath}: {len(m16)} matches")
        for m in m16:
            snippet = data[m.start():m.start()+400].decode('utf-16le', errors='ignore')
            print("  ", snippet)
