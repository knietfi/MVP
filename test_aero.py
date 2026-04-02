import os
import requests
import json
import base64
from dotenv import load_dotenv

load_dotenv()

wallet = "0x2ba20848f5125dd14b2620d978f83a993176a43f"
api_key = os.getenv("VITE_ZERION_API_KEY")
print(f"Key loaded: {api_key is not None}")

auth_str = f"{api_key}:"
base64_auth = base64.b64encode(auth_str.encode("ascii")).decode("ascii")

headers = {
    "accept": "application/json",
    "authorization": f"Basic {base64_auth}"
}

url = f"https://api.zerion.io/v1/wallets/{wallet}/positions/?filter[positions]=only_complex"

resp = requests.get(url, headers=headers)
print("Status:", resp.status_code)

data = resp.json()
with open("zerion_complex.json", "w") as f:
    json.dump(data, f, indent=2)

items = data.get("data", [])
print("Found items:", len(items))

aero_items = [i for i in items if "aero" in str(i).lower()]
print("Aerodrome items:", len(aero_items))
