---
name: shared-user-settings-conflict-pattern
description: _shared_user_settings in llm_service.py means PRs adding duplicate get_user_settings() will conflict on merge from main
type: feedback
bead: none
---

When a PR on the `feat/rag-mode-*` family adds a new `get_user_settings(user_id)` call in `_continue_story()` (for RAG mode resolution or similar), it will conflict with origin/main if main has the jleechan-1hy7 latency fix that pre-fetches settings into `_shared_user_settings` at line ~6362.

**Rule**: Always use `_shared_user_settings` (already fetched, already guarded by `LLMRequestError`) instead of calling `get_user_settings()` again for RAG mode or any other per-user decision in `_continue_story()`.

**Why:** The shared variable was introduced by PR #7818 (`081bf8aea9`) to eliminate a 20-100ms duplicate Firestore roundtrip on the hot streaming path before the first token is served. A second `get_user_settings()` call after `_shared_user_settings` already exists is a latency regression.

**How to apply:** In `mvp_site/llm_service.py` inside `_continue_story()`, check for `_shared_user_settings` at line ~6362 before adding any new per-user settings lookup. If it's there, pass it directly.

**Conflict resolution (2026-06-23):** PR #7802 had exactly this conflict at line 6387. Merged from main using `git merge origin/main --no-commit --no-ff` to isolate, then resolved by taking main's `rag_mode.get_rag_mode(_shared_user_settings)` over PR's duplicate call.

**References:**
- Conflict file: `mvp_site/llm_service.py:6387`
- PR introducing shared var: #7818, commit `081bf8aea9`
- PR with conflict: #7802, merge commit `1d9e9608c2`
