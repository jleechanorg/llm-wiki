---
name: feedback-2026-06-22-pr-evidence-gate-requires-anchor-url
description: "WorldArchitect Green Gate GATE-6 requires a real media/gist/loom/attachment URL in the PR body — plain \"N/A — no UI\" text fails even when the change is test-infra. Use --body-file (not --body \"$()\") when rewriting a long PR body."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 79a12801-6187-4144-846a-f1b1d003e14d
  bead: rev-m5obm
---

While driving PR #7815 (Mobile Auth Same-Origin Regression test timeout fix) to 7-green, hit two separate Green Gate GATE-6 / GATE-6b failures that were both description-shape issues, not code defects.

**Why:** Green Gate has two independent evidence gates:
- **GATE-6** (`green-gate.yml:451`) greps the PR body + comments for `https?://...\.mp4|\.gif|\.cast|gist.github.com/|asciinema.org/a/|loom.com/share/|user-attachments.githubusercontent.com/`. The "EVIDENCE_REQUIRED" check fires when the PR touches `testing_(mcp|ui)/|mvp_site/|deploy.sh|.github/workflows/evidence-gate.yml`. A run URL like `https://github.com/.../actions/runs/27992975784` does NOT match any of those patterns, so the gate fails even though the test passed.
- **GATE-6b** runs `.github/scripts/pr_description_gate.py` which requires each evidence section to contain a real URL or a backticked code block of ≥80 chars (`_section_has_anchor` at line 266, anchor requirement at lines 475-496). `## Non-Unit Test Evidence` always requires an anchor; `## Real LLM Evidence` only requires one if `touches_prompts` is true.

**How to apply:**
- For test-infra PRs (`testing_ui/**` or `testing_mcp/**`): add a gist with the test pass output and link it in BOTH the relevant `## *Test Evidence` section AND a trailing `## Evidence` link line. The GATE-6 grep matches `gist.github.com/` directly.
- For backend PRs: link a `/end2end-testing` payload or a raw LLM HTTP response in `## Non-Unit Test Evidence`.
- Never rely on `## Real LLM Evidence: N/A` to pass on its own unless the PR really doesn't touch `mvp_site/prompts/**` — the gate still wants a URL/code block in the other two evidence sections.

**Gotcha: `gh pr edit --body "$()"` silently wipes a long body.** When I ran `gh pr edit 7815 --body "$(gh pr view 7815 --json body --jq -r .body)\n\n---\n\n**Gist (test output):** ..."` to append a gist URL, the substitution left a 100-character stub body containing only the gist line — every canonical section vanished. Symptom: GATE-6b reports ~5 sections as "section header missing" simultaneously. **Fix: write the new body to a temp file and use `gh pr edit --body-file /tmp/body.md`.** Quote the file path with `--body-file` and avoid `$(...)` substitution for multiline content.
