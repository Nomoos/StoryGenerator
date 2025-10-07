"""
Social Trends Package - Multi-platform trend aggregation system

A modular, extensible package for gathering trending content from multiple sources:
- YouTube Data API v3
- Google Trends (via pytrends)
- TikTok (via third-party APIs)
- Instagram (via official/business APIs)
- Exploding Topics

Design Principles:
- Modular: Each source is a plug-in implementing ITrendSource
- Atomic: Small, focused classes and methods (SRP)
- Extensible: Open/Closed principle for new sources
- Async-first: All I/O operations use async/await
- DI everywhere: Dependency injection for testability
"""

__version__ = "0.1.0"

from social_trends.interfaces import TrendItem, TrendSource

# Pipeline and sources require external dependencies, import only when needed
__all__ = ["TrendItem", "TrendSource"]
