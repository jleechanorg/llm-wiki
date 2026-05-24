---
title: "CXDB"
type: concept
tags: [attractor-pattern, observability, checkpoint, execution-database]
date: 2026-05-24
---
## Overview
CXDB (Code eXecution Data Base) is a special-purpose observability layer that records every interaction in the Attractor pipeline execution. It serves as both an audit log and a recovery mechanism — run history is stored in CXDB while code history is in git.

## Key Properties
- **What**: Execution database that records typed run events (started, finished, checkpoint, completed/failed) and artifacts (logs, outputs, archives)
- **Why matters**: Enables resume-from-CXDB, Healer diagnosis, and full execution replay; "git branch is code history; CXDB is run history"
- **Implementation**: SQLite with WAL mode + 5s busy_timeout for concurrent pipeline access; records (run_id, seq, node, outcome, ts, output_hash, output_head, metadata) per step

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| [[Kilroy]] | Runner | Uses CXDB for checkpoint recovery and resume |
| [[HealerAgent]] | Agent | Reads CXDB to cluster failures and emit diagnoses |
| [[DarkFactory]] | Repo | dark-factory runner records to CXDB via --cxdb flag |

## Connection to Attractor Pattern
CXDB is the observability backbone of the Attractor pattern. Without it, you can't observe agent behavior, cluster failures, or auto-diagnose problems — all essential for the dark factory where nobody reads the code.

## See Also
- [[HealerAgent]]
- [[AttractorPattern]]
- [[DurableExecution]]
- [[EventSourcingForAgents]]
