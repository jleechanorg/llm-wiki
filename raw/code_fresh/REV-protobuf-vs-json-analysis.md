# REV: Protocol Buffers vs JSON for Game State Serialization

**Status:** ANALYSIS
**Priority:** LOW (Optimization - Not Critical)
**Component:** Serialization, Firestore, API
**Created:** 2026-02-15
**Related:** REV-schema-driven-field-access

## Question

Should WorldArchitect.AI migrate from JSON to Protocol Buffers for game state serialization?

**Follow-up:** Would Protocol Buffers be slower than JSON?

**Answer:** NO - Protobuf is 2-10x **FASTER** than JSON, but the ROI is questionable for this use case.

---

## Performance Benchmarks (General)

### Serialization Speed
| Format | Encode Time | Relative Speed |
|--------|-------------|----------------|
| **Protocol Buffers** | 1x | Baseline (fastest) |
| **JSON** | 2-5x | 2-5x slower |
| **JSON (orjson)** | 1.5-3x | Faster than stdlib json |

### Deserialization Speed
| Format | Decode Time | Relative Speed |
|--------|-------------|----------------|
| **Protocol Buffers** | 1x | Baseline (fastest) |
| **JSON** | 3-10x | 3-10x slower |
| **JSON (orjson)** | 2-5x | Faster than stdlib json |

### Size on Wire
| Format | Size | Compression |
|--------|------|-------------|
| **Protocol Buffers** | 1x | Baseline (smallest) |
| **JSON** | 3-10x | 3-10x larger |
| **JSON + gzip** | 1.5-3x | Competitive with protobuf |

**Source:** Industry benchmarks (protobuf.dev, JSON libraries)

---

## WorldArchitect.AI Context Analysis

### Current Architecture

**Serialization Points:**
1. **Firestore persistence** - Game state to/from database (JSON)
2. **LLM API requests** - Game state in prompts (JSON)
3. **Frontend API** - Game state to React app (JSON)
4. **Python internal** - GameState class ↔ dict (Python objects)

**Current Sizes (Estimated):**
- Game state: 50-200KB JSON (narrative-heavy, text content)
- JSON schema: 137KB (schema file itself)
- Story history: 100+ turns × ~500 tokens = 50KB+ text

**Request Frequency:**
- User actions: 1-3 API calls per turn (turn-based game, not real-time)
- Firestore writes: 1 per turn (every 30-120 seconds)
- LLM requests: 1 per turn (Gemini API, 3-10 second latency)

---

## Protobuf Advantages

### 1. Performance (2-10x faster)
```
JSON serialization:   100ms → Protobuf: 20-50ms   (2-5x faster)
JSON deserialization: 150ms → Protobuf: 15-50ms   (3-10x faster)
JSON size:            200KB → Protobuf: 20-60KB   (3-10x smaller)
```

**BUT: Is 100ms serialization the bottleneck?**
- Network latency: 50-200ms (much larger)
- Gemini API latency: 3-10 seconds (1000x larger)
- User think time: 10-60 seconds (10,000x larger)

**Verdict:** Serialization is NOT the bottleneck.

### 2. Schema Enforcement (Compile-Time) ⭐ **STRONGEST ARGUMENT FOR PROTOBUF**

```proto
message GameState {
  required string campaign_id = 1;
  optional PlayerCharacter player_character_data = 2;
  optional CombatState combat_state = 3;
}
```

**Protobuf enforcement is MUCH stronger than JSON Schema:**

| Feature | JSON Schema (Current) | Protocol Buffers |
|---------|----------------------|------------------|
| **Validation time** | Runtime (after serialization) | Compile-time (before code runs) |
| **Invalid data** | ⚠️ Can be serialized (non-blocking warnings) | ❌ Won't compile |
| **Type safety** | ⚠️ Runtime only (dict access) | ✅ Compile-time (generated classes) |
| **IDE support** | ⚠️ Limited (string keys) | ✅ Full autocomplete |
| **Typo detection** | ⚠️ Runtime crash or silent None | ✅ Compile error |

**Example - Typo protection:**
```python
# JSON (current) - typo causes runtime bug
gold = player_character_data.get("resorces").get("gold")  # Typo! Returns None silently

# Protobuf (proposed) - typo caught at compile time
gold = game_state.player_character_data.resorces.gold  # ❌ Compile error: no field 'resorces'
```

**BUT: Critical design conflict with our architecture**

**We INTENTIONALLY made validation non-blocking** (just documented in PR #4534):
- Invalid states generate warnings but don't crash
- Prioritizes gameplay continuity over data integrity
- Users never see errors mid-game due to schema violations

**With Protobuf, we'd face a choice:**

**Option A: Strict enforcement (breaks gameplay)**
```python
# LLM returns invalid state
game_state_proto = GameStateProto()
game_state_proto.player_character_data.level = 999  # Invalid (max 20)
# ❌ Protobuf validator raises exception → User sees error mid-game
```

**Option B: Permissive conversion (loses enforcement benefit)**
```python
# Convert Python dict → Protobuf permissively
game_state_proto = dict_to_proto_lenient(llm_response)  # Use defaults for invalid fields
# ⚠️ Now we're back to non-blocking (same as JSON Schema!)
# Lost the compile-time enforcement benefit
```

**Verdict:** Enforcement benefit is REAL but conflicts with intentional non-blocking design. We'd either:
1. Break gameplay with strict enforcement (bad UX)
2. Use lenient conversion (loses enforcement benefit)

**Alternative: TypedDict + mypy (compromise)**
- Compile-time checking in development (catches typos before runtime)
- No enforcement at boundaries (same as current)
- Much lower migration cost than Protobuf

### 3. Backward Compatibility (Field Evolution)
```proto
message Character {
  optional int32 gold = 1;          // Original field
  optional Resources resources = 2;  // New field (gold moved here)
  reserved 1;                        // Mark gold as deprecated
}
```

**Pros:**
- Field numbers allow safe renames
- Default values for missing fields
- Unknown fields preserved during round-trips

**BUT: We handle this in Python code**
- Migration functions (`_canonicalize_player_gold_in_place`)
- Legacy field handling already implemented
- Schema migration version tracking (SCHEMA_MIGRATION_VERSION)

**Verdict:** Benefit exists but we've already solved this problem.

---

## Protobuf Disadvantages

### 1. Loss of Human Readability
```json
// JSON (human-readable)
{
  "player_character_data": {
    "display_name": "Aragorn",
    "level": 5,
    "resources": {"gold": 150}
  }
}
```

```
// Protobuf binary (not human-readable)
\x0a\x12\x0a\x07Aragorn\x10\x05\x1a\x05\x0a\x03\x08\x96\x01
```

**Impact:**
- **Firestore debugging** - Can't inspect game state in Firebase Console
- **GCP logs** - Can't grep for field values in logs
- **Support tickets** - Can't ask users to copy/paste game state
- **Development** - Can't use `jq` to query state
- **CI/CD** - Can't diff state changes in git (binary files)

**This is CRITICAL for WorldArchitect.AI:**
- Active development (need to debug game state frequently)
- User support (need to inspect failed campaigns)
- Evidence-based testing (TDD requires readable artifacts)

**Verdict:** Major productivity loss. **Dealbreaker.**

### 2. Tooling Fragmentation
```bash
# JSON (universal tooling)
jq '.player_character_data.level' game_state.json
cat game_state.json | grep "Aragorn"
git diff game_state.json  # Works perfectly

# Protobuf (requires special tools)
protoc --decode=GameState game_state.schema.proto < game_state.pb
# No grep, no jq, no git diff
```

**Impact:**
- Need protoc compiler in CI/CD
- Need Python protobuf bindings (extra dependency)
- Need custom debugging tools
- Git diffs show binary blobs (useless)

**Verdict:** Increased complexity with no clear benefit.

### 3. Migration Cost (High)

**Effort estimate:**
- Write .proto schema: 8-12 hours (translate from JSON schema)
- Generate Python bindings: 2-4 hours (protoc setup)
- Migrate serialization points: 12-16 hours (Firestore, API, LLM)
- Update tests: 8-12 hours (binary fixtures, new assertions)
- Update tooling: 4-8 hours (CI/CD, debugging scripts)
- **Total: 34-52 hours (1-1.5 weeks)**

**What do we get?**
- 50-100ms faster serialization (user won't notice)
- Smaller payloads (network is not the bottleneck)
- Loss of debuggability (major productivity hit)

**Verdict:** High cost, low benefit. **Not worth it.**

### 4. Ecosystem Lock-In
- Firestore natively supports JSON (document database)
- Gemini API accepts JSON (not protobuf)
- Frontend expects JSON (REST API standard)
- Would need protobuf ↔ JSON conversion at boundaries (adds latency!)

**Verdict:** Protobuf adds conversion overhead, negating performance gains.

---

## Use Cases Where Protobuf Makes Sense

### ✅ Good Fit (NOT WorldArchitect.AI)
1. **High-frequency APIs** (1000s of requests/sec)
   - Microservices with tight latency budgets (<10ms)
   - gRPC for service-to-service communication
   - Real-time multiplayer games (60 FPS updates)

2. **Mobile apps** (bandwidth-constrained)
   - Cellular data costs matter
   - Battery life (smaller payloads = less radio time)
   - Offline-first apps with sync

3. **IoT devices** (resource-constrained)
   - Limited memory/CPU
   - Low-bandwidth networks
   - Thousands of devices sending telemetry

### ❌ Poor Fit (WorldArchitect.AI)
- **Turn-based game** (1-3 requests per minute, not 1000s/sec)
- **Network-bound** (Gemini API latency >> serialization time)
- **Development velocity matters** (debuggability > optimization)
- **Firestore native JSON** (no protobuf support)
- **Human operators** (need to read game state for debugging)

---

## Hybrid Approach (Protobuf for Internal, JSON for External)

**Theoretically possible:**
- Internal Python: Use protobuf for GameState class
- Firestore writes: Convert protobuf → JSON
- LLM requests: Convert protobuf → JSON
- Frontend API: Convert protobuf → JSON

**Pros:**
- Type safety in Python code
- Fast internal serialization

**Cons:**
- Conversion overhead at every boundary (negates performance gains!)
- Increased complexity (two serialization paths)
- Same debuggability issues (binary in-memory, need conversion to inspect)

**Verdict:** Worst of both worlds. **Don't do this.**

---

## The Schema Enforcement Question (Your Valid Point!)

**You're absolutely right - Protobuf WOULD make schema enforcement easier and stronger.**

### Current Problem (JSON Schema)
```python
# Runtime validation - happens AFTER code runs
def process_llm_response(llm_dict: dict) -> GameState:
    # Code executes with unvalidated data
    gold = llm_dict.get("player_character_data", {}).get("resources", {}).get("gold")
    # Typo "resorces" returns None silently - bug discovered at runtime

    # Validation happens here (too late if code already crashed)
    errors = validate_game_state(llm_dict)  # Non-blocking warnings
    if errors:
        logging_util.warning(f"Schema violations: {errors}")  # Just logs, doesn't crash
```

**Issues:**
- ❌ Typos discovered at runtime (or never, if path returns None silently)
- ❌ No IDE autocomplete for field names
- ❌ Refactoring requires grep + manual verification
- ❌ Tests needed to catch schema violations
- ❌ Non-blocking means invalid data can persist

### Protobuf Solution
```python
# Compile-time enforcement - catches errors BEFORE code runs
def process_llm_response(llm_dict: dict) -> GameStateProto:
    # Convert dict to protobuf (validation happens here)
    game_state = GameStateProto()
    game_state.player_character_data.resources.gold = llm_dict[...]["gold"]
    # Typo "resorces" → AttributeError at assignment (caught immediately)

    # IDE autocomplete shows valid fields
    game_state.player_character_data.  # ← IDE shows: resources, equipment, stats, etc.
```

**Benefits:**
- ✅ Typos caught at development time (IDE/type checker)
- ✅ IDE autocomplete (IntelliSense)
- ✅ Refactoring is safe (rename field → compiler finds all uses)
- ✅ Tests optional (type system catches violations)
- ✅ Can't construct invalid protobuf (enforced by generated code)

### The Dilemma

**We have two conflicting goals:**

1. **Strong schema enforcement** (developer experience, correctness)
   - Catch bugs early (compile-time vs runtime)
   - IDE support (autocomplete, refactoring)
   - Impossible to construct invalid data

2. **Non-blocking validation** (user experience, gameplay continuity)
   - LLM outputs can be malformed (AI makes mistakes)
   - Don't crash user's game mid-session
   - Graceful degradation (use defaults, log warnings)

**Protobuf solves #1 but makes #2 harder.**

### Possible Compromise: Protobuf + Lenient Conversion

```python
def dict_to_proto_lenient(data: dict) -> GameStateProto:
    """Convert dict to protobuf, using defaults for invalid/missing fields."""
    proto = GameStateProto()

    # Use protobuf field defaults for missing/invalid data
    try:
        proto.ParseFromString(json_format.Parse(data))
    except Exception as e:
        logging_util.warning(f"Protobuf conversion failed, using defaults: {e}")
        # Set safe defaults instead of crashing
        proto.campaign_id = data.get("campaign_id", "unknown")
        # ...

    return proto  # Always returns valid protobuf (non-blocking)
```

**Result:**
- ✅ Development: Strong typing, IDE support, refactor-safe
- ✅ Runtime: Non-blocking (defaults used for invalid data)
- ⚠️ Complexity: Need lenient conversion layer
- ⚠️ Loss: Some enforcement benefit lost at boundaries

**This might actually be worth it!** But adds complexity.

---

## Recommendation: STICK WITH JSON (But Consider TypedDict)

### Primary Reasons

1. **Serialization is NOT the bottleneck**
   - Network latency: 50-200ms
   - Gemini API: 3-10 seconds
   - Serialization: ~100ms (negligible)

2. **Debuggability is CRITICAL**
   - Active development (need to inspect game state)
   - Evidence-based testing (TDD requires readable artifacts)
   - User support (need to debug failed campaigns)

3. **Ecosystem compatibility**
   - Firestore native JSON
   - Gemini API expects JSON
   - Frontend expects JSON
   - Universal tooling (jq, grep, git diff)

4. **Already solved the hard problems**
   - JSON Schema validation (PR #4534)
   - Legacy field migration (game_state.py)
   - Schema-driven code generation possible (REV-schema-driven-field-access)

### Optional Optimizations (JSON-Based)

If performance becomes a bottleneck (unlikely):

1. **Use orjson** (2-3x faster than stdlib json)
   ```python
   import orjson
   json_bytes = orjson.dumps(game_state)  # 2-3x faster
   ```

2. **Enable Firestore caching** (avoid redundant reads)

3. **Compress large payloads** (gzip for API responses)

4. **Lazy load story history** (don't send 100+ turns to frontend)

---

## Acceptance Criteria (Do Nothing)

- [x] Document analysis in this bead
- [x] Share with team for awareness
- [ ] Close bead as "Won't Fix" (JSON is the right choice)
- [ ] Revisit if requirements change (e.g., real-time multiplayer added)

---

## Related

- REV-schema-driven-field-access: Generate constants from JSON schema
- PR #4534: Schema Validation Warnings (JSON Schema as source of truth)
- ADR-0003: Unified Game State Schema (JSON-based design)

---

## Benchmarks (If Needed)

To measure actual impact:
```python
import json
import timeit

# Current JSON serialization
json_time = timeit.timeit(
    lambda: json.dumps(game_state.to_dict()),
    number=1000
)
print(f"JSON: {json_time/1000:.2f}ms per serialization")
```

**Expected results:**
- JSON serialization: 50-100ms for 200KB game state
- Network latency: 50-200ms (larger than serialization)
- Gemini API: 3000-10000ms (30-100x larger)

**Conclusion:** Optimizing serialization from 100ms → 20ms saves 80ms per turn. User won't notice (Gemini API dominates latency).

---

## Final Verdict (Revised After Schema Enforcement Discussion)

**Would Protocol Buffers be slower?**
- NO - 2-10x faster for serialization

**Would Protocol Buffers make schema enforcement easier?**
- **YES - Much easier** (compile-time vs runtime, IDE support, impossible to construct invalid data)

**Should we use Protocol Buffers?**
- **MAYBE** - Stronger case than initially assessed, but high migration cost

**Three viable paths forward:**

### Path 1: Stick with JSON + TypedDict (Recommended - Low Effort)
**Effort:** 12-16 hours
```python
# Add TypedDict definitions (generated from JSON schema)
class PlayerCharacterData(TypedDict, total=False):
    resources: ResourcesDict
    equipment: EquipmentDict

# Gradual adoption in code
pc_data: PlayerCharacterData = llm_response["player_character_data"]
gold = pc_data["resources"]["gold"]  # Type-checked, IDE autocomplete
```

**Pros:**
- ✅ Type safety in development (mypy catches typos)
- ✅ IDE autocomplete
- ✅ Low migration cost (add types incrementally)
- ✅ Keep JSON (human-readable, tooling)
- ✅ Non-blocking at runtime (same as current)

**Cons:**
- ⚠️ Runtime strings still hardcoded
- ⚠️ TypedDict can diverge from schema (need codegen)

### Path 2: Protobuf with Lenient Conversion (Best of Both - Medium Effort)
**Effort:** 40-60 hours
```python
# Internal: Protobuf (strong typing)
game_state_proto = dict_to_proto_lenient(llm_response)  # Non-blocking conversion

# Boundaries: JSON (compatibility)
firestore.set(proto_to_json(game_state_proto))
```

**Pros:**
- ✅ Strong schema enforcement (compile-time)
- ✅ IDE autocomplete
- ✅ Refactor-safe
- ✅ Non-blocking at boundaries (lenient conversion)

**Cons:**
- ❌ High migration cost (6-8 weeks)
- ❌ Conversion overhead at boundaries
- ❌ Binary debugging harder (need conversion to inspect)

### Path 3: Full Protobuf + Strict Enforcement (Not Recommended)
**Effort:** 50-80 hours

**Pros:**
- ✅ Maximum type safety

**Cons:**
- ❌ Breaks gameplay (users see errors mid-game)
- ❌ Very high migration cost
- ❌ Loss of debuggability

---

## Recommendation: Path 1 (TypedDict) with Path 2 (Protobuf) Evaluation

**Immediate (Next PR after #4534):**
1. Implement schema-driven field constants (REV-schema-driven-field-access)
2. Add TypedDict definitions (generated from JSON schema)
3. Enable mypy in CI pipeline
4. Gradual adoption in hot paths (game_state.py)

**Future Evaluation (3-6 months):**
- Monitor: How often do schema violations occur in production?
- If frequent: Consider Path 2 (Protobuf with lenient conversion)
- If rare: Path 1 (TypedDict) is sufficient

**Decision criteria:**
- **Schema violations < 1% of turns** → TypedDict sufficient
- **Schema violations > 5% of turns** → Protobuf worth the cost

---

## Status Update

**Status:** ANALYSIS COMPLETE → **OPEN for team discussion**

**Key insight from your question:**
- Schema enforcement IS a legitimate benefit of Protobuf
- Stronger than I initially emphasized
- BUT: Can get 80% of benefit from TypedDict with 20% of effort

**Action items:**
1. [ ] Discuss with team: TypedDict vs Protobuf trade-offs
2. [ ] Measure actual schema violation rate in production
3. [ ] Decide on Path 1 (TypedDict) vs Path 2 (Protobuf) based on data
