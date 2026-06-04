---
name: consulting-server-fixes
description: "Four consulting-server.cjs pitfalls: 302 at root, static asset order, public/ path with .., missing express.json(). IAM gap for Secret Manager."
metadata: 
  node_type: memory
  type: feedback
  bead: jleechan-x7j
  originSessionId: 0847b265-7ef7-433a-881c-56e652b6f853
---

## Context

`agent-universe.ai` is served by Cloud Run service `ai-universe-consulting-v2`,
running `scripts/consulting-server.cjs`. Three user-visible symptoms were fixed
in PR [#466](https://github.com/jleechanorg/ai_universe_frontend/pull/466) on
branch `dev1778450609-react` (commits `f67beae`, `37e9353`, `40591cf`).

## Four bugs and their fixes

### 1. 302 redirect at root (blank white page)

**Bug**: `app.get('/')` and `app.get('/index.html')` both called
`res.redirect('/consulting')`. The consulting Cloud Run service is consulting-only — 
there is no reason to redirect; the root should serve the consulting SPA shell
directly.

**Fix**: Remove both `res.redirect()` handlers. Add a shared `serveConsultingShell`
handler registered at `['/', '/consulting', '/index.html']` plus
`/^\/consulting(\/.*)?$/` (regex needed because Express 5 path-to-regexp dropped
bare `*` wildcards — `'/consulting/*'` throws `PathError: Missing parameter name`).

### 2. JS bundles served as HTML (blank page after 302 fix)

**Bug**: The SPA catch-all middleware ran before any static file handler, so every
request — including `/assets/index-*.js` — returned `text/html`. The browser
silently ignored the HTML when trying to evaluate it as JavaScript; React never
mounted.

**Fix**: Register `express.static(path.join(__dirname, 'dist'), { index: false })`
**before** the SPA catch-all. `index: false` prevents `dist/index.html` from being
auto-served for directory requests (that's the catch-all's job).

**Order matters**:
```
app.use(express.static('public'));          // public assets (headshot.jpg etc.)
app.use(express.static('dist', {index:false})); // React bundles ← must be BEFORE catch-all
app.get(['/', '/consulting', ...], serveShell);  // SPA catch-all
app.use((req, res) => serveShell(req, res));     // fallback catch-all
```

### 3. `public/` path with `..` pointed at wrong directory

**Bug**: `path.join(__dirname, '..', 'public')` was written assuming the script
lives one level deep. In the production Docker image the structure is:
```
/app/
  consulting-server.cjs   ← __dirname = /app
  public/
  dist/
```
`__dirname + '..'` = `/` (root), not `/app`. `public/` never existed at `/`.

**Fix**: Drop the `..`: `path.join(__dirname, 'public')`.

### 4. `/api/contact` body always `undefined` (400 on every submission)

**Bug**: `consulting-server.cjs` registered the `/api/contact` POST handler but
never added a body-parser middleware. `req.body` was always `undefined`, so the
`const { name, email, ... } = req.body || {}` destructuring fell back to `{}`
and the handler always returned `400 "name, email, and message are required"`.

**Fix**: Add `app.use(express.json())` after the morgan logger and before any
route handlers.

## IAM gap for Secret Manager

**Bug**: The compute service account
(`754683067800-compute@developer.gserviceaccount.com`) lacked
`roles/secretmanager.secretAccessor` on the `email-pass` secret. Even though the
Cloud Run revision was deployed with `--set-secrets="EMAIL_PASS=email-pass:latest"`,
the mount failed silently and `process.env.EMAIL_PASS` was `undefined` in the
container.

**Fix**:
```bash
gcloud secrets add-iam-policy-binding email-pass \
  --member="serviceAccount:754683067800-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor" \
  --project=ai-universe-2025
```
Then redeploy the service.

**Verification**: `POST /api/contact` returns `{"success":true}`.
Gmail message `19e941a2a5b2dea6` (`[Consulting] New inquiry from JEFFREY LEE CHAN`)
confirms end-to-end delivery.

## Reusable pattern

When building a standalone Express 5 SPA server:
1. Never use bare `*` in route strings — use regexes for wildcards.
2. Register all `express.static()` handlers before any SPA catch-all.
3. Paths relative to `__dirname` are container-layout-sensitive — always verify in Dockerfile.
4. Add `express.json()` (or `express.urlencoded()`) before any POST handler that reads `req.body`.
5. For Secret Manager bindings in Cloud Run: grant `secretmanager.secretAccessor` to the compute SA **before** deploying the secret binding, not after.

## References

- PR [#466](https://github.com/jleechanorg/ai_universe_frontend/pull/466)
- Commits: `f67beae`, `37e9353`, `40591cf`
- Service: `ai-universe-consulting-v2` (project `ai-universe-2025`, region `us-central1`)
- Bead: `jleechan-x7j` (closed)
