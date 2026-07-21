---
name: usage-signal-substring-count-invalid
description: "Raw substring counting of command/skill names across session history is NOT a valid usage-frequency signal — Claude Code's own skill-catalog system-reminder repeats every name in nearly every turn"
metadata: 
  node_type: memory
  type: feedback
  bead: jleechan-q0w
  originSessionId: 0ffd19bb-d81f-4079-804c-1cea8a822f5b
---

During the thin-skill-command-migration (2026-07-12), I needed to prioritize which of ~60 Claude Code slash commands were worth careful migration effort vs. which were dead/unused. Two methodologies were tried:

1. **Exact tag match** — grep for `<command-name>/X</command-name>` across `~/.claude/projects/*/*.jsonl` and `~/.claude-wa/projects/*/*.jsonl`. This is reliable: it only matches when a human actually typed `/X` and the harness recorded the invocation. Correctly identified `harness`(54), `sidekick`(48), `es`(24), `research`(18), `learn`(14), `swarm`(6), `fable`(6) as genuinely used.

2. **Raw substring count** — `content.count("commandname")` across the same files. This returned 10,000–184,000 "hits" for every single command name, including ones with zero real invocations (`converge`, `exportcommands`, `reviewdeep`, etc.). Traced a sample hit and found it came from the skill-catalog boilerplate text that Claude Code injects as a system-reminder after nearly every tool call — every command/skill name+description in the entire catalog gets repeated dozens of times per session, dwarfing any real signal by 3-4 orders of magnitude.

**Why**: Method 2 conflates "this string appears in the transcript" with "the user invoked this." The skill-catalog reminder alone guarantees every registered command name appears hundreds of times per session regardless of use.

**How to apply**: When measuring real usage frequency of a Claude Code command/skill from session history, use ONLY the exact `<command-name>/X</command-name>` tag match (or equivalent structured invocation marker). Never use a raw string/substring count as a usage proxy — verify by sampling a match's surrounding context before trusting any usage-frequency claim built from raw counts. If a "usage count" claim can't cite the structured tag match, treat it as unverified.

One exception found this session: a command (`/fixpr`) showed 0 tag-match hits but had strong *prose evidence* of real use — a roadmap doc explicitly stated "external automation (fixpr/codex) is already carrying a third of the fleet," describing the `copilot-fixpr` subagent type. That's real evidence (human/agent-authored description of observed behavior), distinct from a noisy substring count. Independent corroborating evidence (docs, beads, agent-type registries) is a legitimate override to a 0-hit tag-match result; a raw substring count is not.

See also: [[fat-command-to-thin-skill-migration-regression-test-check]]
