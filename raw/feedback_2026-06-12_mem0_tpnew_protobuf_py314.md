---
name: mem0-tpnew-protobuf-py314-and-never-persisted
description: "Hermes mem0 'Metaclasses with custom tp_new are not supported' spam = protobuf 4.x can't import under py3.14; fix is upgrade protobuf in the gateway's py3.14 env. Separately, mem0 has never actually persisted (cloud MemoryClient w/ placeholder key + dead self-hosted Qdrant)."
metadata:
  node_type: memory
  type: feedback
  originSessionId: c594d4f0-a942-4271-85f6-5407a3c1d6e6
---

Two stacked mem0 failures in prod Hermes (`~/.hermes_prod`, gateway `ai.hermes.prod` port 8642), 2026-06-12.

## Layer 1 (FIXED + DEPLOYED) — `Metaclasses with custom tp_new are not supported`
Logger `plugins.memory.mem0` spammed `Mem0 sync failed: Metaclasses with custom tp_new are not supported` ~77×/500 log lines, every agent turn (also `mem0_search`).

**This is NOT a mem0 bug.** It's a compiled C-extension import crash under **Python 3.14**. The prod gateway runs `/opt/homebrew/opt/python@3.14` (pinned by the shebang of the pip-installed console script `/opt/homebrew/bin/hermes`; site-packages `/opt/homebrew/lib/python3.14/site-packages/`). `import mem0` → `qdrant_client` → `qdrant_client/grpc/points_pb2.py` → `google._upb._message` (protobuf C ext). The env had **protobuf 4.25.9**, which has no py3.14-compatible build → tp_new crash at import, before any mem0 logic runs.

Why protobuf was pinned at 4.x: `google-cloud-firestore` requires `protobuf<5.0.0dev`; `mem0ai` requires `protobuf<7,>=5.29.6` — unsatisfiable together, resolver kept 4.25.9. **KEY: no protobuf<5 supports py3.14, so every `google-cloud-*` in this shared "junk-drawer" py3.14 env is ALREADY dead on 3.14 → upgrading protobuf regresses nothing currently working.**

**Fix (applied + live):**
```
pip install --break-system-packages --upgrade "protobuf>=5.29.6,<7"   # 4.25.9 -> 6.33.6
launchctl kickstart -k gui/$UID/ai.hermes.prod                         # NEVER `stop` (=bootout)
```
Verified: gateway interpreter now `protobuf 6.33.6`; `from mem0 import Memory, MemoryClient` clears; new gateway pid loads protobuf 6.33.6; 0 tp_new lines post-restart; single-instance on :8642. Rollback: `pip install --break-system-packages "protobuf==4.25.9"`. `--break-system-packages` justified: protobuf was pip-installed (not brew), PEP-668 env; firestore's violated `<5` pin is moot (already dead on 3.14); reversible.

## Layer 2 (FIXED — self-hosted, deployed + PR #28 MERGED) — mem0 now actually persists
**PR #28 MERGED 2026-06-13 08:08Z** into jleechanorg/hermes-agent main (merge commit `bbba9970e`), auto-merged by `skeptic-cron` (`app/github-actions`) once 7-green held on head `9da1a093b` — never `gh pr merge` by hand. Two follow-up review fixes landed before merge: forward configured key as `X-API-Key` (codex P2) and forward `infer` in `/memories` payload (cursor Medium); both no-ops for the current unauthenticated `mem0_server.py` (Pydantic `extra=ignore` drops `infer`; FastAPI ignores extra headers), so safe on any gateway restart.

**User chose self-hosted (local, no cloud).** Resolution:
- Qdrant container `hermes-qdrant` (qdrant/qdrant:latest, 127.0.0.1:6333-6334) brought up via Docker Desktop; Ollama :11434 + `mem0_server.py` :8000 already running.
- Added `_LocalMem0Client` to `plugins/memory/mem0/__init__.py` — urllib adapter mapping the plugin's `search`/`add`/`get_all` onto `mem0_server.py`'s REST contract (`POST /search`, `POST /memories`, `GET /memories`). `_get_client()` branches on configured `host` (from `mem0.json`, already set to `http://localhost:8000`); `is_available()` = `api_key OR host`. All 5 call sites untouched. +82/−1, one file.
- Editable install (`pip install -e` → `/Users/jleechan/projects_other/hermes-agent`) means the live prod gateway loads this working tree; edit went live on `launchctl kickstart -k gui/$UID/ai.hermes.prod`.
- **Verified live**: real Slack turn persisted "Preferred production deploy window is Tuesday at 3pm Pacific" to Qdrant `hermes_mem0` (newest point, `user=U09GH5BR3QU agent=hermes`); 0 `Invalid API key`, 0 `tp_new`, single instance on :8642. NOTE: gateway scopes memory by the **real Slack user id** (e.g. `U09GH5BR3QU`), not `mem0.json` `user_id` — query that scope when verifying.
- PR: https://github.com/jleechanorg/hermes-agent/pull/28 (base jleechanorg/main). `origin` here = NousResearch (upstream, NEVER PR there); fork remote = `jleechanorg`. The live editable checkout keeps the edit UNCOMMITTED on stale branch `fix/slack-thread-ts-injected-reply-leak` so the gateway keeps running the fix until PR #28 merges + `~/.hermes` pulls.
- Gateway port here is **8642** (not the 8643 in some CLAUDE.md tables).

### Original Layer-2 diagnosis (kept for provenance) — mem0 had never actually persisted
Log history shows **1111× "Invalid API key"** alongside the tp_new spam → mem0 was failing *before* py3.14 too. Root cause is an architecture/credential mismatch:
- Plugin `_get_client()` calls `MemoryClient(api_key=self._api_key)` — the **mem0 cloud platform** SDK (`https://api.mem0.ai`, `/v1/...` routes). `api_key` comes from `~/.hermes_prod/mem0.json` = `"local-dev"` (placeholder) → cloud returns **"Invalid API key"**. The plugin **ignores** `mem0.json`'s `host: http://localhost:8000` (never passes host to MemoryClient) and has **no self-hosted `Memory` path**.
- A custom self-hosted `~/.hermes_prod/mem0_server.py` (pid running) listens on :8000 with **custom routes** (`POST /memories`, `POST /search`) backed by `from mem0 import Memory` (Qdrant+Ollama) — it does **NOT** speak the platform `/v1/...` contract, so pointing the plugin at it → "Not Found".
- That self-hosted stack is **fully dead anyway**: **Qdrant :6333 is down** (conn refused) → `mem0_server.py`'s own `POST /memories` hangs to 000. Ollama :11434 is up.

Net: after the protobuf fix mem0 stops crash-spamming and degrades to the *prior* non-fatal "Invalid API key" warning (mem0 sync failures are `logger.warning`, degraded memory, NOT a gateway outage). To make mem0 actually persist, a decision is required:
- **A (cloud)** — put a real `MEM0_API_KEY` in `mem0.json`/env; no code change. External dep + cost + memory leaves machine.
- **B (self-hosted)** — bring up Qdrant :6333 (e.g. docker) + Ollama, AND change the plugin to use `Memory.from_config()` (a PR — plugin has no self-hosted path today). `mem0_server.py` would be redundant or need a route-matching shim.
- **C (accept/disable)** — leave as best-effort warnings, or disable the mem0 plugin to kill log noise since it never persisted.

Plugin code (`plugins.memory.mem0`) is bundled inside the `hermes` pip package, not under `~/.hermes_prod/plugins/` — any Layer-2 code fix is a hermes-package change, governed by worktree→PR. Related: [[config-change-requires-restart]], [[hermes-gateway-bootout-outage-root-cause]].
