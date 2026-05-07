---
description: Use classify_level_up_exit_intent for level-up modal exit detection
type: concept
---

# Level-Up Exit Classifier

The `classify_level_up_exit_intent()` function is the dedicated classifier for detecting level-up modal exit intent. It uses `LEVEL_UP_EXIT_ANCHOR_PHRASES` with a 0.85 threshold.

## Key Distinction

| Function | Purpose | Returns |
|----------|---------|---------|
| `classify_intent(text)` | General-purpose intent across all modes | `(mode: str, confidence: float)` — returns `MODE_CHARACTER` + 0.0 for "finish level up" |
| `classify_level_up_exit_intent(text)` | Level-up modal exit detection | `(matched: bool, score: float)` — returns `True` + 1.0 for "finish level up" |

## Usage in Modal Lock

```python
# mvp_site/world_logic.py:2241
_is_exit_intent, _intent_conf = classify_level_up_exit_intent(_cleaned_input)
if _is_exit_intent:
    selected_choice_id = "finish_level_up_return_to_game"
    user_selected_exit = True
```

## Evidence

App log confirms:
```
LEVEL_UP_EXIT_CLASSIFIER: Input='finish level up' -> matched=True (score=1.000)
MODAL_LOCK: Level-up exit classifier matched 'finish level up' (1.00) → finish_level_up_return_to_game
```

## Related

- [[classifier-architecture]] — general intent classification system
- [[level-up-modal-flow]] — level-up modal lifecycle
- [[zero-framework-cognition]] — ZFC compliance for intent detection