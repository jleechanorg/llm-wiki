---
title: Grep on gh-pr-diff false-positives via .beads/issues.jsonl prose
date: 2026-06-07
type: source
origin: worldarchitect.ai /learn (session 6f4e0216)
bead: rev-15x97
tags: [verification, beads, grep, pr-review, false-positive, dice, code-execution]
---

# Grep on `gh pr diff` false-positives via `.beads/issues.jsonl` prose

**Lesson:** Verifying whether a PR's **code** sets/contains a symbol with
`gh pr diff <PR> | grep <symbol>` is unreliable. The combined diff includes the
1MB+ `.beads/issues.jsonl` DB export, and bead-description PROSE quotes code
symbols, file paths, and flag names verbatim — so the grep matches *descriptions*,
not *code changes*.

**Incident (PR #7330):** Verifying a claim that #7330 attaches the code-execution
tool but never sets `debug_info["code_execution_used"]` (so the dice persistence
gate never fires). `gh pr diff 7330 | grep code_execution_used` returned **3
matches** — appearing to refute the claim. All 3 were inside `.beads/issues.jsonl`
bead prose, **0 in production code**. Re-scoping to the source hunk confirmed the
claim (step-1-only fix). The false positive nearly inverted the verdict.

**Corrective procedure:**

```bash
gh pr diff <PR> --name-only                       # confirm file is touched
gh pr diff <PR> | awk '/^diff --git.*FILE/{f=1} /^diff --git/&&!/FILE/{f=0} f' | grep <symbol>
git show <PR_head_sha>:path/to/file.py | grep -n <symbol>   # read the blob directly
```

Verify the gate side by reading the file, not the diff: gate was at
`mvp_site/dice_integrity.py:634` (`if not debug_info.get("code_execution_used"):`).

**Generalization:** Same error class as `gh pr checks | grep -c fail` (matches
check NAMES, not statuses). In any beads-tracked repo, never treat a raw
`gh pr diff | grep <code-symbol>` count as proof of a code change. Pairs with the
standing rule: never read `.beads/*.jsonl` whole — use the `br` CLI.

**Refs:** PR #7330 (CLOSED, subsumed) · PR #7280 (OPEN, superset; adds
`mvp_site/dice_code_execution_audit.py`) · bead rev-15x97 · cluster bead rev-ncugf.

See also: [[verification-discipline]], [[beads]]
