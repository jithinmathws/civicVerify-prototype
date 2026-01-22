# Contributors App

The Contributors app manages contributor-specific domain logic for the CivicVerify platform.
It extends the core user model with contributor identity, reputation tracking, and access control primitives used by verification and moderation workflows.

This app is intentionally separated from authentication to keep concerns clear:
    - users / auth → identity & access
    - contributors → trust, reputation, and contribution history

## Purpose

The Contributors app is responsible for:
    - Representing a Contributor profile linked to a user
    - Tracking reputation score changes over time
    - Enforcing contributor-specific permissions and access rules
    - Providing APIs for contributors to view and manage their own profile
    - Supporting future verification, moderation, and incentive systems

It does not:
    - Handle authentication
    - Implement claim or evidence logic
    - Compute final rewards (planned for separate services)

# Core Models
## Contributor

Represents a verified participant in the platform.

### Key fields

    - user – One-to-one link to the custom User model
    - display_name – Public-facing contributor name
    - bio – Optional profile description
    - reputation_score – Aggregate trust score (float)
    - is_active – Whether the contributor can participate

A contributor profile is automatically created via signals when a user is created.

## ReputationLog

An immutable audit log of reputation changes.

### Purpose

    - Transparency
    - Debugging trust evolution
    - Future explainability of rewards and moderation decisions

### Key fields

    - contributor
    - change – Positive or negative delta
    - reason – Human-readable explanation
    - created_at

## Signals

The app uses Django signals to enforce invariants:
    - Auto-create Contributor Profile on User Creation
    - Prevent duplicate contributor profiles (OneToOne enforced)

Signals live in:
    - contributors/signals.py

Tests ensure:
    - Profile is created exactly once
    - No duplication on repeated saves
    - Signal behavior can be safely disconnected for isolated tests

## Services & Domain Logic

Business logic is intentionally kept out of views.

Examples:
    - Contributor.adjust_reputation(change, reason)
    - Reputation logging and aggregation
    - Future hooks for verification success/failure

This separation allows:
    - Easier testing
    - Future migration to background jobs or external services

## API Views

The app currently exposes read-oriented APIs:

### MyContributorProfileView

    - Retrieve / update the authenticated contributor’s profile
    - Owner-only access
    - Requires active contributor status

### MyContributorReputationView

    - Returns reputation score
    - Includes recent reputation activity
    - Read-only analytics endpoint

All access is enforced via custom DRF permissions.

## Permissions

Custom permission classes enforce contributor-specific rules:
    - IsContributorOwner
    - IsActiveContributor
    - IsTargetContributorActive

Permissions are:
    - Defined in permissions.py
    - Applied explicitly in views
    - Designed to be reusable across apps (claims, evidence, moderation)

## Admin Integration

The admin interface supports:
    - Contributor profile inspection
    - Reputation audit review
    - Safe read-only visibility into trust evolution

This is intended for research, debugging, and moderation simulations, not full admin tooling.

## Testing Strategy

The Contributors app includes tests for:
    - Models (Contributor, ReputationLog)
    - Signals (auto-creation and invariants)
    - Permissions
    - API views (authenticated access only)

Testing principles:
    - Signals are respected (no manual duplication)
    - Database integrity is enforced
    - Tests model real production behavior

Run tests with:
    python manage.py test apps.contributors

## Design Philosophy

This app prioritizes:
    - Auditability over optimization
    - Explicit domain modeling
    - Clear separation of concerns
    - Future extensibility

It is designed to evolve alongside:
    - Claim verification workflows
    - Incentive algorithms
    - Moderation and dispute resolution systems

## Status

🚧 Prototype / Research Phase

The Contributors app is under active iteration.
Interfaces, reputation semantics, and thresholds may evolve as system design matures.