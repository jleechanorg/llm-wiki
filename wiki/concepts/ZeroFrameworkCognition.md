---
title: "Zero Framework Cognition"
type: concept
tags: [agent-patterns, architecture, orchestration, llm]
sources: []
last_updated: 2026-04-11
---

## Summary

Zero Framework Cognition (ZFC) is an architectural philosophy that mandates delegating ALL reasoning, classification, scoring, and composition decisions to external AI models, while application code handles only pure orchestration, IO, structural safety, and mechanical transforms. Originated by Steve Yegge (2025), it emerged from observing that AI assistants consistently write local-intelligence code (heuristics, keyword routing, scoring algorithms) rather than delegating decisions back to the model — creating brittleness that defeats the purpose of using AI in the first place.

## Core Thesis

Build applications as **pure orchestration** — application code gathers context and executes decisions, but never *makes* decisions about what those decisions should be. Any judgment call (classification, complexity estimation, routing, scoring, composition, scheduling) must go to the AI.

The Unix philosophy analogy: "dumb pipes, smart endpoints." The microservices analogy: Martin Fowler's "smart endpoints, dumb pipes." ZFC extends this to LLM applications: the *code* is the dumb pipe; the *model* is the smart endpoint.

## Forbidden Patterns (ZFC Violations)

These are **never** implemented in application code:

| Pattern | Example | Why |
|---|---|---|
| **Ranking/scoring algorithms** | `score = len(desc) // 10` | Heuristic weights substituting for AI judgment |
| **Keyword-based classification** | `if "analyze" in desc` | Template-matching bypasses model reasoning |
| **Heuristic routing** | `complex_keywords = ["system", "full", ...]` | Hand-coded decision trees replace AI decisions |
| **Complexity estimation** | `complexity_score = ...` | Code guessing task difficulty instead of asking AI |
| **Pattern-matching intent detection** | `hasSignal(signals, ['guard', 'protector'])` | Semantic scoring against keywords |
| **Weighted intent selection** | `weightedChoice(random, intentWeights)` | Hardcoded weights bias action selection |

## Compliant Patterns (Allowed)

These are safe to implement in application code:

- **IO and plumbing**: Read/write files, directory listing, JSON serialization
- **Structural safety checks**: Schema validation, path traversal prevention, allowlists
- **Policy enforcement**: Budget caps, rate limits, token ceilings
- **Mechanical transforms**: Parameter substitution, formatting, compilation
- **State management**: Lifecycle tracking, session persistence
- **Typed error handling**: SDK error classes with instanceof checks
- **Deterministic structural thresholds**: Numeric caps, array limits, timeouts

## The Correct Flow

```
1. Gather raw context  → IO only (files, user input, state)
2. Call AI for decisions → Classification, routing, scoring, composition
3. Validate structure  → Schema conformance, allowlists, budget checks
4. Execute mechanically → Run AI's decisions verbatim
```

## ZFC Evaluation: worldai_claw

### Compliant Core (Harness Layers 1, 3, 4)

**`state_reducer.ts`** — Gold standard ZFC compliance:
- Allowlist enforcement (`ALLOWED_STATE_KEYS`, `ALLOWED_PLAYER_KEYS`)
- Dangerous-key stripping (`__proto__`, `constructor`, etc.)
- D&D 5e mechanical constraints (HP/XP clamping from PHB thresholds)
- Type consistency checks in `deepMerge`
- Item-usage validation against inventory
- **All reasoning comes from the LLM's `state_delta`; the reducer only enforces structure and game rules**

**`slm_narrator.ts`** — All prose flows through `SLMNarrator.narrate()`. No template fallbacks — if the LLM call fails, it throws.

**`budgetEngine.ts`** / **`token_budget.ts`** — Deterministic token ceiling enforcement. Pure policy: trim order is mechanical, not cognitive.

**`openclaw_client.ts`** — OpenAI-compatible gateway client. All LLM decisions are made by the configured model; code only handles transport.

**`faction_simulator.ts` (partial)** — Single-LLM-call-per-tick for living world. The faction simulation itself delegates world-building to the model. LLM prompt explicitly instructs against "regex extraction or generic fallback names."

**`dice_executor.ts`** — Server-side deterministic dice rolling. The LLM *requests* a roll; the server executes mechanically.

### Violations Found

#### HIGH SEVERITY

**`faction_simulator.ts` lines 2096-2116** — Weighted intent selection for `CompanionAutonomyMode.BALANCED`:

```typescript
const intentWeights: Record<string, number> = {
  explore: 3, combat: 2, trade: 2, quest: 2, guard: 2,
};
// +1-2 per keyword signal match:
if (context?.cueTags.includes('trade')) intentWeights.trade += 2;
if (hasSignal(signals, ['guard', 'protector'])) intentWeights.guard += 2;
// ...
const actionType = weightedChoice(random, intentWeights);
```

**ZFC VIOLATION**: Semantic scoring via keyword matching. The code assigns weights based on `cueTags` and `signals` arrays containing keyword strings like `'guard'`, `'trader'`, `'aggressive'`, `'berserker'`. The LLM is instructed to produce these signals, but the *selection* of action type is made by a weighted-random algorithm in code — not by the AI.

**Why it matters**: The LLM generates a rich world simulation, but the companion's *actual behavior* is filtered through hardcoded weight biasing. This means the model's reasoning about what a companion would do is overridden by a heuristic.

**Fix direction**: Replace `weightedChoice(random, intentWeights)` with an LLM call that receives the companion's personality, current signals, and world state, and returns the action type directly.

#### MEDIUM SEVERITY

**`choice_utils.ts` lines 6-7, 27-31** — Hardcoded generic choice fallbacks:

```typescript
export const GENERIC_CHOICE_FALLBACKS = new Set(['continue', 'look around']);

export function _isGenericChoiceFallback(choices: string[]): boolean {
  return choices.every((choice) => GENERIC_CHOICE_FALLBACKS.has(choice.trim().toLowerCase()));
}
```

**ZFC VIOLATION**: Keyword-based classification of LLM output. When the LLM produces only generic choices (flagged by keyword match), the system applies a fallback. The classification is based on a hardcoded set of strings, not on the LLM's own judgment about whether those choices are meaningful.

**Why it matters**: The code is deciding that certain LLM outputs are "not meaningful" based on literal string matching, rather than asking the AI whether the choices are appropriate given the game context.

**Note**: The `_isGenericChoiceFallback` function is only called by `openclawClient.ts` for response parsing — it doesn't directly override LLM output in the critical path, but the pattern is a ZFC violation.

#### LOW SEVERITY (orchestration, not game logic)

**`orchestration/agent_system.py` lines 276-279** — Keyword-based task complexity detection:

```python
def _is_complex_task(self, description: str) -> bool:
    complex_keywords = ["system", "complete", "full", "entire", "comprehensive"]
    return any(keyword in description.lower() for keyword in complex_keywords)
```

**`orchestration/agent_system.py` lines 353-365** — Keyword-based task execution routing:

```python
if "analyze" in desc_lower:
    return f"Analysis complete: Found {len(components)} components..."
if "validate" in desc_lower:
    return f"Validation passed: Task '{description}' meets requirements"
if "optimize" in desc_lower:
    return f"Optimization complete: Improved performance..."
```

**`orchestration/agent_system.py` line 419** — Heuristic complexity scoring:

```python
complexity_score = len(description) // 10
return f"Specialized processing complete: Handled task with complexity level {complexity_score}"
```

**ZFC VIOLATION**: All three patterns implement local intelligence — the code is making routing and scoring decisions based on keyword presence and string length, rather than asking an AI to classify the task.

**Why it matters**: These are in the `orchestration/` package's `agent_system.py`, which appears to be legacy/demo code (the actual production orchestration uses `task_dispatcher.py`). The orchestrator delegates all real task analysis to the LLM CLI; this file contains stub agent classes.

**Note**: `agent_health_monitor.py` calculates a `health_score` using error count and inactivity time (weighted). This is **NOT** a ZFC violation — it's mechanical state monitoring (error_count, timestamp arithmetic), not semantic judgment. Structural scoring of process health is a policy check, not AI-classification.

**`testing_mcp/generate_integration_evidence.py` line 82** — `classify()` function:

```python
def classify(payload: dict[str, Any]) -> tuple[str, bool, int | None, str | None]:
    if "error" in payload and "code" in payload:
        status = payload.get("code")
        status_code = int(status) if isinstance(status, int | str) and str(status).isdigit() else None
        return ("expected_negative", True, status_code, str(payload.get("error")))
    status_raw = payload.get("status") or payload.get("turn_status")
    status_code = int(status_raw) if isinstance(status_raw, int | str) and str(status_raw).isdigit() else None
    passed = status_code is None or 200 <= status_code < 300
    return ("green", passed, status_code, None)
```

**Assessment**: This is a test utility that classifies HTTP responses as `green` / `expected_negative` based on HTTP status codes. It's mechanical HTTP response categorization (200 = pass, error field present = expected_negative), not semantic classification. **Not a ZFC violation** — it's structural response parsing.

### Story Compactor — Edge Case

**`story_compactor.ts` line 73** — Comment says "Simple heuristic: older entries that don't appear in recent are 'resolved'":

```typescript
// Simple heuristic: older entries that don't appear in recent are "resolved"
const resolved = removedTexts.filter(
  (text) => !recentTexts.some((recent) => recent.includes(text.split(' ').slice(-2).join(' ')))
);
```

**Assessment**: Borderline. The "resolved" categorization is a mechanical string-matching heuristic, not semantic analysis. It's applied to *formatting* the compaction artifact, not to decision-making that affects game state. The actual story entries are kept intact; only their categorization in the artifact is heuristic. This is acceptable under ZFC as a mechanical transform on metadata, though the comment is a red flag.

## Summary Assessment

| Component | ZFC Compliance | Notes |
|---|---|---|
| `state_reducer.ts` | ✅ Excellent | Gold standard — allowlist + mechanical rules only |
| `slm_narrator.ts` | ✅ Excellent | All prose via real LLM calls |
| `token_budget.ts` / `budgetEngine.ts` | ✅ Excellent | Deterministic policy enforcement |
| `dice_executor.ts` | ✅ Excellent | Server executes what LLM requests |
| `faction_simulator.ts` (main loop) | ✅ Excellent | Single-LLM-call-per-tick |
| `faction_simulator.ts` (BALANCED mode) | ❌ VIOLATION | Weighted keyword scoring for intent |
| `choice_utils.ts` | ❌ VIOLATION | Hardcoded keyword classification of LLM output |
| `agent_system.py` | ❌ VIOLATION | Keyword routing + heuristic complexity scoring |
| `story_compactor.ts` | ⚠️ Edge case | Mechanical metadata transform, acceptable but flagged |
| `agent_health_monitor.py` | ✅ Compliant | Mechanical state monitoring |
| `task_dispatcher.py` | ✅ Compliant | CLI fallback chains are mechanical ordering |
| `generate_integration_evidence.py::classify()` | ✅ Compliant | Mechanical HTTP response parsing |

**Overall**: worldai_claw's core game loop (LLM-decides / server-executes) is **strongly ZFC-compliant**. The violations are isolated to: (1) companion BALANCED autonomy mode's weighted intent selection, (2) choice fallback keyword matching, and (3) legacy orchestration demo code. The highest-priority fix is the `weightedChoice` in `faction_simulator.ts` — it directly biases companion behavior away from what the LLM would choose.

## Connections

- [[Harness5LayerModel]] — ZFC maps to Layer 3 (Execution: tool orchestration) and Layer 4 (Verification: structural safety checks). worldai_claw's state_reducer is a Layer 1 + Layer 4 combination: allowlists (L1 constraint) + game-rule clamping (L4 verification).
- [[jeffrey-oracle]] — The oracle is an L4 verification layer. Its decision table should similarly be ZFC-compliant: structural checks only, no heuristic scoring of PR intent.

## Sources

- Steve Yegge, "Zero Framework Cognition: A Way to Build Resilient AI Applications" (2025), https://steve-yegge.medium.com/zero-framework-cognition-a-way-to-build-resilient-ai-applications-56b090ed3e69
- Martin Fowler, "Smart Endpoints and Dumb Pipes" (2014)
- Steve Yegge, "The Gilded Rose" (2014)
- Andrej Karpathy, "Software 2.0" (2017)
