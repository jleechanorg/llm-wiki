---
title: "evidence-review triple-duplicate dead code — /green integration silently unused for months"
type: source
tags: [claude-code, skills, evidence-review, harness-hygiene]
date: 2026-07-07
source_file: raw/feedback_2026-07-07_evidence_review_triple_duplicate_dead_code.md
---

## Summary

Three files all declared `name: evidence-review` in frontmatter across different scopes/formats. The command that's supposed to load this skill (`/er`) had a file-resolution script that never checked the path where the newest content actually lived, so a real feature (the `/green` two-tier PRODUCTION/NON_PRODUCTION integration, dated 2026-07-02) was silently dead code from the moment it was written until discovered during an unrelated skill-usage audit.

## Key Claims

- Two or more files sharing the same frontmatter `name:` across scopes (user, repo, plugin) is itself a smell worth checking whenever investigating "why doesn't this recent change seem to take effect."
- A skill/command update living in the "wrong" file relative to what the loader actually checks fails silently — no error, no warning.
- Fix: trace the actual resolution/loader logic and confirm the physical path it reads before assuming "the newest edit wins."

## Connections

- [[archive-not-delete-and-verify-before-prune]] — discovered in the same cleanup pass, same root cause class (trusting assumptions about file state without verifying)
