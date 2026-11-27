"""
Feature Engineering Engine
X-ALGORITHM-INTELLIGENCE

Independent research tools for analyzing post engagement,
audience distribution, and recommendation-related features.
"""

from math import log1p
from typing import Dict, List, Optional, Any

from .schema import PostRecord


def safe_divide(
    numerator: float,
    denominator: float
) -> Optional[float]:
    """Safely divide two numeric values."""

    if denominator == 0:
        return None

    return numerator / denominator


def extract_engagement_features(
    post: PostRecord
) -> Dict[str, Optional[float]]:
    """Extract engagement-related features."""

    engagement = post.engagement
    impressions = post.audience.impressions

    total_engagement = post.total_engagements()

    return {
        "likes": engagement.likes,
        "replies": engagement.replies,
        "reposts": engagement.reposts,
        "quotes": engagement.quotes,
        "bookmarks": engagement.bookmarks,
        "link_clicks": engagement.link_clicks,
        "profile_visits": engagement.profile_visits,

        "total_engagement": total_engagement,

        "engagement_rate": safe_divide(
            total_engagement,
            impressions
        ),

        "like_rate": safe_divide(
            engagement.likes,
            impressions
        ),

        "reply_rate": safe_divide(
            engagement.replies,
            impressions
        ),

        "repost_rate": safe_divide(
            engagement.reposts,
            impressions
        ),

        "bookmark_rate": safe_divide(
            engagement.bookmarks,
            impressions
        ),

        "click_rate": safe_divide(
            engagement.link_clicks,
            impressions
        ),

        "profile_visit_rate": safe_divide(
            engagement.profile_visits,
            impressions
        ),
    }


def extract_audience_features(
    post: PostRecord
) -> Dict[str, Optional[float]]:
    """Extract audience distribution features."""

    audience = post.audience

    impressions = audience.impressions

    follower_impressions = audience.follower_impressions

    non_follower_impressions = (
        audience.non_follower_impressions
    )

    return {
        "impressions": impressions,

        "follower_impressions": follower_impressions,

        "non_follower_impressions": non_follower_impressions,

        "out_of_network_rate": safe_divide(
            non_follower_impressions,
            impressions
        ) if non_follower_impressions is not None else None,

        "follower_reach_rate": safe_divide(
            follower_impressions,
            impressions
        ) if follower_impressions is not None else None,

        "reach_to_followers_ratio": safe_divide(
            impressions,
            post.follower_count
        ),
    }


def extract_content_features(
    post: PostRecord
) -> Dict[str, Any]:
    """Extract basic content characteristics."""

    text = post.text or ""

    words = text.split()

    return {
        "text_length": len(text),

        "word_count": len(words),

        "hashtag_count": len(post.hashtags),

        "has_media": int(post.has_media),

        "is_reply": int(post.is_reply),

        "is_repost": int(post.is_repost),

        "follower_count": post.follower_count,

        "log_follower_count": log1p(
            post.follower_count
        ),

        "post_hour": post.created_at.hour,

        "post_weekday": post.created_at.weekday(),
    }


def extract_post_features(
    post: PostRecord
) -> Dict[str, Any]:
    """
    Extract all research features from one post.

    The function validates the input before extraction.
    """

    if not isinstance(post, PostRecord):
        raise TypeError(
            "post must be an instance of PostRecord"
        )

    post.validate()

    features = {}

    features.update(
        extract_engagement_features(post)
    )

    features.update(
        extract_audience_features(post)
    )

    features.update(
        extract_content_features(post)
    )

    return features


def extract_batch_features(
    posts: List[PostRecord]
) -> List[Dict[str, Any]]:
    """Extract features from multiple posts."""

    if not isinstance(posts, list):
        raise TypeError("posts must be a list")

    results = []

    for index, post in enumerate(posts):

        try:
            features = extract_post_features(post)

            results.append(features)

        except (TypeError, ValueError) as error:

            raise ValueError(
                f"Feature extraction failed at index "
                f"{index}: {error}"
            ) from error

    return results
