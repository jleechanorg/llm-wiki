---
title: "JeffreyCommunicationStyle"
type: concept
tags: [jeffrey, communication, terse, style]
sources: [user-preferences-patterns-learnings]
last_updated: 2026-04-09
---

# Jeffrey's Communication Style

Based on 27,923 actual user messages.

## Core: Extremely Terse

Short, direct bursts. No pleasantries, no filler, no "thanks".

## Real Message Examples

- "no thats wrong" — direct rejection
- "ok continue" — acknowledgment + direction
- "fix the stuck ones" — imperative
- "continue work" — direct command
- "assess open PRs" — single-word verb + noun
- "Reply with exactly OK." — rigorous control
- "Reply OK" — minimal acknowledgment
- "nudge worker" — ultra-condensed
- "investigate and root cause" — investigation
- "what does it prove?" — skeptical question
- "are the AO workers doing work?" — pointed question
- "check Pr now" — inspection command

## Communication Modes

### Direct Imperatives
Single verbs or verb phrases — no politeness markers.

### Confirmation/Control
"Reply with exactly OK." — controls exact response format for testing/automation.

### Pointed Questions When Confused
"what does this have to do with...", "is this true?", "what does it prove?"
He won't pretend to understand — he'll call it out.

### Slash Command Heavy
/copilot, /polish, /integrate, /antig, /fake, /loop, /fixpr, /er — constantly used.

### Corrections
"no thats wrong", "no thats not the default openclaw model"
Non-negotiable.

## What Jeffrey Does NOT Do

- No pleasantries: "please", "thanks", "sorry"
- No filler: "I think", "maybe", "it seems like"
- No hedging: "might", "could be", "perhaps"
- No greeting at session start: "hi", "hey", "how are you"
- No wrap-up pleasantries after approval

## Signature: 🦾

Appears at end of messages — mechanical arm, fitting for someone who builds AI agents.

## Typical Session Flow

1. Direct command or slash command — no greeting
2. Inspect state — gh pr view, ao status, check Pr now
3. Issue specific, actionable commands
4. Iterate inspection/direction until satisfied
5. "ok", "merge", "push", or silent — no wrap-up

## Expectations From AI Agents

- No speculation: no fabricating, no "let me wait"
- Cite concrete file:line issues
- Execute, not narrate
- Minimal changes, existing files first
- Tests pass before claiming done
- Handle feedback loops: fix CodeRabbit items then push
