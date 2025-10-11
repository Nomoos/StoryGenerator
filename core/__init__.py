"""
Core module - Backward compatibility layer.

This module provides backward compatibility by importing from the new PrismQ structure.
All new code should import directly from PrismQ subprojects.
"""

# Lazy imports for backward compatibility to avoid unnecessary dependencies
def __getattr__(name):
    """Lazy import for backward compatibility."""
    # Shared modules
    if name in dir(__import__('PrismQ.Shared.cache', fromlist=[name])):
        from PrismQ.Shared import cache
        return getattr(cache, name)
    elif name in dir(__import__('PrismQ.Shared.config', fromlist=[name])):
        from PrismQ.Shared import config
        return getattr(config, name)
    elif name in dir(__import__('PrismQ.Shared.database', fromlist=[name])):
        from PrismQ.Shared import database
        return getattr(database, name)
    elif name in dir(__import__('PrismQ.Shared.errors', fromlist=[name])):
        from PrismQ.Shared import errors
        return getattr(errors, name)
    elif name in dir(__import__('PrismQ.Shared.logging', fromlist=[name])):
        from PrismQ.Shared import logging
        return getattr(logging, name)
    elif name in dir(__import__('PrismQ.Shared.models', fromlist=[name])):
        from PrismQ.Shared import models
        return getattr(models, name)
    elif name in dir(__import__('PrismQ.Shared.retry', fromlist=[name])):
        from PrismQ.Shared import retry
        return getattr(retry, name)
    elif name in dir(__import__('PrismQ.Shared.validation', fromlist=[name])):
        from PrismQ.Shared import validation
        return getattr(validation, name)
    
    # Check submodules
    try:
        from PrismQ.StoryGenerator import script_development
        if hasattr(script_development, name):
            return getattr(script_development, name)
    except (ImportError, AttributeError):
        pass
    
    try:
        from PrismQ.VoiceOverGenerator import audio_production
        if hasattr(audio_production, name):
            return getattr(audio_production, name)
    except (ImportError, AttributeError):
        pass
    
    try:
        from PrismQ.SceneDescriptions import scene_planning
        if hasattr(scene_planning, name):
            return getattr(scene_planning, name)
    except (ImportError, AttributeError):
        pass
    
    raise AttributeError(f"module 'core' has no attribute '{name}'")
