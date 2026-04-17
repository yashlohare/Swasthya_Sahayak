import requests
import sys

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

tests = [
    ('Hindi', '\u091f\u0947\u0938\u094d\u091f: \u0926\u093f\u0932', 'heart'),
    ('Hindi', '\u091f\u0947\u0938\u094d\u091f: \u0938\u093e\u0902\u092a', 'snake'),
    ('Hindi', '\u091f\u0947\u0938\u094d\u091f: \u091c\u0932\u0928\u093e', 'burn'),
    ('Marathi', '\u091a\u093e\u091a\u0923\u0940: \u0939\u0943\u0926\u092f', 'heart'),
    ('Marathi', '\u091a\u093e\u091a\u0923\u0940: \u0938\u093e\u092a', 'snake'),
    ('Marathi', '\u091a\u093e\u091a\u0923\u0940: \u092d\u093e\u091c\u0923\u0947', 'burn'),
    ('Tamil', '\u0b9a\u0bcb\u0ba4\u0ba9\u0bc8: \u0b87\u0ba4\u0baf\u0bae\u0bcd', 'heart'),
    ('Tamil', '\u0b9a\u0bcb\u0ba4\u0ba9\u0bc8: \u0baa\u0bbe\u0bae\u0bcd\u0baa\u0bc1', 'snake'),
    ('Tamil', '\u0b9a\u0bcb\u0ba4\u0ba9\u0bc8: \u0ba4\u0bc0\u0b95\u0bcd\u0b95\u0bbe\u0baf\u0bae\u0bcd', 'burn'),
    ('Telugu', '\u0c2a\u0c30\u0c40\u0c15\u0c4d\u0c37: \u0c17\u0c41\u0c02\u0c21\u0c46', 'heart'),
    ('Telugu', '\u0c2a\u0c30\u0c40\u0c15\u0c4d\u0c37: \u0c2a\u0c3e\u0c2e\u0c41', 'snake'),
    ('Telugu', '\u0c2a\u0c30\u0c40\u0c15\u0c4d\u0c37: \u0c15\u0c3e\u0c32\u0c41\u0c1f', 'burn'),
    ('English', 'Test: Heart', 'heart'),
]

print('=== REGIONAL TRIAGE VALIDATION ===')
all_pass = True
for lang, text, expected in tests:
    try:
        r = requests.post('http://127.0.0.1:8000/api/triage', json={'text': text, 'language': lang}, timeout=10)
        data = r.json()
        resp = data.get('llm_response', '')
        clean = resp.replace('CPR','').replace('Heimlich','')
        is_english = all(ord(c) < 128 or c in ' .,!?()-:;' for c in clean)
        if lang != 'English' and is_english:
            status = 'FAIL (English!)'
            all_pass = False
        else:
            status = 'PASS'
        print(f'{lang:8} | {expected:6} | {status:20} | {resp[:60]}...')
    except Exception as e:
        print(f'{lang:8} | {expected:6} | ERROR: {e}')
        all_pass = False

if all_pass:
    print('\n=== FINAL RESULT: ALL PASS ===')
else:
    print('\n=== FINAL RESULT: FAILURES DETECTED ===')
