from django.utils import timezone

def record_successful_verification(contributor, *, delta=0.1):
    contributor.trust_score = max(0.0, contributor.trust_score + delta)
    contributor.total_contributions += 1
    contributor.last_contribution_at = timezone.now()
    contributor.save(
        update_fields=[
            "trust_score",
            "total_contributions",
            "last_contribution_at",
        ]
    )