"""
Storage Provider Interface.

This module defines the abstract interface for storage providers,
enabling easy swapping between different storage implementations (file system, S3, etc.).
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO, Optional


class IStorageProvider(ABC):
    """
    Abstract interface for storage providers.

    This interface defines the contract that all storage providers must implement,
    allowing for easy swapping between file system, cloud storage, or other providers.

    Example:
        >>> class MyStorageProvider(IStorageProvider):
        ...     def save(self, path: str, data: bytes) -> bool:
        ...         # Implementation here
        ...         pass
    """

    @abstractmethod
    def save(self, path: str, data: bytes) -> bool:
        """
        Save data to storage.

        Args:
            path: Path where to save the data
            data: Binary data to save

        Returns:
            True if save was successful, False otherwise

        Raises:
            Exception: If save fails
        """
        pass

    @abstractmethod
    def load(self, path: str) -> bytes:
        """
        Load data from storage.

        Args:
            path: Path to load data from

        Returns:
            Binary data

        Raises:
            FileNotFoundError: If file doesn't exist
            Exception: If load fails
        """
        pass

    @abstractmethod
    def exists(self, path: str) -> bool:
        """
        Check if file exists in storage.

        Args:
            path: Path to check

        Returns:
            True if file exists, False otherwise
        """
        pass

    @abstractmethod
    def delete(self, path: str) -> bool:
        """
        Delete file from storage.

        Args:
            path: Path to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        pass

    @abstractmethod
    def list_files(self, directory: str, pattern: str = "*") -> list[str]:
        """
        List files in directory.

        Args:
            directory: Directory to list
            pattern: File pattern to match (default: "*")

        Returns:
            List of file paths
        """
        pass


class IFileSystemProvider(IStorageProvider):
    """
    Extended interface for file system operations.

    Adds additional methods specific to file system operations like
    creating directories, getting file info, etc.
    """

    @abstractmethod
    def create_directory(self, path: str) -> bool:
        """
        Create directory if it doesn't exist.

        Args:
            path: Directory path to create

        Returns:
            True if directory was created or already exists
        """
        pass

    @abstractmethod
    def get_file_size(self, path: str) -> int:
        """
        Get file size in bytes.

        Args:
            path: Path to file

        Returns:
            File size in bytes

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        pass

    @abstractmethod
    def get_modified_time(self, path: str) -> float:
        """
        Get file modification time.

        Args:
            path: Path to file

        Returns:
            Modification time as Unix timestamp

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        pass
