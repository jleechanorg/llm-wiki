---
name: coderabbit-dismissed-stuck-admin-override
description: "CodeRabbit can get permanently stuck at DISMISSED (never APPROVED) after a changes-requested→fix cycle, structurally blocking Green Gate gate-3 + skeptic-cron auto-merge; admin override is the resolution"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c594d4f0-a942-4271-85f6-5407a3c1d6e6
---

After a CodeRabbit CHANGES_REQUESTED → fix → push cycle, CR's formal review object can get **stuck at `DISMISSED`** and never flip to `APPROVED`, even with `.coderabbit.yaml` `approve: true`. The formal review-object `state` stays `DISMISSED` against a **stale SHA** while CR confirms the fix only in **chat prose** ("Still all good! Safe to merge").

This is fatal to the merge pipeline: Green Gate **gate-3 (CR approved)** reads the formal review `state` == `APPROVED` on the current head. `DISMISSED`/chat-prose → gate-3 FAIL → Green Gate check-run `failure` → skeptic-cron (which mirrors Green Gate) posts `VERDICT: FAIL` and **never auto-merges**. There is no in-band fix.

**Why `@coderabbitai review` does NOT help:** CR replies *"CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused."* It refuses to emit a fresh review object on commits it already saw. So you cannot force a new APPROVED on the current head.

**Distinguish the two CR nudges:**
- `@coderabbitai all good?` → **chat prose only** (no review object) — useless for gate-3.
- `@coderabbitai review` → acknowledged but **no-op** on already-reviewed commits — also useless once stuck.
- The only thing that yields a fresh review object is a **brand-new commit** triggering auto-review (and even then, post-changes-requested it has been emitting DISMISSED, not APPROVED).

**Resolution = admin override merge**, but ONLY when ALL hold (matches the repo's "NEVER run gh pr merge yourself" exception):
1. **Explicit user authorization** to merge (e.g. "the pr and merge").
2. **Substantively 7-green** — verify each gate independently: all CI check-runs `success` (Green-Gate meta-check excepted), `mergeable=MERGEABLE`, Bugbot clean, every open inline thread is CR's own self-marked "✅ Addressed", evidence N/A-or-present. Only gate-3 + gate-7-skeptic may be red, and both solely because of the CR stall.
3. **skeptic-cron structurally stalled** — confirmed it mirrors gate-3 and CR will not produce APPROVED (CR's own "does not re-review" message is the proof).

`mergeStateStatus=UNSTABLE` + `mergeable=MERGEABLE` means GitHub itself allows the merge (UNSTABLE = a *non-required* check failing, i.e. the advisory Green Gate). Command: `gh pr merge <N> --repo <owner>/<repo> --squash --admin --delete-branch`. Report old→new main SHA + merge-commit URL.

**Provenance:** PR [#611](https://github.com/jleechanorg/jleechanclaw/pull/611) (deploy.sh PROD_PORT 8643→8642 fix), admin-merged 2026-06-12 20:12Z, merge commit `d951fd23a2`, old main `2fe2e5fa32`. CR stuck at `DISMISSED@b0882cb134` across 13+ min of monitoring and an explicit `@coderabbitai review`. Related: [[skeptic-cli-verdict-author-mismatch]].

**Second variant — CR out of credits / rate-limited (distinct from DISMISSED):** gate-3 also stays `state=none` (CR *never starts* the review) when the org hits CodeRabbit's **fair-usage rate limit** or **runs out of usage credits** — CR posts a `> [!WARNING] Review limit reached … organization has run out of usage credits` comment instead of a review object. Green Gate gate-3 reads `state=none` → FAIL → skeptic-cron never merges, same structural stall. Same admin-override resolution applies (explicit user auth + substantively green + skeptic stalled). **Provenance:** PR [#612](https://github.com/jleechanorg/jleechanclaw/pull/612) (SOUL Agnt-F channel→dir→org mapping, +6 lines, lite-green docs/policy), admin-merged 2026-06-12, squash commit `8aaad833df`, old main `313a1b0de0`. After a squash-merge, the live `~/.hermes` local `main` that carried the cherry-pick **diverges** from origin (content-identical, different SHA) — `git reset --hard origin/main` to restore ff-only-pull for `deploy.sh` (verify full tree diff is only auto-regen timestamp noise first).
