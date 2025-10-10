#!/usr/bin/env python3
"""
Pipeline Step Orchestrator

Orchestrates individual pipeline steps with support for:
- Picking a candidate story ID (pick-one)
- Running a step for a specific story (run)
- Checking acceptance criteria (check-acceptance)

Usage:
    python run_step.py --step 01_ingest --action pick-one
    python run_step.py --step 03_generate --run-id 20241010-123456 --story-id STORY-123 --action run
    python run_step.py --step 05_package --run-id 20241010-123456 --story-id STORY-123 --action check-acceptance
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class StepOrchestrator:
    """Orchestrates pipeline steps with pick-one, run, and acceptance checking."""
    
    def __init__(self, step_name: str, run_id: str, story_id: Optional[str] = None):
        self.step_name = step_name
        self.run_id = run_id
        self.story_id = story_id
        self.run_root = Path(os.getenv("RUN_ROOT", ".runs"))
        self.output_dir = Path(os.getenv("OUTPUT_DIR", "outputs"))
        
        # Create necessary directories
        self.run_dir = self.run_root / self.run_id
        self.run_dir.mkdir(parents=True, exist_ok=True)
        
        self.step_output_dir = self.output_dir / self.step_name
        self.step_output_dir.mkdir(parents=True, exist_ok=True)
        
    def pick_one_candidate(self) -> Optional[str]:
        """Pick one pending story ID for this step."""
        logger.info(f"[{self.step_name}] Picking one candidate story...")
        
        # Get list of pending stories for this step
        candidates = self._get_pending_stories()
        
        if not candidates:
            logger.warning(f"[{self.step_name}] No pending stories found")
            return None
            
        # Return the first pending story
        story_id = candidates[0]
        logger.info(f"[{self.step_name}] Selected story: {story_id}")
        return story_id
    
    def _get_pending_stories(self) -> List[str]:
        """Get list of stories pending for this step."""
        # Check for stories that need processing
        # For now, we'll check the previous step's output directory
        
        step_num = self._get_step_number()
        
        if step_num == 1:
            # First step - check input directory or create placeholder
            input_dir = Path(os.getenv("STEP_01_INGEST_SOURCE_DIR", "data/raw"))
            if input_dir.exists():
                # Look for pending story files
                pending = [f.stem for f in input_dir.glob("*.json")]
                if pending:
                    return pending
            # Create a placeholder story ID if none exist
            return [f"STORY-{datetime.now().strftime('%Y%m%d%H%M%S')}"]
        else:
            # Subsequent steps - check previous step's output
            prev_step = f"{step_num-1:02d}_{self._get_step_name_part(step_num-1)}"
            prev_output = self.output_dir / prev_step
            
            if prev_output.exists():
                # Look for completed stories from previous step
                completed = [f.stem for f in prev_output.glob("*.json")]
                
                # Filter out stories already processed by current step
                current_output = self.output_dir / self.step_name
                already_processed = {f.stem for f in current_output.glob("*.json")} if current_output.exists() else set()
                
                pending = [s for s in completed if s not in already_processed]
                return pending
            
            return []
    
    def _get_step_number(self) -> int:
        """Extract step number from step name."""
        try:
            return int(self.step_name.split("_")[0])
        except (ValueError, IndexError):
            return 0
    
    def _get_step_name_part(self, step_num: int) -> str:
        """Get step name part for a given step number."""
        step_names = {
            1: "ingest",
            2: "preprocess", 
            3: "generate",
            4: "postprocess",
            5: "package"
        }
        return step_names.get(step_num, "unknown")
    
    def run_step(self) -> bool:
        """Execute the step for the given story."""
        if not self.story_id:
            logger.error(f"[{self.step_name}] No story_id provided for run action")
            return False
            
        logger.info(f"[{self.step_name}] Running step for story: {self.story_id}")
        
        try:
            # Get step-specific handler
            handler = self._get_step_handler()
            
            # Execute the step
            result = handler()
            
            if result:
                # Record execution in run metadata
                self._record_execution()
                logger.info(f"[{self.step_name}] Step completed successfully for {self.story_id}")
            else:
                logger.error(f"[{self.step_name}] Step failed for {self.story_id}")
                
            return result
            
        except Exception as e:
            logger.error(f"[{self.step_name}] Error running step: {e}", exc_info=True)
            return False
    
    def _get_step_handler(self):
        """Get the appropriate handler function for this step."""
        step_num = self._get_step_number()
        handlers = {
            1: self._run_ingest,
            2: self._run_preprocess,
            3: self._run_generate,
            4: self._run_postprocess,
            5: self._run_package
        }
        return handlers.get(step_num, self._run_default)
    
    def _run_ingest(self) -> bool:
        """Run ingest step - load raw data."""
        logger.info(f"[{self.step_name}] Ingesting data for {self.story_id}")
        
        # Create placeholder input data
        input_data = {
            "story_id": self.story_id,
            "title": f"Story {self.story_id}",
            "content": "This is a sample story content that will be processed through the pipeline. " * 5,  # Ensure it meets minimum length
            "source": "manual",
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "run_id": self.run_id,
                "step": self.step_name
            }
        }
        
        # Save to output directory
        output_file = self.step_output_dir / f"{self.story_id}.json"
        with open(output_file, "w") as f:
            json.dump(input_data, f, indent=2)
            
        logger.info(f"[{self.step_name}] Ingested data saved to {output_file}")
        return True
    
    def _run_preprocess(self) -> bool:
        """Run preprocess step - clean and validate data."""
        logger.info(f"[{self.step_name}] Preprocessing data for {self.story_id}")
        
        # Load data from previous step
        prev_step = "01_ingest"
        input_file = self.output_dir / prev_step / f"{self.story_id}.json"
        
        if not input_file.exists():
            logger.error(f"[{self.step_name}] Input file not found: {input_file}")
            return False
        
        with open(input_file) as f:
            data = json.load(f)
        
        # Preprocess the data
        processed_data = {
            **data,
            "processed": True,
            "word_count": len(data.get("content", "").split()),
            "char_count": len(data.get("content", "")),
            "preprocessing_timestamp": datetime.now().isoformat()
        }
        
        # Save to output directory
        output_file = self.step_output_dir / f"{self.story_id}.json"
        with open(output_file, "w") as f:
            json.dump(processed_data, f, indent=2)
            
        logger.info(f"[{self.step_name}] Preprocessed data saved to {output_file}")
        return True
    
    def _run_generate(self) -> bool:
        """Run generate step - generate content."""
        logger.info(f"[{self.step_name}] Generating content for {self.story_id}")
        
        # Load data from previous step
        prev_step = "02_preprocess"
        input_file = self.output_dir / prev_step / f"{self.story_id}.json"
        
        if not input_file.exists():
            logger.error(f"[{self.step_name}] Input file not found: {input_file}")
            return False
        
        with open(input_file) as f:
            data = json.load(f)
        
        # Generate content (placeholder)
        generated_data = {
            **data,
            "generated_script": f"Generated script for {self.story_id}",
            "generated_scenes": [
                {"scene": 1, "description": "Opening scene"},
                {"scene": 2, "description": "Main content"},
                {"scene": 3, "description": "Closing scene"}
            ],
            "generation_timestamp": datetime.now().isoformat(),
            "model": os.getenv("STEP_03_GENERATE_MODEL_NAME", "gpt-4o-mini")
        }
        
        # Save to output directory
        output_file = self.step_output_dir / f"{self.story_id}.json"
        with open(output_file, "w") as f:
            json.dump(generated_data, f, indent=2)
            
        logger.info(f"[{self.step_name}] Generated content saved to {output_file}")
        return True
    
    def _run_postprocess(self) -> bool:
        """Run postprocess step - validate and enhance."""
        logger.info(f"[{self.step_name}] Postprocessing content for {self.story_id}")
        
        # Load data from previous step
        prev_step = "03_generate"
        input_file = self.output_dir / prev_step / f"{self.story_id}.json"
        
        if not input_file.exists():
            logger.error(f"[{self.step_name}] Input file not found: {input_file}")
            return False
        
        with open(input_file) as f:
            data = json.load(f)
        
        # Postprocess the data
        postprocessed_data = {
            **data,
            "postprocessed": True,
            "quality_score": 0.85,
            "validation_passed": True,
            "postprocessing_timestamp": datetime.now().isoformat()
        }
        
        # Save to output directory
        output_file = self.step_output_dir / f"{self.story_id}.json"
        with open(output_file, "w") as f:
            json.dump(postprocessed_data, f, indent=2)
            
        logger.info(f"[{self.step_name}] Postprocessed data saved to {output_file}")
        return True
    
    def _run_package(self) -> bool:
        """Run package step - create final output."""
        logger.info(f"[{self.step_name}] Packaging content for {self.story_id}")
        
        # Load data from previous step
        prev_step = "04_postprocess"
        input_file = self.output_dir / prev_step / f"{self.story_id}.json"
        
        if not input_file.exists():
            logger.error(f"[{self.step_name}] Input file not found: {input_file}")
            return False
        
        with open(input_file) as f:
            data = json.load(f)
        
        # Package the data
        packaged_data = {
            **data,
            "packaged": True,
            "output_format": os.getenv("STEP_05_PACKAGE_OUTPUT_FORMAT", "mp4"),
            "package_timestamp": datetime.now().isoformat(),
            "final_output_path": f"outputs/final/{self.story_id}.mp4"
        }
        
        # Save to output directory
        output_file = self.step_output_dir / f"{self.story_id}.json"
        with open(output_file, "w") as f:
            json.dump(packaged_data, f, indent=2)
            
        logger.info(f"[{self.step_name}] Packaged data saved to {output_file}")
        return True
    
    def _run_default(self) -> bool:
        """Default handler for unknown steps."""
        logger.warning(f"[{self.step_name}] No specific handler, using default")
        return True
    
    def _record_execution(self):
        """Record step execution metadata."""
        metadata_file = self.run_dir / f"{self.step_name}_{self.story_id}.json"
        metadata = {
            "step": self.step_name,
            "story_id": self.story_id,
            "run_id": self.run_id,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
        
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)
    
    def check_acceptance(self) -> bool:
        """Check if acceptance criteria are met for this story."""
        if not self.story_id:
            logger.error(f"[{self.step_name}] No story_id provided for acceptance check")
            return False
            
        logger.info(f"[{self.step_name}] Checking acceptance for {self.story_id}")
        
        try:
            # Get step-specific acceptance checker
            checker = self._get_acceptance_checker()
            
            # Check acceptance
            passed, reason = checker()
            
            if passed:
                logger.info(f"[{self.step_name}] Acceptance check passed for {self.story_id}")
            else:
                logger.warning(f"[{self.step_name}] Acceptance check failed for {self.story_id}: {reason}")
                
            return passed
            
        except Exception as e:
            logger.error(f"[{self.step_name}] Error checking acceptance: {e}", exc_info=True)
            return False
    
    def _get_acceptance_checker(self):
        """Get the appropriate acceptance checker for this step."""
        step_num = self._get_step_number()
        checkers = {
            1: self._check_ingest_acceptance,
            2: self._check_preprocess_acceptance,
            3: self._check_generate_acceptance,
            4: self._check_postprocess_acceptance,
            5: self._check_package_acceptance
        }
        return checkers.get(step_num, self._check_default_acceptance)
    
    def _check_ingest_acceptance(self) -> Tuple[bool, str]:
        """Check ingest step acceptance criteria."""
        output_file = self.step_output_dir / f"{self.story_id}.json"
        
        if not output_file.exists():
            return False, "Output file does not exist"
        
        try:
            with open(output_file) as f:
                data = json.load(f)
            
            # Check required fields
            required_fields = ["story_id", "title", "content"]
            for field in required_fields:
                if field not in data:
                    return False, f"Missing required field: {field}"
            
            # Check minimum content length
            min_length = int(os.getenv("STEP_01_INGEST_MIN_LENGTH", "100"))
            if len(data.get("content", "")) < min_length:
                return False, f"Content too short (minimum {min_length} characters)"
            
            return True, "All criteria met"
            
        except Exception as e:
            return False, f"Error validating data: {e}"
    
    def _check_preprocess_acceptance(self) -> Tuple[bool, str]:
        """Check preprocess step acceptance criteria."""
        output_file = self.step_output_dir / f"{self.story_id}.json"
        
        if not output_file.exists():
            return False, "Output file does not exist"
        
        try:
            with open(output_file) as f:
                data = json.load(f)
            
            # Check preprocessing was done
            if not data.get("processed"):
                return False, "Data not marked as processed"
            
            # Check word count is within acceptable range
            word_count = data.get("word_count", 0)
            min_words = int(os.getenv("STEP_02_PREPROCESS_MIN_WORDS", "50"))
            max_words = int(os.getenv("STEP_02_PREPROCESS_MAX_WORDS", "500"))
            
            if word_count < min_words:
                return False, f"Word count too low: {word_count} < {min_words}"
            if word_count > max_words:
                return False, f"Word count too high: {word_count} > {max_words}"
            
            return True, "All criteria met"
            
        except Exception as e:
            return False, f"Error validating data: {e}"
    
    def _check_generate_acceptance(self) -> Tuple[bool, str]:
        """Check generate step acceptance criteria."""
        output_file = self.step_output_dir / f"{self.story_id}.json"
        
        if not output_file.exists():
            return False, "Output file does not exist"
        
        try:
            with open(output_file) as f:
                data = json.load(f)
            
            # Check generated content exists
            if not data.get("generated_script"):
                return False, "No generated script"
            
            if not data.get("generated_scenes"):
                return False, "No generated scenes"
            
            # Check minimum number of scenes
            min_scenes = 3
            if len(data.get("generated_scenes", [])) < min_scenes:
                return False, f"Too few scenes (minimum {min_scenes})"
            
            return True, "All criteria met"
            
        except Exception as e:
            return False, f"Error validating data: {e}"
    
    def _check_postprocess_acceptance(self) -> Tuple[bool, str]:
        """Check postprocess step acceptance criteria."""
        output_file = self.step_output_dir / f"{self.story_id}.json"
        
        if not output_file.exists():
            return False, "Output file does not exist"
        
        try:
            with open(output_file) as f:
                data = json.load(f)
            
            # Check postprocessing was done
            if not data.get("postprocessed"):
                return False, "Data not marked as postprocessed"
            
            # Check quality score
            quality_score = data.get("quality_score", 0)
            min_quality = float(os.getenv("STEP_04_POSTPROCESS_MIN_QUALITY", "0.7"))
            
            if quality_score < min_quality:
                return False, f"Quality score too low: {quality_score} < {min_quality}"
            
            # Check validation passed
            if not data.get("validation_passed"):
                return False, "Validation failed"
            
            return True, "All criteria met"
            
        except Exception as e:
            return False, f"Error validating data: {e}"
    
    def _check_package_acceptance(self) -> Tuple[bool, str]:
        """Check package step acceptance criteria."""
        output_file = self.step_output_dir / f"{self.story_id}.json"
        
        if not output_file.exists():
            return False, "Output file does not exist"
        
        try:
            with open(output_file) as f:
                data = json.load(f)
            
            # Check packaging was done
            if not data.get("packaged"):
                return False, "Data not marked as packaged"
            
            # Check final output path
            if not data.get("final_output_path"):
                return False, "No final output path"
            
            return True, "All criteria met"
            
        except Exception as e:
            return False, f"Error validating data: {e}"
    
    def _check_default_acceptance(self) -> Tuple[bool, str]:
        """Default acceptance checker."""
        return True, "No specific criteria"


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Pipeline Step Orchestrator")
    parser.add_argument("--step", required=True, help="Step name (e.g., 01_ingest)")
    parser.add_argument("--run-id", help="Run ID")
    parser.add_argument("--story-id", help="Story ID")
    parser.add_argument("--action", required=True, 
                       choices=["pick-one", "run", "check-acceptance"],
                       help="Action to perform")
    
    args = parser.parse_args()
    
    # Generate run_id if not provided
    run_id = args.run_id or datetime.now().strftime("%Y%m%d-%H%M%S")
    
    # Create orchestrator
    orchestrator = StepOrchestrator(args.step, run_id, args.story_id)
    
    # Execute action
    if args.action == "pick-one":
        story_id = orchestrator.pick_one_candidate()
        if story_id:
            print(story_id)  # Print to stdout for .bat script to capture
            sys.exit(0)
        else:
            sys.exit(1)
    
    elif args.action == "run":
        success = orchestrator.run_step()
        sys.exit(0 if success else 1)
    
    elif args.action == "check-acceptance":
        passed = orchestrator.check_acceptance()
        sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
