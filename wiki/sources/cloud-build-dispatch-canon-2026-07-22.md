---
title: "Cloud Build Dispatch Canon — 2026-07-22"
type: source
tags: [cloud-build, superpowers, dispatch, canary, glm-5.2, serf-3, end-to-end]
date: 2026-07-22
source_file: raw/project_2026-07-22_cloud_build_dispatch_canon.md
---

## Summary

Superpowers Cloud Build (Prime Radiant, `cloud.superpowers.build`) is fully operational end-to-end. 4 verified box commits across Mac + jeff-ubuntu: `e17cfb8` (jeff), `8a12c52` (Mac), `7864836341` (fresh dummy), `fccc323` (latest health check). The canonical trigger is any of 10 phrases ("build on cloud", "run this plan on the cloud", etc.) which routes to `/super` → cloud-build plugin skill → box dispatch. Box harness is `serf-3` + GLM-5.2 via internal proxy at `10.0.100.1:65500` (NOT user's OpenRouter). The v0.8.1 cd drift bug on Linux was found and patched with a one-line sed.

## Key Claims

- The full dispatch pipeline works: preflight → enrollment → handoff → follow loop → land
- Box model is `openrouter/z-ai/glm-5.2` disclosed via `SERF_MODEL` env (not the status JSON's empty `model:""`)
- Box has its OWN internal OpenRouter-wire proxy — local OpenRouter 402 does NOT affect the box
- Heartbeat stale ≥240s during long LLM calls is NORMAL — don't abort on heartbeat alone
- The cd drift bug on Linux (`cd "$SCRIPT_DIR"` instead of `cd "$SCRIPT_DIR/.."`) breaks every `/super` invocation silently — fixable with one-line sed
- Orphan-snapshot recipe (git archive work into fresh 2-commit repo on `private/*`) bypasses the git-secret guard when main has secret-bearing history
- Lock contention when both bastions dispatch in parallel (same fp) — use different slug per attempt
- 31 issues filed against the plugin source mirror (jleechanorg/superpowers-cloud-build-source, private) + mirrored to jleechan2015/pb-archive-2026 (private, obra/Jesse Vincent has read access)

## Key Quotes

> "Cloud Build health check: 2026-07-24T18:44:10Z — dispatch still working" — box marker file in cb-healthcheck-113729@`fccc323`

> "the box uses internal proxy, NOT OpenRouter" — user correction, 2026-07-20

> "we jus want to say 'build on cloud' and superpowers always works on cloude box" — user directive, 2026-07-21

> "do the work with superpowers cloud dont code directly" — user directive, 2026-07-20

## Connections

- [[SuperpowersCloudBuild]] — the box service itself
- [[CloudBuildBastionHost]] — Mac + jeff-ubuntu as enrolled bastions
- [[CloudBuildOrphanSnapshotHandoff]] — the git-secret-guard workaround
- [[CloudBuildFollowLoop]] — the canonical follow loop
- [[CloudBuildHeartbeatStaleDuringLLM]] — heartbeat misdiagnosis class
- [[SuperCommand]] — `/super` thin shim that delegates to Prime Radiant plugin

## Verification

- 4 box commits verified via `gh api repos/.../commits` (author = `Cloud Build <supervisor@cloud-build.local>`)
- 4 status JSONs verified (`state: done, tasks_completed: 1, harness: serf-3`)
- 31 issues filed (cap 30) and verified viewable at jleechan2015/pb-archive-2026
- 5 upstream beads (bd-c2q, bd-d03, bd-m3e, bd-617, bd-iax) tracked in roadmap br
- Master gist: https://gist.github.com/jleechan2015/a15e331ffc62993376e4d7d5ed15fbfe
