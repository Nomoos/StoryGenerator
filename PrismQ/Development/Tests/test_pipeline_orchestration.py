#!/usr/bin/env python3
"""
Tests for pipeline orchestration (run_step.py).

These tests validate the step orchestrator's ability to:
- Pick candidate stories
- Execute steps
- Check acceptance criteria
"""

import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PrismQ.Pipeline.orchestration.run_step import StepOrchestrator


class TestStepOrchestrator:
    """Test cases for StepOrchestrator."""
    
    def setup_method(self):
        """Set up test environment."""
        # Create temporary directories for testing
        self.temp_dir = tempfile.mkdtemp()
        self.run_root = Path(self.temp_dir) / ".runs"
        self.output_dir = Path(self.temp_dir) / "outputs"
        
        self.run_root.mkdir(parents=True)
        self.output_dir.mkdir(parents=True)
        
        # Set environment variables for testing
        os.environ["RUN_ROOT"] = str(self.run_root)
        os.environ["OUTPUT_DIR"] = str(self.output_dir)
        
    def test_orchestrator_initialization(self):
        """Test that orchestrator initializes correctly."""
        orchestrator = StepOrchestrator("01_ingest", "test-run-001", "STORY-001")
        
        assert orchestrator.step_name == "01_ingest"
        assert orchestrator.run_id == "test-run-001"
        assert orchestrator.story_id == "STORY-001"
        assert orchestrator.run_root == self.run_root
        assert orchestrator.output_dir == self.output_dir
        
        # Check directories were created
        assert orchestrator.run_dir.exists()
        assert orchestrator.step_output_dir.exists()
        
        print("✓ Orchestrator initialization test passed")
    
    def test_pick_one_candidate_creates_story(self):
        """Test that pick_one creates a story when none exist."""
        orchestrator = StepOrchestrator("01_ingest", "test-run-002")
        
        story_id = orchestrator.pick_one_candidate()
        
        assert story_id is not None
        assert story_id.startswith("STORY-")
        
        print(f"✓ Pick one candidate test passed (story_id: {story_id})")
    
    def test_run_ingest_step(self):
        """Test running the ingest step."""
        orchestrator = StepOrchestrator("01_ingest", "test-run-003", "TEST-001")
        
        result = orchestrator.run_step()
        
        assert result is True
        
        # Check output file was created
        output_file = orchestrator.step_output_dir / "TEST-001.json"
        assert output_file.exists()
        
        # Check content
        with open(output_file) as f:
            data = json.load(f)
        
        assert data["story_id"] == "TEST-001"
        assert "content" in data
        assert "timestamp" in data
        
        print("✓ Run ingest step test passed")
    
    def test_check_ingest_acceptance_pass(self):
        """Test acceptance check passes for valid ingest output."""
        orchestrator = StepOrchestrator("01_ingest", "test-run-004", "TEST-002")
        
        # First run the step
        orchestrator.run_step()
        
        # Then check acceptance
        passed = orchestrator.check_acceptance()
        
        assert passed is True
        
        print("✓ Ingest acceptance check (pass) test passed")
    
    def test_check_ingest_acceptance_fail_short_content(self):
        """Test acceptance check fails for too-short content."""
        orchestrator = StepOrchestrator("01_ingest", "test-run-005", "TEST-003")
        
        # Create invalid output (content too short)
        output_file = orchestrator.step_output_dir / "TEST-003.json"
        invalid_data = {
            "story_id": "TEST-003",
            "title": "Test",
            "content": "Short"  # Too short
        }
        
        with open(output_file, "w") as f:
            json.dump(invalid_data, f)
        
        # Check acceptance should fail
        passed = orchestrator.check_acceptance()
        
        assert passed is False
        
        print("✓ Ingest acceptance check (fail short content) test passed")
    
    def test_run_preprocess_step(self):
        """Test running the preprocess step."""
        # First create ingest output
        ingest_orchestrator = StepOrchestrator("01_ingest", "test-run-006", "TEST-004")
        ingest_orchestrator.run_step()
        
        # Now run preprocess
        preprocess_orchestrator = StepOrchestrator("02_preprocess", "test-run-006", "TEST-004")
        result = preprocess_orchestrator.run_step()
        
        assert result is True
        
        # Check output file
        output_file = preprocess_orchestrator.step_output_dir / "TEST-004.json"
        assert output_file.exists()
        
        with open(output_file) as f:
            data = json.load(f)
        
        assert data["processed"] is True
        assert "word_count" in data
        
        print("✓ Run preprocess step test passed")
    
    def test_check_preprocess_acceptance(self):
        """Test preprocess acceptance check."""
        # Setup ingest and preprocess
        ingest_orchestrator = StepOrchestrator("01_ingest", "test-run-007", "TEST-005")
        ingest_orchestrator.run_step()
        
        preprocess_orchestrator = StepOrchestrator("02_preprocess", "test-run-007", "TEST-005")
        preprocess_orchestrator.run_step()
        
        # Check acceptance
        passed = preprocess_orchestrator.check_acceptance()
        
        assert passed is True
        
        print("✓ Preprocess acceptance check test passed")
    
    def test_run_generate_step(self):
        """Test running the generate step."""
        # Setup previous steps
        story_id = "TEST-006"
        run_id = "test-run-008"
        
        ingest = StepOrchestrator("01_ingest", run_id, story_id)
        ingest.run_step()
        
        preprocess = StepOrchestrator("02_preprocess", run_id, story_id)
        preprocess.run_step()
        
        # Run generate
        generate = StepOrchestrator("03_generate", run_id, story_id)
        result = generate.run_step()
        
        assert result is True
        
        # Check output
        output_file = generate.step_output_dir / f"{story_id}.json"
        assert output_file.exists()
        
        with open(output_file) as f:
            data = json.load(f)
        
        assert "generated_script" in data
        assert "generated_scenes" in data
        assert len(data["generated_scenes"]) >= 3
        
        print("✓ Run generate step test passed")
    
    def test_full_pipeline_flow(self):
        """Test complete pipeline flow through all steps."""
        story_id = "TEST-FULL-001"
        run_id = "test-run-full-001"
        
        steps = ["01_ingest", "02_preprocess", "03_generate", "04_postprocess", "05_package"]
        
        for step in steps:
            orchestrator = StepOrchestrator(step, run_id, story_id)
            
            # Run step
            result = orchestrator.run_step()
            assert result is True, f"Step {step} failed"
            
            # Check acceptance
            passed = orchestrator.check_acceptance()
            assert passed is True, f"Step {step} acceptance failed"
            
            print(f"  ✓ {step} completed and passed acceptance")
        
        print("✓ Full pipeline flow test passed")
    
    def test_get_pending_stories_from_previous_step(self):
        """Test getting pending stories from previous step output."""
        # Create some ingest outputs
        ingest_dir = self.output_dir / "01_ingest"
        ingest_dir.mkdir(parents=True, exist_ok=True)
        
        for i in range(3):
            story_file = ingest_dir / f"PENDING-{i}.json"
            with open(story_file, "w") as f:
                json.dump({"story_id": f"PENDING-{i}"}, f)
        
        # Check that preprocess can find these
        orchestrator = StepOrchestrator("02_preprocess", "test-run-009")
        candidates = orchestrator._get_pending_stories()
        
        assert len(candidates) == 3
        assert "PENDING-0" in candidates
        assert "PENDING-1" in candidates
        assert "PENDING-2" in candidates
        
        print("✓ Get pending stories test passed")


def run_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Pipeline Orchestration Tests")
    print("=" * 60 + "\n")
    
    test_suite = TestStepOrchestrator()
    
    tests = [
        test_suite.test_orchestrator_initialization,
        test_suite.test_pick_one_candidate_creates_story,
        test_suite.test_run_ingest_step,
        test_suite.test_check_ingest_acceptance_pass,
        test_suite.test_check_ingest_acceptance_fail_short_content,
        test_suite.test_run_preprocess_step,
        test_suite.test_check_preprocess_acceptance,
        test_suite.test_run_generate_step,
        test_suite.test_full_pipeline_flow,
        test_suite.test_get_pending_stories_from_previous_step,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test_suite.setup_method()  # Reset for each test
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60 + "\n")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_tests())
