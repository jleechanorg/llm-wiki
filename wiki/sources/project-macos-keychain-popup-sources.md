---
title: "macOS Keychain Popup Sources — Multi-Source Fix"
type: source
tags: ["macos", "keychain", "authd", "securityagent", "fix"]
date: 2026-06-04
source_file: project_macos_keychain_popup_sources.md
---

## Summary
The recurring 'Keychain Not Found' popups are NOT a single bug. Three independent headless processes hit the login keychain with no GUI security session. DECISIVE fix: suppress the `system.keychain.create.loginkc` authorization right via `security authorizationdb write ... allow`.

## Key Claims
- Three sources: AO agy workers (session HOME symlink fix PR #653), GitHub Actions self-hosted runner (GIT_CONFIG_GLOBAL), cmux-codex-approve (recurring, empty OPENAI_API_KEY)
- Decisive fix: `sudo security authorizationdb write system.keychain.create.loginkc allow` (changes from `evaluate-mechanisms` to `rule=[allow]`)
- CRITICAL diagnostic lesson: -25294 log spam ≠ actual popups. Measure via SecurityAgent dialog launches, NOT securityd -25294 count

## Key Quotes
> Per-source fixes are whack-a-mole — agy, CI runner, cmux-codex-approve ALL hit the SAME prompt

## Connections
- [[MacOSKeychain]] — concept page
