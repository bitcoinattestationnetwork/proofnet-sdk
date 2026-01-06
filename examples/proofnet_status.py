from __future__ import annotations

import json

from proofnet_sdk import ProofnetClient, ProofWalletClient


def main() -> None:
    pn = ProofnetClient()
    pw = ProofWalletClient()
    print("Proofnet /api/status:")
    print(json.dumps(pn.status(), indent=2, sort_keys=True))
    print()
    print("ProofWallet /readyz:")
    print(json.dumps(pw.readyz(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
