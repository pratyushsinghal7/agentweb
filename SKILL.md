---
name: agentweb
description: >-
  Use websites as fast, typed CLI commands instead of a browser. AgentWeb
  exposes mapped website operations (read data and take confirmed actions on
  sites like npm, arXiv, Wikipedia, GitHub, Hacker News, Amazon, Spotify) as
  JSON-returning shell commands. Use this skill whenever a task needs live
  website data or a website action and the site is in `agentweb sites`.
license: Apache-2.0
compatibility: Claude Code, Codex, and any coding agent with shell access
---

# AgentWeb

AgentWeb turns a website into simple, typed commands that return clean JSON.
Reads look things up; acts do real things on the user's accounts and require an
explicit `--confirm` for impactful or irreversible operations.

## When to use

- The task needs live data from a mapped website (package metadata, papers,
  wiki content, jobs, models, questions, stories).
- The task needs a real website action (play a song, manage a cart, open a
  pull request, post or vote) without driving a browser.

Check support first; never guess:

```bash
agentweb sites
```

## When not to use

- The site is not listed in `agentweb sites` and no adapter is installed.
- The operation reports `declared_gaps` covering exactly what you need.
- A website-mandated human checkpoint (CAPTCHA, passkey, OTP, payment
  confirmation, legal consent) is required — hand that step to the user.

## Quick reference

```bash
agentweb sites                                        # which websites are installed
agentweb capabilities npmjs.com --query download      # find the operation
agentweb describe npmjs.com --operation get_download_count   # one schema, on demand
agentweb npmjs.com get-download-count --package react --period last-week
agentweb --compact npmjs.com get-package --package react     # machine-friendly output
agentweb run npmjs.com get_download_count --input '{"package":"react","period":"last-week"}'
agentweb get https://arxiv.org/abs/1706.03762         # typed route for a normal URL
```

Do not load every schema preemptively; `describe` only the operation you will
call.

## Authentication

Try public operations first. On `authentication_required`, ask the user to run:

```bash
agentweb connect example.com
```

then retry the original call. Never copy browser cookies into chat, logs, or
command arguments.

## Writes

Treat an operation as mutating when its contract says so. Read current state
when practical, resolve ambiguous targets and totals, confirm the user's
request authorizes the specific action, pass the explicit `confirm` value, and
inspect the returned verification instead of assuming success.

## Errors

Expected failures are JSON on stderr. Key classes: `missing_input` /
`invalid_input` (fix the arguments), `authentication_required` (ask the user to
connect), `rate_limited` (respect the returned delay; no retry loops),
`human_required` (hand off only that checkpoint), `flow_drift` (the website
changed; stop relying on that operation and report it).

## Full guide

Read `docs/AGENT_GUIDE.md` for the complete execution loop, and `llms.txt` for
the documentation index. MCP-only hosts can use the four-tool MCP server:
`agentweb mcp-config` prints the configuration snippet.
