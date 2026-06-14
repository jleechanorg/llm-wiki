---
title: "Green Gate GATE-6 is a Hard Evidence-Link Regex with NO Docs-Only/N-A Escape"
type: source
tags: ["green-gate", "evidence", "worldarchitect-ai", "gate-6"]
date: 2026-06-04
source_file: project_2026-06-04_green_gate_gate6_hard_evidence.md
---

## Summary
`.github/workflows/green-gate.yml` lines 458-469: GATE-6 sets EVIDENCE_REQUIRED=true whenever changed files match `^(testing_(mcp|ui)/|mvp_site/|deploy\.sh$|\.github/workflows/evidence-gate\.yml$)`. HAS_EVIDENCE is true only if PR body+comments match the regex `https?://[^ ]*\.(mp4|gif|cast)|gist\.github\.com/|asciinema\.org/a/|loom\.com/share/|user-attachments\.githubusercontent\.com/`.

## Key Claims
- NO label, N/A, or docs-only bypass — any PR touching mvp_site/** cannot go green without a real media/gist evidence link
- PRs #7246 and #7247 reach Gates 1-5 PASS and fail ONLY GATE-6
- When change has no LLM/streaming/state-persistence behavior, fabricating a real-LLM /es run is forbidden — report GATE-6 as hard meta-gate blocker
- reviewDecision stays "" even with CodeRabbit APPROVED (CodeRabbit not CODEOWNERS-required reviewer)

## Key Quotes
> Consequence: PRs touching mvp_site/** — even a string-only tool-description doc change (#7246) or a pure unit-testable detector field-source change (#7247) — cannot make the Green Gate check go green without a real media/gist evidence link

## Connections
- [[GreenGate]] — concept
- [[EvidenceStandards]] — full claim class definitions
