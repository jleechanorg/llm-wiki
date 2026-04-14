---
title: "Single Responsibility Pipeline"
type: concept
tags: [architecture, level-up, rewards, pipeline]
sources: [level-up-engine-v4-design]
last_updated: 2026-04-14
---

## Definition

A software architecture principle applied to the Level-Up Engine v4 design where each file in the rewards/progression flow has exactly ONE job, and the entire flow executes as a single forward pass with no re-entry.

## The 7-Stage Pipeline

| Stage | File | Responsibility |
|-------|------|----------------|
| **Stage 1: FETCH+PARSE** | `llm_parser.py` | Parse LLM response into structured fields (`rewards_box`, `planning_block`, `state_updates`) |
| **Stage 2: XP MATH** | `game_state.py` | Compute level, XP numbers from D&D 5e tables |
| **Stage 3: DETECT+BUILD** | `rewards_engine.py` | Detect level-up signals, build `rewards_box` and `planning_block` |
| **Stage 4: NORMALIZE** | `rewards_engine.py` | Clean types (booleans, coerced ints), compute `should_show` |
| **Stage 5: MODAL+STORY** | `world_logic.py` | Inject modal state, assemble narrative |
| **Stage 6: PERSIST** | `llm_parser.py` | Firestore write of game state + story entry |
| **Stage 7: RENDER** | `app.js` | Pure render — zero logic |

## Single-Responsibility-Per-File Rule

Each file has ONE job and MUST NOT do the job of other files:

| File | ONE Job | What It Does NOT Do |
|------|---------|---------------------|
| `llm_parser.py` | Parse LLM response + orchestrate pipeline + persistence + delivery | No XP math, no rewards detection/building, no modal logic |
| `game_state.py` | D&D 5e XP math + Firestore I/O + persisted state fields | No flag interpretation for UI, no rewards building |
| `rewards_engine.py` | ALL rewards/progression decisions: detect, build, normalize, decide | No XP math, no Firestore I/O, no story entries, no modal state |
| `world_logic.py` | Thin modal wrapper — inject modal state into pre-computed payload | No rewards detection/building, no XP math, no orchestration |
| `app.js` | Render server-decided payload | No boolean coercion, no visibility decisions |

## Single Forward Pass Rule

**No file called twice, no re-canonicalization or re-fetch of XP in the same request.** Each request calls `rewards_engine` exactly once via either `canonicalize_rewards()` (streaming/non-streaming) or `project_level_up_ui()` (polling). After that, `world_logic.inject_modal_state()` wraps the result. No file re-enters the pipeline.

## Contrast with Prior Art (v3)

The v3 architecture had TWO orchestration roots: `streaming_orchestrator.py` (streaming) and `world_logic.process_action_unified()` (non-streaming). Both called rewards normalization twice — once for Firestore persistence and once for the response. This double-touch pattern caused [[RewardsBoxAtomicity]] violations and type inconsistencies between streaming and non-streaming paths.

## Related Concepts

- [[RewardsEngineIdempotency]] — pipeline function must be safe to call once per request (idempotent)
- [[RewardsBoxAtomicity]] — `rewards_box` + `planning_block` must be treated as an atomic pair throughout the pipeline
- [[LevelUpModalRouting]] — Stage 5 modal injection constraints
- [[DefensiveNumericConversion]] — Stage 4 type normalization
