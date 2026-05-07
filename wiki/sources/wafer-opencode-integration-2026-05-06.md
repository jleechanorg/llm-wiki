# Wafer Pass + OpenCode Integration

## Source

Primary verification: curl + tmux opencode run session, 2026-05-06.

## What is Wafer Pass?

Wafer Pass (pass.wafer.ai) is a provably-fair inference provider with flat weekly pricing. It exposes an **OpenAI-compatible API** at `https://pass.wafer.ai/v1`, supporting models including GLM-5.1 and Qwen3.5-397B-A17B.

## OpenCode Integration

OpenCode (v1.14.31, binary at `/Users/jleechan/.opencode/bin/opencode`) reads standard OpenAI env vars at runtime. The correct integration approach uses a **wrapper function** to avoid polluting the host `OPENAI_API_KEY`.

### Environment Variables

| Variable | Value | Purpose |
|---|---|---|
| `WAFER_API_KEY` | `wfr_0c...` | Wafer Bearer token |
| `OPENAI_BASE_URL` | `https://pass.wafer.ai/v1` | Wafer OpenAI-compatible endpoint |

### Wrapper Function

```bash
# In ~/.bashrc
export WAFER_API_KEY=wfr_0c096567c3fbb707e92b94390fe6c0573910802fd04ffaf87f9437865685fa01

opencodew() {
  OPENAI_API_KEY="$WAFER_API_KEY" OPENAI_BASE_URL=https://pass.wafer.ai/v1 \
    opencode "$@"
}
```

### Usage

```bash
opencodew run "count to 3" --model GLM-5.1 --dangerously-skip-permissions
opencodew models    # lists available models via wafer
```

### Model Names

- **Correct**: `GLM-5.1` — works
- **Incorrect**: `GLM-5.1/` (trailing slash) — produces `Model not found: GLM-5.1/.`

### Verification

```bash
# Direct API curl
curl -s -X POST "https://pass.wafer.ai/v1/chat/completions" \
  -H "Authorization: Bearer $WAFER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"GLM-5.1","messages":[{"role":"user","content":"Say hello in 3 words"}],"max_tokens":50}'

# Via opencode wrapper (tmux)
# opencodew run "count to 5" --model GLM-5.1 --dangerously-skip-permissions
# → "1, 2, 3, 4, 5" ✓
# opencodew run "run git status" --model GLM-5.1 --dangerously-skip-permissions
# → "On branch worktree_wafer\nnothing to commit, working tree clean" ✓
```

## Concepts

- [ProviderWrapperIsolation](../concepts/ProviderWrapperIsolation.md) — using a shell wrapper to isolate provider credentials without affecting host env — **related**
- [OpenCodeAgentProtocol](../concepts/OpenCodeAgentProtocol.md) — OpenCode uses `OPENAI_API_KEY` + `OPENAI_BASE_URL` for provider discovery — **related**

## See Also

- [OpenCode CLI docs](https://opencode.ai) — `opencode run`, `opencode models`, `opencode providers`
- [Wafer Pass](https://pass.wafer.ai) — provider pricing and model catalog
