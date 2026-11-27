"""
Recommendation Analysis Engine
X-ALGORITHM-INTELLIGENCE

Experimental research engine for analyzing
candidate posts and recommendation signals.
"""

from typing import List, Dict, Any

from .schema import PostRecord
from .features import extract_post_features


def analyze_recommendation(post: PostRecord) -> Dict[str, Any]:
    """Analyze recommendation signals for one post."""

    features = extract_post_features(post)

    engagement_rate = features["engagement_rate"]
    out_of_network_rate = features["out_of_network_rate"]
    repost_rate = features["repost_rate"]
    reply_rate = features["reply_rate"]

    return {
        "post_id": post.post_id,
        "author_id": post.author_id,
        "engagement_rate": engagement_rate,
        "out_of_network_rate": out_of_network_rate,
        "repost_rate": repost_rate,
        "reply_rate": reply_rate,
        "has_media": post.has_media,
        "follower_count": post.follower_count,
    }


def analyze_candidates(
    posts: List[PostRecord]
) -> List[Dict[str, Any]]:
    """Analyze a collection of candidate posts."""

    if not isinstance(posts, list):
        raise TypeError("posts must be a list")

    return [
        analyze_recommendation(post)
        for post in posts
    ]


def rank_recommendation_candidates(
    posts: List[PostRecord]
) -> List[Dict[str, Any]]:
    """Sort candidates using experimental research signals."""

    results = analyze_candidates(posts)

    def score(item):
        engagement = item["engagement_rate"] or 0
        out_of_network = item["out_of_network_rate"] or 0
        reposts = item["repost_rate"] or 0
        replies = item["reply_rate"] or 0

        return (
            engagement * 0.40
            + out_of_network * 0.30
            + reposts * 0.20
            + replies * 0.10
        )

    for item in results:
        item["experimental_score"] = round(score(item), 6)

    return sorted(
        results,
        key=lambda item: item["experimental_score"],
        reverse=True,
    )
