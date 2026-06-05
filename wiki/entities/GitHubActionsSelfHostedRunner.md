---
title: "GitHub Actions Self-Hosted Runner (macOS)"
type: entity
tags: [github-actions, ci, self-hosted-runner, macos, launchd, keychain]
sources: [keychain-not-found-multi-source-rca-2026-06-04.md]
last_updated: 2026-06-04
---

## Summary

A macOS self-hosted GitHub Actions runner installed as a launchd LaunchAgent (with
`SessionCreate=true`) that executes CI jobs for `jleechanorg` repos. Its git steps invoke
`git-credential-osxkeychain`, which reaches into the login keychain and — in a headless launchd
context — triggers the **"A keychain cannot be found to store 'X'"** popup (X often
`x-access-token` or `jleechan2015`). This is source #2 of the multi-source keychain popup RCA.

## Root Cause

The runner's CI git steps use the default global gitconfig, which on this machine sets
`credential.helper = osxkeychain`. Under the launchd security session there is no GUI keychain to
satisfy that helper, so SecurityAgent throws the modal.

## Fix

Add a CI-only gitconfig to the runner plist `EnvironmentVariables`:

```
GIT_CONFIG_GLOBAL = ~/actions-runner/ci.gitconfig
```

`ci.gitconfig` `include`s `~/.gitconfig` and then resets the credential helper to empty:

```gitconfig
[include]
    path = ~/.gitconfig
[credential]
    helper =
```

This disables osxkeychain for CI only. Interactive git (which uses the unmodified `~/.gitconfig`) is
unaffected.

## Connections
- [[macOSKeychain]] — the store the credential helper fails to reach under launchd.
- [[securityd]] — emits the SecurityAgent dialog when the helper probes the keychain.
- [[AgentOrchestrator]] — a separate (source #1) keychain popup origin with its own symlink fix.
