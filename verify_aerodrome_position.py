"""
verify_aerodrome_position.py
Run this to confirm the on-chain data is accessible before debugging frontend code.

Usage:
    python verify_aerodrome_position.py
"""
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# ──  RPC (use your existing env var, fallback to public endpoint)
RPC_URL = os.getenv("RPC_URL", "https://mainnet.base.org")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

print(f"Connected to RPC: {RPC_URL}")
print(f"Chain ID: {w3.eth.chain_id}")
print(f"Latest block: {w3.eth.block_number}")
print()

# ── Addresses to verify ─────────────────────────────────────────────────────
TOKEN_ID       = 3570965
NFPM_ADDRESS   = Web3.to_checksum_address("0xa990C6a764B73BF43Cee5BB40339C3322fb9D55f")
POOL_ADDRESS   = Web3.to_checksum_address("0x34E3334E845d101205394e0Bd8821fDdc7Cd5559")
GAUGE_ADDRESS  = Web3.to_checksum_address("0x7A01529B70DD997D7723D4AA2EEC0CC301E0E6CF")
EOA_ADDRESS    = Web3.to_checksum_address("0x51C02040F21e0a1aABB2c94b7019F85dCb75845F")

# ── ABIs ────────────────────────────────────────────────────────────────────
NFPM_ABI = [
    {
        "inputs": [{"name": "tokenId", "type": "uint256"}],
        "name": "positions",
        "outputs": [
            {"name": "nonce",                    "type": "uint96"},
            {"name": "operator",                 "type": "address"},
            {"name": "token0",                   "type": "address"},
            {"name": "token1",                   "type": "address"},
            {"name": "tickSpacing",              "type": "int24"},
            {"name": "tickLower",                "type": "int24"},
            {"name": "tickUpper",                "type": "int24"},
            {"name": "liquidity",                "type": "uint128"},
            {"name": "feeGrowthInside0LastX128", "type": "uint256"},
            {"name": "feeGrowthInside1LastX128", "type": "uint256"},
            {"name": "tokensOwed0",              "type": "uint128"},
            {"name": "tokensOwed1",              "type": "uint128"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"name": "tokenId", "type": "uint256"}],
        "name": "ownerOf",
        "outputs": [{"name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
]

POOL_ABI = [
    {
        "inputs": [],
        "name": "slot0",
        "outputs": [
            {"name": "sqrtPriceX96",               "type": "uint160"},
            {"name": "tick",                       "type": "int24"},
            {"name": "observationIndex",            "type": "uint16"},
            {"name": "observationCardinality",      "type": "uint16"},
            {"name": "observationCardinalityNext",  "type": "uint16"},
            {"name": "feeProtocol",                "type": "uint8"},
            {"name": "unlocked",                   "type": "bool"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "token0",
        "outputs": [{"name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "token1",
        "outputs": [{"name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
]

GAUGE_ABI = [
    {
        "inputs": [{"name": "tokenId", "type": "uint256"}],
        "name": "stakedContains",
        "outputs": [{"name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
]

ERC721_ABI = [
    {
        "inputs": [{"name": "tokenId", "type": "uint256"}],
        "name": "ownerOf",
        "outputs": [{"name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
]

# ── Test 1: Who owns NFT #3570965? ──────────────────────────────────────────
print("=" * 60)
print("TEST 1: Who owns NFT #3570965?")
print("=" * 60)
try:
    nfpm = w3.eth.contract(address=NFPM_ADDRESS, abi=NFPM_ABI)
    owner = nfpm.functions.ownerOf(TOKEN_ID).call()
    print(f"  NFT #{TOKEN_ID} owner: {owner}")
    if owner.lower() == GAUGE_ADDRESS.lower():
        print(f"  ✅ Confirmed: NFT is staked in Gauge {GAUGE_ADDRESS}")
    elif owner.lower() == EOA_ADDRESS.lower():
        print(f"  ✅ NFT is in EOA wallet directly")
    else:
        print(f"  ⚠️ Unexpected owner — not Gauge or EOA")
except Exception as e:
    print(f"  ❌ ownerOf({TOKEN_ID}) FAILED: {e}")
    print(f"     → NFPM address may be WRONG: {NFPM_ADDRESS}")

# ── Test 2: NFPM.positions(3570965) ─────────────────────────────────────────
print()
print("=" * 60)
print("TEST 2: NFPM.positions(3570965)")
print("=" * 60)
try:
    pos = nfpm.functions.positions(TOKEN_ID).call()
    print(f"  nonce:       {pos[0]}")
    print(f"  operator:    {pos[1]}")
    print(f"  token0:      {pos[2]}")
    print(f"  token1:      {pos[3]}")
    print(f"  tickSpacing: {pos[4]}")
    print(f"  tickLower:   {pos[5]}")
    print(f"  tickUpper:   {pos[6]}")
    print(f"  liquidity:   {pos[7]}")
    print(f"  ✅ NFPM address is correct: {NFPM_ADDRESS}")
except Exception as e:
    print(f"  ❌ positions({TOKEN_ID}) FAILED: {e}")
    print(f"     → NFPM address is WRONG: {NFPM_ADDRESS}")

# ── Test 3: Pool.slot0() ────────────────────────────────────────────────────
print()
print("=" * 60)
print("TEST 3: Pool.slot0() and token pair")
print("=" * 60)
try:
    pool = w3.eth.contract(address=POOL_ADDRESS, abi=POOL_ABI)
    s0 = pool.functions.slot0().call()
    t0 = pool.functions.token0().call()
    t1 = pool.functions.token1().call()
    print(f"  sqrtPriceX96: {s0[0]}")
    print(f"  currentTick:  {s0[1]}")
    print(f"  token0:       {t0}")
    print(f"  token1:       {t1}")
    print(f"  ✅ Pool address is correct: {POOL_ADDRESS}")
except Exception as e:
    print(f"  ❌ Pool.slot0() FAILED: {e}")
    print(f"     → Pool address is WRONG: {POOL_ADDRESS}")

# ── Test 4: Is token staked in gauge? ───────────────────────────────────────
print()
print("=" * 60)
print("TEST 4: Is NFT staked in Gauge?")
print("=" * 60)
try:
    gauge = w3.eth.contract(address=GAUGE_ADDRESS, abi=GAUGE_ABI)
    is_staked = gauge.functions.stakedContains(TOKEN_ID).call()
    print(f"  Gauge.stakedContains({TOKEN_ID}): {is_staked}")
    if is_staked:
        print(f"  ✅ NFT is currently staked in Gauge")
    else:
        print(f"  ⚠️ NFT is NOT staked (may have been unstaked)")
except Exception as e:
    print(f"  ❌ stakedContains({TOKEN_ID}) FAILED: {e}")

print()
print("=" * 60)
print("SUMMARY: Copy the results above to identify which address is wrong.")
print("=" * 60)
