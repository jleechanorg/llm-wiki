---
title: "Cross-Repo Delegation"
type: concept
tags: [delegation, cross-repo, github, workflow]
sources: [smartclaw-routing-delegation-failures-postmortem.md]
last_updated: 2026-04-07
---

## Description
The practice of delegating AI agent work to be performed in a repository different from the current working context. The March 2026 incident demonstrated that cross-repo delegation requires explicit contract (SOURCE_REPO/TARGET_REPO) to avoid routing to wrong repository.

## Key Requirements
1. Explicit SOURCE_REPO and TARGET_REPO headers in dispatch
2. Mandatory pre-PR repo identity validation
3. Fresh session resets when contamination occurs
4. Proof bundle (file paths, commit URL, PR URL) before completion

## Prevention Rules
- No cross-repo delegation without explicit SOURCE/TARGET contract
- Any repo mismatch triggers immediate stop + correction
