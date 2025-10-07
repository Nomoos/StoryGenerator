"""
Retry logic and fallback mechanisms for external API calls.
Implements exponential backoff with jitter.
"""

import time
import random
from typing import Callable, Any, Optional, Type
from functools import wraps
from Tools.Monitor import logger, log_error


def retry_with_exponential_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """
    Decorator that retries a function with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential calculation
        exceptions: Tuple of exceptions to catch and retry
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_retries:
                        logger.error(f"❌ {func.__name__} failed after {max_retries} retries: {e}")
                        raise
                    
                    # Calculate delay with exponential backoff and jitter
                    delay = min(
                        base_delay * (exponential_base ** attempt),
                        max_delay
                    )
                    # Add jitter (random value between 0 and 25% of delay)
                    jitter = random.uniform(0, delay * 0.25)
                    total_delay = delay + jitter
                    
                    logger.warning(
                        f"⚠️ {func.__name__} failed (attempt {attempt + 1}/{max_retries + 1}): {e}. "
                        f"Retrying in {total_delay:.2f}s..."
                    )
                    time.sleep(total_delay)
            
            # This should never be reached, but just in case
            raise last_exception
        
        return wrapper
    return decorator


class APIFallbackHandler:
    """Handle fallbacks for API failures."""
    
    @staticmethod
    def openai_fallback(func: Callable, *args, **kwargs) -> Optional[Any]:
        """
        Fallback handler for OpenAI API calls.
        Tries with a simpler model if the primary one fails.
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.warning(f"⚠️ Primary OpenAI call failed: {e}")
            
            # Try with a fallback model if model parameter exists
            if 'model' in kwargs:
                original_model = kwargs['model']
                fallback_models = {
                    'gpt-4o-mini': 'gpt-3.5-turbo',
                    'gpt-4o': 'gpt-4o-mini',
                    'gpt-4': 'gpt-3.5-turbo'
                }
                
                if original_model in fallback_models:
                    kwargs['model'] = fallback_models[original_model]
                    logger.info(f"🔄 Trying fallback model: {kwargs['model']}")
                    try:
                        return func(*args, **kwargs)
                    except Exception as fallback_error:
                        logger.error(f"❌ Fallback model also failed: {fallback_error}")
                        raise
            
            raise


class CircuitBreaker:
    """
    Circuit breaker pattern to prevent cascading failures.
    Opens after too many failures and prevents further calls.
    """
    
    def __init__(self, failure_threshold: int = 5, timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection."""
        
        # Check if circuit is open
        if self.state == "open":
            if time.time() - self.last_failure_time > self.timeout:
                logger.info("🔄 Circuit breaker entering half-open state")
                self.state = "half-open"
            else:
                raise Exception(f"Circuit breaker is OPEN. Service unavailable. Try again later.")
        
        try:
            result = func(*args, **kwargs)
            
            # Success - reset or close circuit
            if self.state == "half-open":
                logger.info("✅ Circuit breaker closed after successful call")
                self.state = "closed"
                self.failures = 0
            
            return result
            
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            
            if self.failures >= self.failure_threshold:
                logger.error(
                    f"🚨 Circuit breaker OPENED after {self.failures} failures. "
                    f"Service will be unavailable for {self.timeout}s"
                )
                self.state = "open"
            
            raise


# Global circuit breakers for different services
openai_circuit_breaker = CircuitBreaker(failure_threshold=5, timeout=60.0)
elevenlabs_circuit_breaker = CircuitBreaker(failure_threshold=5, timeout=60.0)


def with_circuit_breaker(service: str):
    """Decorator to use circuit breaker for a service."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if service == "openai":
                return openai_circuit_breaker.call(func, *args, **kwargs)
            elif service == "elevenlabs":
                return elevenlabs_circuit_breaker.call(func, *args, **kwargs)
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator
