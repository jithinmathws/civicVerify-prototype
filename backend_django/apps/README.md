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

### `contributors`
Represents contributors as participants in the platform.

Responsibilities:
- Contributor metadata
- Participation history
- Linkage between users and contributions

Note: This is distinct from authentication and focuses on **behavioral participation**, not identity.

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

