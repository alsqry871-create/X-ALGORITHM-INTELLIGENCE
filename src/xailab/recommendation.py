import unittest
from datetime import datetime

from src.xailab.schema import (
    PostRecord,
    EngagementMetrics,
    AudienceMetrics,
)

from src.xailab.recommendation import (
    analyze_recommendation,
    analyze_candidates,
    rank_recommendation_candidates,
)


class TestRecommendationEngine(unittest.TestCase):

    def create_post(self, post_id, likes, reposts, impressions,
                    non_follower_impressions):

        return PostRecord(
            post_id=post_id,
            author_id="user1",
            created_at=datetime(2026, 11, 27, 12, 0),
            text="Research post",
            follower_count=1000,
            engagement=EngagementMetrics(
                likes=likes,
                reposts=reposts,
            ),
            audience=AudienceMetrics(
                impressions=impressions,
                follower_impressions=(
                    impressions - non_follower_impressions
                ),
                non_follower_impressions=non_follower_impressions,
            ),
        )

    def test_analyze_recommendation(self):
        post = self.create_post("101", 100, 30, 2000, 1200)

        result = analyze_recommendation(post)

        self.assertEqual(result["post_id"], "101")
        self.assertEqual(result["engagement_rate"], 0.065)
        self.assertEqual(result["out_of_network_rate"], 0.6)

    def test_analyze_candidates(self):
        posts = [
            self.create_post("101", 100, 30, 2000, 1200),
            self.create_post("102", 50, 10, 1000, 300),
        ]

        results = analyze_candidates(posts)

        self.assertEqual(len(results), 2)

    def test_rank_candidates(self):
        posts = [
            self.create_post("101", 100, 30, 2000, 1200),
            self.create_post("102", 50, 10, 1000, 300),
        ]

        results = rank_recommendation_candidates(posts)

        self.assertEqual(len(results), 2)
        self.assertIn("experimental_score", results[0])

        scores = [
            item["experimental_score"]
            for item in results
        ]

        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            analyze_candidates("invalid")


if __name__ == "__main__":
    unittest.main()
