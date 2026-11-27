"""
Temporal Analysis Engine
X-ALGORITHM-INTELLIGENCE

Research tools for analyzing post timing
and engagement development over time.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from .schema import PostRecord


def calculate_post_age(
    created_at: datetime,
    reference_time: Optional[datetime] = None,
) -> float:
    """Calculate post age in hours."""

    if not isinstance(created_at, datetime):
        raise TypeError("created_at must be datetime")

    if reference_time is None:
        reference_time = datetime.now(created_at.tzinfo)

    if not isinstance(reference_time, datetime):
        raise TypeError("reference_time must be datetime")

    if created_at.tzinfo != reference_time.tzinfo:
        raise ValueError("Datetime timezone information must match")

    age = (reference_time - created_at).total_seconds() / 3600

    return round(max(age, 0), 4)


def calculate_engagement_velocity(
    post: PostRecord,
    reference_time: Optional[datetime] = None,
) -> Optional[float]:
    """Calculate average engagement per hour."""

    post.validate()

    age_hours = calculate_post_age(
        post.created_at,
        reference_time,
    )

    if age_hours == 0:
        return None

    return round(post.total_engagement() / age_hours, 4)


def analyze_post_timing(
    post: PostRecord,
    reference_time: Optional[datetime] = None,
) -> Dict[str, Any]:
    """Extract temporal and engagement timing indicators."""

    post.validate()

    age_hours = calculate_post_age(
        post.created_at,
        reference_time,
    )

    return {
        "post_id": post.post_id,
        "created_at": post.created_at.isoformat(),
        "post_age_hours": age_hours,
        "engagement_velocity": calculate_engagement_velocity(
            post,
            reference_time,
        ),
        "publishing_hour": post.created_at.hour,
        "publishing_weekday": post.created_at.weekday(),
    }


def analyze_post_batch(
    posts: List[PostRecord],
    reference_time: Optional[datetime] = None,
) -> List[Dict[str, Any]]:
    """Analyze timing indicators for multiple posts."""

    if not isinstance(posts, list):
        raise TypeError("posts must be a list")

    return [
        analyze_post_timing(post, reference_time)
        for post in posts
    ]


def filter_recent_posts(
    posts: List[PostRecord],
    hours: float = 24,
    reference_time: Optional[datetime] = None,
) -> List[PostRecord]:
    """Return posts published within the selected time window."""

    if not isinstance(posts, list):
        raise TypeError("posts must be a list")

    if hours < 0:
        raise ValueError("hours cannot be negative")

    if reference_time is None:
        reference_time = datetime.now()

    cutoff = reference_time - timedelta(hours=hours)

    results = []

    for post in posts:
        post.validate()

        if post.created_at.tzinfo != cutoff.tzinfo:
            raise ValueError("Datetime timezone information must match")

        if cutoff <= post.created_at <= reference_time:
            results.append(post)

    return results
