"""
Core pipeline module - Backward compatibility layer.

This module provides backward compatibility by importing from the new PrismQ structure.
All new code should import directly from PrismQ subprojects.
"""

# Note: This module provides lazy imports for backward compatibility
# Heavy modules are imported on-demand to avoid unnecessary dependencies

def __getattr__(name):
    """Lazy import for backward compatibility."""
    # Map old imports to new PrismQ locations
    if name in ('IdeaAdapter', 'IdeaGenerator', 'merge_and_save_all_ideas'):
        from PrismQ.IdeaScraper.idea_generation import IdeaAdapter, IdeaGenerator, merge_and_save_all_ideas  # noqa: F401
        return locals()[name]
    elif name == 'TopicClusterer':
        from PrismQ.IdeaScraper.topic_clustering import TopicClusterer  # noqa: F401
        return TopicClusterer
    elif name == 'TitleGenerator':
        from PrismQ.StoryTitleProcessor.title_generation import TitleGenerator  # noqa: F401
        return TitleGenerator
    elif name == 'TitleScorer':
        from PrismQ.StoryTitleScoring.title_scoring import TitleScorer  # noqa: F401
        return TitleScorer
    elif name == 'TopSelector':
        from PrismQ.StoryTitleScoring.top_selection import TopSelector  # noqa: F401
        return TopSelector
    elif name == 'VoiceRecommender':
        from PrismQ.VoiceOverGenerator.voice_recommendation import VoiceRecommender  # noqa: F401
        return VoiceRecommender
    elif name in ('VoiceCloner', 'VoiceProfile'):
        from PrismQ.VoiceOverGenerator.voice_cloning import VoiceCloner, VoiceProfile  # noqa: F401
        return locals()[name]
    elif name in ('StyleChecker', 'ConsistencyReport'):
        from PrismQ.StoryGenerator.style_consistency import StyleChecker, ConsistencyReport  # noqa: F401
        return locals()[name]
    
    raise AttributeError(f"module 'core.pipeline' has no attribute '{name}'")
