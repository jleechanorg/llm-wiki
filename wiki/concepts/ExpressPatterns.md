---
title: "Express Patterns"
type: concept
tags: [canonical, typescript, express, nodejs, http-framework]
sources: [canonical-code-repos/express]
last_updated: 2026-04-14
---

## Summary

Express.js provides minimal Node.js HTTP framework with middleware as the core composition pattern. The key insight: everything is middleware, including error handlers. Routes are just middleware with path matching. This simplicity enables flexible request handling but requires explicit structuring for larger apps.

## Key Patterns

### Middleware Chain
```typescript
import express from 'express';
const app = express();

// Middleware runs in order — each must call next()
app.use((req, res, next) => {
  console.log(`${req.method} ${req.path}`);
  next(); // Pass to next middleware
});

// Body parsing middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Route handler — a middleware with path matching
app.get('/users', (req, res) => {
  res.json(users);
});

app.listen(3000);
```

Middleware chains execute sequentially. Every middleware must call `next()` or respond.

### Error-Handling Middleware
```typescript
// Error-handling middleware: 4 args (err, req, res, next)
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal server error' });
});

// Throwing in routes triggers error handler
app.get('/users/:id', async (req, res, next) => {
  try {
    const user = await db.findUser(req.params.id);
    if (!user) throw new Error('Not found');
    res.json(user);
  } catch (e) {
    next(e); // Pass to error handler
  }
});
```

Error middleware has 4 parameters. Errors propagate via `next(err)`.

### Router Pattern
```typescript
const authRouter = express.Router();

// Middleware specific to this router
authRouter.use((req, res, next) => {
  if (!req.headers.authorization) {
    return res.status(401).json({ error: 'No token' });
  }
  next();
});

authRouter.post('/login', (req, res) => {
  // Login logic
  res.json({ token: '...' });
});

authRouter.get('/me', (req, res) => {
  // Get current user
  res.json({ user: req.user });
});

// Mount router
app.use('/auth', authRouter);
```

Routers partition routes. Each router has its own middleware stack and routes.

### Request/Response Pattern
```typescript
// Route parameters
app.get('/users/:id/posts/:postId', (req, res) => {
  const { id, postId } = req.params; // Route params
  const page = req.query.page;       // Query params
});

// Response shortcuts
res.status(201).json({ created: true });
res.redirect('/other-page');
res.send('<html>...</html>');

// Chaining
app.route('/users')
  .get((req, res) => res.json(users))
  .post((req, res) => res.status(201).json(createUser(req.body)));
```

req holds all input (params, query, body). res provides response methods.

### Body Parsing
```typescript
// JSON body
app.use(express.json());

// URL-encoded form data
app.use(express.urlencoded({ extended: true }));

// Raw binary
app.use(express.raw());

// Multer for multipart (files)
import multer from 'multer';
const upload = multer({ dest: 'uploads/' });

app.post('/upload', upload.single('file'), (req, res) => {
  // req.file has uploaded file info
});
```

Built-in parsers handle common body types. For files, use multer.

### CORS and Helmet
```typescript
import cors from 'cors';
import helmet from 'helmet';

// Security headers
app.use(helmet());

// Cross-origin requests
app.use(cors({
  origin: 'https://myapp.com',
  credentials: true,
}));
```

Helmet sets security headers. CORS enables cross-origin API access.

### Async Error Wrapping
```typescript
// Without wrapper — errors don't propagate
app.get('/users', async (req, res, next) => {
  const users = await db.query('SELECT *'); // If this throws, it's unhandled!
  res.json(users);
});

// With wrapper
const asyncHandler = (fn) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);

// Now errors propagate to error handler
app.get('/users', asyncHandler(async (req, res) => {
  const users = await db.query('SELECT *');
  res.json(users);
}));

// Or use express-async-errors package — automatic wrapping
import 'express-async-errors';
```

Async routes need error wrapping or the package to catch errors.

## What This Means for Code Generation

Generated Express code should:
1. Always use async error wrapper — or express-async-errors package
2. Partition routes with Router — keep auth, API, admin separate
3. Put error handler LAST — after all routes
4. Use helmet + cors — minimal security for any API
5. Prefer res.json() — explicit JSON responses
6. Use route() for method chaining — cleaner than separate handlers
7. Validate input early — before business logic, use Zod or similar