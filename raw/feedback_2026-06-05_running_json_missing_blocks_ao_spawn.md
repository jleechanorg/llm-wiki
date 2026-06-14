---
name: running-json-missing-blocks-ao-spawn
description: ao spawn requires ~/.agent-orchestrator/running.json written by ao start; lifecycle-worker alone does not write it
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: 8dfc5e2f-2a26-4883-b6e0-f4e4556ad19b
---

## Context

`ao spawn` fails with "AO is not running — lifecycle polling is inactive" even when a lifecycle-worker process (e.g. PID 91927) is running for the target project.

## Root cause

`ao spawn` calls `ensureAOPollingProject()` → `getRunning()` which reads `~/.agent-orchestrator/running.json`. This file is **only written by `ao start`**, not by individual `ao lifecycle-worker <project>` processes. If the machine was rebooted or `ao start` was never run in the current session, `running.json` is absent and `getRunning()` returns null.

## RunningState format

```typescript
interface RunningState {
  pid: number;        // PID of the ao start process (or lifecycle-worker as proxy)
  configPath: string; // absolute path to agent-orchestrator.yaml
  port: number;       // dashboard port (e.g. 3020)
  startedAt: string;  // ISO8601
  projects: string[]; // list of project names
}
// State file: ~/.agent-orchestrator/running.json
```

## Fix / workaround

Write `running.json` manually when `ao start` was never run:

```python
import json, os
from datetime import datetime, timezone

state = {
  "pid": <lifecycle_worker_pid>,
  "configPath": "/Users/jleechan/.hermes/agent-orchestrator.yaml",
  "port": 3020,
  "startedAt": datetime.now(timezone.utc).isoformat(),
  "projects": ["agent-orchestrator", ...]
}
with open(os.path.expanduser("~/.agent-orchestrator/running.json"), "w") as f:
    json.dump(state, f, indent=2)
```

**Why:** `ao start` is the canonical entry point that writes `running.json`. Individual lifecycle-workers don't because they're sub-processes managed by `ao start`.

**How to apply:** When `ao spawn` errors "AO is not running" but `ps aux | grep lifecycle-worker` shows the process is alive, write `running.json` manually using a lifecycle-worker PID and the correct config path/port.
