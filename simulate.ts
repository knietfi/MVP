import { createPublicClient, http, encodeFunctionData, parseAbi } from 'viem';
import { baseSepolia } from 'viem/chains';

const client = createPublicClient({
  chain: baseSepolia,
  transport: http('https://sepolia.base.org')
});

async function main() {
  const abi = parseAbi([
    'function registerIntent(uint256 agentId, tuple(address targetVault, bytes4 functionSelector, uint256 minExpectedAPY, uint256 deadline, bytes callData) intent)'
  ]);

  const data = encodeFunctionData({
    abi,
    functionName: 'registerIntent',
    args: [
      1n,
      {
        targetVault: '0x8ef5aa77d7f2c54faa3d498ac64ac26506e24a35',
        functionSelector: '0x12345678',
        minExpectedAPY: 200n,
        deadline: BigInt(Math.floor(Date.now() / 1000) + 3600),
        callData: '0x'
      }
    ]
  });

  try {
    console.log("Simulating eth_call to IntentRegistry...");
    const res = await client.call({
      to: '0xeEa52b6e3bda8a93eDdE8D97B272025CC5e20Fba',
      data,
      account: '0x76Fa6fEdD242e85F3D1F1a2a47FccE63cd73B90B' // The agent EOA
    });
    console.log("Success:", res);
  } catch (err: any) {
    console.error("Revert Reason:", err.shortMessage || err.message);
  }
}

main();
