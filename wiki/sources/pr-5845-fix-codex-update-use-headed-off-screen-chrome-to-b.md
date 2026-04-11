---
title: "PR #5845: fix(codex-update): use headed off-screen Chrome to bypass Cloudflare bot detection"
type: source
tags: []
date: 2026-03-04
source_file: raw/prs-worldarchitect-ai/pr-5845.md
sources: []
last_updated: 2026-03-04
---

## Summary
- Headless Playwright is blocked by Cloudflare even with `playwright-stealth` — title stays "Just a moment..." indefinitely
- Switch to headed Chrome with `--window-position=-32000,-32000` (off-screen, invisible to user) which passes Cloudflare checks
- Apply `playwright_stealth` patches for additional bot evasion hardening

## Metadata
- **PR**: #5845
- **Merged**: 2026-03-04
- **Author**: jleechan2015
- **Stats**: +139/-5 in 5 files
- **Labels**: none

## Connections
