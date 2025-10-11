"""
Script Development Module - Generate, Score, and Improve Video Scripts

This module provides functionality for:
1. Generating initial scripts from video ideas
2. Scoring script quality across multiple dimensions
3. Iteratively improving scripts
4. GPT-based enhancement
5. Title optimization
"""

import json
import logging
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from PrismQ.Shared.interfaces.llm_provider import ILLMProvider

logger = logging.getLogger(__name__)


@dataclass
class ScriptQualityScores:
    """Quality scores for a script across multiple dimensions."""
    engagement: float  # 0-100: How engaging is the content?
    clarity: float  # 0-100: How clear is the narrative?
    pacing: float  # 0-100: Is the pacing appropriate?
    demographic_fit: float  # 0-100: Does it fit target demographics?
    storytelling: float  # 0-100: Quality of storytelling elements
    hook_strength: float  # 0-100: Strength of opening hook
    
    @property
    def overall_score(self) -> float:
        """Calculate weighted overall score."""
        weights = {
            'engagement': 0.25,
            'clarity': 0.15,
            'pacing': 0.15,
            'demographic_fit': 0.15,
            'storytelling': 0.20,
            'hook_strength': 0.10
        }
        return (
            self.engagement * weights['engagement'] +
            self.clarity * weights['clarity'] +
            self.pacing * weights['pacing'] +
            self.demographic_fit * weights['demographic_fit'] +
            self.storytelling * weights['storytelling'] +
            self.hook_strength * weights['hook_strength']
        )
    
    def to_dict(self) -> dict[str, float]:
        """Convert to dictionary."""
        data = asdict(self)
        data['overall_score'] = self.overall_score
        return data


@dataclass
class Script:
    """Represents a video script with metadata."""
    script_id: str
    content: str
    title: str
    target_gender: str
    target_age: str
    version: int
    word_count: int
    estimated_duration: float  # in seconds
    quality_scores: ScriptQualityScores | None = None
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: dict[str, object] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, object]:
        """Convert to dictionary."""
        data = asdict(self)
        if self.quality_scores:
            data['quality_scores'] = self.quality_scores.to_dict()
        return data
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)


class ScriptGenerator:
    """
    Generates initial video scripts from ideas.
    
    Takes video ideas and generates engaging scripts suitable for
    short-form video content (30-60 seconds).
    """
    
    def __init__(self, llm_provider: ILLMProvider, output_root: str | None = None):
        """
        Initialize ScriptGenerator.
        
        Args:
            llm_provider: LLM provider for script generation
            output_root: Root directory for output files
        """
        self.llm = llm_provider
        self.output_root = Path(output_root) if output_root else Path("Generator/scripts")
        logger.info(f"Initialized ScriptGenerator with model: {llm_provider.model_name}")
    
    def generate_script(
        self,
        idea: Dict,
        target_duration: float = 45.0,
        style: str = "engaging"
    ) -> Script:
        """
        Generate a script from a video idea.
        
        Args:
            idea: Video idea dict with 'content', 'target_gender', 'target_age', etc.
            target_duration: Target duration in seconds (default: 45)
            style: Script style ('engaging', 'dramatic', 'educational')
        
        Returns:
            Generated Script object
        """
        # Calculate target word count (150 words per minute = 2.5 wpm)
        target_words = int((target_duration / 60) * 150)
        
        prompt = self._build_generation_prompt(
            idea=idea,
            target_words=target_words,
            style=style
        )
        
        try:
            script_content = self.llm.generate_completion(
                prompt=prompt,
                temperature=0.8,
                max_tokens=target_words * 2  # Allow some buffer
            )
            
            # Clean up the generated script
            script_content = self._clean_script(script_content)
            
            # Calculate actual metrics
            word_count = len(script_content.split())
            estimated_duration = (word_count / 150) * 60  # words / wpm * 60
            
            script = Script(
                script_id=idea.get('id', f"script_{datetime.now().timestamp()}"),
                content=script_content,
                title=idea.get('title', 'Untitled'),
                target_gender=idea.get('target_gender', 'all'),
                target_age=idea.get('target_age', 'all'),
                version=0,
                word_count=word_count,
                estimated_duration=estimated_duration,
                metadata={
                    'source_idea_id': idea.get('id'),
                    'generation_style': style,
                    'target_duration': target_duration
                }
            )
            
            logger.info(f"Generated script v0: {script.script_id} ({word_count} words)")
            return script
            
        except Exception as e:
            logger.error(f"Error generating script: {e}")
            raise
    
    def _build_generation_prompt(
        self,
        idea: Dict,
        target_words: int,
        style: str
    ) -> str:
        """Build prompt for script generation."""
        idea_content = idea.get('content', '')
        gender = idea.get('target_gender', 'all')
        age = idea.get('target_age', 'all')
        
        style_instructions = {
            'engaging': 'Create an engaging, captivating script that hooks viewers immediately.',
            'dramatic': 'Create a dramatic script with emotional impact and tension.',
            'educational': 'Create an informative script that teaches while entertaining.'
        }
        
        prompt = f"""Write a video script for a short-form video (TikTok/YouTube Shorts style).

IDEA: {idea_content}

TARGET AUDIENCE: {gender}, age {age}

STYLE: {style_instructions.get(style, style_instructions['engaging'])}

REQUIREMENTS:
- Target length: {target_words} words
- Start with a strong hook in the first 3 seconds
- Use second-person perspective ("you") to engage viewers
- Include storytelling elements (setup, conflict, resolution)
- Maintain fast pacing suitable for short-form content
- End with a thought-provoking question or call-to-action
- Write in a conversational, natural tone
- NO stage directions or camera instructions - just the narration

Write ONLY the script narration, nothing else:"""
        
        return prompt
    
    def _clean_script(self, content: str) -> str:
        """Clean up generated script content."""
        # Remove markdown formatting
        content = re.sub(r'\*\*|\*|__|_', '', content)
        
        # Remove stage directions in brackets or parentheses
        content = re.sub(r'\[.*?\]|\(.*?\)', '', content)
        
        # Remove multiple spaces/newlines
        content = re.sub(r'\n\n+', '\n\n', content)
        content = re.sub(r' +', ' ', content)
        
        return content.strip()
    
    def save_script(self, script: Script, version_label: str = "v0") -> Path:
        """
        Save script to file.
        
        Args:
            script: Script object to save
            version_label: Version label (v0, v1, v2, etc.)
        
        Returns:
            Path to saved file
        """
        # Create output directory
        output_dir = self.output_root / version_label / script.target_gender / script.target_age
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save JSON file
        output_file = output_dir / f"{script.script_id}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(script.to_json())
        
        logger.debug(f"Saved script to: {output_file}")
        return output_file


class ScriptScorer:
    """
    Scores script quality across multiple dimensions.
    
    Evaluates scripts for engagement, clarity, pacing, demographic fit,
    storytelling quality, and hook strength.
    """
    
    def __init__(self, llm_provider: ILLMProvider):
        """
        Initialize ScriptScorer.
        
        Args:
            llm_provider: LLM provider for quality assessment
        """
        self.llm = llm_provider
        logger.info(f"Initialized ScriptScorer with model: {llm_provider.model_name}")
    
    def score_script(
        self,
        script: Script,
        detailed: bool = True
    ) -> ScriptQualityScores:
        """
        Score a script's quality across multiple dimensions.
        
        Args:
            script: Script object to score
            detailed: Whether to generate detailed feedback
        
        Returns:
            ScriptQualityScores object with scores for each dimension
        """
        prompt = self._build_scoring_prompt(script, detailed)
        
        try:
            response = self.llm.generate_completion(
                prompt=prompt,
                temperature=0.3,  # Lower temperature for consistent scoring
                max_tokens=500
            )
            
            scores = self._parse_scores(response)
            
            logger.info(
                f"Scored script {script.script_id}: "
                f"Overall={scores.overall_score:.1f}"
            )
            
            return scores
            
        except Exception as e:
            logger.error(f"Error scoring script: {e}")
            # Return default middle scores on error
            return ScriptQualityScores(
                engagement=50.0,
                clarity=50.0,
                pacing=50.0,
                demographic_fit=50.0,
                storytelling=50.0,
                hook_strength=50.0
            )
    
    def _build_scoring_prompt(self, script: Script, detailed: bool) -> str:
        """Build prompt for script scoring."""
        prompt = f"""Evaluate this video script for short-form content.

SCRIPT:
{script.content}

TARGET AUDIENCE: {script.target_gender}, age {script.target_age}
DURATION: {script.estimated_duration:.1f} seconds

Rate the script on these dimensions (0-100):

1. ENGAGEMENT: How captivating is the content? Does it hook viewers?
2. CLARITY: How clear and easy to understand is the narrative?
3. PACING: Is the pacing appropriate for short-form content?
4. DEMOGRAPHIC FIT: How well does it match the target audience?
5. STORYTELLING: Quality of narrative structure and emotional impact
6. HOOK STRENGTH: How strong is the opening hook?

Provide scores in this exact format:
ENGAGEMENT: <score>
CLARITY: <score>
PACING: <score>
DEMOGRAPHIC_FIT: <score>
STORYTELLING: <score>
HOOK_STRENGTH: <score>"""
        
        if detailed:
            prompt += "\n\nThen provide brief feedback for improvement."
        
        return prompt
    
    def _parse_scores(self, response: str) -> ScriptQualityScores:
        """Parse scores from LLM response."""
        scores_dict = {}
        
        # Extract scores using regex
        patterns = {
            'engagement': r'ENGAGEMENT:\s*(\d+)',
            'clarity': r'CLARITY:\s*(\d+)',
            'pacing': r'PACING:\s*(\d+)',
            'demographic_fit': r'DEMOGRAPHIC[_\s]FIT:\s*(\d+)',
            'storytelling': r'STORYTELLING:\s*(\d+)',
            'hook_strength': r'HOOK[_\s]STRENGTH:\s*(\d+)'
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                scores_dict[key] = float(match.group(1))
            else:
                scores_dict[key] = 50.0  # Default to middle score
        
        return ScriptQualityScores(**scores_dict)


class ScriptIterator:
    """
    Iteratively improves scripts based on quality scores.
    
    Takes scripts and their scores, identifies weaknesses,
    and generates improved versions.
    """
    
    def __init__(self, llm_provider: ILLMProvider):
        """
        Initialize ScriptIterator.
        
        Args:
            llm_provider: LLM provider for script improvement
        """
        self.llm = llm_provider
        logger.info(f"Initialized ScriptIterator with model: {llm_provider.model_name}")
    
    def improve_script(
        self,
        script: Script,
        max_iterations: int = 3,
        target_score: float = 80.0
    ) -> list[Script]:
        """
        Iteratively improve a script until target score is reached or max iterations.
        
        Args:
            script: Initial script to improve
            max_iterations: Maximum number of improvement iterations
            target_score: Target overall quality score to achieve
        
        Returns:
            List of script versions (including original)
        """
        from PrismQ.StoryGenerator.script_development import ScriptScorer
        
        scorer = ScriptScorer(self.llm)
        versions = [script]
        
        # Score initial version if not already scored
        if script.quality_scores is None:
            script.quality_scores = scorer.score_script(script)
            versions[0] = script
        
        logger.info(
            f"Starting iteration for {script.script_id}: "
            f"Initial score={script.quality_scores.overall_score:.1f}"
        )
        
        for iteration in range(max_iterations):
            current = versions[-1]
            
            # Check if target reached
            if current.quality_scores.overall_score >= target_score:
                logger.info(f"Target score reached after {iteration} iterations")
                break
            
            # Identify weaknesses
            weaknesses = self._identify_weaknesses(current.quality_scores)
            
            if not weaknesses:
                logger.info("No significant weaknesses found")
                break
            
            # Generate improved version
            improved = self._generate_improved_version(
                script=current,
                weaknesses=weaknesses,
                iteration=iteration + 1
            )
            
            # Score improved version
            improved.quality_scores = scorer.score_script(improved)
            
            versions.append(improved)
            
            logger.info(
                f"Iteration {iteration + 1}: "
                f"Score={improved.quality_scores.overall_score:.1f} "
                f"(delta={improved.quality_scores.overall_score - current.quality_scores.overall_score:+.1f})"
            )
            
            # Stop if no improvement
            if improved.quality_scores.overall_score <= current.quality_scores.overall_score:
                logger.info("No improvement detected, stopping iteration")
                break
        
        return versions
    
    def _identify_weaknesses(self, scores: ScriptQualityScores) -> List[Tuple[str, float]]:
        """Identify weak dimensions that need improvement."""
        threshold = 70.0  # Dimensions below this are considered weak
        
        dimensions = {
            'engagement': scores.engagement,
            'clarity': scores.clarity,
            'pacing': scores.pacing,
            'demographic_fit': scores.demographic_fit,
            'storytelling': scores.storytelling,
            'hook_strength': scores.hook_strength
        }
        
        weaknesses = [
            (dim, score)
            for dim, score in dimensions.items()
            if score < threshold
        ]
        
        # Sort by score (weakest first)
        weaknesses.sort(key=lambda x: x[1])
        
        return weaknesses
    
    def _generate_improved_version(
        self,
        script: Script,
        weaknesses: List[Tuple[str, float]],
        iteration: int
    ) -> Script:
        """Generate an improved version of the script."""
        prompt = self._build_improvement_prompt(script, weaknesses)
        
        try:
            improved_content = self.llm.generate_completion(
                prompt=prompt,
                temperature=0.7,
                max_tokens=len(script.content.split()) * 2
            )
            
            # Clean up
            improved_content = self._clean_script(improved_content)
            
            # Create new script version
            improved = Script(
                script_id=script.script_id,
                content=improved_content,
                title=script.title,
                target_gender=script.target_gender,
                target_age=script.target_age,
                version=script.version + 1,
                word_count=len(improved_content.split()),
                estimated_duration=(len(improved_content.split()) / 150) * 60,
                metadata={
                    **script.metadata,
                    'iteration': iteration,
                    'weaknesses_addressed': [w[0] for w in weaknesses]
                }
            )
            
            return improved
            
        except Exception as e:
            logger.error(f"Error generating improved version: {e}")
            # Return original on error
            return script
    
    def _build_improvement_prompt(
        self,
        script: Script,
        weaknesses: List[Tuple[str, float]]
    ) -> str:
        """Build prompt for script improvement."""
        weakness_descriptions = {
            'engagement': 'more captivating and attention-grabbing',
            'clarity': 'clearer and easier to understand',
            'pacing': 'better paced for short-form content',
            'demographic_fit': 'better suited to the target audience',
            'storytelling': 'stronger narrative and emotional impact',
            'hook_strength': 'a much stronger opening hook'
        }
        
        improvements_needed = [
            f"- Make it {weakness_descriptions[weak[0]]}"
            for weak in weaknesses[:3]  # Focus on top 3 weaknesses
        ]
        
        prompt = f"""Improve this video script while maintaining its core message.

CURRENT SCRIPT:
{script.content}

TARGET AUDIENCE: {script.target_gender}, age {script.target_age}

IMPROVEMENTS NEEDED:
{chr(10).join(improvements_needed)}

GUIDELINES:
- Keep the same approximate length
- Maintain the conversational tone
- Preserve the core message and storyline
- Focus on the improvements listed above
- Write ONLY the improved script, nothing else

Improved script:"""
        
        return prompt
    
    def _clean_script(self, content: str) -> str:
        """Clean up script content (reuse from ScriptGenerator)."""
        content = re.sub(r'\*\*|\*|__|_', '', content)
        content = re.sub(r'\[.*?\]|\(.*?\)', '', content)
        content = re.sub(r'\n\n+', '\n\n', content)
        content = re.sub(r' +', ' ', content)
        return content.strip()


class ScriptEnhancer:
    """
    Enhances scripts using GPT-4 or advanced LLMs.
    
    Takes scripts and applies sophisticated improvements using
    more capable models for final polish.
    """
    
    def __init__(self, llm_provider: ILLMProvider):
        """
        Initialize ScriptEnhancer.
        
        Args:
            llm_provider: Advanced LLM provider (e.g., GPT-4) for enhancement
        """
        self.llm = llm_provider
        logger.info(f"Initialized ScriptEnhancer with model: {llm_provider.model_name}")
    
    def enhance_script(self, script: Script) -> Script:
        """
        Enhance script using advanced LLM.
        
        Args:
            script: Script to enhance
        
        Returns:
            Enhanced Script object
        """
        prompt = self._build_enhancement_prompt(script)
        
        try:
            enhanced_content = self.llm.generate_completion(
                prompt=prompt,
                temperature=0.7,
                max_tokens=len(script.content.split()) * 2
            )
            
            # Clean up
            enhanced_content = self._clean_script(enhanced_content)
            
            # Create enhanced version
            enhanced = Script(
                script_id=script.script_id,
                content=enhanced_content,
                title=script.title,
                target_gender=script.target_gender,
                target_age=script.target_age,
                version=script.version + 1,
                word_count=len(enhanced_content.split()),
                estimated_duration=(len(enhanced_content.split()) / 150) * 60,
                quality_scores=script.quality_scores,  # Copy scores, will be re-scored
                metadata={
                    **script.metadata,
                    'enhanced': True,
                    'enhancement_model': self.llm.model_name
                }
            )
            
            logger.info(f"Enhanced script {script.script_id} to v{enhanced.version}")
            return enhanced
            
        except Exception as e:
            logger.error(f"Error enhancing script: {e}")
            return script
    
    def _build_enhancement_prompt(self, script: Script) -> str:
        """Build prompt for script enhancement."""
        prompt = f"""Polish and enhance this video script to make it exceptional.

CURRENT SCRIPT:
{script.content}

TARGET AUDIENCE: {script.target_gender}, age {script.target_age}

ENHANCEMENT GOALS:
- Elevate the language while keeping it conversational
- Enhance emotional resonance and impact
- Sharpen the storytelling and narrative flow
- Strengthen transitions between ideas
- Add subtle rhetorical devices for persuasion
- Ensure maximum viewer retention
- Polish the ending for memorable impact

MAINTAIN:
- Same approximate length
- Core message and storyline
- Conversational, accessible tone
- Second-person perspective

Write ONLY the enhanced script:"""
        
        return prompt
    
    def _clean_script(self, content: str) -> str:
        """Clean up script content."""
        content = re.sub(r'\*\*|\*|__|_', '', content)
        content = re.sub(r'\[.*?\]|\(.*?\)', '', content)
        content = re.sub(r'\n\n+', '\n\n', content)
        content = re.sub(r' +', ' ', content)
        return content.strip()


class TitleOptimizer:
    """
    Optimizes video titles for clickability and SEO.
    
    Takes scripts and generates multiple title variations
    optimized for discovery and engagement.
    """
    
    def __init__(self, llm_provider: ILLMProvider):
        """
        Initialize TitleOptimizer.
        
        Args:
            llm_provider: LLM provider for title generation
        """
        self.llm = llm_provider
        logger.info(f"Initialized TitleOptimizer with model: {llm_provider.model_name}")
    
    def generate_title_variants(
        self,
        script: Script,
        num_variants: int = 5
    ) -> List[Dict]:
        """
        Generate multiple title variants for a script.
        
        Args:
            script: Script to generate titles for
            num_variants: Number of title variations to generate
        
        Returns:
            List of title variant dicts with 'title', 'style', 'rationale'
        """
        prompt = self._build_title_prompt(script, num_variants)
        
        try:
            response = self.llm.generate_completion(
                prompt=prompt,
                temperature=0.9,  # Higher creativity for titles
                max_tokens=500
            )
            
            variants = self._parse_title_variants(response)
            
            logger.info(f"Generated {len(variants)} title variants for {script.script_id}")
            return variants
            
        except Exception as e:
            logger.error(f"Error generating title variants: {e}")
            return [{
                'title': script.title,
                'style': 'original',
                'rationale': 'Error generating variants, using original title'
            }]
    
    def _build_title_prompt(self, script: Script, num_variants: int) -> str:
        """Build prompt for title generation."""
        # Extract first 100 words for context
        script_preview = ' '.join(script.content.split()[:100])
        
        prompt = f"""Generate {num_variants} viral video title variations for this script.

SCRIPT PREVIEW:
{script_preview}...

TARGET AUDIENCE: {script.target_gender}, age {script.target_age}

CURRENT TITLE: {script.title}

Generate {num_variants} title variants using different styles:
1. Curiosity Gap (e.g., "What Happens When...")
2. How-To/Value (e.g., "How I Discovered...")
3. Shocking/Controversial (e.g., "Nobody Talks About...")
4. Listicle/Number (e.g., "3 Secrets About...")
5. Personal Story (e.g., "I Tried... and This Happened")

For each variant, provide:
TITLE: <the title>
STYLE: <style category>
RATIONALE: <why this works>

Keep titles under 60 characters for optimal display."""
        
        return prompt
    
    def _parse_title_variants(self, response: str) -> List[Dict]:
        """Parse title variants from LLM response."""
        variants = []
        
        # Split by title markers
        blocks = re.split(r'TITLE:', response, flags=re.IGNORECASE)
        
        for block in blocks[1:]:  # Skip first empty block
            lines = block.strip().split('\n')
            if not lines:
                continue
            
            title = lines[0].strip()
            style = 'unknown'
            rationale = ''
            
            # Extract style and rationale
            for line in lines[1:]:
                if line.strip().upper().startswith('STYLE:'):
                    style = line.split(':', 1)[1].strip()
                elif line.strip().upper().startswith('RATIONALE:'):
                    rationale = line.split(':', 1)[1].strip()
            
            if title:
                variants.append({
                    'title': title,
                    'style': style,
                    'rationale': rationale
                })
        
        return variants


# Convenience function for complete script development workflow
def develop_script(
    idea: Dict,
    llm_provider: ILLMProvider,
    output_root: Optional[str] = None,
    target_score: float = 80.0,
    max_iterations: int = 3,
    enhance: bool = True,
    generate_titles: bool = True
) -> Dict:
    """
    Complete script development workflow.
    
    Args:
        idea: Video idea to develop script for
        llm_provider: LLM provider
        output_root: Root directory for output
        target_score: Target quality score
        max_iterations: Max improvement iterations
        enhance: Whether to enhance with GPT-4
        generate_titles: Whether to generate title variants
    
    Returns:
        Dict with 'scripts', 'best_script', 'titles', 'summary'
    """
    generator = ScriptGenerator(llm_provider, output_root)
    iterator = ScriptIterator(llm_provider)
    
    # Generate initial script
    initial_script = generator.generate_script(idea)
    
    # Iteratively improve
    script_versions = iterator.improve_script(
        initial_script,
        max_iterations=max_iterations,
        target_score=target_score
    )
    
    best_script = script_versions[-1]
    
    # Enhance if requested
    if enhance:
        enhancer = ScriptEnhancer(llm_provider)
        best_script = enhancer.enhance_script(best_script)
    
    # Generate title variants if requested
    titles = []
    if generate_titles:
        optimizer = TitleOptimizer(llm_provider)
        titles = optimizer.generate_title_variants(best_script, num_variants=5)
    
    # Save best version
    output_path = generator.save_script(best_script, f"v{best_script.version}")
    
    return {
        'scripts': script_versions + ([best_script] if enhance else []),
        'best_script': best_script,
        'titles': titles,
        'output_path': str(output_path),
        'summary': {
            'total_versions': len(script_versions) + (1 if enhance else 0),
            'initial_score': script_versions[0].quality_scores.overall_score if script_versions[0].quality_scores else 0,
            'final_score': best_script.quality_scores.overall_score if best_script.quality_scores else 0,
            'improvement': (
                best_script.quality_scores.overall_score - script_versions[0].quality_scores.overall_score
                if best_script.quality_scores and script_versions[0].quality_scores else 0
            )
        }
    }
