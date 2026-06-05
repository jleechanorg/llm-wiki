---
title: "macOS keychain popup multi-source fix + AO skeptic gate ops 2026-06-05"
type: source
tags: [macos, keychain, security-authorizationdb, agent-orchestrator, skeptic-gate, ci-runner, cmux, mem0, qdrant]
date: 2026-06-05
source_file: ../raw/keychain_ao_skeptic_2026-06-05.md
---

## Summary
macOS "A keychain cannot be found to store X" popups have at least three independent headless sources — AO agy/Antigravity workers, GitHub Actions self-hosted runner CI git, and the cmux-codex-approve launchd worker — and ALL of them converge on the same authorization right `system.keychain.create.loginkc`. A single blanket `security authorizationdb write ... allow` suppresses every source at once; two per-source fixes were also merged. Includes AO Skeptic Gate operational lessons and mem0/qdrant fixes.

## Key Claims
- All three keychain-popup sources hit the SAME authorization right `system.keychain.create.loginkc`, so one blanket authorization change fixes them all.
- DECISIVE blanket fix: `sudo security authorizationdb write system.keychain.create.loginkc allow` — back up the rule first; reversible; persists across reboot.
- Per-source fix (MERGED): AO agy worker always symlinks session `Library/Keychains` to real `~/Library/Keychains` — agent-orchestrator PR #653.
- Per-source fix (MERGED): CI runner sets `GIT_CONFIG_GLOBAL` to a `ci.gitconfig` disabling osxkeychain in the runner launchd plist — jleechanclaw PR #592 (also added qdrant `--restart unless-stopped`).
- `securityd -25294` is benign probe noise (863 → 0 popups). Measure ACTUAL popups via `log show --predicate 'process == "SecurityAgent"'`; find the requesting client via `log show --predicate 'process == "authd"' | grep keychain.create.loginkc`.
- Killing AO workers breaks the Skeptic Gate (no verdict-poster → 20-min timeout) and regresses the agent-antigravity dist (AO rebuilds from the checked-out branch); durable fix = merge to main.
- Skeptic verdicts can be posted manually: `ao skeptic verify -n <PR> -m claude --trigger-sha <sha> --request-id <id>`; `--dry-run` previews, `--prompt` scopes evidence to the feasible class.
- Do NOT commit evidence `.md` files (trips CodeRabbit / Evidence Gate) — use gists.
- qdrant container needed `docker update --restart unless-stopped`; "~/.hermes/hermes.json missing" was a FALSE alarm (client reads `~/.hermes/config.yaml` with fallback defaults).

## Key Quotes
> "ALL hit the same authorization right `system.keychain.create.loginkc`" — root cause unifying 3 headless sources

## Connections
- [[system.keychain.create.loginkc]] — the shared authorization right behind all popups
- [[macOS keychain headless suppression]] — the blanket vs per-source fix strategy
- [[AO Skeptic Gate]] — verdict-poster dependency and manual verdict posting
- [[Agent Orchestrator]] — agy worker keychain symlink, dist rebuild from branch
- [[mem0 qdrant store]] — restart policy and config fallback
