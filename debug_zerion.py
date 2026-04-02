import os
import requests
import json
import sys
import base64
from dotenv import load_dotenv

# Try to load from sibling project's .env if needed
load_dotenv('../Kinetifi-agent/.env')
# Also try local
load_dotenv('.env')

key = os.getenv('ZERION_API_KEY')
if not key:
    print("Error: ZERION_API_KEY not found in .env")
    sys.exit(1)

# Zerion expects Basic Auth with key: (empty password)
auth_str = f"{key}:"
auth_bytes = auth_str.encode('ascii')
base64_auth = base64.b64encode(auth_bytes).decode('ascii')

addr = '0x2Ba20848F5125Dd14B2620d978F83A993176A43f'
url = f'https://api.zerion.io/v1/wallets/{addr}/positions/?filter[positions]=only_complex'
headers = {'Authorization': f'Basic {base64_auth}'}

print(f"Fetching from: {url}")
resp = requests.get(url, headers=headers)
if not resp.ok:
    print(f"Error: {resp.status_code} {resp.text}")
    sys.exit(1)

data = resp.json().get('data', [])

print(f"Found {len(data)} complex positions")
with open('debug_zerion_output.txt', 'w', encoding='utf-8') as f:
    for i in data:
        attr = i.get('attributes', {})
        proto_data = attr.get('protocol')
        proto = (proto_data.get('name') if isinstance(proto_data, dict) else proto_data) or 'N/A'
        name = attr.get('name', 'N/A')
        id_str = i.get('id', 'N/A')
        
        if 'Aerodrome' in name or 'Aerodrome' in proto:
            output = f"--- Aerodrome Position ---\nID: {id_str}\nName: {name}\nProtocol: {proto}\nNFT Info: {attr.get('nft_info')}\nValue: ${attr.get('value', 0):.2f}\n--------------------------\n"
            print(output)
            f.write(output)
