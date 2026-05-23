---
title: "worldarchitect.ai — ZFC Violations in worldai_claw"
type: concept
tags: [worldai_claw, ZFC, zero-framework-cognition, violations]
sources: []
last_updated: 2026-04-13
---

# worldarchitect.ai — ZFC Violations in worldai_claw

## Summary

- **HIGH Severity:** 3
- **MEDIUM Severity:** 2
- **LOW Severity:** 2 (exempt — contract validation)

---

## HIGH Severity

### faction_simulator.ts:1709-1712 — Keyword-Based Activity Classification

**File:** `packages/backend/src/world/faction_simulator.ts`

```typescript
const combinedText = (classText + ' ' + personalityText).toLowerCase();
if (/(aggress|fight|combat|war|protect|enforce|hunt|soldier|militant)/.test(combinedText)) weights.combat += 2;
if (/(scout|explor|curio|travel|navigate|pilot|ranger|diver)/.test(combinedText)) weights.explore += 2;
if (/(charm|social|diplo|negotiat|charisma|face|broker|fixer)/.test(combinedText)) weights.social += 2;
if (/(devot|duty|faith|mission|oath|loyal|pious|medic|auditor)/.test(combinedText)) weights.quest += 2;
```

**Why it violates ZFC:** Explicit keyword-based classification of player personality to determine activity weights. Uses regex on `classText` and `personalityText` to classify whether a player is combat/explore/social/quest-oriented. This is heuristic scoring that should be delegated to the model.

---

### mcp/server.ts:531-552 — Keyword-Based Internal Action Classification

**File:** `packages/backend/src/mcp/server.ts`

```typescript
function isInternalAction(action: z.infer<typeof worldGeneratorActionSchema>): boolean {
  const text = `${action.action_type} ${action.summary}`.toLowerCase();
  return [
    'recruit', 'research', 'develop', 'rebuild', 'reconstruction', 'fortif',
    'community', 'aid', 'heal', 'scaven', 'internal', 'consolidat',
    'innovation', 'resource', 'trade', 'smuggling', 'establish', 'patrol',
  ].some((keyword) => text.includes(keyword));
}
```

**Why it violates ZFC:** Keyword-based classification of faction action types as "internal" vs. external. Uses 18 hardcoded keyword strings. This is semantic classification that should be delegated to the model.

---

### system_instruction.ts:681-691 — Keyword-Based Intent Routing

**File:** `packages/backend/src/llm/system_instruction.ts`

```typescript
const characterKeywords: Array<{ kw: string; slot: string }> = [
  { kw: 'talk to', slot: 'target' },
  { kw: 'speak to', slot: 'target' },
  { kw: 'ask', slot: 'target' },
  { kw: 'attack', slot: 'target' },
  { kw: 'kill', slot: 'target' },
  { kw: 'bargain with', slot: 'target' },
  { kw: 'persuade', slot: 'target' },
  { kw: 'convince', slot: 'target' },
  { kw: 'threaten', slot: 'target' },
  ...
];
```

**Why it violates ZFC:** Uses 9+ keyword phrases to route actions into character-targeting vs. gate-checking branches. Intent routing via keyword matching that should be model-delegated.

---

## MEDIUM Severity

### choice_utils.ts:7,27-31 — Generic Choice Fallbacks

**File:** `packages/shared/src/choices/choice_utils.ts`

```typescript
export const GENERIC_CHOICE_FALLBACKS = new Set([
  'continue',
  'look around',
  'wait',
  'nothing happens',
  'nothing',
]);
```

**Why it violates ZFC:** Hardcoded set treating certain choice texts as semantically meaningless. Assumes `continue`, `look around`, `wait` have no meaningful game state effects — but these could be deliberate player choices expressing specific narrative intent.

---

### faction_simulator.ts:1267-1269 — hasSignal Utility with Keyword Arrays

**File:** `packages/backend/src/world/faction_simulator.ts`

```typescript
const hasSignal = (text: string, signals: string[]): boolean =>
  signals.some((sig) => text.toLowerCase().includes(sig.toLowerCase()));
```

Used across 5 companion autonomy modes with keyword arrays:
- `['guard', 'protector', 'paladin', 'sentinel']`
- `['curious', 'scout', 'ranger', 'rogue', 'wander']`

**Why it violates ZFC:** Simple includes-based pattern matching biases companion action selection. Companion behavior is guided by keyword matching rather than model interpretation of narrative context.

---

## LOW Severity (Exempt — Contract Validation)

- `rewardOutcomeClaimed` regex at line 567-571 — structural contract check
- `rollKeywords` check at line 889-898 — structural contract check
- `gateKeywords` at line 752 — borderline (structural gate contract)

---

## Borderline Cases

### story_compactor.ts:73 — Word-Overlap Heuristic

Simple word-overlap heuristic for story resolution. Flagged as borderline — recommended for model delegation.

---

## Related

- [[Harness5LayerModel]] — The evaluation framework used
- [[ZeroFrameworkCognition]] — The ZFC principle being violated
