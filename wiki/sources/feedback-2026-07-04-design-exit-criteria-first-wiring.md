---
title: "Design exit-criteria-first wiring — /design + brainstorming batch-decision review (2026-07-04)"
type: source
tags: [design-process, exit-criteria, adversarial-review, skills, harness]
date: 2026-07-04
source_file: raw/feedback_2026-07-04_design_exit_criteria_first_wiring.md
---

## Summary

After a rigorous-looking draft definition-of-done for the dark-factory daemon cutover was shown
to contain 20+ adversarially-findable loopholes (3-reviewer hostile /advice pass), the design
toolchain itself was rewired so exit criteria come first everywhere: `/design` (command +
design-doc + design + spec-design-docs skills) now runs a Phase 0 that invokes superpowers
brainstorming, writes exit criteria before any spec content, and uses a mandatory batch-decision
mode — the model self-answers all brainstorming questions with recommendations and presents one
consolidated review table instead of serial questioning. The brainstorming skill (plugin cache
5.0.7 + tessl mirror) now requires exit-criteria exploration and specs leading with an Exit
Criteria section.

## Key Claims

- A spec written before its done-criteria optimizes proxies (Goodhart); exit criteria must be
  the FIRST section of the no-code spec, not an afterthought.
- Game-proof exit-criteria bar: binary, executable, externally anchored; implementer-authored
  artifacts corroborating never sufficient; verifier reproduces rather than inspects; mock/
  dry-run satisfaction = FAIL; default verdict FAIL. Canonical charter:
  `~/projects/dark-factory/docs/cutover-exit-criteria.md` (R1–R6 + X1–X10, on main @7152469).
- Serial one-by-one questioning wastes operator attention: batch-decision mode (recommend
  everything, review once) is the /design contract now.
- Plugin-cache skill edits are volatile: the superpowers 5.0.7 cache path is version-keyed and
  a plugin update ships a fresh SKILL.md without the edits. Durable mirror:
  `~/.claude/skills/tessl__brainstorming/SKILL.md`; re-apply per bead jleechan-0bgw.

## Key Quotes

> "Attack your own DoD with hostile reviewers before trusting it — cheaper than discovering the
> loophole after a false PASS."

## Connections

- [[ExitCriteriaFirst]] — the design principle this wiring institutionalizes
- [[AdversarialReview]] — the 3-reviewer hostile pass that motivated it
- [[DarkFactory]] — origin project; cutover charter is the canonical example
- [[GoodhartsLaw]] — why proxy-anchored criteria fail against optimizing agents
- [[ClaudeSkills]] — plugin-cache volatility vs user-scope durability
