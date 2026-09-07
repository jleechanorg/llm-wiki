---
title: "Claude Code Model Picker Entitlement Gap"
type: concept
tags: [claude-code, model-picker, entitlement, upstream-bug]
date: 2026-09-06
---

## Definition
Claude Code's interactive `/model` picker can disagree with the actual, working
entitlement check used by `claude --model <id>`. The picker shows a model as
missing, greyed-out/"disabled", or "requires usage credits" while the same
account can start and run a session on that exact model via the `--model` flag.
This has recurred specifically for the Fable model family across multiple
Claude Code versions (2.1.170–2.1.259), account types (personal, Team Premium,
org-managed), and operating systems (macOS, Windows).

## Root causes observed (from real GitHub issues, verified via `gh api`)
1. **Stale server-side gating flag**: a model gets suspended (e.g. export-control
   related) then re-enabled, but the picker's cached availability flag isn't
   invalidated — [[FableModelPickerUpstreamBug]] / anthropics/claude-code#73423.
2. **Server-controlled policy file that reverts local overrides**: `~/.claude/policy-limits.json`
   can carry a restriction (e.g. `allow_cobalt_plinth: false`); editing it locally
   to `true` gets silently reverted by the server on next launch —
   anthropics/claude-code#66827.
3. **`modelPicker.options` (settings.json) does not inject non-active models into
   the picker's list in v2.1.259** — the picker only shows the fixed GA lineup
   plus whatever model the current session was launched with. A correctly-configured
   `modelPicker.options` entry for a real, entitled model can still never appear
   unless the session is started with `--model <that-id>` first. See
   [[feedback-2026-09-06-fable-model-picker-upstream-bug|the 2026-09-06 investigation]]
   for the full repro.

## Diagnostic procedure
1. Test `claude --model <id> -p "..."` directly. If it works (exit 0, banner
   confirms model), the account IS entitled — the picker's absence/greyed-out
   state is a display bug, not a config or entitlement problem.
2. Check for competing config sources in precedence order: managed-settings.json
   > `--settings` flag > `~/.claude/settings.json` > project `.claude/settings.json`
   — modelPicker rows from a lower-precedence source can be entirely superseded
   (not merged) by a higher one.
3. Check `~/.claude/policy-limits.json` for a server-pushed restriction.
4. If none of the above explain it, treat it as the known upstream defect —
   confirmed unresolved as of 2026-09 (all matching issues closed by inactivity-bot,
   not by an actual fix).

## Workaround (no client-side fix exists)
- `claude --model fable` (or the specific model id) per session — zero side effects.
- Avoid changing the global top-level `"model"` default key in `settings.json`
  to force the picker's preferred model as default — that silently changes the
  default for every future session. See [[SilentModelDowngradeAfterQuotaReset]].

## Related
- [[feedback-2026-09-06-fable-model-picker-upstream-bug|Fable 2026-09-06 investigation]] — the specific instance this concept generalizes
- [[VerifyUpstreamBugClaimsViaLiveAPI]] — verification method
