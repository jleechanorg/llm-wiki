# AsyncWarmupMechanismProof

## Summary

Pattern for proving that an async boot-warmup mechanism (e.g. FastEmbed classifier via `warm_in_background()`) is truly non-blocking and functional.

## The _init_event trap

`LocalIntentClassifier._init_event` is initialized as `threading.Event()` then immediately `.set()` in `__init__` (line 739 of `mvp_site/intent_classifier.py`). Calling `_init_event.wait()` BEFORE `initialize_async()` starts returns instantly (~13ms), making a proof script falsely succeed while the model hasn't loaded.

**Wrong:**
```python
timed_out = not instance._init_event.wait(timeout=30)
# Returns immediately because _init_event starts SET
```

**Right:**
```python
while time.time() - t_start < MAX_WAIT:
    if instance.ready:
        break
    time.sleep(0.05)
```

## /health 200 is insufficient

A `GET /health → {"status": "healthy"}` response proves the server is up. The health endpoint does NOT expose `classifier.ready`. Evidence that only shows a health 200 does not prove async warmup worked.

## Required evidence for async warmup claims

1. `warm_in_background()` call duration < 100ms (non-blocking)
2. `instance.ready == False` at port-bind time (classifier still loading)
3. Server logs: `🧠 CLASSIFIER: Ready for inference` after port-bind time
4. Real `predict()` call returns non-zero score (not `('character', 0.0)` fallback)

## Proven results (PR #7863, SHA 234bd24c7fa415b87bc58339e36cc8a71edfe08c)

- `warm_in_background()`: **0.16ms** (non-blocking ✓)
- Port-bind sim: T+130ms, `ready=False`
- Classifier ready: T+1117ms (987ms after port-bind, in background ✓)
- Real routing: combat 0.871, dialog 0.888, info 0.827, character 0.903 ✓

Proof gist: https://gist.github.com/jleechan2015/578e0b70bc8d733a7e8ecd89f9ef6850

## Related

- [[EvidenceBasedVerification]]
- [[EvidenceTheater]]
- [[DaemonThreadCleanup]]
