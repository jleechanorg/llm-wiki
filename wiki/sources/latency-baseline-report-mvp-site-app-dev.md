---
title: "Latency Baseline Report: mvp-site-app-dev"
type: source
tags: [cloud-run, latency, performance, cold-start, flask, gcp]
source_file: "raw/llm_wiki-raw-worldarchitect.ai-latency-baseline-report.md-69cd14ac.md"
sources: []
last_updated: 2026-04-07
---

## Summary
Performance analysis of mvp-site-app-dev showing 41-second cold start page load vs 737ms warm. Primary bottleneck is Cloud Run cold start (~18s) cascading when 30+ concurrent resource requests exceed containerConcurrency:10, forcing new cold instances to spin up.

## Key Claims
- **41s cold start, 737ms warm** — 56x performance difference
- **Cloud Run cold start ~18s** — Python imports + Gunicorn fork + fastembed model loading
- **containerConcurrency: 10 causes cascading cold starts** — browser fires 30+ requests, exceeds limit, forces new cold instances
- **No compression** — 405KB transferred raw vs ~108KB compressed
- **25 render-blocking resources** — 11 CSS + 17 JS loaded synchronously

## Key Measurements

### Page Load Timing
| Metric | Cold Start | Warm Instance | Ratio |
|--------|-----------|---------------|-------|
| DOM Complete | 41,156 ms | 737 ms | 56x |

### Top 5 Slowest Resources (Cold)
| Resource | TTFB | Duration |
|----------|-----|----------|
| fantasy.css | 23,274 ms | 23,277 ms |
| pagination-styles.css | 23,136 ms | 23,139 ms |
| auth.js | 23,135 ms | 23,139 ms |
| api.js | 17,521 ms | 17,524 ms |
| app.js | 17,411 ms | 17,507 ms |

## Root Causes
1. **Cloud Run Cold Start (~18s)** — PRIMARY bottleneck
2. **containerConcurrency: 10** — overflow triggers new cold instances
3. **No compression** — 405KB transferred raw
4. **30+ render-blocking resources** — all block first paint

## Proposed Fixes (PR #5808)
1. Enable gzip/brotli compression (Flask-Compress)
2. containerConcurrency 10 → 80
3. defer on non-critical scripts
4. Preload critical resources

## Connections
- [[Orchestration Architecture Research]] — uses Cloud Run for deployment
- [[Webhook Pipeline Operator Runbook]] — same Cloud Run infrastructure