"""
Feature Engineering Engine
X-ALGORITHM-INTELLIGENCE

Research tools for analyzing post engagement,
audience distribution, and recommendation signals.
"""

from typing import Dict, List, Optional

from .schema import PostRecord


def safe_divide(
    numerator: float,
    denominator: float
) -> Optional[float]:
    """Safely divide two numeric values."""

    if denominator == 0:
        return None

    return numerator / denominator


def extract_post_features(
    post: PostRecord
) -> Dict[str, Optional[float]]:
    """Extract analytical features from a post."""

    if not isinstance(post, PostRecord):
        raise TypeError("post must be a PostRecord")

    post.validate()

    engagement = post.engagement
    audience = post.audience

    total_engagement = post.total_engagement()
    impressions = audience.impressions

    engagement_rate = safe_divide(
        total_engagement,
        impressions
    )

    like_rate = safe_divide(
        engagement.likes,
        impressions
    )

    reply_rate = safe_divide(
        engagement.replies,
        impressions
    )

    repost_rate = safe_divide(
        engagement.reposts,
        impressions
    )

    out_of_network_rate = safe_divide(
        audience.non_follower_impressions,
        impressions
    ) if audience.non_follower_impressions is not None else None

    follower_reach_rate = safe_divide(
        audience.follower_impressions,
        impressions
    ) if audience.follower_impressions is not None else None

    return {
        "follower_count": post.follower_count,
        "impressions": impressions,

        "likes": engagement.likes,
        "replies": engagement.replies,
        "reposts": engagement.reposts,
        "quotes": engagement.quotes,
        "bookmarks": engagement.bookmarks,

        "total_engagement": total_engagement,

        "engagement_rate": engagement_rate,
        "like_rate": like_rate,
        "reply_rate": reply_rate,
        "repost_rate": repost_rate,

        "out_of_network_rate": out_of_network_rate,
        "follower_reach_rate": follower_reach_rate,

        "has_media": int(post.has_media),
        "hashtag_count": len(post.hashtags),

        "is_reply": int(post.is_reply),
        "is_repost": int(post.is_repost),

        "text_length": len(post.text),
    }


def extract_batch_features(
    posts: List[PostRecord]
) -> List[Dict[str, Optional[float]]]:
    """Extract features from multiple posts."""

    if not isinstance(posts, list):
        raise TypeError("posts must be a list")

    return [
        extract_post_features(post)
        for post in posts
    ]


def extract_engagement_features(
    post: PostRecord
) -> Dict[str, Optional[float]]:
    """Extract engagement-specific features."""

    features = extract_post_features(post)

    return {
        key: value
        for key, value in features.items()
        if key in {
            "likes",
            "replies",
            "reposts",
            "quotes",
            "bookmarks",
            "total_engagement",
            "engagement_rate",
            "like_rate",
            "reply_rate",
            "repost_rate",
        }
    }
