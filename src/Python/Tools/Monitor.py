"""
Performance monitoring and logging utility for StoryGenerator.
Tracks execution times, errors, and output quality metrics.
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, Any, Optional
from functools import wraps
import logging

# Configure logging
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Create logger
logger = logging.getLogger("StoryGenerator")
logger.setLevel(logging.INFO)

# File handler for all logs
log_file = os.path.join(LOG_DIR, f"storygen_{datetime.now().strftime('%Y%m%d')}.log")
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Metrics storage
METRICS_FILE = os.path.join(LOG_DIR, "metrics.json")


class PerformanceMonitor:
    """Monitor and log performance metrics for various operations."""
    
    @staticmethod
    def load_metrics() -> Dict[str, Any]:
        """Load metrics from file."""
        if os.path.exists(METRICS_FILE):
            try:
                with open(METRICS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load metrics: {e}")
        return {"sessions": []}
    
    @staticmethod
    def save_metrics(metrics: Dict[str, Any]):
        """Save metrics to file."""
        try:
            with open(METRICS_FILE, 'w', encoding='utf-8') as f:
                json.dump(metrics, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save metrics: {e}")
    
    @staticmethod
    def log_operation(operation: str, story_title: str, duration: float, 
                      success: bool, error: Optional[str] = None,
                      metrics: Optional[Dict[str, Any]] = None):
        """Log a completed operation with metrics."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "story_title": story_title,
            "duration_seconds": round(duration, 2),
            "success": success,
            "error": error,
            "metrics": metrics or {}
        }
        
        # Load existing metrics
        all_metrics = PerformanceMonitor.load_metrics()
        all_metrics["sessions"].append(entry)
        
        # Keep only last 1000 entries
        if len(all_metrics["sessions"]) > 1000:
            all_metrics["sessions"] = all_metrics["sessions"][-1000:]
        
        PerformanceMonitor.save_metrics(all_metrics)
        
        # Log to console
        status = "✅" if success else "❌"
        msg = f"{status} {operation} for '{story_title}' completed in {duration:.2f}s"
        if error:
            logger.error(f"{msg} - Error: {error}")
        else:
            logger.info(msg)
        
        if metrics:
            logger.info(f"   Metrics: {metrics}")


def time_operation(operation_name: str):
    """Decorator to time and log operations."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            success = True
            error = None
            result = None
            
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                success = False
                error = str(e)
                raise
            finally:
                duration = time.time() - start_time
                
                # Try to extract story title from args
                story_title = "unknown"
                for arg in args:
                    if hasattr(arg, 'story_title'):
                        story_title = arg.story_title
                        break
                    elif isinstance(arg, str) and len(arg) < 100:
                        story_title = arg
                        break
                
                PerformanceMonitor.log_operation(
                    operation=operation_name,
                    story_title=story_title,
                    duration=duration,
                    success=success,
                    error=error
                )
            
            return result
        return wrapper
    return decorator


def log_error(operation: str, story_title: str, error: Exception):
    """Log an error."""
    logger.error(f"❌ {operation} failed for '{story_title}': {error}", exc_info=True)


def log_info(message: str):
    """Log an info message."""
    logger.info(message)


def log_warning(message: str):
    """Log a warning message."""
    logger.warning(message)


def get_performance_summary() -> Dict[str, Any]:
    """Get a summary of recent performance metrics."""
    metrics = PerformanceMonitor.load_metrics()
    sessions = metrics.get("sessions", [])
    
    if not sessions:
        return {"message": "No metrics available"}
    
    # Calculate summary statistics
    total_operations = len(sessions)
    successful = sum(1 for s in sessions if s.get("success", False))
    failed = total_operations - successful
    
    operation_types = {}
    for session in sessions:
        op = session.get("operation", "unknown")
        if op not in operation_types:
            operation_types[op] = {"count": 0, "total_time": 0, "failures": 0}
        
        operation_types[op]["count"] += 1
        operation_types[op]["total_time"] += session.get("duration_seconds", 0)
        if not session.get("success", False):
            operation_types[op]["failures"] += 1
    
    # Calculate averages
    for op in operation_types:
        count = operation_types[op]["count"]
        operation_types[op]["avg_time"] = round(
            operation_types[op]["total_time"] / count if count > 0 else 0, 2
        )
    
    return {
        "total_operations": total_operations,
        "successful": successful,
        "failed": failed,
        "success_rate": round(successful / total_operations * 100, 1) if total_operations > 0 else 0,
        "by_operation": operation_types
    }
