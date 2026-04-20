# ZFC Level-Up Architecture: Model Computes, Backend Formats

**Date**: 2026-04-19
**Status**: Design draft for https://github.com/jleechanorg/worldarchitect.ai/pull/6404 and follow-up cleanup
**Supersedes**: Backend-centralization-only level-up plan for the level-up decision
**Builds on**: `/Users/jleechan/roadmap/level-up-engine-single-responsibility-design-2026-04-14.md`
**Implementation branch**: `feat/zfc-level-up-model-computes`

## Executive Summary

This design replaces backend-owned level-up judgment with a ZFC-compliant contract:
the model computes level-up facts, the backend validates and formats explicit fields,
and the UI renders only server-provided payloads.

The key contract change is that XP state must be expressed as two unambiguous totals:

- `previous_turn_exp`: total character XP before the current user turn.
- `current_turn_exp`: total character XP after the current user turn.

The backend may compute deterministic display values from those explicit totals, such
as `xp_gained = current_turn_exp - previous_turn_exp` and
`progress_percent = current_turn_exp / xp_to_next_level`. The backend must not infer
that a level-up happened from threshold crossings on the new model-owned path.

Current state is transitional, not complete.
https://github.com/jleechanorg/worldarchitect.ai/pull/6404 adds the
prompt/schema/parser field and the first formatter path, but legacy backend recovery
still exists. The next work must intentionally delete no-op or duplicate legacy code
first, then run an MVP real-model compliance probe to measure whether the LLM reliably
emits the new fields before any broad rewrite.

## Table of Contents

1. [Problem](#problem)
2. [Background: Current Request-to-UI Callstack](#background-current-request-to-ui-callstack)
3. [Current State and Gaps vs. Original Centralization](#current-state-and-gaps-vs-original-centralization)
4. [Traversed File Responsibility Summary](#traversed-file-responsibility-summary)
5. [Core Tenets](#core-tenets)
6. [North Star Architecture](#north-star-architecture)
7. [Canonical Model Output](#canonical-model-output)
8. [Backend Contract](#backend-contract)
9. [Fail-Closed Rules](#fail-closed-rules)
10. [Single Root and Call Graph](#single-root-and-call-graph)
11. [File Responsibility Details](#file-responsibility-details)
12. [Implementation Plan](#implementation-plan)
13. [Tests Required](#tests-required)
14. [Grep Gates](#grep-gates)
15. [Design Invariants](#design-invariants)
16. [Current PR Scope](#current-pr-scope)
17. [Follow-Up Queue](#follow-up-queue)

## Problem

The 2026-04-14 design correctly centralized scattered level-up and rewards logic, but
it still treated the server as the place that decides whether a player should level
up. That violates the current Zero-Framework Cognition rule for semantic judgment:
application code must not infer intent, classify narrative state, or make gameplay
judgment from textual or semi-structured cues when the model can be given the context
and asked to decide explicitly.

The current codebase also still has two classes of drift risk:

1. **Decision drift**: prompts, parser schema, backend formatter, and UI can disagree
   about what `level_up_signal`, `rewards_box`, or `planning_block` means.
2. **Responsibility drift**: files can regain level-up logic because the old design
   said "centralize in rewards_engine" but did not make each file's ZFC-safe boundary
   explicit enough.

The desired architecture is therefore not just "centralize level-up code." It is:

```text
Model owns semantic level-up computation.
Backend owns deterministic validation, formatting, persistence, and delivery.
UI owns rendering only.
```

## Background: Current Request-to-UI Callstack

This is the current production streaming path for a normal user action. It is the path
that the ZFC rewrite must simplify, not a finished target state.

| Step | File | Method / Call | What Happens Today |
|------|------|---------------|--------------------|
| 1 | `mvp_site/frontend_v1/app.js` | `handleStreamingInteraction(userInput, mode)` | Creates the in-progress story entry, wires stream handlers, and calls `streamingClient.sendMessage(userInput, mode)`. |
| 2 | `mvp_site/frontend_v1/js/streaming.js` | `StreamingClient.sendMessage(userInput, mode)` | Builds auth headers and POSTs `{input, mode}` to `/api/campaigns/<campaign_id>/interaction/stream`. |
| 3 | `mvp_site/main.py` | `handle_interaction_stream(user_id, campaign_id, user_email)` | Validates JSON, extracts `user_input`, checks mode and rate limits, verifies campaign existence, and starts the SSE generator. |
| 4 | `mvp_site/main.py` | `generate()` inner generator | Iterates `stream_story_with_game_state(...)`, captures SSE events, and yields `event.to_sse()` to the browser. |
| 5 | `mvp_site/llm_parser.py` | `stream_story_with_game_state(user_id, campaign_id, user_input, mode)` | Loads campaign/story context, loads `GameState`, loads user settings, and prepares the streaming game-state flow. |
| 5a | `mvp_site/firestore_service.py` | `get_campaign_game_state(user_id, campaign_id)` | Reads the persisted game-state document that will be converted into the in-memory state object. |
| 5b | `mvp_site/game_state.py` | `GameState.from_dict(game_state_obj)` | Converts persisted state into the object passed through routing, prompt preparation, projection, and persistence. This was missing from earlier callstack drafts. |
| 6 | `mvp_site/world_logic.py` | `_maybe_trigger_level_up_modal(user_input, story_context, current_game_state)` | Current transitional pre-routing shim. It is called on user request because the explicit `level_up_now` modal click must set `level_up_in_progress` / `level_up_pending` before agent selection. Do not delete until that click is handled by another pre-routing boundary. |
| 7 | `mvp_site/rewards_engine.py` | `project_level_up_ui(current_game_state.to_dict())` | Current transitional polling/recovery projection from game state before the model responds. It is not the ZFC target, but it protects pre-modal badge/metadata flows today. The direct streaming call is duplicated with `_build_early_metadata_payload(...)` and is a Stage 0 cleanup candidate; the API itself is not safe to delete yet. |
| 8 | `mvp_site/llm_parser.py` | `_build_early_metadata_payload(current_game_state)` | Builds pre-response metadata and attaches projected `rewards_box` / `planning_block` when present. |
| 9 | `mvp_site/llm_service.py` | `continue_story_streaming(...)` | Starts the model request path using the same preparation machinery as non-streaming. |
| 10 | `mvp_site/llm_service.py` | `_prepare_story_continuation(...)` | Selects agent/provider/model, builds system instructions, story context, game state, and `LLMRequest`. |
| 10a | `mvp_site/game_state.py` | `GameState.to_dict()` / `GameState.validate_checkpoint_consistency(...)` | Serializes deterministic state for prompt/request construction and performs mechanical consistency checks. These calls are in the request path but must not compute level-up semantics. |
| 11 | `mvp_site/llm_service.py` / `mvp_site/llm_request.py` | `prepared.gemini_request.to_json()` / `LLMRequest.to_json()` | The variable name is legacy. The object is the provider-neutral `LLMRequest` payload used by Gemini, OpenRouter, and OpenClaw paths. Rename toward `prepared.llm_request` when touching this area. |
| 12 | `mvp_site/llm_service.py` | `_calculate_prompt_and_system_tokens(...)` / `_get_safe_output_token_limit(...)` | Computes deterministic transport limits. No gameplay judgment belongs here. |
| 13 | `mvp_site/llm_service.py` | `gemini_provider.generate_content_stream_sync(...)`, `openclaw_provider.generate_content_stream_sync(...)`, or `openrouter_provider.generate_content_stream_sync(...)` | Sends the LLM request and receives streaming chunks. This is where the model must compute `level_up_signal`. |
| 14 | `mvp_site/llm_service.py` | `_parse_streamed_response(full_narrative)` | Parses the accumulated LLM response into narrative text plus structured response. |
| 15 | `mvp_site/narrative_response_schema.py` | `NarrativeResponse` parsing / serialization | Preserves `level_up_signal` as model output. It must not decide whether the signal is semantically correct. |
| 16 | `mvp_site/llm_service.py` | `yield StreamEvent(type="done", payload={...})` | Sends `structured_response`, narrative text, state updates, model/provider metadata, and execution trace back to `llm_parser.py`. |
| 17 | `mvp_site/llm_parser.py` | Done-event handling inside `stream_story_with_game_state(...)` | Must persist before yielding final `done` because the browser may close after receiving it. |
| 18 | `mvp_site/world_logic.py` | `_enforce_character_creation_modal_lock(...)` | Applies modal lock state transitions. This should remain modal coordination only. |
| 19 | `mvp_site/rewards_engine.py` | `canonicalize_rewards(structured_fields, updated_state_dict, pre_response_state_dict)` | Target single public backend convergence point. On the ZFC path it must prefer explicit `level_up_signal` and only format/validate. Projection callers should migrate toward `canonicalize_rewards({}, game_state_dict)` instead of a second public API. |
| 20 | `mvp_site/rewards_engine.py` | `_canonicalize_core(...)` | Private implementation detail. Current implementation still contains legacy fallback branches. Stage 0 must remove no-op/duplicate branches before the rewrite expands. |
| 21 | `mvp_site/rewards_engine.py` | `format_model_level_up_signal(level_up_signal)` | ZFC-owned formatter detail. It should become private (`_format_model_level_up_signal`) once `canonicalize_rewards(...)` is the sole public entrypoint. It formats explicit model fields into `rewards_box` and `planning_block`, fail-closing malformed true level-up signals. |
| 22 | `mvp_site/rewards_engine.py` | `resolve_level_up_signal(...)` | Legacy helper still reachable through fallback/projection. Rename/quarantine as legacy, then delete after MVP evidence. New model-owned responses must not call it. |
| 23 | `mvp_site/world_logic.py` | `campaign_upgrade.normalize_planning_block_choices(...)` | Normalizes already-computed choice payload shape. It must not synthesize semantic level-up choices. |
| 24 | `mvp_site/world_logic.py` | `_inject_modal_finish_choice_if_needed(...)` | Adds modal finish affordance when modal state requires it. It must preserve model/server-computed payloads. |
| 25 | `mvp_site/world_logic.py` | `_increment_turn_counter(...)` / `_maybe_update_living_world_tracking(...)` | Updates turn/living-world bookkeeping independent of level-up semantics. |
| 26 | `mvp_site/firestore_service.py` | `update_campaign_game_state(...)` | Persists updated game state. It must receive already-decided fields. |
| 27 | `mvp_site/structured_fields_utils.py` | `_enrich_streaming_structured_fields(...)` calls field extraction helpers indirectly through parsed structured data | Streaming persistence enriches structured fields for story storage; it must not reinterpret level-up meaning. |
| 28 | `mvp_site/firestore_service.py` | `add_story_entry(..., "user", ...)` and `add_story_entry(..., "gemini", ..., structured_fields=...)` | Persists the user action and model response with canonical structured fields. |
| 29 | `mvp_site/llm_parser.py` | `event.payload["structured_response"] = gemini_structured` | Finalizes the canonical response payload that the frontend will receive. |
| 30 | `mvp_site/main.py` | `yield event.to_sse()` | Streams final `done` SSE event to the browser. |
| 31 | `mvp_site/frontend_v1/js/streaming.js` | `_processSSEMessage(...)` | Dispatches `chunk`, `metadata`, `done`, `warning`, and `error` events to callbacks. |
| 32 | `mvp_site/frontend_v1/app.js` | `streamingClient.onMetadata(payload)` | Renders early server-provided `rewards_box` and `planning_block` via existing structured-field rendering. |
| 33 | `mvp_site/frontend_v1/app.js` | `streamingClient.onComplete(payload)` | Calls `renderStoryEntryElement(..., fullData)` with `payload.structured_response`. |
| 34 | `mvp_site/frontend_v1/app.js` | `renderStoryEntryElement(...)` / `generateStructuredFieldsPreNarrative(...)` | User sees the final story entry, XP/rewards UI, and level-up controls if and only if the server sent them. |

Target-state simplification:

```text
user input
  -> frontend streaming client
  -> Flask streaming endpoint
  -> llm_parser loads context and GameState.from_dict()
  -> llm_service prepares request
  -> LLM computes level_up_signal with previous_turn_exp/current_turn_exp
  -> schema/parser preserves signal
  -> rewards_engine.canonicalize_rewards() formats explicit fields
  -> world_logic wraps modal affordances only
  -> Firestore persists canonical structured fields
  -> SSE done payload returns canonical structured_response
  -> frontend renders server-provided UI
```

## Design Q&A Decisions

These are decisions from the 2026-04-19 review comments on the callstack table.

| Question | Decision | Follow-Up |
|----------|----------|-----------|
| Why is `_maybe_trigger_level_up_modal(...)` called on user request? | Because the user request can be the explicit `level_up_now` modal click. That click must set modal state before `llm_service` selects an agent, otherwise the request can stay on the prior mode instead of routing to `LevelUpAgent`. | Keep it for now. Rename/narrow it later as a pre-routing modal-click shim, or move the same responsibility to a cleaner pre-agent-selection boundary. |
| Can `_maybe_trigger_level_up_modal(...)` be deleted? | No, not safely today. Deleting it risks losing streaming modal-lock routing for `level_up_now`. | Delete only after another path proves the explicit modal click sets level-up modal state before agent selection. |
| Why call `project_level_up_ui(current_game_state.to_dict())` before the model responds? | It is a transitional pre-response projection for polling/early metadata/pre-modal badge flows. It computes UI from existing state before model output exists. | Keep the API until the ZFC MVP proves model-owned `level_up_signal` coverage. Stage 0 can remove the duplicate direct streaming call if `_build_early_metadata_payload(...)` already computes the same projection. |
| Can `project_level_up_ui(...)` be deleted? | Not as a first cleanup. Tests and pre-modal UX still rely on it. | Migrate callers toward `canonicalize_rewards({}, game_state_dict)`, then quarantine/delete the wrapper after evidence. |
| Can `prepared.gemini_request.to_json()` handle non-Gemini requests? | Yes in practice. `gemini_request` is a legacy variable name for the generic `LLMRequest`; the serialized payload is used by Gemini, OpenRouter, and OpenClaw paths. | Rename to `prepared.llm_request` when touching this code. Keep provider-specific transport in provider adapters. |
| Can rows 19-22 become one rewards-engine call? | Yes. The desired public API is one call: `canonicalize_rewards(...)`. `_canonicalize_core(...)`, `format_model_level_up_signal(...)`, and `resolve_level_up_signal(...)` should not remain separate public concepts. | Make formatter helpers private. Rename/quarantine legacy resolver. Replace projection wrappers with `canonicalize_rewards({}, state)` after tests are rewritten. |
| Is `game_state.py` in the callstack? | Yes. `GameState.from_dict(...)` and `GameState.to_dict()` are in the live request path and must be explicit in this design. | Treat `game_state.py` as state serialization/mechanical validation only, not model-output interpretation. |

## Current State and Gaps vs. Original Centralization

The original 2026-04-14 design got the codebase closer to a single backend root, but
it centralized too much semantic authority in Python. The current PR is a partial
pivot: it adds model-owned `level_up_signal`, but it still carries legacy inference so
existing flows do not break before evidence exists.

| Area | Current State | Gap vs. Original Centralization | ZFC Target |
|------|---------------|----------------------------------|------------|
| Prompt contract | https://github.com/jleechanorg/worldarchitect.ai/pull/6404 asks the model to emit `level_up_signal`, but field naming still needs to move from `xp_earned` / `xp_total` to `previous_turn_exp` / `current_turn_exp`. | Original design did not require the model to own the decision. | Prompt makes model output the complete level-up fact set. |
| Schema/parser | `level_up_signal` is preserved through structured response parsing. | Centralization is present, but compliance is only as good as model output. | Parser is a lossless transport boundary. |
| Formatter | `format_model_level_up_signal()` exists and is preferred when a signal is present. | Legacy fallback still shares the file, so accidental drift remains possible and the formatter looks like a second public API. | `canonicalize_rewards()` is the public API; formatter helpers are private and handle explicit signal only. |
| Projection | `project_level_up_ui()` still projects UI from game state before the model responds. | This violates the clean ZFC north star but was kept for compatibility. | Migrate projection semantics behind `canonicalize_rewards({}, state)`, then delete the wrapper after MVP shows model emits compliant signals. |
| Inference | `resolve_level_up_signal()` still exists for fallback/projection, with duplicate resolver concepts in `world_logic.py` and `game_state.py`. | Original centralization tolerated centralized backend inference. | No backend semantic inference on model-owned path; remaining legacy resolver calls are named and isolated. |
| Streaming/non-streaming parity | Streaming uses `llm_parser.py` persistence; non-streaming uses `world_logic.process_action_unified`. | The single-root invariant is not fully enforced across transports. | Both transports call the same signal formatter and persistence boundary. |
| UI | Frontend mostly renders server-provided structured fields. | It still has streaming partial JSON heuristics for display, unrelated to level-up decision. | UI never derives level-up availability. |
| Evidence | Unit tests exist for the formatter path. | Real model compliance is not yet measured. | MVP evidence quantifies valid/invalid model signal rates before deletion. |

## Traversed File Responsibility Summary

| File | Responsibility in This Flow | Owns | Must Not Own |
|------|-----------------------------|------|--------------|
| `mvp_site/frontend_v1/app.js` | User interaction orchestration and final story rendering. | DOM state, stream callbacks, structured-field rendering entrypoint. | XP math, level-up detection, semantic coercion. |
| `mvp_site/frontend_v1/js/streaming.js` | SSE transport client. | POST body, auth headers, SSE parsing, callback dispatch. | Gameplay meaning or level-up availability. |
| `mvp_site/main.py` | HTTP/SSE route boundary. | Request validation, auth/rate-limit checks, response streaming. | Level-up formatting or inference. |
| `mvp_site/llm_parser.py` | Streaming orchestration and persistence. | Context loading, `GameState` construction, model stream orchestration, canonical formatter call, Firestore write ordering. | Duplicate rewards formatting or threshold detection. |
| `mvp_site/llm_service.py` | LLM request construction and provider streaming. | Agent/model/provider selection, provider-neutral `LLMRequest`, prompt payload, streaming chunks, structured response parse handoff. | Backend gameplay judgment from response text. |
| `mvp_site/narrative_response_schema.py` | Structured response schema. | Accepting and preserving `level_up_signal`. | Validating D&D semantics or mutating state. |
| `mvp_site/structured_fields_utils.py` | Structured field extraction. | Copying non-empty structured fields forward. | Alias normalization, UI payload construction, semantic validation. |
| `mvp_site/rewards_engine.py` | Deterministic formatter boundary. | Explicit signal validation, `rewards_box`, `planning_block`, atomicity. | Model calls, Firestore writes, text interpretation, new-path threshold inference. |
| `mvp_site/world_logic.py` | Modal/story state wrapper. | Modal locks, finish choice injection, turn/living-world bookkeeping. | Recomputing level-up choices or XP progress. |
| `mvp_site/game_state.py` | Persistent state shape and deterministic primitives. | `GameState.from_dict(...)`, `GameState.to_dict()`, checkpoint consistency, and legacy mechanical helpers. | Model-output interpretation or new-path level-up decisions. |
| `mvp_site/firestore_service.py` | Persistence adapter. | Campaign/game-state/story-entry reads and writes. | Business decisions. |
| `mvp_site/prompts/*.md` | Model contract. | Telling the LLM exactly which structured facts to compute. | Conflicting backend-owned algorithms. |
| `roadmap/zfc-level-up-model-computes-2026-04-19.md` | Architecture contract and migration control. | North star, file boundaries, deletion plan, evidence expectations. | Stale claims that transitional code is already deleted. |

## Core Tenets

### 1. ZFC Boundary

The model decides:

- Whether XP was earned.
- The previous XP total for the turn.
- The current XP total after the turn.
- Whether a level-up is available.
- The target level.
- Which level-up choices or benefits are relevant to present.
- Whether the response should include only XP progress or a full level-up prompt.

The backend must not decide those semantic facts on the new model-owned path.

### 2. Centralization Boundary

There is one canonical backend formatting path for model-owned level-up output:

```text
level_up_signal -> rewards_engine.format_model_level_up_signal()
                -> canonicalize_rewards()
                -> world_logic modal wrapper
                -> response/persistence
                -> app.js render
```

No other file may independently interpret level-up signal semantics, recalculate
threshold crossings, or synthesize competing level-up choices.

### 3. Single Responsibility Per File

Every file gets one job. If a file starts doing a second job, move that logic to the
file that owns it.

| File | One Job | Must Not Do |
|------|---------|-------------|
| `mvp_site/prompts/*.md` | Tell the model exactly what to compute and emit | Hide backend assumptions, mention conflicting direct level mutation paths |
| `mvp_site/narrative_response_schema.py` | Accept the structured model output shape | Decide level-up, compute thresholds, mutate game state |
| `mvp_site/structured_fields_utils.py` | Extract non-empty structured fields | Validate gameplay meaning, format UI payloads |
| `mvp_site/rewards_engine.py` | Deterministically format explicit reward/level-up signals and preserve legacy fallback during migration | Make semantic level-up decisions on the `level_up_signal` path, call the model, persist state |
| `mvp_site/game_state.py` | Store state and provide deterministic mechanical primitives for legacy paths | Interpret model text or own new-path level-up decisions |
| `mvp_site/world_logic.py` | Wrap precomputed payloads with modal/story response semantics | Recompute rewards, detect thresholds, build level-up choices independently |
| `mvp_site/agents.py` | Route to the correct agent/mode | Inspect XP/level-up fields for semantic decisions beyond delegated helpers |
| `mvp_site/llm_parser.py` | Parse model output, call the pipeline once, persist/deliver results | Duplicate rewards formatting or modal logic |
| `mvp_site/frontend_*` / `app.js` | Render server-provided fields | Coerce booleans for business decisions, infer level-up availability |
| `roadmap/*.md` | Keep design and migration truth | Drift into stale implementation claims |

## North Star Architecture

```text
Stage 1: PROMPT          prompt files                        -> model contract
Stage 2: MODEL           LLM                                 -> level_up_signal
Stage 3: PARSE           narrative_response_schema.py         -> typed response field
Stage 4: EXTRACT         structured_fields_utils.py           -> structured_fields
Stage 5: FORMAT          rewards_engine.py                   -> rewards_box/planning_block
Stage 6: MODAL WRAP      world_logic.py                      -> modal lock/finish semantics
Stage 7: PERSIST/RETURN  llm_parser.py                       -> Firestore + API/SSE payload
Stage 8: RENDER          frontend                            -> display only
```

The same stages apply to streaming and non-streaming responses. Transport is allowed
to differ; semantic and formatting code is not.

## Canonical Model Output

Whenever XP is awarded, or level-up is otherwise relevant, the model must emit
`level_up_signal`.

### Level-Up Available

```json
{
  "level_up": true,
  "new_level": 5,
  "previous_turn_exp": 6200,
  "current_turn_exp": 6500,
  "xp_to_next_level": 14000,
  "source": "combat",
  "choices": [
    {"type": "hp", "description": "Gain hit points for Level 5"},
    {"type": "class_feature", "description": "Extra Attack"},
    {"type": "spellcasting", "description": "Unlock 3rd-level spell slots"}
  ],
  "rewards": {
    "gold": 150,
    "loot": ["Potion of Healing"]
  }
}
```

### XP Award Without Level-Up

```json
{
  "level_up": false,
  "previous_turn_exp": 200,
  "current_turn_exp": 250,
  "xp_to_next_level": 300,
  "source": "encounter",
  "rewards": {
    "gold": 0,
    "loot": ["None"]
  }
}
```

### Field Semantics

| Field | Required When | Meaning |
|-------|---------------|---------|
| `level_up` | Always | Model decision. `true` means present level-up UI. `false` means XP/rewards only. |
| `new_level` | `level_up=true` | Target level to offer. Must be 1-20. |
| `previous_turn_exp` | XP awarded | Total character XP before this user turn. |
| `current_turn_exp` | XP awarded | Total character XP after this user turn. |
| `xp_gained` | Derived display field | Backend may compute `current_turn_exp - previous_turn_exp`. The model should not rely on this as the canonical source. |
| `xp_to_next_level` | XP awarded | Total XP threshold for the next level, not remaining XP. Alias: `next_level_xp`. |
| `xp_remaining` | Optional | Remaining XP delta if useful: `xp_to_next_level - current_turn_exp`. |
| `choices` | `level_up=true` only | Model-owned level-up choices or benefits to preserve. Must be omitted for `level_up=false`. |
| `rewards.gold` | Any reward | Numeric currency value, even if the narrative calls it credits, crowns, or scrip. |
| `rewards.loot` | Any reward | List of reward item names, or `["None"]`. |

## Backend Contract

`mvp_site/rewards_engine.py` owns the only formatter for this signal:

```python
format_model_level_up_signal(level_up_signal) -> (rewards_box, planning_block)
```

Allowed backend work on the model-owned path:

- Confirm the signal is a non-empty dict.
- Resolve explicit migration aliases such as old `xp_total` into `current_turn_exp`
  only while compatibility is required.
- Coerce primitive values to deterministic types.
- Reject malformed or unsafe explicit values.
- Copy model-provided choices only when `level_up` is true.
- Build deterministic UI controls such as `level_up_now` and `continue_adventuring`.
- Compute deterministic display values from explicit model fields, such as
  `xp_gained = current_turn_exp - previous_turn_exp` and
  `progress_percent = round(current_turn_exp / xp_to_next_level * 100)`.
- Preserve raw/legacy fallback when no valid model-owned non-level signal exists.

Forbidden backend work on the model-owned path:

- Calling `level_from_xp()` to decide whether a level-up is available.
- Calling `xp_needed_for_level()` to infer a target level.
- Comparing old XP to new XP to detect threshold crossings.
- Interpreting stale flags such as `level_up_pending` as a substitute for model output.
- Reading narrative text for keywords.
- Rebuilding level-up benefit lists from class/level data when the model supplied choices.

## Fail-Closed Rules

Malformed model-owned signals must not create fake UI.

| Case | Behavior |
|------|----------|
| `level_up=true` without `new_level` | Return `(None, None)`. Do not derive target level. |
| `level_up=true` with `new_level > 20` | Return `(None, None)`. Do not surface invalid level UI. |
| `level_up=true` without `previous_turn_exp`, `current_turn_exp`, or `xp_to_next_level` | Return `(None, None)`. Do not synthesize `0/0` progress. |
| `level_up=false` with XP but missing progress fields | Return `(None, None)` from model formatter so canonicalization can fall back to raw `rewards_box` if present. |
| `level_up=false` with `choices` | Drop choices. No `level_up_choices` in `rewards_box`. |
| Top-level `gold` / `loot` instead of nested `rewards` | Accept as defensive alias. |
| Alias key exists with `None` value | Skip it and use the next non-`None` alias. Preserve valid `0`. |

## Single Root and Call Graph

The ZFC path must preserve the 2026-04-14 single-root invariant:

```text
llm_parser.py
  -> structured_fields_utils.extract_structured_fields()
  -> rewards_engine.canonicalize_rewards(structured_fields, game_state, original_state)
  -> world_logic.inject_modal_state(...)
  -> persistence / response delivery
```

There must be one canonicalize call per request. After `rewards_engine` returns, later
files may wrap or render the payload but may not recalculate the level-up decision.

Polling or legacy recovery may call:

```python
rewards_engine.project_level_up_ui(game_state_dict)
```

That path is transitional and must be deleted after live evidence shows model responses
consistently emit valid `level_up_signal`.

## File Responsibility Details

### Prompt Files

Prompt files define the model contract. They must say:

- Emit `level_up_signal` for every XP award.
- Use `level_up=true` only when level-up UI should be offered.
- Use `level_up=false` for normal XP progress.
- `xp_to_next_level` means total threshold, not remaining delta.
- `choices` is only for `level_up=true`.
- Do not wait for backend code to compute thresholds.
- Do not instruct direct level mutation as the level-up decision path.

Prompt files must not contain both the ZFC signal contract and an older direct algorithm
that tells the model to increment `level`, reset XP, and apply benefits automatically.

### `narrative_response_schema.py`

The schema accepts and preserves the model-owned field. It does not decide whether the
signal is correct.

Responsibilities:

- Parse `level_up_signal` as a structured response field.
- Keep it available through `to_dict()`.
- Avoid lossy cleanup that drops valid signal fields.

Non-responsibilities:

- No XP threshold math.
- No class feature synthesis.
- No state mutation.

### `structured_fields_utils.py`

This file extracts fields from a parsed response into `structured_fields`.

Responsibilities:

- Include `level_up_signal` only when it is a non-empty dict.
- Omit empty dicts and wrong-typed values.
- Preserve the exact dict for `rewards_engine`.

Non-responsibilities:

- No semantic validation.
- No alias normalization.
- No UI formatting.

### `rewards_engine.py`

This is the deterministic backend boundary for rewards and level-up presentation.

Responsibilities:

- Prefer valid `level_up_signal` over legacy inferred paths.
- Format model-owned XP/reward fields into `rewards_box`.
- Build `planning_block` only when `level_up=true`.
- Enforce atomicity for level-up UI: level-up rewards and planning block travel together.
- Preserve non-level rewards without requiring a planning block.
- Fail closed for malformed true level-up signals.
- Fall back to raw rewards for malformed false/non-level signals when raw rewards exist.

Non-responsibilities:

- No model calls.
- No Firestore writes.
- No semantic level-up detection on the model-owned path.
- No prompt text parsing.
- No frontend rendering decisions beyond deterministic show/hide payload fields.

### `world_logic.py`

World logic wraps precomputed payloads in modal and story semantics.

Allowed:

- Add modal locks.
- Inject finish choices.
- Preserve already-computed `rewards_box` and `planning_block`.
- Add non-level-up story/adventure hooks outside the rewards decision.

Forbidden:

- Recomputing XP progress.
- Synthesizing level-up choices from class data on the model-owned path.
- Calling `resolve_level_up_signal()` for new model-owned responses.

### `game_state.py`

Game state remains the owner of deterministic storage and legacy mechanical primitives.

Allowed:

- Store `level_up_pending`, XP totals, and character level.
- Provide deterministic XP threshold helpers for legacy paths and tests.
- Persist state updates provided by the pipeline.

Forbidden on the model-owned path:

- Deciding that a new response should level up because XP crossed a threshold.
- Replacing missing model choices with server-derived choices.

### `agents.py`

Routing should delegate to central helpers and not grow its own level-up flag logic.

Allowed:

- Use a centralized helper to determine whether the level-up modal is active.
- Route active level-up interactions to the correct modal/agent flow.

Forbidden:

- Inline flag interpretation.
- XP extraction.
- Stale pending flag recovery logic.

### Frontend

The frontend renders exactly what the server sends.

Allowed:

- Display `rewards_box`.
- Display `planning_block`.
- Render `level_up_now` and `continue_adventuring` choices.

Forbidden:

- Inferring `level_up_available` from XP numbers.
- Re-coercing business booleans to fix backend ambiguity.
- Creating level-up buttons without a server `planning_block`.

## Implementation Plan

The implementation order is deliberately cleanup-first. The failure mode in the older
stack was adding new centralization layers while old recovery paths stayed alive. That
made every test failure ambiguous: either the model contract was wrong, the formatter
was wrong, or a legacy repair path quietly rewrote the result. Stage 0 removes that
ambiguity before the MVP asks the model to prove compliance.

### Stage 0: Delete No-Op and Duplicate Logic First

Goal: reduce the amount of live level-up logic before adding more behavior.

Scope:

- Remove transient review/trigger comments and no-op scaffolding in test/repro files.
- Delete or quarantine unreachable legacy branches inside `rewards_engine._canonicalize_core()`.
- Isolate `project_level_up_ui()` behind a clearly named transitional call site so it
  cannot look like a permanent ZFC path.
- Remove the duplicate direct streaming projection if `_build_early_metadata_payload()`
  already computes the same `project_level_up_ui()` pair for the same `GameState`.
- Rename legacy `prepared.gemini_request` references toward `prepared.llm_request`
  when touching request preparation; the underlying `LLMRequest` is provider-neutral.
- Identify every `resolve_level_up_signal()` call and classify it as:
  - keep temporarily for legacy response compatibility,
  - replace with `format_model_level_up_signal()`,
  - delete because the signal is already explicit.
- Identify every parallel resolver concept in `rewards_engine.py`, `world_logic.py`,
  and `game_state.py`; the target shape is one public rewards-engine entrypoint and
  no model-owned semantic inference outside the model response.
- Remove duplicated helper logic in repro tests only when it can be done without a new
  abstraction file. If DRYing requires new shared infrastructure, defer it.
- Keep https://github.com/jleechanorg/worldarchitect.ai/pull/6378's repro-suite
  lesson: non-production repro/test code should exercise production behavior, not
  patch it.

Acceptance:

- `rg -n "trigger coderabbit|TODO delete|temporary review" testing_mcp mvp_site roadmap`
  returns no tracked transient scaffolding.
- The doc lists every remaining legacy level-up inference call site and why it still
  exists.
- The doc lists `GameState.from_dict()` / `GameState.to_dict()` as callstack steps
  where state is transported, not interpreted.
- No production behavior changes unless a deleted branch is proven unreachable or
  redundant by tests.

### Stage 1: MVP Real-Model Compliance Probe

Goal: measure whether the LLM can reliably compute level-up facts before deleting
legacy safety nets.

MVP contract:

```json
{
  "level_up": false,
  "previous_turn_exp": 200,
  "current_turn_exp": 250,
  "xp_to_next_level": 300,
  "source": "encounter",
  "rewards": {"gold": 0, "loot": ["None"]}
}
```

and:

```json
{
  "level_up": true,
  "new_level": 5,
  "previous_turn_exp": 6200,
  "current_turn_exp": 6500,
  "xp_to_next_level": 6500,
  "source": "combat",
  "choices": [
    {"type": "class_feature", "description": "Extra Attack"}
  ],
  "rewards": {"gold": 150, "loot": ["Potion of Healing"]}
}
```

Implementation:

- Update the prompt contract to require `previous_turn_exp` and `current_turn_exp`.
- Keep old `xp_earned` / `xp_total` aliases only as temporary input compatibility in
  `format_model_level_up_signal()`.
- Add a diagnostic evidence script or focused `testing_mcp` run that records raw model
  output and formatter result for:
  - XP award without level-up,
  - XP award exactly crossing threshold,
  - XP award above threshold,
  - no XP award with unrelated loot.
- Record compliance counts:
  - valid signal,
  - missing `previous_turn_exp`,
  - missing `current_turn_exp`,
  - inconsistent `current_turn_exp < previous_turn_exp`,
  - true level-up without `new_level`,
  - true level-up without choices.

Acceptance:

- Real streaming evidence shows the model emits the new fields in raw structured output.
- Formatter rejects malformed true signals without fabricating UI.
- Formatter can still render reward-only signals without planning blocks.
- Failures are classified as model-compliance failures, not hidden by backend repairs.

### Stage 2: Formatter Narrowing

Goal: make `rewards_engine.py` the only production file that translates model level-up
fields into UI payloads.

Work:

- Make `format_model_level_up_signal()` accept canonical names first:
  `previous_turn_exp`, `current_turn_exp`, `xp_to_next_level`.
- Compute `xp_gained` from those totals.
- Make `choices` illegal for `level_up=false`.
- Keep strict atomicity: true level-up needs both rewards/progress and choices.
- Remove or gate any fallback that tries to build missing choices from class data when
  `level_up_signal` is present.

Acceptance:

- Unit tests prove canonical fields work without legacy aliases.
- Alias tests exist only as migration tests and are labeled for deletion.
- No direct threshold-crossing decision is made in the model-owned formatter path.

### Stage 3: Transport Parity

Goal: streaming and non-streaming both converge on the same formatter with the same
fail-closed behavior.

Work:

- Confirm `llm_parser.py` streaming calls `canonicalize_rewards()` exactly once.
- Confirm non-streaming `world_logic.process_action_unified` uses the same helper.
- Move any remaining transport-specific reward formatting into `rewards_engine.py` or
  delete it if duplicate.

Acceptance:

- A grep/test gate proves only the canonical formatter path formats `level_up_signal`.
- Both transports persist the same `structured_response.rewards_box` and
  `structured_response.planning_block` shape for equivalent model output.

### Stage 4: Delete Legacy Backend Inference

Goal: remove the old Python-owned level-up decision path after evidence shows the model
contract works.

Deletion candidates:

- `resolve_level_up_signal()` new-path usage.
- `project_level_up_ui()` polling/recovery usage.
- Any backend code that compares old/current XP to decide level-up availability after
  `level_up_signal` exists.
- Any code that synthesizes ASI/class choices from level data to repair missing model
  choices on the new path.

Acceptance:

- Real model evidence passes for XP-only and level-up cases.
- UI evidence shows rewards-only and level-up states.
- Legacy deletion PR removes code instead of adding alternate inference.

### Stage 5: Enforcement

Goal: stop future drift.

Work:

- Add grep gates for old prompt algorithms and duplicate inference call sites.
- Add an architecture test that fails when a new file interprets `level_up_signal`
  outside `rewards_engine.py`.
- Require PR descriptions to state whether production level-up behavior changed.
- Keep lane discipline: branch health and 7-green proof matter more than merging
  during unattended sessions.

## Tests Required

### Unit Tests

- Parse and preserve `level_up_signal` in `NarrativeResponse`.
- Extract only non-empty dict `level_up_signal` values.
- Format true signals into atomic `(rewards_box, planning_block)`.
- Format false signals into rewards-only payloads.
- Drop choices when `level_up=false`.
- Reject `new_level > 20`.
- Reject true signals missing required XP totals.
- Skip `None` aliases while preserving valid `0`.
- Fall back to raw rewards when a false signal is malformed.
- Populate `progress_percent`.
- Preserve top-level `gold` / `loot` aliases.

### Integration Tests

- Streaming response with `level_up_signal` persists the signal and returns formatted UI.
- Non-streaming response with `level_up_signal` follows the same formatter path.
- Stored story entry can be reloaded without recomputing the level-up decision.
- Legacy response without `level_up_signal` still uses the old fallback during migration.

### Evidence Tests

- Real model, real server, streaming path for XP-only reward.
- Real model, real server, streaming path for level-up reward.
- Browser/UI evidence for both visible states.
- Green Gate logs must show gate-level pass lines, not just workflow success.

## Grep Gates

These are intended as executable acceptance checks.

```bash
# No direct level-up mutation algorithm in prompt contract.
rg -n 'Increment `?level`?|Reset `?experience\.current`?|Apply level-up benefits' \
  mvp_site/prompts/game_state_instruction.md \
  mvp_site/prompts/rewards_system_instruction.md

# Choices must be conditional on true level-up.
rg -n "choices.*level_up.*false|level_up=false.*choices" mvp_site/prompts

# Backend model-owned path must not call XP threshold helpers inside formatter.
rg -n "format_model_level_up_signal|level_from_xp|xp_needed_for_level" mvp_site/rewards_engine.py

# New field must travel through all required layers.
rg -n "FIELD_LEVEL_UP_SIGNAL|level_up_signal" \
  mvp_site/constants.py \
  mvp_site/narrative_response_schema.py \
  mvp_site/structured_fields_utils.py \
  mvp_site/rewards_engine.py \
  mvp_site/tests
```

## Design Invariants

1. **Model decides; backend formats.**
2. **One formatter path owns `level_up_signal`.**
3. **No file gets a second job to patch around another file's ambiguity.**
4. **True level-up is atomic: rewards plus planning block, or neither.**
5. **False level-up is rewards-only: no level-up choices.**
6. **Malformed true signals fail closed.**
7. **Malformed false signals may fall back to raw rewards but must not invent `0/0` progress.**
8. **Prompt, schema, formatter, tests, and roadmap must change together.**
9. **Legacy fallback is temporary and must be deleted only after live evidence.**
10. **UI renders; it does not decide.**

## Current PR Scope

https://github.com/jleechanorg/worldarchitect.ai/pull/6404 intentionally keeps the
design, prompt contract, parser schema, formatter, and tests together. That reduces
the drift seen in the previous split PR stack.

In scope:

- Add the ZFC design anchor.
- Add and preserve `level_up_signal`.
- Prefer the model-owned formatter when a signal is present.
- Fail closed for malformed true level-up signals.
- Preserve reward-only fallback for malformed false signals.
- Align prompt language with the new signal contract.
- Add targeted tests for the model-owned path.

Out of scope for this first PR:

- Deleting every legacy backend level-up fallback.
- Rewriting modal completion.
- Rewriting frontend rendering.
- Closing or merging older PRs.
- Producing final real-server UI evidence for every branch of the migration.

## Follow-Up Queue

1. Add grep gates from this document to CI or an existing architecture test.
2. Run real streaming evidence for XP-only and level-up cases.
3. Audit `world_logic.py`, `agents.py`, and `game_state.py` for legacy level-up
   interpretation still reachable from new model-owned responses.
4. Delete legacy fallback only when evidence shows valid `level_up_signal` coverage.
5. Update any stale roadmap/beads that still describe backend threshold computation as
   the north star for level-up decisions.
