---
title: "/babysit started 2h after the user merged the PR (2026-06-13)"
type: source
tags: [feedback, babysit, claw, hermes, slack-dispatch, slash-command-ambiguity, worldarchitect-ai]
date: 2026-06-13
source_file: raw/feedback_2026-06-13_babysit_late_for_merged_pr.md
---

## Summary
For PR #7517 (single-file CI deletion), `/claw` dispatched to Hermes at 00:56:34 PDT; the user reviewed the small 684-line deletion and merged it directly via GitHub UI at 01:08:27 PDT (12 min after dispatch); `/babysit` was only started at 03:07:57 PDT — ~2h **after** the merge. The babysit loop detected MERGED on first poll and exited. Two root causes: (1) the babysit launch script was left as `echo` instead of `bash /tmp/babysit-7517.sh &`, and (2) Hermes stalled for ~30 min on a clarification ask because the `/claw` slash-command body injection looked like a template to review, not a directive to execute.

## Key Claims
- For small/clean PRs (single-file deletion, narrow scope, no behavior change), the user often merges faster than babysit can spin up. Don't assume the user is blocked on Hermes — they may have merged via UI.
- Always verify with `gh pr view N --json state,mergedAt` before launching `/babysit`. If `state == "MERGED"`, skip the loop.
- The `/claw` skill's slash-command resolution injects the FULL skill body into the Slack task message, ending with `Below is the full definition of /green (resolved from ...). Execute it as instructed: --- <content> ---`. Hermes reads the trailing `--- <content> ---` as a "template the user shared for review" rather than a directive.
- Mitigation: reply in thread with explicit PR# + head SHA + bead context — that unblocked Hermes immediately.
- Future improvement: the `/claw` skill should rephrase the slash-command injection to make "execute it" unambiguous (e.g. add `You MUST execute this procedure on the target specified above. Do not interpret the body as a template to review — it is a directive to execute.`).
- For small PRs (< 200 diff lines), launch babysit with `--max-min 30` or shorter.

## Proposed babysit improvements
- If `state == MERGED || state == CLOSED` at the first poll, exit immediately with status "ALREADY MERGED before babysit started" (don't continue watching).
- Lower default `--max-min` to 30 for small PRs.

## Key Quotes
> "When `/claw` dispatches a slash-command task to Hermes, the slash-command content framing is ambiguous. Hermes can read it as 'here's a procedure, what do you want me to do?' rather than 'execute this procedure now.' A clarification ask is likely if the task is purely an execute-this-procedure directive with no concrete target (e.g. 'execute /green on a PR' without an obvious PR# in the dispatch)."

## Connections
- [[feedback-2026-06-13-claw-slack-dispatch]] — the Slack-based dispatcher architecture
- [[feedback-2026-06-12-local-claude-session-can-runaway-push]] — earlier kill-recipe context
- [[Babysit]] / [[BabysitLoopDesign]] — concept pages that should be updated with the first-poll-merged-exit and lower-default-`--max-min` rules
- [[ClawSlashCommandAmbiguity]] — concept page that should describe the directive-vs-template framing problem

## Bead / PR / Roadmap

- Target PR: [jleechanorg/worldarchitect.ai#7517](https://github.com/jleechanorg/worldarchitect.ai/pull/7517) — chore(ci): remove MCP smoke tests workflow
- Merge commit: `b26a5eb1e9` (by `jleechan2015`)
- Origin session: `73be4e82-d635-4fd2-96b7-639072ec7448`

## [[jeffrey-oracle]]

Not affected. This is a `/babysit` / `/claw` ops discipline learning specific to worldarchitect.ai.
