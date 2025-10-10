#!/usr/bin/env python3
"""
Example demonstrating infrastructure components.

Shows how to use configuration management and logging system.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.Python.config import get_settings
from src.Python.logging import get_logger, setup_logging


def main():
    """Demonstrate infrastructure usage."""
    # Setup logging first
    print("=" * 60)
    print("Infrastructure Demo: Configuration & Logging")
    print("=" * 60)
    print()

    # Initialize logging
    print("1. Setting up logging...")
    setup_logging(level="INFO", json_format=False)
    logger = get_logger(__name__)
    logger.info("Logging system initialized")
    print()

    # Get configuration
    print("2. Loading configuration...")
    settings = get_settings()
    logger.info("Configuration loaded")
    print()

    # Display configuration
    print("3. Configuration values:")
    print(f"   - Default Model: {settings.default_model}")
    print(f"   - Temperature: {settings.temperature}")
    print(f"   - Max Tokens: {settings.max_tokens}")
    print(f"   - Story Root: {settings.story_root}")
    print(f"   - Log Directory: {settings.log_dir}")
    print(f"   - Cache Directory: {settings.cache_dir}")
    print(f"   - Log Level: {settings.log_level}")
    print(f"   - Enable Cache: {settings.enable_cache}")
    print(f"   - Max Retries: {settings.max_retries}")
    print()

    # Demonstrate logging at different levels
    print("4. Demonstrating log levels:")
    logger.debug("This is a DEBUG message (not shown at INFO level)")
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")
    print()

    # Show that directories were created
    print("5. Verifying directories were created:")
    print(f"   - Story Root exists: {settings.story_root.exists()}")
    print(f"   - Log Directory exists: {settings.log_dir.exists()}")
    print(f"   - Cache Directory exists: {settings.cache_dir.exists()}")
    print()

    # Check log file
    log_file = settings.log_dir / "app.log"
    if log_file.exists():
        print(f"6. Log file created: {log_file}")
        print(f"   Log file size: {log_file.stat().st_size} bytes")
        print()
        print("   Last 5 lines of log file:")
        lines = log_file.read_text().strip().split("\n")
        for line in lines[-5:]:
            print(f"   {line}")
    else:
        print("6. Log file not yet created")
    print()

    print("=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)
    logger.info("Infrastructure demo completed")


if __name__ == "__main__":
    main()
