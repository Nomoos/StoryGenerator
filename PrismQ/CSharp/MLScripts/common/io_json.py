"""
JSON I/O utilities for subprocess communication via JSONL protocol.

This module provides functionality to read and write JSON lines (JSONL)
for communication between C# orchestrator and Python ML scripts.

Protocol:
    Request:  {"id": "<uuid>", "op": "<command>", "args": {...}}
    Response: {"id": "<uuid>", "ok": true, "data": {...}, "error": null}
"""

import json
import sys
from typing import Any, Dict, Optional


def read_request() -> Optional[Dict[str, Any]]:
    """
    Read a single JSON request from stdin.
    
    Returns:
        Parsed JSON request dictionary, or None if EOF or invalid JSON.
    """
    try:
        line = sys.stdin.readline()
        if not line:
            return None
        return json.loads(line.strip())
    except json.JSONDecodeError as e:
        write_error_response("", f"Invalid JSON: {e}")
        return None


def write_response(request_id: str, data: Any, error: Optional[str] = None) -> None:
    """
    Write a JSON response to stdout.
    
    Args:
        request_id: The request ID from the incoming request
        data: Response data to send back
        error: Error message if operation failed
    """
    response = {
        "id": request_id,
        "ok": error is None,
        "data": data if error is None else None,
        "error": error
    }
    print(json.dumps(response), flush=True)


def write_error_response(request_id: str, error: str) -> None:
    """
    Write an error response to stdout.
    
    Args:
        request_id: The request ID from the incoming request
        error: Error message
    """
    write_response(request_id, None, error)


def run_jsonl_loop(handler_func) -> None:
    """
    Run the main JSONL processing loop.
    
    Reads requests from stdin, dispatches to handler_func,
    and writes responses to stdout.
    
    Args:
        handler_func: Function that takes (request_id, op, args) and returns result
    """
    while True:
        request = read_request()
        if request is None:
            break
            
        request_id = request.get("id", "")
        op = request.get("op", "")
        args = request.get("args", {})
        
        try:
            result = handler_func(request_id, op, args)
            write_response(request_id, result)
        except Exception as e:
            write_error_response(request_id, str(e))
