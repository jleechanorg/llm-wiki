---
title: "Competing-PR subsumption — close the subset, migrate follow-ups to the superset"
date: 2026-06-07
type: source
tags: [pr-workflow, verification, merge-discipline]
bead: rev-15x97
---

When two OPEN PRs implement overlapping fixes touching the **same production files** and one is a strict superset, do not merge the subset. Close it as **subsumed** and migrate its unique follow-ups to a comment on the superset.

**Incident:** PR #7330 (4 files) attached `types.Tool(code_execution={})` but never set `debug_info["code_execution_used"]`, so the persistence gate `mvp_site/dice_integrity.py:634` never fired — an inert half-fix. PR #7280 (38 files) is the strict superset (attaches tool + sets the flag + adds `dice_code_execution_audit.py`). Both touch `gemini_provider.py` + `test_streaming_orchestrator.py` → textual conflict. Resolution: close #7330 subsumed, keep #7280, migrate caveats to a #7280 comment.

```bash
# Confirm overlap and superset, then close the subset:
gh pr diff <subset> --name-only ; gh pr diff <superset> --name-only      # compare file sets
# read the PRODUCTION hunks to confirm superset — NOT a raw `gh pr diff | grep`
gh pr close <subset> --comment "Subsumed by #<superset>: <reason>"
# migrate unique follow-ups to a comment on <superset> BEFORE closing
```

Closing-as-subsumed is allowed under the human MERGE-APPROVED gate; merging the superset is not.

See also [[verification-discipline]], [[beads]], [[sources/2026-06-07-grep-beads-false-positive-pr-verification]].
