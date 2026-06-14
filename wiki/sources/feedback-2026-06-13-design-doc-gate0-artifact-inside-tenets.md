---
title: "2026-06-13 Design Doc Gate0 Artifact Inside Tenets"
type: source
tags: ["feedback", "worldarchitect"]
date: 2026-06-13
source_file: raw/feedback_2026-06-13_design_doc_gate0_artifact_inside_tenets.md
---

## Summary
Design Doc Gate 0 requires the .md/rev- artifact link INSIDE the Tenets/Design Decision section, not elsewhere in the PR body

## Key Claims
- design-doc-gate.yml Gate 0 ("Design Decision prerequisite") extracts ONLY the `## Tenets` (or `## Design Decision` / `## Governing Design Doc & Tracking`) section via awk — the section ends at the next `## ` heading — then greps that extracted text for a linked artifact (`rev-[a-z0-9]+` or a `*.md` path). If non-test production .py delta > 50 lines and the Tenets section has no artifact link, Gate 0 FAILS even when a governing-doc link exists elsewhere (e.g. in `## Background`). The job fails fast (~10s).

## Connections
- [[feedback_2026-06-11_body_edit_triggers_fresh_green_gate]]
