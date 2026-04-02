import os
import json
from google import genai
from dotenv import load_dotenv
from web3 import Web3

# Try to find .env in Kinetifi-agent2
load_dotenv("c:/Users/malon/Web3 Development/Portfolio/Portfolio_Projects/Kinetifi-agent2/.env")

def diagnostic():
    api_key = os.getenv("GEMINI_API_KEY")
    rpc_url = os.getenv("RPC_URL")
    
    print(f"--- Diagnostic Start ---")
    print(f"RPC_URL: {rpc_url}")
    print(f"API_KEY (last 4): {api_key[-4:] if api_key else 'MISSING'}")
    
    # 1. Check RPC and Contract
    print("\n--- RPC Check ---")
    try:
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        if w3.is_connected():
            chain_id = w3.eth.chain_id
            print(f"OK: Connected to Chain ID {chain_id}")
            
            # Check ETH/USD Feed on Base (8453)
            feed_addr = "0x71041dddad3595f8ce35ac4573e1869751c295de"
            code = w3.eth.get_code(Web3.to_checksum_address(feed_addr))
            if len(code) > 2:
                print(f"OK: Contract found at {feed_addr} (Code length: {len(code)})")
            else:
                print(f"FAIL: No contract at {feed_addr} on this chain (Code: {code.hex()}).")
        else:
            print("FAIL: Could not connect to RPC.")
    except Exception as e:
        print(f"FAIL: RPC Error: {e}")

    # 2. Check Gemini Models
    print("\n--- Gemini Models ---")
    try:
        if not api_key:
            print("FAIL: GEMINI_API_KEY is missing.")
            return

        client = genai.Client(api_key=api_key)
        
        test_models = [
            "gemini-1.5-flash",
            "gemini-1.5-flash-latest",
            "gemini-2.0-flash-exp",
            "gemini-2.0-flash",
            "gemini-pro"
        ]
        
        for model in test_models:
            try:
                # Use a very short timeout/test
                resp = client.models.generate_content(model=model, contents="ping")
                print(f"OK: '{model}' is supported.")
            except Exception as e:
                print(f"FAIL: '{model}' error: {str(e)[:100]}")

    except Exception as e:
        print(f"CRITICAL: Gemini Check failed: {e}")

if __name__ == "__main__":
    diagnostic()
