# REV: Smoke token allowed path check overly broad

## Status: done
## Priority: medium
## Type: security

## Summary

`smoke_token_allowed_path` in `mvp_site/main.py` used `request.path.endswith("/interaction/stream")`
which matched ANY URL ending with that suffix (e.g. `/admin/interaction/stream`). While the actual
security impact is minimal (requires valid HMAC smoke token + preview environment), it violated
the principle of least privilege compared to the exact-match `/mcp` check.

## Fix

Replaced `.endswith()` with `re.fullmatch(r"/api/campaigns/[A-Za-z0-9]+/interaction/stream", ...)`
to match only the intended campaign streaming endpoint pattern.

## Files Changed

- `mvp_site/main.py`
