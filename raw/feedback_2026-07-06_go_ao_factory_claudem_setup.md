---
name: Go AO factory dispatch + claudem-equivalent MiniMax routing
description: dark-factory /af now uses Go ao-go (not TS ao-ts); MiniMax via project env sync --all; claudem harness name requires mirror patch
type: feedback
bead: jleechan-sy4m
---

## Context

2026-07-06: Switched factory AO dispatch from TypeScript `@jleechanorg/ao-cli` to the Go mirror at `~/projects/agent-orchestrator-mirror`, built as `~/bin/ao-go` with `~/bin/ao` symlink. TS fallback preserved as `~/bin/ao-ts`.

## Technical detail

- **Go daemon**: headless `ao-go daemon` on `:3001`, data `~/.ao/data` — NOT `ao start` (opens Electron app).
- **Factory scripts**: `daemon/factory-ao-bin.sh` resolves Go first; `factory-ao-remediate.sh` spawns with 120s timeout; `factory-af-tick.sh` uses JSON session cap (30).
- **claudem / MiniMax**: Bash `claudem()` from `~/.bashrc` is NOT callable by Go AO (tmux exec, no bashrc). `--worker-agent claudem` rejected (`unknown harness`). Equivalent: `claude-code` + project env via `daemon/factory-ao-minimax-sync.sh --all` (requires `MINIMAX_API_KEY`).
- **Global CLI**: `~/bin/claudem` executable mirrors bashrc routing for any repo.
- **Session namespaces**: Go `worldarchitect-N` vs legacy TS `wa-N` are separate; kill TS zombies before dispatch.
- **Cap**: `AO_MAX_CONCURRENT_SESSIONS=30` (was 20).

## Rule / pattern

1. Factory `/af` → Go `ao-go`, not TS, unless `AO_BIN=~/bin/ao-ts`.
2. After `ao project add`, run `bash daemon/factory-ao-minimax-sync.sh --all` (remediate runs this automatically).
3. Do not expect harness name `claudem` in config without mirror code change.
4. Register target repo once: `ao project add --id <id> --path <git-root> --worker-agent claude-code`.

## Verification

- `ao version` → `dev` from `ao-go`
- `ao status --json` → `"state": "ready"`, port 3001
- `ao spawn --project worldarchitect --name test --agent claude-code --prompt ...` → process shows `--model MiniMax-M3`, `ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic`
- `factory-ao-minimax-sync.sh --all` → ok per registered project

## References

- Mirror: `/Users/jleechan/projects/agent-orchestrator-mirror` (upstream AgentWrapper/agent-orchestrator)
- Scripts: `dark-factory/daemon/factory-ao-bin.sh`, `factory-ao-minimax-sync.sh`, `factory-ao-remediate.sh`, `factory-af-tick.sh`
- PRs under test: [#8058](https://github.com/jleechanorg/worldarchitect.ai/pull/8058), [#8116](https://github.com/jleechanorg/worldarchitect.ai/pull/8116), [#8061](https://github.com/jleechanorg/worldarchitect.ai/pull/8061)
- Beads: jleechan-9byt.1/.2/.5
