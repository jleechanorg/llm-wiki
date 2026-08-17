---
name: llm-bug-root-cause-needs-direct-ablation-not-research-fanout
description: "For LLM-behavior bugs, run a real minimal ablation against the actual API FIRST — /research, /advice, /web-advice, and rollback-style fixes are not substitutes for a controlled experiment you can run yourself in minutes"
metadata: 
  node_type: memory
  type: feedback
  bead: "rev-xph5o, rev-37zkv, rev-0y9cv"
  originSessionId: eac8d54a-bfae-4316-9c1b-d1ae0b314e68
  modified: 2026-08-16T21:25:38.195Z
---

## What happened

Investigating why `gemini-3.7-flash` (WorldArchitect.AI's new default model) entered
a runaway `code_execution` tool-call loop — `FinishReason.TOO_MANY_TOOL_CALLS` after
~240-270 internal iterations, 55s+ latency, tens of millions of cached tokens per
turn — I spent a full round of external investigation before finding the actual
cause:

1. `/research` — a background agent did excellent primary-source work (SDK git
   archaeology, Google forum bug reports, `TOO_MANY_TOOL_CALLS` enum history) and
   it was genuinely valuable context. But it could not and did not find the trigger,
   because the trigger isn't documented anywhere.
2. `/advice` (Opus subagent + `/secondo` 4-model panel) — converged on "exclude
   `gemini-3.7-flash` from code_execution" as the safe recommendation, and one
   model fabricated a specific but false ceiling number ("256 internal calls")
   that two other models later had to refute.
3. `/web-advice` (real browser sessions, Grok + Perplexity) — independently
   refuted the fabricated number and confirmed no caller-side knob exists, but
   also converged on "exclude the model" as the practical answer.
4. I then started **writing a client-side circuit-breaker patch directly into
   `mvp_site/llm_providers/gemini_provider.py`** — a defensive workaround for the
   symptom (cut the stream early after N tool calls) rather than a fix for the
   cause.

The user stopped me mid-edit: *"another agent is coding and stop these fucking
workarounds figure out root cause and use ablation. can gemini execute 2+2? with
3.7 flash. if so then gradually make it more complicated until it approaches our
actual code and see where it goes wrong dont code mvp site code yet."*

I reverted the patch, wrote a ~30-line standalone script against the real Gemini
API (not mvp_site code), and within a handful of runs found it: the loop is
triggered specifically by `code_execution` + a **bare**
`response_mime_type="application/json"` (no schema) — reproduced 5/5 on a trivial
"what is 2+2" prompt. `gemini-3-flash-preview` doesn't loop because it happens to
tolerate that combination; `gemini-3.6-flash` and `gemini-3.7-flash` both do not.
Adding an explicit `response_json_schema` (a raw dict — not `response_schema`,
which is separately blocked by SDK client-side validation) fixed it 10/10 times,
including with `additionalProperties: true` on dynamic sections (matching the
app's real NPC/inventory-keyed game state). Total time from "start ablation" to
"root cause + validated fix" was well under an hour; the prior research round had
taken longer and not found it.

## Why the research round couldn't find this

Not a research-quality failure — it's a structural mismatch between the method
and the problem. `/research`, `/advice`, and `/web-advice` all query *externally
documented or externally reasoned* knowledge. This bug's trigger is an
**undocumented interaction between two SDK config fields on two specific model
versions** — nothing indexed anywhere states it, so no amount of better prompting
those tools would have surfaced it. It was only discoverable by actually varying
the two config fields against the real API and watching what happened. External
research is upper-bounded by what's been written down; a live systems bug in an
opaque server-side component isn't written down until someone runs the
experiment — in this case, us.

## The generalizable rule

For a **live LLM-behavior bug** (wrong finish reason, runaway tool loop, garbled
structured output, model-version-specific regression), when direct API access is
available and a minimal repro is cheap (seconds, pennies), **build the ablation
harness first** — this is systematic-debugging Phase 1 ("build a feedback loop")
applied literally:

1. Reproduce the *simplest possible* version of the failure directly against the
   real API/SDK, outside the application (a standalone script, not the app's own
   code path). Confirm it fails.
2. Reproduce the *working* comparison case (the model/config that doesn't exhibit
   the bug) on the identical minimal prompt. Confirm it succeeds. This proves the
   difference is mechanistic, not incidental to your specific production prompt.
3. Add exactly one variable at a time (JSON mode, a system instruction, a specific
   config flag) and re-run, watching for the exact point where it flips from
   working to broken.
4. Only once the trigger is isolated, evaluate fixes *for that trigger specifically*
   — not defensive patches for the symptom (circuit breakers, timeouts, retries)
   and not rollback/exclusion of the whole feature.

**Sequencing matters**: research/second-opinion fan-outs are legitimate and were
not wasted (the SDK version/enum history and forum corroboration are genuinely
useful context, now folded into the bead) — but they belong *after* or *parallel
to* the ablation, never as a substitute for it when direct reproduction is this
cheap. And root-cause-first (`~/.claude/skills/root-cause-first/SKILL.md`) should
have stopped me from reaching for a circuit-breaker patch before the trigger was
even isolated — a defensive fix for an unknown cause is exactly the pattern that
skill exists to block.

## Verification

- Ablation scripts: `/tmp/gemini_ablation/step1_trivial.py` through
  `step7_variations.py` (ephemeral, not committed) — 2+2 → JSON mode → system
  instruction → `thinking_level` → `response_json_schema` → dynamic
  `additionalProperties` schema, each run against the real Gemini API with the
  key from GCP Secret Manager (`gemini-api-key`).
- Full narrative and fix path: bead `rev-xph5o` (root cause), `rev-37zkv`
  (implementation), `rev-0y9cv` (PR #8951 does not actually fix it — same
  evidence-thinness pattern as prior incidents, see
  [[fabricated-evidence-reports-recurring-pattern]]).
- Research doc (still valid context, just not the thing that found the fix):
  `docs/research/gemini-3.7-flash-code-execution-tool-call-loop.md`.

## Reusable pattern

When a bug report is "model X behaves correctly, model Y (or model X's newer
version) doesn't," and you have direct API/SDK access: reach for a minimal
ablation script before reaching for research tools or defensive code. If the
repro is expensive (can't cheaply call the real API/service), *then* research and
multi-model synthesis become the right first move — the decision hinges on
reproduction cost, not on how hard the bug looks.
