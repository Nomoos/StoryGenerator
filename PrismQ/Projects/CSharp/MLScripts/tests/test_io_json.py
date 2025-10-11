"""
Tests for common.io_json module.

Tests the JSONL protocol for subprocess communication between C# and Python.
"""

import json
import io
import sys
from unittest.mock import patch

import pytest

# Add parent directory to path to import common module
sys.path.insert(0, '..')

from common.io_json import (
    read_request,
    write_response,
    write_error_response,
)


class TestReadRequest:
    """Tests for read_request function."""
    
    def test_read_valid_json(self):
        """Test reading a valid JSON request."""
        mock_input = '{"id": "123", "op": "test", "args": {}}\n'
        with patch('sys.stdin', io.StringIO(mock_input)):
            result = read_request()
            assert result == {"id": "123", "op": "test", "args": {}}
    
    def test_read_empty_line_returns_none(self):
        """Test reading an empty line returns None."""
        with patch('sys.stdin', io.StringIO('')):
            result = read_request()
            assert result is None
    
    def test_read_invalid_json_writes_error(self):
        """Test reading invalid JSON writes an error response."""
        mock_input = '{invalid json}\n'
        mock_stdout = io.StringIO()
        
        with patch('sys.stdin', io.StringIO(mock_input)):
            with patch('sys.stdout', mock_stdout):
                result = read_request()
                assert result is None
                
                # Check error response was written
                output = mock_stdout.getvalue()
                response = json.loads(output.strip())
                assert response["ok"] is False
                assert "Invalid JSON" in response["error"]


class TestWriteResponse:
    """Tests for write_response function."""
    
    def test_write_success_response(self):
        """Test writing a successful response."""
        mock_stdout = io.StringIO()
        with patch('sys.stdout', mock_stdout):
            write_response("123", {"result": "success"})
            
            output = mock_stdout.getvalue()
            response = json.loads(output.strip())
            
            assert response["id"] == "123"
            assert response["ok"] is True
            assert response["data"] == {"result": "success"}
            assert response["error"] is None
    
    def test_write_error_response(self):
        """Test writing an error response."""
        mock_stdout = io.StringIO()
        with patch('sys.stdout', mock_stdout):
            write_response("456", None, "Something went wrong")
            
            output = mock_stdout.getvalue()
            response = json.loads(output.strip())
            
            assert response["id"] == "456"
            assert response["ok"] is False
            assert response["data"] is None
            assert response["error"] == "Something went wrong"


class TestWriteErrorResponse:
    """Tests for write_error_response function."""
    
    def test_write_error_response(self):
        """Test writing an error response."""
        mock_stdout = io.StringIO()
        with patch('sys.stdout', mock_stdout):
            write_error_response("789", "Test error message")
            
            output = mock_stdout.getvalue()
            response = json.loads(output.strip())
            
            assert response["id"] == "789"
            assert response["ok"] is False
            assert response["data"] is None
            assert response["error"] == "Test error message"


class TestJsonlProtocol:
    """Integration tests for JSONL protocol."""
    
    def test_echo_roundtrip(self):
        """Test echo operation roundtrip."""
        request = {"id": "echo-1", "op": "echo", "args": {"message": "hello"}}
        mock_input = json.dumps(request) + '\n'
        mock_stdout = io.StringIO()
        
        with patch('sys.stdin', io.StringIO(mock_input)):
            with patch('sys.stdout', mock_stdout):
                req = read_request()
                assert req is not None
                
                # Simulate handler
                result = req["args"]
                write_response(req["id"], result)
                
                output = mock_stdout.getvalue()
                response = json.loads(output.strip())
                
                assert response["id"] == "echo-1"
                assert response["ok"] is True
                assert response["data"] == {"message": "hello"}
