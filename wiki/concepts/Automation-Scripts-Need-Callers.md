---
title: "Automation Scripts Need Callers"
type: concept
tags: [jeffrey, oracle, automation, PR-review]
sources: [jeffrey-oracle]
last_updated: 2026-04-10
---

New automation scripts require two things before they are considered legitimate: a body description accurately explaining what the script does, and a caller or trigger visible in the diff (a workflow step, cron entry, or parent script that is itself auto-triggered). A bare script file with no workflow wiring and no explanation is orphaned code — it exists on disk but has no execution path, which means it will never run and will silently rot.

This rule applies to new scripts and to extensions of existing scripts: adding a new script invocation to an automation workflow requires the caller to be visible in the diff. Adding `generate_evidence_bundle.sh` to skeptic-cron.yml without showing that invocation step is the same violation as adding a standalone script with no caller at all.

Skill documents are a related category: a skill doc is the protocol definition, and a slash command in `.claude/commands/` that invokes it IS a valid caller. Both being present in the same repo satisfies the "who calls this?" criterion. Skill docs without any integration pathway (neither slash command caller nor hook nor parent script) are orphaned documentation. Observed across batches 1, 5, and 6: PR #6176 flagged `bypass-claims.md` with no caller, PR #6168 added two evidence scripts with no visible workflow wiring, and PR #6187 added a 465-line script with no visible caller. [[jeffrey-oracle]]
