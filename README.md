# Proofnet BTC SDK (MIT)

Client helpers and examples for building against a local Proofnet BTC node:

- Proofnet API: `http://127.0.0.1:25556`
- ProofWallet API: `http://127.0.0.1:9756`
- Native Explorer (optional connectors): `http://127.0.0.1:3006`

This repo intentionally contains **no Proofnet core source**.

## Core vs connectors (why 3006 exists)

- Proofnet BTC *core* is the canonical PQ chain + deterministic lane state. Apps can build only against core APIs.
- External integrations (EVM vault watchers, Solana adapters, etc.) are *optional connectors* and can be added later.
- Native Explorer exposes a few convenience “bridge” endpoints (like EVM address registration) that sit on top of ProofWallet.

## Core API quick map (25556)

- Node status: `GET /api/status`
- Core chain snapshot: `GET /core/info`, `GET /core/block/tip`, `GET /core/assets`
- Memory Blocks SPV: `GET /mblk/spv/proof?digest=...`, `POST /mblk/spv/proofs`
- Variant Nova (read-only local snapshot): `GET /vnova/prices`, `GET /vnova/price`, `GET /vnova/health`, `GET /vnova/overview`
- Blockie AI (repo-local grounding): `POST /ai/chat`, `GET /ai/docs/search`, `GET /ai/qbit/context`

## Python quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ./python
python examples/proofnet_status.py
```

## JavaScript/TypeScript (Node/Next.js) quickstart

This repo also ships a small, dependency-free JS SDK (published as the
`@proofnet/sdk` package when installed from this git repo).

Example:

```bash
node -e 'import { getApiStatus, resolveCoreBaseUrl } from "@proofnet/sdk"; const base=resolveCoreBaseUrl(); getApiStatus(base).then(r=>console.log(r.status, r.data)).catch(console.error)'
```

Optional connector helpers:

```bash
node -e 'import { resolveNativeExplorerBaseUrl, resolveProofwalletBaseUrl, registerProofwalletAddress } from "@proofnet/sdk"; const pw=resolveProofwalletBaseUrl(); registerProofwalletAddress(pw,{wallet:"wallet_id",asset:"seth",address:"0x0000000000000000000000000000000000000000"}).then(r=>console.log(r.status,r.data)).catch(console.error)'
```

## Curl (no SDK)

```bash
curl -s http://127.0.0.1:25556/api/status | jq
curl -s http://127.0.0.1:25556/core/info | jq
curl -s 'http://127.0.0.1:25556/ai/docs/search?q=proofnet%20core%20facts' | jq
curl -s http://127.0.0.1:9756/readyz | jq
curl -s http://127.0.0.1:3006/healthz | jq
```
