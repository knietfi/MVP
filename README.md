# KinetiFi: AI-Driven DeFi Optimization

**KinetiFi** is a next-generation decentralized finance (DeFi) portfolio optimizer that bridges AI-driven market intelligence with non-custodial on-chain execution. It enables users to deploy a personal **KinetiFi AI Agent** that scans the multichain ecosystem for yield opportunities and registers "Intents" to autonomously improve portfolio performance.

---

## 🏗 System Architecture

KinetiFi is composed of three primary layers working in orchestration:

### 1. Smart Contract Layer (Base Sepolia)

The foundation of KinetiFi is a secure, intent-based account abstraction framework.

- **KinetiFiAccount**: An advanced smart account (ERC-4337 style) supporting local session modules.
- **KinetiFiAccountFactory**: Provides deterministic `CREATE2` deployment for user accounts based on their EOA.
- **IntentRegistry**: A central logic contract where Agents log signed optimization intents (Target Vault, Min APY, CallData, Deadline).
- **KinetiFiSessionModule**: Manages ephemeral authorizations. Users grant the Agent a 24-hour session key, allowing it to register intents without a manual signature for every discovery.

### 2. AI Agent Backend (Python/FastAPI)

The "Brain" of the project, responsible for heavy lifting and cross-chain discovery.

- **KinetiFiScanner**: Aggregates live portfolio data from **Zerion** and tracks global yield benchmarks via **DefiLlama**.
- **Discovery Engine**: Identifies "Upgrade Opportunities" (moves with >200bps yield delta) and calculates optimal swap paths.
- **Safety & Risk Module**: Enforces strict guardrails:
  - **Yield Minimum**: Forces a minimum 2% APY improvement.
  - **Gas Efficiency**: Defers moves if gas exceeds 5% of monthly projected earnings.
  - **Slippage Control**: Strict 0.5% max slippage buffer on all intents.
- **Reasoning Engine**: Generates technical explanations for every move, visible in the UI.

### 3. Frontend Dashboard (React/Vite)

A premium, glassmorphism-inspired interface built for transparency and control.

- **Technology**: React 18, Vite, Framer Motion, Tailwind CSS, Wagmi v2, Reown AppKit, TanStack Query.
- **Zero-CORS Proxy**: Custom Edge Function proxy to fetch Zerion data securely without exposing API keys.

---

## 🎨 UI/UX Features

- **Portoflio Intelligence**: Real-time USD valuation and asset allocation across 10+ chains.
- **Visual Feedback System**:
  - **Scanning Animations**: Sidebar indicates active multichain searches.
  - **Agent Success Glow**: Breathing "Active" status once on-chain authorization is confirmed.
  - **Branded Skeletons**: High-fidelity shimmer loaders matching the KinetiFi aesthetic.
- **Strategy Feed**: A real-time log of Agent activity including "AI Insights" and a history of registered optimization intents.
- **Mobile Responsive**: Fully optimized for small screens with stacked layouts and fluid headers.

---

## 🔄 The User Workflow ("The Zen Loop")

1. **Connect**: User connects via MetaMask or WalletConnect on Base Sepolia.
2. **Authorize**: User enables the AI Agent via the Dashboard. This grants a 24h session key to the Agent.
3. **Discover**: The Backend Agent scans holdings and identifies yield upgrades (e.g., _"Move USDC from Aave (5%) to Morpho (12%)"_).
4. **Validation**: The Agent checks gas viability and yield delta (Safety & Risk Module).
5. **Register**: User clicks "Register Intent" to commit the move on-chain to the `IntentRegistry`.

---

## 🛠 Technical Setup

### Frontend (.env)

```bash
VITE_ZERION_API_KEY=your_key
VITE_WALLETCONNECT_PROJECT_ID=...
VITE_AGENT_API_URL=http://localhost:8000
```

### Agent Backend (.env)

```bash
RPC_URL=https://base-sepolia.infura.io/v3/...
INTENT_REGISTRY_ADDRESS=0xeEa52b6e3bda8a93eEddE8D97B272025CC5e20Fba
AGENT_PRIVATE_KEY=...
```

### Running Locally

1. **Agent**: `uvicorn main:app --port 8000`
2. **Frontend**: `npm run dev`

---

## 📜 Deployment Details (Base Sepolia)

| Contract            | Address                                       |
| :------------------ | :-------------------------------------------- |
| **KinetiFiAccount** | `0xbA355fF2b2d0391A789669d4d8D695E70A2d4e40`  |
| **IntentRegistry**  | `0xeEa52b6e3bda8a93eEddE8D97B272025CC5e20Fba` |
| **SessionModule**   | `0x72af5B8b25D7fE949177397D09b5CEeC22e44004`  |
| **Factory**         | `0xCB6350D5a52930a5C06196614B94E67B418cbD41`  |

---

_Built with ❤️ for the KinetiFi Ecosystem. AI is the standard. Optimization is the goal._
