# REV: Streaming cache merge payload duplicates helper logic

## Status: done
## Priority: low
## Type: refactor

## Summary

`_build_streaming_merged_payload` (streaming path) duplicated the exact same
dictionary-merge-then-concatenate-story_history logic as `_merge_explicit_cache_payload`
(non-streaming path). Both were nested functions in different parent functions,
preventing code sharing. Divergence risk if merge logic changes in one but not the other.

## Fix

Extracted shared logic into module-level `_merge_cache_payloads()` helper.
Non-streaming path aliases it as `_merge_explicit_cache_payload = _merge_cache_payloads`.
Streaming path calls it directly in `_build_streaming_merged_payload`.

## Files Changed

- `mvp_site/llm_service.py`
