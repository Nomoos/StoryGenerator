"""
Output quality validation and metrics tracking.
Validates generated files and tracks quality metrics.
"""

import os
from typing import Dict, Any, Optional, Tuple
from Tools.Monitor import logger, log_info, log_warning


class OutputValidator:
    """Validate output files and track quality metrics."""
    
    @staticmethod
    def validate_audio_file(file_path: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Validate an audio file and return metrics.
        
        Returns:
            Tuple of (is_valid, metrics_dict)
        """
        metrics = {
            "exists": False,
            "size_bytes": 0,
            "size_mb": 0.0,
            "is_valid": False
        }
        
        if not os.path.exists(file_path):
            log_warning(f"Audio file does not exist: {file_path}")
            return False, metrics
        
        metrics["exists"] = True
        
        try:
            size_bytes = os.path.getsize(file_path)
            metrics["size_bytes"] = size_bytes
            metrics["size_mb"] = round(size_bytes / (1024 * 1024), 2)
            
            # Basic validation: file should be at least 10KB
            if size_bytes < 10240:
                log_warning(f"Audio file too small ({size_bytes} bytes): {file_path}")
                return False, metrics
            
            # Try to get duration using ffmpeg
            try:
                import ffmpeg
                probe = ffmpeg.probe(file_path)
                duration = float(probe['format']['duration'])
                metrics["duration_seconds"] = round(duration, 2)
                
                # Validate duration (should be at least 5 seconds for a story)
                if duration < 5.0:
                    log_warning(f"Audio too short ({duration}s): {file_path}")
                    return False, metrics
                
                # Check bitrate
                bitrate = int(probe['format'].get('bit_rate', 0))
                metrics["bitrate"] = bitrate
                
                # Audio should have reasonable bitrate (at least 32kbps)
                if bitrate < 32000:
                    log_warning(f"Audio bitrate too low ({bitrate}): {file_path}")
                    return False, metrics
                
            except Exception as e:
                log_warning(f"Could not probe audio file: {e}")
                # Don't fail validation if probe fails, file might still be valid
            
            metrics["is_valid"] = True
            log_info(f"✅ Audio file validated: {file_path} ({metrics['size_mb']}MB)")
            return True, metrics
            
        except Exception as e:
            logger.error(f"Error validating audio file: {e}")
            return False, metrics
    
    @staticmethod
    def validate_text_file(file_path: str, min_length: int = 100) -> Tuple[bool, Dict[str, Any]]:
        """
        Validate a text file (script, subtitles, etc.).
        
        Args:
            file_path: Path to text file
            min_length: Minimum expected length in characters
            
        Returns:
            Tuple of (is_valid, metrics_dict)
        """
        metrics = {
            "exists": False,
            "size_bytes": 0,
            "char_count": 0,
            "word_count": 0,
            "line_count": 0,
            "is_valid": False
        }
        
        if not os.path.exists(file_path):
            log_warning(f"Text file does not exist: {file_path}")
            return False, metrics
        
        metrics["exists"] = True
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            metrics["size_bytes"] = len(content.encode('utf-8'))
            metrics["char_count"] = len(content)
            metrics["word_count"] = len(content.split())
            metrics["line_count"] = len(content.split('\n'))
            
            # Validate content length
            if len(content) < min_length:
                log_warning(
                    f"Text file too short ({len(content)} chars, expected >= {min_length}): "
                    f"{file_path}"
                )
                return False, metrics
            
            # Check if file is not empty or only whitespace
            if not content.strip():
                log_warning(f"Text file is empty or whitespace only: {file_path}")
                return False, metrics
            
            metrics["is_valid"] = True
            log_info(
                f"✅ Text file validated: {file_path} "
                f"({metrics['word_count']} words, {metrics['line_count']} lines)"
            )
            return True, metrics
            
        except Exception as e:
            logger.error(f"Error validating text file: {e}")
            return False, metrics
    
    @staticmethod
    def validate_subtitle_sync(audio_duration: float, subtitle_file: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Validate that subtitles are properly synced with audio.
        
        Args:
            audio_duration: Duration of audio in seconds
            subtitle_file: Path to SRT subtitle file
            
        Returns:
            Tuple of (is_valid, metrics_dict)
        """
        metrics = {
            "subtitle_count": 0,
            "max_time": 0.0,
            "sync_valid": False,
            "coverage_percent": 0.0
        }
        
        if not os.path.exists(subtitle_file):
            log_warning(f"Subtitle file does not exist: {subtitle_file}")
            return False, metrics
        
        try:
            with open(subtitle_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse SRT timestamps (format: HH:MM:SS,mmm --> HH:MM:SS,mmm)
            import re
            timestamps = re.findall(
                r'(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})',
                content
            )
            
            metrics["subtitle_count"] = len(timestamps)
            
            if not timestamps:
                log_warning(f"No valid timestamps found in subtitle file: {subtitle_file}")
                return False, metrics
            
            # Find the maximum timestamp
            max_time = 0.0
            for ts in timestamps:
                # Parse end time (last 4 values)
                h, m, s, ms = int(ts[4]), int(ts[5]), int(ts[6]), int(ts[7])
                time_sec = h * 3600 + m * 60 + s + ms / 1000.0
                max_time = max(max_time, time_sec)
            
            metrics["max_time"] = round(max_time, 2)
            
            # Check if subtitles cover the audio duration
            # Allow 5% tolerance
            tolerance = audio_duration * 0.05
            if abs(max_time - audio_duration) <= tolerance:
                metrics["sync_valid"] = True
                metrics["coverage_percent"] = round((max_time / audio_duration) * 100, 1)
                log_info(
                    f"✅ Subtitles synced: {subtitle_file} "
                    f"({metrics['subtitle_count']} entries, {metrics['coverage_percent']}% coverage)"
                )
                return True, metrics
            else:
                log_warning(
                    f"Subtitle timing mismatch: audio={audio_duration}s, "
                    f"subtitles={max_time}s (diff={(audio_duration - max_time):.2f}s)"
                )
                metrics["coverage_percent"] = round((max_time / audio_duration) * 100, 1)
                return False, metrics
                
        except Exception as e:
            logger.error(f"Error validating subtitle sync: {e}")
            return False, metrics
    
    @staticmethod
    def validate_video_file(file_path: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Validate a video file.
        
        Returns:
            Tuple of (is_valid, metrics_dict)
        """
        metrics = {
            "exists": False,
            "size_bytes": 0,
            "size_mb": 0.0,
            "is_valid": False
        }
        
        if not os.path.exists(file_path):
            log_warning(f"Video file does not exist: {file_path}")
            return False, metrics
        
        metrics["exists"] = True
        
        try:
            size_bytes = os.path.getsize(file_path)
            metrics["size_bytes"] = size_bytes
            metrics["size_mb"] = round(size_bytes / (1024 * 1024), 2)
            
            # Video should be at least 100KB
            if size_bytes < 102400:
                log_warning(f"Video file too small ({size_bytes} bytes): {file_path}")
                return False, metrics
            
            # Try to get video properties
            try:
                import ffmpeg
                probe = ffmpeg.probe(file_path)
                
                video_stream = next(
                    (s for s in probe['streams'] if s['codec_type'] == 'video'),
                    None
                )
                audio_stream = next(
                    (s for s in probe['streams'] if s['codec_type'] == 'audio'),
                    None
                )
                
                if video_stream:
                    metrics["width"] = int(video_stream.get('width', 0))
                    metrics["height"] = int(video_stream.get('height', 0))
                    metrics["codec"] = video_stream.get('codec_name', 'unknown')
                
                if audio_stream:
                    metrics["audio_codec"] = audio_stream.get('codec_name', 'unknown')
                
                duration = float(probe['format'].get('duration', 0))
                metrics["duration_seconds"] = round(duration, 2)
                
                # Validate that video has both video and audio streams
                if not video_stream:
                    log_warning(f"Video file has no video stream: {file_path}")
                    return False, metrics
                
                if not audio_stream:
                    log_warning(f"Video file has no audio stream: {file_path}")
                    return False, metrics
                
            except Exception as e:
                log_warning(f"Could not probe video file: {e}")
            
            metrics["is_valid"] = True
            log_info(f"✅ Video file validated: {file_path} ({metrics['size_mb']}MB)")
            return True, metrics
            
        except Exception as e:
            logger.error(f"Error validating video file: {e}")
            return False, metrics
