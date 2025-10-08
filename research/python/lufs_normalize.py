"""
FFmpeg audio normalization using loudnorm filter.
Research prototype for LUFS-based audio normalization.
"""

import subprocess
import json
import tempfile
from pathlib import Path
from typing import Optional, Dict


class LUFSNormalizer:
    """
    FFmpeg-based audio normalization using EBU R128 loudness normalization.
    
    This is a research prototype demonstrating how to:
    - Use FFmpeg loudnorm filter for professional audio normalization
    - Perform two-pass normalization for accurate results
    - Handle various audio formats
    - Extract audio metrics
    """
    
    def __init__(
        self,
        target_lufs: float = -14.0,
        target_lra: float = 7.0,
        target_tp: float = -1.0,
        sample_rate: int = 48000
    ):
        """
        Initialize LUFS normalizer.
        
        Args:
            target_lufs: Target integrated loudness in LUFS (typically -14 to -16)
            target_lra: Target loudness range in LU
            target_tp: Target true peak in dBTP
            sample_rate: Output sample rate in Hz
        """
        self.target_lufs = target_lufs
        self.target_lra = target_lra
        self.target_tp = target_tp
        self.sample_rate = sample_rate
    
    def normalize(
        self,
        input_path: str,
        output_path: str,
        two_pass: bool = True
    ) -> Dict:
        """
        Normalize audio to target LUFS.
        
        Args:
            input_path: Path to input audio file
            output_path: Path to save normalized audio
            two_pass: Use two-pass normalization for better accuracy
            
        Returns:
            Dictionary with normalization metrics
        """
        if two_pass:
            return self._normalize_two_pass(input_path, output_path)
        else:
            return self._normalize_single_pass(input_path, output_path)
    
    def _normalize_single_pass(
        self,
        input_path: str,
        output_path: str
    ) -> Dict:
        """Single-pass normalization (faster but less accurate)."""
        cmd = [
            "ffmpeg", "-y", "-i", input_path,
            "-af", f"loudnorm=I={self.target_lufs}:LRA={self.target_lra}:TP={self.target_tp}",
            "-ar", str(self.sample_rate),
            output_path
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return {"success": True, "method": "single_pass"}
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg normalization failed: {e.stderr}")
    
    def _normalize_two_pass(
        self,
        input_path: str,
        output_path: str
    ) -> Dict:
        """
        Two-pass normalization for accurate results.
        
        Pass 1: Analyze audio and get measurements
        Pass 2: Apply normalization with measured values
        """
        # First pass: analyze
        measurements = self._measure_loudness(input_path)
        
        # Second pass: normalize with measured values
        cmd = [
            "ffmpeg", "-y", "-i", input_path,
            "-af",
            (
                f"loudnorm=I={self.target_lufs}:"
                f"LRA={self.target_lra}:"
                f"TP={self.target_tp}:"
                f"measured_I={measurements['input_i']}:"
                f"measured_LRA={measurements['input_lra']}:"
                f"measured_TP={measurements['input_tp']}:"
                f"measured_thresh={measurements['input_thresh']}:"
                f"offset={measurements['target_offset']}:"
                "linear=true:print_format=json"
            ),
            "-ar", str(self.sample_rate),
            output_path
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return {
                "success": True,
                "method": "two_pass",
                "measurements": measurements
            }
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg normalization failed: {e.stderr}")
    
    def _measure_loudness(self, audio_path: str) -> Dict:
        """
        Measure audio loudness using FFmpeg loudnorm filter.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Dictionary with loudness measurements
        """
        cmd = [
            "ffmpeg", "-i", audio_path,
            "-af",
            f"loudnorm=I={self.target_lufs}:LRA={self.target_lra}:TP={self.target_tp}:print_format=json",
            "-f", "null",
            "-"
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False  # loudnorm outputs to stderr even on success
            )
            
            # Parse JSON output from stderr
            output = result.stderr
            
            # Find JSON block in output
            json_start = output.rfind("{")
            json_end = output.rfind("}") + 1
            
            if json_start == -1 or json_end == 0:
                raise RuntimeError("Could not find JSON output in FFmpeg response")
            
            json_str = output[json_start:json_end]
            measurements = json.loads(json_str)
            
            return measurements
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg measurement failed: {e.stderr}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse FFmpeg JSON output: {e}")
    
    def get_audio_info(self, audio_path: str) -> Dict:
        """
        Get audio file information using FFprobe.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Dictionary with audio information
        """
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            audio_path
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            info = json.loads(result.stdout)
            
            # Extract relevant audio info
            audio_stream = None
            for stream in info.get("streams", []):
                if stream.get("codec_type") == "audio":
                    audio_stream = stream
                    break
            
            if not audio_stream:
                raise RuntimeError("No audio stream found")
            
            return {
                "duration": float(info["format"].get("duration", 0)),
                "sample_rate": int(audio_stream.get("sample_rate", 0)),
                "channels": int(audio_stream.get("channels", 0)),
                "codec": audio_stream.get("codec_name", "unknown"),
                "bit_rate": int(audio_stream.get("bit_rate", 0))
            }
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFprobe failed: {e.stderr}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse FFprobe output: {e}")
    
    def batch_normalize(
        self,
        input_files: list,
        output_dir: str,
        two_pass: bool = True
    ) -> Dict:
        """
        Normalize multiple audio files.
        
        Args:
            input_files: List of input file paths
            output_dir: Directory to save normalized files
            two_pass: Use two-pass normalization
            
        Returns:
            Dictionary with results for each file
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        results = {}
        
        for input_file in input_files:
            input_path = Path(input_file)
            output_path = output_dir / f"{input_path.stem}_normalized{input_path.suffix}"
            
            try:
                result = self.normalize(
                    str(input_path),
                    str(output_path),
                    two_pass=two_pass
                )
                results[str(input_path)] = {
                    "success": True,
                    "output": str(output_path),
                    "metrics": result
                }
            except Exception as e:
                results[str(input_path)] = {
                    "success": False,
                    "error": str(e)
                }
        
        return results


# Example usage
if __name__ == "__main__":
    # Initialize normalizer
    normalizer = LUFSNormalizer(target_lufs=-16.0)
    
    # Example file paths
    input_file = "input.mp3"
    output_file = "output_normalized.mp3"
    
    # Get audio info
    try:
        info = normalizer.get_audio_info(input_file)
        print("Audio Info:")
        print(f"  Duration: {info['duration']:.2f}s")
        print(f"  Sample Rate: {info['sample_rate']} Hz")
        print(f"  Channels: {info['channels']}")
        print(f"  Codec: {info['codec']}")
    except Exception as e:
        print(f"Error getting info: {e}")
    
    # Normalize audio
    try:
        result = normalizer.normalize(input_file, output_file, two_pass=True)
        print("\nNormalization completed:")
        print(f"  Method: {result['method']}")
        if 'measurements' in result:
            print(f"  Input LUFS: {result['measurements']['input_i']}")
            print(f"  Target LUFS: {normalizer.target_lufs}")
    except Exception as e:
        print(f"Error normalizing: {e}")
    
    # Batch normalize
    files = ["audio1.mp3", "audio2.mp3"]
    results = normalizer.batch_normalize(files, "normalized_output/")
    print(f"\nBatch normalization: {sum(1 for r in results.values() if r['success'])}/{len(files)} succeeded")
