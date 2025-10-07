import os
import json
from typing import Optional, Dict, Any
from Models.StoryIdea import StoryIdea
from Generators.GSceneAnalyzer import SceneAnalyzer
from Generators.GSceneDescriber import SceneDescriber
from Generators.GKeyframeGenerator import KeyframeGenerator
from Generators.GVideoInterpolator import VideoInterpolator
from Generators.GVideoCompositor import VideoCompositor
from Tools.Utils import TITLES_PATH, sanitize_filename


class VideoPipeline:
    """
    Main orchestrator for the complete video generation pipeline.
    
    Pipeline Flow:
    1. Scene Analysis: Analyze subtitles to create scene segments
    2. Scene Description: Generate visual descriptions for each scene
    3. Keyframe Generation: Create keyframe images using Stable Diffusion
    4. Video Interpolation: Interpolate between keyframes to create smooth video
    5. Final Composition: Combine video segments, audio, and subtitles
    """

    def __init__(
        self,
        use_gpu: bool = True,
        num_inference_steps: int = 30,
        target_fps: int = 30
    ):
        """
        Initialize the video pipeline
        
        Args:
            use_gpu: Whether to use GPU for image generation
            num_inference_steps: Number of steps for Stable Diffusion
            target_fps: Target frames per second for output video
        """
        self.use_gpu = use_gpu
        self.num_inference_steps = num_inference_steps
        self.target_fps = target_fps
        
        # Initialize components
        self.scene_analyzer = SceneAnalyzer()
        self.scene_describer = SceneDescriber()
        self.keyframe_generator = None  # Lazy load (heavy model)
        self.video_interpolator = VideoInterpolator(target_fps=target_fps)
        self.video_compositor = VideoCompositor()

    def generate_video(
        self,
        story_idea: StoryIdea,
        skip_existing: bool = True,
        add_subtitles: bool = True,
        background_music: Optional[str] = None
    ) -> str:
        """
        Generate complete video for a story
        
        Args:
            story_idea: StoryIdea object
            skip_existing: Skip steps if output already exists
            add_subtitles: Whether to add subtitles overlay
            background_music: Path to background music file
            
        Returns:
            Path to final video file
        """
        print(f"\n{'='*60}")
        print(f"🎬 VIDEO PIPELINE: {story_idea.story_title}")
        print(f"{'='*60}\n")
        
        folder_path = os.path.join(TITLES_PATH, sanitize_filename(story_idea.story_title))
        
        # Create pipeline state file
        state_file = os.path.join(folder_path, "pipeline_state.json")
        state = self._load_state(state_file)
        
        try:
            # Step 1: Scene Analysis
            if not state.get('scenes_analyzed') or not skip_existing:
                print("\n📊 STEP 1: Scene Analysis")
                print("-" * 60)
                self.scene_analyzer.analyze_story(story_idea)
                state['scenes_analyzed'] = True
                self._save_state(state, state_file)
            else:
                print("\n✅ STEP 1: Scene Analysis (skipped - already done)")
            
            # Step 2: Scene Description
            if not state.get('scenes_described') or not skip_existing:
                print("\n🎨 STEP 2: Visual Scene Description")
                print("-" * 60)
                self.scene_describer.describe_scenes(story_idea)
                state['scenes_described'] = True
                self._save_state(state, state_file)
            else:
                print("\n✅ STEP 2: Visual Scene Description (skipped - already done)")
            
            # Step 3: Keyframe Generation
            if not state.get('keyframes_generated') or not skip_existing:
                print("\n🖼️  STEP 3: Keyframe Generation")
                print("-" * 60)
                
                # Lazy load the keyframe generator (heavy model)
                if self.keyframe_generator is None:
                    device = "cuda" if self.use_gpu else "cpu"
                    self.keyframe_generator = KeyframeGenerator(
                        device=device,
                        num_inference_steps=self.num_inference_steps
                    )
                
                self.keyframe_generator.generate_keyframes(story_idea)
                state['keyframes_generated'] = True
                self._save_state(state, state_file)
            else:
                print("\n✅ STEP 3: Keyframe Generation (skipped - already done)")
            
            # Step 4: Video Interpolation
            if not state.get('videos_interpolated') or not skip_existing:
                print("\n🎞️  STEP 4: Video Interpolation")
                print("-" * 60)
                self.video_interpolator.interpolate_scenes(story_idea)
                state['videos_interpolated'] = True
                self._save_state(state, state_file)
            else:
                print("\n✅ STEP 4: Video Interpolation (skipped - already done)")
            
            # Step 5: Final Composition
            print("\n🎬 STEP 5: Final Video Composition")
            print("-" * 60)
            final_video = self.video_compositor.compose_final_video(
                story_idea=story_idea,
                add_subtitles=add_subtitles,
                background_music=background_music
            )
            state['video_composed'] = True
            state['final_video_path'] = final_video
            self._save_state(state, state_file)
            
            print(f"\n{'='*60}")
            print(f"✅ PIPELINE COMPLETE!")
            print(f"📁 Final Video: {final_video}")
            print(f"{'='*60}\n")
            
            return final_video
            
        except Exception as e:
            print(f"\n❌ Pipeline failed: {e}")
            state['error'] = str(e)
            self._save_state(state, state_file)
            raise
        
        finally:
            # Cleanup GPU memory if keyframe generator was used
            if self.keyframe_generator is not None:
                self.keyframe_generator.cleanup()

    def generate_batch(
        self,
        story_ideas: list,
        skip_existing: bool = True,
        add_subtitles: bool = True
    ) -> Dict[str, str]:
        """
        Generate videos for multiple stories
        
        Args:
            story_ideas: List of StoryIdea objects
            skip_existing: Skip steps if output already exists
            add_subtitles: Whether to add subtitles overlay
            
        Returns:
            Dictionary mapping story titles to video paths
        """
        results = {}
        
        print(f"\n{'='*60}")
        print(f"🎬 BATCH VIDEO GENERATION: {len(story_ideas)} stories")
        print(f"{'='*60}\n")
        
        for i, story_idea in enumerate(story_ideas, 1):
            print(f"\n📽️  Processing {i}/{len(story_ideas)}: {story_idea.story_title}")
            
            try:
                video_path = self.generate_video(
                    story_idea=story_idea,
                    skip_existing=skip_existing,
                    add_subtitles=add_subtitles
                )
                results[story_idea.story_title] = video_path
                print(f"✅ Success: {story_idea.story_title}")
                
            except Exception as e:
                print(f"❌ Failed: {story_idea.story_title} - {e}")
                results[story_idea.story_title] = None
        
        # Summary
        successful = sum(1 for v in results.values() if v is not None)
        print(f"\n{'='*60}")
        print(f"📊 BATCH SUMMARY: {successful}/{len(story_ideas)} successful")
        print(f"{'='*60}\n")
        
        return results

    def resume_pipeline(self, story_idea: StoryIdea) -> str:
        """
        Resume pipeline from last successful step
        
        Args:
            story_idea: StoryIdea object
            
        Returns:
            Path to final video file
        """
        folder_path = os.path.join(TITLES_PATH, sanitize_filename(story_idea.story_title))
        state_file = os.path.join(folder_path, "pipeline_state.json")
        
        if not os.path.exists(state_file):
            print("⚠️ No previous state found. Starting from beginning...")
            return self.generate_video(story_idea, skip_existing=False)
        
        state = self._load_state(state_file)
        print(f"🔄 Resuming pipeline from last checkpoint...")
        print(f"   Completed steps: {', '.join([k for k, v in state.items() if v is True])}")
        
        return self.generate_video(story_idea, skip_existing=True)

    def _load_state(self, state_file: str) -> Dict[str, Any]:
        """Load pipeline state from file"""
        if os.path.exists(state_file):
            with open(state_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_state(self, state: Dict[str, Any], state_file: str):
        """Save pipeline state to file"""
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)

    def get_pipeline_status(self, story_idea: StoryIdea) -> Dict[str, Any]:
        """
        Get current pipeline status for a story
        
        Args:
            story_idea: StoryIdea object
            
        Returns:
            Dictionary with pipeline status information
        """
        folder_path = os.path.join(TITLES_PATH, sanitize_filename(story_idea.story_title))
        state_file = os.path.join(folder_path, "pipeline_state.json")
        
        if not os.path.exists(state_file):
            return {
                'status': 'not_started',
                'progress': 0,
                'completed_steps': []
            }
        
        state = self._load_state(state_file)
        
        steps = [
            'scenes_analyzed',
            'scenes_described',
            'keyframes_generated',
            'videos_interpolated',
            'video_composed'
        ]
        
        completed = [step for step in steps if state.get(step)]
        progress = (len(completed) / len(steps)) * 100
        
        return {
            'status': 'completed' if state.get('video_composed') else 'in_progress',
            'progress': progress,
            'completed_steps': completed,
            'final_video': state.get('final_video_path'),
            'error': state.get('error')
        }
