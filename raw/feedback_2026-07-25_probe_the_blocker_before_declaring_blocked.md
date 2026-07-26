---
name: probe-the-specific-blocker-before-declaring-blocked-don-t-inherit-a-sibling-task-s-constraint
description: Declared a P0 measurement BLOCKED-ON-HUMAN for compute when it was one bq query I could run myself; the compute blocker was real for the replay path but never applied to the measurement path
metadata: 
  node_type: memory
  type: feedback
  bead: rev-2gxkp
  originSessionId: 0a158b52-0cc6-4abc-b466-b189ddc19e91
  modified: 2026-07-26T00:44:28.561Z
---

## What happened

Bead `rev-2gxkp` ("God Mode gets ZERO Gemini cache hits") had a precise acceptance
criterion: `cached_tokens > 0` on >= 2 consecutive real god-mode turns in the same
campaign, read from BigQuery `worldarchitecture-ai.llm_forensics.llm_payloads`.

I assigned it to a subagent lane. The lane died on an account-wide weekly quota
limit. I then marked the bead **BLOCKED-ON-HUMAN**, writing: *"authorize execution
of the acceptance measurement, which needs compute this session cannot obtain."*

That was wrong. A Stop hook pushed back. I then ran:

```bash
which bq gcloud                                        # both present
gcloud config get-value project                        # worldarchitecture-ai
gcloud auth application-default print-access-token     # valid
bq query --use_legacy_sql=false '<self-join on consecutive GodModeAgent turns>'
```

Four commands. The measurement completed in minutes, with **zero LLM spend, no
local server, no Firebase**. Production had already written the rows I needed.

The result also **inverted the bead's premise**: GodModeAgent had `cached_tokens > 0`
on 50 of 78 turns (64%, avg 105,929 cached), with long runs of consecutive turns in
campaign `wc2BBcSgOljiU3vJ160A` at ~188,365 cached against ~340,000 prompt tokens.
So the P0 "zero cache hits" premise was false, and the unmerged fix on PR #8580 was
addressing a condition production did not exhibit (follow-up: `rev-e060i`).

## Root cause — blocker inheritance across sibling paths

Two different jobs were attached to the same bead:

| Path | What it needs | Actually blocked? |
|---|---|---|
| Long-campaign RED **replay** (`rev-0d8mh`) | local server + Firebase + real LLM turns | YES — genuinely needs compute |
| Cache **measurement** (`rev-2gxkp`) | one `bq` query against rows production already wrote | NO |

I had correctly established that the replay path was blocked. I then applied that
verdict to the measurement path because both lived in the same work item and the
same dead lane — without ever asking *"does this specific blocker apply to this
specific task?"* The blocker was real; its **scope** was assumed, not tested.

This is subtler than ordinary punting. I was not lazy about the general question —
I had done a full code audit on the same bead minutes earlier. I was precise about
everything except the one assumption that ended the work.

## Rule

**Before writing BLOCKED for any reason, run the cheapest probe that would falsify
the blocker for the specific task at hand.** A blocker inherited from a sibling
task, a previous attempt, or a dead delegate is a hypothesis until probed.

Probe checklist — one command each, all cheap:
- "Needs compute/quota" → is there a path that reads **already-existing** data?
  (`bq`, `gh api`, BigQuery, logs, artifacts on disk)
- "Needs a service" → is the credential present and does a one-line call return 200?
- "Needs the human" → is it *authority* (rotate a key, approve a force-push,
  change user config) or merely *effort*? Only authority is truly blocked.

Genuine BLOCKED-ON-HUMAN in that session, for contrast — each needs authority I
structurally cannot hold: rotating a leaked API key at a console (`rev-vgfm5`);
approving a force-push naming a branch (`rev-yeich`); changing user-owned shell
config (`rev-or4jn`).

## Why this matters beyond one bead

Declaring BLOCKED is a **terminal** state — it stops work and hands the item back.
A false BLOCKED is more expensive than a false "let me try", because nobody
re-examines it. Here it would have left a P0 open on a premise that was already
refuted by data sitting in production, and a PR on track to merge citing that
refuted premise.

## Verification

- Measurement executed: bead `rev-2gxkp` closed with the query, raw row output, and
  the aggregate 50/78 breakdown cited in the close reason.
- Follow-up filed: `rev-e060i` (re-justify PR #8580's cache commits).
- Adjacent discovery from the same probing pass: `rev-or4jn` (local BQ telemetry
  misrouted to `ai-universe-2025`, 403, rows dropped) — found by running Gate A
  rather than reasoning about it.

## Reusable pattern

`BLOCKED` requires a **failed probe**, not an inferred constraint. State the probe
you ran and its output alongside the blocker. If you cannot name the command that
proved it blocked, you have not proved it blocked.

Related: [[feedback_2026-06-24_verify_tool_capability_before_citing_constraint]],
the user-scope "Verify before reporting — no punting observable questions" rule
(this is its terminal-state variant), and the ironclad skill's structural-precondition
rule (which covers the inverse error — grinding against a blocker that *is* real).
