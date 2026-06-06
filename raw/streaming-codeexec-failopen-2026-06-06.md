# Streaming code-exec fail-open RCA and subagent cleanup discipline

On 2026-06-05/06, WorldArchitect preview campaign `8J0RzsHVHH1GLg6E6BLM`
persisted a fallback story entry: `The story continues...` with
`Missing action_resolution field`.

Recovered payload:

- `sha256=1b2c8bbfb79b085b8af7976183f88ff230bb57fc1d4576bf03203b7767a0295c`
- `bytes=2070`
- top-level JSON list length `2`
- each item had `tool=code_execution` and `args.code`
- no normal text response
- no observed `code_execution_result.output`

Root cause: the Gemini streaming path applied code-execution instructions but
did not attach the actual `code_execution` tool. Gemini emitted code containing
the intended structured answer, but the platform returned it inert. The
extraction path read text parts only, so parsing never saw the answer and
fail-open persisted the fallback.

Future prevention:

- For streaming placeholder narratives, inspect request tool config and response
  part types before blaming truncation or model failure.
- Keep streaming and non-streaming provider config parity when prompts mention
  tools.
- Treat executable-code-without-result as a hard diagnostic.
- Do not store full request/response payloads inline in Cloud Logging; use
  pointer logs to short-TTL GCS or BigQuery artifacts.
- Avoid parallel `close_agent` sweeps on stuck subagents; use bounded waits and
  report stale lanes.
