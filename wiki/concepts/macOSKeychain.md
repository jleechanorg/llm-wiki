---
title: "macOS Keychain"
type: concept
tags: [macos, keychain, security, securityd, headless, ci, authorizationdb, loginkc]
sources: [keychain-not-found-multi-source-rca-2026-06-04.md, keychain-ao-skeptic-2026-06-05.md]
last_updated: 2026-06-05
---

## Summary

The macOS login keychain is a per-user encrypted credential store unlocked by a GUI security
session. Headless processes (launchd agents, AO worker `$HOME`s, CI runners) that try to read or
write the login keychain without a GUI session trigger the modal popup
**"A keychain cannot be found to store 'X'"**. The popup is a symptom of *where the process's `$HOME`
and security session point*, not of a corrupt keychain.

## Failure Mode

A process touches the login keychain (directly, or via `git-credential-osxkeychain`) while running
under a `$HOME` that has no `Library/Keychains`, or in a launchd context with no interactive security
session. macOS then surfaces a modal asking the user to create/locate a keychain.

## Observed Trigger Sources

See [[AgentOrchestrator]], [[GitHubActionsSelfHostedRunner]], and the
`com.jleechan.cmux-codex-approve` launchd loop — three independent headless processes documented in
the 2026-06-04 multi-source RCA.

**Common authorization right (2026-06-05):** all three sources hit the *same* authorization right
`system.keychain.create.loginkc`. Confirm the requesting client with:
`log show --predicate 'process == "authd"' | grep keychain.create.loginkc`. Because they converge
on one right, a single blanket authorization change suppresses every source at once.

## Decisive Blanket Fix (2026-06-05)

```bash
sudo security authorizationdb write system.keychain.create.loginkc allow
```

- Back up the existing rule first (read it before overwriting).
- Reversible, and persists across reboot.
- Suppresses the prompt for **every** source simultaneously — use this when per-source fixes are
  not yet deployed everywhere.

## Diagnostic Discipline

- **Measure real popups, not probe noise.** securityd `MacOS error: -25294` (`errSecNoSuchKeychain`)
  is constant internal probing — 863 occurrences produced **0** GUI dialogs. Count actual
  [[securityd]] SecurityAgent dialog launches instead:
  `log show --predicate 'process == "SecurityAgent"'`.
- **Never click "Reset To Defaults"** on the popup.
- **Check the worker's actual `$HOME`**, not your shell's — the failing process usually has a
  different `$HOME` than your interactive terminal.
- **`~/.bashrc` is not a fix** for git keychain popups: the credential helper lives in gitconfig, not
  env, and bashrc deliberately disables `GITHUB_TOKEN`/`GH_TOKEN`.

## Fixes (per source — both MERGED 2026-06-05)

- **AO worker `$HOME`:** always symlink session `Library/Keychains` → real `~/Library/Keychains` —
  agent-orchestrator PR #653.
- **CI git:** point the runner at a CI-only gitconfig via `GIT_CONFIG_GLOBAL` that resets
  `[credential] helper=` empty, disabling osxkeychain for CI without affecting interactive git —
  jleechanclaw PR #592 (the same PR also added qdrant `--restart unless-stopped`).

## Connections
- [[securityd]] — the daemon that emits `-25294` probe noise and launches SecurityAgent dialogs.
- [[AgentOrchestrator]] — source #1 of the popup.
- [[GitHubActionsSelfHostedRunner]] — source #2 of the popup.
- [[ZeroFrameworkCognition]] — env-sniffing to detect headless mode is a ZFC violation.
