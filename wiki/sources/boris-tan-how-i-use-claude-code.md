---
title: "How I Use Claude Code" by Boris Tan
type: source
tags: [boris-workflow, research-first, plan-in-files, annotation-cycle, claude-code, research-phase]
date: 2026-02-01
source_file: https://boristane.com/blog/how-i-use-claude-code/
---

## Summary
Boris Tan describes his 9-month workflow built on one core principle: never let Claude write code until a written plan is reviewed and approved. The workflow has four phases — deep research, detailed planning in markdown, iterative annotation where he adds inline corrections, and finally implementation. By separating planning from execution, he maintains control over architecture decisions and produces better results with less token usage.

## Key Claims
- **"Never let Claude write code until you've reviewed and approved a written plan"** — the foundational rule
- **Research must produce a written artifact** (`research.md`), not verbal summaries — must include words like "deeply," "in great details," "intricacies" or Claude skims function signatures
- **Use own `.md` files** instead of built-in plan mode for full control and persistence
- **Annotation cycle**: open plan in editor, add inline notes (correcting assumptions, rejecting approaches, adding constraints), send Claude back to address them — repeat 1–6 times
- **"Don't implement yet" guard** is essential — explicit instruction to prevent premature implementation
- **Implementation should be "boring"** once the plan is validated
- **Implementation directive**: "implement it all. when you're done with a task or phase, mark it as completed in the plan document. do not stop until all tasks and phases are completed. do not add unnecessary comments or jsdocs. do not use any or unknown types. continuously run typecheck"

## Key Quotes
> "Never let Claude write code until you've reviewed and approved a written plan."

## Key Implementation Directives
1. **Research directive**: "read this folder in depth, understand how it works deeply... when that's done, write a detailed report... in research.md"
2. **Plan request**: "write a detailed plan.md document outlining how to implement this. include code snippets"
3. **Annotation return**: "I added a few notes to the document, address all the notes and update the document accordingly. don't implement yet"
4. **Todo list**: "add a detailed todo list to the plan... don't implement yet"
5. **Implementation command**: "implement it all..."

## Connections
- [[BorisWorkflow]] — the workflow pattern from this source
- [[ResearchFirst]] — mandatory deep-read before planning
- [[PlanInMarkdown]] — persistent .md files over built-in plan mode
- [[AnnotationCycle]] — iterative inline note corrections
- [[DontImplementYet]] — explicit guard against premature code writing
