from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, Optional


def _json_request(url: str, method: str = "GET", payload: Optional[Dict[str, Any]] = None) -> Any:
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url=url, method=method, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else ""
        raise RuntimeError(f"HTTP {e.code} for {url}: {body}") from e


@dataclass(frozen=True)
class ProofnetClient:
    base_url: str = "http://127.0.0.1:25556"

    def status(self) -> Any:
        """
        Return the Proofnet status snapshot from /api/status.

        Note: Proofnet core does not guarantee a /health endpoint.
        """
        return _json_request(f"{self.base_url}/api/status")

    def health(self) -> Any:
        # Back-compat alias; /health is not a stable Proofnet endpoint.
        return self.status()

    # -----------------------------
    # Convenience wrappers
    # -----------------------------

    def core_info(self) -> Any:
        return self.get("/core/info")

    def core_tip(self) -> Any:
        return self.get("/core/block/tip")

    def core_assets(self) -> Any:
        return self.get("/core/assets")

    def vnova_prices(self, *, max_age_sec: int = 600) -> Any:
        return self.get(f"/vnova/prices?max_age_sec={int(max_age_sec)}")

    def vnova_price(self, *, asset: str, quote: str = "USD", max_age_sec: int = 600) -> Any:
        asset = str(asset or "").strip()
        quote = str(quote or "").strip()
        return self.get(f"/vnova/price?asset={asset}&quote={quote}&max_age_sec={int(max_age_sec)}")

    def vnova_health(self) -> Any:
        return self.get("/vnova/health")

    def vnova_overview(self) -> Any:
        return self.get("/vnova/overview")

    def ai_chat(
        self,
        *,
        messages: list[dict[str, str]],
        profile: Optional[str] = None,
        include_docs: Optional[bool] = None,
        wallet_id: Optional[str] = None,
    ) -> Any:
        payload: Dict[str, Any] = {"messages": messages or []}
        if profile is not None:
            payload["profile"] = profile
        if include_docs is not None:
            payload["include_docs"] = bool(include_docs)
        if wallet_id is not None:
            payload["wallet_id"] = wallet_id
        return self.post("/ai/chat", payload)

    def ai_docs_search(self, *, q: str, top_k: int = 8, max_chars: int = 2400) -> Any:
        q = str(q or "").strip()
        return self.get(f"/ai/docs/search?q={q}&top_k={int(top_k)}&max_chars={int(max_chars)}")

    def ai_qbit_context(self, *, max_chars: int = 2500, limit_blocks: int = 10) -> Any:
        return self.get(f"/ai/qbit/context?max_chars={int(max_chars)}&limit_blocks={int(limit_blocks)}")

    def mblk_spv_proof(self, *, digest: str, require_finalized: bool = True) -> Any:
        d = str(digest or "").strip()
        rf = "true" if bool(require_finalized) else "false"
        return self.get(f"/mblk/spv/proof?digest={d}&require_finalized={rf}")

    def explorer_qbtc_events(
        self,
        *,
        wallet: Optional[str] = None,
        entry_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Any:
        qs = [f"limit={int(limit)}", f"offset={int(offset)}"]
        if wallet:
            qs.append(f"wallet={wallet}")
        if entry_id:
            qs.append(f"entry_id={entry_id}")
        return self.get("/explorer/qbtc/events?" + "&".join(qs))

    def get(self, path: str) -> Any:
        path = path if path.startswith("/") else f"/{path}"
        return _json_request(f"{self.base_url}{path}")

    def post(self, path: str, payload: Dict[str, Any]) -> Any:
        path = path if path.startswith("/") else f"/{path}"
        return _json_request(f"{self.base_url}{path}", method="POST", payload=payload)


@dataclass(frozen=True)
class ProofWalletClient:
    base_url: str = "http://127.0.0.1:9756"

    def readyz(self) -> Any:
        """
        Return wallet readiness from /readyz.

        Note: ProofWallet uses /readyz (not /health).
        """
        return _json_request(f"{self.base_url}/readyz")

    def health(self) -> Any:
        # Back-compat alias; /health is not a stable ProofWallet endpoint.
        return self.readyz()

    def get(self, path: str) -> Any:
        path = path if path.startswith("/") else f"/{path}"
        return _json_request(f"{self.base_url}{path}")

    def post(self, path: str, payload: Dict[str, Any]) -> Any:
        path = path if path.startswith("/") else f"/{path}"
        return _json_request(f"{self.base_url}{path}", method="POST", payload=payload)

    def register_address(self, *, wallet: str, asset: str, address: str) -> Any:
        return self.post(
            "/wallet/address/register",
            {"wallet": wallet, "asset": asset, "address": address},
        )


@dataclass(frozen=True)
class NativeExplorerClient:
    """
    Optional connector surface (Native Explorer).

    Proofnet core does not require this service to be present, but apps may use
    it for convenience endpoints like the EVM address bridge.
    """

    base_url: str = "http://127.0.0.1:3006"

    def get(self, path: str) -> Any:
        path = path if path.startswith("/") else f"/{path}"
        return _json_request(f"{self.base_url}{path}")

    def post(self, path: str, payload: Dict[str, Any]) -> Any:
        path = path if path.startswith("/") else f"/{path}"
        return _json_request(f"{self.base_url}{path}", method="POST", payload=payload)

    def register_evm_address(self, *, wallet_id: str, evm_address: str, assets: Optional[list[str]] = None) -> Any:
        payload: Dict[str, Any] = {"wallet_id": wallet_id, "evm_address": evm_address}
        if assets is not None:
            payload["assets"] = assets
        return self.post("/bridge/evm/register", payload)

    # Native Explorer SDK surface (local-first orchestrator endpoints)
    def sdk_get(self, path: str) -> Any:
        path = path if path.startswith("/") else f"/{path}"
        return self.get("/sdk/v1" + path)

    def sdk_post(self, path: str, payload: Dict[str, Any]) -> Any:
        path = path if path.startswith("/") else f"/{path}"
        return self.post("/sdk/v1" + path, payload)

    def sdk_node_info(self) -> Any:
        return self.sdk_get("/node/info")

    def sdk_node_capabilities(self) -> Any:
        return self.sdk_get("/node/capabilities")

    def sdk_index_stats(self) -> Any:
        return self.sdk_get("/index/stats")

    def sdk_index_query(self, payload: Dict[str, Any]) -> Any:
        return self.sdk_post("/index/query", payload)

    def sdk_models_installed(self) -> Any:
        return self.sdk_get("/models/installed")

    def sdk_releases_list(self) -> Any:
        return self.sdk_get("/releases/list")

    def sdk_fees(self) -> Any:
        return self.sdk_get("/fees")
