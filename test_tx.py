import os
import sys

# Add Kinetifi-agent to path so we can import its modules
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Kinetifi-agent"))
from discovery_engine import KinetiFiAgent, UpgradeOpportunity, Position

rpc = "https://base-sepolia.infura.io/v3/af810698c71c46dc865ec27dd1bfa6f9"
reg = "0xeEa52b6e3bda8a93eDdE8D97B272025CC5e20Fba"
pk = "0x2db62c054fc6605f38e5ed5ab5ff5b930fffa6dc02ef3cc2010c53d1da6c7f50"

agent = KinetiFiAgent(rpc_url=rpc, registry_address=reg, private_key=pk, agent_id=1)

pos = Position(
    protocol="Mock Aave",
    tokens=["USDC"],
    value_usd=1000.0,
    vault_address="0x8ef5aa77d7f2c54faa3d498ac64ac26506e24a35",
    apy_pct=2.0,
)
opp = UpgradeOpportunity(
    current=pos,
    candidate_project="Compound V3",
    candidate_chain="base",
    candidate_apy_pct=2.0,
    delta_bps=0,
)

try:
    print("Testing register_intent_for_opportunity...")
    agent.register_intent_for_opportunity(
        opp, "0xbA355fF2b2d0391A789669d4d8D695E70A2d4e40"
    )
    print("Done")
except Exception as e:
    print(f"Exception: {e}")
