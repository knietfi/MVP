import os
import json
import base64
import urllib.request
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

api_key = os.getenv("VITE_ZERION_API_KEY")
if not api_key:
    # try other
    api_key = os.getenv("ZERION_API_KEY")
    if not api_key:
        print("No ZERION_API_KEY found")
        exit(1)

auth_str = f"{api_key}:"
base64_auth = base64.b64encode(auth_str.encode("ascii")).decode("ascii")

headers = {
    "accept": "application/json",
    "authorization": f"Basic {base64_auth}"
}

addresses = [
    "0xdf53b8dfc22aeCb06a8Dbf9A7482525b5AbaFe5b",
    "0x2Ba20848F5125Dd14B2620d978F83A993176A43f"
]

results = {}

for addr in addresses:
    url = f"https://api.zerion.io/v1/wallets/{addr}/positions/?filter[positions]=only_complex"
    req = urllib.request.Request(url, headers=headers)
    try:
        res = urllib.request.urlopen(req)
        data = json.loads(res.read())
        results[addr] = data
    except Exception as e:
        print(f"Error for {addr}: {e}")

with open("zerion_test.json", "w") as f:
    json.dump(results, f, indent=2)

print("Saved to zerion_test.json")
