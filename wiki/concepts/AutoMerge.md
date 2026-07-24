---
title: "Auto-Merge"
type: concept
tags: [auto-merge, automation, github-actions]
sources: []
last_updated: 2026-07-11
---

## Definition
Auto-merge is a GitHub feature that automatically merges a PR when all required checks pass. In the AO/Cursor workflow, this is controlled by skeptic-cron workflow but can be disabled via configuration.

## Controls
- **Enable all**: Set `SKEPTIC_CRON_AUTO_MERGE` to `true` or delete variable
- **Disable all**: Set `SKEPTIC_CRON_AUTO_MERGE` to `false`
- **Selective hold**: Add PR numbers to `SKEPTIC_MERGE_DENYLIST`

## Use Case
Auto-merge is disabled for PRs requiring manual verification or when coordination with other PRs is needed before merging.

## dark-factory merge-guard pathway (2026-07-10 incident)
A second, separate auto-merge mechanism lives in dark-factory: `daemon/scripts/auto-merge-guard.sh` on a 60s systemd timer greps `daemon.jsonl` for the latest GATE_ASSESSMENT per factory/* PR and squash-merges when no gate verdict is `fail`/`red` (warn/unknown non-blocking; `all_green` ignored; READY_FOR_MERGE events invisible). Recording a no-fail assessment is therefore the merge command itself. Proven live: PR #228 (first zero-touch merge, 13:48 PDT 2026-07-10) and the PR #207 incident (merged 18s after a subagent's assessment despite a standing no-merge directive). Freeze mechanism: `systemctl --user stop dark-factory-merge-guard.timer`. See [[feedback-2026-07-10-gate-assessment-is-merge-authorization]] and beads jleechan-81v4 (interlock), jleechan-98v3 (multi-writer CXDB).
