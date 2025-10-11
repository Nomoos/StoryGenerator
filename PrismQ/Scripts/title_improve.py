#!/usr/bin/env python3
"""
Title Improvement Module for StoryGenerator

Generates improved title variants using GPT or local LLM:
- Generates 5 title variants per selected title
- Scores each variant using the scoring rubric
- Selects and saves the best variant
- Outputs to /titles/{segment}/{age}/{title_id}_improved.json
- Updates title registry if changed
"""

import os
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import sys

# Add scripts directory to path to import title_score
sys.path.insert(0, str(Path(__file__).parent))
import title_score


def load_llm_config(config_path: str = None) -> Dict:
    """
    Load LLM configuration for title generation.

    Args:
        config_path: Path to LLM config file

    Returns:
        Configuration dictionary
    """
    if config_path is None:
        # Check for various config locations
        possible_paths = [
            Path(__file__).parent.parent / "data" / "config" / "llm_config.yaml",
            Path(__file__).parent / "config" / "llm_config.yaml",
        ]

        for path in possible_paths:
            if path.exists():
                config_path = path
                break

    if config_path and Path(config_path).exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            print(f"✅ Loaded LLM config from {config_path}")
            return config
        except Exception as e:
            print(f"⚠️  Error loading LLM config: {e}")

    # Return default config if not found
    print("⚠️  Using default LLM configuration")
    return {
        "provider": "ollama",
        "model": "qwen2.5:14b-instruct",
        "ollama_host": "http://localhost:11434",
        "temperature": 0.7,
        "max_tokens": 200,
    }


def generate_title_variants_ollama(
    original_title: str, segment: str, age: str, config: Dict, count: int = 5
) -> List[str]:
    """
    Generate title variants using Ollama local LLM.

    Args:
        original_title: The original title to improve
        segment: Target gender (men/women)
        age: Target age range
        config: LLM configuration
        count: Number of variants to generate

    Returns:
        List of title variants
    """
    try:
        import requests

        ollama_host = config.get("ollama_host", "http://localhost:11434")
        model = config.get("model", "qwen2.5:14b-instruct")

        prompt = f"""You are an expert at creating viral social media titles. Generate {count} improved variants of the following title that are more clickable and engaging.

Original Title: {original_title}
Target Audience: {segment}, ages {age}

Requirements:
- Each variant should be 40-60 characters long
- Create curiosity and emotional appeal
- Use proven viral title patterns (questions, numbers, secrets, etc.)
- Keep it clear and easy to understand
- Make each variant distinctly different

Generate exactly {count} title variants, one per line, numbered 1-{count}."""

        response = requests.post(
            f"{ollama_host}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": config.get("temperature", 0.7),
                    "num_predict": config.get("max_tokens", 200),
                },
            },
            timeout=60,
        )

        if response.status_code == 200:
            result = response.json()
            generated_text = result.get("response", "")

            # Parse numbered lines
            variants = []
            for line in generated_text.split("\n"):
                line = line.strip()
                # Match numbered lines like "1. Title" or "1) Title"
                if line and (line[0].isdigit() or line.startswith("- ")):
                    # Remove numbering and cleanup
                    cleaned = line.lstrip("0123456789.-) ").strip()
                    if cleaned and len(cleaned) > 10:  # Minimum reasonable length
                        variants.append(cleaned)

            if len(variants) >= count:
                return variants[:count]
            elif len(variants) > 0:
                print(f"⚠️  Generated only {len(variants)} variants instead of {count}")
                return variants
            else:
                print("⚠️  Failed to parse variants from LLM response")
                return []
        else:
            print(f"⚠️  Ollama request failed with status {response.status_code}")
            return []

    except ImportError:
        print("❌ requests library not installed. Install with: pip install requests")
        return []
    except Exception as e:
        print(f"⚠️  Error generating variants with Ollama: {e}")
        return []


def generate_title_variants_openai(
    original_title: str, segment: str, age: str, config: Dict, count: int = 5
) -> List[str]:
    """
    Generate title variants using OpenAI GPT.

    Args:
        original_title: The original title to improve
        segment: Target gender (men/women)
        age: Target age range
        config: LLM configuration
        count: Number of variants to generate

    Returns:
        List of title variants
    """
    try:
        import openai

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠️  OPENAI_API_KEY environment variable not set")
            return []

        client = openai.OpenAI(api_key=api_key)
        model = config.get("model", "gpt-4")

        prompt = f"""You are an expert at creating viral social media titles. Generate {count} improved variants of the following title that are more clickable and engaging.

Original Title: {original_title}
Target Audience: {segment}, ages {age}

Requirements:
- Each variant should be 40-60 characters long
- Create curiosity and emotional appeal
- Use proven viral title patterns (questions, numbers, secrets, etc.)
- Keep it clear and easy to understand
- Make each variant distinctly different

Generate exactly {count} title variants, one per line, numbered 1-{count}."""

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at creating viral social media titles.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=config.get("temperature", 0.7),
            max_tokens=config.get("max_tokens", 200),
        )

        generated_text = response.choices[0].message.content

        # Parse numbered lines
        variants = []
        for line in generated_text.split("\n"):
            line = line.strip()
            # Match numbered lines like "1. Title" or "1) Title"
            if line and (line[0].isdigit() or line.startswith("- ")):
                # Remove numbering and cleanup
                cleaned = line.lstrip("0123456789.-) ").strip()
                if cleaned and len(cleaned) > 10:  # Minimum reasonable length
                    variants.append(cleaned)

        if len(variants) >= count:
            return variants[:count]
        elif len(variants) > 0:
            print(f"⚠️  Generated only {len(variants)} variants instead of {count}")
            return variants
        else:
            print("⚠️  Failed to parse variants from LLM response")
            return []

    except ImportError:
        print("❌ openai library not installed. Install with: pip install openai")
        return []
    except Exception as e:
        print(f"⚠️  Error generating variants with OpenAI: {e}")
        return []


def generate_title_variants_local(
    original_title: str, segment: str, age: str, count: int = 5
) -> List[str]:
    """
    Generate title variants using local heuristic rules (fallback).

    Args:
        original_title: The original title to improve
        segment: Target gender (men/women)
        age: Target age range
        count: Number of variants to generate

    Returns:
        List of title variants
    """
    variants = []

    # Pattern 1: Question format
    if "?" not in original_title:
        variants.append(f"Why {original_title}?")
        variants.append(f"What If {original_title}?")

    # Pattern 2: Number list format
    variants.append(f"5 Things About {original_title}")
    variants.append(f"The Secret Behind {original_title}")

    # Pattern 3: Curiosity hook
    variants.append(f"You Won't Believe {original_title}")

    # Pattern 4: Personal story
    variants.append(f"How I Discovered {original_title}")

    # Pattern 5: Controversy
    variants.append(f"The Truth About {original_title}")

    # Return only the requested count
    return variants[:count]


def generate_title_variants(
    original_title: str, segment: str, age: str, llm_config: Dict, count: int = 5
) -> List[str]:
    """
    Generate title variants using configured LLM provider.

    Args:
        original_title: The original title to improve
        segment: Target gender (men/women)
        age: Target age range
        llm_config: LLM configuration
        count: Number of variants to generate

    Returns:
        List of title variants
    """
    provider = llm_config.get("provider", "ollama").lower()

    if provider == "openai":
        variants = generate_title_variants_openai(original_title, segment, age, llm_config, count)
    elif provider == "ollama":
        variants = generate_title_variants_ollama(original_title, segment, age, llm_config, count)
    else:
        print(f"⚠️  Unknown provider '{provider}', using local fallback")
        variants = generate_title_variants_local(original_title, segment, age, count)

    # Fallback to local generation if LLM fails
    if not variants:
        print("⚠️  LLM generation failed, using local fallback")
        variants = generate_title_variants_local(original_title, segment, age, count)

    return variants


def score_and_select_best_variant(
    original_title: str, variants: List[str], segment: str, age: str, scoring_config: Dict
) -> Tuple[str, Dict, List[Dict]]:
    """
    Score all variants and select the best one.

    Args:
        original_title: The original title
        variants: List of title variants
        segment: Target gender (men/women)
        age: Target age range
        scoring_config: Scoring configuration

    Returns:
        Tuple of (best_title, best_score_data, all_scores)
    """
    all_scores = []

    # Score original title
    original_score = title_score.score_title_locally(original_title, segment, age, scoring_config)
    original_score["is_original"] = True
    original_score["variant_number"] = 0
    all_scores.append(
        {"title": original_title, "variant_number": 0, "is_original": True, **original_score}
    )

    print(f"  Original: {original_title}")
    print(f"    Score: {original_score['overall_score']:.1f}/100")

    # Score each variant
    for i, variant in enumerate(variants, 1):
        variant_score = title_score.score_title_locally(variant, segment, age, scoring_config)
        variant_score["is_original"] = False
        variant_score["variant_number"] = i
        all_scores.append(
            {"title": variant, "variant_number": i, "is_original": False, **variant_score}
        )

        print(f"  Variant {i}: {variant}")
        print(f"    Score: {variant_score['overall_score']:.1f}/100")

    # Find the best title
    best_score_data = max(all_scores, key=lambda x: x["overall_score"])
    best_title = best_score_data["title"]

    return best_title, best_score_data, all_scores


def improve_title(
    title_file: Path,
    segment: str,
    age: str,
    output_dir: Path,
    llm_config: Dict,
    scoring_config: Dict,
    variant_count: int = 5,
) -> Optional[Dict]:
    """
    Improve a single title by generating and scoring variants.

    Args:
        title_file: Path to the title file
        segment: Target gender (men/women)
        age: Target age range
        output_dir: Output directory for improved titles
        llm_config: LLM configuration
        scoring_config: Scoring configuration
        variant_count: Number of variants to generate

    Returns:
        Dictionary with improvement results or None if failed
    """
    # Extract original title
    original_title = title_score.extract_title_from_file(title_file)
    if not original_title:
        print(f"⚠️  Could not extract title from {title_file}")
        return None

    # Generate title_id from filename
    title_id = title_file.stem
    if title_file.name == "idea.json":
        title_id = title_file.parent.name

    print(f"\n{'='*60}")
    print(f"Improving Title: {title_id}")
    print(f"Original: {original_title}")
    print(f"{'='*60}")

    # Generate variants
    print(f"\nGenerating {variant_count} title variants...")
    variants = generate_title_variants(original_title, segment, age, llm_config, variant_count)

    if not variants:
        print("⚠️  Failed to generate variants")
        return None

    print(f"✅ Generated {len(variants)} variants")

    # Score and select best
    print("\nScoring variants...")
    best_title, best_score, all_scores = score_and_select_best_variant(
        original_title, variants, segment, age, scoring_config
    )

    improvement_pct = 0
    if all_scores[0]["overall_score"] > 0:
        improvement_pct = (
            (best_score["overall_score"] - all_scores[0]["overall_score"])
            / all_scores[0]["overall_score"]
            * 100
        )

    print(f"\n🏆 Best Title: {best_title}")
    print(f"   Score: {best_score['overall_score']:.1f}/100")
    if best_score["is_original"]:
        print("   (Original title was best)")
    else:
        print(f"   Improvement: {improvement_pct:+.1f}%")

    # Prepare output data
    result = {
        "metadata": {
            "title_id": title_id,
            "source_file": str(title_file.name),
            "segment": segment,
            "age": age,
            "improved_at": datetime.now().isoformat(),
            "variant_count": len(variants),
        },
        "original_title": {
            "title": original_title,
            "score": all_scores[0]["overall_score"],
            "scores": all_scores[0]["scores"],
            "rationale": all_scores[0]["rationale"],
        },
        "best_title": {
            "title": best_title,
            "score": best_score["overall_score"],
            "scores": best_score["scores"],
            "rationale": best_score["rationale"],
            "is_original": best_score["is_original"],
            "variant_number": best_score["variant_number"],
            "improvement_pct": improvement_pct,
        },
        "all_variants": all_scores,
    }

    # Save to output file
    output_file = output_dir / segment / age / f"{title_id}_improved.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Saved results to {output_file}")

    return result


def update_title_registry(improved_results: List[Dict], registry_path: Path) -> None:
    """
    Update title registry with improved titles.

    Args:
        improved_results: List of improvement results
        registry_path: Path to registry file
    """
    # Load existing registry or create new
    if registry_path.exists():
        with open(registry_path, "r", encoding="utf-8") as f:
            registry = json.load(f)
    else:
        registry = {
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "total_titles": 0,
            },
            "titles": {},
        }

    # Update registry
    for result in improved_results:
        if not result:
            continue

        title_id = result["metadata"]["title_id"]
        segment = result["metadata"]["segment"]
        age = result["metadata"]["age"]

        key = f"{segment}/{age}/{title_id}"

        # Create slug from title
        best_title = result["best_title"]["title"]
        slug = best_title.lower().replace(" ", "-")
        slug = "".join(c for c in slug if c.isalnum() or c == "-")
        slug = slug[:50]  # Limit length

        registry["titles"][key] = {
            "title_id": title_id,
            "segment": segment,
            "age": age,
            "original_title": result["original_title"]["title"],
            "improved_title": best_title,
            "slug": slug,
            "original_score": result["original_title"]["score"],
            "improved_score": result["best_title"]["score"],
            "improvement_pct": result["best_title"]["improvement_pct"],
            "is_changed": not result["best_title"]["is_original"],
            "improved_at": result["metadata"]["improved_at"],
        }

    # Update metadata
    registry["metadata"]["updated_at"] = datetime.now().isoformat()
    registry["metadata"]["total_titles"] = len(registry["titles"])

    # Save registry
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Updated title registry at {registry_path}")
    print(f"   Total titles: {registry['metadata']['total_titles']}")
    changed_count = sum(1 for t in registry["titles"].values() if t["is_changed"])
    print(f"   Changed: {changed_count}")


def main():
    """Main entry point for title improvement."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate and score improved title variants")
    parser.add_argument("segment", nargs="?", help="Target segment (men/women)")
    parser.add_argument("age", nargs="?", help="Target age range (e.g., 18-23)")
    parser.add_argument("--title-id", help="Specific title ID to improve")
    parser.add_argument(
        "--variant-count", type=int, default=5, help="Number of variants to generate (default: 5)"
    )
    parser.add_argument("--titles-dir", help="Custom titles directory path")
    parser.add_argument("--output-dir", help="Custom output directory path")

    args = parser.parse_args()

    # Determine base paths
    base_path = Path(__file__).parent.parent / "data"
    titles_path = Path(args.titles_dir) if args.titles_dir else base_path / "titles"
    output_path = Path(args.output_dir) if args.output_dir else titles_path

    # Load configurations
    print("Loading configurations...")
    llm_config = load_llm_config()

    try:
        scoring_config_path = base_path / "config" / "scoring.yaml"
        scoring_config = title_score.load_scoring_config(str(scoring_config_path))
    except Exception as e:
        print(f"❌ Failed to load scoring config: {e}")
        return

    # Determine which titles to process
    segments_to_process = []

    if args.segment and args.age:
        segments_to_process.append((args.segment, args.age))
    else:
        # Process all segments
        for segment in ["men", "women"]:
            for age in ["10-13", "14-17", "18-23", "24-30"]:
                segments_to_process.append((segment, age))

    # Process titles
    all_results = []

    for segment, age in segments_to_process:
        print(f"\n{'='*60}")
        print(f"Processing Segment: {segment} / {age}")
        print(f"{'='*60}")

        # Find title files
        title_files = title_score.find_title_files(titles_path, segment, age)

        if not title_files:
            print(f"⚠️  No title files found for {segment}/{age}")
            continue

        # Filter by title_id if specified
        if args.title_id:
            title_files = [f for f in title_files if args.title_id in str(f)]
            if not title_files:
                print(f"⚠️  No files found matching title_id: {args.title_id}")
                continue

        print(f"Found {len(title_files)} title file(s)")

        # Improve each title
        for title_file in title_files:
            result = improve_title(
                title_file,
                segment,
                age,
                output_path,
                llm_config,
                scoring_config,
                args.variant_count,
            )

            if result:
                all_results.append(result)

    # Update registry
    if all_results:
        registry_path = output_path / "title_registry.json"
        update_title_registry(all_results, registry_path)

        print(f"\n{'='*60}")
        print("Title Improvement Complete")
        print(f"{'='*60}")
        print(f"Total titles improved: {len(all_results)}")
        improved_count = sum(1 for r in all_results if not r["best_title"]["is_original"])
        print(f"Titles changed: {improved_count}")
        print(
            f"Average improvement: {sum(r['best_title']['improvement_pct'] for r in all_results) / len(all_results):.1f}%"
        )
    else:
        print("\n⚠️  No titles were improved")


if __name__ == "__main__":
    main()
