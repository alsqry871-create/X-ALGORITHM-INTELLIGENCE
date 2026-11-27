"""
Temporal analysis engine for X-ALGORITHM-INTELLIGENCE.
"""

from datetime import datetime
from typing import Optional, Iterable

from .schema import PostRecord


def calculate_post_age(
    post_time: datetime,
    reference_time: Optional[datetime] = None,
) -> float:
    """Calculate post age in hours."""

    if not isinstance(post_time, datetime):
        raise TypeError("post_time must be datetime")

    reference_time = reference_time or datetime.now(
        tz=post_time.tzinfo
    )

    if not isinstance(reference_time, datetime):
        raise TypeError("reference_time must be datetime")

    age = (reference_time - post_time).total_seconds() / 3600

    if age < 0:
        raise ValueError("Post time cannot be in the future")

    return age


def calculate_engagement_velocity(
    post: PostRecord,
    reference_time: Optional[datetime] = None,
) -> Optional[float]:
    """Calculate average engagements per hour."""

    if not isinstance(post, PostRecord):
        raise TypeError("post must be a PostRecord")

    post.validate()

    age = calculate_post_age(
        post.created_at,
        reference_time,
    )

    if age == 0:
        return None

    return post.total_engagements() / age


def analyze_post_timing(
    post: PostRecord,
    reference_time: Optional[datetime] = None,
) -> dict:
    """Analyze temporal properties of a post."""

    if not isinstance(post, PostRecord):
        raise TypeError("post must be a PostRecord")

    post.validate()

    age = calculate_post_age(
        post.created_at,
        reference_time,
    )

    return {
        "post_id": post.post_id,
        "post_age_hours": age,
        "publishing_hour": post.created_at.hour,
        "publishing_weekday": post.created_at.weekday(),
        "engagement_velocity": calculate_engagement_velocity(
            post,
            reference_time,
        ),
    }


def analyze_post_batch(
    posts: Iterable[PostRecord],
    reference_time: Optional[datetime] = None,
) -> list:
    """Analyze temporal properties of multiple posts."""

    return [
        analyze_post_timing(post, reference_time)
        for post in posts
    ]


def filter_recent_posts(
    posts: Iterable[PostRecord],
    hours: float = 24,
    reference_time: Optional[datetime] = None,
) -> list:
    """Return posts created within the specified time window."""

    if hours < 0:
        raise ValueError("hours cannot be negative")

    recent_posts = []

    for post in posts:
        if not isinstance(post, PostRecord):
            raise TypeError("All items must be PostRecord objects")

        age = calculate_post_age(
            post.created_at,
            reference_time,
        )

        if age <= hours:
            recent_posts.append(post)

    return recent_posts
