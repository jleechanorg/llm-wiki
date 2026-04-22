# ZFC Level-Up Architecture: Model Computes, Backend Formats

**Date**: 2026-04-19
**Status**: Design draft for https://github.com/jleechanorg/worldarchitect.ai/pull/6404 and follow-up cleanup
**Supersedes**: Backend-centralization-only level-up plan for the level-up decision
**Builds on**: `roadmap/level-up-engine-single-responsibility-design-2026-04-14.md`
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
`progress_percent = current_turn_exp / total_exp_for_next_level`. The backend must
not infer that a level-up happened from threshold crossings on the new model-owned
path.

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
5. [Deletion Candidates](#deletion-candidates)
6. [Public Method Contract Catalog](#public-method-contract-catalog)
7. [Core Tenets](#core-tenets)
8. [North Star Architecture](#north-star-architecture)
9. [Canonical Model Output](#canonical-model-output)
10. [Backend Contract](#backend-contract)
11. [Fail-Closed Rules](#fail-closed-rules)
12. [Single Root and Call Graph](#single-root-and-call-graph)
13. [File Responsibility Details](#file-responsibility-details)
14. [Implementation Plan](#implementation-plan)
15. [Tests Required](#tests-required)
16. [Grep Gates](#grep-gates)
17. [Design Invariants](#design-invariants)
18. [Current PR Scope](#current-pr-scope)
19. [Follow-Up Queue](#follow-up-queue)
20. [Wiki Search and Two-Hop BFS Findings](#wiki-search-and-two-hop-bfs-findings)
21. [TDD Implementation Roadmap](#tdd-implementation-roadmap)

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

Visual target:

```text
Browser
  app.js
    handleStreamingInteraction()
      -> streaming.js StreamingClient.sendMessage()
        -> main.py handle_interaction_stream()
          -> llm_parser.py stream_story_with_game_state()
            -> game_state.py GameState.from_dict()
            -> world_logic.py pre-routing modal click shim
            -> llm_service.py continue_story_streaming()
              -> llm_service.py _prepare_story_continuation()
                -> llm_request.py LLMRequest.to_json()
                -> provider adapter
                  -> LLM emits level_up_signal
              -> narrative_response_schema.py preserves level_up_signal
            -> structured_fields_utils.py extracts level_up_signal
            -> rewards_engine.py canonicalize_rewards()
              -> private formatter validates explicit model fields
              -> returns rewards_box/planning_block or suppresses malformed UI
            -> world_logic.py wraps modal affordances only
            -> firestore_service.py persists canonical fields
          -> SSE done payload
      -> app.js renders server-provided UI
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
| Prompt contract | https://github.com/jleechanorg/worldarchitect.ai/pull/6404 asks the model to emit `level_up_signal`, but field naming still needs to move from `xp_earned` / `xp_total` / `xp_to_next_level` to `previous_turn_exp` / `current_turn_exp` / `total_exp_for_next_level` / `additional_exp_to_next_level`. | Original design did not require the model to own the decision. | Prompt makes model output the complete level-up fact set. |
| Schema/parser | `level_up_signal` is preserved through structured response parsing. | Centralization is present, but compliance is only as good as model output. | Parser is a lossless transport boundary. |
| Formatter | `format_model_level_up_signal()` exists and is preferred when a signal is present. | Legacy fallback still shares the file, so accidental drift remains possible and the formatter looks like a second public API. | `canonicalize_rewards()` is the public API; formatter helpers are private and handle explicit signal only. |
| Projection | `project_level_up_ui()` still projects UI from game state before the model responds. | This violates the clean ZFC north star but was kept for compatibility. | Migrate projection semantics behind `canonicalize_rewards({}, state)`, then delete the wrapper after MVP shows model emits compliant signals. |
| Inference | `resolve_level_up_signal()` still exists for fallback/projection, with duplicate resolver concepts in `world_logic.py` and `game_state.py`. | Original centralization tolerated centralized backend inference. | No backend semantic inference on model-owned path; remaining legacy resolver calls are named and isolated. |
| Streaming/non-streaming parity | Streaming uses `llm_parser.py` persistence; non-streaming uses `world_logic.process_action_unified`. | The single-root invariant is not fully enforced across transports. | Both transports call the same signal formatter and persistence boundary. |
| UI | Frontend mostly renders server-provided structured fields. | It still has streaming partial JSON heuristics for display, unrelated to level-up decision. | UI never derives level-up availability. |
| Evidence | Unit tests exist for the formatter path. | Real model compliance is not yet measured. | MVP evidence quantifies valid/invalid model signal rates before deletion. |

## Traversed File Responsibility Summary

This table distinguishes the target responsibility from the current violations. The
violations column is intentionally explicit so future PRs can delete or quarantine
drift instead of normalizing it.

| File | Ideally Owns | Must Not Own | Current Violations / Drift | Delete or Quarantine? |
|------|--------------|--------------|----------------------------|-----------------------|
| `mvp_site/frontend_v1/app.js` | User interaction orchestration, stream callbacks, final story rendering, structured-field rendering entrypoint. | XP math, level-up detection, semantic coercion, creating level-up buttons without server payloads. | Some streaming partial-render helpers parse and stage structured UI before the final done payload; keep only display logic. | Do not delete file. Quarantine level-up rendering behind server-provided `planning_block` / `rewards_box` only. |
| `mvp_site/frontend_v1/js/streaming.js` | POST body, auth headers, SSE parsing, callback dispatch. | Gameplay meaning, level-up availability, rewards formatting. | No level-up decision ownership found in the target path; keep it transport-only. | Do not delete. |
| `mvp_site/main.py` | HTTP/SSE route boundary, request validation, auth/rate-limit checks, response streaming. | Level-up formatting, inference, modal state mutation. | No target-path level-up ownership should live here. | Do not delete. |
| `mvp_site/llm_parser.py` | Streaming orchestration, `GameState` construction, model stream handoff, exactly one canonical formatter call, Firestore write ordering. | Duplicate rewards formatting, threshold detection, modal decision logic. | It currently computes early metadata through `project_level_up_ui()` and also persists final canonical fields. The direct streaming projection appears duplicated with `_build_early_metadata_payload(...)`. | Keep file. Stage 0 should remove duplicate projection and leave one metadata builder. |
| `mvp_site/llm_service.py` | Agent/model/provider selection, provider-neutral `LLMRequest`, prompt payload, provider stream, structured response parse handoff. | Backend gameplay judgment from response text, rewards formatting, level-up modal state. | `prepared.gemini_request` is a legacy name for provider-neutral request data. | Keep file. Rename request field to `llm_request` when touching this area. |
| `mvp_site/llm_request.py` | Provider-neutral request serialization. | Provider-specific gameplay decisions or Gemini-only semantics. | `to_json()` doc/naming imply Gemini because callers call it through `gemini_request`. | Keep file. Update naming/docs only. |
| `mvp_site/narrative_response_schema.py` | Canonical structured response schema, lossless `level_up_signal` preservation. | D&D semantic validation, XP threshold math, state mutation, UI construction. | Existing experience validation warns on threshold crossing in player state; that is separate legacy validation and must not become signal interpretation. | Keep file. Add canonical `level_up_signal` schema docs and field names. |
| `mvp_site/structured_fields_utils.py` | Extract non-empty structured fields from parsed response. | Alias normalization, UI payload construction, semantic validation. | If it normalizes `level_up_signal` aliases later, that would be drift; aliases belong in the formatter during migration. | Keep file. |
| `mvp_site/rewards_engine.py` | Deterministically format explicit model reward/level-up signals into UI payloads, enforce atomicity, preserve temporary legacy fallback. | Model calls, Firestore writes, text interpretation, new-path threshold inference, class-benefit synthesis when model choices are missing. | Contains legacy `resolve_level_up_signal()`, `project_level_up_ui()`, public-looking formatter/helper APIs, and fallback branches that still infer from state. | Keep file, but delete/quarantine legacy resolver/projection after MVP evidence. This should be the largest net deletion target. |
| `mvp_site/world_logic.py` | Modal/story wrapper, modal locks, finish choice injection, turn/living-world bookkeeping. | Recomputing XP progress, synthesizing level-up choices, deciding level-up from state on model-owned responses. | Has `_resolve_level_up_signal(...)` and finish-choice paths that can re-evaluate state. `_maybe_trigger_level_up_modal(...)` is still needed as a pre-routing click shim. | Keep file. Quarantine/remove duplicate resolver usage; keep only modal coordination. |
| `mvp_site/game_state.py` | Persistent state shape, `GameState.from_dict(...)`, `GameState.to_dict()`, mechanical consistency checks, legacy helpers. | Model-output interpretation, new-path level-up decisions, missing-choice repair. | Has a parallel `resolve_level_up_signal(...)` concept for legacy state mechanics. | Keep file. Rename/quarantine legacy resolver or delete if unused after formatter migration. |
| `mvp_site/firestore_service.py` | Campaign/game-state/story-entry reads and writes. | Business decisions, formatting, schema repair. | No target-path level-up ownership should live here. | Do not delete. |
| `mvp_site/prompts/*.md` | Model contract: tell the LLM exactly which structured facts to compute. | Conflicting backend-owned algorithms or stale XP field ambiguity. | Several prompt files still mention older fields or direct XP/state mutation language alongside the new signal. | Keep files. Update prompt contract and remove conflicting old instructions. |
| `roadmap/zfc-level-up-model-computes-2026-04-19.md` | Architecture contract, file boundaries, deletion plan, evidence expectations. | Stale claims that transitional code is already deleted. | Must stay synchronized between the repo copy and the operator's home-roadmap copy. | Do not delete. |

## Deletion Candidates

The goal is a negative net line count across the ZFC migration. New schema/tests/docs
are allowed, but production level-up logic should shrink.

| Candidate | File | Estimated Net LOC | Why It Can Go | Prerequisite |
|-----------|------|-------------------|---------------|--------------|
| Duplicate direct streaming projection | `mvp_site/llm_parser.py` | -10 to -25 | `_build_early_metadata_payload(...)` already computes projected early metadata for the same state. | Unit test proving metadata payload is unchanged. |
| Public `project_level_up_ui(...)` wrapper | `mvp_site/rewards_engine.py` | -10 to -20 | It is a wrapper around `_canonicalize_core(None, None, state, None)`. | Callers migrated to `canonicalize_rewards({}, state)` or the feature is deleted after model evidence. |
| Legacy `resolve_level_up_signal(...)` in rewards engine | `mvp_site/rewards_engine.py` | -50 to -100 | New path uses explicit model signal. | Real-model compliance for XP-only and level-up cases; legacy callers removed. |
| Legacy `_canonicalize_core(...)` fallback branches | `mvp_site/rewards_engine.py` | -120 to -250 | They infer/synthesize UI from state when explicit model signal should exist. | MVP evidence and focused regression tests. |
| Duplicate resolver in `world_logic.py` | `mvp_site/world_logic.py` | -60 to -140 | Modal wrapper should consume canonical payload, not re-resolve level-up state. | Finish-choice and stale-flag tests moved to canonical output assertions. |
| Duplicate resolver in `game_state.py` | `mvp_site/game_state.py` | -40 to -100 | Game state should serialize and validate mechanically, not own new-path decisions. | Confirm no non-level-up state migrations require it. |
| Old prompt algorithms / ambiguous field text | `mvp_site/prompts/*.md` | -80 to -200 | Conflicts with the canonical model-output contract. | Prompt update plus real-model evidence. |

Expected production net for the full migration: **roughly -250 to -650 LOC** after
legacy deletion. The first PR may be positive because it adds schema/tests/docs, but
the migration is not successful until production code deletion exceeds production code
addition.

Files that should not be deleted: `llm_parser.py`, `llm_service.py`, `llm_request.py`,
`narrative_response_schema.py`, `structured_fields_utils.py`, `world_logic.py`,
`game_state.py`, `firestore_service.py`, and frontend transport/rendering files. The
target is not fewer files; it is fewer owners of level-up semantics.

## Public Method Contract Catalog

Only the public surfaces listed here should be used by the ZFC level-up path. Any new
public method added for level-up must update this section and justify why it cannot be
private.

| File | Public Surface Used | Goal | Tenet | Why It Exists | What It Does |
|------|---------------------|------|-------|---------------|--------------|
| `mvp_site/frontend_v1/app.js` | `handleStreamingInteraction(userInput, mode)` | Start a user action stream. | UI initiates, server decides. | Entry point from browser input to server stream. | Creates the in-progress entry and delegates transport to `StreamingClient`. |
| `mvp_site/frontend_v1/app.js` | `renderStoryEntryElement(..., fullData)` | Render final server payload. | Render-only UI. | Single final-story rendering entrypoint. | Displays narrative and structured server fields, including rewards/planning blocks. |
| `mvp_site/frontend_v1/app.js` | `generateStructuredFieldsPreNarrative(fullData, debugMode)` | Render server-provided pre-narrative structured fields. | No UI inference. | Existing display hook for rewards boxes. | Converts present fields to HTML; must not invent level-up state. |
| `mvp_site/frontend_v1/app.js` | `parsePlanningBlocks(planningBlock)` / `parsePlanningBlocksJson(planningBlock)` | Render server choices. | Server owns choice semantics. | Existing planning-block button renderer. | Parses JSON planning blocks and renders choices already supplied by the server. |
| `mvp_site/frontend_v1/js/streaming.js` | `StreamingClient.sendMessage(userInput, mode)` | Transport request to streaming endpoint. | Transport only. | Browser needs one POST/SSE entrypoint. | Sends input/mode and dispatches stream callbacks. |
| `mvp_site/main.py` | `handle_interaction_stream(user_id, campaign_id, user_email)` | HTTP boundary. | Route only. | Flask endpoint for streaming interactions. | Validates request/auth/rate limits and starts SSE generation. |
| `mvp_site/llm_parser.py` | `stream_story_with_game_state(user_id, campaign_id, user_input, mode)` | Streaming orchestration. | One canonical formatter call. | Coordinates context load, model stream, persistence, and final SSE payload. | Loads state, calls LLM service, canonicalizes structured fields, persists, and yields events. |
| `mvp_site/llm_parser.py` | `_build_early_metadata_payload(current_game_state)` | Transitional early metadata. | Compatibility during migration. | Existing pre-response UI needs a single projection point until model signal coverage is proven. | Emits early rewards/planning metadata from current state; delete or narrow later. |
| `mvp_site/llm_service.py` | `continue_story_streaming(...)` | Provider streaming entrypoint. | Model computes. | Starts the LLM request pipeline. | Prepares request, streams chunks, parses final structured response. |
| `mvp_site/llm_service.py` | `_prepare_story_continuation(...)` | Build provider-neutral request. | No gameplay judgment in transport. | Shared prep for streaming/non-streaming paths. | Selects agent/model/provider and creates `LLMRequest`. |
| `mvp_site/llm_request.py` | `LLMRequest.to_json()` | Serialize provider-neutral model context. | Request serialization only. | Providers need a stable JSON prompt payload. | Serializes context, state, tools, and prompt metadata without deciding gameplay. |
| `mvp_site/narrative_response_schema.py` | `NarrativeResponse(...)` | Typed structured response container. | Preserve model output. | Central schema object for parsed model responses. | Stores `level_up_signal` without deciding semantics. |
| `mvp_site/narrative_response_schema.py` | `NarrativeResponse.to_dict()` | Lossless response serialization. | Preserve model output. | Downstream pipeline needs structured fields as dicts. | Emits `level_up_signal` alongside other structured fields. |
| `mvp_site/narrative_response_schema.py` | `parse_structured_response(...)` | Parse model JSON into schema. | Parse, do not infer. | Converts raw model output into `NarrativeResponse`. | Parses and validates syntax/shape, not D&D level-up correctness. |
| `mvp_site/structured_fields_utils.py` | `extract_structured_fields(gemini_response_obj)` | Extract non-empty fields. | Lossless extraction. | Persistence pipeline uses a compact structured-field dict. | Copies `level_up_signal` forward when it is a non-empty dict. |
| `mvp_site/rewards_engine.py` | `canonicalize_rewards(structured_fields, game_state_dict, original_state_dict=None)` | Single public rewards UI convergence point. | Model decides; backend formats. | Prevents scattered level-up UI construction. | Consumes explicit model signal when present, returns canonical `(rewards_box, planning_block)`. |
| `mvp_site/rewards_engine.py` | `format_model_level_up_signal(level_up_signal)` | Transitional explicit-signal formatter. | Private-by-default formatter detail. | Exists now for tests and migration; should become `_format_model_level_up_signal`. | Coerces explicit fields, computes deterministic display values, and builds UI payloads. |
| `mvp_site/rewards_engine.py` | `project_level_up_ui(game_state_dict)` | Transitional pre-response projection. | Legacy compatibility only. | Existing early metadata/pre-modal badge flows need projection before model output. | Projects UI from state; migrate/delete after MVP evidence. |
| `mvp_site/world_logic.py` | `_maybe_trigger_level_up_modal(user_input, story_context, current_game_state)` | Pre-routing modal-click bridge. | Modal coordination only. | `level_up_now` user clicks must set modal flags before agent selection. | Mutates modal flags for explicit modal choices; must not infer level-up from XP. |
| `mvp_site/world_logic.py` | `_inject_modal_finish_choice_if_needed(...)` | Modal affordance wrapper. | Preserve canonical payload. | Modal flows need finish/continue choices. | Adds finish choices without rebuilding rewards or level-up choices. |
| `mvp_site/game_state.py` | `GameState.from_dict(state_dict)` | State construction. | State transport only. | Converts Firestore dict into runtime state. | Builds `GameState` without interpreting model response semantics. |
| `mvp_site/game_state.py` | `GameState.to_dict()` | State serialization. | State transport only. | Prompt/persistence layers need dict state. | Serializes state mechanically. |
| `mvp_site/firestore_service.py` | `get_campaign_game_state(...)` | Load state. | Persistence only. | Request path needs stored state. | Reads persisted game-state document. |
| `mvp_site/firestore_service.py` | `update_campaign_game_state(...)` | Persist state. | Persistence only. | Request path must save state updates. | Writes already-decided state. |
| `mvp_site/firestore_service.py` | `add_story_entry(...)` | Persist story entries. | Persistence only. | Story history needs user/model entries. | Stores canonical structured fields without interpreting them. |

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
level_up_signal -> rewards_engine.canonicalize_rewards()
                -> private explicit-signal formatter
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

### 4. File-Level Responsibility Headers

Every touched production file in this migration should get a short top-of-file
responsibility docstring or existing module docstring update. The docstring is not a
replacement for tests; it is a local tripwire for future drift.

Required shape:

```python
"""[File name] responsibility for ZFC level-up.

Owns:
- ...

Must not own:
- ...

Level-up boundary:
- ...
"""
```

For JavaScript files, use the same content in a top file comment. The skeptic review
should read these headers and fail the PR if code below the header violates the stated
boundary.

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

### Target Path Latency Shape

This is a qualitative graph, not a benchmark. The target may spend the same model
latency, but it removes backend repair branches and duplicated projection work.

```text
Relative work after model response

high | old path:    parse -> infer -> repair -> project -> wrap -> persist -> render
     |              ***************^^^^^^^^^^^************
     |
     | target path: parse -> validate/format -> wrap -> persist -> render
low  |              ********^^^^^^^************
     +--------------------------------------------------------------------------> time
                    parse    backend decision/formatting       delivery/render

Legend:
  * transport / persistence / rendering work that still exists
  ^ backend level-up decision or repair work that should shrink or disappear
```

### Level-Up Available

```json
{
  "level_up": true,
  "current_level": 4,
  "new_level": 5,
  "next_level": 5,
  "previous_turn_exp": 6200,
  "current_turn_exp": 6500,
  "total_exp_for_next_level": 6500,
  "additional_exp_to_next_level": 0,
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
  "current_level": 1,
  "next_level": 2,
  "previous_turn_exp": 200,
  "current_turn_exp": 250,
  "total_exp_for_next_level": 300,
  "additional_exp_to_next_level": 50,
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
| `current_level` | Always when XP is awarded | Character level before applying the level-up decision for this response. |
| `new_level` | `level_up=true` | Target level to offer. Must be 1-20. Kept for compatibility with existing UI wording. |
| `next_level` | XP awarded | The next level number being evaluated. For `level_up=true`, this should match `new_level`; for `level_up=false`, it is the next level threshold the player has not reached yet. |
| `previous_turn_exp` | XP awarded | Total character XP before this user turn. |
| `current_turn_exp` | XP awarded | Total character XP after this user turn. |
| `xp_gained` | Derived display field | Backend may compute `current_turn_exp - previous_turn_exp`. The model should not rely on this as the canonical source. |
| `total_exp_for_next_level` | XP awarded | Total lifetime XP threshold for `next_level`. This replaces ambiguous `xp_to_next_level`. |
| `additional_exp_to_next_level` | XP awarded | Remaining XP delta from `current_turn_exp` to `total_exp_for_next_level`. For available level-up it should be `0`. |
| `xp_to_next_level` | Temporary alias only | Deprecated ambiguous name. During migration, formatter may accept it as `total_exp_for_next_level`; prompts and canonical schema must stop emitting it. |
| `xp_remaining` | Temporary alias only | Deprecated alias for `additional_exp_to_next_level`. |
| `choices` | `level_up=true` only | Model-owned level-up choices or benefits to preserve. Must be omitted for `level_up=false`. |
| `caveats` | Deferred optional extension | Model self-critique about uncertainty or gaps. Not part of M0/M1 acceptance unless explicitly promoted by a separate schema PR. |
| `rewards.gold` | Any reward | Numeric currency value, even if the narrative calls it credits, crowns, or scrip. |
| `rewards.loot` | Any reward | List of reward item names, or `["None"]`. |

### Deferred Caveats Contract

`caveats` is useful future observability, but it is not the fail-closed guardrail for
the base ZFC migration. The base guardrail is deterministic validation of explicit
fields plus suppression of malformed true level-up UI.

If `caveats` is promoted from follow-up to implementation scope, the same PR must add:

- prompt/schema documentation for `level_up_signal.caveats`,
- parser preservation tests,
- formatter behavior that records or passes through caveats without changing the
  level-up decision,
- evidence showing caveats do not become a backend semantic classifier,
- a deletion-gate rule stating whether caveats are required before legacy inference is
  removed.

Until then, deletion PRs must not claim caveats as proof that model output is safe.

## Backend Contract

`mvp_site/rewards_engine.py` owns the only formatter for this signal:

```python
format_model_level_up_signal(level_up_signal) -> (rewards_box, planning_block)
```

Allowed backend work on the model-owned path:

- Confirm the signal is a non-empty dict.
- Resolve explicit migration aliases such as old `xp_total` into `current_turn_exp`
  and old `xp_to_next_level` into `total_exp_for_next_level` only while compatibility
  is required.
- Coerce primitive values to deterministic types.
- Reject malformed or unsafe explicit values.
- Copy model-provided choices only when `level_up` is true.
- Build deterministic UI controls such as `level_up_now` and `continue_adventuring`.
- Compute deterministic display values from explicit model fields, such as
  `xp_gained = current_turn_exp - previous_turn_exp`,
  `additional_exp_to_next_level = max(0, total_exp_for_next_level - current_turn_exp)`,
  and `progress_percent = round(current_turn_exp / total_exp_for_next_level * 100)`.
- Preserve raw/legacy fallback when no valid model-owned non-level signal exists.

The formatter exists because earlier layers should not know presentation payload shape.
The model owns semantic facts; schema/parser layers preserve those facts; the formatter
does the deterministic translation from explicit facts into current UI fields:

- canonical signal fields to legacy display keys (`current_xp`, `xp_total`,
  `next_level_xp`) while the UI still expects them,
- model choices to `planning_block.choices`,
- reward details to `rewards_box`,
- safe defaults for optional non-semantic display fields,
- atomic suppression when true level-up UI is malformed.

Forbidden backend work on the model-owned path:

- Calling `level_from_xp()` to decide whether a level-up is available.
- Calling `xp_needed_for_level()` to infer a target level.
- Comparing old XP to new XP to detect threshold crossings.
- Interpreting stale flags such as `level_up_pending` as a substitute for model output.
- Reading narrative text for keywords.
- Rebuilding level-up benefit lists from class/level data when the model supplied choices.

## Fail-Closed Rules

Malformed model-owned signals must not create fake UI.

**Fail closed** means quietly suppressing the level-up UI/rewards badge for malformed
true signals so the user is not soft-locked by a broken modal. It never means
synthesizing a repair block, inventing choices, deriving a target level, or showing a
half-valid `0/0` progress payload.

| Case | Behavior |
|------|----------|
| `level_up=true` without `new_level` | Return `(None, None)`. Do not derive target level. |
| `level_up=true` with `new_level > 20` | Return `(None, None)`. Do not surface invalid level UI. |
| `level_up=true` without `previous_turn_exp`, `current_turn_exp`, or `total_exp_for_next_level` | Return `(None, None)`. Do not synthesize `0/0` progress. |
| `level_up=false` with XP but missing progress fields | Return `(None, None)` from model formatter so canonicalization can fall back to raw `rewards_box` if present. |
| `level_up=false` with `choices` | Drop choices. No `level_up_choices` in `rewards_box`. |
| Top-level `gold` / `loot` instead of nested `rewards` | Accept as defensive alias. |
| Alias key exists with `None` value | Skip it and use the next non-`None` alias. Preserve valid `0`. |

### Fail-Closed Decision Tree

```text
level_up_signal present?
|
+-- no ----------------------------------------------------+
|                                                        |
|   Use temporary legacy fallback if this is a legacy     |
|   response and the fallback is still allowed in M0-M2.  |
|
+-- yes
    |
    +-- level_up == true?
    |   |
    |   +-- required fields valid?
    |   |   |
    |   |   +-- yes -> format rewards_box + planning_block atomically
    |   |   |
    |   |   +-- no  -> return (None, None); do not repair or infer
    |   |
    |   +-- choices present?
    |       |
    |       +-- yes -> preserve model choices
    |       +-- no  -> fail closed; do not synthesize class choices
    |
    +-- level_up == false?
        |
        +-- XP/reward fields valid?
        |   |
        |   +-- yes -> format reward/progress payload without level-up choices
        |   +-- no  -> fall back only to explicit raw rewards_box when allowed
        |
        +-- choices present? -> drop choices; false signals never create modal UI
```

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
- `previous_turn_exp` means total XP before this user turn.
- `current_turn_exp` means total XP after this user turn.
- `total_exp_for_next_level` means total lifetime XP threshold for `next_level`.
- `additional_exp_to_next_level` means the remaining delta after this turn.
- `xp_to_next_level`, `xp_total`, and `xp_earned` are deprecated aliases and should
  not appear in the canonical prompt examples after this migration.
- `choices` is only for `level_up=true`.
- Do not wait for backend code to compute thresholds.
- Do not instruct direct level mutation as the level-up decision path.

Prompt files must not contain both the ZFC signal contract and an older direct algorithm
that tells the model to increment `level`, reset XP, and apply benefits automatically.

Prompt updates must be paired with the canonical JSON schema update. The prompt,
schema, formatter, and tests must use the same canonical field names in the same PR;
otherwise agents will keep repairing one layer while another layer teaches the old
contract.

### `narrative_response_schema.py`

The schema accepts and preserves the model-owned field. It does not decide whether the
signal is correct.

Responsibilities:

- Parse `level_up_signal` as a structured response field.
- Document the canonical JSON object with:
  `level_up`, `current_level`, `next_level`, `new_level` when true,
  `previous_turn_exp`, `current_turn_exp`, `total_exp_for_next_level`,
  `additional_exp_to_next_level`, `source`, `choices`, and `rewards`.
- Keep it available through `to_dict()`.
- Avoid lossy cleanup that drops valid signal fields.
- Treat `xp_to_next_level`, `xp_total`, and `xp_earned` as migration aliases only;
  the canonical schema examples must not prefer them.

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
- Track the skipped assertion in
  `mvp_site/tests/test_rewards_engine_wiring.py:116` as a named temporary exception:
  it should fail once `world_logic.py` no longer imports or calls a level-up resolver.
  The deletion deadline is Stage 4, when duplicate resolver usage is removed.

Acceptance:

- `rg -n "trigger coderabbit|TODO delete|temporary review" testing_mcp mvp_site roadmap`
  returns no tracked transient scaffolding.
- The doc lists every remaining legacy level-up inference call site and why it still
  exists.
- The doc lists `GameState.from_dict()` / `GameState.to_dict()` as callstack steps
  where state is transported, not interpreted.
- Every legacy branch scheduled for deletion has a characterization test that calls
  the legacy path and produces known output before deletion. That test is deleted or
  rewritten with the branch in Stage 4; otherwise branch deletion is not evidence-backed.
- No production behavior changes unless a deleted branch is proven unreachable or
  redundant by tests.

### Stage 1: MVP Real-Model Compliance Probe

Goal: measure whether the LLM can reliably compute level-up facts before deleting
legacy safety nets.

MVP contract:

```json
{
  "level_up": false,
  "current_level": 1,
  "next_level": 2,
  "previous_turn_exp": 200,
  "current_turn_exp": 250,
  "total_exp_for_next_level": 300,
  "additional_exp_to_next_level": 50,
  "source": "encounter",
  "rewards": {"gold": 0, "loot": ["None"]}
}
```

and:

```json
{
  "level_up": true,
  "current_level": 4,
  "new_level": 5,
  "next_level": 5,
  "previous_turn_exp": 6200,
  "current_turn_exp": 6500,
  "total_exp_for_next_level": 6500,
  "additional_exp_to_next_level": 0,
  "source": "combat",
  "choices": [
    {"type": "class_feature", "description": "Extra Attack"}
  ],
  "rewards": {"gold": 150, "loot": ["Potion of Healing"]}
}
```

Implementation:

- Update the prompt contract to require `previous_turn_exp` and `current_turn_exp`.
- Update prompt examples and canonical schema docs to require
  `total_exp_for_next_level` and `additional_exp_to_next_level`.
- Keep old `xp_earned` / `xp_total` / `xp_to_next_level` aliases only as temporary
  input compatibility in `format_model_level_up_signal()`.
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
  `previous_turn_exp`, `current_turn_exp`, `total_exp_for_next_level`,
  `additional_exp_to_next_level`.
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
- Add skeptic-agent review criteria for responsibility drift:
  - read every touched file's top-level responsibility docstring/comment,
  - inspect the diff for code that violates the stated "Must not own" list,
  - fail if a file gains a new level-up semantic responsibility outside this design,
  - fail if production LOC added exceeds production LOC deleted without explicit
    justification.
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

# Canonical prompt/schema examples should not prefer deprecated XP field names.
rg -n '"xp_earned"|"xp_total"|"xp_to_next_level"' \
  mvp_site/prompts \
  mvp_site/narrative_response_schema.py

# Canonical field names must exist in prompt/schema/formatter/test layers.
rg -n "previous_turn_exp|current_turn_exp|total_exp_for_next_level|additional_exp_to_next_level" \
  mvp_site/prompts \
  mvp_site/narrative_response_schema.py \
  mvp_site/rewards_engine.py \
  mvp_site/tests

# Backend model-owned path must not call XP threshold helpers inside formatter.
# Transitional matches are expected before Stage 4 because legacy fallback still calls
# resolver/threshold helpers. After Stage 4, this gate must have no new-path matches.
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
6. **Malformed true signals fail closed: suppress the malformed UI instead of repairing it.**
7. **Malformed false signals may fall back to raw rewards but must not invent `0/0` progress.**
8. **Prompt, schema, formatter, tests, and roadmap must change together.**
9. **Legacy fallback is temporary and must be deleted only after live evidence.**
10. **UI renders; it does not decide.**
11. **Transitional state is explicit: code labeled transitional must have a named removal trigger, such as Stage N evidence or a specific test condition.**
12. **Caveats are not implicit safety evidence: if `caveats` becomes a release
    blocker, it must have schema, parser, formatter, and evidence gates before any
    legacy fallback is deleted because of it.**

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
4. Remove the `test_rewards_engine_wiring.py:116` skip when the `world_logic.py`
   duplicate resolver exception is deleted in Stage 4.
5. Delete legacy fallback only when evidence shows valid `level_up_signal` coverage
   and the legacy characterization tests prove the deleted branches were understood.
6. Update any stale roadmap/beads that still describe backend threshold computation as
   the north star for level-up decisions.

## Wiki Search and Two-Hop BFS Findings

On 2026-04-20, this document was ingested into the local LLM wiki and
searched with a two-hop BFS over the ZFC, rewards-engine, level-up centralization,
stale-flag, schema, streaming, and frontend rewards-box topics. The exact-term memory
searches for the new `previous_turn_exp` / `current_turn_exp` language returned no
matches, which means this document is the first canonical indexed source for that
field naming.

The BFS surfaced five constraints that must shape implementation:

1. **Old centralization pages conflict with the ZFC target.** Wiki pages such as
   `RewardsEngine`, `LevelUpArchitecture`, and the 2026-04-14 design describe
   `rewards_engine.py` as the owner of backend signal detection and threshold
   inference. This document supersedes that for the model-owned path: the backend may
   format and validate explicit facts, but it must not decide level-up availability
   from XP thresholds on new responses.
2. **Streaming passthrough caused real drift before.** The
   `StreamingPassthroughNormalization` page records a prior bug where raw model
   `rewards_box` data bypassed normalization before persistence. The ZFC rewrite must
   keep streaming and non-streaming on one canonical formatter path, even while
   deleting duplicate legacy branches.
3. **Frontend double-gates regressed server-owned UI before.** The
   `FrontendRewardsBoxGate` history shows that `app.js` once duplicated backend
   visibility logic and suppressed valid rewards UI. The target UI contract remains:
   if the server sends canonical `rewards_box` / `planning_block`, the frontend
   renders rather than re-deciding.
4. **Stale modal flags are historical guardrails, not random clutter.** The
   `LevelUpStaleFlagGuards` and `LevelUpModalRouting` pages explain why modal shims
   still exist. Stage 0 may remove duplicate projection calls, but it must not delete
   modal-start or stale-flag guards until characterization tests and live evidence
   prove the replacement path is behaviorally equivalent.
5. **Prior proof artifacts did not equal landed architecture.** `PR6339` and the
   `LevelUpCentralTracker` history show local green slices and evidence can exist for
   branches that do not land. Implementation PRs must therefore use merged-code tests,
   Green Gate log verification, and skeptic gates rather than relying on roadmap
   claims or branch-local evidence.

Follow-up from the BFS: `roadmap/caveats-field-2026-04-19.md` proposes a model
`caveats` field. That is relevant to future fail-closed observability, but it is not
part of M0 cleanup and is not a hidden prerequisite for M1. Treat it as a separate
M1/M2 schema extension only after the basic model-computes contract is stable. If a
future PR wants to use caveats as deletion evidence, it must first promote the field
from follow-up to canonical contract and add the tests listed in
[Deferred Caveats Contract](#deferred-caveats-contract).

## TDD Implementation Roadmap

This roadmap turns the design into a sequence of independently mergeable PRs. The
system must be fully working after every PR; no PR may rely on a broken intermediate
state that is fixed by a later PR.

### Roadmap Rules

- Use `/4layer` for every behavior-changing PR:
  - **Layer 1**: Unit tests.
  - **Layer 2**: End-to-end tests with mocked external services.
  - **Layer 3**: MCP/HTTP API tests against a real local server.
  - **Layer 4**: Browser tests with real services, only when UI behavior can change.
- Every commit must be **500 changed lines or fewer**. If a change is larger, split it.
- Test commits and production-code commits must be separate:
  - Commit A: failing or characterization tests.
  - Commit B: production cleanup/change.
  - Commit C: test expectation deletion/update only when deleting legacy behavior.
- Every PR must leave the app shippable after merge.
- Prefer deletion and narrowing over abstraction. New helper files require explicit
  justification.
- M0 is cleanup/deletion first. Do not start the broader ZFC rewrite while duplicate
  legacy paths still make failures ambiguous.

### Milestone Checklist Crosswalk

This table converts the implementation stages into 1-2 week milestones with concrete
0.5-2 day steps. Percentages are planning state, not completion claims.

| Milestone | Target | Progress | Outstanding Steps |
|-----------|--------|----------|-------------------|
| M0 cleanup | Delete/quarantine duplicate legacy paths before rewrite | 0% | 10 |
| M1 compliance | Measure real model compliance for canonical signal fields | 0% | 8 |
| M2 deletion | Remove legacy backend inference sequentially | 0% | 8 |
| M3 enforcement | Lock the architecture with gates and skeptic checks | 0% | 8 |

#### M0 Steps

- [ ] Delete transient scaffolding.
  - [ ] Remove review-trigger comments from tracked tests and repros.
  - [ ] Remove no-op prompt or evidence placeholders.
  - [ ] Confirm no tracked `TODO delete` comments survive without bead links.
  - [ ] Keep historical evidence files only when referenced by CI or roadmap.
- [ ] Quarantine `rewards_engine._canonicalize_core()` legacy branches.
  - [ ] Characterize each branch with a Layer 1 test before deletion.
  - [ ] Label legacy-only branches with a Stage 4 deletion trigger.
  - [ ] Prevent malformed true `level_up_signal` from entering fallback repair.
  - [ ] Keep alias compatibility isolated in the formatter.
- [ ] Isolate `project_level_up_ui()`.
  - [ ] Identify every caller.
  - [ ] Replace safe callers with `canonicalize_rewards({}, game_state_dict)`.
  - [ ] Preserve pre-modal behavior until live evidence exists.
  - [ ] Mark the wrapper transitional with a deletion trigger.
- [ ] Remove duplicate streaming projection.
  - [ ] Prove `_build_early_metadata_payload()` computes the same pair.
  - [ ] Delete the direct duplicate call in `stream_story_with_game_state(...)`.
  - [ ] Verify no double projection occurs in one request.
  - [ ] Run the Layer 1 and Layer 2 streaming metadata slices.
- [ ] Rename provider-neutral request variables.
  - [ ] Rename touched `prepared.gemini_request` references to `prepared.llm_request`.
  - [ ] Keep provider-specific behavior inside provider adapters.
  - [ ] Update tests that assert request serialization names.
  - [ ] Avoid unrelated transport refactors.
- [ ] Classify each `resolve_level_up_signal()` call.
  - [ ] Mark keep/replace/delete for `rewards_engine.py`.
  - [ ] Mark keep/replace/delete for `world_logic.py`.
  - [ ] Mark keep/replace/delete for `game_state.py`.
  - [ ] Add the Stage 4 deletion deadline to each kept call.
- [ ] Audit public formatter surfaces.
  - [ ] Keep `canonicalize_rewards(...)` as the only target public entrypoint.
  - [ ] Make `format_model_level_up_signal()` private after migration callers are gone.
  - [ ] Keep `llm_parser` to one canonicalize call per request.
  - [ ] Confirm `world_logic.process_action_unified()` wraps but does not recompute.
- [ ] Add responsibility headers.
  - [ ] Document what each touched file owns.
  - [ ] Document what each touched file must not own.
  - [ ] Include `GameState.from_dict()` / `GameState.to_dict()` transport-only wording.
  - [ ] Feed these headers to skeptic review.
- [ ] Add architecture tests.
  - [ ] Assert `level_up_signal` formatting stays in rewards engine.
  - [ ] Assert prompt examples use canonical XP field names.
  - [ ] Assert deprecated aliases are accepted only as input aliases.
  - [ ] Assert skipped resolver wiring test has a Stage 4 deletion trigger.
- [ ] Keep each PR shippable.
  - [ ] Split test and production commits.
  - [ ] Keep every commit under 500 changed lines.
  - [ ] Run the relevant `/4layer` subset.
  - [ ] Push evidence with the PR before requesting review.

#### M1 Steps

- [ ] Build real-model probe prompts.
- [ ] Capture raw `level_up_signal` output for XP-only responses.
- [ ] Capture raw `level_up_signal` output for level-up-available responses.
- [ ] Classify failures as model, schema, formatter, persistence, or UI.
- [ ] Tune prompts without deleting legacy fallback.
- [ ] Verify `previous_turn_exp` and `current_turn_exp` are present and total-valued.
- [ ] Decide whether `caveats` is still deferred or promoted to a schema PR.
- [ ] Publish `/4layer` evidence before any deletion PR starts.

#### M2 Steps

- [ ] Delete one legacy projection or resolver path per PR.
- [ ] Start each deletion PR with characterization tests.
- [ ] Keep production deletion commits separate from test commits.
- [ ] Delete `project_level_up_ui()` only after callers migrate.
- [ ] Delete `resolve_level_up_signal()` new-path usage only after evidence.
- [ ] Delete duplicate `world_logic.py` resolver usage after modal parity proof.
- [ ] Delete duplicate `game_state.py` resolver usage after state parity proof.
- [ ] Remove deprecated aliases only after real model output is stable.

#### M3 Steps

- [ ] Add CI grep gates for deprecated output names.
- [ ] Add CI grep gates for duplicate resolver ownership.
- [ ] Add architecture tests for one formatter root.
- [ ] Add PR-template evidence requirements for level-up changes.
- [ ] Add skeptic-agent checks against file responsibility headers.
- [ ] Add net LOC deletion check against the M0 baseline.
- [ ] Add Green Gate log verification to merge readiness.
- [ ] Close or retarget stale roadmap/beads after enforcement lands.

### Whole-File Deletion Answer

No major traversed production file should be deleted wholesale. The files are still
valid owners of their non-level-up responsibilities:

- Keep `llm_parser.py`, `llm_service.py`, `llm_request.py`,
  `narrative_response_schema.py`, `structured_fields_utils.py`, `rewards_engine.py`,
  `world_logic.py`, `game_state.py`, `firestore_service.py`, and frontend files.
- Delete or quarantine **code paths**, not files:
  - `project_level_up_ui()` wrapper after callers migrate.
  - `resolve_level_up_signal()` duplicates after characterization and evidence.
  - `_canonicalize_core()` legacy fallback branches after MVP coverage.
  - old prompt algorithms and ambiguous field examples.
  - duplicate streaming projection call sites.

Whole-file deletion candidates are limited to obsolete one-off repro/evidence files if
they are not imported, not referenced by CI, and not needed as historical evidence.
Those deletions belong in a separate non-production cleanup PR with no production-code
changes.

### Parallelization Model

Parallel work is safe only when write scopes do not overlap.

| Lane | Can Run In Parallel? | Write Scope | Notes |
|------|----------------------|-------------|-------|
| M0-A duplicate streaming projection | Yes | `mvp_site/llm_parser.py`, focused tests | Independent of prompt/schema naming. |
| M0-B rewards-engine legacy characterization | Yes with M0-C only if tests are disjoint | `mvp_site/tests/test_rewards_engine*.py` first, then `mvp_site/rewards_engine.py` | Do not edit prompts here. |
| M0-C world/game-state resolver audit | Yes | `mvp_site/tests/test_rewards_engine_wiring.py`, `mvp_site/world_logic.py`, `mvp_site/game_state.py` | Must not touch rewards formatter internals in the same PR. |
| M0-D prompt/schema naming prep | Yes | `mvp_site/prompts/*`, `mvp_site/narrative_response_schema.py`, schema tests | No production deletion. |
| M1 model compliance evidence | After M0-A/B/D | `testing_mcp/`, evidence docs | Requires stable contract. |
| M2 deletion PRs | Sequential after evidence | production code deletion | Each deletion PR proves no behavior regression. |

### M0 Goal: Cleanup Before Rewrite

M0 reduces ambiguity without changing the user-visible level-up contract. It should
delete or isolate duplicate paths while preserving current behavior.

#### M0-PR1: Remove Duplicate Early Projection Call

Purpose: make streaming early metadata have one projection point.

Scope:

- Keep `_build_early_metadata_payload(current_game_state)` as the only early metadata
  projection call.
- Remove the direct duplicate `project_level_up_ui(current_game_state.to_dict())`
  call from `stream_story_with_game_state(...)` if tests prove identical metadata.
- No prompt/schema changes.
- No rewards-engine semantic changes.

Commits:

1. Test commit, max 500 lines:
   - Add/adjust a Layer 1 unit test proving `_build_early_metadata_payload(...)`
     emits the same `rewards_box` / `planning_block` currently added by the direct
     projection block.
   - Add a regression assertion that `stream_story_with_game_state(...)` does not
     double-project for one request, using a spy/fake where practical.
2. Production commit, max 500 lines:
   - Delete the duplicate direct projection block.
   - Route all early metadata through `_build_early_metadata_payload(...)`.

`/4layer` plan:

- Layer 1: `./vpython -m pytest mvp_site/tests/test_rewards_engine_wiring.py -q`
- Layer 2: run the narrow streaming end-to-end test if present; otherwise add one
  under `mvp_site/tests/test_end2end/`.
- Layer 3: only if Layer 2 passes and streaming metadata is still suspect:
  `./vpython testing_mcp/streaming/test_level_up_streaming_e2e.py`
- Layer 4: not required unless browser metadata rendering changes.

Merge condition:

- Metadata shape is unchanged.
- PR diff is net negative or neutral in production code.
- App remains fully functional after merge.

#### M0-PR2: Characterize Legacy Rewards-Engine Fallback Before Deletion

Purpose: prove the legacy fallback behavior before deleting or narrowing it later.

Scope:

- No production deletion in this PR unless the branch is proven unreachable.
- Add characterization tests for:
  - legacy `resolve_level_up_signal(...)` path,
  - `_canonicalize_core(...)` fallback when no model `level_up_signal` exists,
  - malformed true `level_up_signal` suppressing fallback,
  - false/reward-only signal preserving raw rewards where intended.
- Mark each characterization test with the Stage 4 deletion trigger.

Commits:

1. Test commit, max 500 lines:
   - Add characterization tests with known output.
   - Include comments naming the Stage 4 deletion trigger.
2. Optional production cleanup commit, max 500 lines:
   - Delete only unreachable branches proven by the tests.
   - Rename legacy helper to make transitional status explicit only if the diff stays
     under 500 lines.

`/4layer` plan:

- Layer 1: `./vpython -m pytest mvp_site/tests/test_rewards_engine.py -q`
- Layer 2: `./vpython -m pytest mvp_site/tests/test_end2end/test_*level* -q` if such
  tests exist; otherwise skip with explicit reason.
- Layer 3: not required unless fallback affects streaming persistence.
- Layer 4: not required.

Merge condition:

- Legacy behavior is captured before deletion.
- No user-visible behavior changes unless explicitly proven unreachable.
- Production LOC should not increase except for transitional naming comments.

#### M0-PR3: Quarantine Duplicate Resolver Ownership

Purpose: stop `world_logic.py` and `game_state.py` from looking like permanent
level-up decision owners.

Scope:

- Track and resolve the `mvp_site/tests/test_rewards_engine_wiring.py:116` skip.
- Rename or wrap duplicate resolver usages with explicit transitional naming.
- Add architecture tests that fail if new model-owned responses call duplicate
  resolver paths outside `rewards_engine.canonicalize_rewards(...)`.
- Keep `_maybe_trigger_level_up_modal(...)` because it handles explicit modal clicks
  before agent selection.

Commits:

1. Test commit, max 500 lines:
   - Add/enable wiring assertions for duplicate resolver imports/calls.
   - Add a positive allowance for explicitly named transitional legacy paths.
2. Production commit, max 500 lines:
   - Rename/quarantine resolver helper usage without changing behavior.
   - Update comments/docstrings to state removal trigger.

`/4layer` plan:

- Layer 1: `./vpython -m pytest mvp_site/tests/test_rewards_engine_wiring.py mvp_site/tests/test_world_logic.py -q`
- Layer 2: targeted end-to-end modal/level-up flow if available.
- Layer 3: `./vpython testing_mcp/streaming/test_level_up_streaming_e2e.py` if modal
  routing is touched.
- Layer 4: browser test only if visible modal behavior changes.

Merge condition:

- Current modal routing still works.
- Duplicate resolver ownership is visibly temporary.
- No broken intermediate state.

#### M0-PR4: Add Responsibility Headers and Skeptic Gate Inputs

Purpose: create local enforcement points before refactoring logic.

Scope:

- Add top-of-file responsibility docstrings/comments to only files touched by the ZFC
  migration.
- Add skeptic-agent checklist text or a lightweight architecture test that reads the
  headers and checks for forbidden ownership terms.
- No behavior changes.

Commits:

1. Test commit, max 500 lines:
   - Add architecture/header test or checker fixture.
2. Production/doc commit, max 500 lines:
   - Add docstrings/comments to touched production files.

`/4layer` plan:

- Layer 1: architecture/header unit test.
- Layer 2: not required for docstring-only changes.
- Layer 3: not required.
- Layer 4: not required.

Merge condition:

- Header test passes.
- No production behavior changed.
- Future skeptic reviews have concrete file-local responsibility statements to audit.

#### M0-PR5: Prompt and Canonical Schema Naming Prep

Purpose: align language before the model compliance MVP.

Scope:

- Update prompt examples and canonical schema documentation to prefer:
  `current_level`, `next_level`, `previous_turn_exp`, `current_turn_exp`,
  `total_exp_for_next_level`, `additional_exp_to_next_level`.
- Mark `xp_to_next_level`, `xp_total`, and `xp_earned` as deprecated input aliases.
- Do not delete backend alias support yet.

Commits:

1. Test commit, max 500 lines:
   - Add grep/contract tests that canonical examples use the new names.
   - Add tests proving deprecated names are aliases, not canonical output names.
2. Prompt/schema commit, max 500 lines:
   - Update prompts and schema docs only.

`/4layer` plan:

- Layer 1: prompt/schema grep tests and parser/schema unit tests.
- Layer 2: narrow end-to-end model-output parsing test with fake response.
- Layer 3: not required until real-model compliance.
- Layer 4: not required.

Merge condition:

- Existing model outputs still parse through alias compatibility.
- New canonical examples are unambiguous.
- No UI behavior changes.

### M1: Model Compliance MVP

Purpose: measure real model compliance before deleting legacy backend inference.

PR shape:

- One PR for evidence harness/tests.
- One PR for prompt tuning if the model fails compliance.
- Keep production formatter deletion out of M1.

`/4layer` plan:

- Layer 1: formatter tests for canonical signal fields.
- Layer 2: fake LLM end-to-end tests for XP-only and level-up signals.
- Layer 3: real local server `testing_mcp` runs that capture raw model output and
  formatter output.
- Layer 4: browser evidence for XP-only reward and level-up available UI.

Merge condition:

- Evidence classifies failures as model compliance, formatter, persistence, or UI.
- No legacy deletion occurs until evidence is good enough to make deletion safe.

### M2: Sequential Deletion PRs

Purpose: remove legacy backend inference after M0 characterization and M1 evidence.

PR order:

1. Delete `project_level_up_ui()` wrapper after callers use
   `canonicalize_rewards({}, state)` or no longer need pre-response projection.
2. Delete/quarantine `rewards_engine.resolve_level_up_signal(...)` new-path usage.
3. Delete duplicate resolver usage from `world_logic.py`.
4. Delete duplicate resolver usage from `game_state.py`.
5. Remove deprecated prompt aliases once real model output is stable.

Each deletion PR:

- starts with a test commit proving current behavior or proving the path is no longer
  reachable,
- has a separate production deletion commit,
- stays under 500 changed lines per commit,
- runs the minimum `/4layer` ladder needed for the touched behavior,
- leaves the app fully working after merge.

### M3: Final Enforcement

Purpose: prevent regression after deletion.

Scope:

- CI grep gates for deprecated canonical names and duplicate resolver ownership.
- Architecture test that only `rewards_engine.canonicalize_rewards(...)` formats
  `level_up_signal`.
- PR template requirement for level-up behavior changes.
- Skeptic-agent exit criteria requiring file responsibility headers, net LOC check,
  `/4layer` evidence, and no broken intermediate PR state.

Merge condition:

- All enforcement gates pass.
- The production code line count for level-up logic is net negative versus the M0
  baseline.
