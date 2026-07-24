---
title: "Superpowers Cloud Build — Install & Enrollment"
type: source
tags: [cloud-build, superpowers, enrollment, bastion, glm-5.2, dispatch]
date: 2026-07-20
source_file: raw/cloud-build-install-instructions.md
---

## Summary
Superpowers Cloud Build is a remote coding-box service at `cloud.superpowers.build:22` reached via SSH with a shared cloud-build key. It runs GLM-5.2 through its OWN internal proxy (`10.0.100.1:65500`) — NOT OpenRouter. Both the Mac and jeff-ubuntu are enrolled bastion hosts sharing one key; the box authenticates the key, not the machine. New machine enrollment = copy the keypair + state.json + scripts dir from a sibling machine.

## Key Claims
- The box authenticates the **shared cloud-build SSH key**, not the machine → same key on Mac + jeff-ubuntu = both are valid bastion hosts (verified 2026-07-20).
- The box runs GLM-5.2 via its internal proxy, NOT OpenRouter — credit exhaustion on OpenRouter does NOT affect the box.
- The box's **git-secret guard** scans the pushed branch's ancestry and REJECTS repos with secret-bearing commits (e.g. worldarchitect.ai main has `serviceAccountKey.json` @ b0ef410911, old `.env` files).
- Workaround for the git-secret guard = **orphan-snapshot handoff**: `git archive` the work into a fresh 2-commit repo, push to a throwaway `private/*` branch.
- Work branch MUST be `private/*` (box refuses non-private/* branches).
- Enrollment codes are single-use, expire ~5 days. The 2026-07-17 code is expired.
- Official invocation: design + commit a plan in your repo (Superpowers brainstorm + writing-plans), then say "run this plan on the cloud" → the box checks the repo, guides handoff, executes remotely, lands work back.
- Heartbeat stale ≥240s is **normal during long LLM ops**, NOT a wedge — see [[feedback-2026-07-20-cloud-build-heartbeat-stale-during-llm]]. Do NOT abort on heartbeat-stale alone; only abort if `cloud_build_fetch_status` shows the run FAILED. When `head_sha` advances, call `cloud_build_land_result` to fetch the commit.

## Key Quotes
> "Cloud Build will check the repository, guide the handoff, ask for the enrollment code above on your first run, execute the plan remotely, and land the completed work back in your repository."

> "cloud-bastion: interactive shell is not permitted" — the box accepted the key but refuses interactive shells; git push is the real channel. (jeff-ubuntu direct SSH probe, 2026-07-20)

## Connections
- [[SuperpowersCloudBuild]] — the box service itself
- [[CloudBuildBastionHost]] — both Mac + jeff-ubuntu as enrolled dispatch hosts
- [[CloudBuildOrphanSnapshotHandoff]] — the git-secret-guard workaround
- [[SuperCommand]] — the slash entry that dispatches to the box
- [[SuperlightCommand]] — legacy local-GLM-5.2 router (claudeg/OpenRouter), NOT the box
