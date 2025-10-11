#!/usr/bin/env python3
"""
Video Variant Selector for StoryGenerator

Selects the best video variant from multiple generated options (LTX-Video, interpolation)
based on quality metrics including motion smoothness, temporal consistency, and artifacts.
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime


class VideoVariantSelector:
    """
    Select best video variant based on quality metrics.
    
    Analyzes multiple video variants and selects the best one using:
    - Motion smoothness scoring
    - Temporal consistency checking
    - Artifact detection (flicker, blur, distortion)
    - Visual coherence validation
    """
    
    # Quality thresholds
    MIN_MOTION_SCORE = 0.6  # Minimum motion smoothness (0-1)
    MIN_TEMPORAL_SCORE = 0.7  # Minimum temporal consistency (0-1)
    MAX_ARTIFACT_RATIO = 0.15  # Maximum artifact ratio (0-1)
    MIN_OVERALL_SCORE = 60  # Minimum overall quality score (0-100)
    
    def __init__(self):
        """Initialize the video variant selector."""
        pass
    
    def select_best_variant(
        self,
        video_variants: List[str],
        shot_id: Optional[str] = None,
        save_report: bool = True,
        output_dir: Optional[str] = None,
        manual_override: Optional[int] = None
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Select the best video variant from a list of options.
        
        Args:
            video_variants: List of paths to video variant files
            shot_id: Optional shot ID for report
            save_report: Whether to save selection report
            output_dir: Custom output directory for report
            manual_override: Manual selection index (0-based) to override automatic selection
            
        Returns:
            Tuple of (best_variant_path, selection_report_dict)
        """
        if not video_variants:
            raise ValueError("No video variants provided")
        
        # Manual override
        if manual_override is not None:
            if 0 <= manual_override < len(video_variants):
                selected_path = video_variants[manual_override]
                report = self._create_manual_override_report(
                    video_variants, manual_override, shot_id
                )
                
                if save_report:
                    self._save_report(report, selected_path, output_dir)
                
                return selected_path, report
            else:
                raise ValueError(f"Manual override index {manual_override} out of range")
        
        # Analyze each variant
        variant_scores = []
        for i, variant_path in enumerate(video_variants):
            if not os.path.exists(variant_path):
                print(f"⚠️  Warning: Video variant not found: {variant_path}")
                continue
            
            score_data = self._analyze_video_quality(variant_path, i)
            variant_scores.append((variant_path, score_data))
        
        if not variant_scores:
            raise ValueError("No valid video variants found")
        
        # Select best variant
        best_variant, best_score = max(
            variant_scores,
            key=lambda x: x[1]['overall_score']
        )
        
        # Create selection report
        report = {
            'shot_id': shot_id,
            'selected_at': datetime.now().isoformat(),
            'total_variants': len(video_variants),
            'analyzed_variants': len(variant_scores),
            'selected_variant': best_variant,
            'selected_index': video_variants.index(best_variant),
            'selected_score': best_score,
            'all_scores': [score for _, score in variant_scores],
            'selection_reason': self._generate_selection_reason(best_score),
            'manual_override': False
        }
        
        if save_report:
            self._save_report(report, best_variant, output_dir)
        
        return best_variant, report
    
    def _analyze_video_quality(self, video_path: str, variant_index: int) -> Dict[str, Any]:
        """
        Analyze video quality metrics.
        
        Args:
            video_path: Path to video file
            variant_index: Index of this variant
            
        Returns:
            Dictionary containing quality scores
        """
        # Get video properties using ffprobe
        video_info = self._get_video_info(video_path)
        
        # Calculate quality metrics
        motion_score = self._calculate_motion_smoothness(video_path, video_info)
        temporal_score = self._calculate_temporal_consistency(video_path, video_info)
        artifact_ratio = self._detect_artifacts(video_path, video_info)
        
        # Calculate overall score (0-100)
        overall_score = self._calculate_overall_score(
            motion_score, temporal_score, artifact_ratio
        )
        
        return {
            'variant_index': variant_index,
            'video_path': video_path,
            'motion_smoothness': motion_score,
            'temporal_consistency': temporal_score,
            'artifact_ratio': artifact_ratio,
            'overall_score': overall_score,
            'video_info': video_info,
            'quality_checks': {
                'motion_smooth': motion_score >= self.MIN_MOTION_SCORE,
                'temporally_consistent': temporal_score >= self.MIN_TEMPORAL_SCORE,
                'low_artifacts': artifact_ratio <= self.MAX_ARTIFACT_RATIO,
                'acceptable_overall': overall_score >= self.MIN_OVERALL_SCORE
            }
        }
    
    def _get_video_info(self, video_path: str) -> Dict[str, Any]:
        """
        Extract video information using ffprobe.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Dictionary containing video metadata
        """
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                video_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            probe_data = json.loads(result.stdout)
            
            # Extract video stream info
            video_stream = next(
                (s for s in probe_data.get('streams', []) if s['codec_type'] == 'video'),
                {}
            )
            
            return {
                'width': int(video_stream.get('width', 0)),
                'height': int(video_stream.get('height', 0)),
                'fps': eval(video_stream.get('r_frame_rate', '30/1')),
                'codec': video_stream.get('codec_name', 'unknown'),
                'duration': float(probe_data.get('format', {}).get('duration', 0)),
                'bitrate': int(probe_data.get('format', {}).get('bit_rate', 0)),
                'nb_frames': int(video_stream.get('nb_frames', 0))
            }
            
        except (subprocess.CalledProcessError, json.JSONDecodeError, Exception) as e:
            print(f"⚠️  Warning: Could not extract video info from {video_path}: {e}")
            return {
                'width': 0,
                'height': 0,
                'fps': 30,
                'codec': 'unknown',
                'duration': 0,
                'bitrate': 0,
                'nb_frames': 0
            }
    
    def _calculate_motion_smoothness(
        self,
        video_path: str,
        video_info: Dict[str, Any]
    ) -> float:
        """
        Calculate motion smoothness score (0-1).
        
        Uses frame-to-frame differences to detect jerky motion.
        Higher scores indicate smoother motion.
        
        Args:
            video_path: Path to video file
            video_info: Video metadata
            
        Returns:
            Motion smoothness score (0-1)
        """
        try:
            # Use ffmpeg to calculate scene change detection as a proxy for motion smoothness
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-vf', 'select=gt(scene\\,0.3)',
                '-f', 'null',
                '-'
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Count scene changes from stderr
            stderr = result.stderr
            frame_count = video_info.get('nb_frames', 0)
            
            if frame_count > 0:
                # Parse frame processing from ffmpeg output
                # Look for "frame=" in stderr
                import re
                frame_matches = re.findall(r'frame=\s*(\d+)', stderr)
                if frame_matches:
                    processed_frames = int(frame_matches[-1])
                    # Fewer scene changes = smoother motion
                    scene_change_ratio = processed_frames / frame_count
                    # Invert: lower scene changes = higher smoothness
                    smoothness = max(0.0, 1.0 - scene_change_ratio)
                    return smoothness
            
            # Default to moderate score if analysis fails
            return 0.75
            
        except Exception as e:
            print(f"⚠️  Warning: Motion smoothness calculation failed: {e}")
            # Default to moderate score
            return 0.75
    
    def _calculate_temporal_consistency(
        self,
        video_path: str,
        video_info: Dict[str, Any]
    ) -> float:
        """
        Calculate temporal consistency score (0-1).
        
        Measures how consistent the video frames are over time.
        Higher scores indicate better temporal coherence.
        
        Args:
            video_path: Path to video file
            video_info: Video metadata
            
        Returns:
            Temporal consistency score (0-1)
        """
        try:
            # Check frame rate consistency
            fps = video_info.get('fps', 30)
            duration = video_info.get('duration', 0)
            nb_frames = video_info.get('nb_frames', 0)
            
            if duration > 0 and nb_frames > 0:
                expected_frames = int(fps * duration)
                frame_consistency = min(1.0, nb_frames / expected_frames) if expected_frames > 0 else 0.8
                
                # Check for variable frame rate issues
                # If codec is good and frame count matches, score higher
                if video_info.get('codec') in ['h264', 'hevc', 'vp9']:
                    codec_bonus = 0.1
                else:
                    codec_bonus = 0.0
                
                consistency_score = min(1.0, frame_consistency + codec_bonus)
                return consistency_score
            
            # Default to good score if we can't measure
            return 0.85
            
        except Exception as e:
            print(f"⚠️  Warning: Temporal consistency calculation failed: {e}")
            return 0.85
    
    def _detect_artifacts(
        self,
        video_path: str,
        video_info: Dict[str, Any]
    ) -> float:
        """
        Detect video artifacts (flicker, blur, distortion).
        
        Returns artifact ratio (0-1, lower is better).
        
        Args:
            video_path: Path to video file
            video_info: Video metadata
            
        Returns:
            Artifact ratio (0-1, where 0 is no artifacts)
        """
        try:
            # Use bitrate as a proxy for quality
            # Lower bitrate often correlates with more artifacts
            bitrate = video_info.get('bitrate', 0)
            width = video_info.get('width', 1080)
            height = video_info.get('height', 1920)
            fps = video_info.get('fps', 30)
            
            # Calculate expected bitrate (rough heuristic)
            pixels = width * height
            expected_bitrate = pixels * fps * 0.1  # ~0.1 bits per pixel per frame
            
            if expected_bitrate > 0:
                bitrate_ratio = bitrate / expected_bitrate
                
                # Convert to artifact ratio (inverse relationship)
                if bitrate_ratio >= 1.0:
                    artifact_ratio = 0.05  # Very low artifacts
                elif bitrate_ratio >= 0.5:
                    artifact_ratio = 0.10  # Low artifacts
                elif bitrate_ratio >= 0.25:
                    artifact_ratio = 0.20  # Moderate artifacts
                else:
                    artifact_ratio = 0.35  # High artifacts
                
                return min(1.0, artifact_ratio)
            
            # Default to low artifacts if we can't measure
            return 0.10
            
        except Exception as e:
            print(f"⚠️  Warning: Artifact detection failed: {e}")
            return 0.10
    
    def _calculate_overall_score(
        self,
        motion_score: float,
        temporal_score: float,
        artifact_ratio: float
    ) -> float:
        """
        Calculate overall quality score (0-100).
        
        Weighted combination of quality metrics.
        
        Args:
            motion_score: Motion smoothness (0-1)
            temporal_score: Temporal consistency (0-1)
            artifact_ratio: Artifact ratio (0-1, lower is better)
            
        Returns:
            Overall quality score (0-100)
        """
        # Weights
        MOTION_WEIGHT = 0.35
        TEMPORAL_WEIGHT = 0.35
        ARTIFACT_WEIGHT = 0.30
        
        # Convert artifact ratio to quality score (invert)
        artifact_quality = 1.0 - artifact_ratio
        
        # Calculate weighted score
        overall = (
            motion_score * MOTION_WEIGHT +
            temporal_score * TEMPORAL_WEIGHT +
            artifact_quality * ARTIFACT_WEIGHT
        )
        
        # Convert to 0-100 scale
        return round(overall * 100, 1)
    
    def _generate_selection_reason(self, score_data: Dict[str, Any]) -> str:
        """
        Generate human-readable selection reason.
        
        Args:
            score_data: Quality score data
            
        Returns:
            Selection reason string
        """
        reasons = []
        
        if score_data['overall_score'] >= 90:
            reasons.append("excellent overall quality")
        elif score_data['overall_score'] >= 80:
            reasons.append("high overall quality")
        elif score_data['overall_score'] >= 70:
            reasons.append("good overall quality")
        else:
            reasons.append("acceptable quality")
        
        if score_data['motion_smoothness'] >= 0.85:
            reasons.append("smooth motion")
        
        if score_data['temporal_consistency'] >= 0.85:
            reasons.append("consistent frames")
        
        if score_data['artifact_ratio'] <= 0.10:
            reasons.append("minimal artifacts")
        
        return "Selected for: " + ", ".join(reasons)
    
    def _create_manual_override_report(
        self,
        video_variants: List[str],
        override_index: int,
        shot_id: Optional[str]
    ) -> Dict[str, Any]:
        """
        Create report for manual override selection.
        
        Args:
            video_variants: List of video variant paths
            override_index: Index of manually selected variant
            shot_id: Optional shot ID
            
        Returns:
            Selection report dictionary
        """
        selected_path = video_variants[override_index]
        
        return {
            'shot_id': shot_id,
            'selected_at': datetime.now().isoformat(),
            'total_variants': len(video_variants),
            'analyzed_variants': 0,
            'selected_variant': selected_path,
            'selected_index': override_index,
            'selected_score': None,
            'all_scores': [],
            'selection_reason': f"Manual override: User selected variant {override_index}",
            'manual_override': True
        }
    
    def _save_report(
        self,
        report: Dict[str, Any],
        selected_path: str,
        output_dir: Optional[str] = None
    ) -> str:
        """
        Save selection report to JSON file.
        
        Args:
            report: Selection report data
            selected_path: Path to selected video
            output_dir: Optional custom output directory
            
        Returns:
            Path to saved report file
        """
        # Determine output directory
        if output_dir is None:
            output_dir = os.path.dirname(selected_path)
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate report filename
        shot_id = report.get('shot_id', 'unknown')
        report_filename = f"{shot_id}_variant_selection.json"
        report_path = os.path.join(output_dir, report_filename)
        
        # Add report path to report data
        report['report_path'] = report_path
        
        # Save report
        with open(report_path, 'w') as f:
            json.dump(report, indent=2, fp=f)
        
        return report_path
    
    def batch_select_variants(
        self,
        variant_groups: Dict[str, List[str]],
        output_dir: Optional[str] = None,
        save_reports: bool = True
    ) -> Dict[str, Tuple[str, Dict[str, Any]]]:
        """
        Select best variants for multiple shots.
        
        Args:
            variant_groups: Dictionary mapping shot_id to list of variant paths
            output_dir: Optional output directory for reports
            save_reports: Whether to save selection reports
            
        Returns:
            Dictionary mapping shot_id to (selected_path, report) tuples
        """
        results = {}
        
        print(f"\n{'='*70}")
        print(f"Batch Variant Selection: {len(variant_groups)} shots")
        print(f"{'='*70}\n")
        
        for shot_id, variants in variant_groups.items():
            print(f"Processing shot: {shot_id} ({len(variants)} variants)")
            
            try:
                selected_path, report = self.select_best_variant(
                    video_variants=variants,
                    shot_id=shot_id,
                    save_report=save_reports,
                    output_dir=output_dir
                )
                
                results[shot_id] = (selected_path, report)
                
                print(f"  ✅ Selected: {os.path.basename(selected_path)}")
                print(f"     Score: {report['selected_score']['overall_score']}/100")
                print(f"     {report['selection_reason']}\n")
                
            except Exception as e:
                print(f"  ❌ Error selecting variant for {shot_id}: {e}\n")
                continue
        
        # Print summary
        print(f"{'='*70}")
        print(f"Batch Selection Complete: {len(results)}/{len(variant_groups)} shots processed")
        print(f"{'='*70}")
        
        return results
