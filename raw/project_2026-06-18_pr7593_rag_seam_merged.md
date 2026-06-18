---
name: pr7593-rag-seam-merged
description: PR
metadata:
  node_type: memory
  type: project
  bead: none
  originSessionId: baee859c-0328-48bc-b07d-40fdcc827a7e
---

## PR #7593 RAG Prompt Seam — MERGED 2026-06-18T18:17:17Z

**Merge commit**: `bfb88e1fa1c05d136aefb0f0fdd23bf7f75d7837`
**PR HEAD**: `889c908a6f190b6da2211995779cc94c1708604c`
**Branch**: `feat/rag-seam-combined` → `main`

### What landed

Three RAG modes selectable per user via Firestore `settings.rag_mode`:
- `original` — full 333,169-char system instruction (default, byte-identical to main)
- `rag` — chunked ~137K-char instruction (0.411×); skips Gemini explicit cache; `\n\n[...]\n\n` separator present at char 20568
- `shadow` — serves full prompt but fires parallel RAG build on daemon thread; logs `rag_shadow_comparison` to BQ `log_events`

**Token savings at level-up turn (BQ confirmed)**: RAG 59,545 prompt tokens vs original 106,130 = 0.561× (43.9% fewer tokens).

**New modules**: `prompt_rag.py` (BM25+embedding rerank, 323L), `rag_mode.py` (mode resolver, 84L).

**Evidence gist**: `624a5077c8bb848a45268c2daac2290d` — 9 files including BQ `llm_payloads` readback (98 rows), RAG-mode Gemini HTTP sample (137,010-char system instruction, separator present), shadow Firestore record.

### Gate path to merge (key gotchas)

1. **Gate 6b MEDIA_URL_RE bug** — `pr_description_gate.py` line 106 has `MEDIA_URL_RE` with `$` anchor but no `re.MULTILINE`. GitHub Releases `.gif`/`.mp4` URLs in the MIDDLE of section content don't match (only URLs at end of string match). **Workaround**: add a gist URL (matches `GIST_URL_RE` which has no `$` anchor) to `## Non-Unit Test Evidence`. **Permanent fix needed**: add `re.MULTILINE` flag to `MEDIA_URL_RE` in a separate PR.

2. **Skeptic-smoke timing race** — Skeptic Self-Verify ran while MCP Smoke was still in progress → VERDICT had `Gate 8: WAIT`. Green Gate then saw VERDICT: WAIT and failed. Fix: after smoke completes, dispatch a SECOND Skeptic run. The new VERDICT with Gate 8: PASS lets the next Green Gate pass.

3. **Directory tests (claude) persistent rate-limit** — self-hosted runner at IP `47.151.147.179` keeps hitting GitHub's unauthenticated API rate limit during `actions/checkout`. Multiple re-runs failed. NOT a code failure — Gate-1 (CI=success) in Green Gate ignores this check. All other Directory tests pass.

### Next steps (from class-lookup + RAG roadmap)

- **Phase 3 class-lookup seam injection** — bead in `project_2026-06-17_rag_class_lookup_phase12_pr7651.md`; deferred pending #7593 merge (now unblocked). PR #7651 wires `class_lookup.py` into the RAG seam.
- **`MEDIA_URL_RE` fix PR** — add `re.MULTILINE` to `pr_description_gate.py` line 106-109.
- **`rev-yr1ic` nits** — shadow `served_instruction_chars=None` asymmetry, `_fire_shadow_rag_call` record-extraction, defensive getattr drops, `build_rag_prompt` split, SCHEMA_POSTAMBLE drift check.
- **Class-agnostic PRs #7640/#7641/#7642** — still OPEN/UNSTABLE; unblocked now that #7593 merged.
</content>
</invoke>
