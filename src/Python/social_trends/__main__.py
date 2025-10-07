"""
Main entry point for running the social_trends package as a module.

Usage:
    python -m social_trends --sources youtube,google_trends --region US --limit 50
"""

from social_trends.cli import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
