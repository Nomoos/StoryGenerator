"""
Pipeline Stage Interface.

This module defines the abstract interface for pipeline stages,
enabling independent development and testing of each stage in the content creation pipeline.
Each stage has clear input/output contracts and can be developed in isolation.
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class StageStatus(Enum):
    """Status of a pipeline stage execution."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class StageMetadata:
    """
    Metadata for pipeline stage execution.
    
    Attributes:
        stage_name: Name of the pipeline stage
        stage_id: Unique identifier for this stage
        version: Version of the stage implementation
        executed_at: Timestamp of execution
        execution_time_ms: Execution time in milliseconds
        status: Current status of the stage
        error_message: Error message if status is FAILED
    """
    stage_name: str
    stage_id: str
    version: str
    executed_at: datetime
    execution_time_ms: float
    status: StageStatus
    error_message: str | None = None


# Type variables for input and output types
TInput = TypeVar('TInput')
TOutput = TypeVar('TOutput')


@dataclass
class StageResult(Generic[TOutput]):
    """
    Result from a pipeline stage execution.
    
    Attributes:
        data: The output data from the stage
        metadata: Metadata about the execution
    """
    data: TOutput
    metadata: StageMetadata


class IPipelineStage(ABC, Generic[TInput, TOutput]):
    """
    Abstract interface for pipeline stages.
    
    Each pipeline stage is independently testable and replaceable.
    Stages follow Single Responsibility Principle - each stage does one thing.
    
    Type Parameters:
        TInput: Type of input data the stage accepts
        TOutput: Type of output data the stage produces
    
    Example:
        >>> class IdeaGenerationStage(IPipelineStage[IdeaGenerationInput, IdeaGenerationOutput]):
        ...     @property
        ...     def stage_name(self) -> str:
        ...         return "IdeaGeneration"
        ...     
        ...     @property
        ...     def stage_version(self) -> str:
        ...         return "1.0.0"
        ...     
        ...     async def execute(self, input_data: IdeaGenerationInput) -> StageResult[IdeaGenerationOutput]:
        ...         # Implementation here
        ...         pass
        ...     
        ...     async def validate_input(self, input_data: IdeaGenerationInput) -> bool:
        ...         # Validation logic
        ...         return True
    """
    
    @property
    @abstractmethod
    def stage_name(self) -> str:
        """
        Get the name of the pipeline stage.
        
        Returns:
            Name of the stage (e.g., "IdeaGeneration", "TextGeneration")
        """
        pass
    
    @property
    @abstractmethod
    def stage_id(self) -> str:
        """
        Get the unique identifier of the pipeline stage.
        
        Returns:
            Unique identifier (e.g., "01_idea_generation", "02_text_generation")
        """
        pass
    
    @property
    @abstractmethod
    def stage_version(self) -> str:
        """
        Get the version of the stage implementation.
        
        Returns:
            Semantic version string (e.g., "1.0.0")
        """
        pass
    
    @abstractmethod
    async def execute(self, input_data: TInput) -> StageResult[TOutput]:
        """
        Execute the pipeline stage.
        
        Args:
            input_data: Input data for the stage
        
        Returns:
            StageResult containing output data and metadata
        
        Raises:
            ValidationError: If input validation fails
            StageExecutionError: If stage execution fails
        """
        pass
    
    @abstractmethod
    async def validate_input(self, input_data: TInput) -> bool:
        """
        Validate input before execution.
        
        Args:
            input_data: Input to validate
        
        Returns:
            True if input is valid, False otherwise
        
        Raises:
            ValidationError: If validation fails with detailed error message
        """
        pass
    
    def get_input_schema(self) -> dict[str, Any]:
        """
        Get the JSON schema for input data.
        
        Returns:
            JSON schema dictionary describing expected input format
        """
        return {}
    
    def get_output_schema(self) -> dict[str, Any]:
        """
        Get the JSON schema for output data.
        
        Returns:
            JSON schema dictionary describing output format
        """
        return {}


class BasePipelineStage(IPipelineStage[TInput, TOutput]):
    """
    Base implementation of IPipelineStage with common functionality.
    
    Provides default implementations for common pipeline stage operations.
    Stages can extend this class to reduce boilerplate code.
    """
    
    def __init__(self, stage_name: str, stage_id: str, version: str = "1.0.0"):
        """
        Initialize the base pipeline stage.
        
        Args:
            stage_name: Name of the stage
            stage_id: Unique identifier for the stage
            version: Version of the stage implementation
        """
        self._stage_name = stage_name
        self._stage_id = stage_id
        self._version = version
    
    @property
    def stage_name(self) -> str:
        """Get the stage name."""
        return self._stage_name
    
    @property
    def stage_id(self) -> str:
        """Get the stage ID."""
        return self._stage_id
    
    @property
    def stage_version(self) -> str:
        """Get the stage version."""
        return self._version
    
    async def execute(self, input_data: TInput) -> StageResult[TOutput]:
        """
        Execute the pipeline stage with error handling and timing.
        
        Args:
            input_data: Input data for the stage
        
        Returns:
            StageResult containing output data and metadata
        """
        import time
        
        # Validate input
        if not await self.validate_input(input_data):
            raise ValueError(f"Invalid input for stage {self.stage_name}")
        
        # Track execution time
        start_time = time.time()
        executed_at = datetime.now()
        
        try:
            # Execute the stage-specific logic
            output_data = await self._execute_impl(input_data)
            
            execution_time_ms = (time.time() - start_time) * 1000
            
            metadata = StageMetadata(
                stage_name=self.stage_name,
                stage_id=self.stage_id,
                version=self.stage_version,
                executed_at=executed_at,
                execution_time_ms=execution_time_ms,
                status=StageStatus.COMPLETED,
                error_message=None
            )
            
            return StageResult(data=output_data, metadata=metadata)
            
        except Exception as e:
            execution_time_ms = (time.time() - start_time) * 1000
            
            metadata = StageMetadata(
                stage_name=self.stage_name,
                stage_id=self.stage_id,
                version=self.stage_version,
                executed_at=executed_at,
                execution_time_ms=execution_time_ms,
                status=StageStatus.FAILED,
                error_message=str(e)
            )
            
            raise RuntimeError(f"Stage {self.stage_name} failed: {str(e)}") from e
    
    @abstractmethod
    async def _execute_impl(self, input_data: TInput) -> TOutput:
        """
        Implement the actual stage logic.
        
        This method should be overridden by subclasses to provide
        the stage-specific implementation.
        
        Args:
            input_data: Validated input data
        
        Returns:
            Output data from the stage
        """
        pass
    
    async def validate_input(self, input_data: TInput) -> bool:
        """
        Default input validation.
        
        Override this method to provide custom validation logic.
        
        Args:
            input_data: Input to validate
        
        Returns:
            True if input is valid
        """
        return input_data is not None
