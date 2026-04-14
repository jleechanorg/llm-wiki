# Latency Baseline Report: mvp-site-app-dev

**Date:** 2026-03-01
**URL:** https://mvp-site-app-dev-i6xf2p72ka-uc.a.run.app
**Branch:** worktree_load
**Protocol:** HTTP/3 (h3)

## Executive Summary

The dev site has a **41-second cold start page load** vs **737ms warm**. The primary
bottleneck is Cloud Run cold start cascading: a burst of 30+ concurrent resource requests
exceeds `containerConcurrency: 10`, forcing Cloud Run to spin up additional cold instances
for static file serving.

## Baseline Measurements

### Page Load Timing (Browser - Performance API)

| Metric               | Cold Start   | Warm Instance | Ratio   |
|----------------------|-------------|---------------|---------|
| HTML TTFB            | 17,787 ms   | 242 ms        | 73x     |
| DOM Interactive      | 41,139 ms   | 644 ms        | 64x     |
| DOM Complete         | 41,156 ms   | 737 ms        | 56x     |
| Total Page Load      | 41,157 ms   | 737 ms        | 56x     |

### Server-Side (curl, warm instance)

| Metric          | Value    |
|-----------------|----------|
| DNS Lookup      | 1.8 ms   |
| TCP Connect     | 13.6 ms  |
| TLS Handshake   | 33.1 ms  |
| TTFB            | 101 ms   |
| Total           | 102 ms   |
| HTML Size       | 17,077 B |

### Resource Loading (Cold Start)

Top 5 slowest resources during cold start:

| Resource                      | TTFB (ms) | Duration (ms) | Size (KB) |
|-------------------------------|-----------|---------------|-----------|
| fantasy.9094b902.css          | 23,274    | 23,277        | 21.3      |
| pagination-styles.acbb0945.css| 23,136    | 23,139        | 2.3       |
| auth.7b5ef33c.js              | 23,135    | 23,139        | 11.2      |
| api.368776d6.js               | 17,521    | 17,524        | 12.5      |
| app.db40ce1f.js               | 17,411    | 17,507        | 124.7     |

### Resource Summary

| Type | Count | Total Size (KB) | Total Duration (ms) |
|------|-------|-----------------|---------------------|
| JS   | 17    | 208.4           | 148,087             |
| CSS  | 13    | 76.1            | 167,683             |
| API  | 1     | 0.4             | 71                  |
| IMG  | 1     | 103.0           | 152                 |
| ICO  | 1     | 17.1            | 143                 |
| **Total** | **33** | **405 KB** | -               |

## Cloud Run Configuration

```
minScale: 1
maxScale: 6
containerConcurrency: 10
CPU: 1
Memory: 4 Gi
startup-cpu-boost: true
```

Gunicorn: gthread workers, (2*CPU+1) = 3 workers x 4 threads = 12 concurrent requests

## Root Causes

### 1. Cloud Run Cold Start (~18s) - PRIMARY
Container startup (Python imports + Gunicorn fork + fastembed model loading) takes ~18s.
Despite `minScale: 1`, cold instances get created when concurrency limit is exceeded.

### 2. containerConcurrency: 10 Causes Cascading Cold Starts
Browser fires 30+ requests simultaneously over h3. With limit of 10 concurrent requests
per container, Cloud Run routes overflow to new (cold) instances. This is why static
file TTFB is 12-23s even AFTER the HTML loads.

### 3. No Compression
Static files served without gzip/brotli. `app.js` = 127KB raw (est. ~30KB gzipped).
Total 405KB could be ~100KB compressed.

### 4. 30+ Render-Blocking Resources
11 CSS + 17 JS files loaded individually, all render-blocking (no async/defer).

### 5. Flask Serving Static Files (No CDN)
All assets served through Flask `send_from_directory` on Cloud Run.

## Fix Plan

1. Enable gzip compression (Flask-Compress)
2. Increase containerConcurrency to 80
3. Add defer to non-critical scripts
4. Preload critical resources
5. Re-measure after each fix

## Proposed Fixes (PR #5808 — NOT YET DEPLOYED)

### Changes in PR

| Fix | Detail |
|-----|--------|
| flask-compress | Brotli/gzip compression on text responses (CSS, JS, HTML, JSON) |
| containerConcurrency 10 → 80 | Prevents cascading cold starts from resource burst |
| 10 scripts deferred | `defer` on non-critical JS (animation, search, editor, etc.) |
| 4 CSS async-loaded | `media="print" onload` for non-critical CSS only |
| 3 CSS kept render-blocking | loading-messages, planning-blocks, inline-editor (needed at first paint) |
| DNS prefetch + preconnect | For cdn.jsdelivr.net, gstatic.com, identitytoolkit |

### Expected Impact

The primary fix is `containerConcurrency: 10 → 80`. With only 10 concurrent requests
per container, a browser's burst of 30+ resource requests forces Cloud Run to spin up
additional cold instances (each ~18s to start). With 80, all requests route to the
single warm `minScale=1` instance.

**Compression** should reduce transfer size from ~405 KB to ~108 KB (~73% reduction).

### Tradeoffs

- **defer scripts**: Enhancement features (loading-messages, campaign-wizard,
  inline-editor) may initialize slightly after first paint. All cross-script
  references use `if (window.XXX)` guards so no crashes, but features may be
  briefly unavailable on slow connections.
- **Warm page load (DOM Complete)**: May increase slightly due to deferred script
  execution shifting work after DOMContentLoaded. First Contentful Paint improves,
  but total page load may not.

### Validation Required (Post-Deploy)

These measurements must be taken AFTER deploying the PR:

1. **Cold-start comparison** — Scale to 0 instances, measure first request
2. **Warm-to-warm comparison** — Same conditions as baseline (5 curl requests)
3. **Compression verification** — Wire-level size check with `curl --raw`
4. **Functional check** — Verify no FOUC on loading overlay, planning blocks

## Remaining Opportunities

1. **Cold start time** (~18s) still exists for the first container — addressable via
   lazy imports or moving heavy deps (fastembed) to a separate service
2. **CDN for static files** — serve from Cloud Storage/CDN instead of Flask
3. **CSS/JS bundling** — reduce 25 requests to 2-3 bundles
4. **Service worker** — cache static assets for returning visitors
