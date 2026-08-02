---
title: Mem0QdrantDeployment
type: concept
tags: [mem0, qdrant, fastembed, ollama, launchd, deployment]
sources: [sources/feedback-2026-07-27-mem0-qdrant-diagnosis-recipe.md]
last_updated: 2026-07-27
---

The local self-hosted mem0 deployment on this machine: native qdrant (v1.14.1) at
`~/.local/bin/qdrant`, listening on `127.0.0.1:6333` (HTTP) and `127.0.0.1:6334` (gRPC),
launched by launchd job `ai.hermes.qdrant.plist` as a Background process under
`WorkingDirectory=/Users/jleechan/.local/share/qdrant/storage`. Embedder is
**fastembed** (BAAI/bge-base-en-v1.5, 768d, in-process — no Ollama, no API key). LLM
provider is **Ollama** (`llama3.2:3b` at http://localhost:11434). Groq and OpenAI were
removed in earlier fixes; nothing API-key-dependent remains.

## Mandatory 5-step diagnosis when mem0 is broken

Run, in order, before declaring "mem0 unavailable":

1. **lsof** `lsof -nP -iTCP:6333 -sTCP:LISTEN` — is qdrant bound?
2. **curl** `curl -sS -m 3 http://127.0.0.1:6333/healthz` — does it respond?
3. **launchctl** `launchctl print "gui/$(id -u)/ai.hermes.qdrant" | grep -E "state|runs|program|last exit"`
4. **log** `tail -30 ~/Library/Logs/ai.hermes.qdrant.err.log` and the matching `.log`
5. **grep** for canonical patterns: `"no usable Docker context"`, `"Read-only file system"`
   (qdrant panic), `"Top-level entity parameters ... are not supported in search()"` (mem0 2.0)

If step 1 or 2 fail and step 4 shows "no usable Docker context" → swap the launcher to
the native binary + WorkingDirectory. If step 1/2 are OK but the helper raises a
`ValueError` about top-level entity params → migrate the helper from `user_id=` to
`filters={'user_id': ...}`.

## Anti-pattern to avoid

Collapsing "service can't start" into "API key missing." Twice on this machine
(2026-06-24 and 2026-07-27) the failure was in the launcher/API shape layer, not in
embedder auth. Setting `GROQ_API_KEY` or commenting out the hook wastes hours and masks
the real defect.

## Cost: hours per failure

Each cycle of "OpenAI API key missing" → "switch to Ollama" → "still doesn't work" →
"actually it's the qdrant launchd job" has been 1-3 hours. The 5-step recipe runs in
under a minute end-to-end.

## See also

- [[Mem0HelperFiles]] — the 3 helpers that have to be migrated on every mem0 major bump
- [[QdrantLaunchdPlist]] — what the current plist looks like and why
- [[Mem0Server]] — collection name, host, port
- [[ProbeTheBlockerBeforeDeclaringBlocked]] — parent anti-pattern
