---
name: feedback-2026-06-14-er-verdict-sub100loc-unit-acceptance
description: "/evidence_review accepts unit-test-only proof for production changes under 100 delta lines of non-test code; first-pass PARTIAL verdicts come from PR body overclaims, not from evidence gap. Correct the body, re-run, expect PASS."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8e1493a5-115a-4b66-9790-42973f21fc27
---

The /evidence_review (Codex via ai_orch) verdict has two failure modes that look the same but are fixable differently:

1. **Genuine evidence gap** — claim class higher than evidence can support. Fix: add Layer 2/3 evidence (real callstack, real services, captioned video for UI).
2. **PR body inaccuracy** — evidence bundle is fine, but the PR body overclaims what the evidence shows. Fix: rewrite the PR body to match the actual evidence; re-run /er.

**Pattern observed on PR #686** (2026-06-14):
- First /er verdict: PARTIAL. Reason: PR body claimed `test-colima-roundtrip.mjs` ran 3 sessions (it actually ran 1).
- The actual evidence WAS sufficient — 25/25 unit tests + multi-worker-colima-test.mjs (3 sessions) + runtime round-trip. The "gap" was a 1-sentence overclaim in the body.
- Fix: rewrote the "Testing" section to describe `test-colima-roundtrip.mjs` as the single-session env-serialization check and made `multi-worker-colima-test.mjs` the primary 3-worker evidence.
- Second /er verdict: PASS. Same evidence, accurate description.

**Claim class floor for sub-100-LOC production changes**:
- The /es evidence-standards exception "unit-only proof IS acceptable for non-production changes (docs, tests, tooling/scripts) or for production changes under 100 delta lines of non-test code" applies.
- For env-var pinning in a plugin (8 lines impl), `unit` claim class is the floor; you do NOT need a real-VM bootstrap test in CI infra.
- For multi-worker behavior, the right evidence is **direct plugin invocation** (real plugin code, real env, real config) — not a unit test, not live `ao spawn` (which may be blocked by other config bugs).
- For runtime serialization, the right evidence is `Object.entries(env).filter(...)` simulation — also direct invocation.

**How to apply**:
- Before declaring "evidence gap" and rebuilding tests, re-read the PR body for overclaims. A PARTIAL verdict is faster to resolve by rewriting the body than by adding new tests.
- For sub-100-LOC production changes, state "Claim floor override: N/A (X delta lines of non-test code; matches existing test pattern; no end-to-end real-VM bootstrap test in CI infra)" in the Evidence section. /er recognizes this and passes.
- Distinguish "evidence insufficient" from "evidence accurate but body misleading" before responding to a PARTIAL.

**Why**: PR #686 first /er pass returned PARTIAL, causing a 20-minute cycle of re-evaluating whether unit tests were enough. The actual issue was a 1-sentence overclaim, not a gap. Rewriting the body fixed it on the second pass with no new tests. Future sessions should distinguish these two failure modes before reacting to a PARTIAL.
