#!/usr/bin/env python3
"""
Title Scoring Module for StoryGenerator

Scores video titles (0-100) for viral potential using local LLM and rubric from config/scoring.yaml.
For each segment/age:
- Scores titles with rationale
- Recommends voice (F/M)
- Saves JSON results to /scores/{gender}/{age}/YYYYMMDD_title_scores.json
- Selects top 5 titles and writes voice notes to /voices/choice/{gender}/{age}/YYYYMMDD_voice_notes.md
"""

import os
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import re


def load_scoring_config(config_path: str = None) -> Dict:
    """
    Load scoring rubric configuration from YAML file.
    
    Args:
        config_path: Path to scoring.yaml file
        
    Returns:
        Configuration dictionary
    """
    if config_path is None:
        config_path = Path(__file__).parent / "config" / "scoring.yaml"
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        print(f"✅ Loaded scoring config from {config_path}")
        return config
    except FileNotFoundError:
        print(f"❌ Config file not found: {config_path}")
        raise
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        raise


def load_audience_config(config_path: str = None) -> Dict:
    """
    Load audience configuration from JSON file.
    
    Args:
        config_path: Path to audience_config.json file
        
    Returns:
        Configuration dictionary
    """
    if config_path is None:
        config_path = Path(__file__).parent / "config" / "audience_config.json"
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"✅ Loaded audience config from {config_path}")
        return config
    except FileNotFoundError:
        print(f"❌ Config file not found: {config_path}")
        raise
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        raise


def find_title_files(titles_path: Path, gender: str, age: str) -> List[Path]:
    """
    Find all title-related files in a specific segment directory.
    
    Args:
        titles_path: Base path to titles directory
        gender: Target gender (men/women)
        age: Target age range
        
    Returns:
        List of paths to title files (JSON or text files)
    """
    segment_path = titles_path / gender / age
    
    if not segment_path.exists():
        print(f"⚠️  Path does not exist: {segment_path}")
        return []
    
    title_files = []
    
    # Look for JSON files with title information
    for json_file in segment_path.glob("*.json"):
        if not json_file.name.startswith("_"):  # Skip underscore-prefixed files
            title_files.append(json_file)
    
    # If no JSON files, look for text files
    if not title_files:
        for txt_file in segment_path.glob("*.txt"):
            if not txt_file.name.startswith("_"):
                title_files.append(txt_file)
    
    # Also check subdirectories for idea.json files
    for subdir in segment_path.iterdir():
        if subdir.is_dir() and not subdir.name.startswith("_"):
            idea_file = subdir / "idea.json"
            if idea_file.exists():
                title_files.append(idea_file)
    
    return title_files


def extract_title_from_file(file_path: Path) -> Optional[str]:
    """
    Extract title text from a file.
    
    Args:
        file_path: Path to file containing title
        
    Returns:
        Title string or None if not found
    """
    try:
        if file_path.suffix == ".json":
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Try different possible keys for title
            for key in ['title', 'story_title', 'video_title', 'name']:
                if key in data:
                    return data[key]
            
            # If file is idea.json in a subfolder, use folder name as fallback
            if file_path.name == "idea.json":
                return file_path.parent.name
        
        elif file_path.suffix == ".txt":
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                # Take first line as title if multi-line
                return content.split('\n')[0] if content else None
        
    except Exception as e:
        print(f"⚠️  Error reading file {file_path}: {e}")
    
    return None


def score_title_locally(title: str, gender: str, age: str, config: Dict) -> Dict:
    """
    Score a title using local heuristic rules based on the scoring rubric.
    
    This is a fallback method when LLM is not available. It applies rule-based scoring
    based on common viral title patterns and best practices.
    
    Args:
        title: The title to score
        gender: Target gender
        age: Target age range
        config: Scoring configuration
        
    Returns:
        Dictionary with scores, rationale, and voice recommendation
    """
    scores = {}
    
    # 1. Hook Strength (30% weight)
    hook_score = 50  # Base score
    
    # Bonus for question format
    if '?' in title:
        hook_score += 15
    
    # Bonus for emotional words
    emotional_words = ['shocking', 'amazing', 'unbelievable', 'secret', 'truth', 
                       'revealed', 'never', 'always', 'must', 'need', 'forbidden']
    word_lower = title.lower()
    for word in emotional_words:
        if word in word_lower:
            hook_score += 10
            break
    
    # Bonus for numbers
    if re.search(r'\d+', title):
        hook_score += 10
    
    # Bonus for "how to" or "why"
    if 'how to' in word_lower or 'why ' in word_lower:
        hook_score += 15
    
    scores['hook_strength'] = min(hook_score, 100)
    
    # 2. Clarity (20% weight)
    clarity_score = 70  # Base score
    
    # Deduct for overly complex words or structure
    words = title.split()
    avg_word_length = sum(len(w) for w in words) / len(words) if words else 0
    
    if avg_word_length > 8:
        clarity_score -= 15
    elif avg_word_length < 4:
        clarity_score += 10
    
    # Deduct for too many clauses
    if title.count(',') > 2:
        clarity_score -= 15
    
    scores['clarity'] = max(min(clarity_score, 100), 0)
    
    # 3. Relevance (20% weight)
    relevance_score = 60  # Base score
    
    # Age-based relevance adjustments
    age_start = int(age.split('-')[0])
    
    # Younger audiences (10-23) prefer trending, social topics
    if age_start < 24:
        if any(word in word_lower for word in ['tiktok', 'trend', 'viral', 'challenge', 'life', 'friend']):
            relevance_score += 20
    
    # Older audiences (24+) prefer practical, life content
    else:
        if any(word in word_lower for word in ['career', 'money', 'health', 'relationship', 'life']):
            relevance_score += 20
    
    # Gender-based adjustments
    if gender == 'women':
        if any(word in word_lower for word in ['beauty', 'style', 'wellness', 'self-care', 'relationship']):
            relevance_score += 10
    elif gender == 'men':
        if any(word in word_lower for word in ['fitness', 'tech', 'gaming', 'career', 'money']):
            relevance_score += 10
    
    scores['relevance'] = min(relevance_score, 100)
    
    # 4. Length & Format (15% weight)
    title_length = len(title)
    
    if 40 <= title_length <= 60:
        length_score = 95
    elif 30 <= title_length <= 70:
        length_score = 80
    elif 20 <= title_length < 30 or 70 < title_length <= 80:
        length_score = 60
    else:
        length_score = 40
    
    scores['length_format'] = length_score
    
    # 5. Viral Potential (15% weight)
    viral_score = 50  # Base score
    
    # Bonus for controversy or strong opinion
    if any(word in word_lower for word in ['everyone', 'nobody', 'never', 'always', 'worst', 'best']):
        viral_score += 15
    
    # Bonus for personal story hooks
    if any(phrase in word_lower for phrase in ['i ', 'my ', 'how i ']):
        viral_score += 15
    
    # Bonus for list format
    if re.search(r'\d+\s+(ways|reasons|things|tips|secrets)', word_lower):
        viral_score += 20
    
    scores['viral_potential'] = min(viral_score, 100)
    
    # Calculate overall weighted score
    weights = {
        'hook_strength': 0.30,
        'clarity': 0.20,
        'relevance': 0.20,
        'length_format': 0.15,
        'viral_potential': 0.15
    }
    
    overall_score = sum(scores[key] * weights[key] for key in scores)
    
    # Generate rationale
    rationale_parts = []
    
    if scores['hook_strength'] >= 70:
        rationale_parts.append("Strong hook with curiosity-inducing elements")
    else:
        rationale_parts.append("Hook could be more compelling")
    
    if scores['clarity'] >= 70:
        rationale_parts.append("Clear and easy to understand")
    else:
        rationale_parts.append("Could be clearer or more concise")
    
    if scores['relevance'] >= 70:
        rationale_parts.append("Well-aligned with target audience")
    else:
        rationale_parts.append("May not fully resonate with target audience")
    
    rationale = ". ".join(rationale_parts) + "."
    
    # Voice recommendation
    voice_gender = recommend_voice(title, gender, age)
    voice_reasoning = generate_voice_reasoning(title, gender, age, voice_gender)
    
    return {
        'scores': scores,
        'overall_score': round(overall_score, 2),
        'rationale': rationale,
        'voice_recommendation': {
            'gender': voice_gender,
            'reasoning': voice_reasoning
        }
    }


def recommend_voice(title: str, target_gender: str, age: str) -> str:
    """
    Recommend narrator voice gender based on title and target audience.
    
    Args:
        title: Video title
        target_gender: Target audience gender
        age: Target age range
        
    Returns:
        'M' or 'F' for recommended voice gender
    """
    title_lower = title.lower()
    
    # Mystery/Thriller/Horror tend to work better with male voices
    if any(word in title_lower for word in ['mystery', 'secret', 'dark', 'horror', 'scary', 'hidden', 'truth']):
        return 'M'
    
    # Romance/Beauty/Wellness often work better with matching gender
    if any(word in title_lower for word in ['beauty', 'makeup', 'style', 'wellness', 'self-care']):
        return 'F'
    
    # Tech/Gaming often work better with male voices
    if any(word in title_lower for word in ['tech', 'gaming', 'build', 'hack', 'code']):
        return 'M'
    
    # For general content, match target audience gender
    if target_gender == 'women':
        return 'F'
    else:
        return 'M'


def generate_voice_reasoning(title: str, target_gender: str, age: str, recommended_gender: str) -> str:
    """
    Generate reasoning for voice recommendation.
    
    Args:
        title: Video title
        target_gender: Target audience gender
        age: Target age range
        recommended_gender: Recommended voice gender
        
    Returns:
        Reasoning string
    """
    title_lower = title.lower()
    
    if 'mystery' in title_lower or 'secret' in title_lower:
        return "Mystery content benefits from authoritative, deeper voice to build suspense"
    
    if 'beauty' in title_lower or 'style' in title_lower:
        return "Beauty/style content resonates better with female voice for target audience"
    
    if 'tech' in title_lower or 'gaming' in title_lower:
        return "Tech content traditionally performs well with male narrator"
    
    if recommended_gender == 'F' and target_gender == 'women':
        return "Female voice matches target audience and builds relatability"
    
    if recommended_gender == 'M' and target_gender == 'men':
        return "Male voice matches target audience preferences"
    
    return "Voice gender chosen to match target audience demographic"


def score_titles_for_segment(
    titles_path: Path,
    scores_path: Path,
    voices_path: Path,
    gender: str,
    age: str,
    config: Dict
) -> Tuple[int, int]:
    """
    Score all titles for a specific audience segment.
    
    Args:
        titles_path: Base path to titles directory
        scores_path: Base path to scores directory
        voices_path: Base path to voices/choice directory
        gender: Target gender
        age: Target age range
        config: Scoring configuration
        
    Returns:
        Tuple of (titles_scored, top_titles_selected)
    """
    print(f"\n{'='*60}")
    print(f"Processing segment: {gender} / {age}")
    print(f"{'='*60}")
    
    # Find title files
    title_files = find_title_files(titles_path, gender, age)
    
    if not title_files:
        print(f"⚠️  No title files found for {gender}/{age}")
        return 0, 0
    
    print(f"Found {len(title_files)} title file(s)")
    
    # Score each title
    results = []
    
    for file_path in title_files:
        title_text = extract_title_from_file(file_path)
        
        if not title_text:
            print(f"⚠️  Could not extract title from {file_path.name}")
            continue
        
        print(f"\nScoring: {title_text}")
        
        # Score the title
        score_result = score_title_locally(title_text, gender, age, config)
        
        # Add metadata
        result = {
            'title': title_text,
            'source_file': str(file_path.name),
            'target_audience': {
                'gender': gender,
                'age': age
            },
            'scored_at': datetime.now().isoformat(),
            **score_result
        }
        
        results.append(result)
        
        print(f"  Score: {result['overall_score']:.1f}/100")
        print(f"  Voice: {result['voice_recommendation']['gender']}")
    
    if not results:
        print("⚠️  No titles were successfully scored")
        return 0, 0
    
    # Sort by overall score (descending)
    results.sort(key=lambda x: x['overall_score'], reverse=True)
    
    # Select top 5
    top_count = config.get('title_scoring', {}).get('top_selection', {}).get('count', 5)
    top_titles = results[:top_count]
    
    print(f"\n📊 Scoring complete: {len(results)} titles scored")
    print(f"🏆 Top {len(top_titles)} titles selected")
    
    # Save results to JSON
    save_scores_json(scores_path, gender, age, results)
    
    # Save voice notes to markdown
    save_voice_notes(voices_path, gender, age, top_titles)
    
    return len(results), len(top_titles)


def save_scores_json(scores_path: Path, gender: str, age: str, results: List[Dict]) -> None:
    """
    Save scoring results to JSON file.
    
    Args:
        scores_path: Base path to scores directory
        gender: Target gender
        age: Target age range
        results: List of scoring results
    """
    # Create directory if needed
    output_dir = scores_path / gender / age
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename with date
    date_str = datetime.now().strftime("%Y%m%d")
    output_file = output_dir / f"{date_str}_title_scores.json"
    
    # Prepare output data
    output_data = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'segment': {
                'gender': gender,
                'age': age
            },
            'total_titles': len(results)
        },
        'scores': results
    }
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved scores to: {output_file}")


def save_voice_notes(voices_path: Path, gender: str, age: str, top_titles: List[Dict]) -> None:
    """
    Save voice notes for top titles to markdown file.
    
    Args:
        voices_path: Base path to voices/choice directory
        gender: Target gender
        age: Target age range
        top_titles: List of top-scoring title results
    """
    # Create directory if needed
    output_dir = voices_path / gender / age
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename with date
    date_str = datetime.now().strftime("%Y%m%d")
    output_file = output_dir / f"{date_str}_voice_notes.md"
    
    # Generate markdown content
    lines = [
        f"# Voice Notes - {gender.title()} / {age}",
        f"",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Top Titles:** {len(top_titles)}",
        f"",
        "---",
        ""
    ]
    
    for i, result in enumerate(top_titles, 1):
        lines.extend([
            f"## {i}. {result['title']}",
            f"",
            f"**Score:** {result['overall_score']:.1f}/100",
            f"",
            f"**Voice Recommendation:** {result['voice_recommendation']['gender']}",
            f"",
            f"**Reasoning:** {result['voice_recommendation']['reasoning']}",
            f"",
            f"**Rationale:** {result['rationale']}",
            f"",
            f"### Detailed Scores",
            f"",
            f"- Hook Strength: {result['scores']['hook_strength']}/100",
            f"- Clarity: {result['scores']['clarity']}/100",
            f"- Relevance: {result['scores']['relevance']}/100",
            f"- Length & Format: {result['scores']['length_format']}/100",
            f"- Viral Potential: {result['scores']['viral_potential']}/100",
            f"",
            "---",
            ""
        ])
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ Saved voice notes to: {output_file}")


def process_all_segments(
    base_path: str = None,
    audience_config: Dict = None,
    scoring_config: Dict = None
) -> None:
    """
    Process all audience segments and score titles.
    
    Args:
        base_path: Base path for Generator folders (default: "Generator")
        audience_config: Audience configuration (default: load from file)
        scoring_config: Scoring configuration (default: load from file)
    """
    # Load configurations if not provided
    if audience_config is None:
        audience_config = load_audience_config()
    
    if scoring_config is None:
        scoring_config = load_scoring_config()
    
    # Determine base path
    root = Path(__file__).parent
    if base_path is None:
        base_path = audience_config.get('folder_structure', {}).get('base_path', 'Generator')
    
    if base_path:
        base_dir = root / base_path
    else:
        base_dir = root
    
    titles_path = base_dir / "titles"
    scores_path = base_dir / "scores"
    voices_path = base_dir / "voices" / "choice"
    
    # Extract audience segments
    genders = [g['name'] for g in audience_config.get('audience', {}).get('genders', [])]
    age_groups = [a['range'] for a in audience_config.get('audience', {}).get('age_groups', [])]
    
    if not genders or not age_groups:
        print("❌ No audience segments defined in configuration")
        return
    
    print("=" * 60)
    print("Title Scoring - Processing All Segments")
    print("=" * 60)
    print(f"Base path: {base_dir}")
    print(f"Genders: {', '.join(genders)}")
    print(f"Age groups: {len(age_groups)}")
    print()
    
    total_scored = 0
    total_top = 0
    
    # Process each segment
    for gender in genders:
        for age_group in age_groups:
            scored, top = score_titles_for_segment(
                titles_path,
                scores_path,
                voices_path,
                gender,
                age_group,
                scoring_config
            )
            total_scored += scored
            total_top += top
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Total titles scored: {total_scored}")
    print(f"Total top titles selected: {total_top}")
    print(f"Segments processed: {len(genders) * len(age_groups)}")
    print()
    print("✅ Title scoring complete!")


def main():
    """Main entry point."""
    import sys
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        # Process specific segment
        if len(sys.argv) >= 3:
            gender = sys.argv[1]
            age = sys.argv[2]
            
            print(f"Processing single segment: {gender}/{age}")
            
            # Load configurations
            audience_config = load_audience_config()
            scoring_config = load_scoring_config()
            
            # Determine paths
            root = Path(__file__).parent
            base_path = audience_config.get('folder_structure', {}).get('base_path', 'Generator')
            base_dir = root / base_path if base_path else root
            
            titles_path = base_dir / "titles"
            scores_path = base_dir / "scores"
            voices_path = base_dir / "voices" / "choice"
            
            # Process single segment
            scored, top = score_titles_for_segment(
                titles_path,
                scores_path,
                voices_path,
                gender,
                age,
                scoring_config
            )
            
            print(f"\n✅ Scored {scored} titles, selected {top} top titles")
        else:
            print("Usage: python title_score.py [gender] [age]")
            print("Example: python title_score.py women 18-23")
            sys.exit(1)
    else:
        # Process all segments
        process_all_segments()


if __name__ == "__main__":
    main()
