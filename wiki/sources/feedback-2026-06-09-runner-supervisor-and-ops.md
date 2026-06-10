# Runner supervisor + RC sourcing + GitHub-side busy state (PR #7271)

**Date**: 2026-06-09
**Type**: feedback
**Classification**: 🚨 Critical (anti-pattern, repeatedly blocks Mac fleet recovery)

## Context

Self-hosted GitHub Actions runners on macOS run inside a launchd-supervised
Docker container pool. The original supervisor (`self-hosted-oss/launchd-start.sh`)
was a one-shot wrapper around `heal-runners.sh` — launchd would mark the agent
"not running" after a single bad cycle and wait up to 3600s (`StartInterval`)
before retrying, far too long for a CI outage.

The full learn is split across two memory files:

- `feedback_2026-06-03_self_hosted_race_fix.md` — the `docker_rm_force_with_timeout` race fix (sync `docker rm -f` + poll `docker ps -a` until container disappears). This is the underlying Docker cleanup primitive.
- `feedback_2026-06-09_runner_supervisor_and_ops.md` — the supervisor + ops layer around it: loop pattern, RC sourcing isolation, GH-side `busy=true`, hard-reset order, stable-install sync, PR-cancel collateral damage. **This file.**

PR: [jleechanorg/worldarchitect.ai#7271](https://github.com/jleechanorg/worldarchitect.ai/pull/7271) — merged 2026-06-07T22:06:25Z by jleechan2015, merge commit `bdaadff0f5f156f23639a44e6e0fc7d01ff95307`.

## Summary of rules

1. **Supervisor is a `while true; ...; sleep 300` loop with `set -uo pipefail` (NOT `set -e`)** so a transient heal failure cannot kill the loop. `KeepAlive` + one-shot + `set -e` was three independently-broken assumptions; replacing them with their opposites is a single, testable change.
2. **bashrc sourcing needs `set +u` AND `set +e` around the rc-sourcing block** — `cmux-bash-integration.bash` touches `$PROMPT_COMMAND` (aborts `set -u`) and many user dotfiles run `set -o errexit` (which would re-enable errexit in the supervisor and convert logged failures into fatal exits).
3. **GH-side `busy=true` corruption on all 16 self-hosted runners is local-unrecoverable** — wait ~1h for GH session-timeout or admin DELETE. Local actions cannot clear it; attempting to do so is wasted work.
4. **Hard-reset order: `docker stop` → `docker rm -f` → `docker volume rm`.** Volume fails with `is in use` if the container is still attached. `docker rm -f` does NOT stop a running container on some Docker versions — stop must happen first.
5. **`Session already exists` loop on a container = full recreation.** The `.runner` file in the named volume holds stale credentials tied to a GH-side session; full container recreation with a fresh named volume is the only fix. Editing `.runner` alone does not help.
6. **Stable install path `~/.local/share/worldarchitect-runners/` is what launchd runs from, NOT the worktree copy.** After every edit to the worktree scripts, `cp` them to the stable install. If you forget, `heal-runners.sh` exits with code 127 and the fix is invisible.
7. **PR-cancellation fanout subagents must also protect the in-flight /green PR**, not just the user's pre-declared protected set. Otherwise the cancel subagent kills the CI runs the /green subagent just pushed for.

## Verification after deploy

```bash
launchctl print gui/$(id -u)/com.worldarchitect.org-runners   # state=running, last exit code=0
tail -f ~/.local/share/worldarchitect-runners/supervisor.log # one full 5-min cycle OK
docker ps | grep org-runner                                   # full pool Running
```

## References

- Companion memory: `feedback_2026-06-03_self_hosted_race_fix.md` (race in `docker_rm_force_with_timeout`)
- Memory file: `~/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-09_runner_supervisor_and_ops.md`
- Roadmap entry: `~/roadmap/learnings-2026-06.md` § 2026-06-09
- Bead: `rev-5ysuv` (closed 2026-06-09)
- PR: [jleechanorg/worldarchitect.ai#7271](https://github.com/jleechanorg/worldarchitect.ai/pull/7271)

## Concept pages updated

- `[[Self-Hosted-Runner-Infra-Flake-vs-Real-Failure]]` — adds the supervisor-loop and busy=true failure modes
- `[[Launchd]]` — adds the `set +u` + `set +e` rc-sourcing isolation rule
- `[[SelfHostedRunnerNaming]]` — stable install path requirement

## [[jeffrey-oracle]]

Not affected. This is a technical operations learning specific to the
self-hosted runner infra.
