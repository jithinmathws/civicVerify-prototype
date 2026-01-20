## Related Design Documents

- [Reward Algorithm](reward_algorithm.md)

# Architecture Overview

> **Project:** CrowdVerify (Research Prototype)
> **Author:** Jithin Mathews
> **Status:** Exploratory / Non‑production Architecture

---

## 1. Architectural Goals

This architecture is designed to explore **how a crowdsourced media‑verification system could be structured**, not to serve as a production deployment.

Primary goals:

* Clear separation of responsibilities
* Support for experimentation and simulation
* Explicit handling of uncertainty and failure modes
* Scalability *in principle*, without premature optimization

Non‑goals:

* High availability guarantees
* Real‑world user scale
* Automated truth determination

---

## 2. High‑Level System View

The system follows a **hybrid architecture**:

* **Django REST** acts as the *System of Record*
* **FastAPI services** handle async, compute‑heavy, or experimental workloads
* **Simulation modules** stress‑test incentives and trust models offline

```
Clients / Scripts
        │
        ▼
Django REST API (Core Platform)
        │
        ├── PostgreSQL + PostGIS (Metadata)
        ├── Object Storage (Media)
        │
        ▼
FastAPI Services (Async / Compute)
        │
        ├── Verification Signals
        ├── Reward Calculation
        │
        ▼
Simulation & Analysis Layer
```

---

## 3. Core Components

### 3.1 Django REST – System of Record

**Responsibilities:**

* Event and claim lifecycle management
* Contributor profiles and reputation state
* Evidence metadata persistence
* Authorization and permissions

**Rationale:**
Django provides a stable ORM, migrations, and admin tooling, making it suitable as the authoritative data layer.

---

### 3.2 FastAPI Services – Compute & Experimentation

FastAPI services are intentionally isolated to allow:

* Independent scaling
* Async processing
* Rapid experimentation without destabilizing core data

#### a) Verification Service

Handles:

* Media metadata inspection
* Integrity and consistency checks
* Signal generation (not final judgments)

This service **does not determine truth**; it emits probabilistic or heuristic signals.

#### b) Reward Service

Handles:

* Demand–supply‑based reward calculation
* Time‑aware incentive adjustments
* Reputation‑weighted payouts

Reward logic is kept outside Django to avoid tight coupling with persistence.

---

## 4. Data Flow: Event Lifecycle

1. **Event Creation**

   * Event or claim registered in Django
   * Initial uncertainty is high

2. **Evidence Submission**

   * Contributors upload media
   * Metadata stored in PostgreSQL
   * Media stored in object storage

3. **Verification Signals**

   * FastAPI verification service analyzes metadata
   * Emits confidence and consistency signals

4. **Reward Calculation**

   * Reward service evaluates demand vs supply
   * Contributor rewards adjusted dynamically

5. **Aggregation & Review**

   * Django aggregates signals
   * Human‑in‑the‑loop moderation assumed

---

## 5. Demand–Supply Incentive Model (Architectural View)

Key architectural decision:

> Incentive logic is treated as a **pure function of system state**, not as a side effect of user actions.

Inputs:

* Event uncertainty
* Submission volume
* Temporal demand curve
* Contributor reputation

Outputs:

* Reward multipliers
* Diminishing returns for redundant evidence

This allows:

* Replay‑based testing
* Deterministic simulation
* Easier auditing

---

## 6. Simulation Architecture

Simulation runs **outside live request paths**.

Components:

* Synthetic event generator
* Contributor behavior models
* Attack scenario definitions
* Metric collectors

Simulations replay event timelines to observe:

* Incentive stability
* Abuse success rates
* Convergence behavior

---

## 7. Trust Boundaries & Failure Isolation

| Boundary         | Purpose                                            |
| ---------------- | -------------------------------------------------- |
| Django ↔ FastAPI | Prevent compute failures from corrupting core data |
| Media storage    | Isolate large binary handling                      |
| Simulation       | Avoid mixing experimental logic with live flows    |

Failure in FastAPI services **must not** invalidate persisted data.

---

## 8. API Boundaries (High-Level)

### Core API (Django REST)
- User identity and contributor profiles
- Claims and events
- Evidence metadata
- Reward state persistence

### Verification Service (FastAPI)
- Media analysis pipeline
- Integrity signals
- Evidence scoring

### Reward Service (FastAPI)
- Reward computation
- Simulation endpoints
- Replay and auditing

---

## 9. Security & Safety Considerations

* No public endpoints exposed
* No real user data processed
* JWT used only for local testing
* Rate‑limiting and abuse prevention are *conceptual only*

The architecture assumes additional safeguards would be required for real deployment.

---

## 10. Scalability (Conceptual)

While not implemented, the architecture supports:

* Horizontal scaling of FastAPI services
* CDN‑backed media delivery
* Partitioning by geography or event type

Scalability is discussed as a **design exercise**, not a performance claim.

---

## 11. Known Architectural Limitations

Authentication, authorization, and throttling are intentionally relaxed during prototyping and will be enforced at the API and gateway level in later stages.

* No strong identity guarantees
* No cryptographic media provenance
* Reputation bootstrapping remains unresolved
* Simulation accuracy depends on assumptions

These limitations are intentionally documented.

---

## 12. Why This Architecture Matters

This design emphasizes:

* Explicit uncertainty handling
* Separation of trust‑critical data from heuristics
* Incentive experimentation without user harm

The architecture is intended as a **thinking tool**, not a deployment blueprint.

---

## 13. Disclaimer

This architecture document represents a personal research exercise and should not be interpreted as a production recommendation or policy guidance.
