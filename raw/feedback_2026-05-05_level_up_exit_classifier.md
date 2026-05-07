---
name: LEVEL_UP_EXIT_CLASSIFIER vs classify_intent for modal exit
description: Use classify_level_up_exit_intent for level-up modal exit, not classify_intent
type: feedback
bead: none
---

## Context

PR #6799 code review identified ZFC violations in `_enforce_character_creation_modal_lock`:
- `world_logic.py:2024` had hardcoded natural-language phrase list for "finish level up" variants
- `intent_classifier.py:377` had generic anchors ("return to game") that could misclassify story input

## Technical Detail

Two classifier paths exist for level-up modal exit:

1. **`classify_intent(text)`** — General-purpose intent classification across all modes. For "finish level up" it returns `MODE_CHARACTER` with 0.0 confidence (the anchor phrases require context to match).

2. **`classify_level_up_exit_intent(text)`** — Dedicated level-up exit classifier using `LEVEL_UP_EXIT_ANCHOR_PHRASES`. Returns `(matched: bool, score: float)` where `matched=True` when `score >= 0.85`. "finish level up" scores 1.0 (perfect match).

The fix correctly uses `classify_level_up_exit_intent` in world_logic.py modal lock:

```python
_is_exit_intent, _intent_conf = classify_level_up_exit_intent(_cleaned_input)
if _is_exit_intent:
    selected_choice_id = "finish_level_up_return_to_game"
    user_selected_exit = True
```

**NOT `classify_intent`** — that path is for general routing, not modal-specific exit detection.

## Verification

App log line 14180 confirms:
```
🧠 LEVEL_UP_EXIT_CLASSIFIER: Input='finish level up' -> matched=True (score=1.000)
🔒 MODAL_LOCK: Level-up exit classifier matched 'finish level up' (1.00) → finish_level_up_return_to_game
🚪 MODAL_LOCK: Server enforced level-up exit via finish_level_up_return_to_game - modal lock released
```

Test evidence bundle: `/tmp/worldarchitect.ai/finish-level-up-merge/level_up_finish_return_bug_red/latest/`
- streaming_evidence.json: 146 chunks
- story entries show Lvl 1 → Lvl 2 transition via CHOICE path

## References

- PR #6799: https://github.com/jleechanorg/worldarchitect.ai/pull/6799
- `mvp_site/intent_classifier.py:1153` — `classify_level_up_exit_intent` function
- `mvp_site/world_logic.py:2241` — modal lock usage
- `mvp_site/intent_classifier.py:1050-1111` — `predict_level_up_exit` implementation

## Pattern

When adding modal-specific exit detection, use the dedicated modal-exit classifier (`classify_level_up_exit_intent`) not the general intent classifier (`classify_intent`). The dedicated classifier has anchors specific to that modal's completion phrases.