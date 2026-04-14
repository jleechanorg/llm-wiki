---
title: "SQLAlchemy Patterns"
type: concept
tags: [canonical, python, sqlalchemy, orm, session-management]
sources: [canonical-code-repos/sqlalchemy]
last_updated: 2026-04-14
---

## Summary

SQLAlchemy is the canonical reference for Python ORM and database abstraction. Its defining insight: separate the Core (SQL composition) from the ORM (object-relational mapping), then unify them under a single `select()` construct in SQLAlchemy 2.0. Session management follows a strict lifecycle — open, use, commit/rollback, close — with explicit control over transaction boundaries. The object state machine (Transient → Pending → Persistent → Deleted → Detached) is the mental model for understanding identity and persistence.

## Key Patterns

### Declarative ORM Mapping
```python
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(unique=True)
```

`DeclarativeBase` is the modern SQLAlchemy 2.0 pattern. `Mapped[]` annotations declare types; `mapped_column()` replaces the old `Column()`. Type safety via `Mapped[str]` annotations, not runtime-only schema.

### Session Factory (sessionmaker)
```python
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://user:pass@localhost/db")
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
```

`sessionmaker` is the factory for `Session` instances with consistent configuration. Key settings: `autoflush=False` (manual control over when queries fire), `expire_on_commit=False` (objects remain usable after commit without re-fetching).

### Session Lifecycle via Context Manager
```python
from contextlib import contextmanager

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

with get_session() as session:
    user = session.get(User, 1)
    user.name = "Alice"
# commits on exit, rolls back on exception
```

Context manager pattern for session lifecycle: commit on success, rollback on exception, always close. This is the canonical pattern for ensuring transaction boundaries are respected.

### Scoped Session for Thread-Local Web Apps
```python
from sqlalchemy.orm import scoped_session, sessionmaker

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# In a web request:
session = Session()       # thread-local session
try:
    user = session.query(User).first()
    session.commit()
finally:
    Session.remove()      # clean up at end of request
```

`scoped_session` provides thread-local session registry. In web frameworks (Flask, Pyramid), one session per thread/request is the standard pattern. `Session.remove()` cleans up at request end.

### Query with select() (SQLAlchemy 2.0)
```python
from sqlalchemy import select

stmt = select(User).where(User.email == "alice@example.com")
user = session.execute(stmt).scalar_one_or_none()
```

`select()` is the unified query construct in SQLAlchemy 2.0. Works for both Core and ORM. `scalar_one_or_none()` / `scalar_one()` / `scalars().all()` for result extraction. Old `.query()` style still works but `select()` is preferred.

### Relationships and back_populates
```python
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    accounts: Mapped[list["Account"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="accounts")
```

`relationship()` with `back_populates` establishes bidirectional links. `cascade="all, delete-orphan"` ensures parent deletion cascades to children. Lazy loading (`lazy="select"`) is default; use `lazy="selectin"` for batch loading.

### Object State Machine
```
Transient → Pending → Persistent → Deleted → Detached
```
- **Transient**: object exists, no session, not in DB
- **Pending**: object added to session, not yet flushed to DB
- **Persistent**: object in session and committed to DB
- **Deleted**: object marked for deletion on flush
- **Detached**: object was in session but session closed

Understanding states is critical for `merge()`, `expunge()`, and `refresh()` behavior. `session.flush()` syncs pending changes to the DB within the current transaction.

### Transaction Management
```python
with engine.begin() as conn:
    conn.execute(text("INSERT INTO users (name) VALUES (:name)"), {"name": "Alice"})
# auto-commit on context exit

# Or with session savepoints:
session.begin_nested()  # savepoint
try:
    session.add(User(name="Bob"))
    session.flush()
except:
    session.rollback_nested()
    raise
```

Savepoints (`begin_nested()`) allow partial rollback within a transaction. Isolation levels set on `create_engine(isolation_level="REPEATABLE READ")`. Two-phase commit for distributed transactions.

### Bulk Operations
```python
# Bulk insert
session.execute(
    insert(User),
    [{"name": "Alice", "email": "alice@example.com"},
     {"name": "Bob", "email": "bob@example.com"}]
)

# Upsert (PostgreSQL)
from sqlalchemy.dialects.postgresql import insert
stmt = insert(User).values(name="Alice", email="alice@example.com")
stmt = stmt.on_conflict_do_update(index_elements=['email'], set_=dict(name="Alice"))
session.execute(stmt)
```

Bulk operations bypass ORM overhead for large datasets. `insert().values(list_of_dicts)` for bulk inserts. Dialect-specific `insert().on_conflict_do_update()` for upsert.

### Events and Observability
```python
from sqlalchemy import event

@event.listens_for(Session, "before_flush")
def before_flush(session, flush_context, instances):
    for obj in session.new:
        validate_object(obj)

@event.listens_for(User, "before_insert")
def set_created_at(mapper, connection, target):
    target.created_at = func.now()
```

`@event.listens_for()` hooks into mapper and session lifecycle. `before_flush`/`after_flush` for session observability. `before_insert`/`before_update` for automatic column population.

## Connections

- [[FastAPIErrorHandling]] — FastAPI typically uses SQLAlchemy with a session-per-request context manager pattern. The session lifecycle mirrors FastAPI's dependency injection pattern: open on request, commit/rollback on response.
- [[RequestsAPIDesign]] — SQLAlchemy's sessionmaker follows the same "factory with consistent defaults" pattern as `requests.Session()`.
- [[AsyncIO]] — SQLAlchemy 2.0 supports async with `AsyncSession` and `async_sessionmaker`, enabling non-blocking database access in async frameworks.

## What This Means for Code Generation

Generated code should:
1. Use `DeclarativeBase` and `Mapped[]` annotations — not the old `Column()` style
2. Wrap sessions in context managers with explicit commit/rollback
3. Prefer `scoped_session` for web apps; plain `sessionmaker` for scripts
4. Use `select()` over `.query()` for all new code
5. Set `autoflush=False` and `expire_on_commit=False` for predictable behavior
6. Express relationships bidirectionally with `back_populates`
7. Understand the object state machine — don't mix detached objects across sessions
8. Use bulk operations for datasets > 1000 rows
