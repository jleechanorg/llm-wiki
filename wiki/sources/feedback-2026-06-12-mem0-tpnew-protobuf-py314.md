---
title: "2026-06-12 Mem0 Tpnew Protobuf Py314"
type: source
tags: ["feedback", "hermes"]
date: 2026-06-12
source_file: raw/feedback_2026-06-12_mem0_tpnew_protobuf_py314.md
---

## Summary
Hermes mem0

## Key Claims
- Two stacked mem0 failures in prod Hermes (`~/.hermes_prod`, gateway `ai.hermes.prod` port 8642), 2026-06-12.
- Logger `plugins.memory.mem0` spammed `Mem0 sync failed: Metaclasses with custom tp_new are not supported` ~77×/500 log lines, every agent turn (also `mem0_search`).
- Why protobuf was pinned at 4.x: `google-cloud-firestore` requires `protobuf<5.0.0dev`; `mem0ai` requires `protobuf<7,>=5.29.6` — unsatisfiable together, resolver kept 4.25.9. **KEY: no protobuf<5 supports py3.14, so every `google-cloud-*` in this shared "junk-drawer" py3.14 env is ALREADY dead on 3.14 → upgrading protobuf regresses nothing currently working.**
- pip install --break-system-packages --upgrade "protobuf>=5.29.6,<7"   # 4.25.9 -> 6.33.6
- launchctl kickstart -k gui/$UID/ai.hermes.prod                         # NEVER `stop` (=bootout)
- Verified: gateway interpreter now `protobuf 6.33.6`; `from mem0 import Memory, MemoryClient` clears; new gateway pid loads protobuf 6.33.6; 0 tp_new lines post-restart; single-instance on :8642. Rollback: `pip install --break-system-packages "protobuf==4.25.9"`. `--break-system-packages` justified: protobuf was pip-installed (not brew), PEP-668 env; firestore's violated `<5` pin is moot (already dead on 3.14); reversible.

## Connections
- [[config-change-requires-restart]]
- [[hermes-gateway-bootout-outage-root-cause]]
