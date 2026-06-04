# Consulting Server Express.js Fixes (agent-universe.ai)

**Date**: 2026-06-04  
**Project**: ai_universe_frontend  
**PR**: https://github.com/jleechanorg/ai_universe_frontend/pull/466  
**Bead**: jleechan-x7j (closed)

## Summary

Four bugs in `scripts/consulting-server.cjs` caused `agent-universe.ai` to serve
a blank white page and reject every contact form submission. All four were fixed
in PR #466 (commits `f67beae`, `37e9353`, `40591cf`).

## Bug 1 — 302 redirect at root

`app.get('/')` redirected to `/consulting`. For a consulting-only service, the
root should serve the SPA shell directly (200, not 302).

**Pattern**: Never redirect a path to itself on a single-purpose server.

## Bug 2 — `express.static(dist)` registered after SPA catch-all

The catch-all returned `text/html` for `/assets/*.js` requests. Browsers silently
ignore HTML when evaluating JavaScript; React never mounted.

**Pattern**: Always register `express.static()` handlers **before** any catch-all
route. Use `{ index: false }` on the `dist` handler to prevent auto-serving
`dist/index.html` — let the explicit catch-all do that.

## Bug 3 — `public/` path with `..`

`path.join(__dirname, '..', 'public')` assumed the script is one level deep. In
the Docker image the layout is flat: `consulting-server.cjs` and `public/` are
siblings. The `..` made the path point at `/` (root) instead of `/app`.

**Pattern**: Always match static path assumptions to the actual Dockerfile layout.

## Bug 4 — No body parser before `/api/contact`

`req.body` was always `undefined`. The handler always returned 400.

**Pattern**: Add `app.use(express.json())` before any route that reads `req.body`.

## IAM gap — Secret Manager accessor missing

`--set-secrets="EMAIL_PASS=email-pass:latest"` silently fails if the compute
service account (`754683067800-compute@developer.gserviceaccount.com`) lacks
`roles/secretmanager.secretAccessor` on the secret. Grant it before deploying.

## Express 5 note — no bare `*` in route strings

`'/consulting/*'` throws `PathError: Missing parameter name at index 13` in
Express 5. Use a regex: `/^\/consulting(\/.*)?$/`.

## Verification

`POST /api/contact` → `{"success":true}`.  
Gmail message `19e941a2a5b2dea6` (`[Consulting] New inquiry from JEFFREY LEE CHAN`).
