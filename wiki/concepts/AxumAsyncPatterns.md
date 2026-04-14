---
title: "Axum Async Patterns"
type: concept
tags: [canonical, axum, tokio, rust, async, composable]
sources: [~/canonical-code-repos/tokio/tokio/src/future/mod.rs, ~/canonical-code-repos/tokio/tokio-stream/src/stream_ext/mod.rs]
last_updated: 2026-04-14
---

## Summary

Axum (built on Tokio) uses composable middleware layers and trait-based handler extraction. Tokio's async model uses `Future` as a trait from std, with `InstrumentedFuture` wrapping for tracing. Streams use the `StreamExt` trait pattern with individual composable operators.

## Key Patterns

**Future type from std, not re-exported** — Tokio uses std::future::Future directly, only wrapping for instrumentation:
```rust
cfg_not_trace! {
    cfg_rt! {
        pub(crate) use std::future::Future;
    }
}

cfg_trace! {
    mod trace;
    #[allow(unused_imports)]
    pub(crate) use trace::InstrumentedFuture as Future;
}
```

**try_join for fallible async composition** — Combines multiple futures that can error:
```rust
cfg_process! {
    mod try_join;
    pub(crate) use try_join::try_join3;
}
```

**Feature-gated modules** — Code is compiled only when features are enabled:
```rust
cfg_process! {
    mod try_join;  // only compiled with process feature
}

cfg_sync! {
    mod block_on;  // only compiled with sync feature
}
```

**StreamExt trait with individual operators** — Each stream transformation is a method on the trait:
```rust
// tokio-stream/src/stream_ext/all.rs
pub struct AllFuture<S, F> {
    stream: S,
    async_move: F,
}

impl<S, F> Future for AllFuture<S, F>
where
    S: Stream,
    F: FnMut(S::Item) -> bool,
{
    type Output = bool;
    // ...
}
```

**async_buf_read for split read/write streams** — Async buffered reading is its own trait:
```rust
// tokio/src/io/async_buf_read.rs
pub trait AsyncBufRead: AsyncRead {
    fn fill_buf(&mut self) -> impl Future<Output = Result<&[u8], Error>>;
    fn consume(&mut self, amt: usize);
}
```

**poll_evented for I/O-based async** — Evented I/O wraps file descriptors with interest flags:
```rust
// tokio/src/io/poll_evented.rs
pub struct PollEvented<M: AsyncRead + AsyncWrite> {
    // ...
}
```

## What to Steal

- Feature-gated modules for compile-time dependency management
- `cfg_*!` macros to conditionally include code based on features
- StreamExt trait pattern — composable operators that each return a future
- Keep Future as std::future::Future, only wrap for tracing/metrics
- Separation between async primitives (Future/Stream) and I/O types (PollEvented)

## Connections

- [[FastAPIErrorHandling]] — Both use async; FastAPI is Python, Tokio is Rust
- [[CanonicalCodePatterns]] — Parent concept linking all canonical patterns
