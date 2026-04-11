---
title: "PR #6104: fix(avatar): CR nits — constants consolidation, imports, storage error test"
type: source
tags: []
date: 2026-04-05
source_file: raw/prs-worldarchitect-ai/pr-6104.md
sources: []
last_updated: 2026-04-05
---

## Summary
- Add `AVATAR_EXTENSIONS` / `AVATAR_CONTENT_TYPE_BY_EXT` as single source of truth within `firestore_service.py`; remove all redundant local `allowed_extensions` sets and `content_type_map` dicts. (Note: `main.py` retains its own avatar constants for Flask upload routing — consolidating those is out of scope.)
- Replace bare `import firestore_service` in test methods with module-level `from mvp_site import firestore_service` (consistent canonical patch targets).
- Mock `_get_avatar_extension_for

## Metadata
- **PR**: #6104
- **Merged**: 2026-04-05
- **Author**: jleechan2015
- **Stats**: +116/-50 in 3 files
- **Labels**: none

## Connections
