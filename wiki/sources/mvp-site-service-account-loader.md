---
title: "mvp_site service_account_loader"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/service_account_loader.py
---

## Summary
Service Account Credentials Loader for secure Google Cloud authentication. Supports file-based (serviceAccount.json) and environment variable loading. Zero hardcoded secrets, git-safe template pattern.

## Key Claims
- Supports GOOGLE_PROJECT_ID, GOOGLE_CLIENT_EMAIL, GOOGLE_PRIVATE_KEY env vars
- GOOGLE_PRIVATE_KEY with \n escape sequences for PEM string
- Optional: GOOGLE_PRIVATE_KEY_ID, GOOGLE_CLIENT_ID
- Safe for git: no hardcoded secrets, env vars not committed

## Connections
- [[Validation]] — credentials management
