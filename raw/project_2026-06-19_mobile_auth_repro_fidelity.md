---
name: Mobile auth repro fidelity: classify boundary signals vs exact iOS Chrome symptom
description: Faithful mobile auth repro needs same-symptom criteria, simulator Safari/private NON-REPRO evidence, and a reusable WebKit supporting lane.
type: project
bead: rev-g7mp3
---

# Mobile Auth Repro Fidelity

On 2026-06-19, the mobile auth investigation tried to reproduce Chrome iOS Incognito / Safari ITP style Firebase Google sign-in failure without the user's phone. The exact symptom was not "any OAuth problem"; it was: after Google redirect returns to `worldarchitect.ai`, the app remains unauthenticated on the welcome card because Firebase `getRedirectResult()` effectively resolves null.

The correct repro approach was to write the phenotype table first:

- `REPRO`: real mobile-ish browser returns to `worldarchitect.ai` after Google OAuth and still shows the welcome/login UI with no authenticated user.
- `RELATED_REDIRECT_BOUNDARY_REACHED`: browser reaches `worldarchitecture-ai.firebaseapp.com/__/auth/handler` or `accounts.google.com` under partitioned storage.
- `RELATED_SILENT_NULL_SIGNATURE`: storage eviction makes Firebase `getRedirectResult()` settle with `hasUser=false`, `error=null`.
- `NON-REPRO`: flow authenticates successfully or fails at an unrelated OAuth configuration page.

Evidence gathered:

- iOS 18.6 Simulator Safari normal production cross-origin auth returned authenticated as `jleechantest@gmail.com`; `NON-REPRO`. Evidence: `/tmp/worldarchitectai/prod-ios-crossorigin-20260619T101813Z/03_after_tap_43s.png`, SHA256 `17e5c83330cee93f0ee7bf7f4f0bedbe5694ae99ba9936bc2726e13c3ade5b53`.
- iOS 18.6 Simulator Safari Private production cross-origin auth also returned authenticated; `NON-REPRO`. Evidence: `/tmp/worldarchitectai/prod-ios-crossorigin-20260619T101813Z/22_private_after_password_next_67s.png`, SHA256 `77e5569103546bb196edd324901eabb16a2f0cac42080ea0b6c56798d097814e`.
- PR #7698 Chromium harness reproduced the partition boundary and storage-eviction silent-null signature.
- PR #7698 commit `02c6af2b2cc17f68bf11c7879e01baa2bc5d58b5` added WebKit/iPhone-context D2c storage eviction. It produced `getRedirectResultAfterEviction.resolved=true`, `hasUser=false`, `error=null`.

Reusable command:

```bash
PATH=/Users/jleechan/.nvm/versions/node/v22.22.0/bin:$PATH \
node --test --test-timeout=90000 testing_ui/mobile_3pc_repro/repro_3pc_auth.spec.mjs
```

Result after D2c:

```text
# tests 4
# pass 4
# fail 0
```

Why it was hard:

- Chrome iOS cannot be installed in the local iOS Simulator; Simulator Safari is not Chrome iOS Incognito.
- Real OAuth includes Google account, passkey, password, CAPTCHA/2FA risk, save-password sheets, and redirect URI policy.
- Mechanism evidence is tempting but not the same as the original user-visible symptom.
- Simulator Safari normal and Private contradicted the suspected symptom by authenticating successfully.
- BrowserStack/Sauce/Appium credentials were not configured locally, in common dotfiles, repo config, GitHub secret names, or repo variables.

Durable rule: for mobile auth bugs, separate `REPRO`, `RELATED`, and `NON-REPRO` explicitly. Do not describe boundary/storage evidence as the original bug reproduced unless the same post-return user-visible symptom appears.

References:

- PR #7698: https://github.com/jleechanorg/worldarchitect.ai/pull/7698
- Commit: https://github.com/jleechanorg/worldarchitect.ai/commit/02c6af2b2cc17f68bf11c7879e01baa2bc5d58b5
- Memory: `/Users/jleechan/.Codex/projects/-Users-jleechan-projects-worktree_mobile_login/memory/project_2026-06-19_mobile_auth_repro_fidelity.md`
- Bead: `rev-g7mp3`

[[jeffrey-oracle]]: NO.
