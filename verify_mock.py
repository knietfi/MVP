import os
import sys
import json
from unittest.mock import Mock, patch

# Add the agent folder to sys.path
sys.path.append(r'c:\Users\malon\Web3 Development\Portfolio\Portfolio_Projects\Kinetifi-agent')

from discovery_engine import KinetiFiScanner, RejectionLogger, Position

def verify_mock():
    # Mock Zerion Response
    mock_data = {
        "data": [
            {
                "id": "wallet-base-usdc",
                "attributes": {
                    "name": "USDC",
                    "quantity": {"float": 9.01},
                    "value": 9.01,
                    "position_type": "wallet",
                    "chain": "base",
                    "protocol": None,
                    "fungible_info": {"symbol": "USDC", "name": "USD Coin"}
                }
            }
        ]
    }

    with patch('requests.get') as mock_get:
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = mock_data
        
        scanner = KinetiFiScanner("0xd3fD8179aA2cF6d00e6b63B0bDd60259BeA05637", "dummy_key", target_chain="Base")
        
        print("Scanned positions (Mocked):")
        positions = scanner.get_current_positions()
        for pos in positions:
            print(f" - {pos.protocol} | {pos.tokens} | ${pos.value_usd:.2f} | {pos.apy_pct}%")
            
        # Test APY Floor and Small Balance Override
        print("\nVerifying APY Floor & Small Balance Override...")
        # Test Risk Tier Quotas and stability scoring
        print("\nVerifying Risk Tier Quotas & Stability Score...")
        scanner._llama_cache = [
            {
                "project": "LowRisk_Large",
                "symbol": "USDC",
                "tokens": ["USDC"],
                "tvlUsd": 50_000_000,
                "apy": 10.0,
                "chain": "Base",
                "pool": "low1"
            },
            {
                "project": "LowRisk_Small",
                "symbol": "USDC",
                "tokens": ["USDC"],
                "tvlUsd": 11_000_000,
                "apy": 12.0,
                "chain": "Base",
                "pool": "low2"
            },
            {
                "project": "MedRisk_Large",
                "symbol": "USDC",
                "tokens": ["USDC"],
                "tvlUsd": 5_000_000,
                "apy": 25.0,
                "chain": "Base",
                "pool": "med1"
            },
            {
                "project": "MedRisk_Small",
                "symbol": "USDC",
                "tokens": ["USDC"],
                "tvlUsd": 1_500_000,
                "apy": 30.0,
                "chain": "Base",
                "pool": "med2"
            },
            {
                "project": "HighRisk_Supernova",
                "symbol": "USDC",
                "tokens": ["USDC"],
                "tvlUsd": 500_000,
                "apy": 500.0,
                "chain": "Base",
                "pool": "high1"
            }
        ]
        
        # Add a $1000 position to test the 20% floor
        positions.append(Position(
            protocol="Aave",
            tokens=["USDC"],
            value_usd=1000.0,
            vault_address="0x123",
            apy_pct=2.0
        ))
        
        opps = scanner.hunt_opportunities(positions)
        print(f"Total Opportunities found: {len(opps)}")
        
        low_opps = [o for o in opps if o.risk_tier == "Low"]
        med_opps = [o for o in opps if o.risk_tier == "Medium"]
        high_opps = [o for o in opps if o.risk_tier == "High"]
        
        print(f"Risk Distribution: {len(low_opps)} Low, {len(med_opps)} Medium, {len(high_opps)} High")
        
        for o in opps:
            print(f" - [{o.risk_tier}] {o.candidate_project} | APY: {o.candidate_apy_pct}% | Stability: {o.stability_score:.2f}")

        # Assert Quotas
        if len(low_opps) >= 2:
            print("SUCCESS: Low Risk Quota met (>= 2)")
        else:
            print(f"FAILURE: Low Risk Quota NOT met ({len(low_opps)} < 2)")
            
        if len(med_opps) >= 2:
            print("SUCCESS: Medium Risk Quota met (>= 2)")
        else:
            print(f"FAILURE: Medium Risk Quota NOT met ({len(med_opps)} < 2)")

        # Assert Sorting (Stability for Low/Medium)
        if len(low_opps) >= 2:
            if low_opps[0].stability_score >= low_opps[1].stability_score:
                print("SUCCESS: Low Risk sorted by Stability Score.")
            else:
                print("FAILURE: Low Risk NOT sorted by Stability Score.")

        # Test Asset Preservation Bypass
        print("\nVerifying Asset Preservation Bypass (Low Risk < 20% Floor)...")
        # Added a 15% Low Risk pool. Standard floor is 20%. 
        # For $1000 pos, delta is 13% (>2%). Should bypass.
        scanner._llama_cache = [
            {
                "project": "Stable_15_Percent",
                "symbol": "USDC",
                "tokens": ["USDC"],
                "tvlUsd": 25_000_000,
                "apy": 15.0,
                "chain": "Base",
                "pool": "stable1"
            }
        ]
        RejectionLogger.clear()
        opps_bypass = scanner.hunt_opportunities([positions[-1]]) # Aave $1000
        if any(o.candidate_project == "Stable_15_Percent" for o in opps_bypass):
             print("SUCCESS: 15% Low Risk move bypassed 20% floor (Asset Preservation working).")
        else:
             print("FAILURE: 15% Low Risk move blocked by floor.")
             for l in RejectionLogger.get_logs(): print(f" Log: {l['reason']} | {l['details']}")

if __name__ == "__main__":
    verify_mock()
