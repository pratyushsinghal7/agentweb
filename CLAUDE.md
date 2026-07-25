# Claude Code instructions

Read [AGENTS.md](AGENTS.md) for repository invariants and the required
verification commands, and [SKILL.md](SKILL.md) for how to *use* AgentWeb as a
tool. `llms.txt` is the documentation index; `docs/ARCHITECTURE.md` maps the
code.

Quick facts:

- Source lives in `src/agentweb`; tests in `tests/`; reference adapters in
  `src/agentweb/builtin_registry` (immutable, hash-pinned — never lint or edit
  released snapshots).
- Verify changes with `python -m pytest -q`, `python -m build`, and
  `PYTHONPATH=src python -m agentweb.cli audit`.
- Lint/format with ruff (see `pyproject.toml`); pre-commit mirrors CI.
