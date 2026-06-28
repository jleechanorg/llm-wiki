---
name: No preview-only config bypasses — match prod config always
description: Preview servers must mirror GCP dev/stable config; do not add preview-only env bypasses (e.g. SKIP_*_PRECOMPUTE) that diverge from prod, even to dodge CI OOMs.
metadata:
  type: feedback
  originSessionId: 526f1dac-9a42-4da8-94cb-1cdf5cc62822
---

PR [#7926](https://github.com/jleechanorg/worldarchitect.ai/pull/7926) (`fix(ci): skip precompute in PR preview to prevent OOM on prompt-changing PRs`, branch `fix/skip-precompute-pr-preview`, HEAD `65988605b`, CLOSED-not-merged) proposed setting `SKIP_PROMPT_EMBEDDINGS_PRECOMPUTE: 'true'` only on the PR-preview deploy step so the self-hosted runner wouldn't OOM-kill when a PR changed prompt files. **This approach is wrong.** Even though the symptom (4 OOM-kill deploy-preview runs on PR #7860) was real, the fix is in the wrong direction: any preview-only divergence from dev/prod config is a class of fix that hides real issues and should be rejected up front.

**Why this rule holds:**

The principle "preview == dev == prod config (only min-instances differs for cost)" is already established by [PR #7599](https://github.com/jleechanorg/worldarchitect.ai/pull/7599) (memory `project_2026-06-15_prodcfg_pr7599_dev_stable_unified.md`). User explicitly said at the time: **"make preview same as dev and prod."** Adding `SKIP_PROMPT_EMBEDDINGS_PRECOMPUTE` for preview reintroduces the divergence PR #7599 fixed. We must NOT undo that with feature-flag-shaped "skip X in preview only" patches.

**What preview-only bypasses hide:**

1. **OOM symptoms become prod symptoms.** If precompute OOMs in preview (8Gi preview), it will OOM in prod dev (8Gi) under real load. Fix the actual cause (OOM in the precompute step itself — memory limit, batch size, or feature flag interaction) so prod dev/stable also stops OOMing, instead of dodging the symptom only in preview.
2. **False-green CI signal.** A preview deploy that "passes" because precompute is skipped is not the same signal as a prod deploy that runs precompute. The deploy-preview job is supposed to be a faithful rehearsal of prod deploy.
3. **Stale embeddings in preview.** PR #7926's own PR body admits "preview pods use embeddings from the most recent main-branch deploy" — this is by design, but it means the preview never exercises the embedding path that prod will. A future regression that breaks embedding freshness will pass preview CI and break prod.
4. **Config sprawl.** Every `SKIP_X` / `BYPASS_Y` / `DISABLE_Z` adds another env var to the deploy matrix, another writer/reader alignment point, and another deploy.sh cell to drift.

**What to do instead when preview OOMs:**

- Reproduce the OOM in dev (which runs the same config) — `dev` also got the bug if `preview` did.
- Fix the root cause in the precompute step (`scripts/precompute_prompt_embeddings.py`): batch size, parallelism, memory map, lazy load.
- If the root cause is genuinely a runner-resource limit on self-hosted only (not a code bug), increase the self-hosted runner's memory alloc (in `install.sh` / launchd plist), not the deploy config.
- If the feature itself is too expensive for preview windows, **the feature is too expensive for prod**. Cut the scope, not the test fidelity.

**Acceptance criterion for a "preview-only env" PR:**

> "Does this env var appear in `deploy.sh` for stable/dev, or is it ONLY in `pr-preview.yml`?"

If ONLY in `pr-preview.yml`, the PR is the wrong shape. Reject and redirect to either (a) fix the underlying OOM/cost root cause in shared code, or (b) bump the self-hosted runner's resources so the standard config fits.

**Why:** This is a Critical anti-pattern, not a Best Practice. The "preview-only bypass" shape keeps recurring (precompute skip, mock-LLM toggle, threads=1 cap, `minScale=0` override) — each one individually looks cheap, but collectively they make preview CI a different system than prod, which is exactly the failure mode the [#7599](https://github.com/jleechanorg/worldarchitect.ai/pull/7599) reversal fixed.

**How to apply:**

- When reviewing or proposing a PR that touches `pr-preview.yml` env vars but not `deploy.sh` shared config → flag it and redirect.
- When CI green only because of a preview-only toggle → fail the PR; require shared-config parity.
- When designing a new feature that "would be expensive to test in preview" → redesign the test (smaller fixture, faster model, scoped integration), don't bypass the prod path.

**Bead:** [`rev-q9lvd`](.beads/issues.jsonl) — "Preview servers must mirror GCP dev/stable config — no preview-only env bypasses" (type=task, priority=2, labels=[learning])

**References:**

- [PR #7926](https://github.com/jleechanorg/worldarchitect.ai/pull/7926) — the violating PR (CLOSED, not merged)
- [PR #7599](https://github.com/jleechanorg/worldarchitect.ai/pull/7599) — established the "preview == prod" principle
- Memory: `project_2026-06-15_prodcfg_pr7599_dev_stable_unified.md` (the rule source)
- Memory: `feedback_2026-06-07_optimization_baseline_fidelity.md` (related: A/B control must be deployed config, not a "preview off" shortcut)
- Workflow: `.github/workflows/pr-preview.yml`
- Scripts: `scripts/precompute_prompt_embeddings.py`, `deploy.sh`
- User message 2026-06-28T03:25Z: "to stop trying to do this i want preview servers to be as close to gcp dev/stable in config as possible"

**Reusable pattern:** When tempted to add an env var that differs across deploy targets (`pr-preview.yml` vs `deploy.sh`), first ask "is this fixing a bug or hiding one?" If hiding, the fix belongs upstream (in shared config or in the runner's resource budget), not in the deploy-config matrix.
