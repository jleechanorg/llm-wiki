---
name: green-gate-gate5-resolveReviewThread
description: "Green Gate gate 5 counts GraphQL isResolved review threads, not REST comment replies. CodeRabbit threads auto-resolve when CR confirms; codex-connector threads require explicit resolveReviewThread mutation via gh api graphql."
metadata:
  node_type: memory
  type: feedback
  bead: jleechan-5xho
  originSessionId: 0045c60d-afe5-4e07-84a6-54dde9b7d8b0
---

Green Gate `gate 5` (Comments resolved) is implemented against the **GraphQL `isResolved` flag on review threads**, NOT against REST comment count. Replying to a thread via `gh pr comment` (which creates a REST review comment) does **not** resolve the thread for Green Gate purposes. After every fix push, a Green Gate run will still report `N unresolved` until the threads are explicitly resolved via the GraphQL `resolveReviewThread` mutation.

**Why this matters:** On 2026-06-14, PR #621 fixed all 3 codex-connector P1/P2 findings + 2 CodeRabbit major/minor findings in a single commit (12a4dc99eb). I replied to all 5 threads via `gh pr comment`. The Green Gate still failed with `5. Comments resolved: FAIL | 3 unresolved`. The CodeRabbit threads had auto-resolved (CR's own confirm-fix replies do set `isResolved=true`), but the 3 codex-connector threads stayed unresolved.

**The fix (GraphQL):**

```bash
# 1. List unresolved threads:
gh api graphql -f query='
  query($owner: String!, $name: String!, $number: Int!) {
    repository(owner: $owner, name: $name) {
      pullRequest(number: $number) {
        reviewThreads(first: 100) {
          nodes { id isResolved }
        }
      }
    }
  }
' -f owner='jleechanorg' -F name='jleechanclaw' -F number=621
# Returns: PRRT_kwDORP9hos6JYBj8 (codex-connector), etc.

# 2. Resolve each one:
for tid in PRRT_kwDORP9hos6JYBj8 PRRT_kwDORP9hos6JYBj- ...; do
  gh api graphql -f query='
    mutation($threadId: ID!) {
      resolveReviewThread(input: {threadId: $threadId}) {
        thread { id isResolved }
      }
    }
  ' -f threadId="$tid"
done

# 3. Re-trigger Green Gate:
gh workflow run green-gate.yml --repo jleechanorg/jleechanclaw \
  --ref <branch> -f pr_number=621 -f head_sha=12a4dc99eb3b323a5c5e2de3aa4572c10819f9f7
```

**Why CR threads auto-resolve but codex-connector threads don't:** CodeRabbit's reply confirming the fix ("✅ Addressed") is the bot author clicking the GitHub "Resolve conversation" button on its own thread — the GitHub UI does this automatically when the bot's reply contains the resolved marker. codex-connector does not emit that marker, so its threads stay open.

**Gate 5 filter logic** (from `.github/workflows/green-gate.yml`):
- Counts threads where `isResolved == false`
- Filters out comments authored by the PR author
- Filters out comments starting with `nit:` or `nitpick` (case-insensitive)
- When `LATEST_CR == APPROVED`, gate 5 is non-blocking (CR sign-off pre-empts unresolved noise)

**How to apply:**
- After any PR push that closes a finding: check Green Gate output for "Comments resolved" detail. If `N unresolved` and the threads are all from `chatgpt-codex-connector[bot]` or other non-CR bots, manually call `resolveReviewThread` for each.
- Use `gh api graphql` (not the web UI) for headless resolution.
- One `resolveReviewThread` call per thread; the mutation is idempotent.

**Related:** [[feedback_2026-06-12_coderabbit_dismissed_stuck]] (the upstream CR-stall that this gate-5 resolution completes the picture for).
