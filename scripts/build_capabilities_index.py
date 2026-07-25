"""Regenerate capabilities.json from the built-in reference registry.

Usage: python scripts/build_capabilities_index.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITES = ROOT / "src" / "agentweb" / "builtin_registry" / "sites"

NOTE = (
    "Machine-readable index of the reference adapters shipped in this "
    "repository. The full installer catalog is larger; run `agentweb sites` "
    "and `agentweb capabilities DOMAIN` for the live inventory. Regenerate "
    "with: python scripts/build_capabilities_index.py"
)


def main() -> None:
    out = {
        "generated_from": "src/agentweb/builtin_registry",
        "note": NOTE,
        "sites": [],
    }
    for site_dir in sorted(SITES.iterdir()):
        for version_dir in sorted(site_dir.iterdir()):
            manifest = json.loads(
                (version_dir / "manifest.json").read_text(encoding="utf-8")
            )
            commands = manifest.get("commands", {})
            contracts = manifest.get("operation_contracts", {})
            operations = []
            for name in sorted(set(commands) | set(contracts)):
                entry: dict[str, object] = {"operation": name}
                command = commands.get(name)
                contract = contracts.get(name)
                description = None
                if isinstance(command, dict):
                    description = command.get("description")
                if not description and isinstance(contract, dict):
                    description = contract.get("description")
                if description:
                    entry["description"] = description
                if isinstance(contract, dict) and contract.get("mutating") is not None:
                    entry["mutating"] = contract["mutating"]
                operations.append(entry)
            out["sites"].append(
                {
                    "name": manifest.get("name"),
                    "version": manifest.get("version"),
                    "canonical_domain": manifest.get("canonical_domain"),
                    "base_url": manifest.get("base_url"),
                    "description": manifest.get("description"),
                    "operations": operations,
                }
            )
    (ROOT / "capabilities.json").write_text(
        json.dumps(out, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(
        "wrote capabilities.json:",
        [(s["name"], len(s["operations"])) for s in out["sites"]],
    )


if __name__ == "__main__":
    main()
