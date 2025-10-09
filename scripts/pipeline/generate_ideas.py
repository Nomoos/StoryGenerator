#!/usr/bin/env python3
"""
Idea Generation Pipeline Script.

Orchestrates the complete idea generation pipeline:
1. Reddit story adaptation
2. LLM-based idea generation
3. Topic clustering
4. Title generation
5. Title scoring
6. Voice recommendation
7. Top selection

Usage:
    python -m scripts.pipeline.generate_ideas --gender women --age 18-23
    python -m scripts.pipeline.generate_ideas --all-segments
"""

import argparse
import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from core.pipeline.idea_generation import (
    IdeaAdapter,
    IdeaGenerator,
    merge_and_save_all_ideas
)
from core.pipeline.topic_clustering import TopicClusterer
from core.pipeline.title_generation import TitleGenerator
from core.pipeline.title_scoring import TitleScorer
from core.pipeline.voice_recommendation import VoiceRecommender
from core.pipeline.top_selection import TopSelector
from providers.mock_provider import MockLLMProvider

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_pipeline(
    gender: str,
    age_bucket: str,
    output_base: Path,
    llm_provider,
    reddit_stories: list = None,
    ideas_count: int = 20,
    titles_per_topic: int = 10,
    top_n: int = 5,
    mock_mode: bool = False
):
    """
    Run the complete idea generation pipeline.
    
    Args:
        gender: Target gender segment (e.g., 'women', 'men')
        age_bucket: Target age bucket (e.g., '18-23')
        output_base: Base output directory
        llm_provider: LLM provider instance
        reddit_stories: Optional list of Reddit stories to adapt
        ideas_count: Number of LLM ideas to generate
        titles_per_topic: Number of title variants per topic
        top_n: Number of top titles to select
        mock_mode: Whether running in mock mode
    """
    logger.info(f"=" * 60)
    logger.info(f"Starting Idea Generation Pipeline")
    logger.info(f"Segment: {gender} / {age_bucket}")
    logger.info(f"=" * 60)
    
    # Setup output directories
    ideas_dir = output_base / "ideas" / gender / age_bucket
    topics_dir = output_base / "topics" / gender / age_bucket
    titles_dir = output_base / "titles" / gender / age_bucket
    selected_dir = output_base / "selected" / gender / age_bucket
    voices_dir = output_base / "voices" / "choice" / gender / age_bucket
    
    # Step 1: Reddit Story Adaptation (if stories provided)
    adapted_ideas = []
    if reddit_stories and not mock_mode:
        logger.info(f"\n[1/7] Adapting {len(reddit_stories)} Reddit stories...")
        adapter = IdeaAdapter(llm_provider)
        adapted_ideas = adapter.adapt_stories(reddit_stories, gender, age_bucket)
        adapter.save_ideas(adapted_ideas, ideas_dir, "reddit_adapted.json")
        logger.info(f"✓ Adapted {len(adapted_ideas)} Reddit stories")
    else:
        logger.info("\n[1/7] Skipping Reddit adaptation (no stories provided or mock mode)")
    
    # Step 2: LLM-Based Idea Generation
    logger.info(f"\n[2/7] Generating {ideas_count} original ideas...")
    generator = IdeaGenerator(llm_provider)
    generated_ideas = generator.generate_ideas(gender, age_bucket, count=ideas_count)
    generator.save_ideas(generated_ideas, ideas_dir, "llm_generated.json")
    logger.info(f"✓ Generated {len(generated_ideas)} original ideas")
    
    # Merge all ideas
    all_ideas = adapted_ideas + generated_ideas
    merge_and_save_all_ideas(adapted_ideas, generated_ideas, ideas_dir)
    logger.info(f"✓ Total ideas: {len(all_ideas)}")
    
    if not all_ideas:
        logger.error("No ideas generated. Stopping pipeline.")
        return None
    
    # Step 3: Topic Clustering
    logger.info(f"\n[3/7] Clustering ideas into topics...")
    clusterer = TopicClusterer(llm_provider)
    topics = clusterer.cluster_ideas(all_ideas, min_clusters=8, max_clusters=12)
    clusterer.save_topics(topics, topics_dir)
    logger.info(f"✓ Clustered into {len(topics)} topics")
    
    if not topics:
        logger.error("No topics created. Stopping pipeline.")
        return None
    
    # Step 4: Title Generation
    logger.info(f"\n[4/7] Generating {titles_per_topic} titles per topic...")
    title_gen = TitleGenerator(llm_provider)
    titles_by_topic = title_gen.generate_all_titles(topics, titles_per_topic)
    title_gen.save_titles(titles_by_topic, titles_dir, "titles_raw.json")
    
    total_titles = sum(len(titles) for titles in titles_by_topic.values())
    logger.info(f"✓ Generated {total_titles} total titles")
    
    if not titles_by_topic or total_titles == 0:
        logger.error("No titles generated. Stopping pipeline.")
        return None
    
    # Step 5: Title Scoring
    logger.info(f"\n[5/7] Scoring all titles for viral potential...")
    scorer = TitleScorer()
    scored_titles = scorer.score_all_titles(titles_by_topic)
    scorer.save_scored_titles(scored_titles, titles_dir, "titles_scored.json")
    logger.info(f"✓ Scored {total_titles} titles")
    
    # Step 6: Voice Recommendation
    logger.info(f"\n[6/7] Generating voice recommendations...")
    voice_rec = VoiceRecommender()
    titles_with_voices = voice_rec.recommend_all_voices(scored_titles)
    voice_rec.save_recommendations(titles_with_voices, voices_dir)
    logger.info(f"✓ Generated voice recommendations for {total_titles} titles")
    
    # Step 7: Top Selection
    logger.info(f"\n[7/7] Selecting top {top_n} titles...")
    selector = TopSelector()
    selected_titles = selector.select_top_titles(titles_with_voices, top_n=top_n)
    selector.save_selected_titles(selected_titles, selected_dir, gender, age_bucket)
    
    if selected_titles:
        logger.info(f"✓ Selected {len(selected_titles)} top titles")
        logger.info("\nTop Selected Titles:")
        for i, title in enumerate(selected_titles, 1):
            score = title.get('score', 0)
            text = title.get('text', '')
            logger.info(f"  {i}. [{score:.1f}] {text}")
    else:
        logger.warning("No titles met selection criteria")
    
    logger.info(f"\n" + "=" * 60)
    logger.info("Pipeline completed successfully!")
    logger.info(f"=" * 60)
    
    return {
        "ideas": all_ideas,
        "topics": topics,
        "titles": titles_by_topic,
        "selected": selected_titles
    }


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Run the idea generation pipeline for story content"
    )
    parser.add_argument(
        "--gender",
        type=str,
        choices=["women", "men"],
        help="Target gender segment"
    )
    parser.add_argument(
        "--age",
        type=str,
        help="Target age bucket (e.g., '18-23', '24-29')"
    )
    parser.add_argument(
        "--all-segments",
        action="store_true",
        help="Run pipeline for all segments"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data"),
        help="Base output directory (default: data)"
    )
    parser.add_argument(
        "--ideas-count",
        type=int,
        default=20,
        help="Number of LLM ideas to generate (default: 20)"
    )
    parser.add_argument(
        "--titles-per-topic",
        type=int,
        default=10,
        help="Number of title variants per topic (default: 10)"
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=5,
        help="Number of top titles to select (default: 5)"
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use mock LLM provider for testing"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o-mini",
        help="OpenAI model to use (default: gpt-4o-mini)"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.all_segments and (not args.gender or not args.age):
        parser.error("Either --all-segments or both --gender and --age must be specified")
    
    # Initialize LLM provider
    if args.mock:
        logger.info("Using mock LLM provider")
        # Create a smarter mock that returns different responses
        llm_provider = MockLLMProvider(response="1. Mock idea about relationships\n2. Mock idea about career success\n3. Mock idea about personal growth")
    else:
        logger.info(f"Using OpenAI provider with model: {args.model}")
        try:
            from providers.openai_provider import OpenAIProvider
            llm_provider = OpenAIProvider(model=args.model)
        except ImportError as e:
            logger.error(f"Failed to import OpenAI provider: {e}")
            logger.error("Please install required dependencies: pip install openai tenacity")
            sys.exit(1)
        except ValueError as e:
            logger.error(f"Failed to initialize OpenAI provider: {e}")
            logger.error("Please set OPENAI_API_KEY environment variable")
            sys.exit(1)
    
    # Define segments to process
    if args.all_segments:
        segments = [
            ("women", "18-23"),
            ("women", "24-29"),
            ("women", "30-40"),
            ("men", "18-23"),
            ("men", "24-29"),
            ("men", "30-40"),
        ]
    else:
        segments = [(args.gender, args.age)]
    
    # Run pipeline for each segment
    results = {}
    for gender, age_bucket in segments:
        try:
            result = run_pipeline(
                gender=gender,
                age_bucket=age_bucket,
                output_base=args.output,
                llm_provider=llm_provider,
                ideas_count=args.ideas_count,
                titles_per_topic=args.titles_per_topic,
                top_n=args.top_n,
                mock_mode=args.mock
            )
            results[f"{gender}_{age_bucket}"] = result
            
        except Exception as e:
            logger.error(f"Pipeline failed for {gender}/{age_bucket}: {e}", exc_info=True)
            continue
    
    logger.info(f"\nProcessed {len(results)} segments successfully")


if __name__ == "__main__":
    main()
