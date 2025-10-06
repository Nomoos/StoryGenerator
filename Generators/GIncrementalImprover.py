import os
import json
import openai
from typing import Dict, List, Any, Optional
from datetime import datetime
from Models.StoryIdea import StoryIdea
from Generators.GSceneAnalyzer import SceneAnalyzer
from Tools.Utils import TITLES_PATH, sanitize_filename

openai.api_key = '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'


class IncrementalImprover:
    """
    Implements iterative improvement system for video generation.
    
    Features:
    - Analyzes generated outputs for quality issues
    - Suggests improvements based on feedback
    - Tracks improvement history
    - Learns from successful iterations
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.analyzer = SceneAnalyzer()

    def analyze_video_quality(
        self,
        story_idea: StoryIdea,
        user_feedback: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze video quality and suggest improvements
        
        Args:
            story_idea: StoryIdea object
            user_feedback: Optional user feedback on the video
            
        Returns:
            Dictionary with analysis and improvement suggestions
        """
        folder_path = os.path.join(TITLES_PATH, sanitize_filename(story_idea.story_title))
        
        # Load scenes and their descriptions
        scenes = self.analyzer.load_scenes(story_idea)
        
        # Load improvement history
        history = self._load_improvement_history(folder_path)
        
        # Analyze current state
        analysis = {
            'story_title': story_idea.story_title,
            'timestamp': datetime.now().isoformat(),
            'iteration': len(history) + 1,
            'scene_count': len(scenes),
            'issues': [],
            'suggestions': [],
            'scores': {}
        }
        
        # Automated quality checks
        print(f"🔍 Analyzing video quality for '{story_idea.story_title}'...")
        
        # Check 1: Scene duration consistency
        durations = [scene.duration for scene in scenes]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        if any(d < 2 for d in durations):
            analysis['issues'].append("Some scenes are too short (< 2 seconds)")
            analysis['suggestions'].append("Consider merging very short scenes or adjusting segmentation")
        
        if any(d > 15 for d in durations):
            analysis['issues'].append("Some scenes are too long (> 15 seconds)")
            analysis['suggestions'].append("Split long scenes into multiple segments for better pacing")
        
        analysis['scores']['scene_duration'] = min(1.0, 1 - (abs(avg_duration - 7) / 10))
        
        # Check 2: Visual description quality
        description_lengths = [len(scene.description.split()) for scene in scenes if scene.description]
        avg_desc_length = sum(description_lengths) / len(description_lengths) if description_lengths else 0
        
        if avg_desc_length < 20:
            analysis['issues'].append("Scene descriptions are too brief")
            analysis['suggestions'].append("Regenerate scene descriptions with more visual detail")
        
        if avg_desc_length > 100:
            analysis['issues'].append("Scene descriptions are too verbose")
            analysis['suggestions'].append("Simplify scene descriptions for better image generation")
        
        analysis['scores']['description_quality'] = min(1.0, avg_desc_length / 50)
        
        # Check 3: Keyframe coverage
        scenes_with_keyframes = sum(1 for scene in scenes if scene.keyframes)
        keyframe_coverage = scenes_with_keyframes / len(scenes) if scenes else 0
        
        if keyframe_coverage < 1.0:
            missing = len(scenes) - scenes_with_keyframes
            analysis['issues'].append(f"{missing} scenes missing keyframes")
            analysis['suggestions'].append("Regenerate keyframes for all scenes")
        
        analysis['scores']['keyframe_coverage'] = keyframe_coverage
        
        # Check 4: Get GPT-based quality assessment
        if user_feedback:
            gpt_analysis = self._get_gpt_quality_analysis(story_idea, scenes, user_feedback)
            analysis['gpt_analysis'] = gpt_analysis
            analysis['issues'].extend(gpt_analysis.get('issues', []))
            analysis['suggestions'].extend(gpt_analysis.get('suggestions', []))
        
        # Calculate overall quality score
        scores = analysis['scores']
        analysis['overall_score'] = sum(scores.values()) / len(scores) if scores else 0
        
        # Save analysis
        self._save_improvement_history(folder_path, history + [analysis])
        
        return analysis

    def _get_gpt_quality_analysis(
        self,
        story_idea: StoryIdea,
        scenes: List,
        user_feedback: str
    ) -> Dict[str, Any]:
        """Use GPT to analyze quality based on user feedback"""
        
        scenes_summary = "\n".join([
            f"Scene {s.scene_id}: {s.text[:100]}... (duration: {s.duration:.1f}s)"
            for s in scenes[:5]  # First 5 scenes for context
        ])
        
        prompt = f"""Analyze this short-form vertical video and provide quality assessment.

Story: {story_idea.story_title}
Total Scenes: {len(scenes)}

Sample Scenes:
{scenes_summary}

User Feedback:
{user_feedback}

Please provide:
1. Key issues identified (be specific)
2. Concrete improvement suggestions
3. Priority areas to focus on

Format your response as JSON with keys: "issues" (list), "suggestions" (list), "priorities" (list)"""

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional video quality analyst for short-form vertical content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            content = response.choices[0].message.content.strip()
            
            # Try to parse as JSON
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {'issues': [content], 'suggestions': [], 'priorities': []}
                
        except Exception as e:
            print(f"⚠️ GPT analysis failed: {e}")
            return {'issues': [], 'suggestions': [], 'priorities': []}

    def apply_improvements(
        self,
        story_idea: StoryIdea,
        improvements: List[str]
    ) -> Dict[str, Any]:
        """
        Apply specific improvements to the video pipeline
        
        Args:
            story_idea: StoryIdea object
            improvements: List of improvement actions to apply
                         e.g., ["regenerate_scenes", "improve_descriptions", "regenerate_keyframes"]
            
        Returns:
            Dictionary with results of improvement actions
        """
        folder_path = os.path.join(TITLES_PATH, sanitize_filename(story_idea.story_title))
        results = {}
        
        print(f"🔧 Applying improvements to '{story_idea.story_title}'...")
        
        for improvement in improvements:
            print(f"  → {improvement}")
            
            try:
                if improvement == "regenerate_scenes":
                    # Re-analyze with different parameters
                    from Generators.GSceneAnalyzer import SceneAnalyzer
                    analyzer = SceneAnalyzer(min_scene_duration=4.0, max_scene_duration=12.0)
                    analyzer.analyze_story(story_idea)
                    results[improvement] = "success"
                    
                elif improvement == "improve_descriptions":
                    # Regenerate scene descriptions
                    from Generators.GSceneDescriber import SceneDescriber
                    describer = SceneDescriber()
                    describer.describe_scenes(story_idea)
                    results[improvement] = "success"
                    
                elif improvement == "regenerate_keyframes":
                    # Regenerate keyframes
                    from Generators.GKeyframeGenerator import KeyframeGenerator
                    generator = KeyframeGenerator()
                    generator.generate_keyframes(story_idea)
                    results[improvement] = "success"
                    
                elif improvement == "adjust_pacing":
                    # Modify scene durations
                    self._adjust_scene_pacing(story_idea)
                    results[improvement] = "success"
                    
                else:
                    results[improvement] = f"unknown_action: {improvement}"
                    
            except Exception as e:
                print(f"  ❌ Failed: {e}")
                results[improvement] = f"error: {str(e)}"
        
        return results

    def _adjust_scene_pacing(self, story_idea: StoryIdea):
        """Adjust scene pacing based on content"""
        scenes = self.analyzer.load_scenes(story_idea)
        
        # Analyze emotional intensity and adjust timing
        for scene in scenes:
            # This is a placeholder - would implement actual pacing logic
            # based on emotion detection, content analysis, etc.
            pass
        
        # Save adjusted scenes
        folder_path = os.path.join(TITLES_PATH, sanitize_filename(story_idea.story_title))
        self.analyzer._save_scenes(scenes, folder_path)

    def get_improvement_suggestions(
        self,
        story_idea: StoryIdea,
        focus_area: Optional[str] = None
    ) -> List[str]:
        """
        Get AI-generated improvement suggestions
        
        Args:
            story_idea: StoryIdea object
            focus_area: Optional area to focus on (e.g., "pacing", "visuals", "emotional_impact")
            
        Returns:
            List of improvement suggestions
        """
        analysis = self.analyze_video_quality(story_idea)
        
        suggestions = analysis['suggestions']
        
        if focus_area:
            # Filter suggestions by focus area
            filtered = [s for s in suggestions if focus_area.lower() in s.lower()]
            return filtered if filtered else suggestions
        
        return suggestions

    def _load_improvement_history(self, folder_path: str) -> List[Dict[str, Any]]:
        """Load improvement history from file"""
        history_file = os.path.join(folder_path, "improvement_history.json")
        
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                return json.load(f)
        return []

    def _save_improvement_history(self, folder_path: str, history: List[Dict[str, Any]]):
        """Save improvement history to file"""
        history_file = os.path.join(folder_path, "improvement_history.json")
        
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)

    def compare_iterations(self, story_idea: StoryIdea) -> Dict[str, Any]:
        """
        Compare different iterations of the video
        
        Args:
            story_idea: StoryIdea object
            
        Returns:
            Comparison data showing improvements over iterations
        """
        folder_path = os.path.join(TITLES_PATH, sanitize_filename(story_idea.story_title))
        history = self._load_improvement_history(folder_path)
        
        if len(history) < 2:
            return {
                'message': 'Need at least 2 iterations to compare',
                'current_iteration': len(history)
            }
        
        # Compare scores across iterations
        comparison = {
            'iterations': len(history),
            'score_progression': [h.get('overall_score', 0) for h in history],
            'improvement': None,
            'best_iteration': None
        }
        
        if comparison['score_progression']:
            scores = comparison['score_progression']
            comparison['improvement'] = scores[-1] - scores[0]
            comparison['best_iteration'] = scores.index(max(scores)) + 1
        
        return comparison
