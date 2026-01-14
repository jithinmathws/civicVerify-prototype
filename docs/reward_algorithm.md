## Related Design Documents

- [System Architecture](architecture.md)

# Reward Algorithm Design

> **Project:** CrowdVerify (Research Prototype)
> **Author:** Jithin Mathews
> **Status:** Exploratory / Conceptual (Non-production)

---

## 1. Purpose & Scope

This document describes the **conceptual reward algorithm** used in CrowdVerify to incentivize contributors to submit valuable evidence during real-world events.

The goal of the reward system is **not** to determine truth or guarantee fairness, but to:

* Encourage timely, high-signal contributions
* Discourage spam, redundancy, and low-effort submissions
* Adapt incentives dynamically as events evolve
* Make incentive behavior analyzable through simulation

This algorithm is designed as a **research artifact** and is intentionally conservative in scope.

---

## 2. Design Principles

The reward system follows these guiding principles:

1. **Marginal Value Over Volume**
   Contributors are rewarded for adding *new information*, not for submitting more data.

2. **Time Sensitivity**
   Early, high-quality evidence is more valuable than late or redundant evidence.

3. **Demand-Driven Incentives**
   Rewards scale with event uncertainty and civic impact, not popularity.

4. **Diminishing Returns**
   As supply increases, the reward for additional evidence decreases.

5. **Reputation-Weighted Influence**
   Historical reliability affects reward magnitude but does not fully exclude new contributors.

6. **Auditability Over Optimization**
   The algorithm favors transparency and replayability over maximal efficiency.

---

## 3. Core Concepts & Variables

### 3.1 Event Demand

Event demand represents the *current need for verification* and is modeled as a function of:

* Event recency
* Conflicting claims or reports
* Geographic or civic impact

Demand is highest during early or highly uncertain phases and decays over time.

---

### 3.2 Evidence Supply

Supply represents the *current volume and redundancy* of submitted evidence:

* Number of submissions
* Similarity between submissions
* Geographic clustering

High supply reduces marginal reward value.

---

### 3.3 Evidence Novelty

Novelty captures how much a submission contributes new information:

* Independent vantage point
* Distinct timing
* Unique metadata patterns

Novelty is evaluated heuristically and produces a normalized score.

---

### 3.4 Contributor Reliability

Contributor reliability is an evolving signal based on:

* Historical accuracy
* Dispute resolution outcomes
* Consistency over time

Reliability influences rewards multiplicatively but is capped to avoid entrenched dominance.

---

### 3.5 Temporal Weight

Time weighting reflects that:

* Early submissions are more valuable
* Late submissions face diminishing impact

Temporal decay is smooth rather than abrupt to avoid cliff effects.

---

## 4. Baseline Reward Function (Conceptual)

At a high level, rewards are modeled as:

```
Reward ∝ Demand × Novelty × Reliability × TimeWeight × SupplyAdjustment
```

Where:

* Each factor is normalized
* SupplyAdjustment decreases as redundancy increases
* The output represents *relative reward magnitude*, not currency

This formulation allows deterministic replay in simulation.

---

## 5. Event Lifecycle–Aware Incentives

The algorithm adapts incentives across an event’s lifecycle:

### Phase 1: Emergence

* High demand
* Low supply
* Strong rewards for primary evidence

### Phase 2: Acceleration

* Rising supply
* Conflicting claims
* Rewards favor independent confirmation

### Phase 3: Saturation

* Low marginal demand
* High redundancy
* Rewards shift toward synthesis and dispute resolution

This prevents late-stage spam and reward exploitation.

---

## 6. Abuse & Gaming Considerations

The design explicitly considers failure modes:

* **Spam Flooding:** Mitigated via diminishing returns
* **Collusion:** Reduced through diversity and novelty checks
* **Sybil Attacks:** Partially mitigated via capped reputation influence
* **Early Capture:** Temporal smoothing reduces winner-take-all effects

These mitigations are incomplete by design and are evaluated via simulation.

---

## 7. Simulation Strategy

Because real-world validation is not feasible, the reward algorithm is tested through simulation:

* Synthetic events with varying demand curves
* Contributor behavior models (honest, opportunistic, malicious)
* Controlled attack scenarios

Metrics observed:

* Reward distribution skew
* Signal-to-noise ratio
* Abuse success rates
* Convergence time

---

## 8. Known Limitations & Open Questions

* Identity and uniqueness assumptions are weak
* Reputation bootstrapping remains unresolved
* Novelty detection is heuristic
* Ethical implications of financial incentives require further study

These limitations are intentionally documented.

---

## 9. Non-Goals

This reward system does **not** aim to:

* Guarantee correctness
* Replace editorial judgment
* Eliminate misinformation
* Optimize contributor earnings

---

## 10. Conclusion

The reward algorithm in CrowdVerify is treated as a **policy-aware, time-sensitive incentive mechanism** rather than a payout formula.

Its primary value lies in enabling **experimentation, simulation, and critical evaluation** of incentive behavior under uncertainty.

---

## Disclaimer

This document represents a personal research exploration and should not be interpreted as a production-ready economic model or policy recommendation.
