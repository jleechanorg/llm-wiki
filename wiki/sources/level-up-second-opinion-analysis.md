---
title: "Level-Up Second Opinion Analysis"
type: source
tags: [level-up, architecture, second-opinion, ai-feedback]
date: 2026-04-14
source_file: /tmp/secondo_levelup_analysis.md
---

## Summary
Real multi-model AI second opinion on the Level-Up Engine v4 design (Cerebras primary + Gemini 3 Flash + Perplexity Sonar Pro). All 3 models confirmed the single-responsibility separation is correct, the double-touch bug analysis is accurate, and the "What Moves Where" migration table is sound. Five edge case warnings were identified requiring explicit coverage: zero/negative XP guards, multiclass XP total-level rule, level 20 cap, rapid polling idempotency, and streaming partial JSON handling.

## Key Claims

- **SRP Separation ✅**: llm_parser (thin coordinator), game_state (pure math), rewards_engine (canonicalizer), world_logic (modal wrapper) — all 3 models confirm correct Clean Architecture layering
- **Double-touch bug ✅**: v4 correctly identified and resolved — both streaming and non-streaming now route through _canonicalize_core()
- **Off-by-one bugs**: No obvious off-by-one errors remain in XP threshold calculation; modal-injection index logic is a soft edge case
- **What Moves Where**: Migration table is sound — one gap noted: missing "experience overflow flag" entry
- **Idempotency guard**: Added but no explicit versioning — recommend canonicalisation_version field
- **XSS risk**: Modal injection returns raw strings — client-side sanitization needed (bleach/markdown)

## Key Warnings (5 Edge Cases)

| Warning | Detail |
|---------|--------|
| Zero/negative XP guard | Guard xp_gained >= 0; negative = no-op + warning log |
| Multiclass XP total-level rule | Must use total_level = sum(class_levels), not class level |
| Level cap 20 | Clamp resolved_target_level <= 20, return max_level flag |
| Rapid polling idempotency | Polling <100ms can cause duplicate emission if idempotency is broken |
| Streaming partial JSON | Parser must handle partial JSON fragments during streaming to avoid UI stutter |

## Security Concerns

- **Input validation**: Enforce strict `extra = "forbid"` in Pydantic schema + 16KB max byte size
- **Idempotency versioning**: Add `canonicalisation_version` field to reject old payloads
- **XSS in modals**: Escape all user-visible strings client-side or use sanitized markdown
- **Timing side-channels**: O(1) loops — no immediate action needed

## Sources
- [martinfowler.com LayeredArchitecture](https://martinfowler.com/bliki/LayeredArchitecture.html)
- [Roll20 SRD: Experience Points](https://roll20.net/compendium/dnd5e/Experience%20Points%20and%20Level%20Advancement#content)
- [OWASP Double Submit Cookie](https://owasp.org/www-community/Double_Submit_Cookie)

## Connections
- [[LevelUpCodeArchitecture]] — v4 design this reviewed
- [[SingleResponsibilityPipeline]] — confirmed correct SRP
- [[RewardsEngineIdempotency]] — idempotency is critical for DeferredRewardsProtocol
- [[LevelUpMechanics]] — zero XP guard and level cap needed
- [[DefensiveNumericConversion]] — DNC pattern for malformed LLM output
