import re

def find_keys(filename, encoding='utf-16'):
    try:
        with open(filename, 'r', encoding=encoding) as f:
            content = f.read()
            # Look for 64-character hex strings
            keys = re.findall(r'[a-fA-F0-9]{64}', content)
            return list(set(keys))
    except Exception as e:
        return [f"Error reading {filename}: {e}"]

print("--- Keys in output.txt (UTF-16) ---")
print(find_keys('output.txt', 'utf-16'))

print("\n--- Keys in check.json (UTF-16) ---")
print(find_keys('check.json', 'utf-16'))
