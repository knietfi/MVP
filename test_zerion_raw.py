import requests
import base64

def test_zerion():
    key = "zk_ed6e90d4326a4845b2fe67024573d6e2"
    auth_str = f"{key}:"
    auth_bytes = auth_str.encode("ascii")
    base64_auth = base64.b64encode(auth_bytes).decode("ascii")
    
    headers = {
        "accept": "application/json",
        "authorization": f"Basic {base64_auth}",
    }
    
    wallet = "0xd3fD8179aA2cF6d00e6b63B0bDd60259BeA05637"
    # Try simple positions
    url = f"https://api.zerion.io/v1/wallets/{wallet}/positions/?filter[positions]=only_simple"
    
    print(f"Testing Zerion simple positions for {wallet}...")
    resp = requests.get(url, headers=headers)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json().get("data", [])
        print(f"Found {len(data)} simple positions.")
        for item in data:
            attr = item.get("attributes", {})
            print(f" - {attr.get('name')}: {attr.get('value')} USD")
    else:
        print(f"Error: {resp.text}")

    import time
    print("\nWaiting 5s to avoid rate limit...")
    time.sleep(5)

    # Try complex positions
    url = f"https://api.zerion.io/v1/wallets/{wallet}/positions/?filter[positions]=only_complex"
    print(f"\nTesting Zerion complex positions for {wallet}...")
    resp = requests.get(url, headers=headers)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json().get("data", [])
        print(f"Found {len(data)} complex positions.")
    else:
        print(f"Error: {resp.text}")

if __name__ == "__main__":
    test_zerion()
