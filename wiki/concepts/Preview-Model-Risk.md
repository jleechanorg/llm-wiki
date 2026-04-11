---
title: "Preview Model Risk Requires Explicit Acknowledgment"
type: concept
tags: [jeffrey, oracle, PR-review, model-safety, risk]
sources: [jeffrey-oracle]
last_updated: 2026-04-10
---

Adding preview, nightly, or non-production-grade models to critical configuration sets (e.g., `MODELS_WITH_CODE_EXECUTION`, execution allowlists) triggers a conditional verdict even when all other oracle checks pass: CI green, surgical change (+2/-1), body matches diff. The risk is fail-open: a preview model with unexpected edge cases could silently route execution to the wrong path, bypassing security controls that rely on model classification. Jeffrey accepts "properly flagged medium risk" in the PR body as sufficient acknowledgment but will not give an unconditional "ok" on preview model additions.

The concern is specifically about adding preview models to security-critical paths, not about all preview model changes. Removing a preview model from a critical set is fine. Adding `PRODUCTION_MODE=true` to a preview environment is a tightening (safe, not a bypass). The conditional status is specifically about additions to security boundaries or execution allowlists.

This pattern was first formally observed in batch 4 with PR #6178 (adding gemini-3.1-flash-lite to `MODELS_WITH_CODE_EXECUTION`), which received a conditional "ok — properly flagged medium risk on preview model, all checks green, surgical fix. continue" verdict. The pattern confirms that all oracle checks passing is necessary but not sufficient when preview models touch security-critical configurations. [[jeffrey-oracle]]
