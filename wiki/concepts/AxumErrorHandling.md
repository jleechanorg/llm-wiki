---
title: "Axum Error Handling"
type: concept
tags: [axum, rust, error-handling, async, composable]
last_updated: 2026-04-14
---

## Summary

Axum uses `IntoResponse` as the core error-handling primitive. Any type implementing `IntoResponse` can be returned from a handler, enabling a uniform response model. Errors propagate via `Result<T, E>` where `E: IntoResponse`.

## Key Patterns

**Result-based handlers** — Handler functions return `Result<impl IntoResponse, impl IntoResponse>`:
```rust
async fn handler() -> Result<Json<Value>, StatusCode> {
    let data = fetch_data().await?;
    Ok(Json(data))
}
```

**Custom error types implementing IntoResponse** — Aggregate errors into a single response type:
```rust
struct AppError {
    status: StatusCode,
    message: String,
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        (self.status, self.message).into_response()
    }
}
```

**Using thiserror for ergonomic error types**:
```rust
#[derive(Debug, thiserror::Error)]
enum MyError {
    #[error("not found")]
    NotFound,
    #[error("db error: {0}")]
    Db(#[from] sqlx::Error),
}

impl IntoResponse for MyError { ... }
```

## Middleware-based Error Handling

Axum's middleware layer can intercept errors via the `map_request` and `map_response` combinators. For global error handling, use a custom layer:
```rust
layer_fn(|res| async move {
    match res {
        Ok(v) => Ok(v),
        Err(e) => handle_error(e).await,
    }
})
```

## Connections
- [[FastAPIErrorHandling]] — Python async equivalent
- [[ErrorHandlingPatterns]] — Generic error patterns
