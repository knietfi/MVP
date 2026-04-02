import os
import sys
from dotenv import load_dotenv

# Add the agent folder to sys.path
sys.path.append(r'c:\Users\malon\Web3 Development\Portfolio\Portfolio_Projects\Kinetifi-agent')

from discovery_engine import KinetiFiScanner, RejectionLogger

def verify():
    load_dotenv(r'c:\Users\malon\Web3 Development\Portfolio\Portfolio_Projects\Kinetifi-agent\.env')
    wallet = "0xd3fD8179aA2cF6d00e6b63B0bDd60259BeA05637"
    zerion_key = os.getenv("ZERION_API_KEY")
    
    scanner = KinetiFiScanner(wallet, zerion_key, target_chain="Base")
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print("Fetching positions...")
    positions = scanner.get_current_positions()
    if not positions:
        print("No positions found.")
    for pos in positions:
        print(f"---")
        print(f"Protocol: {pos.protocol}")
        print(f"Tokens: {pos.tokens}")
        print(f"Value: ${pos.value_usd:.2f}")
        print(f"APY: {pos.apy_pct}%")
        print(f"ID: {pos.token_id}")
        print(f"Key: {pos.token_key}")
    
    print("\nHunting opportunities...")
    opps = scanner.hunt_opportunities(positions)
    print(f"Found {len(opps)} opportunities.")
    
    print("\nRejection Logs:")
    for log in RejectionLogger.get_logs():
        print(f"Rejected {log['project']} [{log['token']}]: {log['reason']} - {log['details']}")

if __name__ == "__main__":
    verify()
