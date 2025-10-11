"""
Pattern Matching Examples (PEP 634-636)

This module demonstrates practical uses of structural pattern matching
in the StoryGenerator pipeline for cleaner, more expressive code.
"""

from dataclasses import dataclass
from typing import TypedDict


# Example 1: Processing API Responses with TypedDict
class APIResponse(TypedDict, total=False):
    """Structured API response format."""
    status: str
    data: dict[str, object] | None
    error: str | None
    code: int | None


def handle_api_response(response: APIResponse) -> str:
    """
    Handle different API response types using pattern matching.
    
    Pattern matching provides clearer intent than nested if-elif chains
    and enables destructuring of response data directly in the match.
    """
    match response:
        case {"status": "success", "data": data} if data:
            return f"Success: Processed {len(data)} items"
        
        case {"status": "error", "error": error_msg, "code": 404}:
            return f"Not found: {error_msg}"
        
        case {"status": "error", "error": error_msg, "code": 500}:
            return f"Server error: {error_msg}"
        
        case {"status": "error", "error": error_msg}:
            return f"Error: {error_msg}"
        
        case {"status": "pending"}:
            return "Request is still processing..."
        
        case _:
            return "Unknown response format"


# Example 2: Processing Script Quality Scores
@dataclass
class QualityScore:
    """Quality score for a generated script."""
    overall: float
    engagement: float
    clarity: float


def recommend_action(score: QualityScore) -> str:
    """
    Recommend action based on quality score patterns.
    
    Pattern matching with guards (if conditions) makes it easy
    to handle complex decision logic.
    """
    match score:
        case QualityScore(overall=o) if o >= 90:
            return "Excellent! Ready for production."
        
        case QualityScore(overall=o, engagement=e) if o >= 75 and e < 70:
            return "Good overall, but improve engagement hooks."
        
        case QualityScore(overall=o, clarity=c) if o >= 75 and c < 70:
            return "Good overall, but simplify language for clarity."
        
        case QualityScore(overall=o) if o >= 75:
            return "Good quality. Consider minor improvements."
        
        case QualityScore(overall=o) if o >= 60:
            return "Needs improvement. Run another iteration."
        
        case _:
            return "Quality too low. Generate a new script."


# Example 3: Processing Video Generation Results
def process_generation_result(result: dict[str, object]) -> str:
    """
    Process video generation results with pattern matching.
    
    This example shows how to destructure nested dictionaries
    and handle various success/failure states cleanly.
    """
    match result:
        # Perfect case - all stages successful
        case {
            "script": {"status": "complete"},
            "audio": {"status": "complete"},
            "video": {"status": "complete", "path": video_path}
        }:
            return f"Video ready: {video_path}"
        
        # Video generation failed but audio is ready
        case {
            "script": {"status": "complete"},
            "audio": {"status": "complete", "path": audio_path},
            "video": {"status": "failed", "error": error}
        }:
            return f"Video failed ({error}), but audio available: {audio_path}"
        
        # Early stage failure
        case {"script": {"status": "failed", "error": error}}:
            return f"Script generation failed: {error}"
        
        case {"audio": {"status": "failed", "error": error}}:
            return f"Audio generation failed: {error}"
        
        # Processing in progress
        case {"script": {"status": "processing"}}:
            return "Script is being generated..."
        
        case {"audio": {"status": "processing"}}:
            return "Audio is being generated..."
        
        case {"video": {"status": "processing", "progress": progress}}:
            return f"Video rendering: {progress}%"
        
        case _:
            return "Unknown generation state"


# Example 4: Content Type Router
def route_content(content: str | dict[str, object] | list[dict[str, object]]) -> str:
    """
    Route content to appropriate processor based on type and structure.
    
    Pattern matching makes handling multiple types and structures elegant.
    """
    match content:
        # Empty cases
        case "" | [] | {}:
            return "No content to process"
        
        # String content (raw text)
        case str(text) if len(text) > 1000:
            return "Processing long-form text content"
        
        case str(text):
            return f"Processing text: {len(text)} chars"
        
        # Single item (dict)
        case {"type": "reddit", "content": text, "score": score}:
            return f"Processing Reddit post (score: {score})"
        
        case {"type": "idea", "content": text}:
            return "Processing story idea"
        
        # Multiple items (list)
        case [item, *rest] if len(rest) > 10:
            return f"Batch processing {len(rest) + 1} items"
        
        case [single_item]:
            return "Processing single item from list"
        
        case list(items):
            return f"Processing {len(items)} items"
        
        case _:
            return "Unknown content type"


# Example 5: Status-based workflow with enums
def handle_workflow_state(state: dict[str, str | int]) -> tuple[str, bool]:
    """
    Handle workflow state transitions with pattern matching.
    
    Returns: (action_description, should_continue)
    """
    match state:
        case {"stage": "init", "retry_count": 0}:
            return ("Starting new workflow", True)
        
        case {"stage": "init", "retry_count": count} if count < 3:
            return (f"Retrying initialization (attempt {count + 1})", True)
        
        case {"stage": "init", "retry_count": count} if count >= 3:
            return ("Max retries reached, aborting", False)
        
        case {"stage": "processing", "progress": p} if p < 100:
            return (f"Processing: {p}% complete", True)
        
        case {"stage": "processing", "progress": 100}:
            return ("Processing complete, moving to next stage", True)
        
        case {"stage": "complete", "output": path}:
            return (f"Workflow complete: {path}", False)
        
        case {"stage": "error", "error": msg}:
            return (f"Workflow failed: {msg}", False)
        
        case _:
            return ("Unknown state", False)


# Example usage
if __name__ == "__main__":
    # Example 1: API Response
    print("=== API Response Handling ===")
    success_response: APIResponse = {"status": "success", "data": {"count": 5}}
    print(handle_api_response(success_response))
    
    error_response: APIResponse = {"status": "error", "error": "Not found", "code": 404}
    print(handle_api_response(error_response))
    
    # Example 2: Quality Scores
    print("\n=== Quality Score Recommendations ===")
    excellent_score = QualityScore(overall=92.0, engagement=88.0, clarity=90.0)
    print(recommend_action(excellent_score))
    
    needs_engagement = QualityScore(overall=78.0, engagement=65.0, clarity=85.0)
    print(recommend_action(needs_engagement))
    
    # Example 3: Generation Results
    print("\n=== Video Generation Results ===")
    complete_result = {
        "script": {"status": "complete"},
        "audio": {"status": "complete"},
        "video": {"status": "complete", "path": "/output/video.mp4"}
    }
    print(process_generation_result(complete_result))
    
    # Example 4: Content Routing
    print("\n=== Content Routing ===")
    reddit_content = {"type": "reddit", "content": "Story text...", "score": 1500}
    print(route_content(reddit_content))
    
    batch_content = [{"id": i} for i in range(15)]
    print(route_content(batch_content))
    
    # Example 5: Workflow State
    print("\n=== Workflow State Handling ===")
    init_state = {"stage": "init", "retry_count": 0}
    action, should_continue = handle_workflow_state(init_state)
    print(f"{action} (continue: {should_continue})")
    
    processing_state = {"stage": "processing", "progress": 75}
    action, should_continue = handle_workflow_state(processing_state)
    print(f"{action} (continue: {should_continue})")
