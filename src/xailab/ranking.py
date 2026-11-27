"""
Ranking Engine
X-ALGORITHM-INTELLIGENCE

Independent experimental ranking models.
"""

from typing import List, Dict, Any

from .schema import PostRecord


DEFAULT_WEIGHTS = {
    "likes": 1.0,
    "replies": 2.0,
    "reposts": 3.0,
    "quotes": 3.0,
    "bookmarks": 3.0,
    "link_clicks": 2.0,
    "profile_visits": 2.0,
}


def score_post(post: PostRecord) -> float:
    """Calculate an experimental post ranking score."""

    if not isinstance(post, PostRecord):
        raise TypeError("post must be a PostRecord")

    post.validate()

    engagement = post.engagement
    impressions = post.audience.impressions

    weighted_engagement = sum(
        getattr(engagement, metric) * weight
        for metric, weight in DEFAULT_WEIGHTS.items()
    )

    if impressions == 0:
        return 0.0

    engagement_score = weighted_engagement / impressions

    non_follower_rate = (
        post.audience.non_follower_impressions / impressions
        if post.audience.non_follower_impressions is not None
        else 0.0
    )

    final_score = (
        engagement_score * 0.7
        + non_follower_rate * 0.3
    )

    return round(final_score, 6)


def rank_posts(posts: List[PostRecord]) -> List[Dict[str, Any]]:
    """Rank posts by experimental recommendation score."""

    if not isinstance(posts, list):
        raise TypeError("posts must be a list")

    results = []

    for post in posts:
        results.append({
            "post_id": post.post_id,
            "author_id": post.author_id,
            "ranking_score": score_post(post),
        })

    return sorted(
        results,
        key=lambda item: item["ranking_score"],
        reverse=True,
    )
