"""Regenerate llms-full.txt from the repository documentation.

Usage: python scripts/build_llms_full.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SOURCES = [
    "README.md",
    "AGENTS.md",
    "SKILL.md",
    "docs/README.md",
    "docs/AGENT_GUIDE.md",
    "docs/AGENT_HOSTS.md",
    "docs/ARCHITECTURE.md",
    "docs/BUILDING_ADAPTERS.md",
    "docs/SECURITY.md",
    "docs/ANALYTICS.md",
    "CONTRIBUTING.md",
]

HEADER = """\
# AgentWeb — full documentation

This file concatenates the repository documentation for one-shot ingestion by
LLMs and agents. The index lives in llms.txt. Each section names its source
file; sources in the repository are authoritative if this file is stale.
Regenerate with: python scripts/build_llms_full.py
"""


def main() -> None:
    parts = [HEADER]
    for rel in SOURCES:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8").strip()
        parts.append(f"\n---\n\nSource: {rel}\n\n{text}\n")
    (ROOT / "llms-full.txt").write_text("".join(parts), encoding="utf-8", newline="\n")
    print(f"wrote llms-full.txt from {len(SOURCES)} sources")


if __name__ == "__main__":
    main()
