---
name: Canonicalize world_logic cooldown stripping fields
description: Use firestore_service authoritative LW field set in world_logic cooldown strip logic to prevent drift from canonical living-world schema changes
bead: rev-247t8
type: feedback
---

- **Date**: 2026-05-08
- **Severity**: low runtime risk / high maintainability risk
- **Context**:
  - In `mvp_site/world_logic.py`, non-trigger turn cooldown handling used duplicated hardcoded tuples of living-world fields in two places: pre-persistence stripping and response-only stripping.
  - `mvp_site/llm_parser.py` was already using `firestore_service._AUTHORITATIVE_LIVING_WORLD_FIELDS`.
- **Finding**:
  - Duplicated literals could diverge from the canonical authoritative living-world field set and cause inconsistent stripping behavior over time.
- **Fix**:
  - Replaced both hardcoded tuples with iteration over `firestore_service._AUTHORITATIVE_LIVING_WORLD_FIELDS`.
  - Kept existing restore/purge logic and guard checks unchanged.
- **Verification**:
  - Confirmed both cooldown blocks now reference `firestore_service._AUTHORITATIVE_LIVING_WORLD_FIELDS`.
  - Current working tree SHA: `9350cef1f58fdabe9d9eea27855b8dd737a247b6`.
- **Reusable pattern**:
  - Prefer canonical field source-of-truth constants in `firestore_service` for all LW field strips/restores.
  - Avoid local duplicate tuples in `world_logic.py` and other call sites unless truly divergent.
- **References**:
  - Working files: `mvp_site/world_logic.py`
  - Canonical field source: `mvp_site/firestore_service.py`
  - Related PR history: merged work in PR stack around `#6837`
