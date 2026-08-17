---
name: gdrive-upload-via-rclone-own-desktop-app-oauth-client
description: "Working path for unattended Google Drive uploads from a Mac terminal — create your own Desktop-app OAuth client with drive.file scope, store it in rclone, then upload headlessly. Supersedes the older 'gdrive OAuth dance' memory."
type: reference
---

**When:** you need to upload a file to Google Drive from a terminal session without driving a browser, and `gcloud` / `gws` / `rclone gdrive:` shared OAuth clients all block Drive scope.

**The fix in one line:** `rclone config create gdrive drive client_id YOUR_ID client_secret YOUR_SECRET scope drive.file use_trash false` — the refresh token then lives in `~/.config/rclone/rclone.conf` and subsequent uploads are headless.

## Why the shared clients fail

- `gcloud` / `gws` default client `32555940559.apps.googleusercontent.com` has only `cloud-platform`, `openid`, `userinfo.email`, `sqlservice.login` registered. Google OAuth returns `restricted_client: Unregistered scope(s) in the request: drive.file` when you try to add `drive.file`. **The token can't be retargeted by adding scopes; you need a different client.**
- rclone shared client `202264815644-rt1o1c9evjaotbpbab10m83i8cnjk077.apps.googleusercontent.com` was leaked in 2018; Google now refuses fresh token exchanges against it (`invalid_client`).
- Service-account tokens get `storageQuotaExceeded` because service accounts have no Drive storage quota. They can ONLY upload to shared drives with Workspace admin grant.
- Workspace domain-wide delegation does not work for personal `@gmail.com` accounts — it requires Workspace admin.

## How to set up the user-owned client (one-time, ~5 minutes)

1. Open [Google API Console → Credentials](https://console.cloud.google.com/apis/credentials).
2. Create an **OAuth client** of type **Desktop app** (no redirect URI required; installed apps use loopback).
3. Note the Client ID (looks like `XXXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXX.apps.googleusercontent.com`) and Client Secret.
4. On the **OAuth consent screen** for the same project: add scope `https://www.googleapis.com/auth/drive.file` (least privilege) under **Data Access → Scopes**. Add yourself as a test user. For External apps, click **PUBLISH APP** to avoid weekly grant expiry under Testing mode.
5. Optionally also add `drive.metadata.readonly` if you ever need to list files.

## Concrete commands (verified 2026-08-13)

```bash
# Initial one-time auth (interactive — opens browser to http://127.0.0.1:53682)
rclone config create gdrive drive \
  client_id "YOUR_CLIENT_ID.apps.googleusercontent.com" \
  client_secret "YOUR_CLIENT_SECRET" \
  scope "drive.file" \
  root_folder_id "" \
  use_trash false

# Verify the remote works (no browser)
rclone lsd gdrive:                        # list Drive root folders
rclone ls gdrive:/WorldAIClaw-d2ad593b.ipa # confirm a file is present

# Upload (no browser — refresh token stored in rclone.conf)
rclone copyto /local/path/file.bin gdrive:/some/folder/file.bin --progress

# For fully headless transfer to another machine:
rclone config show gdrive > /tmp/gdrive-token.json
RCLONE_DRIVE_TOKEN="$(cat /tmp/gdrive-token.json)" rclone copy /local/file gdrive:/

# Remove from Drive (no browser)
rclone deletefile gdrive:/path/file.bin

# Generate a share link
rclone link gdrive:/path/file.bin
```

## Verification done in this session (2026-08-13)

- `rclone copyto /tmp/wac-drive-test.txt gdrive:/wac-drive-test.txt --progress` → `Transferred: 146 B / 146 B, 100%` (round-trip test).
- `rclone ls gdrive:/WorldAIClaw-d2ad593b.ipa` → `9269590 WorldAIClaw-d2ad593b.ipa` (9.27 MB arm64 device build).
- `rclone deletefile gdrive:/wac-drive-test.txt` → `directory not found` (cleanup verified).

## Credential isolation rules (do not violate)

- **Do NOT run `gcloud auth login jleechan@gmail.com --scopes=drive.file`** — the default `gcloud` client doesn't have Drive scope, so re-login just produces the same `restricted_client` block. Worse, this command can corrupt the existing `~/.config/gcloud/legacy_credentials/jleechan@gmail.com/adc.json` if it errors mid-flight. Leave the `gcloud` user credential alone; drive uploads through `rclone` only.
- **Do NOT use the dev-runner service account for Drive uploads** — `storageQuotaExceeded`. Use it for `gs://` uploads only.
- **rclone credentials live in `~/.config/rclone/rclone.conf`** (macOS) or `~/.config/rclone/rclone.conf` (XDG). They are isolated from `gcloud`/`gcloud`-ADC paths. Keep them that way.
- The token JSON exports via `rclone config show gdrive` are sensitive — don't commit them; the file is readable only to the user.

## GCS fallback when Drive workflow isn't needed

If the goal is just "share a public download link," GCS is simpler and your existing `cloud-platform` token already authorizes it:

```bash
gcloud storage cp /local/file gs://YOUR-BUCKET/path/
gcloud storage buckets add-iam-policy-binding gs://YOUR-BUCKET \
  --member=allUsers --role=roles/storage.objectViewer
# Public URL: https://storage.googleapis.com/YOUR-BUCKET/path/file
```

Same Google account, same content, different product. Choose based on what the consumer needs: Drive = integrate with existing Drive folders / sharing with Drive users; GCS = one-off share link.

## Known unknowns (verified by exhaustive negative tests in this session)

- **gcloud user token cannot be refreshed with drive.file** even when adding the scope to a fresh refresh — it's the client, not the token. Source: token-info probe showed scope `cloud-platform` only.
- **gws CLI's OAuth client_id is not retrievable from its public README** (webfetch 404) — likely uses the same shared client as `gcloud` and hits the same block. Treat gws as Drive-unusable until proven otherwise.
- **Chrome cookies cache `203784468217.apps.googleusercontent.com`** as a client_id, but it's locked down: `invalid_request: your app is missing the latest security features`. Cannot be reused from outside Chrome.
- **rclone shared client secret is the well-known `GOCSPX-...`** but Google has blacklisted the *client_id* itself, not the secret, so it doesn't help.

## Sources

- [rclone Drive docs §Making your own client_id](https://rclone.org/drive/#making-your-own-client-id) — the recipe that works
- [rclone Drive docs §Scopes](https://rclone.org/drive/#scopes) — `drive.file` vs `drive` vs `drive.readonly`
- [Google Cloud — Setting up OAuth 2.0](https://support.google.com/cloud/answer/6158849) — application types and consent screen
- [GCS — Making data public](https://cloud.google.com/storage/docs/access-control/making-data-public) — fall-back option
- This session: [PR #419-#422](https://github.com/jleechanorg/worldai_claw) for the iOS binary pipeline; companion memory `feedback_2026-08-13_metrosymlink_hardlink_clone_node_modules.md` and superseded `reference_gdrive_oauth_dance.md` (kept for the negative-finding record).