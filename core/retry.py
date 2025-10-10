"""
Retry logic with exponential backoff and circuit breaker patterns.

This module provides decorators and utilities for handling transient failures
in API calls and external services.
"""

import functools
import time
from typing import Any, Callable, Optional, Tuple, Type, Union

from core.errors import APIError, RateLimitError, TimeoutError
from core.logging import get_logger

logger = get_logger(__name__)


class CircuitBreaker:
    """Circuit breaker pattern implementation.
    
    Prevents repeated calls to a failing service by "opening" the circuit
    after a threshold of failures. After a timeout period, the circuit
    "half-opens" to test if the service has recovered.
    
    States:
    - CLOSED: Normal operation, calls pass through
    - OPEN: Service is failing, calls fail immediately
    - HALF_OPEN: Testing if service has recovered
    
    Attributes:
        failure_threshold: Number of failures before opening circuit
        recovery_timeout: Seconds to wait before half-opening
        expected_exception: Exception type(s) that count as failures
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception,
    ):
        """Initialize CircuitBreaker.
        
        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Seconds to wait before half-opening
            expected_exception: Exception type(s) that count as failures
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def call(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """Execute function with circuit breaker protection.
        
        Args:
            func: Function to call
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func
            
        Returns:
            Result of func call
            
        Raises:
            Exception: If circuit is OPEN or func raises
        """
        if self.state == "OPEN":
            if self._should_attempt_reset():
                self.state = "HALF_OPEN"
                logger.info(f"Circuit breaker half-open for {func.__name__}")
            else:
                raise Exception(
                    f"Circuit breaker is OPEN for {func.__name__}. "
                    f"Will retry after {self.recovery_timeout}s"
                )

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if self.last_failure_time is None:
            return False
        return time.time() - self.last_failure_time >= self.recovery_timeout

    def _on_success(self) -> None:
        """Handle successful call."""
        if self.state == "HALF_OPEN":
            logger.info("Circuit breaker recovered, closing circuit")
        self.failure_count = 0
        self.state = "CLOSED"

    def _on_failure(self) -> None:
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            logger.warning(
                f"Circuit breaker opened after {self.failure_count} failures. "
                f"Will retry after {self.recovery_timeout}s"
            )


def retry_with_backoff(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (APIError,),
    on_retry: Optional[Callable[[Exception, int], None]] = None,
) -> Callable:
    """Decorator for retrying functions with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential backoff calculation
        exceptions: Tuple of exception types to retry on
        on_retry: Optional callback called on each retry (exc, attempt)
        
    Returns:
        Decorator function
        
    Example:
        @retry_with_backoff(max_attempts=5, initial_delay=2.0)
        def call_api():
            response = requests.get("https://api.example.com")
            return response.json()
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_attempts:
                        logger.error(
                            f"Failed after {max_attempts} attempts: {func.__name__}",
                            extra={"error": str(e), "attempts": attempt},
                        )
                        raise
                    
                    # Calculate delay with exponential backoff
                    delay = min(
                        initial_delay * (exponential_base ** (attempt - 1)),
                        max_delay,
                    )
                    
                    # Handle rate limit retry_after if available
                    if isinstance(e, RateLimitError) and e.retry_after:
                        delay = max(delay, e.retry_after)
                    
                    logger.warning(
                        f"Attempt {attempt}/{max_attempts} failed for {func.__name__}, "
                        f"retrying in {delay:.1f}s",
                        extra={"error": str(e), "delay": delay, "attempt": attempt},
                    )
                    
                    if on_retry:
                        on_retry(e, attempt)
                    
                    time.sleep(delay)
            
            # This should never be reached, but just in case
            if last_exception:
                raise last_exception
            raise Exception("Unexpected state in retry logic")
        
        return wrapper
    
    return decorator


def with_circuit_breaker(
    failure_threshold: int = 5,
    recovery_timeout: int = 60,
    expected_exception: Union[Type[Exception], Tuple[Type[Exception], ...]] = APIError,
) -> Callable:
    """Decorator for applying circuit breaker pattern.
    
    Args:
        failure_threshold: Number of failures before opening circuit
        recovery_timeout: Seconds to wait before half-opening
        expected_exception: Exception type(s) that count as failures
        
    Returns:
        Decorator function
        
    Example:
        @with_circuit_breaker(failure_threshold=3)
        def call_external_service():
            response = requests.get("https://service.example.com")
            return response.json()
    """
    # Create circuit breaker instance (shared across calls)
    circuit_breaker = CircuitBreaker(
        failure_threshold=failure_threshold,
        recovery_timeout=recovery_timeout,
        expected_exception=expected_exception,
    )
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return circuit_breaker.call(func, *args, **kwargs)
        
        return wrapper
    
    return decorator


def retry_api_call(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 10.0,
) -> Callable:
    """Convenience decorator for API calls with standard retry logic.
    
    Combines retry with backoff for common API error scenarios.
    Retries on APIError, RateLimitError, and TimeoutError.
    
    Args:
        max_attempts: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        
    Returns:
        Decorator function
        
    Example:
        @retry_api_call(max_attempts=5)
        def get_openai_completion(prompt: str):
            from providers import OpenAIProvider
            provider = OpenAIProvider()
            response = provider.generate_completion(prompt)
            return response
    """
    return retry_with_backoff(
        max_attempts=max_attempts,
        initial_delay=initial_delay,
        max_delay=max_delay,
        exponential_base=2.0,
        exceptions=(APIError, RateLimitError, TimeoutError),
    )


class RetryContext:
    """Context manager for retry logic.
    
    Provides a more flexible way to handle retries when decorators
    aren't suitable.
    
    Example:
        with RetryContext(max_attempts=3) as retry:
            response = requests.get("https://api.example.com")
            if not response.ok:
                retry.should_retry()  # Will retry
    """

    def __init__(
        self,
        max_attempts: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
    ):
        """Initialize RetryContext.
        
        Args:
            max_attempts: Maximum number of retry attempts
            initial_delay: Initial delay in seconds
            max_delay: Maximum delay in seconds
            exponential_base: Base for exponential backoff
        """
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.attempt = 0
        self._should_retry = False

    def __enter__(self) -> "RetryContext":
        """Enter retry context."""
        self.attempt = 1
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        """Exit retry context."""
        if exc_type is None and not self._should_retry:
            return False  # Success, no retry needed
        
        if self.attempt >= self.max_attempts:
            return False  # Max attempts reached, propagate exception
        
        # Calculate delay and sleep
        delay = min(
            self.initial_delay * (self.exponential_base ** (self.attempt - 1)),
            self.max_delay,
        )
        
        logger.warning(
            f"Retry attempt {self.attempt}/{self.max_attempts}, "
            f"waiting {delay:.1f}s",
            extra={"attempt": self.attempt, "delay": delay},
        )
        
        time.sleep(delay)
        self.attempt += 1
        self._should_retry = False
        
        # Don't propagate exception, will retry
        return True

    def should_retry(self) -> None:
        """Mark that operation should be retried."""
        self._should_retry = True
