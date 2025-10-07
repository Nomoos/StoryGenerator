"""
GVideoClipGenerator - Video Clip Generation for Shots

This generator creates video clips from shots using either:
- Variant A: LTX-Video (AI-based image-to-video)
- Variant B: Frame Interpolation (RIFE/DAIN/FILM)

Output structure: /videos/{ltx|interp}/{segment}/{age}/{title_id}/shot_{k}.mp4

The implementation uses the research prototypes from src/research/python/
and provides a clean interface following the Generator (G*) naming convention.
"""

import os
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Optional

# Add research path for importing prototypes
RESEARCH_PATH = Path(__file__).parent.parent.parent / "research" / "python"
if str(RESEARCH_PATH) not in sys.path:
    sys.path.insert(0, str(RESEARCH_PATH))

try:
    from ltx_generate import LTXVideoGenerator
    from interpolation import VideoInterpolator
    LTX_AVAILABLE = True
except ImportError:
    LTX_AVAILABLE = False
    print("⚠️  Warning: LTX/Interpolation modules not available from research directory")


class GVideoClipGenerator:
    """
    Generator for creating video clips from shots.
    
    Supports two variants:
    - LTX-Video: AI-based image-to-video generation (10-20s clips)
    - Frame Interpolation: Smooth transitions between keyframes
    
    Usage:
        generator = GVideoClipGenerator(use_ltx=True)
        clips = generator.generate_clips_for_story(
            shots=shots,
            segment="tech",
            age="18-23", 
            title_id="my_story"
        )
    """
    
    def __init__(
        self,
        config_path: Optional[str] = None,
        use_ltx: Optional[bool] = None,
        fps: int = 30,
        device: str = "auto"
    ):
        """
        Initialize video clip generator.
        
        Args:
            config_path: Path to pipeline.yaml config
            use_ltx: Override to use LTX (True) or interpolation (False)
            fps: Target frames per second
            device: Device ("cpu", "cuda", "auto")
        """
        self.fps = fps
        self.device = device
        
        # Load config
        self.config = self._load_config(config_path)
        
        # Determine variant
        if use_ltx is not None:
            self.use_ltx = use_ltx
        else:
            self.use_ltx = self.config.get("switches", {}).get("use_ltx", True)
        
        # Lazy loading
        self.ltx_generator = None
        self.interpolator = None
        
        if not LTX_AVAILABLE:
            print("⚠️  LTX/Interpolation not available - will use fallback methods")
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load pipeline configuration."""
        if config_path is None:
            # Try default paths
            base = Path(__file__).parent.parent.parent.parent
            default_paths = [
                base / "data" / "config" / "pipeline.yaml",
                "data/config/pipeline.yaml",
                "pipeline.yaml"
            ]
            for path in default_paths:
                if Path(path).exists():
                    config_path = str(path)
                    break
        
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def _get_ltx_generator(self):
        """Get or create LTX generator (lazy loading)."""
        if not LTX_AVAILABLE:
            raise RuntimeError("LTX generator not available")
        
        if self.ltx_generator is None:
            model_id = self.config.get("models", {}).get(
                "video", "stabilityai/stable-video-diffusion-img2vid"
            )
            self.ltx_generator = LTXVideoGenerator(
                model_id=model_id,
                device=self.device,
                fps=self.fps
            )
        return self.ltx_generator
    
    def _get_interpolator(self):
        """Get or create interpolator (lazy loading)."""
        if not LTX_AVAILABLE:
            raise RuntimeError("Interpolator not available")
        
        if self.interpolator is None:
            self.interpolator = VideoInterpolator(
                method="rife",
                device=self.device
            )
        return self.interpolator
    
    def generate_shot_clip(
        self,
        shot: Dict,
        output_path: str,
        duration: float = 10.0,
        seed: Optional[int] = None
    ) -> str:
        """
        Generate video clip for a single shot.
        
        Args:
            shot: Shot description with image_path or keyframes
            output_path: Output video path
            duration: Duration in seconds (10-20s for LTX)
            seed: Random seed
            
        Returns:
            Path to generated video
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if "duration" in shot:
            duration = shot["duration"]
        
        if self.use_ltx:
            return self._generate_ltx_clip(shot, output_path, duration, seed)
        else:
            return self._generate_interpolated_clip(shot, output_path, duration, seed)
    
    def _generate_ltx_clip(self, shot: Dict, output_path: str, duration: float, seed: Optional[int]) -> str:
        """Generate using LTX-Video (Variant A)."""
        generator = self._get_ltx_generator()
        
        shot_desc = {
            "image_path": shot.get("image_path", shot.get("keyframes", [None])[0]),
            "motion": shot.get("motion", "subtle movement"),
            "intensity": shot.get("intensity", 0.5),
            "duration": duration
        }
        
        return generator.shot_to_clip(
            shot_description=shot_desc,
            output_path=output_path,
            duration=duration,
            seed=seed
        )
    
    def _generate_interpolated_clip(self, shot: Dict, output_path: str, duration: float, seed: Optional[int]) -> str:
        """Generate using frame interpolation (Variant B)."""
        interpolator = self._get_interpolator()
        
        keyframes = shot.get("keyframes", [shot.get("image_path")])
        if len(keyframes) < 2:
            raise ValueError(f"Interpolation requires 2+ keyframes, got {len(keyframes)}")
        
        # Create temp video from keyframes, then interpolate
        temp_video = self._create_keyframe_video(keyframes, duration)
        
        try:
            result = interpolator.interpolate_video(
                input_path=temp_video,
                output_path=output_path,
                target_fps=self.fps
            )
            if os.path.exists(temp_video):
                os.remove(temp_video)
            return result
        except Exception as e:
            # Fallback to basic keyframe video
            if os.path.exists(temp_video):
                os.rename(temp_video, output_path)
            return output_path
    
    def _create_keyframe_video(self, keyframes: List[str], duration: float) -> str:
        """Create basic video from keyframes using FFmpeg."""
        import subprocess
        import tempfile
        
        temp_video = tempfile.mktemp(suffix=".mp4")
        duration_per_frame = duration / len(keyframes)
        
        concat_file = tempfile.mktemp(suffix=".txt")
        with open(concat_file, 'w') as f:
            for keyframe in keyframes:
                f.write(f"file '{os.path.abspath(keyframe)}'\n")
                f.write(f"duration {duration_per_frame}\n")
            f.write(f"file '{os.path.abspath(keyframes[-1])}'\n")
        
        cmd = [
            "ffmpeg", "-f", "concat", "-safe", "0",
            "-i", concat_file,
            "-vf", f"fps={self.fps},scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
            "-c:v", "libx264", "-preset", "medium", "-crf", "23",
            "-y", temp_video
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        finally:
            if os.path.exists(concat_file):
                os.remove(concat_file)
        
        return temp_video
    
    def generate_clips_for_story(
        self,
        shots: List[Dict],
        segment: str,
        age: str,
        title_id: str,
        base_output_dir: str = "videos",
        base_seed: Optional[int] = None
    ) -> List[str]:
        """
        Generate video clips for all shots in a story.
        
        Args:
            shots: List of shot dictionaries
            segment: Content segment (tech, lifestyle, etc.)
            age: Age group (18-23, 24-30, etc.)
            title_id: Unique story identifier
            base_output_dir: Base output directory
            base_seed: Base random seed
            
        Returns:
            List of paths to generated clips
        """
        variant_dir = "ltx" if self.use_ltx else "interp"
        output_dir = os.path.join(
            base_output_dir,
            variant_dir,
            segment,
            age,
            title_id
        )
        
        os.makedirs(output_dir, exist_ok=True)
        
        if base_seed is None:
            base_seed = self.config.get("seeds", {}).get("video", 5678)
        
        clip_paths = []
        
        for i, shot in enumerate(shots):
            output_path = os.path.join(output_dir, f"shot_{i}.mp4")
            seed = base_seed + i
            
            try:
                clip_path = self.generate_shot_clip(
                    shot=shot,
                    output_path=output_path,
                    duration=shot.get("duration", 10.0),
                    seed=seed
                )
                clip_paths.append(clip_path)
            except Exception as e:
                print(f"❌ Failed to generate shot_{i}: {e}")
                clip_paths.append(None)
        
        return clip_paths
    
    def cleanup(self):
        """Free resources and GPU memory."""
        if self.ltx_generator is not None:
            self.ltx_generator.unload_model()


# Example usage
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate video clips for shots"
    )
    parser.add_argument("--shots", required=True, help="Shots YAML file")
    parser.add_argument("--segment", required=True, help="Content segment")
    parser.add_argument("--age", required=True, help="Age group")
    parser.add_argument("--title-id", required=True, help="Title ID")
    parser.add_argument("--use-ltx", action="store_true", help="Use LTX-Video")
    parser.add_argument("--use-interpolation", action="store_true", help="Use interpolation")
    
    args = parser.parse_args()
    
    # Load shots
    with open(args.shots, 'r') as f:
        shots_data = yaml.safe_load(f)
    shots = shots_data if isinstance(shots_data, list) else shots_data.get("shots", [])
    
    # Determine variant
    use_ltx = None
    if args.use_ltx:
        use_ltx = True
    elif args.use_interpolation:
        use_ltx = False
    
    # Generate
    generator = GVideoClipGenerator(use_ltx=use_ltx)
    clips = generator.generate_clips_for_story(
        shots=shots,
        segment=args.segment,
        age=args.age,
        title_id=args.title_id
    )
    
    print(f"\n✅ Generated {sum(1 for c in clips if c)} / {len(clips)} clips")
    generator.cleanup()
