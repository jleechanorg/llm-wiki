# AO Cursor workers — 7-green queue (no auto-merge)

Use this when **Agent Orchestrator** + **Cursor** workers should drive fixes until **7-green** (CI + CR + Bugbot + threads + evidence + skeptic verdict), while **skeptic-cron must not merge** selected PRs automatically.

## GitHub repository variables (`jleechanorg/worldarchitect.ai`)

| Variable | Purpose |
|----------|---------|
| `SKEPTIC_MERGE_DENYLIST` | Comma-separated PR numbers **never** merged by `.github/workflows/skeptic-cron.yml` when 7-green. |
| `SKEPTIC_CRON_AUTO_MERGE` | Set to `false` to disable **all** skeptic-cron merges (optional). Default `true`. |

Set or update the denylist:

```bash
# Example: queue from P0/P1 beads (adjust when PRs merge or new ones open)
gh variable set SKEPTIC_MERGE_DENYLIST -b '6094,6086,6093,6095,6034,6069' -R jleechanorg/worldarchitect.ai
```

Merged/closed PRs on the list are harmless (merge step no-ops). Trim the list periodically. Clear when auto-merge is OK:

```bash
gh variable delete SKEPTIC_MERGE_DENYLIST -R jleechanorg/worldarchitect.ai
```

## WorldArchitect.AI — bead → PR mapping (verify state before claiming)

Check `gh pr view <n> -R jleechanorg/worldarchitect.ai` before dispatch; PRs close/merge often.

| Priority | Bead | PR | Focus |
|----------|------|-----|--------|
| P0 | rev-n2td | [#6094](https://github.com/jleechanorg/worldarchitect.ai/pull/6094) | Self-hosted MVP shards / Firestore transaction (verify merged/closed) |
| P0 | rev-3srb | [#6086](https://github.com/jleechanorg/worldarchitect.ai/pull/6086) | Deploy `gcloud` `--quiet` / ABORTED retry (verify merged/closed) |
| P1 | rev-smrb | [#6093](https://github.com/jleechanorg/worldarchitect.ai/pull/6093) | JWT / auth hardening (verify merged/closed) |
| P1 | rev-1j5h | [#6095](https://github.com/jleechanorg/worldarchitect.ai/pull/6095) | Core test infra + skeptic workflows (verify merged/closed) |
| P1 | rev-zz65 | [#6034](https://github.com/jleechanorg/worldarchitect.ai/pull/6034) | Custom Campaign Wizard re-enable (**often still open**) |
| P1 | rev-bn76 | [#6069](https://github.com/jleechanorg/worldarchitect.ai/pull/6069) | Skeptic align with AO (verify merged/closed) |

**Workflow / upstream (not a single WA PR):** **rev-ev01**, **rev-f0pa** (evidence CI + AO evidence-gate port), **rev-g41u** (`jleechanorg/agent-orchestrator` **PR #335** installer), **rev-skptzerojobs** (skeptic trigger / zero jobs).

## OpenClaw / harness (outside `worldarchitect.ai` PRs)

| Bead | Topic |
|------|--------|
| rev-rev9p4n | `no_worktree` result missing `exit_code` — pair live completion |
| rev-revgejn | pairv2 retry — `git worktree` not pruned on terminate |

Land fixes in the **openclaw / harness / agent-orchestrator** repo; WA `skeptic-cron` does not apply.

## Operator checklist

1. Set `SKEPTIC_MERGE_DENYLIST` to every **open** PR you want held back (re-run `gh pr list` first).
2. Run AO / Cursor workers until checks pass and skeptic posts **VERDICT: PASS** on the current head SHA.
3. Merge manually when ready; remove PR numbers from the denylist or delete the variable.
