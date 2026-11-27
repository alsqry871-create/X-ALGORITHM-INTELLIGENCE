"""X-ALGORITHM-INTELLIGENCE package."""

from .schema import (
    PostRecord,
    EngagementMetrics,
    AudienceMetrics,
)

from .features import (
    safe_divide,
    extract_post_features,
    extract_batch_features,
    extract_engagement_features,
)

__all__ = [
    "PostRecord",
    "EngagementMetrics",
    "AudienceMetrics",
    "safe_divide",
    "extract_post_features",
    "extract_batch_features",
    "extract_engagement_features",
]
