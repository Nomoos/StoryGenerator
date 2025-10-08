"""
Microstep validation and progress tracking utility for StoryGenerator.
Handles artifact creation, config logging, progress tracking, and validation for each pipeline microstep.
"""

import os
import json
import yaml
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path
import logging

# Configure logging
logger = logging.getLogger("MicrostepValidator")


class MicrostepValidator:
    """
    Validates and tracks progress for pipeline microsteps.
    
    For each microstep:
    - Creates artifacts in the specified folder
    - Logs config used (copy of YAML subset)
    - Appends to running progress.md in the same folder
    - Provides validation interface for @copilot check
    """
    
    # Define all 19 pipeline microsteps
    MICROSTEPS = {
        1: {"name": "trends", "folder": "trends", "description": "Process Google Trends data"},
        2: {"name": "ideas", "folder": "ideas", "description": "Generate story ideas"},
        3: {"name": "topics", "folder": "topics", "description": "Classify and organize topics"},
        4: {"name": "titles", "folder": "titles", "description": "Create engaging video titles"},
        5: {"name": "scores", "folder": "scores", "description": "Quality scoring and metrics"},
        6: {"name": "scripts_raw", "folder": "scripts/raw_local", "description": "Initial script generation"},
        7: {"name": "scripts_iter", "folder": "scripts/iter_local", "description": "Iteratively refined scripts"},
        8: {"name": "scripts_gpt", "folder": "scripts/gpt_improved", "description": "GPT-improved scripts"},
        9: {"name": "voice_choice", "folder": "voices/choice", "description": "Voice selection"},
        10: {"name": "audio_tts", "folder": "audio/tts", "description": "Text-to-speech audio"},
        11: {"name": "audio_normalized", "folder": "audio/normalized", "description": "Normalized audio"},
        12: {"name": "subtitles_srt", "folder": "subtitles/srt", "description": "SRT subtitle files"},
        13: {"name": "subtitles_timed", "folder": "subtitles/timed", "description": "Timed subtitle data"},
        14: {"name": "scenes", "folder": "scenes/json", "description": "Scene descriptions"},
        15: {"name": "keyframes_v1", "folder": "images/keyframes_v1", "description": "Keyframe images v1"},
        16: {"name": "keyframes_v2", "folder": "images/keyframes_v2", "description": "Keyframe images v2"},
        17: {"name": "videos_ltx", "folder": "videos/ltx", "description": "LTX video files"},
        18: {"name": "videos_interp", "folder": "videos/interp", "description": "Interpolated videos"},
        19: {"name": "final", "folder": "final", "description": "Final output"},
    }
    
    def __init__(self, base_path: str = None, config_path: str = None):
        """
        Initialize the MicrostepValidator.
        
        Args:
            base_path: Base path for Generator folder (default: src/Generator)
            config_path: Path to pipeline.yaml config file (default: data/config/pipeline.yaml)
        """
        if base_path is None:
            # Assume we're in src/Python/Tools, so go up to project root
            project_root = Path(__file__).parent.parent.parent.parent
            self.base_path = project_root / "src" / "Generator"
        else:
            self.base_path = Path(base_path)
        
        if config_path is None:
            project_root = Path(__file__).parent.parent.parent.parent
            self.config_path = project_root / "data" / "config" / "pipeline.yaml"
        else:
            self.config_path = Path(config_path)
        
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load the pipeline configuration."""
        if not self.config_path.exists():
            logger.warning(f"Config file not found: {self.config_path}")
            return {}
        
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {}
    
    def get_microstep_folder(self, step_number: int, gender: str = None, age: str = None) -> Path:
        """
        Get the full path to a microstep folder.
        
        Args:
            step_number: Microstep number (1-19)
            gender: Target gender (optional, e.g., 'men', 'women')
            age: Target age group (optional, e.g., '18-23', '24-29')
        
        Returns:
            Path to the microstep folder
        """
        if step_number not in self.MICROSTEPS:
            raise ValueError(f"Invalid microstep number: {step_number}. Must be 1-19.")
        
        step_info = self.MICROSTEPS[step_number]
        folder_path = self.base_path / step_info["folder"]
        
        # Add gender/age subdirectories if provided
        if gender:
            folder_path = folder_path / gender
            if age:
                folder_path = folder_path / age
        
        return folder_path
    
    def create_artifact(self, step_number: int, artifact_name: str, content: Any,
                       gender: str = None, age: str = None) -> Path:
        """
        Create an artifact file for a microstep.
        
        Args:
            step_number: Microstep number (1-19)
            artifact_name: Name of the artifact file
            content: Content to write (string, dict, or list)
            gender: Target gender (optional)
            age: Target age group (optional)
        
        Returns:
            Path to the created artifact
        """
        folder = self.get_microstep_folder(step_number, gender, age)
        folder.mkdir(parents=True, exist_ok=True)
        
        artifact_path = folder / artifact_name
        
        # Determine file type and write accordingly
        if isinstance(content, (dict, list)):
            # JSON content
            with open(artifact_path, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2, ensure_ascii=False)
        else:
            # Text content
            with open(artifact_path, 'w', encoding='utf-8') as f:
                f.write(str(content))
        
        logger.info(f"Created artifact: {artifact_path}")
        return artifact_path
    
    def log_config(self, step_number: int, config_subset: Dict[str, Any] = None,
                   gender: str = None, age: str = None) -> Path:
        """
        Log the configuration used for a microstep.
        
        Args:
            step_number: Microstep number (1-19)
            config_subset: Specific config subset to log (if None, extracts relevant config)
            gender: Target gender (optional)
            age: Target age group (optional)
        
        Returns:
            Path to the config log file
        """
        folder = self.get_microstep_folder(step_number, gender, age)
        folder.mkdir(parents=True, exist_ok=True)
        
        step_info = self.MICROSTEPS[step_number]
        
        # If no subset provided, extract relevant config based on step
        if config_subset is None:
            config_subset = self._extract_relevant_config(step_number)
        
        # Create config log with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        config_log_path = folder / f"config_{step_info['name']}_{timestamp}.yaml"
        
        config_data = {
            "microstep": step_number,
            "name": step_info['name'],
            "description": step_info['description'],
            "timestamp": datetime.now().isoformat(),
            "gender": gender,
            "age": age,
            "config": config_subset
        }
        
        with open(config_log_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
        
        logger.info(f"Logged config: {config_log_path}")
        return config_log_path
    
    def _extract_relevant_config(self, step_number: int) -> Dict[str, Any]:
        """Extract relevant config subset for a specific microstep."""
        # Map microsteps to relevant config sections
        config_mapping = {
            1: ["paths"],  # trends
            2: ["models", "paths"],  # ideas
            3: ["models", "paths"],  # topics
            4: ["models", "paths"],  # titles
            5: ["paths"],  # scores
            6: ["models", "paths"],  # scripts_raw
            7: ["models", "paths"],  # scripts_iter
            8: ["models", "paths"],  # scripts_gpt
            9: ["models", "audio", "paths"],  # voice_choice
            10: ["models", "audio", "paths"],  # audio_tts
            11: ["audio", "paths"],  # audio_normalized
            12: ["models", "paths"],  # subtitles_srt
            13: ["paths"],  # subtitles_timed
            14: ["models", "paths"],  # scenes
            15: ["models", "video", "seeds", "paths"],  # keyframes_v1
            16: ["models", "video", "seeds", "paths"],  # keyframes_v2
            17: ["models", "video", "seeds", "paths", "switches"],  # videos_ltx
            18: ["models", "video", "seeds", "paths", "switches"],  # videos_interp
            19: ["video", "paths"],  # final
        }
        
        relevant_sections = config_mapping.get(step_number, ["paths"])
        subset = {}
        
        for section in relevant_sections:
            if section in self.config:
                subset[section] = self.config[section]
        
        return subset
    
    def update_progress(self, step_number: int, status: str, details: str = "",
                       gender: str = None, age: str = None, 
                       artifacts: List[str] = None) -> Path:
        """
        Update the progress.md file for a microstep.
        
        Args:
            step_number: Microstep number (1-19)
            status: Status of the step (e.g., 'started', 'completed', 'failed', 'validated')
            details: Additional details about the progress
            gender: Target gender (optional)
            age: Target age group (optional)
            artifacts: List of artifact filenames created (optional)
        
        Returns:
            Path to the progress.md file
        """
        folder = self.get_microstep_folder(step_number, gender, age)
        folder.mkdir(parents=True, exist_ok=True)
        
        progress_path = folder / "progress.md"
        step_info = self.MICROSTEPS[step_number]
        
        # Prepare progress entry
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = [
            f"\n## {timestamp} - Step {step_number}: {step_info['name']} - {status.upper()}\n",
            f"**Description:** {step_info['description']}\n",
        ]
        
        if gender:
            entry.append(f"**Target:** {gender}/{age or 'all ages'}\n")
        
        if details:
            entry.append(f"**Details:** {details}\n")
        
        if artifacts:
            entry.append(f"**Artifacts Created:**\n")
            for artifact in artifacts:
                entry.append(f"- `{artifact}`\n")
        
        entry.append(f"\n---\n")
        
        # Append to progress file
        mode = 'a' if progress_path.exists() else 'w'
        with open(progress_path, mode, encoding='utf-8') as f:
            if mode == 'w':
                # Write header for new file
                f.write(f"# Progress Log - Step {step_number}: {step_info['name']}\n")
                f.write(f"\n**Folder:** `{step_info['folder']}`\n")
                if gender:
                    f.write(f"**Target Audience:** {gender}/{age or 'all ages'}\n")
                f.write(f"\n---\n")
            
            f.writelines(entry)
        
        logger.info(f"Updated progress: {progress_path}")
        return progress_path
    
    def validate_step(self, step_number: int, gender: str = None, age: str = None,
                     validation_checks: Dict[str, bool] = None) -> Dict[str, Any]:
        """
        Validate a microstep's completion and artifacts.
        
        Args:
            step_number: Microstep number (1-19)
            gender: Target gender (optional)
            age: Target age group (optional)
            validation_checks: Custom validation checks (optional)
        
        Returns:
            Validation report as a dictionary
        """
        folder = self.get_microstep_folder(step_number, gender, age)
        step_info = self.MICROSTEPS[step_number]
        
        report = {
            "step_number": step_number,
            "step_name": step_info['name'],
            "description": step_info['description'],
            "folder": str(folder),
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "artifacts": [],
            "is_valid": False
        }
        
        # Check if folder exists
        report["checks"]["folder_exists"] = folder.exists()
        
        if folder.exists():
            # List all artifacts in the folder
            artifacts = [f.name for f in folder.iterdir() if f.is_file()]
            report["artifacts"] = artifacts
            report["checks"]["has_artifacts"] = len(artifacts) > 0
            report["checks"]["has_progress"] = "progress.md" in artifacts
            report["checks"]["has_config"] = any("config_" in a for a in artifacts)
        else:
            report["checks"]["has_artifacts"] = False
            report["checks"]["has_progress"] = False
            report["checks"]["has_config"] = False
        
        # Add custom validation checks if provided
        if validation_checks:
            report["checks"].update(validation_checks)
        
        # Overall validation: folder exists, has artifacts, progress, and config
        report["is_valid"] = all([
            report["checks"].get("folder_exists", False),
            report["checks"].get("has_artifacts", False),
            report["checks"].get("has_progress", False),
            report["checks"].get("has_config", False)
        ])
        
        # Log validation report
        validation_path = folder / f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        if folder.exists():
            with open(validation_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            logger.info(f"Validation report saved: {validation_path}")
        
        return report
    
    def copilot_check(self, step_number: int, gender: str = None, age: str = None) -> str:
        """
        Perform a @copilot check for a microstep.
        Returns a formatted validation summary for easy review.
        
        Args:
            step_number: Microstep number (1-19)
            gender: Target gender (optional)
            age: Target age group (optional)
        
        Returns:
            Formatted validation summary as a string
        """
        report = self.validate_step(step_number, gender, age)
        
        # Format validation summary
        summary = [
            f"\n{'='*60}",
            f"@copilot CHECK - Step {step_number}: {report['step_name']}",
            f"{'='*60}",
            f"\n📁 Folder: {report['folder']}",
            f"📅 Timestamp: {report['timestamp']}\n",
            f"\n✅ Validation Checks:",
        ]
        
        for check, result in report['checks'].items():
            status = "✅" if result else "❌"
            summary.append(f"  {status} {check.replace('_', ' ').title()}: {result}")
        
        summary.append(f"\n📦 Artifacts ({len(report['artifacts'])}):")
        if report['artifacts']:
            for artifact in report['artifacts']:
                summary.append(f"  - {artifact}")
        else:
            summary.append("  (No artifacts found)")
        
        summary.append(f"\n{'='*60}")
        summary.append(f"Overall Status: {'✅ VALID' if report['is_valid'] else '❌ INVALID'}")
        summary.append(f"{'='*60}\n")
        
        result = "\n".join(summary)
        print(result)
        return result
    
    @classmethod
    def list_microsteps(cls) -> str:
        """List all available microsteps with their descriptions."""
        lines = [
            "\n" + "="*60,
            "Available Microsteps",
            "="*60 + "\n"
        ]
        
        for step_num, info in cls.MICROSTEPS.items():
            lines.append(f"{step_num:2d}. {info['name']:20s} - {info['description']}")
            lines.append(f"    Folder: {info['folder']}\n")
        
        result = "\n".join(lines)
        print(result)
        return result


# Convenience functions for common operations
def create_microstep_artifact(step_number: int, artifact_name: str, content: Any,
                              gender: str = None, age: str = None,
                              base_path: str = None, config_path: str = None) -> Path:
    """
    Quick function to create a microstep artifact.
    
    Args:
        step_number: Microstep number (1-19)
        artifact_name: Name of the artifact file
        content: Content to write
        gender: Target gender (optional)
        age: Target age group (optional)
        base_path: Base path for Generator folder (optional)
        config_path: Path to config file (optional)
    
    Returns:
        Path to the created artifact
    """
    validator = MicrostepValidator(base_path, config_path)
    return validator.create_artifact(step_number, artifact_name, content, gender, age)


def log_microstep_config(step_number: int, config_subset: Dict[str, Any] = None,
                        gender: str = None, age: str = None,
                        base_path: str = None, config_path: str = None) -> Path:
    """
    Quick function to log microstep configuration.
    
    Args:
        step_number: Microstep number (1-19)
        config_subset: Specific config subset to log (optional)
        gender: Target gender (optional)
        age: Target age group (optional)
        base_path: Base path for Generator folder (optional)
        config_path: Path to config file (optional)
    
    Returns:
        Path to the config log file
    """
    validator = MicrostepValidator(base_path, config_path)
    return validator.log_config(step_number, config_subset, gender, age)


def update_microstep_progress(step_number: int, status: str, details: str = "",
                              gender: str = None, age: str = None,
                              artifacts: List[str] = None,
                              base_path: str = None, config_path: str = None) -> Path:
    """
    Quick function to update microstep progress.
    
    Args:
        step_number: Microstep number (1-19)
        status: Status of the step
        details: Additional details (optional)
        gender: Target gender (optional)
        age: Target age group (optional)
        artifacts: List of artifact filenames (optional)
        base_path: Base path for Generator folder (optional)
        config_path: Path to config file (optional)
    
    Returns:
        Path to the progress.md file
    """
    validator = MicrostepValidator(base_path, config_path)
    return validator.update_progress(step_number, status, details, gender, age, artifacts)


def copilot_check_microstep(step_number: int, gender: str = None, age: str = None,
                           base_path: str = None, config_path: str = None) -> str:
    """
    Quick function to perform @copilot check on a microstep.
    
    Args:
        step_number: Microstep number (1-19)
        gender: Target gender (optional)
        age: Target age group (optional)
        base_path: Base path for Generator folder (optional)
        config_path: Path to config file (optional)
    
    Returns:
        Formatted validation summary
    """
    validator = MicrostepValidator(base_path, config_path)
    return validator.copilot_check(step_number, gender, age)
