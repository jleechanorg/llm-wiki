---
title: "/claw Slack dispatch independent of :8642 gateway HTTP"
type: source
tags: [claw, dispatch, hermes, slack, gateway, feedback]
date: 2026-06-15
source_file: raw/feedback_2026-06-15_claw_slack_vs_gateway_dispatch.md
---

## Summary

The `/claw` skill dispatches via Slack `#claw-dispatch` and via the Hermes HTTP gateway at `:8642`. These are **independent transport layers**. Hermes receives Slack messages via Socket Mode which remains alive even when the `:8642` HTTP endpoint is down. The skill's current hard-exit on gateway health check failure incorrectly blocks Slack dispatch.

## Key Claims

- `:8642` HTTP endpoint and Hermes Socket Mode (Slack listener) are separate processes
- Hard-exiting `/claw` when `:8642` is down silently prevents valid Slack dispatch
- Fix: degrade the gateway health check to a warning; proceed to Slack; use `ao spawn` only if Slack also fails
- Wrong execution on 2026-06-15: went directly to `ao spawn` when `:8642` was down, bypassing Slack

## Key Quotes

> "Gateway :8642 being down does NOT mean Slack dispatch is unavailable."

## Connections

- [[HermesGateway]] — the `:8642` HTTP endpoint for synchronous dispatch
- [[ClawDispatch]] — the `/claw` skill and its transport layers
