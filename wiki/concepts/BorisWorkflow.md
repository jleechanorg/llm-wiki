---
title: "Boris Workflow"
type: concept
tags: [boris, research-first, plan-in-markdown, annotation-cycle, implementation-directive]
date: 2026-02-01
source: [[boris-tan-how-i-use-claude-code]]
---

## Definition
A four-phase workflow built on the principle: never let Claude write code until a written plan is reviewed and approved. Phases: Research → Plan in .md → Annotation cycle → Implementation.

## Core Principle
> "Never let Claude write code until you've reviewed and approved a written plan."

## Phase 1: Research (Mandatory)
- Output: `research.md` (>50 lines)
- Must use words like "deeply," "in great details," "intricacies" — otherwise Claude skims function signatures
- If research is wrong, plan is wrong, implementation is wrong

## Phase 2: Plan in Markdown
- Use own `.md` files, not built-in plan mode
- Full control, editable in editor, persists as a real artifact

## Phase 3: Annotation Cycle
- Open plan in editor, add inline notes (correcting assumptions, rejecting approaches, adding constraints)
- Send Claude back to address notes — repeat 1–6 times
- Explicit "don't implement yet" guard is essential

## Phase 4: Implementation
Once plan is validated:
```
implement it all. when you're done with a task or phase, mark it as completed
in the plan document. do not stop until all tasks and phases are completed.
do not add unnecessary comments or jsdocs. do not use any or unknown types.
continuously run typecheck to make sure you are not introducing new issues.
```

## Connections
- [[ResearchFirst]] — mandatory deep-read before planning
- [[PlanInMarkdown]] — persistent .md files over built-in plan mode
- [[AnnotationCycle]] — iterative inline note corrections
- [[DontImplementYet]] — explicit guard against premature code writing