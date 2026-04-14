---
title: "Next.js Patterns"
type: concept
tags: [canonical, typescript, nextjs, react-framework, server-components]
sources: [canonical-code-repos/nextjs]
last_updated: 2026-04-14
---

## Summary

Next.js App Router shifts the paradigm: components are server-only by default, client is opt-in via 'use client'. The key architectural decisions: streaming with Suspense, caching at the route level, and server actions as the mutation primitive. This enables hybrid apps where most code stays on the server.

## Key Patterns

### App Router Conventions
```typescript
// app/
// ├── page.tsx          // Route: /
// ├── layout.tsx        // Shared layout (root, auth, etc.)
// ├── error.tsx         // Error boundary
// ├── loading.tsx       // Loading UI (streaming)
// ├── not-found.tsx     // 404 page
// └── route.ts          // API route handler
```

File-based routing. Each folder is a route segment with special files.

### Server vs Client Components
```typescript
// server-component.tsx (default in App Router)
// - Runs on server only
// - Can access DB, filesystem, secrets
// - Can be async
// - Renders to HTML
async function ServerComponent() {
  const data = await db.query('SELECT * FROM users');
  return <ul>{data.map(u => <li>{u.name}</li>)}</ul>;
}

// client-component.tsx
'use client';
// - Runs on client (browser)
// - Can use hooks (useState, useEffect)
// - Can handle events (onClick)
// - Must be serialized for hydration
function ClientComponent({ initialData }) {
  const [data, setData] = useState(initialData);
  return <button onClick={() => setData(newData)}>Update</button>;
}
```

Default is server. Opt-in to client with 'use client' directive.

### Route Handlers
```typescript
// app/api/users/route.ts
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const users = await db.user.findMany();
  return NextResponse.json(users);
}

export async function POST(request: Request) {
  const body = await request.json();
  const user = await db.user.create({ data: body });
  return NextResponse.json(user, { status: 201 });
}
```

API routes via route.ts files. Same file handles GET, POST, PUT, DELETE.

### Server Actions
```typescript
// app/actions.ts
'use server';

export async function createUser(formData: FormData) {
  'use server';
  const name = formData.get('name');
  await db.user.create({ data: { name: String(name) } });
}

// app/page.tsx
import { createUser } from './actions';

export default function Page() {
  return (
    <form action={createUser}>
      <input name="name" />
      <button type="submit">Create</button>
    </form>
  );
}
```

Server Actions let server functions be called directly from client forms.

### Streaming with Suspense
```typescript
import { Suspense } from 'react';

async function HeavyComponent() {
  const data = await slowDataFetch(); // May suspend
  return <div>{data}</div>;
}

export default function Page() {
  return (
    <Suspense fallback={<Skeleton />}>
      <HeavyComponent />
    </Suspense>
  );
}
```

Suspense boundaries split the page. Fast parts render immediately, slow parts stream in.

### Caching Strategies
```typescript
// Force dynamic — no cache
export const dynamic = 'force-dynamic';

// Static with revalidation
export const revalidate = 3600; // Revalidate every hour

// Cache tags for on-demand invalidation
export default async function Page() {
  revalidateTag('users');
  const users = await fetch('/api/users', { next: { tags: ['users'] } });
  return <UserList users={users} />
}
```

Route-level caching control. Use tags for selective invalidation.

### Middleware
```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token');
  
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*'],
};
```

Middleware runs before requests hit routes. Use for auth, redirects, A/B tests.

## What This Means for Code Generation

Generated Next.js code should:
1. Default to Server Components — add 'use client' only when needed
2. Use Server Actions for mutations — not API routes for form submissions
3. Wrap slow data fetches in Suspense — stream UI, don't block
4. Use Route Handlers for external API consumption, not for internal mutations
5. Set cache headers explicitly — don't rely on defaults for dynamic data
6. Put auth logic in middleware — runs before any route code
7. Prefer Server Components for data fetching — client fetches only for real-time