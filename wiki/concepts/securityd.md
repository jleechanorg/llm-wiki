---
title: "securityd / SecurityAgent"
type: concept
tags: [macos, security, securityd, keychain, logging]
sources: [keychain-not-found-multi-source-rca-2026-06-04.md]
last_updated: 2026-06-04
---

## Summary

`securityd` is the macOS security daemon that mediates keychain access; `SecurityAgent` is the
process that renders the user-facing modal dialogs (e.g. keychain-not-found, unlock prompts). The
critical distinction for debugging keychain popups: `securityd` emits constant internal probe errors
that are NOT popups, while `SecurityAgent` dialog launches ARE the real popups to measure.

## The -25294 Trap

`securityd` continuously logs `MacOS error: -25294` (`errSecNoSuchKeychain`) as benign internal
probing. In the 2026-06-04 RCA, **863 of these errors produced 0 GUI dialogs**. Counting `-25294` as
a proxy for popups is a false signal that wastes debugging effort.

## Correct Measurement

Measure actual popups via SecurityAgent dialog launches:

```bash
log show --predicate 'process == "SecurityAgent"'
```

A SecurityAgent launch corresponds to a real modal the user sees; a `-25294` does not.

## Connections
- [[macOSKeychain]] — the store whose access these processes mediate.
- [[GitHubActionsSelfHostedRunner]] — CI git invokes the credential helper that reaches securityd.
- [[AgentOrchestrator]] — AO workers under a keychain-less `$HOME` trip SecurityAgent dialogs.
