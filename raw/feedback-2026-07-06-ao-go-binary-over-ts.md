---
name: prefer-ao-go-binary-over-ts-for-dispatch-and-status
description: "User explicitly prefers `/Users/jleechan/bin/ao-go` (the Mach-O Go-AO binary in tracker repo) over the TS-ao wrapper; the TS-ao and Go-ao are separate daemons. Go-AO HTTP server listens on 127.0.0.1:3001 but DOES NOT serve GET / (returns ROUTE_NOT_FOUND). Use `ao session ls` + tmux attach instead of expecting a web dashboard."
metadata: 
  node_type: memory
  type: feedback
  bead: jleechan-evk5
  originSessionId: d421bc04-a527-477c-ace9-9ba022848a4a
---

# Prefer AO Go binary over TS for factory dispatch + status

## What happened (2026-07-06)

When user asked for "the ao golang repo" and to "see how the ao golang repo works", I investigated:

1. `/Users/jleechan/bin/ao` is a **Mach-O 64-bit arm64** executable (the TS-AO wrapper around the Node.js orchestrator).
2. **GO-AO** is `/Users/jleechan/bin/ao-go` (also Mach-O, from `/Users/jleechan/projects/tracker/cmd/tracker`).
3. The **GO-AO server** is the one bound to `127.0.0.1:3001`. `curl http://localhost:3001/` returns:
   ```
   {"error":"not_found","code":"ROUTE_NOT_FOUND",
    "message":"GET / has no handler",
    "requestId":"jeffreys-macbook-pro.local/O53yHJuAzc-000648"}
   ```
4. The GO-AO source at `/Users/jleechan/projects/tracker/cmd/` does have HTTP handlers, but no `/` route — likely only API/JSON routes. The TS-AO has the actual web dashboard (Next.js frontend), but TS-AO's live console had a known bug (`noServer: true` fix in [agent-orchestrator PR #648](https://github.com/jleechanorg/agent-orchestrator/pull/648)).

## User correction

User stated explicitly: **"I want to use the golang binary — stop forgetting"**. After multiple turns I kept defaulting to the TS-ao wrapper for `ao session ls` etc. The fix: distinguish TS-AO (`/Users/jleechan/bin/ao`, Node.js) from Go-AO (`/Users/jleechan/bin/ao-go`, Mach-O binary).

## What works

- **Status / session listing**: `ao session ls` (works against either daemon — they're the same `ao` CLI surface backed by the locally-bind server on :3001).
- **HTTP query**: `curl http://127.0.0.1:3001/api/...` or per the tracker repo's `cmd/` HTTP routes (need to enumerate with `grep -rn 'HandleFunc' /Users/jleechan/projects/tracker/cmd/tracker/*.go`).
- **Web dashboard**: there isn't a `/` handler on :3001; do NOT expect one. The TS-AO dashboard (port 3020+) is separate and has known issues.

## What the GO-AO repo offers

`/Users/jleechan/projects/tracker/` (also called `agent-orchestrator` upstream):
- `cmd/tracker/` — main HTTP server (port 3001, dashboard port varies)
- `pipeline/handlers/` — parallel reviewer (`parallel.go`), conditional, fanout, codergen, decider, exit, etc.
- `pipeline/handlers/parallel.go` — concurrent goroutines per branch target, JSON-aggregated results
- `examples/consensus_task.dot` — multi-model consensus (Opus + Gemini + GPT parallel via DoD rubric)
- `examples/subgraphs/final-review-consensus.dip` — multi-model final review + cross-critique + synthesize → conservative-merge with the iron law "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE"
- `pipeline/expand.go` — branch-from-candidates fan-out
- Verification: PERFECT for the `/af` verifier mode — the daemon's `daemon/src/verifier.rs::assess` should integrate this multi-vendor consensus + cross-critique instead of single-skeptic.
- HTTP routes: search `cmd/tracker/*.go` for `HandleFunc` and `http.Handle` to enumerate (likely `/api/sessions`, `/api/projects`, etc.; no `/`).

## Anti-pattern (DON'T)

- Re-discovering that `ao-g`o is the Go binary every turn.
- Trying to `curl http://localhost:3001/` and expecting HTML — it returns JSON `ROUTE_NOT_FOUND`.
- Defaulting to the TS-ao wrapper when the user references "ao golang repo" or "the golang binary" — they specifically mean `/Users/jleechan/projects/tracker` (Go AO upstream).
- Forwarding to agent-orchestrator's known dashboard console bug as if it's the current state — that fix shipped in PR #648.

## Verification

```
$ file /Users/jleechan/bin/ao /Users/jleechan/bin/ao-go
/Users/jleechan/bin/ao:    Mach-O 64-bit executable arm64  ← TS-AO wrapper
/Users/jleechan/bin/ao-go: Mach-O 64-bit executable arm64  ← Go-AO (the one user prefers)

$ lsof -nP -iTCP -sTCP:LISTEN | grep ":3001"
ao-go  27164  jleechan  IPv4 127.0.0.1:3001  TCP 127.0.0.1:3001 (LISTEN)

$ curl -s http://127.0.0.1:3001/
{"error":"not_found","code":"ROUTE_NOT_FOUND","message":"GET / has no handler","requestId":"jeffreys-macbook-pro.local/O53yHJuAzc-000658"}

$ /Users/jleechan/bin/ao-go status --json | jq .state
"ready"

$ ao session ls | head -5
worldarchitect:
  worldarchitect-1   (1h)     [no_signal]   worker
  worldarchitect-11  (12m)    [working]     worker
  ...
```

## How to apply

When the user says "ao golang repo", "the golang binary", "tracker", or "agent-orchestrator":
- Open `/Users/jleechan/projects/tracker/` to read Go-AO reference impl
- For HTTP server behavior, look in `cmd/tracker/*.go` for `HandleFunc` / `http.Handle`
- For worker consensus patterns, look in `pipeline/handlers/parallel.go` + `examples/subgraphs/final-review-consensus.dip`
- For `/af` verifier integration, treat the multi-vendor `final-review-consensus.dip` pattern as the canonical reference (vs. the daemon's single-skeptic + iteration-stub today)

**Cross-reference**: [[feedback_2026-05-30_ao_darkfactory_worker_bringup]] (prior AO worker bringup details), [[reference_2026-06-21_official_dynamic_workflows_vs_dotfactory]] (parser vs Go-AO dist)
