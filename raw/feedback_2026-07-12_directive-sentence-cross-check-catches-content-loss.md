---
name: directive-sentence-cross-check-catches-content-loss
description: "Grepping old content for must/never/always/do-not sentences and confirming each survives in the new location is a cheap, effective technique for catching silent content loss during any consolidation/relocation refactor — confirmed successful pattern from this session"
metadata: 
  node_type: memory
  type: feedback
  bead: jleechan-wqz
  originSessionId: 0ffd19bb-d81f-4079-804c-1cea8a822f5b
---

While consolidating fat inline Claude Code command files into thin stubs + canonical skill files (dark-factory migration, ~40+ files this session), the first pass (done manually, without a systematic check) silently dropped two real guardrail passages from `f.md`/`fs.md` during the merge into `dark-factory/SKILL.md` — an `/advice` review caught it, verified by direct diff inspection. After that incident, every subsequent migration (done by me directly or delegated to subagents) was instructed to run a specific technique before finalizing: extract every directive sentence from the OLD content (`grep -n "must\|never\|always\|do not\|Do not\|required\|not allowed"`), then confirm each one's *substance* (not necessarily verbatim wording) survives somewhere in the NEW content, adding it if missing.

**Result**: this cheap technique (a few grep calls plus manual/LLM judgment on substance-equivalence) caught real gaps in several subsequent migrations before they shipped — e.g. a subagent doing the `harness.md` → `harness-engineering` merge found and folded in an `--audit` mode section that existed only in the old command file; another doing `sidekick.md` found two missing hard-limit statements. It essentially never had zero findings on a file over ~80 lines — even "clean" migrations usually surfaced at least one borderline case worth a second look.

**Why it works**: unlike a manual read-through (which pattern-matches on "does this look complete" and is easy to fool with well-organized new content), grepping for directive-marker words forces an exhaustive, mechanical enumeration of every RULE (not just every topic) in the old content, then requires an explicit yes/no on each one surviving — turning "does this look complete" into a checklist that's hard to silently skip.

**How to apply**: make this the default step (not an optional nice-to-have) in ANY content-relocation refactor — moving logic from one file to another, consolidating duplicate docs, migrating a command to a skill, merging two similar files. Cheap enough to run every time; caught real regressions at a rate high enough (multiple hits across ~10 migrations) that skipping it would be a mistake.

See also: [[fat-command-to-thin-skill-migration-regression-test-check]]
