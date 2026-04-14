# PR #3: Add Codex copilot-process skill mirroring Claude copilot workflow

**Repo:** jleechanorg/worldai_claw
**Merged:** 2026-02-17
**Author:** jleechan2015
**Stats:** +119/-0 in 3 files
**Labels:** codex

## Summary
(none)

## Raw Body
### Motivation

- Provide a canonical Copilot-style implementation process and ensure Codex can execute the workflow programmatically rather than leaving TODO steps. 
- Align Codex behavior to the human-readable workflow at `.claude/commands/copilot.md` while making the process runnable by Codex with an executable helper.

### Description

- Add a source workflow document at ` .claude/commands/copilot.md` that enumerates the Copilot process steps and execution rules. 
- Add a Codex skill at ` .codex/skills/copilot-process/SKILL.md` with frontmatter (`name`/`description`) instructing Codex to follow the Claude workflow and to run runnable steps via shell/tool commands. 
- Add an executable helper script at ` .codex/skills/copilot-process/scripts/run-copilot-process.sh` that runs `npm test`, `npm run lint`, and `npm run build` when available and prints `git status`, and make the script executable with `chmod +x`.

### Testing

- Ran `bash .codex/skills/copilot-process/scripts/run-copilot-process.sh` to validate the helper script behavior and detect available npm scripts. 
- Result: the run failed at `npm test` because the backend workspace Jest configuration has no tests (Jest exits with "No tests found"), so the script exited early; lint/build checks would run if corresponding npm scripts exist.

------
[Codex Task](https://chatgpt.com/codex/tasks/task_e_6993d81811ec832f90a6f6eb5ef5fcf2)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Low Risk**
> Documentation and a standalone helper script only; no production code paths or runtime behavior are modified.
> 
> **Overview**
> Introduces a canonical Copilot-style implementation workflow in `.claude/commands/copilot.md`, defining the expected sequence (plan → implement → run checks → review diff → commit/PR) and execution rules.
> 
> Adds a matching Codex skill (`.codex/skills/copilot-process/SKILL.md`) that instructs Codex to follow that workflow and to execute runnable steps via shell commands, plus a helper script (`run-
