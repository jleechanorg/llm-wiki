---
title: "macOS Keychain Not Found popups — multi-source root cause and fixes"
type: source
tags: [macos, keychain, securityd, agent-orchestrator, github-actions, ci, launchd, zfc, headless]
date: 2026-06-04
source_file: raw/keychain-not-found-multi-source-rca-2026-06-04.md
---

# macOS "Keychain Not Found" popups — multi-source root cause and fixes

- **Raw source:** `~/llm_wiki/raw/keychain-not-found-multi-source-rca-2026-06-04.md`
- **md5:** `9da1806f9ca2f31f65db94eae62940c3` (49 lines)
- **Ingested:** 2026-06-04

## Summary
The recurring macOS popups "A keychain cannot be found to store 'X'" (X = `antigravity`,
`x-access-token`, `jleechan2015`) come from THREE independent headless processes that touch the
login keychain with no GUI security session. Each source has its own root cause and fix. The
overriding lesson: measure ACTUAL SecurityAgent dialog launches, not securityd `-25294` probe noise.

## Key Claims

### Three independent sources of the popup
1. **Agent Orchestrator `agy` (antigravity) workers** run under `$HOME=~/.ao-sessions/<id>`, which
   has no keychain. **Fix:** always symlink the session `Library/Keychains` → real
   `~/Library/Keychains`. The old code guessed headless-vs-interactive from `TERM_PROGRAM`/`COLORTERM`,
   but tmux sets those variables, so workers were misclassified — a ZFC violation (heuristic env
   sniffing standing in for a model/structural decision). PR
   [jleechanorg/agent-orchestrator#653](https://github.com/jleechanorg/agent-orchestrator/pull/653),
   commit `9712e8e15`.
2. **GitHub Actions self-hosted runner** (launchd LaunchAgent with `SessionCreate=true`) whose CI git
   steps invoke `git-credential-osxkeychain`. **Fix:** add
   `GIT_CONFIG_GLOBAL=~/actions-runner/ci.gitconfig` to the runner plist `EnvironmentVariables`.
   `ci.gitconfig` `include`s `~/.gitconfig` and then resets `[credential] helper=` to empty — disabling
   osxkeychain for CI only, leaving interactive git unaffected.
3. **`com.jleechan.cmux-codex-approve` launchd loop** — currently benign, but a third independent
   keychain-touching headless process to be aware of.

### Measurement lesson (the most important takeaway)
- securityd `MacOS error: -25294` (`errSecNoSuchKeychain`) is **constant internal probe noise** —
  863 of them produced **0** GUI dialogs.
- Measure ACTUAL popups via SecurityAgent dialog launches:
  `log show --predicate 'process == "SecurityAgent"'` — never `-25294` counts.
- Never click **"Reset To Defaults"** on a keychain prompt.

### `~/.bashrc` does not fix git keychain popups
- Sourcing `~/.bashrc` does NOT fix git keychain popups: the credential helper lives in gitconfig,
  not env, and bashrc deliberately disables `GITHUB_TOKEN`/`GH_TOKEN`.
- Always check the **worker's actual `$HOME`**, not your own shell's.

## Key Quotes
> "A keychain cannot be found to store 'X'" — the popup text; X is `antigravity`, `x-access-token`, or `jleechan2015`.

## Connections
- [[AgentOrchestrator]] — `agy`/antigravity workers run under a session `$HOME` lacking a keychain; symlink fix in PR #653.
- [[GitHubActionsSelfHostedRunner]] — launchd runner with `SessionCreate=true` triggers `git-credential-osxkeychain` in CI; fixed via `GIT_CONFIG_GLOBAL`.
- [[macOSKeychain]] — login keychain access from headless sessions with no GUI security session is the common failure mode.
- [[securityd]] — `-25294` (`errSecNoSuchKeychain`) is benign probe noise, not a popup signal; measure SecurityAgent dialogs instead.
- [[ZeroFrameworkCognition]] — guessing headless-vs-interactive from `TERM_PROGRAM`/`COLORTERM` is a ZFC violation (tmux sets those vars).
