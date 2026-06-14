---
name: design-doc-gate0-artifact-inside-tenets
description: "Design Doc Gate 0 requires the .md/rev- artifact link INSIDE the Tenets/Design Decision section, not elsewhere in the PR body"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b02a0ef1-c69d-4d00-87b0-083d5297f59f
---

design-doc-gate.yml Gate 0 ("Design Decision prerequisite") extracts ONLY the `## Tenets` (or `## Design Decision` / `## Governing Design Doc & Tracking`) section via awk — the section ends at the next `## ` heading — then greps that extracted text for a linked artifact (`rev-[a-z0-9]+` or a `*.md` path). If non-test production .py delta > 50 lines and the Tenets section has no artifact link, Gate 0 FAILS even when a governing-doc link exists elsewhere (e.g. in `## Background`). The job fails fast (~10s).

**Why:** PR #7531 (level-up v2 PR-4) failed "Design Doc Grep Gates" with the governing-doc URL in `## Background` but the `## Tenets` section containing only prose bullets — the extractor stopped at the next `##` and found no `.md`/`rev-`.

**How to apply:** Put a `.md` path or `rev-xxxx` bead ref directly inside the Tenets/Design Decision section (a plain repo path like `docs/plans/foo.md` satisfies the regex). Fix is a body edit (`gh pr edit --body-file`), which also re-triggers the gate on the existing head — see [[feedback_2026-06-11_body_edit_triggers_fresh_green_gate]]. Line-count Gate 6 bound is 11100 for world_logic.py (11033 currently passes). Other grep gates (1–6) target rewards_engine/constants/llm_parser and don't fire for world_logic-only PRs.
