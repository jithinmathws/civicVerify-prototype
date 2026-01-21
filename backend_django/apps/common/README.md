# Common App

The `common` app contains shared models, services, and utilities used across
the CivicVerify backend. It centralizes cross-cutting concerns to avoid
duplication and enforce consistent behavior across domain modules.

This app is intentionally domain-aware (not a generic utils folder).

---

## Responsibilities

### 1. Shared Base Models
Reusable abstract models that provide common fields and behavior.

- `TimeStampedModel`
  - UUID primary key
  - `created_at`, `updated_at`

Used by most domain models across the system.

---

### 2. Content View Tracking

Tracks views across different content types using Django’s generic relations.

**Key goals:**
- Unified analytics across claims, evidence, and media
- Anti-gaming protection
- Support for reward weighting and moderation insights

**Core model:**
- `ContentView`

**Features:**
- Per-user and per-IP tracking
- View deduplication
- Lockout-aware filtering
- Time-window based rate limiting

---

### 3. Anti-Abuse & View Validation

Logic to prevent artificial inflation of engagement metrics.

**Implemented safeguards:**
- Ignore self-views
- Ignore creator views
- Exclude locked accounts
- Rate limiting based on recent activity
- IP-aware anonymous protection

Relevant modules:
- `services/anti_abuse.py`
- `services/view_tracking.py`

---

### 4. Analytics Foundation

Provides a clean data layer for future analytics, including:
- View counts per content
- Unique viewers
- Engagement velocity
- Abuse signals

No reporting UI exists here — only queryable primitives.

---

## Design Principles

- Domain-first (not framework-first)
- Shared logic lives here, not duplicated
- Side-effect aware (signals, throttling, abuse detection)
- Safe defaults over permissive counting

---

## Testing

Tests focus on:
- Abuse scenarios
- Edge cases (anonymous users, locked users)
- Rate-limiting correctness
- Idempotent view tracking

Run tests:
```bash
python manage.py test apps.common
```

---

## Contributing

The common app contains shared domain primitives used across the CrowdVerify backend.
It is intentionally conservative and stability-focused, as changes here can affect multiple
apps and services.

This app is not feature-oriented; it provides foundational building blocks.

### Scope

The common app includes:

- Abstract base models (e.g. `TimeStampedModel`)
- Cross-cutting domain models (e.g. view tracking, analytics signals)
- Shared services (anti-abuse, rate limiting, heuristics)
- Reusable utilities and helpers
- Common test utilities and fixtures

It must not contain:

- Business-specific logic (claims, rewards, verification decisions)
- UI- or API-specific behavior
- Direct dependencies on higher-level apps

### Design Principles

When contributing to common, follow these principles:

- **Stability over features**
  Changes should minimize breaking effects on downstream apps.
- **Explicitness over magic**
  Avoid implicit behavior, signals, or side effects that are hard to reason about.
- **Composable, not opinionated**
  Provide primitives and helpers — not workflows.
- **Security-aware by default**
  Anti-abuse, rate limiting, and integrity checks should be conservative.
- **Test-first mindset**
  Any behavioral change should include or update tests.