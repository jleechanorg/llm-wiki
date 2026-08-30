---
name: Cloud Run and Mem0 drift require executable and live-state guardrails
description: Repository policy needs live remediation, while Mem0 health must execute a real search and expose SDK errors.
type: feedback
bead: none (Beads workspace lock held by another process)
---

# Cloud Run and Mem0 drift require executable and live-state guardrails

## Context

On 2026-08-30, WorldArchitect Cloud Run spend reached $128.93/day because a
shared capacity change left preview services warm at one 8-CPU/16-GiB instance
each. PR #9586 restored the intended exact-name policy: only
`mvp-site-app-dev` and `mvp-site-app-stable` default to one minimum instance;
staging, preview, ad-hoc, and unknown services default to zero. After merge,
live inspection still found `mvp-site-app-s1`, `s3`, `s4`, and `s5` at one,
because repository defaults do not mutate existing Cloud Run revisions. Those
four were updated and a fresh enumeration verified all 22 preview services at
zero while dev and stable remained at one.

The same session diagnosed Mem0. Qdrant, Ollama, Groq, the helper, and the
Python package were all healthy, but `mem0_recall.py` silently swallowed:

`ValueError: Top-level entity parameters ... user_id ... are not supported in search(). Use filters={'user_id': '...'} instead.`

Mem0 2.0.14 accepts `search(query, filters={"user_id": ...}, top_k=...)`; the
stale hook still called `search(query, user_id=..., limit=...)`. This exact API
drift was documented in July, but documentation did not protect the duplicate
client and blanket `except: pass` made the regression invisible.

A real `/learn` save then exposed a second failure: the configured Groq key was
present but invalid (`401 invalid_api_key`). Presence-only enablement therefore
reported Mem0 as available while inferred writes were discarded. PR #841 makes
authentication failure preserve a bounded direct memory with `infer=False`
through the healthy local embedder and Qdrant path, while reporting the error.

## Mandatory rules

1. Cloud Run capacity changes require two independent proofs: an exact-name
   repository enforcement test and a post-change live service enumeration.
   A merged default does not prove existing revisions were remediated.
2. Only `mvp-site-app-dev` and `mvp-site-app-stable` may default to
   `min-instances=1`. Every preview, staging, experiment, ad-hoc, and unknown
   service must fail safe to zero.
3. Mem0 availability cannot be inferred from imports, Qdrant readiness, or
   `Memory.from_config()` alone. Run one real, read-only semantic search using
   the installed SDK's current signature.
4. Every Mem0 client boundary must have a compatibility test that asserts the
   SDK call shape. Do not duplicate untested `search` or `get_all` calls.
5. Fail-open hooks may not fail silently. Preserve prompt execution, but emit
   the exception type and message to stderr or a bounded diagnostic log.
6. `/ms` intentionally searches file-backed memory systems and skips Mem0; it
   is a recovery path, not proof that Mem0 recall works.
7. Credential presence is not credential health. An extraction-auth failure
   must either use a verified extractor or preserve a bounded direct memory;
   never silently drop the write.

## Fix and verification

- Cloud Run: PR #9586 merged as `67869b9d4882773cd21fb4970d0018de92cc485d`.
- Live remediation: `mvp-site-app-s1`, `s3`, `s4`, and `s5` were redeployed
  with minimum instances zero; all 22 preview services then enumerated at zero.
- Mem0 fix worktree: `/Users/jleechan/projects/worktree_mem0_hardening`.
- Mem0 fix: PR #841, commit `e614e005d2ad9fe640f31a21881739a452799aab`.
- Mem0 TDD: two tests pass; a real authentication-fallback add returned `ADD`,
  and a real search returned the saved canary first at score `0.929`.
- `/integrate`: WorldArchitect synchronized to merge `67869b9d` and created
  fresh branch `dev1788118943`.

## References

- https://github.com/jleechanorg/worldarchitect.ai/pull/9586
- https://github.com/jleechanorg/worldarchitect.ai/commit/67869b9d4882773cd21fb4970d0018de92cc485d
- https://github.com/jleechanorg/jleechanclaw/pull/841
- https://github.com/jleechanorg/jleechanclaw/commit/e614e005d2ad9fe640f31a21881739a452799aab
- `/Users/jleechan/projects/worktree_mem0_hardening/.claude/hooks/mem0_recall.py`
- `/Users/jleechan/projects/worktree_mem0_hardening/tests/test_mem0_recall_hook.py`
- `/Users/jleechan/.claude/projects/-Users-jleechan-projects-other-disk-magician/memory/feedback_2026-07-27_mem0_qdrant_diagnosis_recipe.md`
