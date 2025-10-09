"""
Shared pytest fixtures and configuration.

This file is automatically loaded by pytest and provides fixtures
that are available to all test modules.
"""

import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Provide a temporary directory that is cleaned up after the test.

    Yields:
        Path: Path to temporary directory

    Example:
        def test_file_creation(temp_dir):
            file_path = temp_dir / "test.txt"
            file_path.write_text("content")
            assert file_path.exists()
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def sample_json_file(temp_dir: Path) -> Path:
    """Create a sample JSON file for testing.

    Args:
        temp_dir: Temporary directory fixture

    Returns:
        Path: Path to the created JSON file

    Example:
        def test_json_parsing(sample_json_file):
            with open(sample_json_file) as f:
                data = json.load(f)
            assert data["test"] == "value"
    """
    import json

    file_path = temp_dir / "sample.json"
    data = {"test": "value", "number": 42, "array": [1, 2, 3]}
    file_path.write_text(json.dumps(data, indent=2))
    return file_path


@pytest.fixture
def sample_text_file(temp_dir: Path) -> Path:
    """Create a sample text file for testing.

    Args:
        temp_dir: Temporary directory fixture

    Returns:
        Path: Path to the created text file

    Example:
        def test_text_processing(sample_text_file):
            content = sample_text_file.read_text()
            assert "sample" in content
    """
    file_path = temp_dir / "sample.txt"
    file_path.write_text("This is a sample text file.\nWith multiple lines.\n")
    return file_path


@pytest.fixture
def mock_environment_variables(monkeypatch) -> dict:
    """Set up mock environment variables for testing.

    Args:
        monkeypatch: pytest's monkeypatch fixture

    Returns:
        dict: Dictionary of set environment variables

    Example:
        def test_with_env_vars(mock_environment_variables):
            assert os.getenv("TEST_VAR") == "test_value"
    """
    env_vars = {
        "TEST_VAR": "test_value",
        "DEBUG": "true",
    }
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    return env_vars


@pytest.fixture
def captured_logs(caplog):
    """Fixture for capturing and analyzing log output.

    Args:
        caplog: pytest's caplog fixture

    Returns:
        LogCaptureFixture: The caplog fixture

    Example:
        def test_logging(captured_logs):
            logger.info("Test message")
            assert "Test message" in captured_logs.text
    """
    return caplog


@pytest.fixture
def mock_openai_client(mocker):
    """Mock OpenAI client for testing.

    Returns:
        Mock: Mocked OpenAI client

    Example:
        def test_with_openai(mock_openai_client):
            mock_openai_client.chat.completions.create.return_value = mock_response
    """
    mock_client = mocker.MagicMock()
    mock_response = mocker.MagicMock()
    mock_response.choices = [mocker.MagicMock()]
    mock_response.choices[0].message.content = "Test response"
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client


@pytest.fixture
def mock_elevenlabs_client(mocker):
    """Mock ElevenLabs client for testing.

    Returns:
        Mock: Mocked ElevenLabs client

    Example:
        def test_with_elevenlabs(mock_elevenlabs_client):
            mock_elevenlabs_client.generate.return_value = b"audio_data"
    """
    mock_client = mocker.MagicMock()
    mock_client.generate.return_value = b"mock_audio_data"
    return mock_client


@pytest.fixture
def isolated_config(tmp_path, monkeypatch):
    """Provide isolated configuration for testing.

    Creates temporary directories and sets environment variables
    to avoid interfering with actual configuration.

    Returns:
        dict: Dictionary with temporary paths

    Example:
        def test_with_config(isolated_config):
            assert isolated_config['story_root'].exists()
    """
    story_root = tmp_path / "stories"
    log_dir = tmp_path / "logs"
    cache_dir = tmp_path / "cache"

    # Set environment variables
    monkeypatch.setenv("STORY_ROOT", str(story_root))
    monkeypatch.setenv("LOG_DIR", str(log_dir))
    monkeypatch.setenv("CACHE_DIR", str(cache_dir))
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("ELEVENLABS_API_KEY", "test-key")

    return {
        "story_root": story_root,
        "log_dir": log_dir,
        "cache_dir": cache_dir,
    }


# Markers for test categorization
def pytest_configure(config):
    """Register custom markers for test categorization."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "requires_api: mark test as requiring API access")
    config.addinivalue_line("markers", "requires_gpu: mark test as requiring GPU")


# Hooks for test reporting
def pytest_collection_modifyitems(config, items):
    """Automatically mark tests based on their location/name."""
    for item in items:
        # Auto-mark integration tests
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)

        # Auto-mark tests in test_slow_* files as slow
        if "test_slow_" in item.nodeid:
            item.add_marker(pytest.mark.slow)
