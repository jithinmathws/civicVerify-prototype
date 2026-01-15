# CrowdVerify

This project explores how to build a scalable, crowdsourced fact-checking platform where contributors upload multimedia evidence (photos, videos, metadata) to verify claims. Evidence is validated through AI-assisted checks and human moderation, with contributors rewarded dynamically based on demand–supply dynamics, timeliness, and quality.

CrowdVerify is an exploratory backend prototype for a **crowdsourced media verification platform**.
It explores how distributed contributors can submit evidence for real-world events, and how
incentives, verification signals, and system design interact under uncertainty.

This project is maintained as a **personal research and learning initiative**, with a focus on:
- System design
- Trust and incentive modeling
- Media verification workflows

It is **not** a production system.

---

## High-Level Overview

The system is designed around:
- A core system of record for users, claims, and evidence
- Independent services for media verification and reward computation
- Simulation-driven evaluation of incentive behavior

The architecture favors clarity and auditability over optimization.

---

## Documentation

- [Design Documents](docs/README.md)
  - [System Architecture](docs/architecture.md)
  - [Reward Algorithm](docs/reward_algorithm.md)

---

## Tech Stack (Prototype)

- Django REST Framework (core data & APIs)
- FastAPI (verification and reward services)
- PostgreSQL + object storage (media metadata)
- Containerized local setup (Docker)

---

## Status

This project is currently in **early prototype development**.
Design documents describe intent and assumptions and may evolve.

---

## Disclaimer

This repository represents a personal technical exploration.
It does not reflect the policies, views, or systems of any organization.
