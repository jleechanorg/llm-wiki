---
title: "GitHub Path Filter Window"
type: concept
tags: [github-actions, ci, preview-deploy, failure-mode]
sources: [pr-6719-evidence-bloat-preview-skip]
last_updated: 2026-04-30
---

## Summary

GitHub Actions path filters on `pull_request` events can silently skip a workflow when the files that match the workflow's `paths` list fall outside GitHub's changed-file evaluation window. In PR 6719, generated evidence and design-doc files made the PR large enough that preview-triggering files under `mvp_site/` and `scripts/` appeared after the first 300 changed files, so the preview deploy workflow did not schedule for the final head.

## Failure Pattern

- A PR contains hundreds of generated or documentation files.
- A workflow relies on `pull_request.paths` to decide whether to run.
- The first files matching the workflow's path filter appear late in the PR file list.
- The workflow is skipped, so no preview deployment exists for the current SHA.

## Mitigations

- Keep generated evidence bundles out of the production PR when possible.
- Commit deploy-triggering files in a way that path filters can see, or reduce path-filter fragility.
- Add `workflow_dispatch` to preview deploy workflows so operators can force a preview for a specific branch/head.
- Treat rerunning an old workflow as insufficient if it deploys an older SHA.

## Connections

- [[GitHubActions]] - Platform behavior involved in the skip.
- [[EvidenceShaFreeze]] - Current-head evidence and deploy proof need the same SHA discipline.
- [[SkepticGate]] - Green checks do not imply skipped workflows ran.
