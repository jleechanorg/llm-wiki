---
title: "File-Level Audit"
type: concept
tags: ["audit", "methodology", "code-review"]
sources: ["smartclaw-ao-exhaustive-audit-findings-file-level-sweep.md"]
last_updated: 2026-04-07
---

Audit methodology that compares files at the path level before scoring capabilities.

## Method
1. `rg --files` to get tracked paths
2. Full read pass for coverage
3. Verify key capability claims against implementation files

## Audit Results
- mctrl: 25 tracked files
- jleechanclaw: 188 tracked files
- worldarchitect.ai: 4,136 tracked files

## Connections
- [[mctrl]] — audited
- [[jleechanclaw]] — audited
- [[worldarchitect.ai]] — audited
- [[AgentOrchestrator]] — reference baseline
