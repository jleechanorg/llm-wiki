---
title: "Google Drive Upload via rclone + User-Owned Desktop-app OAuth Client"
type: source
tags: [google-drive, rclone, oauth, cli, reference]
date: 2026-08-13
source_file: reference-gdrive-upload-via-rclone-own-client.md
---

## Summary
A working, verified path for headless Google Drive uploads from a Mac terminal: create your own Desktop-app OAuth client in Google API Console with `drive.file` scope, then drive `rclone` against it. Every shared OAuth client on this machine (gcloud's `32555940559`, rclone's leaked `202264815644-…`) blocks `drive.file`; this path avoids them by being user-owned.

## Key Claims
- `rclone` configured with a user-owned Desktop-app OAuth client uploads to Drive headlessly via `rclone config create gdrive drive client_id … client_secret … scope drive.file use_trash false` + `rclone copyto` / `rclone deletefile` / `rclone link`.
- `gcloud auth login` cannot grant Drive scope — the default `gcloud`/`gws` OAuth client has no Drive scopes registered, so Google returns `restricted_client: Unregistered scope(s) in the request: drive.file`. The token cannot be retargeted by adding scopes; you need a different client_id.
- The rclone shared client `202264815644-rt1o1c9evjaotbpbab10m83i8cnjk077.apps.googleusercontent.com` is blacklisted by Google since a 2018 leak (returns `invalid_client`).
- Service-account tokens cannot upload to Drive (no Drive storage quota → `storageQuotaExceeded`).
- Workspace domain-wide delegation is not applicable to personal `@gmail.com` accounts.

## Key Quotes
> "The fix in one line: `rclone config create gdrive drive client_id YOUR_ID client_secret YOUR_SECRET scope drive.file use_trash false` — the refresh token then lives in `~/.config/rclone/rclone.conf` and subsequent uploads are headless."

> "Do NOT run `gcloud auth login jleechan@gmail.com --scopes=drive.file` — the default `gcloud` OAuth client doesn't have Drive scope registered, so re-login just produces the same `restricted_client` block. Worse, this command can corrupt the existing `~/.config/gcloud/legacy_credentials/jleechan@gmail.com/adc.json` if it errors mid-flight."

## Connections
- [[gws-cli]] — Google Workspace CLI; same OAuth-block failure as gcloud; treat as Drive-unusable until proven otherwise
- [[rclone]] — the headless-capable CLI used; supports Desktop-app refresh-token flow with user-owned client_id
- [[gcloud-auth-login]] — anti-pattern: do not use to add Drive scope
- [[workspace-domain-wide-delegation]] — Workspace-only path; not applicable to @gmail.com
- [[google-api-console]] — where the user-owned Desktop-app OAuth client is created
- [[gcs-public-download-link]] — fall-back when Drive workflow isn't needed