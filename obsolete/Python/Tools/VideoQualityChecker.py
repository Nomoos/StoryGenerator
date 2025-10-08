"""
Video Quality Checker for StoryGenerator

Performs comprehensive quality checks on final videos including:
- Codec and format validation
- Bitrate and file size analysis
- Audio/video sync verification
- Resolution and legibility checks
- Overall quality scoring

Saves QC reports to /final/{segment}/{age}/{title_id}_qc.json
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from pathlib import Path

from Tools.Monitor import logger, log_info, log_warning


class VideoQualityChecker:
    """Perform quality checks on final videos and generate QC reports."""
    
    # Quality thresholds
    MIN_VIDEO_SIZE_MB = 1.0  # Minimum size for 60s video
    MAX_VIDEO_SIZE_MB = 100.0  # Maximum size for 60s video
    TARGET_RESOLUTION = (1080, 1920)  # Target resolution for vertical video
    MIN_BITRATE_KBPS = 2000  # Minimum video bitrate
    TARGET_BITRATE_KBPS = 8000  # Target video bitrate
    MIN_AUDIO_BITRATE_KBPS = 128  # Minimum audio bitrate
    TARGET_AUDIO_BITRATE_KBPS = 192  # Target audio bitrate
    MIN_DURATION_SECONDS = 5  # Minimum video duration
    MAX_DURATION_SECONDS = 180  # Maximum video duration (3 minutes)
    
    def __init__(self):
        """Initialize video quality checker."""
        pass
    
    def check_video_quality(
        self,
        video_path: str,
        title_id: Optional[str] = None,
        save_report: bool = True,
        output_dir: Optional[str] = None
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Perform comprehensive quality check on a video file.
        
        Args:
            video_path: Path to the video file to check
            title_id: Optional title ID for the report filename
            save_report: Whether to save the QC report to JSON
            output_dir: Directory to save the report (defaults to /final structure)
            
        Returns:
            Tuple of (passed, qc_report_dict)
        """
        log_info(f"🔍 Performing quality check on: {video_path}")
        
        qc_report = {
            "video_path": video_path,
            "title_id": title_id or self._extract_title_id(video_path),
            "checked_at": datetime.now().isoformat(),
            "checks": {},
            "overall_status": "pending"
        }
        
        # Perform all quality checks
        checks_passed = []
        
        # 1. File existence and basic properties
        file_check = self._check_file_properties(video_path)
        qc_report["checks"]["file_properties"] = file_check
        checks_passed.append(file_check["passed"])
        
        if not file_check["passed"]:
            qc_report["overall_status"] = "failed"
            qc_report["failure_reason"] = "File does not exist or is invalid"
            qc_report["checks_passed"] = 0
            qc_report["checks_total"] = 1
            qc_report["pass_rate"] = 0.0
            qc_report["quality_score"] = 0
            return False, qc_report
        
        # 2. Codec and format validation
        codec_check = self._check_codec_format(video_path)
        qc_report["checks"]["codec_format"] = codec_check
        checks_passed.append(codec_check["passed"])
        
        # 3. Resolution and legibility
        resolution_check = self._check_resolution_legibility(video_path)
        qc_report["checks"]["resolution_legibility"] = resolution_check
        checks_passed.append(resolution_check["passed"])
        
        # 4. Bitrate analysis
        bitrate_check = self._check_bitrate(video_path)
        qc_report["checks"]["bitrate"] = bitrate_check
        checks_passed.append(bitrate_check["passed"])
        
        # 5. File size validation
        file_size_check = self._check_file_size(video_path)
        qc_report["checks"]["file_size"] = file_size_check
        checks_passed.append(file_size_check["passed"])
        
        # 6. Audio/video sync verification
        sync_check = self._check_av_sync(video_path)
        qc_report["checks"]["av_sync"] = sync_check
        checks_passed.append(sync_check["passed"])
        
        # 7. Duration validation
        duration_check = self._check_duration(video_path)
        qc_report["checks"]["duration"] = duration_check
        checks_passed.append(duration_check["passed"])
        
        # Determine overall status
        all_passed = all(checks_passed)
        qc_report["overall_status"] = "passed" if all_passed else "failed"
        qc_report["checks_passed"] = sum(checks_passed)
        qc_report["checks_total"] = len(checks_passed)
        qc_report["pass_rate"] = round(sum(checks_passed) / len(checks_passed) * 100, 1)
        
        # Generate quality score (0-100)
        qc_report["quality_score"] = self._calculate_quality_score(qc_report["checks"])
        
        # Save report if requested
        if save_report:
            report_path = self._save_qc_report(qc_report, output_dir)
            qc_report["report_path"] = report_path
            log_info(f"📄 QC report saved to: {report_path}")
        
        # Log summary
        status_emoji = "✅" if all_passed else "⚠️"
        log_info(
            f"{status_emoji} Quality check {qc_report['overall_status']}: "
            f"{qc_report['checks_passed']}/{qc_report['checks_total']} checks passed "
            f"(Score: {qc_report['quality_score']}/100)"
        )
        
        return all_passed, qc_report
    
    def _check_file_properties(self, video_path: str) -> Dict[str, Any]:
        """Check basic file properties."""
        check = {
            "name": "File Properties",
            "passed": False,
            "details": {}
        }
        
        try:
            if not os.path.exists(video_path):
                check["details"]["error"] = "File does not exist"
                check["message"] = "Video file not found"
                return check
            
            file_size = os.path.getsize(video_path)
            check["details"]["file_exists"] = True
            check["details"]["size_bytes"] = file_size
            check["details"]["size_mb"] = round(file_size / (1024 * 1024), 2)
            
            if file_size > 0:
                check["passed"] = True
                check["message"] = f"File exists ({check['details']['size_mb']} MB)"
            else:
                check["message"] = "File is empty"
                
        except Exception as e:
            check["details"]["error"] = str(e)
            check["message"] = f"Error checking file: {str(e)}"
            logger.error(f"Error checking file properties: {e}")
        
        return check
    
    def _check_codec_format(self, video_path: str) -> Dict[str, Any]:
        """Check video codec and format."""
        check = {
            "name": "Codec & Format",
            "passed": False,
            "details": {}
        }
        
        try:
            import ffmpeg
            probe = ffmpeg.probe(video_path)
            
            # Get format info
            format_info = probe.get('format', {})
            check["details"]["format"] = format_info.get('format_name', 'unknown')
            check["details"]["format_long"] = format_info.get('format_long_name', 'unknown')
            
            # Get video codec
            video_stream = next(
                (s for s in probe['streams'] if s['codec_type'] == 'video'),
                None
            )
            
            if video_stream:
                video_codec = video_stream.get('codec_name', 'unknown')
                check["details"]["video_codec"] = video_codec
                check["details"]["pixel_format"] = video_stream.get('pix_fmt', 'unknown')
                
                # Check for recommended codec (h264)
                if video_codec in ['h264', 'libx264']:
                    check["passed"] = True
                    check["message"] = f"Using recommended codec: {video_codec}"
                else:
                    check["message"] = f"Non-standard codec: {video_codec} (expected h264)"
            else:
                check["message"] = "No video stream found"
            
            # Get audio codec
            audio_stream = next(
                (s for s in probe['streams'] if s['codec_type'] == 'audio'),
                None
            )
            
            if audio_stream:
                audio_codec = audio_stream.get('codec_name', 'unknown')
                check["details"]["audio_codec"] = audio_codec
                
                # Prefer AAC for audio
                if audio_codec not in ['aac', 'mp3']:
                    check["details"]["audio_codec_warning"] = f"Non-standard audio codec: {audio_codec}"
                    
        except Exception as e:
            check["details"]["error"] = str(e)
            check["message"] = f"Error checking codec: {str(e)}"
            logger.error(f"Error checking codec format: {e}")
        
        return check
    
    def _check_resolution_legibility(self, video_path: str) -> Dict[str, Any]:
        """Check video resolution and legibility."""
        check = {
            "name": "Resolution & Legibility",
            "passed": False,
            "details": {}
        }
        
        try:
            import ffmpeg
            probe = ffmpeg.probe(video_path)
            
            video_stream = next(
                (s for s in probe['streams'] if s['codec_type'] == 'video'),
                None
            )
            
            if video_stream:
                width = int(video_stream.get('width', 0))
                height = int(video_stream.get('height', 0))
                
                check["details"]["width"] = width
                check["details"]["height"] = height
                check["details"]["resolution"] = f"{width}x{height}"
                check["details"]["aspect_ratio"] = round(width / height if height > 0 else 0, 2)
                
                # Check if resolution matches target (1080x1920 for vertical video)
                target_width, target_height = self.TARGET_RESOLUTION
                if width == target_width and height == target_height:
                    check["passed"] = True
                    check["message"] = f"Perfect resolution: {width}x{height}"
                elif width >= 720 and height >= 1280:
                    # Acceptable HD resolution for vertical video
                    check["passed"] = True
                    check["message"] = f"Acceptable resolution: {width}x{height}"
                else:
                    check["message"] = f"Low resolution: {width}x{height} (expected {target_width}x{target_height})"
                
                # Check frame rate
                fps_str = video_stream.get('r_frame_rate', '0/1')
                if '/' in fps_str:
                    num, den = map(int, fps_str.split('/'))
                    fps = num / den if den > 0 else 0
                    check["details"]["fps"] = round(fps, 2)
                    
                    if fps >= 24:
                        check["details"]["fps_status"] = "good"
                    else:
                        check["details"]["fps_status"] = "low"
                        check["details"]["fps_warning"] = f"Low frame rate: {fps} fps"
            else:
                check["message"] = "No video stream found"
                
        except Exception as e:
            check["details"]["error"] = str(e)
            check["message"] = f"Error checking resolution: {str(e)}"
            logger.error(f"Error checking resolution: {e}")
        
        return check
    
    def _check_bitrate(self, video_path: str) -> Dict[str, Any]:
        """Check video and audio bitrate."""
        check = {
            "name": "Bitrate Analysis",
            "passed": False,
            "details": {}
        }
        
        try:
            import ffmpeg
            probe = ffmpeg.probe(video_path)
            
            # Overall bitrate
            format_info = probe.get('format', {})
            overall_bitrate = int(format_info.get('bit_rate', 0))
            check["details"]["overall_bitrate_bps"] = overall_bitrate
            check["details"]["overall_bitrate_kbps"] = round(overall_bitrate / 1000, 2)
            
            # Video stream bitrate
            video_stream = next(
                (s for s in probe['streams'] if s['codec_type'] == 'video'),
                None
            )
            
            if video_stream:
                video_bitrate = int(video_stream.get('bit_rate', 0))
                check["details"]["video_bitrate_bps"] = video_bitrate
                check["details"]["video_bitrate_kbps"] = round(video_bitrate / 1000, 2)
                
                # Validate video bitrate
                video_bitrate_kbps = video_bitrate / 1000
                if video_bitrate_kbps >= self.MIN_BITRATE_KBPS:
                    check["passed"] = True
                    check["message"] = f"Good video bitrate: {round(video_bitrate_kbps, 2)} kbps"
                else:
                    check["message"] = f"Low video bitrate: {round(video_bitrate_kbps, 2)} kbps (min: {self.MIN_BITRATE_KBPS} kbps)"
            
            # Audio stream bitrate
            audio_stream = next(
                (s for s in probe['streams'] if s['codec_type'] == 'audio'),
                None
            )
            
            if audio_stream:
                audio_bitrate = int(audio_stream.get('bit_rate', 0))
                check["details"]["audio_bitrate_bps"] = audio_bitrate
                check["details"]["audio_bitrate_kbps"] = round(audio_bitrate / 1000, 2)
                
                # Validate audio bitrate
                audio_bitrate_kbps = audio_bitrate / 1000
                if audio_bitrate_kbps < self.MIN_AUDIO_BITRATE_KBPS:
                    check["details"]["audio_bitrate_warning"] = f"Low audio bitrate: {round(audio_bitrate_kbps, 2)} kbps"
                    
        except Exception as e:
            check["details"]["error"] = str(e)
            check["message"] = f"Error checking bitrate: {str(e)}"
            logger.error(f"Error checking bitrate: {e}")
        
        return check
    
    def _check_file_size(self, video_path: str) -> Dict[str, Any]:
        """Check if file size is within acceptable range."""
        check = {
            "name": "File Size",
            "passed": False,
            "details": {}
        }
        
        try:
            file_size = os.path.getsize(video_path)
            size_mb = file_size / (1024 * 1024)
            
            check["details"]["size_bytes"] = file_size
            check["details"]["size_mb"] = round(size_mb, 2)
            check["details"]["min_size_mb"] = self.MIN_VIDEO_SIZE_MB
            check["details"]["max_size_mb"] = self.MAX_VIDEO_SIZE_MB
            
            if self.MIN_VIDEO_SIZE_MB <= size_mb <= self.MAX_VIDEO_SIZE_MB:
                check["passed"] = True
                check["message"] = f"File size acceptable: {round(size_mb, 2)} MB"
            elif size_mb < self.MIN_VIDEO_SIZE_MB:
                check["message"] = f"File too small: {round(size_mb, 2)} MB (min: {self.MIN_VIDEO_SIZE_MB} MB)"
            else:
                check["message"] = f"File too large: {round(size_mb, 2)} MB (max: {self.MAX_VIDEO_SIZE_MB} MB)"
                
        except Exception as e:
            check["details"]["error"] = str(e)
            check["message"] = f"Error checking file size: {str(e)}"
            logger.error(f"Error checking file size: {e}")
        
        return check
    
    def _check_av_sync(self, video_path: str) -> Dict[str, Any]:
        """Check audio/video synchronization."""
        check = {
            "name": "Audio/Video Sync",
            "passed": False,
            "details": {}
        }
        
        try:
            import ffmpeg
            probe = ffmpeg.probe(video_path)
            
            # Get video duration
            video_stream = next(
                (s for s in probe['streams'] if s['codec_type'] == 'video'),
                None
            )
            
            # Get audio duration
            audio_stream = next(
                (s for s in probe['streams'] if s['codec_type'] == 'audio'),
                None
            )
            
            if video_stream and audio_stream:
                # Get durations
                format_duration = float(probe['format'].get('duration', 0))
                video_duration = float(video_stream.get('duration', format_duration))
                audio_duration = float(audio_stream.get('duration', format_duration))
                
                check["details"]["video_duration"] = round(video_duration, 2)
                check["details"]["audio_duration"] = round(audio_duration, 2)
                check["details"]["format_duration"] = round(format_duration, 2)
                
                # Check sync (allow up to 0.5 second difference)
                sync_diff = abs(video_duration - audio_duration)
                check["details"]["sync_difference"] = round(sync_diff, 3)
                
                if sync_diff <= 0.5:
                    check["passed"] = True
                    check["message"] = f"Audio/video in sync (diff: {round(sync_diff, 3)}s)"
                else:
                    check["message"] = f"Audio/video out of sync (diff: {round(sync_diff, 3)}s)"
            elif not audio_stream:
                check["message"] = "No audio stream found"
            elif not video_stream:
                check["message"] = "No video stream found"
            else:
                check["message"] = "Could not verify sync"
                
        except Exception as e:
            check["details"]["error"] = str(e)
            check["message"] = f"Error checking sync: {str(e)}"
            logger.error(f"Error checking AV sync: {e}")
        
        return check
    
    def _check_duration(self, video_path: str) -> Dict[str, Any]:
        """Check video duration."""
        check = {
            "name": "Duration",
            "passed": False,
            "details": {}
        }
        
        try:
            import ffmpeg
            probe = ffmpeg.probe(video_path)
            
            duration = float(probe['format'].get('duration', 0))
            check["details"]["duration_seconds"] = round(duration, 2)
            check["details"]["duration_formatted"] = self._format_duration(duration)
            check["details"]["min_duration"] = self.MIN_DURATION_SECONDS
            check["details"]["max_duration"] = self.MAX_DURATION_SECONDS
            
            if self.MIN_DURATION_SECONDS <= duration <= self.MAX_DURATION_SECONDS:
                check["passed"] = True
                check["message"] = f"Duration acceptable: {round(duration, 2)}s"
            elif duration < self.MIN_DURATION_SECONDS:
                check["message"] = f"Duration too short: {round(duration, 2)}s (min: {self.MIN_DURATION_SECONDS}s)"
            else:
                check["message"] = f"Duration too long: {round(duration, 2)}s (max: {self.MAX_DURATION_SECONDS}s)"
                
        except Exception as e:
            check["details"]["error"] = str(e)
            check["message"] = f"Error checking duration: {str(e)}"
            logger.error(f"Error checking duration: {e}")
        
        return check
    
    def _calculate_quality_score(self, checks: Dict[str, Dict]) -> int:
        """Calculate overall quality score (0-100) based on all checks."""
        scores = []
        weights = {
            "file_properties": 10,
            "codec_format": 15,
            "resolution_legibility": 20,
            "bitrate": 20,
            "file_size": 15,
            "av_sync": 10,
            "duration": 10
        }
        
        for check_name, check_data in checks.items():
            weight = weights.get(check_name, 10)
            if check_data.get("passed", False):
                scores.append(weight)
            else:
                # Partial credit based on severity
                if "error" not in check_data.get("details", {}):
                    scores.append(weight * 0.5)  # 50% credit for non-critical fails
                else:
                    scores.append(0)  # No credit for errors
        
        total_weight = sum(weights.values())
        total_score = sum(scores)
        
        return round((total_score / total_weight) * 100)
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration in human-readable format."""
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        ms = int((seconds % 1) * 1000)
        
        if mins > 0:
            return f"{mins}m {secs}s"
        else:
            return f"{secs}.{ms:03d}s"
    
    def _extract_title_id(self, video_path: str) -> str:
        """Extract title ID from video path."""
        # Try to extract from filename
        filename = os.path.basename(video_path)
        # Remove extension
        name_without_ext = os.path.splitext(filename)[0]
        # Remove common suffixes
        title_id = name_without_ext.replace('final_video', '').replace('_', '').strip()
        
        if not title_id:
            # Use parent directory name
            title_id = os.path.basename(os.path.dirname(video_path))
        
        return title_id or "unknown"
    
    def _save_qc_report(self, qc_report: Dict[str, Any], output_dir: Optional[str] = None) -> str:
        """Save QC report to JSON file."""
        try:
            # Determine output directory
            if output_dir:
                report_dir = output_dir
            else:
                # Try to determine from video path
                video_path = qc_report.get("video_path", "")
                if video_path:
                    # Use the same directory as the video
                    report_dir = os.path.dirname(video_path)
                else:
                    # Fallback to temp directory
                    report_dir = "/tmp"
            
            # Ensure directory exists
            os.makedirs(report_dir, exist_ok=True)
            
            # Generate report filename
            title_id = qc_report.get("title_id", "unknown")
            report_filename = f"{title_id}_qc.json"
            report_path = os.path.join(report_dir, report_filename)
            
            # Save report
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(qc_report, f, indent=2, ensure_ascii=False)
            
            log_info(f"QC report saved: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error(f"Error saving QC report: {e}")
            return ""
