---
name: claimed-working-vs-actually-working
description: Every "merged + deployed + live" claim must include end-state-layer probes — bind-mount, gh API state, hook md5 inside container — not just the implementation-layer tool output
type: feedback
bead: none
---

## Context

After 4 runner-fleet hardening PRs merged (#7851, #8024, #8026, #8027), I claimed "runners healthy, fleet operational" based on:
- Merge succeeded ✓
- Green Gate passed ✓
- Lima VM SSH works ✓
- Watchdog cron installed ✓
- Container is Up (Up X minutes) ✓

The /advice reviewer caught this as MEDIUM confidence — "claimed working ≠ actually working until proven otherwise."

Probes revealed:
1. ✅ Bind-mount source on Lima VM DID match the deployed path (`/home/jleechan.linux/.local/share/...`)
2. ✅ gh auth on Mac has admin:org scope (check_github_session_state will actually fire)
3. ⚠️ Pre-job-hook inside running container has correct md5 — GITHUB_REPOSITORY will be set by runner before hook fires
4. ❌ Reviewer caught a missed issue: `check_github_session_state` filtered only `^org-runner-mac-`, missing the same session-conflict class on the 16 Linux runners
5. ❌ Reviewer caught: silent skip on `gh api` failure returned 0 — exactly the silent-divergence class the function was built to catch

This memory entry captures the general principle + the 5 specific probe types.

## The 5 silent-divergence / end-state-layer probes

Any claim of "X is working" for runner-infrastructure work must include at least these 5 probe results:

### Probe 1 — Bind-mount vs COPY trap

Docker image `myoung34/github-runner` has its own hook path expectation. Any custom hook path requires explicit bind-mount from the deployed VM path. The deploy is no-op if the running container's bind-mount source doesn't match where you wrote the file.

```bash
# Verify hook actually reached the running container's bind-mount source
ssh jeff-ubuntu "
  for CONT in org-runner-1 org-runner-5 org-runner-10; do
    ~/.local/bin/limactl shell colima -- docker inspect \$CONT \
      | jq '.[0].Mounts[] | select(.Destination == \"/usr/local/bin/pre-job-hook.sh\")'
  done
"
# Expect: Source = the path where you deployed the file (NOT a phantom path)
```

**Failure mode if you skip this:** Your code merged, your script changed on disk, but the running container is reading a stale version because the bind-mount source diverged.

### Probe 2 — Hook content md5 inside running container

Even with correct bind-mount source, the file content can diverge (e.g., permissions issue, symlink target missing).

```bash
ssh jeff-ubuntu "
  ~/.local/bin/limactl shell colima -- docker exec \$(... docker ps -q | head -1) \
    md5sum /usr/local/bin/pre-job-hook.sh
"
# Expect: md5 matches the file on the deployed VM path (run md5 there too to compare)
```

**Failure mode if you skip this:** Mount source is correct path, but file is empty/wrong content due to copy bug.

### Probe 3 — GITHUB_REPOSITORY + key env vars set by runner before hook

When the hook reads `${GITHUB_REPOSITORY##*/}` to derive REPO_NAME, the runner must set GITHUB_REPOSITORY BEFORE invoking the hook. If not, the fallback path fires silently.

```bash
# Watch a real CI run's hook output for the GITHUB_REPOSITORY value:
gh run view <id> --log 2>/dev/null | grep -A2 "ACTIONS_RUNNER_HOOK_JOB_STARTED\|pre-job-hook\|disk low\|REPO_NAME"
```

**Failure mode if you skip this:** Hook runs but ${GITHUB_REPOSITORY:-} resolves to empty, fallback path no-ops, cleanup never happens.

### Probe 4 — GitHub-side runner registration state ≠ container state

The most critical probe: container can be Up + Listening while GitHub shows offline (session-conflict class — Runner.Listener stuck in `Error: Conflict. Retrying until reconnected.`).

```bash
gh api orgs/jleechanorg/actions/runners \
  --jq '.runners[] | select(.name | test("^org-runner")) | {name, status, busy}'
# Compare against:
docker ps --filter "name=org-runner" --format "{{.Names}}\t{{.Status}}"
# If status=offline in GitHub but container=Up locally → session conflict
# Heal: gh api -X DELETE .../runners/<id> && docker restart <name>
```

**Failure mode if you skip this:** "Runners healthy" claim is wrong; jobs are NOT being dispatched; CI degrades silently.

### Probe 5 — Cross-check `gh api` itself works

The health-monitor function that catches divergence returns 0 silently if `gh api` itself fails. This is the meta-divergence: the divergence detector is offline.

```bash
gh auth status  # must show active account + admin:org scope
gh api orgs/jleechanorg/actions/runners --jq '.total_count'
# Both must succeed for check_github_session_state() to actually fire
```

**Failure mode if you skip this:** gh CLI expires on the MacBook or org scope is revoked; function silently returns 0; no alerts; session-conflicts recur undetected.

## The general principle (also captured in ~/.claude/CLAUDE.md "Verify end-state layer" section)

When a tool reports "success" or "healthy" (e.g. `Listening for Jobs`, `Up 4 minutes`, `=== done: healthy ===`), that's the **implementation layer** saying the tool did its part. It does NOT prove the **end-state layer** is correct.

| Tool layer | End-state layer (must verify) |
|------------|------------------------------|
| Runner.Listener logs `Listening for Jobs` | `gh api .../runners` shows `status:"online"` |
| Container `Up X minutes` | Health check returns 200 |
| `git push` success | PR appears in `gh pr list` |
| `npm test` exit 0 | CI workflow run `conclusion:"success"` |
| `docker compose up -d` exits 0 | `docker ps` shows `Up` |

Rule: Before claiming "X is working", verify at the end-state layer. If you can only cite the implementation-layer tool's output, say so explicitly.

## Existing coverage (already saved by the post-merge harness fixes)

- [x] `~/.claude/CLAUDE.md:226-249` — general end-state-layer principle (captured 2026-06-28)
- [x] repo `CLAUDE.md:132-134` — "Post-merge runner fleet validation" section
- [x] memory `feedback_2026-06-28_runner_session_conflict.md` — the specific session-conflict class
- [x] `.claude/skills/runner-session-conflict/SKILL.md` — heal procedure

## How to apply (rules for future agent)

1. After merging any PR that touches runner infrastructure, run ALL 5 probes above before claiming success.
2. Save this memory to feedback docs — the 5-probe checklist is durable.
3. When adding new check functions to runner health monitors, **NEVER** return 0 silently on the health-check API call itself failing (silent skip = meta-divergence).
4. The `find -printf '%T@ %f\n'` pattern silently returns empty on empty dirs — always check for empty result and fail-open (use disk-threshold cleanup path even if REPO_NAME is unknown) rather than silently no-oping.

## References

- Session: 2026-06-28 (post PR #7851, #8024, #8026, #8027 merge)
- /advice reviewer verdict: MEDIUM confidence — probes required
- Memory: [[runner-session-conflict]] — sibling memory on the specific session-conflict class
- Skill: [[runner-session-conflict]] at `.claude/skills/runner-session-conflict/SKILL.md`
