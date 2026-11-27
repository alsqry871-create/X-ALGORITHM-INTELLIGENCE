"""Data schemas for X-ALGORITHM-INTELLIGENCE."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class EngagementMetrics:
    likes: int = 0
    replies: int = 0
    reposts: int = 0
    quotes: int = 0
    bookmarks: int = 0
    link_clicks: int = 0
    profile_visits: int = 0

    def validate(self):
        for name, value in self.__dict__.items():
            if not isinstance(value, int) or isinstance(value, bool):
                raise TypeError(f"{name} must be an integer")

            if value < 0:
                raise ValueError(f"{name} cannot be negative")


@dataclass
class AudienceMetrics:
    impressions: int = 0
    follower_impressions: Optional[int] = None
    non_follower_impressions: Optional[int] = None

    def validate(self):
        values = {
            "impressions": self.impressions,
            "follower_impressions": self.follower_impressions,
            "non_follower_impressions": self.non_follower_impressions,
        }

        for name, value in values.items():
            if value is not None:
                if not isinstance(value, int) or isinstance(value, bool):
                    raise TypeError(f"{name} must be an integer")

                if value < 0:
                    raise ValueError(f"{name} cannot be negative")

        if (
            self.follower_impressions is not None
            and self.non_follower_impressions is not None
            and self.follower_impressions
            + self.non_follower_impressions
            > self.impressions
        ):
            raise ValueError(
                "Audience impressions exceed total impressions"
            )


@dataclass
class PostRecord:
    post_id: str
    author_id: str
    created_at: datetime
    text: str = ""
    follower_count: int = 0

    engagement: EngagementMetrics = field(
        default_factory=EngagementMetrics
    )

    audience: AudienceMetrics = field(
        default_factory=AudienceMetrics
    )

    has_media: bool = False
    hashtags: List[str] = field(default_factory=list)
    is_reply: bool = False
    is_repost: bool = False
    link: Optional[str] = None

    def validate(self):
        if not self.post_id:
            raise ValueError("post_id is required")

        if not self.author_id:
            raise ValueError("author_id is required")

        if not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be datetime")

        if (
            not isinstance(self.follower_count, int)
            or isinstance(self.follower_count, bool)
        ):
            raise TypeError(
                "follower_count must be an integer"
            )

        if self.follower_count < 0:
            raise ValueError(
                "follower_count cannot be negative"
            )

        if not isinstance(self.text, str):
            raise TypeError("text must be a string")

        if not isinstance(self.engagement, EngagementMetrics):
            raise TypeError(
                "engagement must be EngagementMetrics"
            )

        if not isinstance(self.audience, AudienceMetrics):
            raise TypeError(
                "audience must be AudienceMetrics"
            )

        if not isinstance(self.has_media, bool):
            raise TypeError("has_media must be boolean")

        if not isinstance(self.hashtags, list):
            raise TypeError("hashtags must be a list")

        if not all(
            isinstance(tag, str) for tag in self.hashtags
        ):
            raise TypeError(
                "All hashtags must be strings"
            )

        self.engagement.validate()
        self.audience.validate()

    def total_engagement(self) -> int:
        """Calculate total recorded engagement."""

        return (
            self.engagement.likes
            + self.engagement.replies
            + self.engagement.reposts
            + self.engagement.quotes
            + self.engagement.bookmarks
            + self.engagement.link_clicks
            + self.engagement.profile_visits
        )
