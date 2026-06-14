---
title: "consulting-server.cjs Four Pitfalls (PR #466)"
type: source
tags: ["consulting-server", "express", "ai-universe-frontend", "pr-466", "feedback"]
date: 2026-06-04
source_file: feedback_2026-06-04_consulting-server-fixes.md
---

## Summary
`agent-universe.ai` served by Cloud Run `ai-universe-consulting-v2` running `scripts/consulting-server.cjs`. Four user-visible symptoms fixed in PR #466 on branch `dev1778450609-react`.

## Key Claims
- 1. 302 redirect at root — `app.get('/')` and `app.get('/index.html')` both called `res.redirect('/consulting')`. Remove both; add shared `serveConsultingShell` registered at multiple paths
- 2. JS bundles served as HTML — SPA catch-all middleware ran BEFORE any static file handler. Register `express.static(...)` BEFORE the SPA catch-all
- 3. `public/` path with `..` pointed at wrong directory — `__dirname + '..'` = `/` (root), not `/app`. Drop the `..`
- 4. `/api/contact` body always `undefined` — no `express.json()` body-parser middleware added
- IAM gap for Secret Manager: compute SA lacked `roles/secretmanager.secretAccessor` on `email-pass` secret

## Key Quotes
> When building a standalone Express 5 SPA server: never use bare `*` in route strings; register all express.static() handlers before any SPA catch-all; paths relative to __dirname are container-layout-sensitive; add express.json() before any POST handler

## Connections
- [[ConsultingServer]] — entity
- [[Express5Patterns]] — concept
