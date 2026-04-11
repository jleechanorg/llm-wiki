---
title: "PR #16: feat: Add automated PR preview deployment with github-actions-deploy"
type: source
tags: []
date: 2025-10-02
source_file: raw/prs-/pr-16.md
sources: []
last_updated: 2025-10-02
---

## Summary
Implements automated PR preview deployments using the `github-actions-deploy` PyPI package with VPC-SC support and comprehensive PR commenting.

### 🚀 Key Features
- **PyPI Package Integration**: Uses `github-actions-deploy` v0.1.0 (cleaner than custom scripts)
- **VPC-SC Compatible**: Async Cloud Build prevents log streaming issues in CI
- **Automatic PR Comments**: Build status with service URLs
- **Organization Secret**: Shared `GCP_SA_KEY` across repos

### 📦 What's Included
1. **GitHub Work

## Metadata
- **PR**: #16
- **Merged**: 2025-10-02
- **Author**: jleechan2015
- **Stats**: +139/-0 in 2 files
- **Labels**: none

## Connections
