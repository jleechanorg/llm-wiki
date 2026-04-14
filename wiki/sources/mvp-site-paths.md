---
title: "mvp_site paths"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/paths.py
---

## Summary
Centralized path configuration for WorldArchitect.AI providing single source of truth for all file and directory paths used throughout the application and tests.

## Key Claims
- PathConfig class with base_dir, frontend_dir, test_data_dir
- Validates mvp_site location by checking for main.py
- Eliminates hardcoded path calculations

## Connections
- [[Validation]] — path configuration
