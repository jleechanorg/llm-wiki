---
title: "Zustand Patterns"
type: concept
tags: [canonical, typescript, zustand, state-management, react]
sources: [canonical-code-repos/zustand]
last_updated: 2026-04-14
---

## Summary

Zustand provides minimal boilerplate state management with hooks-first API. The key insight: stores are just functions that return state and setters — no Context providers, no reducers, no connect() HOCs. Selectors are first-class, enabling fine-grained subscriptions that avoid unnecessary re-renders.

## Key Patterns

### Store as Hook
```typescript
import { create } from 'zustand';

const useStore = create((set) => ({
  count: 0,
  inc: () => set((state) => ({ count: state.count + 1 })),
}));

function Counter() {
  const { count, inc } = useStore(); // Select multiple values
  return <button onClick={inc}>{count}</button>;
}
```

Stores are hooks. Components call them directly — no wrapping with Context.Provider.

### Slice Pattern for Large Stores
```typescript
// counterSlice.ts
interface CounterState {
  count: number;
  inc: () => void;
}

const createCounterSlice = (set) => ({
  count: 0,
  inc: () => set((state) => ({ count: state.count + 1 })),
});

// userSlice.ts
interface UserState {
  user: User | null;
  setUser: (user: User) => void;
}

const createUserSlice = (set) => ({
  user: null,
  setUser: (user) => set({ user }),
});

// Combine in store
const useStore = create<CounterState & UserState>()((...args) => ({
  ...createCounterSlice(...args),
  ...createUserSlice(...args),
}));
```

Slice pattern composes smaller stores into one, keeping code organized by domain.

### Middleware: Devtools
```typescript
const useStore = create(
  devtools(
    (set) => ({
      count: 0,
      inc: () => set((state) => ({ count: state.count + 1 })),
    }),
    { name: 'my-store' }
  )
);
```

DevTools middleware enables time-travel debugging in browser extension.

### Middleware: Persist
```typescript
const useStore = create(
  persist(
    (set) => ({
      theme: 'dark',
      setTheme: (theme) => set({ theme }),
    }),
    { name: 'theme-storage' }
  )
);
```

Persist middleware automatically saves state to localStorage/sessionStorage.

### Middleware: SubscribeWithSelector
```typescript
const useStore = create(
  subscribeWithSelector(
    (set) => ({
      count: 0,
      inc: () => set((state) => ({ count: state.count + 1 })),
    })
  )
);

// Subscribe to specific slices without re-rendering
const unsubscribe = useStore.subscribe(
  (state) => state.count,
  (count) => console.log('count changed:', count)
);
```

subscribeWithSelector enables external subscriptions for analytics or derived state.

### Cross-Component Subscriptions
```typescript
// Select single value — component only re-renders when value changes
const count = useStore((state) => state.count);

// Computed selection — derived without re-render parent
const doubleCount = useStore((state) => state.count * 2);

// External component — no re-render at all
useStore.subscribe((state) => console.log(state.count));
```

Selectors are the core pattern. Pass a function to get only what you need.

### Immer Integration
```typescript
import { immer } from 'zustand/middleware/immer';

const useStore = create(
  immer((set) => ({
    nested: { a: 1, b: 2 },
    update: () =>
      set((state) => {
        state.nested.a += 1; // Mutating works due to Immer
      }),
  }))
);
```

Immer middleware allows mutable-style syntax that produces immutable updates.

## What This Means for Code Generation

Generated React state management code should:
1. Prefer Zustand over Redux — less boilerplate, hooks-native
2. Use slice pattern for stores > 10 fields — organize by domain
3. Always use selectors — `useStore(s => s.field)`, not destructuring
4. Add persist for user preferences — automatic localStorage sync
5. Add devtools in development — time-travel debugging
6. Use Immer for complex nested updates — cleaner mutation syntax
7. Never wrap with Context.Provider — stores ARE hooks