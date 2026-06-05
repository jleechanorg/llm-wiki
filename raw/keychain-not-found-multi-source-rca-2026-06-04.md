---
title: "macOS Keychain Not Found popups — multi-source root cause and fixes"
type: source
tags: [macos, keychain, securityd, agent-orchestrator, github-actions, ci, launchd, zfc, headless]
date: 2026-06-04
source_file: raw/keychain-not-found-multi-source-rca-2026-06-04.md
---

## Summary
The recurring macOS popups "A keychain cannot be found to store 'X'" (X = antigravity,
x-access-token, jleechan2015) come from THREE independent headless processes that touch the
login keychain with no GUI security session. Root causes and fixes are documented per source.
The key lesson: measure ACTUAL SecurityAgent dialog launches, not securityd -25294 probe noise.

## Key Claims

### Three independent sources of the popup
1. **Agent Orchestrator `agy` (antigravity) workers** running under `$HOME=~/.ao-sessions/<id>`
   (no keychain there). Fix: always symlink session `Library/Keychains` → real
   `~/Library/Keychains`. Old code guessed headless-vs-interactive from `TERM_PROGRAM`/`COLORTERM`,
   but tmux sets those so workers were misclassified (ZFC violation).
   PR jleechanorg/agent-orchestrator#653, commit `9712e8e15`.
2. **GitHub Actions self-hosted runner** (launchd LaunchAgent, `SessionCreate=true`) whose CI git
   steps invoke `git-credential-osxkeychain`. Fix: add `GIT_CONFIG_GLOBAL=~/actions-runner/ci.gitconfig`
   to the runner plist `EnvironmentVariables`; `ci.gitconfig` includes `~/.gitconfig` then resets
   `[credential] helper=` empty (disables osxkeychain for CI only; interactive git unaffected).
3. **`com.jleechan.cmux-codex-approve` launchd loop** — currently benign.

### Measurement lesson (most important)
- securityd `MacOS error: -25294` (`errSecNoSuchKeychain`) is constant internal probe noise —
  **863 of them produced 0 GUI dialogs**.
- Measure ACTUAL popups via SecurityAgent dialog launches:
  `log show --predicate 'process == "SecurityAgent"'`, NOT -25294 counts.
- Never click "Reset To Defaults".

### bashrc does not fix git keychain popups
- Sourcing `~/.bashrc` does NOT fix git keychain popups (the credential helper is in gitconfig,
  not env; bashrc deliberately disables `GITHUB_TOKEN`/`GH_TOKEN`).
- Always check the worker's actual `$HOME`, not your own shell's.

## Key Quotes
> "A keychain cannot be found to store 'X'" — the popup text; X is antigravity, x-access-token, or jleechan2015.

## Connections
- [[AgentOrchestrator]] — `agy`/antigravity workers run under a session `$HOME` lacking a keychain; symlink fix in PR #653.
- [[GitHubActionsSelfHostedRunner]] — launchd runner with SessionCreate=true triggers git-credential-osxkeychain in CI.
- [[macOSKeychain]] — login keychain access from headless sessions with no GUI security session.
- [[ZeroFrameworkCognition]] — guessing headless-vs-interactive from TERM_PROGRAM/COLORTERM is a ZFC violation (tmux sets those vars).
- [[securityd]] — -25294 (errSecNoSuchKeychain) is benign probe noise; not a popup signal.
