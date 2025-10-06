"""
Sources package - Individual trend source implementations.

Each module is a plug-in that implements the TrendSource interface.
"""

from social_trends.sources.youtube import YouTubeSource
from social_trends.sources.google_trends import GoogleTrendsSource

# Stub implementations for future integration
from social_trends.sources.tiktok import TikTokSource
from social_trends.sources.instagram import InstagramSource
from social_trends.sources.exploding_topics import ExplodingTopicsSource

__all__ = [
    "YouTubeSource",
    "GoogleTrendsSource",
    "TikTokSource",
    "InstagramSource",
    "ExplodingTopicsSource",
]
