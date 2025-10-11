#!/usr/bin/env python3
"""
Video Quality Checker for StoryGenerator

Performs comprehensive quality control checks on final video output including:
- File properties validation
- Codec and format verification
- Resolution and legibility checks
- Bitrate analysis
- File size validation
- Audio-video synchronization
- Duration validation

Generates detailed QC reports with pass/fail status and quality scores.
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime


class VideoQualityChecker:
    """
    Automated video quality control system.
    
    Validates videos against quality standards and generates detailed QC reports.
    Checks include file properties, codec/format, resolution, bitrate, file size,
    A/V sync, and duration validation.
    """
    
    # Quality Standards
    TARGET_RESOLUTION = (1080, 1920)  # Width x Height (9:16 vertical)
    MIN_RESOLUTION = (720, 1280)
    
    TARGET_VIDEO_CODEC = "h264"
    TARGET_AUDIO_CODEC = "aac"
    
    TARGET_VIDEO_BITRATE = 8_000_000  # 8 Mbps
    MIN_VIDEO_BITRATE = 2_000_000     # 2 Mbps
    
    TARGET_AUDIO_BITRATE = 192_000    # 192 kbps
    MIN_AUDIO_BITRATE = 128_000       # 128 kbps
    
    TARGET_FPS = 30
    MIN_FPS = 24
    
    MIN_FILE_SIZE = 1_000_000         # 1 MB
    MAX_FILE_SIZE = 100_000_000       # 100 MB
    
    # Aliases for test compatibility
    MIN_VIDEO_SIZE_MB = 1              # 1 MB
    MAX_VIDEO_SIZE_MB = 100            # 100 MB
    MIN_BITRATE_KBPS = 2_000           # 2 Mbps
    TARGET_BITRATE_KBPS = 8_000        # 8 Mbps
    MIN_AUDIO_BITRATE_KBPS = 128       # 128 kbps
    MIN_DURATION_SECONDS = 5           # seconds
    MAX_DURATION_SECONDS = 180         # seconds
    
    MIN_DURATION = 5                   # seconds
    MAX_DURATION = 180                 # seconds
    
    MAX_SYNC_OFFSET = 0.5              # seconds
    
    # Scoring weights for overall quality
    WEIGHTS = {
        'file_properties': 0.10,
        'codec_format': 0.15,
        'resolution_legibility': 0.20,
        'bitrate_analysis': 0.20,
        'file_size': 0.15,
        'av_sync': 0.10,
        'duration': 0.10
    }
    
    def __init__(self):
        """Initialize the video quality checker."""
        self.ffprobe_cmd = self._find_ffprobe()
    
    def _find_ffprobe(self) -> str:
        """Find ffprobe executable."""
        # Try common locations
        for cmd in ['ffprobe', '/usr/bin/ffprobe', '/usr/local/bin/ffprobe']:
            try:
                result = subprocess.run(
                    [cmd, '-version'],
                    capture_output=True,
                    timeout=5
                )
                if result.returncode == 0:
                    return cmd
            except (FileNotFoundError, subprocess.TimeoutExpired):
                continue
        
        # Fallback to 'ffprobe' and let it fail later if not found
        return 'ffprobe'
    
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
            video_path: Path to the video file
            title_id: Optional title ID for the report
            save_report: Whether to save the QC report to a JSON file
            output_dir: Directory to save the report (defaults to video directory)
        
        Returns:
            Tuple of (passed: bool, report: dict)
            - passed: True if video passes all critical checks
            - report: Detailed QC report dictionary
        """
        video_path = Path(video_path)
        
        # Initialize report
        report = {
            'video_path': str(video_path),
            'title_id': title_id or video_path.stem,
            'checked_at': datetime.now().isoformat(),
            'checks': {},
            'overall_status': 'unknown',
            'quality_score': 0,
            'issues': [],
            'warnings': []
        }
        
        # Check if file exists
        if not video_path.exists():
            report['overall_status'] = 'failed'
            report['failure_reason'] = f"Video file not found: {video_path}"
            report['checks']['file_exists'] = {
                'name': 'File Existence',
                'passed': False,
                'details': {'exists': False},
                'message': 'Video file does not exist'
            }
            
            if save_report:
                self._save_report(report, video_path, output_dir)
            
            return False, report
        
        # Perform all quality checks
        try:
            # Get video metadata using ffprobe
            metadata = self._get_video_metadata(video_path)
            
            if metadata is None:
                report['overall_status'] = 'failed'
                report['failure_reason'] = 'Failed to read video metadata'
                
                if save_report:
                    self._save_report(report, video_path, output_dir)
                
                return False, report
            
            # Run individual checks
            report['checks']['file_properties'] = self._check_file_properties(video_path)
            report['checks']['codec_format'] = self._check_codec_format(metadata)
            report['checks']['resolution_legibility'] = self._check_resolution(metadata)
            report['checks']['bitrate_analysis'] = self._check_bitrate(metadata)
            report['checks']['file_size'] = self._check_file_size(video_path, metadata)
            report['checks']['av_sync'] = self._check_av_sync(metadata)
            report['checks']['duration'] = self._check_duration(metadata)
            
            # Calculate overall quality score
            quality_score = self._calculate_quality_score(report['checks'])
            report['quality_score'] = quality_score
            
            # Collect issues and warnings
            for check_name, check_data in report['checks'].items():
                if not check_data['passed']:
                    if check_data.get('severity') == 'warning':
                        report['warnings'].append(f"{check_data['name']}: {check_data['message']}")
                    else:
                        report['issues'].append(f"{check_data['name']}: {check_data['message']}")
            
            # Determine overall status
            # Pass if quality score >= 70 and no critical issues
            critical_checks = ['file_properties', 'codec_format', 'resolution_legibility']
            critical_failed = any(
                not report['checks'][check]['passed'] 
                for check in critical_checks 
                if check in report['checks']
            )
            
            passed = quality_score >= 70 and not critical_failed
            report['overall_status'] = 'passed' if passed else 'failed'
            
            # Save report if requested
            if save_report:
                report_path = self._save_report(report, video_path, output_dir)
                report['report_path'] = str(report_path)
            
            return passed, report
            
        except Exception as e:
            report['overall_status'] = 'error'
            report['failure_reason'] = f"Error during quality check: {str(e)}"
            
            if save_report:
                self._save_report(report, video_path, output_dir)
            
            return False, report
    
    def _get_video_metadata(self, video_path: Path) -> Optional[Dict]:
        """
        Extract video metadata using ffprobe.
        
        Args:
            video_path: Path to video file
        
        Returns:
            Dictionary with video metadata or None if extraction failed
        """
        try:
            cmd = [
                self.ffprobe_cmd,
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                str(video_path)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                return None
            
            metadata = json.loads(result.stdout)
            
            # Extract video and audio streams
            video_streams = [s for s in metadata.get('streams', []) if s.get('codec_type') == 'video']
            audio_streams = [s for s in metadata.get('streams', []) if s.get('codec_type') == 'audio']
            
            if not video_streams:
                return None
            
            return {
                'format': metadata.get('format', {}),
                'video_stream': video_streams[0],
                'audio_stream': audio_streams[0] if audio_streams else None
            }
            
        except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception):
            return None
    
    def _check_file_properties(self, video_path: Path) -> Dict[str, Any]:
        """Check basic file properties."""
        file_size = video_path.stat().st_size
        file_size_mb = file_size / (1024 * 1024)
        
        passed = video_path.exists() and file_size > 0
        
        return {
            'name': 'File Properties',
            'passed': passed,
            'details': {
                'file_exists': video_path.exists(),
                'size_bytes': file_size,
                'size_mb': round(file_size_mb, 2)
            },
            'message': f"File exists ({file_size_mb:.1f} MB)" if passed else "File validation failed"
        }
    
    def _check_codec_format(self, metadata: Dict) -> Dict[str, Any]:
        """Check video and audio codecs."""
        video_stream = metadata['video_stream']
        audio_stream = metadata['audio_stream']
        format_info = metadata['format']
        
        video_codec = video_stream.get('codec_name', '').lower()
        audio_codec = audio_stream.get('codec_name', '').lower() if audio_stream else 'none'
        format_name = format_info.get('format_name', '')
        
        # Check if using recommended codecs
        video_codec_ok = video_codec == self.TARGET_VIDEO_CODEC
        audio_codec_ok = audio_codec == self.TARGET_AUDIO_CODEC
        format_ok = 'mp4' in format_name.lower() or 'mov' in format_name.lower()
        
        passed = video_codec_ok and audio_codec_ok and format_ok
        
        details = {
            'format': format_name,
            'format_long': format_info.get('format_long_name', ''),
            'video_codec': video_codec,
            'audio_codec': audio_codec,
            'pixel_format': video_stream.get('pix_fmt', 'unknown')
        }
        
        if not passed:
            message = []
            if not video_codec_ok:
                message.append(f"video codec {video_codec} (expected {self.TARGET_VIDEO_CODEC})")
            if not audio_codec_ok:
                message.append(f"audio codec {audio_codec} (expected {self.TARGET_AUDIO_CODEC})")
            if not format_ok:
                message.append(f"format {format_name}")
            message_str = f"Non-standard: {', '.join(message)}"
        else:
            message_str = f"Using recommended codec: {video_codec}"
        
        return {
            'name': 'Codec & Format',
            'passed': passed,
            'details': details,
            'message': message_str,
            'severity': 'warning' if not passed else 'ok'
        }
    
    def _check_resolution(self, metadata: Dict) -> Dict[str, Any]:
        """Check video resolution and aspect ratio."""
        video_stream = metadata['video_stream']
        
        width = int(video_stream.get('width', 0))
        height = int(video_stream.get('height', 0))
        
        # Check if resolution matches target
        resolution_ok = (width, height) == self.TARGET_RESOLUTION
        
        # Check if at least minimum
        min_resolution_ok = width >= self.MIN_RESOLUTION[0] and height >= self.MIN_RESOLUTION[1]
        
        # Calculate aspect ratio
        aspect_ratio = width / height if height > 0 else 0
        target_aspect = self.TARGET_RESOLUTION[0] / self.TARGET_RESOLUTION[1]
        aspect_ok = abs(aspect_ratio - target_aspect) < 0.01
        
        passed = resolution_ok or (min_resolution_ok and aspect_ok)
        
        details = {
            'width': width,
            'height': height,
            'aspect_ratio': round(aspect_ratio, 3),
            'target_resolution': f"{self.TARGET_RESOLUTION[0]}x{self.TARGET_RESOLUTION[1]}",
            'is_vertical': height > width
        }
        
        if resolution_ok:
            message = f"Perfect: {width}x{height} (9:16 vertical)"
        elif passed:
            message = f"Acceptable: {width}x{height} (9:16 aspect ratio)"
        else:
            message = f"Resolution {width}x{height} doesn't meet requirements"
        
        return {
            'name': 'Resolution & Legibility',
            'passed': passed,
            'details': details,
            'message': message
        }
    
    def _check_bitrate(self, metadata: Dict) -> Dict[str, Any]:
        """Check video and audio bitrates."""
        video_stream = metadata['video_stream']
        audio_stream = metadata['audio_stream']
        
        video_bitrate = int(video_stream.get('bit_rate', 0))
        audio_bitrate = int(audio_stream.get('bit_rate', 0)) if audio_stream else 0
        
        # If stream doesn't have bitrate, try format-level bitrate
        if video_bitrate == 0:
            total_bitrate = int(metadata['format'].get('bit_rate', 0))
            # Estimate video bitrate (assume audio is ~10% of total)
            video_bitrate = int(total_bitrate * 0.9) if total_bitrate > 0 else 0
        
        video_bitrate_ok = video_bitrate >= self.MIN_VIDEO_BITRATE
        audio_bitrate_ok = audio_bitrate >= self.MIN_AUDIO_BITRATE or audio_bitrate == 0
        
        passed = video_bitrate_ok and audio_bitrate_ok
        
        details = {
            'video_bitrate_bps': video_bitrate,
            'video_bitrate_kbps': round(video_bitrate / 1000),
            'audio_bitrate_bps': audio_bitrate,
            'audio_bitrate_kbps': round(audio_bitrate / 1000),
            'target_video_kbps': round(self.TARGET_VIDEO_BITRATE / 1000),
            'target_audio_kbps': round(self.TARGET_AUDIO_BITRATE / 1000)
        }
        
        if passed:
            message = f"Good bitrates: Video {details['video_bitrate_kbps']} kbps, Audio {details['audio_bitrate_kbps']} kbps"
        else:
            message = f"Low bitrate: Video {details['video_bitrate_kbps']} kbps (min {self.MIN_VIDEO_BITRATE // 1000} kbps)"
        
        return {
            'name': 'Bitrate Analysis',
            'passed': passed,
            'details': details,
            'message': message,
            'severity': 'warning' if not passed else 'ok'
        }
    
    def _check_file_size(self, video_path: Path, metadata: Dict) -> Dict[str, Any]:
        """Check if file size is reasonable for duration."""
        file_size = video_path.stat().st_size
        duration = float(metadata['format'].get('duration', 0))
        
        size_mb = file_size / (1024 * 1024)
        
        # Check size limits
        size_ok = self.MIN_FILE_SIZE <= file_size <= self.MAX_FILE_SIZE
        
        # Calculate size per second (for 60s video at 8Mbps = ~60MB)
        if duration > 0:
            size_per_second = file_size / duration
            expected_size_per_second = self.TARGET_VIDEO_BITRATE / 8  # Convert bits to bytes
            size_ratio = size_per_second / expected_size_per_second if expected_size_per_second > 0 else 0
            
            # Size should be between 50% and 200% of expected
            reasonable = 0.5 <= size_ratio <= 2.0
        else:
            reasonable = True
            size_ratio = 0
        
        passed = size_ok and reasonable
        
        details = {
            'file_size_bytes': file_size,
            'file_size_mb': round(size_mb, 2),
            'duration_seconds': round(duration, 2),
            'size_per_second_mb': round(size_mb / duration, 2) if duration > 0 else 0,
            'size_ratio': round(size_ratio, 2)
        }
        
        if passed:
            message = f"Reasonable size: {size_mb:.1f} MB for {duration:.1f}s"
        elif not size_ok:
            message = f"File size {size_mb:.1f} MB outside acceptable range"
        else:
            message = f"Unusual size ratio: {size_ratio:.2f}x expected"
        
        return {
            'name': 'File Size',
            'passed': passed,
            'details': details,
            'message': message,
            'severity': 'warning' if not passed else 'ok'
        }
    
    def _check_av_sync(self, metadata: Dict) -> Dict[str, Any]:
        """
        Check audio-video synchronization.
        
        Note: This is a basic check. More sophisticated sync checking would
        require analyzing actual frame data and audio waveforms.
        """
        video_stream = metadata['video_stream']
        audio_stream = metadata['audio_stream']
        
        if not audio_stream:
            # No audio stream, so no sync issues
            return {
                'name': 'A/V Sync',
                'passed': True,
                'details': {'has_audio': False},
                'message': 'No audio stream (video only)'
            }
        
        # Check start times
        video_start = float(video_stream.get('start_time', 0))
        audio_start = float(audio_stream.get('start_time', 0))
        
        sync_offset = abs(video_start - audio_start)
        sync_ok = sync_offset <= self.MAX_SYNC_OFFSET
        
        details = {
            'has_audio': True,
            'video_start_time': round(video_start, 3),
            'audio_start_time': round(audio_start, 3),
            'sync_offset_seconds': round(sync_offset, 3),
            'max_allowed_offset': self.MAX_SYNC_OFFSET
        }
        
        if sync_ok:
            message = f"Good sync: offset {sync_offset:.3f}s"
        else:
            message = f"Sync issues: offset {sync_offset:.3f}s exceeds {self.MAX_SYNC_OFFSET}s"
        
        return {
            'name': 'A/V Sync',
            'passed': sync_ok,
            'details': details,
            'message': message
        }
    
    def _check_duration(self, metadata: Dict) -> Dict[str, Any]:
        """Check video duration."""
        duration = float(metadata['format'].get('duration', 0))
        
        duration_ok = self.MIN_DURATION <= duration <= self.MAX_DURATION
        
        details = {
            'duration_seconds': round(duration, 2),
            'duration_formatted': f"{int(duration // 60)}:{int(duration % 60):02d}",
            'min_duration': self.MIN_DURATION,
            'max_duration': self.MAX_DURATION
        }
        
        if duration_ok:
            message = f"Good duration: {duration:.1f}s"
        elif duration < self.MIN_DURATION:
            message = f"Too short: {duration:.1f}s (min {self.MIN_DURATION}s)"
        else:
            message = f"Too long: {duration:.1f}s (max {self.MAX_DURATION}s)"
        
        return {
            'name': 'Duration',
            'passed': duration_ok,
            'details': details,
            'message': message,
            'severity': 'warning' if not duration_ok else 'ok'
        }
    
    def _calculate_quality_score(self, checks: Dict[str, Dict]) -> float:
        """
        Calculate overall quality score (0-100) based on weighted checks.
        
        Args:
            checks: Dictionary of check results
        
        Returns:
            Quality score from 0 to 100
        """
        total_score = 0.0
        
        for check_name, weight in self.WEIGHTS.items():
            if check_name in checks:
                check_passed = checks[check_name]['passed']
                total_score += weight * (100 if check_passed else 0)
        
        return round(total_score, 1)
    
    def _save_report(
        self,
        report: Dict[str, Any],
        video_path: Path,
        output_dir: Optional[str] = None
    ) -> Path:
        """
        Save QC report to JSON file.
        
        Args:
            report: QC report dictionary
            video_path: Path to video file
            output_dir: Optional output directory (defaults to video directory)
        
        Returns:
            Path to saved report file
        """
        if output_dir:
            report_dir = Path(output_dir)
        else:
            report_dir = video_path.parent
        
        report_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate report filename
        title_id = report.get('title_id', video_path.stem)
        report_filename = f"{title_id}_qc.json"
        report_path = report_dir / report_filename
        
        # Save report
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report_path


def main():
    """Command-line interface for quality checking."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Check video quality and generate QC report'
    )
    parser.add_argument(
        'video_path',
        help='Path to video file or directory'
    )
    parser.add_argument(
        '--title-id',
        help='Title ID for the report'
    )
    parser.add_argument(
        '--no-save',
        dest='save_report',
        action='store_false',
        help='Do not save report to file'
    )
    parser.add_argument(
        '--output-dir',
        help='Directory to save report'
    )
    
    args = parser.parse_args()
    
    checker = VideoQualityChecker()
    
    passed, report = checker.check_video_quality(
        video_path=args.video_path,
        title_id=args.title_id,
        save_report=args.save_report,
        output_dir=args.output_dir
    )
    
    # Print summary
    print(f"\n{'='*70}")
    print(f"Quality Check: {'✅ PASSED' if passed else '❌ FAILED'}")
    print(f"Quality Score: {report['quality_score']}/100")
    print(f"{'='*70}\n")
    
    if report.get('issues'):
        print("Issues:")
        for issue in report['issues']:
            print(f"  ❌ {issue}")
        print()
    
    if report.get('warnings'):
        print("Warnings:")
        for warning in report['warnings']:
            print(f"  ⚠️  {warning}")
        print()
    
    if report.get('report_path'):
        print(f"Report saved to: {report['report_path']}\n")
    
    return 0 if passed else 1


if __name__ == '__main__':
    exit(main())
