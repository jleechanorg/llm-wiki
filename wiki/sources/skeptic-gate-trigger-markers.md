# Skeptic Gate CI Trigger Marker Injection

**Source**: `feedback_2026-05-23_skeptic_gate_trigger_markers.md`
**Date**: 2026-05-23
**Type**: Feedback / Mandatory

## Summary

`ao skeptic verify` run standalone (manual or cron) does **not** embed the three trigger markers that the Skeptic Gate CI polling step requires:

```
<!-- skeptic-gate-trigger-<SHA> -->
<!-- skeptic-head-sha-<SHA> -->
<!-- skeptic-request-id-gate-<SHA>-<RUN_ID>-<N> -->
```

The lifecycle-worker invocation embeds them (reads trigger comment ID and passes it to the verdict writer). Standalone does not.

## Workaround

```bash
# 1. Get trigger comment to extract markers
TRIGGER_BODY=$(gh api repos/OWNER/REPO/issues/comments/TRIGGER_COMMENT_ID --jq '.body')
TRIGGER_MARKERS=$(echo "$TRIGGER_BODY" | grep "skeptic-gate-trigger\|skeptic-head-sha\|skeptic-request-id")

# 2. Prepend markers to verdict comment
VERDICT_BODY=$(gh api repos/OWNER/REPO/issues/comments/VERDICT_COMMENT_ID --jq '.body')
gh api --method PATCH repos/OWNER/REPO/issues/comments/VERDICT_COMMENT_ID \
  --field body="$TRIGGER_MARKERS
$VERDICT_BODY"
```

## Verification

PR #585 — Skeptic Gate CI run 26350007538 completed `success` after manual marker injection into verdict comment 4526930225.

## References

- PR: https://github.com/jleechanorg/agent-orchestrator/pull/585
- Bead: bd-vqfw
