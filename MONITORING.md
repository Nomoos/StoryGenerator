# Performance Monitoring, Retry Logic, and Validation

This document describes the new robustness features added to the StoryGenerator project in Step 5.

## Overview

Three new modules have been added to improve reliability, observability, and quality control:

1. **Monitor.py** - Performance monitoring and logging
2. **Retry.py** - Retry logic with exponential backoff and circuit breaker pattern
3. **Validator.py** - Output quality validation

## Features

### 1. Performance Monitoring (`Tools/Monitor.py`)

Tracks execution times, errors, and output quality metrics for all operations.

#### Key Features:
- **Automatic Timing**: Measures duration of all major operations (TTS, alignment, rendering, etc.)
- **Persistent Logging**: Saves logs to timestamped files in `logs/` directory
- **Metrics Storage**: Stores operation metrics in JSON format for analysis
- **Console & File Output**: Logs to both console and file for easy debugging

#### Usage:

```python
from Tools.Monitor import PerformanceMonitor, log_info, log_error, time_operation

# Manual logging
PerformanceMonitor.log_operation(
    operation="TTS_Generation",
    story_title="My Story",
    duration=12.5,
    success=True,
    error=None,
    metrics={"audio_duration": 30.2, "file_size_mb": 2.5}
)

# Or use the decorator
@time_operation("Script_Generation")
def generate_script(story_idea):
    # Your code here
    pass

# Simple logging
log_info("Script generation started")
log_error("Script Generation", "Story Title", Exception("Error message"))
```

#### View Metrics:

```bash
python Tools/view_metrics.py
```

This displays a summary of:
- Total operations
- Success/failure rates
- Average execution times per operation type
- Failure counts

### 2. Retry Logic (`Tools/Retry.py`)

Implements robust retry mechanisms for external API calls with exponential backoff and circuit breaker pattern.

#### Key Features:
- **Exponential Backoff**: Gradually increases wait time between retries
- **Jitter**: Adds randomness to prevent thundering herd
- **Circuit Breaker**: Prevents cascading failures by temporarily blocking calls after repeated failures
- **Configurable**: Customizable retry counts, delays, and exceptions

#### Usage:

```python
from Tools.Retry import retry_with_exponential_backoff, with_circuit_breaker

# Retry decorator
@retry_with_exponential_backoff(
    max_retries=3,
    base_delay=2.0,
    max_delay=30.0,
    exceptions=(Exception,)
)
def call_external_api():
    # API call that might fail
    pass

# Circuit breaker decorator
@with_circuit_breaker("openai")
def call_openai_api():
    # OpenAI API call
    pass

# Combined (recommended for external APIs)
@retry_with_exponential_backoff(max_retries=3)
@with_circuit_breaker("openai")
def generate_text(prompt):
    return openai.ChatCompletion.create(...)
```

#### Circuit Breaker States:
- **CLOSED**: Normal operation, all calls go through
- **OPEN**: Too many failures, all calls are blocked for a timeout period
- **HALF-OPEN**: After timeout, one test call is allowed to check if service recovered

### 3. Output Validation (`Tools/Validator.py`)

Validates generated files to ensure quality and completeness.

#### Key Features:
- **Audio Validation**: Checks file size, duration, bitrate
- **Text Validation**: Checks character count, word count, line count
- **Video Validation**: Checks video/audio streams, resolution, codec
- **Subtitle Sync Validation**: Verifies subtitle timestamps align with audio duration

#### Usage:

```python
from Tools.Validator import OutputValidator

# Validate audio file
is_valid, metrics = OutputValidator.validate_audio_file("voiceover.mp3")
if is_valid:
    print(f"Audio valid: {metrics['duration_seconds']}s, {metrics['size_mb']}MB")
else:
    print("Audio validation failed")

# Validate text file
is_valid, metrics = OutputValidator.validate_text_file("script.txt", min_length=200)
print(f"Word count: {metrics['word_count']}")

# Validate video file
is_valid, metrics = OutputValidator.validate_video_file("output.mp4")
print(f"Resolution: {metrics['width']}x{metrics['height']}")

# Validate subtitle synchronization
is_valid, metrics = OutputValidator.validate_subtitle_sync(
    audio_duration=30.5,
    subtitle_file="subtitles.srt"
)
print(f"Subtitle coverage: {metrics['coverage_percent']}%")
```

## Integration

All generator classes have been updated to use these new features:

### GVoice.py
- ✅ TTS generation with retry logic
- ✅ Circuit breaker for ElevenLabs API
- ✅ Performance timing for TTS and normalization
- ✅ Audio file validation

### GTitles.py
- ✅ Transcription with retry logic
- ✅ Performance timing for transcription and alignment
- ✅ Subtitle file validation

### GStoryIdeas.py
- ✅ OpenAI calls with retry logic and circuit breaker
- ✅ Performance timing for idea generation
- ✅ Error logging for parsing failures

### GScript.py
- ✅ Script generation with retry logic and circuit breaker
- ✅ Performance timing and metrics
- ✅ Script file validation

### GRevise.py
- ✅ Script revision with retry logic and circuit breaker
- ✅ Performance timing and metrics
- ✅ Revised script validation

### Utils.py (convert_to_mp4)
- ✅ Performance timing for video rendering
- ✅ Video file validation
- ✅ Detailed error logging

## Metrics Collected

The system now tracks:

### Performance Metrics:
- Operation duration (seconds)
- TTS generation time
- Transcription time
- Alignment time
- Normalization time
- Rendering time

### Quality Metrics:
- Audio file size (MB)
- Audio duration (seconds)
- Audio bitrate
- Script length (characters, words)
- Subtitle count and coverage
- Video resolution and codecs

### Reliability Metrics:
- Success/failure counts
- Error messages
- Retry attempts
- Circuit breaker state changes

## Log Files

Logs are stored in the `logs/` directory (excluded from git):

- `storygen_YYYYMMDD.log` - Daily log files with all operations
- `metrics.json` - Structured metrics for analysis

## Benefits

1. **Better Observability**: See exactly what's happening and where time is spent
2. **Improved Reliability**: Automatic retries prevent transient failures
3. **Quality Assurance**: Validation catches invalid outputs early
4. **Debugging**: Detailed logs help troubleshoot issues
5. **Performance Analysis**: Identify bottlenecks and optimization opportunities
6. **Failure Protection**: Circuit breaker prevents cascading failures

## Best Practices

1. **Always validate outputs**: Use validators after generating files
2. **Check metrics regularly**: Run `python Tools/view_metrics.py` to spot issues
3. **Monitor circuit breakers**: If a circuit opens frequently, investigate the underlying service
4. **Tune retry settings**: Adjust `max_retries` and delays based on your use case
5. **Archive old logs**: Keep the `logs/` directory clean by archiving old files

## Future Enhancements

Potential improvements:
- Real-time monitoring dashboard
- Alerting for high failure rates
- Performance regression detection
- Automated quality reports
- Integration with monitoring services (Prometheus, Grafana, etc.)

## Troubleshooting

### High Failure Rate
- Check internet connection
- Verify API keys are valid
- Check if external services are down
- Review error logs for patterns

### Slow Performance
- Check `metrics.json` to identify bottlenecks
- Consider parallelizing independent operations
- Optimize GPU usage for WhisperX
- Use caching where appropriate

### Circuit Breaker Opens Frequently
- Increase `failure_threshold` if service is flaky
- Increase `timeout` to give service more recovery time
- Investigate root cause of failures in the external service
