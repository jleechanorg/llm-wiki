---
name: grep-on-gh-pr-diff-gives-false-positives-beads-jsonl-prose-hunk-isolate-the-source-file
description: "Verifying a code-symbol claim with grep over `gh pr diff` is wrong — `.beads/issues.jsonl` prose matches code symbols; isolate the production-file hunk"
metadata: 
  node_type: memory
  type: feedback
  bead: rev-15x97
  originSessionId: 6f4e0216-7a79-412a-a259-d6347e84b0d0
---

When verifying whether a PR's **code** sets or contains a symbol (e.g. `code_execution_used = True`), a naive `gh pr diff <PR> | grep <symbol>` produces **false positives**, because the diff includes `.beads/issues.jsonl` and bead-description PROSE inside it mentions code symbols verbatim.

**Concrete failure (PR #7330 verification, 2026-06-07):** Asked to verify a pasted analysis claiming #7330 attaches the code-execution tool but **never sets** `debug_info["code_execution_used"]` (so the persistence gate never fires). A first `gh pr diff 7330 | grep code_execution_used` returned **count=3 apparent assignments**, which looked like it *contradicted* the analysis (suggesting #7330 does set the flag). All 3 matches were inside `.beads/issues.jsonl` bead-description text (beads about dice fabrication), **not production code**. Re-scoping the grep to the actual source hunk showed **0** production assignments — flipping the verdict back to confirming the analysis. The false positive nearly inverted the conclusion.

**Correct procedure — isolate the production-file hunk before grepping:**

```bash
# Pull just one file's hunk out of the combined PR diff, then grep that:
gh pr diff <PR> | awk '/^diff --git.*FILE/{f=1} /^diff --git/&&!/FILE/{f=0} f' | grep <symbol>
# or skip the diff entirely and grep the file in the PR's tree:
gh pr diff <PR> --name-only            # confirm the file is even touched
git show <PR_head>:path/to/file.py | grep -n <symbol>
```

For the gate side, verify against the file directly, not the combined diff: the persistence gate in #7330's tree was at `mvp_site/dice_integrity.py:634` (`if not debug_info.get("code_execution_used"):`), confirmed by reading the file — NOT by grepping the diff.

**Why:** `.beads/issues.jsonl` is a 1MB+ full-DB export committed in this repo; nearly every PR diff includes large beads churn, and bead titles/descriptions routinely quote code symbols, file paths, and flag names. A repo-wide grep over `gh pr diff` therefore conflates "this symbol appears in a bead description" with "this PR's code changes this symbol." This is the same class of error as `gh pr checks | grep -c fail` matching text in check NAMES.

**How to apply:** Whenever a verification hinges on whether a PR's *code* contains/sets/removes a symbol: (1) get the touched files (`gh pr diff <PR> --name-only`); (2) isolate the specific production file's hunk via awk on `diff --git`, or read the symbol from the PR-head blob with `git show <sha>:file`; (3) never trust a raw `gh pr diff | grep <code-symbol>` count as proof of a code change in a beads-tracked repo. Pair with the existing rule "never read `.beads/*.jsonl` whole — use `br`."

**References:**
- PR #7330 https://github.com/jleechanorg/worldarchitect.ai/pull/7330 (CLOSED as subsumed, closedAt 2026-06-07T20:22:50Z) — tool-attach-only, 4 files.
- PR #7280 https://github.com/jleechanorg/worldarchitect.ai/pull/7280 (OPEN, superset; does both halves + NEW `mvp_site/dice_code_execution_audit.py`) — follow-up comment https://github.com/jleechanorg/worldarchitect.ai/pull/7280#issuecomment-4643996220.
- Gate file `mvp_site/dice_integrity.py:634`; producer `mvp_site/llm_providers/gemini_provider.py`.
- Related beads: rev-ncugf (streaming code-exec fail-open root cause).
- Related memory: [[bq-forensic-payload-logging-two-stream-design-pr]] (same streaming RCA cluster).
