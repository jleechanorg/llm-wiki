---
title: "No preview-only config bypasses — match prod config always"
type: source
tags: [feedback, anti-pattern, deploy-config, ci, pr-preview, gcp]
date: 2026-06-28
source_file: ~/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-28_no_preview_only_bypasses.md
---

## Summary
The worldarchitect PR-preview server must mirror GCP dev/stable config. Adding an env var only to `.github/workflows/pr-preview.yml` (not to shared `deploy.sh`) is the wrong shape of fix, even to dodge CI OOMs. The principle was established by PR #7599 ("make preview same as dev and prod"); PR #7926 violated it with `SKIP_PROMPT_EMBEDDINGS_PRECOMPUTE=true` and was rejected. Fix root causes in shared code or bump self-hosted runner resources instead.

## Key Claims
- Preview-only env toggles hide real bugs by creating preview ≠ prod CI signal.
- The rule predates PR #7926: PR #7599 already set "preview == dev == prod config, only min-instances differs for cost."
- When preview OOMs, fix the root cause in shared code (`scripts/precompute_prompt_embeddings.py`) or bump self-hosted runner memory in `install.sh` / launchd plist — never add a preview-only env bypass.
- If the feature is genuinely too expensive for preview windows, the feature is too expensive for prod.

## Key Quotes
> "to stop trying to do this i want preview servers to be as close to gcp dev/stable in config as possible." — user, 2026-06-28

> "Does this env var appear in `deploy.sh` for stable/dev, or is it ONLY in `pr-preview.yml`?" — acceptance criterion from the lesson

## Connections
- [[PR-7599-prod-config-unified]] — rule source ("preview == dev == prod config")
- [[PR-7926-skip-precompute-preview]] — violating PR (CLOSED-not-merged)
- [[WorldArchitect-Deploy-Config-Matrix]] — `deploy.sh` + `shared_config.sh` shared config mechanism
- [[Optimization-Baseline-Fidelity]] — sister principle: A/B control must be deployed config, not "preview off" shortcut
- [[Self-Hosted-Runner-Resource-Budget]] — the runner-side lever when feature is too expensive for shared config
- [[Bead-rev-q9lvd]] — formal bead tracking the rule
