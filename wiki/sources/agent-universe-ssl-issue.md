---
title: "agent-universe.ai SSL Issue"
type: source
tags: [project, memory-file]
date: 2026-06-13
source_file: raw/memory_backfill_2026_06_13/agent-universe-ssl-issue.md
---

## Summary

SSL certificate never provisions for agent-universe.ai despite: DNS A records correctly pointing to Firebase Hosting IPs (216.239.32.x) Cloud Run domain mapping created successfully Status shows "CertificatePending" indefinitely Domain not verified/claimed in Firebase Hosting. Cloud Run can create domain mappings but SSL provisioning requires Firebase Hosting to manage the certificate, which requires domain ownership verification. consensus-ml.ai works because it was set up through Firebase Console with proper domain verification.

## Key Claims

- DNS A records correctly pointing to Firebase Hosting IPs (216.239.32.x)
- Cloud Run domain mapping created successfully
- Status shows "CertificatePending" indefinitely
- `gcloud beta run domain-mappings describe agent-universe.ai` shows `CertificatePending`
- `openssl s_client` shows no certificate served, connection closes immediately
- GoDaddy API returns NOT_FOUND for all requests (credentials not working)
- consensus-ml.ai works correctly via Firebase Hosting
- worldarchitect.ai works correctly (Cloud Run + Firebase Hosting verified)

## Key Quotes

_(No blockquotes in source)_

## Connections

- [[rebase]]
