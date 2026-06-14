---
title: "Feedback 2026 06 10 Green Gate Gate6 Gate7 Evidence Skeptic Sequence"
type: source
tags: [memory, ao-worker, codex-worker, 2026-06]
date: 2026-06-10
source_file: .claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-10_green_gate_gate6_gate7_evidence_skeptic_sequence.md
---

## Summary

When a worldarchitect.ai PR's Green Gate (`green-gate.yml`) check-run shows FAILURE but every other check (CI, Directory tests, Design Doc Grep Gates, Bugbot, CodeRabbit ping) is SUCCESS, the failure is almost always Gate 6 or Gate 7, not real CI. Read the failed run log: `gh run view <id> --repo jleechanorg/worldarchitect.ai --log-failed` and grep `GATE-[0-9]` for the verdict lines. **Gate 6 (Evidence)** — fires when changed files match `^(testing_(mcp|ui)/|mvp_site/|deploy\.sh$|\.github/workfl...

## Original

When a worldarchitect.ai PR's Green Gate (`green-gate.yml`) check-run shows FAILURE but every other check (CI, Directory tests, Design Doc Grep Gates, Bugbot, CodeRabbit ping) is SUCCESS, the failure is almost always Gate 6 or Gate 7, not real CI. Read the failed run log: `gh run view <id> --repo jleechanorg/worldarchitect.ai --log-failed` and grep `GATE-[0-9]` for the verdict lines.

**Gate 6 (Evidence)** — fires when changed files match `^(testing_(mcp|ui)/|mvp_site/|deploy\.sh$|\.github/workflows/evidence-gate\.yml$)`. It greps PR body + issue comments for this regex: `https?://[^ ]*\.(mp4|gif|cast)|gist\.github\.com/|asciinema\.org/a/|loom\.com/share/|user-attachments\.githubusercontent\.com/`. A thorough prose PR body is NOT enough — you need a literal `gist.github.com/...` (or video/asciinema/loom/user-attachments) URL. Fix: `gh gist create --public <evidence.txt>` then add the URL to the PR body Testing section via `gh pr edit <N> --body-file`.

**Gate 7 (Skeptic)** — required when changed files are production-impacting (`mvp_site/**` qualifies). Green Gate posts a trigger comment then POLLS for a `VERDICT:` comment tagged `skeptic-head-sha-<headsha>`. If no verdict exists for the current head SHA it fails closed. Fix: dispatch the fallback `gh workflow run skeptic-self-verify.yml --repo jleechanorg/worldarchitect.ai --ref <branch> -f pr_number=<N>` — it evaluates gates 1-8 and posts `VERDICT: PASS/FAIL` as the skeptic bot. The Green Gate poll then finds it and passes (timing can line up within seconds).

**Why:** PR #7447 (deletion-only, fix/delete-dead-level-up-functions, head 1694125029) — Green Gate failed GATE-6 with all other checks green. Created gist https://gist.github.com/jleechan2015/92ef9569df4101b50ad45617516a674d (96-passed pytest + zero-caller audit), added URL to body, dispatched skeptic-self-verify which posted VERDICT: PASS, then Green Gate rerun reported GREEN GATE: PASS (all 8 gates) and mergeStateStatus flipped to CLEAN.

**How to apply:** For any mvp_site PR driven to 7-green, pre-empt both gates: put a gist evidence URL in the body BEFORE the first Green Gate run, and run skeptic-self-verify on the head SHA. Note: stale pre-fix Green Gate runs stay attached to the SHA, so the canonical failing-check count can report >0 even after the fix — trust `mergeStateStatus == CLEAN` + the latest Green Gate run's conclusion, not the raw rollup count. See [[feedback_2026-06-10_green_gate_first_run_after_push_false_negative]] and [[feedback_2026-06-10_green_gate_gate3_filters_by_head_sha]].
