---
name: mem0-qdrant-broken-mem0-unavailable-diagnose-the-launcher-not-the-api-key
description: "When `mem0 unavailable` is the only symptom, the cause is almost always the qdrant launcher (Docker wait / launchd cwd / cwd-relative storage paths), not an API key, not Groq. This is the second time this misread happened (2026-06-24, 2026-07-27)"
metadata: 
  node_type: memory
  type: feedback
  bead: "disk_magician-yua (ezgha deploy drift; sister: nothing specific)"
  originSessionId: d1c16e37-c03b-4f8d-bf7d-57d09005a2a4
  modified: 2026-07-27T10:15:42.251Z
---

Context: on 2026-07-27 the user reported `/history` and `/ms` had been broken for some time.
I had earlier (2026-07-26) closed a /learn session by reporting `mem0 unavailable: Qdrant
Connection refused at localhost` without investigating the cause. The blocker was a real
service problem, not a configuration mistake on the user's side, and crucially NOT a missing
API key. Persistence was missing for at least 18 days (`/Users/jleechan/.hermes/logs/qdrant.err.log`
contains 18 lines of "no usable Docker context after 60s, giving up" between 2026-06-28 and
2026-07-26).

FIX: 2026-07-27 03:00 the qdrant launchd job `ai.hermes.qdrant.plist` was rewritten to
invoke the native `qdrant` binary at `/Users/jleechan/.local/bin/qdrant` (v1.14.1, same
upstream as the docker image) directly, and:
- added `WorkingDirectory = /Users/jleechan/.local/share/qdrant/storage` so cwd-relative
  fallbacks (`./snapshots/tmp`, `./.qdrant_init` indicator) have a writable home;
- added absolute `storage_path` and `snapshots_path` keys in
  `/Users/jleechan/.local/share/qdrant/config/config.yaml`;
- retained `ProcessType: Background`, `RunAtLoad: true`;
- retired `start-qdrant-container.sh` (renamed to `*.bak.<timestamp>` for traceability).

A second, hidden defect fixed in the same session: the mem0 API release to 2.x
replaced the `user_id=` kwarg with `filters={'user_id': ...}` on
`m.search()` and `m.get_all()`. The three helpers — `~/.hermes/scripts/mem0_shared_client.py`,
`~/.hermes/.claude/hooks/mem0_recall.py`, `~/.hermes/scripts/mem0_dedup.py` — were all on
the old API and silently failing because `mem0_save.py` swallows exceptions with `pass # Never
block`. Fixed in place 2026-07-27:
- `~/.hermes/scripts/mem0_shared_client.py:346` (m.search)
- `~/.hermes/.claude/hooks/mem0_recall.py:93` (m.search)
- `~/.hermes/scripts/mem0_dedup.py:88` (m.get_all)

Why both belong in this one memory entry: the user observation "mem0 is always breaking"
is actually two distinct failures — a service-launch failure and an API-shape regression —
and they both surfaced in the same `/learn` capture. Future /learn captures on this topic
should treat them as one cluster, not two unrelated facts.

---

## Mandatory diagnosis recipe (run, in order, before declaring "mem0 unavailable")

Whenever `m = Memory.from_config(MEM0_CONFIG); m.search(...)` raises a
`Connection refused`, `Qdrant` exception, or any of these specifically
mem0 raise types — DO NOT report "mem0 unavailable" and stop. The first probe
must distinguish **service down** from **client-side breakage**:

1. **Can qdrant itself even be reached?**
   ```bash
   lsof -nP -iTCP:6333 -sTCP:LISTEN
   curl -sS -m 3 http://127.0.0.1:6333/healthz
   ```
   If both fail → the launchd job is the suspect, not config. Go to step 2.

2. **What is the launchd job doing?**
   ```bash
   # state, last exit code, what command
   launchctl print "gui/$(id -u)/ai.hermes.qdrant" | grep -E "state|runs|program|last exit"
   # recent stderr — look for the same error repeated 18+ times (the docker-wait pattern)
   tail -30 ~/Library/Logs/ai.hermes.qdrant.err.log
   ```
   The exact evidence this recipe looked for: `no usable Docker context after 60s, giving up`
   repeated = docker-dependent launcher can't find a context on this machine. The fix used here
   was to swap the launcher to the native `qdrant` binary + add `WorkingDirectory` +
   absolute `storage_path`/`snapshots_path`.

3. **If launchd says qdrant is running but it's not bound to 6333:**
   look for `Failed to create snapshots temp directory` or `Failed to create init file
   indicator: Read-only file system (os error 30)` in the qdrant stdout log. Both mean
   cwd-relative paths resolved to a read-only directory (default `ProcessType: Background`
   launchd jobs get `/var/empty` as cwd). Fix: pin `WorkingDirectory` in the plist AND pin
   `storage_path` / `snapshots_path` to absolute paths in qdrant config.

4. **If qdrant IS reachable and the helpers are raising:**
   `m.search()` and `m.get_all()` raised on mem0 2.x with the old `user_id=` kwarg.
   Use `filters={'user_id': ...}` instead. `m.add()` still accepts `user_id=`.

5. **If a Stop-hook-fire Qdrant-side delta can't be confirmed**, you may still be saving
   but the assumption that "mem0 unavailable" means "the embedder API key is missing" is
   almost always wrong on this machine. `mem0_config.py` switched to fastembed + Ollama
   on 2026-07-19; no API key is needed for either path. Probe the launchd job first.

## Anti-pattern: collapsing "service can't start" into "API key missing"

The wrong fix path is to set GROQ_API_KEY or OPENAI_API_KEY, or to comment out the hook
entirely. Both waste rounds and mask the real defect for the next session. The skill's
verification step exists precisely to prevent this — but only works if actually executed
**first**, not just sourced from the file. The 2026-06-24 incident had the same shape
(reported at the time in feedback_2026-06-24-verify-harness-status-before-reporting.md)
and the same root cause modulo which layer of the helper stack breaks.

**How to apply:** before any "/learn" capture that mentions mem0, qdrant, fastembed, or hooks,
run the four-step recipe above and grep for the canonical signatures:
`"no usable Docker context"`, `"Read-only file system"`,
`"Top-level entity parameters ... are not supported in search()"`. Any one of those IS the
answer; do not narrate beyond it.

**See also:**
- `feedback_2026-06-24-verify-harness-status-before-reporting.md` — earlier SKILL.md probe
  was stale for 2 months after the Ollama/Groq switch (rev-1cmaj).
- `disk_magician-yua` — `~/.local/libexec/ezgha/` has the same pattern: a hand-copied
  deploy with no installer. Would prevent this class of breakage if extended.
- The launcher swap itself: `git log -p ~/Library/LaunchAgents/ai.hermes.qdrant.plist`
  should show the post-fix ProgramArguments (`/Users/jleechan/.local/bin/qdrant` ...).
