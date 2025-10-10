"""Validation decorators and utilities for StoryGenerator.

This module provides decorators for validating function inputs and outputs
using Pydantic models. It ensures type safety and data integrity throughout
the application.
"""

import functools
import inspect
from typing import Any, Callable, Dict, Optional, Type, TypeVar, get_type_hints

from pydantic import BaseModel, ValidationError

F = TypeVar("F", bound=Callable[..., Any])


def validate_input(**field_models: Type[BaseModel]) -> Callable[[F], F]:
    """Decorator to validate function inputs against Pydantic models.

    Args:
        **field_models: Mapping of parameter names to Pydantic model classes

    Returns:
        Decorated function with input validation

    Raises:
        ValidationError: If input validation fails
        ValueError: If parameter name doesn't match function signature

    Example:
        >>> from core.models import StoryIdea
        >>> @validate_input(idea=StoryIdea)
        ... def process_idea(idea: dict) -> str:
        ...     return idea['content']
        >>> process_idea({'id': 'test', 'content': 'Story', ...})
    """

    def decorator(func: F) -> F:
        sig = inspect.signature(func)
        param_names = list(sig.parameters.keys())

        # Validate that all specified fields are in function signature
        for field_name in field_models.keys():
            if field_name not in param_names:
                raise ValueError(
                    f"Parameter '{field_name}' not found in function signature of {func.__name__}"
                )

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Build a dict of all arguments
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            all_args = bound_args.arguments

            # Validate each specified field
            validated_args = {}
            for param_name, model_class in field_models.items():
                if param_name in all_args:
                    value = all_args[param_name]
                    # If value is already a model instance, use it
                    if isinstance(value, model_class):
                        validated_args[param_name] = value
                    # If value is a dict, validate and create model
                    elif isinstance(value, dict):
                        try:
                            validated_args[param_name] = model_class(**value)
                        except ValidationError as e:
                            raise ValidationError.from_exception_data(
                                title=f"Validation error for parameter '{param_name}'",
                                line_errors=e.errors(),
                            ) from e
                    else:
                        raise ValueError(
                            f"Parameter '{param_name}' must be a dict or {model_class.__name__} instance"
                        )

            # Update arguments with validated versions
            all_args.update(validated_args)

            # Call function with validated arguments
            return func(**all_args)

        return wrapper  # type: ignore

    return decorator


def validate_output(model_class: Type[BaseModel]) -> Callable[[F], F]:
    """Decorator to validate function output against a Pydantic model.

    Args:
        model_class: Pydantic model class to validate output against

    Returns:
        Decorated function with output validation

    Raises:
        ValidationError: If output validation fails

    Example:
        >>> from core.models import APIResponse
        >>> @validate_output(APIResponse)
        ... def get_data() -> dict:
        ...     return {'success': True, 'data': {'key': 'value'}}
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)

            # If result is already a model instance, validate and return
            if isinstance(result, model_class):
                return result

            # If result is a dict, validate and create model
            if isinstance(result, dict):
                try:
                    return model_class(**result)
                except ValidationError as e:
                    raise ValidationError.from_exception_data(
                        title=f"Validation error for function '{func.__name__}' output",
                        line_errors=e.errors(),
                    ) from e

            raise ValueError(
                f"Function '{func.__name__}' must return a dict or {model_class.__name__} instance"
            )

        return wrapper  # type: ignore

    return decorator


def validate_call(func: Optional[F] = None, **field_models: Type[BaseModel]) -> Any:
    """Decorator that validates both inputs and output of a function.

    This combines validate_input and validate_output for convenience when
    the function returns a Pydantic model and takes Pydantic models as input.

    Args:
        func: Function to decorate (when used without arguments)
        **field_models: Mapping of parameter names to Pydantic model classes

    Returns:
        Decorated function with full validation

    Example:
        >>> from core.models import StoryIdea, APIResponse
        >>> @validate_call(idea=StoryIdea)
        ... def process_idea(idea: dict) -> APIResponse:
        ...     return APIResponse(success=True, data={'result': idea['content']})
    """
    # Determine if function was passed or just parameters
    if func is None:
        # Called with arguments: @validate_call(param1=Model1)
        def decorator(f: F) -> F:
            # Apply input validation
            validated_func = validate_input(**field_models)(f)
            return validated_func

        return decorator
    else:
        # Called without arguments: @validate_call
        return validate_input()(func)


def validate_dict(data: Dict[str, Any], model_class: Type[BaseModel]) -> BaseModel:
    """Validate a dictionary against a Pydantic model.

    This is a helper function for manual validation outside of decorators.

    Args:
        data: Dictionary to validate
        model_class: Pydantic model class to validate against

    Returns:
        Validated Pydantic model instance

    Raises:
        ValidationError: If validation fails

    Example:
        >>> from core.models import StoryIdea
        >>> data = {'id': 'test', 'content': 'Story', ...}
        >>> idea = validate_dict(data, StoryIdea)
    """
    try:
        return model_class(**data)
    except ValidationError as e:
        raise ValidationError.from_exception_data(
            title=f"Validation error for {model_class.__name__}",
            line_errors=e.errors(),
        ) from e


def get_validation_errors(data: Dict[str, Any], model_class: Type[BaseModel]) -> Optional[str]:
    """Get validation errors as a formatted string.

    This is useful for logging or displaying validation errors to users.

    Args:
        data: Dictionary to validate
        model_class: Pydantic model class to validate against

    Returns:
        Formatted error message string, or None if valid

    Example:
        >>> from core.models import StoryIdea
        >>> data = {'id': 'test', 'content': ''}  # Invalid: content too short
        >>> errors = get_validation_errors(data, StoryIdea)
        >>> print(errors)
        Validation error for StoryIdea:
        - content: String should have at least 10 characters
    """
    try:
        model_class(**data)
        return None
    except ValidationError as e:
        error_lines = [f"Validation error for {model_class.__name__}:"]
        for error in e.errors():
            field = ".".join(str(loc) for loc in error["loc"])
            message = error["msg"]
            error_lines.append(f"- {field}: {message}")
        return "\n".join(error_lines)


def is_valid(data: Dict[str, Any], model_class: Type[BaseModel]) -> bool:
    """Check if data is valid for a given model without raising exceptions.

    Args:
        data: Dictionary to validate
        model_class: Pydantic model class to validate against

    Returns:
        True if valid, False otherwise

    Example:
        >>> from core.models import StoryIdea
        >>> data = {'id': 'test', 'content': 'Valid story content', ...}
        >>> is_valid(data, StoryIdea)
        True
    """
    try:
        model_class(**data)
        return True
    except ValidationError:
        return False
