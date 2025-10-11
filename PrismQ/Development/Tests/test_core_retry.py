"""
Tests for core.retry module - retry logic and circuit breaker.
"""

import time
from unittest.mock import MagicMock, patch

import pytest

from PrismQ.Shared.errors import APIError, RateLimitError, TimeoutError
from PrismQ.Shared.retry import (
    CircuitBreaker,
    RetryContext,
    retry_api_call,
    retry_with_backoff,
    with_circuit_breaker,
)


class TestCircuitBreaker:
    """Test CircuitBreaker class."""

    def test_circuit_breaker_initial_state(self):
        """Test circuit breaker initial state."""
        cb = CircuitBreaker()
        assert cb.state == "CLOSED"
        assert cb.failure_count == 0
        assert cb.last_failure_time is None

    def test_circuit_breaker_success(self):
        """Test successful calls through circuit breaker."""
        cb = CircuitBreaker()
        
        def success_func():
            return "success"
        
        result = cb.call(success_func)
        assert result == "success"
        assert cb.state == "CLOSED"
        assert cb.failure_count == 0

    def test_circuit_breaker_opens_after_threshold(self):
        """Test circuit breaker opens after failure threshold."""
        cb = CircuitBreaker(failure_threshold=3, recovery_timeout=10)
        
        def failing_func():
            raise Exception("Test failure")
        
        # Trigger failures up to threshold
        for i in range(3):
            with pytest.raises(Exception):
                cb.call(failing_func)
        
        assert cb.state == "OPEN"
        assert cb.failure_count == 3

    def test_circuit_breaker_rejects_when_open(self):
        """Test circuit breaker rejects calls when open."""
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=10)
        
        def failing_func():
            raise Exception("Test failure")
        
        # Open the circuit
        for i in range(2):
            with pytest.raises(Exception):
                cb.call(failing_func)
        
        # Try another call - should be rejected immediately
        with pytest.raises(Exception) as exc_info:
            cb.call(failing_func)
        
        assert "Circuit breaker is OPEN" in str(exc_info.value)

    def test_circuit_breaker_half_open_after_timeout(self):
        """Test circuit breaker half-opens after recovery timeout."""
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1)
        
        def failing_func():
            raise Exception("Test failure")
        
        # Open the circuit
        for i in range(2):
            with pytest.raises(Exception):
                cb.call(failing_func)
        
        assert cb.state == "OPEN"
        
        # Wait for recovery timeout
        time.sleep(0.15)
        
        # Next call should half-open and then fail
        with pytest.raises(Exception):
            cb.call(failing_func)
        
        assert cb.state == "OPEN"  # Back to open after failure

    def test_circuit_breaker_recovery(self):
        """Test circuit breaker recovers after successful call."""
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1)
        call_count = [0]
        
        def sometimes_failing_func():
            call_count[0] += 1
            if call_count[0] <= 2:
                raise Exception("Test failure")
            return "success"
        
        # Open the circuit
        for i in range(2):
            with pytest.raises(Exception):
                cb.call(sometimes_failing_func)
        
        assert cb.state == "OPEN"
        
        # Wait for recovery timeout
        time.sleep(0.15)
        
        # Successful call should close circuit
        result = cb.call(sometimes_failing_func)
        assert result == "success"
        assert cb.state == "CLOSED"
        assert cb.failure_count == 0


class TestRetryWithBackoff:
    """Test retry_with_backoff decorator."""

    def test_retry_success_first_attempt(self):
        """Test function succeeds on first attempt."""
        call_count = [0]
        
        @retry_with_backoff(max_attempts=3)
        def success_func():
            call_count[0] += 1
            return "success"
        
        result = success_func()
        assert result == "success"
        assert call_count[0] == 1

    def test_retry_success_after_failures(self):
        """Test function succeeds after some failures."""
        call_count = [0]
        
        @retry_with_backoff(max_attempts=3, initial_delay=0.01)
        def sometimes_failing():
            call_count[0] += 1
            if call_count[0] < 3:
                raise APIError("Temporary failure")
            return "success"
        
        result = sometimes_failing()
        assert result == "success"
        assert call_count[0] == 3

    def test_retry_fails_after_max_attempts(self):
        """Test function fails after max attempts."""
        call_count = [0]
        
        @retry_with_backoff(max_attempts=3, initial_delay=0.01)
        def always_failing():
            call_count[0] += 1
            raise APIError("Always fails")
        
        with pytest.raises(APIError) as exc_info:
            always_failing()
        
        assert "Always fails" in str(exc_info.value)
        assert call_count[0] == 3

    def test_retry_exponential_backoff(self):
        """Test exponential backoff timing."""
        call_times = []
        
        @retry_with_backoff(
            max_attempts=3,
            initial_delay=0.1,
            exponential_base=2.0,
        )
        def failing_func():
            call_times.append(time.time())
            raise APIError("Test failure")
        
        with pytest.raises(APIError):
            failing_func()
        
        # Check that delays increase exponentially
        assert len(call_times) == 3
        delay1 = call_times[1] - call_times[0]
        delay2 = call_times[2] - call_times[1]
        
        # Second delay should be roughly 2x first delay
        assert delay2 > delay1
        assert delay2 >= 0.2  # Should be at least 0.2s (0.1 * 2^1)

    def test_retry_respects_rate_limit(self):
        """Test retry respects rate limit retry_after."""
        call_times = []
        
        @retry_with_backoff(max_attempts=2, initial_delay=0.05)
        def rate_limited_func():
            call_times.append(time.time())
            raise RateLimitError("Rate limited", retry_after=0.2)
        
        with pytest.raises(RateLimitError):
            rate_limited_func()
        
        assert len(call_times) == 2
        delay = call_times[1] - call_times[0]
        # Should use retry_after (0.2) instead of initial_delay (0.05)
        assert delay >= 0.2

    def test_retry_only_specific_exceptions(self):
        """Test retry only retries specific exceptions."""
        call_count = [0]
        
        @retry_with_backoff(
            max_attempts=3,
            initial_delay=0.01,
            exceptions=(APIError,),
        )
        def mixed_failures():
            call_count[0] += 1
            if call_count[0] == 1:
                raise APIError("Retry this")
            raise ValueError("Don't retry this")
        
        with pytest.raises(ValueError):
            mixed_failures()
        
        assert call_count[0] == 2  # APIError was retried, ValueError was not

    def test_retry_on_retry_callback(self):
        """Test on_retry callback is called."""
        callback_calls = []
        
        def on_retry_callback(exc, attempt):
            callback_calls.append((str(exc), attempt))
        
        @retry_with_backoff(
            max_attempts=3,
            initial_delay=0.01,
            on_retry=on_retry_callback,
        )
        def failing_func():
            raise APIError("Test failure")
        
        with pytest.raises(APIError):
            failing_func()
        
        assert len(callback_calls) == 2  # Called before each retry (not on last)
        assert callback_calls[0][1] == 1
        assert callback_calls[1][1] == 2


class TestWithCircuitBreaker:
    """Test with_circuit_breaker decorator."""

    def test_circuit_breaker_decorator_success(self):
        """Test circuit breaker decorator with successful calls."""
        
        @with_circuit_breaker(failure_threshold=2)
        def success_func():
            return "success"
        
        result = success_func()
        assert result == "success"

    def test_circuit_breaker_decorator_opens(self):
        """Test circuit breaker decorator opens after failures."""
        
        @with_circuit_breaker(failure_threshold=2, recovery_timeout=10)
        def failing_func():
            raise APIError("Test failure")
        
        # Trigger failures to open circuit
        for i in range(2):
            with pytest.raises(APIError):
                failing_func()
        
        # Next call should be rejected by circuit breaker
        with pytest.raises(Exception) as exc_info:
            failing_func()
        
        assert "Circuit breaker is OPEN" in str(exc_info.value)


class TestRetryAPICall:
    """Test retry_api_call convenience decorator."""

    def test_retry_api_call_success(self):
        """Test retry_api_call with successful call."""
        
        @retry_api_call(max_attempts=3)
        def api_call():
            return {"status": "success"}
        
        result = api_call()
        assert result["status"] == "success"

    def test_retry_api_call_retries_api_errors(self):
        """Test retry_api_call retries API errors."""
        call_count = [0]
        
        @retry_api_call(max_attempts=3, initial_delay=0.01)
        def failing_api_call():
            call_count[0] += 1
            if call_count[0] < 3:
                raise APIError("Temporary failure")
            return {"status": "success"}
        
        result = failing_api_call()
        assert result["status"] == "success"
        assert call_count[0] == 3


class TestRetryContext:
    """Test RetryContext context manager."""

    def test_retry_context_success_first_attempt(self):
        """Test retry context with successful first attempt."""
        attempt_count = 0
        
        while True:
            with RetryContext(max_attempts=3) as retry:
                attempt_count += 1
                result = "success"
                break
        
        assert result == "success"
        assert attempt_count == 1

    def test_retry_context_success_after_retries(self):
        """Test retry context succeeds after retries."""
        attempt_count = 0
        
        while True:
            with RetryContext(max_attempts=3, initial_delay=0.01) as retry:
                attempt_count += 1
                if attempt_count < 3:
                    retry.should_retry()
                    continue
                result = "success"
                break
        
        assert result == "success"
        assert attempt_count == 3

    def test_retry_context_max_attempts(self):
        """Test retry context respects max attempts."""
        attempt_count = 0
        
        while True:
            with RetryContext(max_attempts=3, initial_delay=0.01) as retry:
                attempt_count += 1
                if retry.attempt < 3:
                    retry.should_retry()
                    continue
                break
        
        assert attempt_count == 3
