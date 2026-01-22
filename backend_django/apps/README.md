# Core Domain Applications

This directory contains the core Django applications that make up the **system of record** for the Civic Integrity platform.

Each app represents a **distinct domain concern**, following a modular and domain-oriented design.  
The goal is to keep responsibilities clear, loosely coupled, and easy to evolve as the platform grows.

---

## Design Principles

- **Single Responsibility**: Each app owns one domain concept.
- **Explicit Boundaries**: Cross-app dependencies are kept minimal and intentional.
- **Extensible by Design**: Apps are designed to evolve independently.
- **Backend-First**: These apps form the authoritative source of truth for the platform.

---

## Applications Overview

### `user_auth`
Manages **user identity and authentication**.

Responsibilities:
- User model and identity lifecycle
- Authentication primitives (intentionally minimal)
- Ownership attribution for claims and evidence

Out of scope:
- Social login
- Role-based access control
- Reputation or scoring logic

---

### `common`
Shared infrastructure and cross-cutting utilities used across Django apps.

Responsibilities:
- Abstract base models (e.g. `TimeStampedModel`)
- Cross-app domain models (e.g. content view tracking)
- Generic services (anti-abuse, rate limiting, heuristics)
- Reusable permissions, helpers, and utilities
- Shared testing utilities and fixtures

Design principles:
- Contains **no app-specific business logic**
- Safe to depend on from any other app
- Optimized for reuse, auditability, and testability

Examples:
- View tracking with anti-gaming safeguards
- Rate limiting and abuse detection utilities
- UUID-based base models and shared mixins

Feature-specific logic should not live in this app.

---

### `contributors`
Represents contributors as trust-bearing participants in the platform.

Responsibilities:
- Contributor profiles linked to users
- Reputation tracking and audit logs
- Contributor-specific permissions and access rules
- Participation and verification-related metadata

Note: This app is distinct from authentication and identity.
It models **behavior, trust, and participation state**, not login or credentials.

---

### `claims`
Represents verifiable claims related to real-world events.

Responsibilities:
- Claim creation and lifecycle
- Status tracking (e.g., pending, under review, verified)
- Association with evidence and contributors

Claims are treated as **first-class domain entities**.

---

### `evidence` (planned)
Handles media and supporting material attached to claims.

Responsibilities:
- Evidence metadata (media type, location, timestamp)
- Linkage to claims and contributors
- References to externally stored media (object storage / CDN)

Media processing itself is handled by external services.

---

### `rewards`
Manages contributor incentives and reward attribution.

Responsibilities:
- Reward calculation inputs
- Attribution records
- Interfaces with reward algorithms

Note: Reward logic is intentionally separated from claims and contributors to allow independent iteration.

---

## Architectural Notes

- These apps form the **core backend** and act as the authoritative data layer.
- Advanced processing (e.g., media verification, AI pipelines) is delegated to external services.
- This structure supports a hybrid architecture where Django provides stability and FastAPI services provide scalability.

---

## Status

This project is in an **early prototyping phase**.  
APIs and models are expected to evolve as real-world constraints are discovered.

