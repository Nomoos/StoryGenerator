"""
Story Pattern Analyzer

Analyzes successful YouTube story subtitles to extract patterns, rules, and 
best practices for creating engaging content.

Usage:
    python story_pattern_analyzer.py subtitle1.txt subtitle2.txt ...
    python story_pattern_analyzer.py /path/to/subtitles/*.txt
"""

import os
import re
import sys
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from pathlib import Path
from collections import Counter
import json


@dataclass
class StoryAnalysis:
    """Analysis results for a single story."""
    filename: str
    title: str
    word_count: int
    sentence_count: int
    avg_words_per_sentence: float
    hook_first_sentence: str
    hook_word_count: int
    story_arc: List[str]
    emotional_words: List[str]
    dialogue_present: bool
    dialogue_count: int
    time_markers: List[str]
    conflict_indicators: List[str]
    resolution_present: bool
    
    def to_dict(self):
        return asdict(self)


class StoryPatternAnalyzer:
    """Analyzes story patterns in successful YouTube content."""
    
    # Emotional trigger words commonly found in viral stories
    EMOTIONAL_WORDS = [
        'shocked', 'angry', 'furious', 'devastated', 'heartbroken', 'revenge',
        'betrayed', 'humiliated', 'embarrassed', 'scared', 'terrified', 'horrified',
        'happy', 'excited', 'thrilled', 'amazing', 'incredible', 'unbelievable',
        'crazy', 'insane', 'ridiculous', 'absurd', 'outrageous', 'disgusting',
        'karma', 'justice', 'payback', 'deserved', 'regret', 'sorry'
    ]
    
    # Time markers that indicate story progression
    TIME_MARKERS = [
        'first time', 'next day', 'later', 'then', 'after', 'finally',
        'two weeks', 'months', 'years', 'yesterday', 'last night',
        'immediately', 'suddenly', 'eventually', 'meanwhile'
    ]
    
    # Conflict indicators
    CONFLICT_WORDS = [
        'but', 'however', 'unfortunately', 'problem', 'issue', 'wrong',
        'refused', 'denied', 'ignored', 'wouldn\'t', 'couldn\'t', 'shouldn\'t',
        'fight', 'argue', 'yell', 'scream', 'confront'
    ]
    
    def __init__(self):
        self.analyses: List[StoryAnalysis] = []
    
    def extract_title_from_filename(self, filename: str) -> str:
        """Extract readable title from filename."""
        # Remove common patterns
        title = filename.replace('[English (auto-generated)]', '')
        title = title.replace('[DownSub.com]', '')
        title = title.replace('.txt', '')
        title = title.replace('_', ' ')
        title = re.sub(r'\s+', ' ', title)
        return title.strip()
    
    def detect_dialogue(self, text: str) -> tuple[bool, int]:
        """Detect if story contains dialogue and count instances."""
        # Look for quoted text
        quotes = re.findall(r'"[^"]*"', text)
        return len(quotes) > 0, len(quotes)
    
    def extract_hook(self, text: str) -> tuple[str, int]:
        """Extract the opening hook (first sentence)."""
        # Find first sentence
        match = re.match(r'^([^.!?]+[.!?])', text)
        if match:
            hook = match.group(1).strip()
            word_count = len(hook.split())
            return hook, word_count
        return "", 0
    
    def find_emotional_words(self, text: str) -> List[str]:
        """Find emotional trigger words in the text."""
        text_lower = text.lower()
        found = []
        for word in self.EMOTIONAL_WORDS:
            if word in text_lower:
                found.append(word)
        return found
    
    def find_time_markers(self, text: str) -> List[str]:
        """Find time progression markers."""
        text_lower = text.lower()
        found = []
        for marker in self.TIME_MARKERS:
            if marker in text_lower:
                found.append(marker)
        return found
    
    def find_conflict_indicators(self, text: str) -> List[str]:
        """Find conflict indicators."""
        text_lower = text.lower()
        found = []
        for word in self.CONFLICT_WORDS:
            if word in text_lower:
                found.append(word)
        return found
    
    def detect_resolution(self, text: str) -> bool:
        """Detect if story has a clear resolution."""
        text_lower = text.lower()
        resolution_words = [
            'finally', 'in the end', 'turned out', 'learned',
            'now', 'never again', 'moral', 'lesson'
        ]
        return any(word in text_lower for word in resolution_words)
    
    def analyze_story_arc(self, text: str) -> List[str]:
        """Identify story arc components."""
        arc = []
        text_lower = text.lower()
        
        # Setup/Introduction
        if any(word in text_lower[:200] for word in ['so', 'this', 'my', 'i was']):
            arc.append('Setup/Introduction')
        
        # Conflict/Problem
        if any(word in text_lower for word in self.CONFLICT_WORDS):
            arc.append('Conflict/Problem')
        
        # Escalation
        if any(phrase in text_lower for phrase in ['worse', 'more', 'again', 'kept', 'continued']):
            arc.append('Escalation')
        
        # Climax/Turning Point
        if any(phrase in text_lower for phrase in ['decided', 'had enough', 'finally', 'then']):
            arc.append('Climax/Turning Point')
        
        # Resolution
        if self.detect_resolution(text):
            arc.append('Resolution')
        
        return arc
    
    def analyze_file(self, filepath: str) -> StoryAnalysis:
        """Analyze a single subtitle file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        
        filename = os.path.basename(filepath)
        title = self.extract_title_from_filename(filename)
        
        # Basic metrics
        words = text.split()
        word_count = len(words)
        sentences = re.split(r'[.!?]+', text)
        sentence_count = len([s for s in sentences if s.strip()])
        avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0
        
        # Hook analysis
        hook, hook_word_count = self.extract_hook(text)
        
        # Dialogue detection
        has_dialogue, dialogue_count = self.detect_dialogue(text)
        
        # Pattern detection
        emotional_words = self.find_emotional_words(text)
        time_markers = self.find_time_markers(text)
        conflict_indicators = self.find_conflict_indicators(text)
        resolution = self.detect_resolution(text)
        story_arc = self.analyze_story_arc(text)
        
        analysis = StoryAnalysis(
            filename=filename,
            title=title,
            word_count=word_count,
            sentence_count=sentence_count,
            avg_words_per_sentence=round(avg_words_per_sentence, 1),
            hook_first_sentence=hook,
            hook_word_count=hook_word_count,
            story_arc=story_arc,
            emotional_words=emotional_words,
            dialogue_present=has_dialogue,
            dialogue_count=dialogue_count,
            time_markers=time_markers,
            conflict_indicators=conflict_indicators,
            resolution_present=resolution
        )
        
        self.analyses.append(analysis)
        return analysis
    
    def analyze_batch(self, filepaths: List[str]) -> List[StoryAnalysis]:
        """Analyze multiple files."""
        for filepath in filepaths:
            if os.path.exists(filepath):
                print(f"Analyzing: {os.path.basename(filepath)}")
                self.analyze_file(filepath)
            else:
                print(f"⚠️ File not found: {filepath}")
        return self.analyses
    
    def extract_success_patterns(self) -> Dict:
        """Extract common patterns from all analyzed stories."""
        if not self.analyses:
            return {}
        
        patterns = {
            'total_stories_analyzed': len(self.analyses),
            'average_word_count': round(sum(a.word_count for a in self.analyses) / len(self.analyses), 0),
            'average_sentence_count': round(sum(a.sentence_count for a in self.analyses) / len(self.analyses), 0),
            'average_words_per_sentence': round(sum(a.avg_words_per_sentence for a in self.analyses) / len(self.analyses), 1),
            'average_hook_length': round(sum(a.hook_word_count for a in self.analyses) / len(self.analyses), 1),
            'dialogue_usage': sum(1 for a in self.analyses if a.dialogue_present) / len(self.analyses),
            'resolution_rate': sum(1 for a in self.analyses if a.resolution_present) / len(self.analyses),
            'common_emotional_words': self._get_most_common_words([a.emotional_words for a in self.analyses]),
            'common_time_markers': self._get_most_common_words([a.time_markers for a in self.analyses]),
            'common_conflict_indicators': self._get_most_common_words([a.conflict_indicators for a in self.analyses]),
            'typical_story_arc': self._get_most_common_arc(),
        }
        
        return patterns
    
    def _get_most_common_words(self, word_lists: List[List[str]], top_n: int = 10) -> List[tuple]:
        """Get most common words across all stories."""
        all_words = []
        for word_list in word_lists:
            all_words.extend(word_list)
        counter = Counter(all_words)
        return counter.most_common(top_n)
    
    def _get_most_common_arc(self) -> List[str]:
        """Determine the most common story arc structure."""
        if not self.analyses:
            return []
        
        # Count occurrence of each arc component
        arc_components = []
        for analysis in self.analyses:
            arc_components.extend(analysis.story_arc)
        
        component_counts = Counter(arc_components)
        # Return in logical story order
        typical_order = [
            'Setup/Introduction',
            'Conflict/Problem',
            'Escalation',
            'Climax/Turning Point',
            'Resolution'
        ]
        
        return [comp for comp in typical_order if component_counts.get(comp, 0) > 0]
    
    def generate_report(self, output_path: Optional[str] = None) -> str:
        """Generate comprehensive analysis report."""
        patterns = self.extract_success_patterns()
        
        report = f"""# YouTube Story Success Patterns Analysis

## Overview

Analyzed {patterns['total_stories_analyzed']} successful YouTube stories to extract patterns and rules for creating engaging content.

## Individual Story Analyses

"""
        
        for analysis in self.analyses:
            report += f"""### {analysis.title}

**Basic Metrics:**
- Word Count: {analysis.word_count}
- Sentence Count: {analysis.sentence_count}
- Avg Words/Sentence: {analysis.avg_words_per_sentence}

**Hook Analysis:**
- First Sentence: "{analysis.hook_first_sentence}"
- Hook Length: {analysis.hook_word_count} words

**Story Structure:**
- Story Arc: {' → '.join(analysis.story_arc)}
- Dialogue Present: {'Yes' if analysis.dialogue_present else 'No'} ({analysis.dialogue_count} instances)
- Resolution: {'Yes' if analysis.resolution_present else 'No'}

**Engagement Elements:**
- Emotional Words: {', '.join(analysis.emotional_words[:5])}{'...' if len(analysis.emotional_words) > 5 else ''}
- Time Markers: {', '.join(analysis.time_markers[:5])}{'...' if len(analysis.time_markers) > 5 else ''}
- Conflict Indicators: {', '.join(analysis.conflict_indicators[:5])}{'...' if len(analysis.conflict_indicators) > 5 else ''}

---

"""
        
        report += f"""## Success Patterns & Rules

### Content Length
- **Average Word Count**: {patterns['average_word_count']:.0f} words
- **Average Sentence Count**: {patterns['average_sentence_count']:.0f} sentences
- **Average Words per Sentence**: {patterns['average_words_per_sentence']:.1f} words
- **Recommendation**: Aim for {patterns['average_word_count']-50:.0f}-{patterns['average_word_count']+50:.0f} words per story

### Hook Strategy
- **Average Hook Length**: {patterns['average_hook_length']:.1f} words
- **Rule**: Open with a compelling, concise hook that immediately presents conflict or intrigue
- **Pattern**: Most successful hooks are {patterns['average_hook_length']-5:.0f}-{patterns['average_hook_length']+5:.0f} words

### Story Structure
- **Typical Arc**: {' → '.join(patterns['typical_story_arc'])}
- **Dialogue Usage**: {patterns['dialogue_usage']*100:.0f}% of stories use dialogue
- **Resolution Rate**: {patterns['resolution_rate']*100:.0f}% of stories have clear resolution
- **Rule**: Follow the complete story arc with clear setup, conflict, escalation, climax, and resolution

### Emotional Engagement
**Top Emotional Triggers:**
"""
        
        for word, count in patterns['common_emotional_words'][:10]:
            report += f"- **{word}**: {count} occurrences\n"
        
        report += f"""
**Rule**: Incorporate emotional trigger words naturally throughout the story to maintain engagement.

### Time Progression
**Common Time Markers:**
"""
        
        for marker, count in patterns['common_time_markers'][:10]:
            report += f"- **{marker}**: {count} occurrences\n"
        
        report += f"""
**Rule**: Use time markers to create clear narrative progression and maintain pacing.

### Conflict Development
**Common Conflict Indicators:**
"""
        
        for word, count in patterns['common_conflict_indicators'][:10]:
            report += f"- **{word}**: {count} occurrences\n"
        
        report += f"""
**Rule**: Establish conflict early and escalate throughout the story.

## Key Success Rules

### 1. Hook Formula
- Start with immediate conflict or intrigue
- Keep it under {patterns['average_hook_length']+5:.0f} words
- Use emotional or action-oriented language
- Create curiosity gap

### 2. Story Length
- Target {patterns['average_word_count']:.0f} words (±50 words)
- Break into {patterns['average_sentence_count']:.0f} sentences
- Keep sentences conversational ({patterns['average_words_per_sentence']:.1f} words/sentence average)

### 3. Structure Requirements
✅ Clear setup/introduction
✅ Immediate conflict presentation
✅ Progressive escalation
✅ Dramatic climax/turning point
✅ Satisfying resolution

### 4. Engagement Tactics
- Use dialogue ({patterns['dialogue_usage']*100:.0f}% of successful stories do)
- Include emotional trigger words
- Show clear time progression
- Build conflict naturally
- Provide resolution/payoff

### 5. Content Guidelines
- Focus on relatable conflicts (neighbors, family, work)
- Include specific details and quotes
- Show character reactions
- Create justice/karma moments
- End with closure or lesson learned

## Implementation for StoryGenerator

### Script Generation (GScript.py)
```python
STORY_CONFIG = {{
    'target_word_count': {patterns['average_word_count']:.0f},
    'target_sentences': {patterns['average_sentence_count']:.0f},
    'words_per_sentence': {patterns['average_words_per_sentence']:.1f},
    'hook_max_words': {patterns['average_hook_length']+5:.0f},
    'use_dialogue': {patterns['dialogue_usage']*100:.0f}% probability,
    'require_resolution': True,
    'story_arc': {patterns['typical_story_arc']},
    'emotional_words': {[w for w, c in patterns['common_emotional_words'][:5]]},
}}
```

### Quality Validation
```python
def validate_story(text):
    checks = {{
        'word_count': {patterns['average_word_count']-100:.0f} <= word_count <= {patterns['average_word_count']+100:.0f},
        'has_hook': first_sentence_compelling(),
        'has_conflict': detect_conflict_words(),
        'has_arc': follows_story_structure(),
        'has_resolution': ending_provides_closure(),
        'uses_dialogue': {patterns['dialogue_usage']*100:.0f}% recommended,
    }}
    return all(checks.values())
```

## Conclusion

Successful YouTube stories follow a consistent pattern:
1. **Strong Hook** ({patterns['average_hook_length']:.0f} words) that presents conflict
2. **Optimal Length** (~{patterns['average_word_count']:.0f} words)
3. **Clear Structure** (Setup → Conflict → Escalation → Climax → Resolution)
4. **Emotional Engagement** through trigger words and relatable situations
5. **Natural Dialogue** for authenticity
6. **Satisfying Resolution** for viewer payoff

These patterns should guide story generation in the StoryGenerator pipeline to maximize engagement and virality.

---

**Analysis Date**: {self._get_timestamp()}
**Stories Analyzed**: {patterns['total_stories_analyzed']}
**Output Format**: Markdown Report
"""
        
        if output_path:
            Path(output_path).write_text(report, encoding='utf-8')
            print(f"\n✅ Report saved to: {output_path}")
        
        return report
    
    def _get_timestamp(self):
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def save_json(self, output_path: str):
        """Save analysis data as JSON."""
        data = {
            'analyses': [a.to_dict() for a in self.analyses],
            'patterns': self.extract_success_patterns(),
            'timestamp': self._get_timestamp()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ JSON data saved to: {output_path}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python story_pattern_analyzer.py <subtitle_file1> <subtitle_file2> ...")
        print("Example: python story_pattern_analyzer.py /tmp/subtitle*.txt")
        sys.exit(1)
    
    filepaths = sys.argv[1:]
    
    print(f"\n🔬 Story Pattern Analyzer")
    print(f"📊 Analyzing {len(filepaths)} subtitle files...\n")
    
    analyzer = StoryPatternAnalyzer()
    analyzer.analyze_batch(filepaths)
    
    if analyzer.analyses:
        # Generate report
        report = analyzer.generate_report('/tmp/story_patterns_report.md')
        print(report)
        
        # Save JSON
        analyzer.save_json('/tmp/story_patterns_analysis.json')
        
        print("\n✅ Analysis complete!")
        print(f"📄 Markdown report: /tmp/story_patterns_report.md")
        print(f"💾 JSON data: /tmp/story_patterns_analysis.json")
    else:
        print("\n❌ No stories analyzed")
        sys.exit(1)


if __name__ == "__main__":
    main()
