---
title: "Rotate Google Cloud service account key"
type: source
tags: ["task", "p1", "bead"]
bead_id: "jleechan-2cm"
priority: P1
issue_type: task
status: open
created_at: 2026-02-19
updated_at: 2026-02-19
created_by: jleechan
source_repo: "."
---

## Summary
**[P1] [task]** Rotate Google Cloud service account key

## Details
- **Bead ID:** `jleechan-2cm`
- **Priority:** P1
- **Type:** task
- **Status:** open
- **Created:** 2026-02-19
- **Updated:** 2026-02-19
- **Author:** jleechan
- **Source Repo:** .

## Description

1. Go to https://console.cloud.google.com/iam-admin/serviceaccounts
2. Find project: infinite-zephyr-487405-d0
3. Find service account: openclaw-chat@infinite-zephyr-487405-d0.iam.gserviceaccount.com
4. Go to Keys tab
5. Delete compromised key (ID: b250f2bbd0f4dc8385432b8db10082383da27576)
6. Add new key → JSON
7. Save new key to ~/.openclaw/googlechat-service-account.json
8. Test Google Chat connection: openclaw channels login googlechat

