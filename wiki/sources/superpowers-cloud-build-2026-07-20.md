---
title: Superpowers Cloud Build — install + 3rd-execution-mode spec (2026-07-20)
type: source
tags: [superpowers, cloud-build, remote-execution, plugin, prime-radiant, ssh, hermetic, plan-execution]
created: 2026-07-20
updated: 2026-07-20
sources:
  - superpowers-cloud-build-2026-07-20.md
last_updated: 2026-07-20
---

# Superpowers Cloud Build — what it is and what it does differently

Verified 2026-07-20 from local plugin source at `~/superpowers-cloud-build-main/` (v0.8.1, author Prime Radiant, Inc.) and Slack thread `C09GRLXF9GR/p1784573431`.

## TL;DR

`superpowers-cloud-build` is a plugin that adds a **3rd execution mode** to the Superpowers `plan.md` workflow. Instead of running the plan with local subagents, you push the frozen work branch + a control JSON to `cloud.superpowers.build:22`; a remote box provisions on demand and commits as `Cloud Build <supervisor@cloud-build.local>`. Run state rides on two git branches (`cloud/control` you write, `cloud/status` the box writes).

## What it adds that normal Superpowers doesn't

- **Remote execution** — commits authored by the box's identity, not yours
- **Pinned host key + per-project box ownership** (one client key per project)
- **Server-enforced `refs/heads/private/*` work-branch policy**
- **Preflight hermeticity gate** — `preflight-local.sh` requires `CLOUD_HERMETIC_CONFIRMED=1`
- **`needs_input` Q&A loop** — box emits `qid`/`prompt`; client pushes answer via `cloud_build_mk_answer`
- **Abort + box reaping** — `cloud_build_mk_abort` triggers supervisor kill
- **One bounded retry on `provisioning_timed_out`** — frozen run_id replayed once
- **Fail-safe land** — diverged commits saved under `refs/cloud-build/landed/<run_id>`

## What it does NOT do (the big traps)

- ❌ Cannot `/green` existing PRs — writes only to `cloud/control` + `cloud/status`
- ❌ Does not bypass server-side git secret guard
- ❌ Cannot start the box yourself (door provisions on demand)
- ❌ macOS zsh refspec corruption — always run from bash, never source `lib-client.sh`
- ❌ Function name confusion: use `cloud_build_handoff`, NOT `cloud_build_hand_off_run_plan`

## 5-step protocol

```
Preflight → Setup/connect → Hand off → Follow loop (10-min cadence) → Land
```

Full skill text: `~/superpowers-cloud-build-main/skills/cloud-build/SKILL.md` (read in full).

## Verified end-to-end

- **Plugin installed:** `codex plugin list | grep cloud-build` → `installed, enabled, 0.8.1`
- **Enrollment valid:** `~/.config/cloud-build/state.json` shows `contract_version=cloud-build-friend-v0`, host `cloud.superpowers.build`, ed25519 identity at `~/.ssh/cloud-build/id_ed25519`, pinned host key
- **Real work:** [PR #8466](https://github.com/jleechanorg/worldarchitect.ai/pull/8466) for issue #8353 — orphan-snapshot handoff, 4 Cloud Build–authored commits, 12/12 hermetic tests, box model GLM-5.2 on `serf` harness

## See also

- [[Prime Radiant]] — plugin author
- [[Cloud-Superpowers-Build]] — remote build host
- [[Superpowers-Plan-Execution-Modes]] — the 3-mode framework
- [[Drive-PR-To-Green]] — for `/green` on existing PRs (NOT a cloud-build substitute)
- Source report: `~/roadmap/superpowers-cloud-build-2026-07-20.md`
- Memory: `~/.claude/projects/-Users-jleechan/memory/feedback_2026-07-20_superpowers_cloud_build_install_and_differences.md`
