---
title: "Config-First Principle"
type: concept
tags: [config-first, openclaw, soul-md, tools-md, python-as-last-resort, orchestration]
last_updated: 2026-04-05
sources: [jleechanclaw-operational-runbook, jleechanclaw-orchestration-system-design]
---

## Summary
Before writing Python code in `src/orchestration/`, always check if the goal can be achieved by editing openclaw config files at the repo root. openclaw has rich built-in capabilities (SOUL.md, TOOLS.md, cron/, openclaw.json) that should be exhausted before adding Python code.

## The Hierarchy

| Want to change | Edit this |
|---|---|
| jleechanclaw behavior / decision-making | `SOUL.md` |
| Tool allow/deny list | `TOOLS.md` or `openclaw.json` |
| Memory, history, compaction settings | `openclaw.json` |
| Cron / scheduled tasks | `cron/` at repo root |
| PR automation jobs | `~/.openclaw/cron/jobs.json` directly (exception, not tracked in repo) |
| AO project config / reactions / notifiers | `<worktree>/agent-orchestrator.yaml` → PR → merge |
| New Python orchestration logic | `src/orchestration/` — **only if config cannot express it** |

## Why Config-First

Python code in `src/` requires: compile, test, deploy. Config changes take effect immediately (for openclaw) or after restart. Config is:
- Easier to audit
- More portable across model updates
- Less likely to break when the orchestration layer is replaced
- Already what the LLM reads on every turn

## openclaw.json Mutation Rules

**NEVER rewrite the entire file.** Full rewrites silently drop config sections. Always use surgical updates:

```python
with open(path) as f: d = json.load(f)
d['some']['nested']['key'] = new_value
with open(path, 'w') as f: json.dump(d, f, indent=2)
```

Protected keys (enforced by `doctor.sh`, treat as immutable unless Jeffrey explicitly authorizes):
- `agents.defaults.heartbeat.every` → `"5m"`
- `agents.defaults.heartbeat.target` → `"last"`
- `agents.defaults.timeoutSeconds` → `≤ 600`
- `agents.defaults.maxConcurrent` → `≤ 3`
- `agents.defaults.subagents.maxConcurrent` → `≤ 3`
- `plugins.slots.memory` → `"openclaw-mem0"` (without this, mem0 silently disabled)

## Indicator: When to Write Python

If the goal is:
- Routing based on content/meaning → LLM, not Python if-else
- Transforming data deterministically → Python OK
- Changing agent behavior/convention → SOUL.md/AGENTS.md/CLAUDE.md
- Scheduling → cron/ files
- Reacting to CI/review state → AO yaml reactions

New Python in `src/orchestration/` is only justified for capabilities that genuinely don't exist in openclaw's config surface.

## Related Concepts
- [[HarnessEngineering]]
- [[GatewayRestartSafety]]
- [[AutonomousAgentLoop]]