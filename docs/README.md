# Crowdsourced Fact‑Checking Platform (Research Prototype)

> **Status:** Exploratory / Research Prototype
> **Author:** Jithin Mathews
> **Purpose:** Portfolio project exploring system design, incentives, and failure modes in crowdsourced media verification

---

## 1. Overview

This project explores how a **crowdsourced, media‑based fact‑checking system** *could* be designed to support verification of real‑world events (e.g., breaking news, civic incidents) using user‑submitted photos, videos, and metadata.

The focus is **not** on building a production‑ready platform, but on:

* Designing scalable backend architecture
* Exploring incentive mechanisms under uncertainty
* Understanding trust, abuse, and verification challenges
* Demonstrating systems‑level thinking

The project is intentionally scoped as a **research and learning prototype** rather than a deployable product.

---

## 2. Problem Statement

Misinformation during rapidly developing events creates an **integrity gap**:

* Early information is scarce and unreliable
* Centralized moderation does not scale well in real time
* Valuable on‑the‑ground evidence often goes unverified or underutilized

While crowdsourcing can surface evidence quickly, it introduces challenges:

* Incentive gaming and spam
* Coordinated manipulation
* Uneven geographic participation
* Difficulty evaluating evidence quality at scale

This project investigates how **architecture, incentives, and trust models** might address these challenges.

---

## 3. Non‑Goals (Important)

This project explicitly does **not** attempt to:

* Launch a public platform
* Run real‑world pilots
* Handle real user data
* Claim empirical validation of effectiveness

All testing is performed via **simulation and synthetic data**.

---

## 4. High‑Level Architecture

**Core components:**

* **API Layer:** Event ingestion, media submission, verification actions
* **Media Processing:** Metadata extraction, basic integrity checks
* **Verification Engine:** Scoring, confidence aggregation, conflict detection
* **Incentive Engine:** Demand–supply‑based reward calculation
* **Simulation Engine:** Synthetic contributors, events, and attack scenarios
* **Visualization Layer:** Maps, timelines, reward curves

The system is designed as **loosely coupled services** to explore scalability and failure isolation.

---

## 5. Technology Stack (Planned / Partial)

* **Backend APIs:** Django REST Framework + FastAPI (hybrid exploration)
* **Media Processing:** FFmpeg, metadata extraction pipelines
* **Data Storage:**

  * PostgreSQL (metadata)
  * PostGIS (geospatial queries)
  * Object storage (media blobs)
* **Geospatial Visualization:** Mapbox
* **Orchestration (conceptual):** Kubernetes
* **Simulation & Analysis:** Python‑based simulation framework

> Note: Not all components are fully implemented; some are mocked or simulated to focus on design and reasoning.

---

## 6. Demand–Supply‑Based Incentive Design

A central focus of the project is **dynamic contributor incentives**.

### Core Principle

> Rewards should track **marginal verification value**, not volume.

### Key Signals

* **Verification Demand:**

  * Event recency
  * Uncertainty / conflicting claims
  * Civic impact

* **Supply Saturation:**

  * Number of submissions
  * Redundancy of evidence
  * Geographic concentration

### Simplified Reward Model

```
Final Reward = Base × Demand(t) × (1 − Supply(t)) × Contributor Reliability
```

Rewards evolve as an event develops, shifting incentives from:

* Early primary evidence
* Independent confirmation
* Conflict resolution and synthesis

---

## 7. Time‑Aware Event Lifecycle

The system models events across three phases:

1. **Emergence Phase**

   * Scarce information
   * High reward for unique, on‑site evidence

2. **Acceleration Phase**

   * Conflicting reports
   * Incentives favor independent verification

3. **Saturation Phase**

   * Evidence abundance
   * Incentives shift toward synthesis and dispute resolution

This prevents late‑stage spam and reduces incentive gaming.

---

## 8. Trust & Reputation Model

Contributor reliability is modeled using:

* Historical accuracy
* Dispute outcomes
* Diversity of confirmation
* Temporal consistency

Reputation:

* Multiplies rewards
* Limits abuse impact
* Encourages long‑term participation

---

## 9. Simulation‑Based Testing

Because real‑world testing is impractical and risky at small scale, the project relies on **simulation**.

### Simulated Actors

* Honest contributors
* Opportunistic contributors
* Malicious actors
* High‑reputation verifiers

### Tested Scenarios

* Breaking‑news demand spikes
* Evidence floods
* Coordinated misinformation attacks
* Reputation gaming attempts

### Metrics Observed

* Signal‑to‑noise ratio
* Reward distribution fairness
* Abuse success rates
* Convergence time toward consensus

---

## 10. Failure Modes & Limitations

Known limitations explored in this project:

* Sybil attacks under weak identity guarantees
* Geographic participation imbalance
* Collusion between contributors
* Over‑reliance on early evidence

These are **documented intentionally** as part of the learning outcome.

---

## 11. Ethical & Safety Considerations

* No real user data is collected
* No public deployment
* No automated truth labeling
* Human‑in‑the‑loop assumed for high‑impact decisions

The project treats misinformation mitigation as a **risk‑sensitive domain**.

---

## 12. What This Project Demonstrates

* Backend system design
* API design tradeoffs
* Incentive modeling
* Geospatial data handling
* Adversarial thinking
* Honest scoping and documentation

---

## 13. Future Work (Conceptual)

* More realistic contributor behavior models
* Better uncertainty estimation
* Integration with public datasets
* Formal incentive simulations

---

## 14. Disclaimer

This repository represents a **personal learning project** and does not reflect the views, policies, or systems of any organization. It should not be used as a production system or policy recommendation.

---

## 15. Prototype Scope & Components

This repository focuses on **design exploration and selective prototyping**, rather than feature completeness. Components fall into three categories to clearly distinguish what is implemented, simulated, or intentionally out of scope.

### Implemented / Partially Implemented

* Core system architecture and contributor workflow design
* Backend API prototyping (Django REST + FastAPI comparison)
* Multimedia ingestion and metadata handling (basic pipeline)
* Geospatial data modeling and querying concepts

### Simulated / Mocked

* Contributor behavior (honest, opportunistic, malicious actors)
* Demand–supply–based reward calculation under evolving events
* AI-assisted verification signals (conceptual placeholders)
* Event lifecycle progression and demand spikes

### Out of Scope (By Design)

* Public deployment or live pilots
* Real user data collection
* Production-grade moderation tools
* Fully automated truth classification

This scoping reflects the constraints of a single-developer research project and prioritizes **understanding system behavior, incentives, and failure modes**.

---

## 16. Contact

**Jithin Mathews**
GitHub: **

Feedback and discussion are welcome.
