from __future__ import annotations

import unittest
from unittest.mock import patch


class TestClientEndpoints(unittest.TestCase):
    def test_proofnet_health_aliases_api_status(self) -> None:
        from proofnet_sdk.client import ProofnetClient

        calls: list[str] = []

        def fake_json_request(url: str, method: str = "GET", payload=None):
            calls.append(url)
            return {"ok": True}

        with patch("proofnet_sdk.client._json_request", new=fake_json_request):
            client = ProofnetClient(base_url="http://127.0.0.1:25556")
            _ = client.health()

        self.assertEqual(calls, ["http://127.0.0.1:25556/api/status"])

    def test_proofwallet_health_aliases_readyz(self) -> None:
        from proofnet_sdk.client import ProofWalletClient

        calls: list[str] = []

        def fake_json_request(url: str, method: str = "GET", payload=None):
            calls.append(url)
            return {"ok": True}

        with patch("proofnet_sdk.client._json_request", new=fake_json_request):
            client = ProofWalletClient(base_url="http://127.0.0.1:9756")
            _ = client.health()

        self.assertEqual(calls, ["http://127.0.0.1:9756/readyz"])

    def test_get_prefixes_slash(self) -> None:
        from proofnet_sdk.client import ProofnetClient

        calls: list[str] = []

        def fake_json_request(url: str, method: str = "GET", payload=None):
            calls.append(url)
            return {"ok": True}

        with patch("proofnet_sdk.client._json_request", new=fake_json_request):
            client = ProofnetClient(base_url="http://127.0.0.1:25556")
            _ = client.get("api/status")

        self.assertEqual(calls, ["http://127.0.0.1:25556/api/status"])


if __name__ == "__main__":
    unittest.main()

