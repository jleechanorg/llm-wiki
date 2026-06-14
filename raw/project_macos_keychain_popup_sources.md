---
name: project_macos_keychain_popup_sources
description: "Root causes + fixes for recurring macOS 'Keychain Not Found' popups (antigravity / x-access-token / jleechan2015) — multiple independent headless sources"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0856e99f-c5c9-4754-9c31-17bf03a53924
---

## macOS "A keychain cannot be found to store 'X'" popups — there are MULTIPLE independent headless sources

The recurring popups are NOT a single bug. Three independent headless processes hit the
login keychain with no GUI (Aqua) security session, so macOS throws SecurityAgent dialogs:

1. **AO `agy` (antigravity) workers** — run under `$HOME=~/.ao-sessions/<id>` where
   `$HOME/Library/Keychains` doesn't exist. Popup names: `antigravity` (OAuth token).
   **Fix (proven, PR jleechanorg/agent-orchestrator#653):** in
   `packages/plugins/agent-antigravity/src/index.ts`, ALWAYS symlink the session
   `Library/Keychains` → real `~/Library/Keychains`. The old code guessed headless-vs-
   interactive from `TERM_PROGRAM`/`COLORTERM`; tmux sets those, so every worker was
   misclassified as interactive and the bypass never ran (ZFC violation). Net −64 LOC.

2. **GitHub Actions self-hosted runner** (`actions.runner.jleechanorg.wa-oss-runner-local`,
   `/Users/jleechan/actions-runner/`) — runs as a launchd LaunchAgent with `SessionCreate=true`
   → own session without the login keychain. CI job `git`/`gh` steps invoke
   `git-credential-osxkeychain` (from `~/.gitconfig` `[credential] helper = osxkeychain`).
   Popup names: `x-access-token`, `jleechan2015`. **Fix:** added to the runner's launchd plist
   `EnvironmentVariables`: `GIT_CONFIG_GLOBAL=/Users/jleechan/actions-runner/ci.gitconfig`
   (a file that `[include]`s `~/.gitconfig` then resets `[credential] helper =` empty) +
   `GIT_TERMINAL_PROMPT=0`. Reload with `launchctl bootout gui/501/<label>` then
   `launchctl bootstrap gui/501 <plist>`. Confirmed: CI jobs write `safe.directory` into
   ci.gitconfig, proving inheritance. Interactive git is UNAFFECTED (still osxkeychain).

3. **`com.jleechan.cmux-codex-approve`** launchd loop — historically a source (see
   [[never-kill-active-user-app-cmux]] / 2026-05-29). Currently NOT popping (its errors are
   benign network -999, not keychain). Leave running.

## DECISIVE fix (2026-06-04): suppress the authorization right itself

Per-source fixes are whack-a-mole — agy, the CI runner, cmux-codex-approve, and sporadic
other `security`/`git-credential-osxkeychain` callers ALL hit the SAME prompt:
`system.keychain.create.loginkc` (the "create a login keychain?" SecurityAgent dialog,
authd mechanism `loginKC:queryCreate`). The single lever that kills ALL of them regardless
of source:

```bash
# back up first (reversible)
security authorizationdb read system.keychain.create.loginkc > ~/keychain-create-loginkc.rule.backup.plist
# suppress the prompt (auto-allow, no dialog) — needs sudo
sudo security authorizationdb write system.keychain.create.loginkc allow
# restore later:  sudo security authorizationdb write system.keychain.create.loginkc < ~/keychain-create-loginkc.rule.backup.plist
```

This changes the right from `class=evaluate-mechanisms` (prompts) to `rule=[allow]` (silent).
Headless processes that can't find a login keychain then resolve silently instead of popping.
Low-risk: the user already has a login keychain so legitimate creation never triggers.

Diagnose the live source via authd (NOT -25294 noise):
`log show --last 5m --predicate 'process == "authd"' | grep keychain.create.loginkc` →
shows `by client '<path>' [pid]`. cmux-codex-approve was confirmed by pausing it
(`launchctl bootout gui/501/com.jleechan.cmux-codex-approve`) and watching the rate drop to 0.

## cmux-codex-approve worker is a recurring source
Its launchd plist has `OPENAI_API_KEY=""` (empty) and no ANTHROPIC/CLAUDE token, so the
`codex`/`claude` CLIs it spawns to classify dialogs fall back to the keychain via `security`.
The authd suppression above makes it stop popping; a per-source fix would be giving it real
API keys via env (it does NOT source ~/.bashrc).

## CRITICAL diagnostic lesson: -25294 log spam ≠ actual popups

`securityd` logs `MacOS error: -25294` (errSecNoSuchKeychain) constantly as internal probe
noise — the runner threw 863 of them and produced ZERO GUI dialogs. **Do not measure popups
by `-25294` count.** Measure ACTUAL popups via SecurityAgent dialog launches:
`log show --last 60m --predicate 'process == "SecurityAgent"'` (cluster timestamps = real
dialogs). Also: `pgrep -f SecurityAgent` = dialog up now; dismiss with
`pkill -9 -f SecurityAgent` (or `/keychain_kill`). NEVER click "Reset To Defaults" — the
login keychain is healthy; reset can orphan saved passwords.

## Also relevant
- First-pass mistake: inspecting the keychain from your own shell's `$HOME` shows it healthy;
  the failing workers run under a DIFFERENT `$HOME`. Always check the worker's actual HOME.
- AO lifecycle workers are orphan daemons (PPID 1); `ao stop --all` only stops things tracked
  in running.json. `ao start <path>` revives lifecycle workers that then respawn `agy`.
