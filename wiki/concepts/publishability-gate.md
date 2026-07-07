---
title: "Publishability Gate"
type: concept
tags: [publishability-gate, adversarial-verification, swarm, quality-gate]
date: 2026-07-07
last_updated: 2026-07-07
---

## Overview

A publishability gate is a final, whole-artifact verification stage that runs AFTER all writer/producer agents in a multi-agent pipeline have finished, and BEFORE the output is considered done. It exists to close a structural blind spot in adversarial-verification pipelines: verification that only ever scores *candidate claims* (before they're written up) never catches defects introduced at write-time, or defects that only become visible when the finished artifacts are read as a whole.

## Origin

Introduced 2026-07-07 after a cold review of the worldarchitect.ai design-retro-2026-06 docset (~180 adversarial agents across 5 Workflow-tool swarms, PR #8191) found six real defect classes that survived the entire verification chain:

1. Leaked credential/workstation-specific paths and token-shaped strings published in docs.
2. A stale numeric claim in a top-level summary doc that contradicted a correction already made in a per-finding doc (the correction never propagated upstream).
3. A recommendation that violated a hard architectural policy (ZFC-leveling) the evidence/severity/design verify lenses never checked.
4. Multiple sibling docs making contradictory claims about the same fact (route counts: 3 vs "3 of ~8" vs "8 + ~15"), none marked as superseded.
5. A copyable validation recipe that asserted the WRONG expected outcome (green where red was correct for a negative test).
6. The root cause of 1-5: no lane in the pipeline ever re-read the finished, rendered output as a whole.

## Why adversarial verification alone doesn't catch this

Per-finding adversarial verification (multiple independent lenses trying to REFUTE each candidate claim) is excellent at killing false or overstated *claims*, but it runs BEFORE the doc-writer agents produce the actual artifact, and each writer agent is typically restricted to a single output file (for parallel-safety). This means: no agent ever holds two sibling docs in context at once (so cross-doc contradictions are invisible), corrections made to one finding never propagate to summary docs written by a different agent in a different lane, and nothing ever checks the finished markdown against policy rules that aren't among the verify lenses.

## The gate's checklist

1. **Redaction sweep** — regex/grep for machine paths, token-shaped strings, credential patterns; replace with generic placeholders.
2. **Cross-doc consistency** — diff every numeric/factual claim in a summary doc against its per-finding source doc.
3. **Freshness re-baseline** — re-check every present-tense claim against the artifact's current head/version; mark historical evidence explicitly as "at base `<version>`".
4. **Supersession markers** — ensure each finding has exactly one authoritative doc; earlier superseded drafts carry a banner pointing to it.
5. **Policy lens** — check recommendations against hard repo/organizational law not covered by the existing verify lenses.
6. **Recipe validity** — verify every copyable command/acceptance-check states the correct expected outcome.
7. **Mechanical hygiene** — basic diff/whitespace cleanliness checks.

## Related

- [[swarm-orchestration-pattern]] — the multi-agent pipeline pattern this gate is a mandatory final stage of
