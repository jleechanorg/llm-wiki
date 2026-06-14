---
name: 7-green proof artifact is the github-actions VERDICT comment
description: Proof of 7-green for a PR is the github-actions[bot] "VERDICT: PASS" comment with `<!-- skeptic-head-sha-XXX -->` marker; not gh pr checks or any other surrogate
type: feedback
bead: rev-igs3c
---

The canonical proof artifact for "PR is at 7-green" is a comment posted by
`github-actions[bot]` (not `coderabbitai`, not a check-run status) that
literally contains the text `VERDICT: PASS` plus an HTML comment marker
`<!-- skeptic-head-sha-<HEAD_SHA> -->`. The comment is produced by
`skeptic-self-verify.yml`. It enumerates all 8 gates and shows PASS for each.

**Why:** previously I'd been treating "all checks SUCCESS in `gh pr checks`"
as proof. That is necessary but not sufficient. The skeptic-self-verify
workflow runs AFTER `Green Gate` succeeds and writes the binding evidence.

**How to apply:**
- To prove 7-green, query:
  `gh pr view <N> --json comments --jq '.comments[] | select(.body | test("VERDICT: PASS")) | select(.body | test("<HEAD_SHA>"))'`
- A comment must exist matching BOTH `VERDICT: PASS` AND the current HEAD SHA marker.
- The 8 gates are: CI passing, no merge conflicts, CodeRabbit APPROVED (status+comment),
  Cursor Bugbot, inline comments resolved, evidence, self-verify, smoke gate.
- `Green Gate` itself often **runs twice** per HEAD — the first run typically
  FAILS with `GATE-1 FAIL: CI=pending` (it kicks off immediately on push,
  before CI/CR/Skeptic complete). A second `Green Gate` run triggers after the
  cycle. Always check the LATEST `Green Gate` run per HEAD, not "any FAILURE".

**Verification (this session):**
- PR #7048 produced two valid VERDICT: PASS comments:
  - 2026-05-24T06:15:18Z for HEAD `7ea51b546c` (comment 4527591720)
  - 2026-05-24T06:26:10Z for HEAD `e979224079` (comment 4527601295)
- PR merged at 2026-05-24T07:09:07Z (merge sha `25cee34d6f`).

**Pattern (reusable):**
```bash
# Check 7-green proof for current PR HEAD
head=$(gh pr view 7048 --json headRefOid --jq .headRefOid)
gh pr view 7048 --json comments --jq \
  ".comments[] | select(.author.login == \"github-actions[bot]\") |
   select(.body | test(\"VERDICT: PASS\")) |
   select(.body | test(\"$head\")) | .html_url"
# If output is empty -> 7-green NOT proven for this HEAD.
```

Related: [[green-gate-timing]], [[pr-green-definition]]
