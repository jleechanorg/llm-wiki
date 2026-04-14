---
title: "mvp_site start_flask"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/start_flask.py
---

## Summary
Standalone Flask app starter for run_ui_tests.sh. Resolves import path issues when running in subshells. Runs Flask app on PORT env var (default 8088) with FLASK_DEBUG env var control.

## Key Claims
- Standalone Flask starter for test scripts
- PORT env var (default 8088)
- FLASK_DEBUG env var (default True)
- Resolves Python path issues for subshell execution

## Connections
- [[Main]] — Flask app startup
