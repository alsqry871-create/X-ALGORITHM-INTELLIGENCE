import unittest
from datetime import datetime, timedelta

from src.xailab.schema import (
    PostRecord,
    EngagementMetrics,
    AudienceMetrics,
)

from src.xailab.temporal import (
    calculate_post_age,
    calculate_engagement_velocity,
    analyze_post_timing,
    analyze_post_batch,
    filter_recent_posts,
)


class TestTemporalAnalysis(unittest.TestCase):

    def setUp(self):
        self.reference_time = datetime(2026, 11, 27, 12, 0)

    def create_post(self, post_id, hours_ago, likes=100):
        return PostRecord(
            post_id=post_id,
            author_id="user1",
            created_at=self.reference_time - timedelta(hours=hours_ago),
            text="Research post",
            follower_count=1000,
            engagement=EngagementMetrics(likes=likes),
            audience=AudienceMetrics(impressions=2000),
        )

    def test_calculate_post_age(self):
        post_time = self.reference_time - timedelta(hours=5)

        result = calculate_post_age(
            post_time,
            self.reference_time,
        )

        self.assertEqual(result, 5.0)

    def test_engagement_velocity(self):
        post = self.create_post("101", 2, likes=100)

        result = calculate_engagement_velocity(
            post,
            self.reference_time,
        )

        self.assertEqual(result, 50.0)

    def test_analyze_post_timing(self):
        post = self.create_post("102", 4)

        result = analyze_post_timing(
            post,
            self.reference_time,
        )

        self.assertEqual(result["post_id"], "102")
        self.assertEqual(result["post_age_hours"], 4.0)
        self.assertEqual(result["publishing_hour"], 8)

    def test_analyze_post_batch(self):
        posts = [
            self.create_post("101", 2),
            self.create_post("102", 4),
        ]

        results = analyze_post_batch(
            posts,
            self.reference_time,
        )

        self.assertEqual(len(results), 2)

    def test_filter_recent_posts(self):
        posts = [
            self.create_post("101", 2),
            self.create_post("102", 12),
            self.create_post("103", 48),
        ]

        results = filter_recent_posts(
            posts,
            hours=24,
            reference_time=self.reference_time,
        )

        self.assertEqual(len(results), 2)
        self.assertEqual(
            [post.post_id for post in results],
            ["101", "102"],
        )

    def test_zero_age_velocity(self):
        post = self.create_post("104", 0)

        result = calculate_engagement_velocity(
            post,
            self.reference_time,
        )

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
