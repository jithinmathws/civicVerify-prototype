# CrowdVerify

CrowdVerify is an exploratory backend prototype for a **crowdsourced media verification platform**.
It investigates how distributed contributors can submit multimedia evidence (photos, videos, metadata)
to verify real-world claims, and how AI-assisted checks, human moderation, and incentive design interact
under uncertainty.

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

The architecture favors clarity, auditability, and reasoning about incentives
over performance optimization or feature completeness.

---

## Documentation

Design documents describe architectural intent, assumptions, and tradeoffs.
They are expected to evolve as the prototype develops.

- [Design Documents](docs/README.md)
  - [System Architecture](docs/architecture.md)
  - [Reward Algorithm](docs/reward_algorithm.md)
  - [Django Apps](backend_django/apps/README.md)
    - [Common App](backend_django/apps/common/README.md)

---

## Tech Stack (Prototype)

- Django REST Framework (core system of record & APIs)
- FastAPI (isolated verification and reward computation services)
- PostgreSQL + object storage (media metadata)
- Containerized local development (Docker)

---

## Status

This project is currently in **early prototype development**.
Design documents describe intent and assumptions and may evolve.

---

## Disclaimer

This repository represents a personal technical exploration.
It does not reflect the policies, views, or systems of any current or former employer.
