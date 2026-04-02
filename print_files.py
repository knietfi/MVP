import os

def print_file(filename, encoding='utf-16'):
    print(f"\n--- CONTENT OF {filename} ---")
    try:
        with open(filename, 'r', encoding=encoding) as f:
            print(f.read())
    except Exception as e:
        print(f"Error reading {filename}: {e}")

print_file('output.txt')
print_file('check.json')
