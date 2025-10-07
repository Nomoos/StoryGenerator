"""
Ollama CLI wrapper for local LLM inference.
Research prototype for local-only model orchestration.
"""

import subprocess
import json
from typing import Optional, Dict, Any, List


class OllamaClient:
    """
    Wrapper for Ollama CLI to run local language models.
    
    This is a research prototype demonstrating how to:
    - Call Ollama models via subprocess
    - Handle streaming responses
    - Manage model loading and context
    """
    
    def __init__(self, model: str = "llama2", base_url: str = "http://localhost:11434"):
        """
        Initialize Ollama client.
        
        Args:
            model: Name of the Ollama model to use (e.g., "llama2", "mistral")
            base_url: URL of the Ollama server
        """
        self.model = model
        self.base_url = base_url
        
    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> str:
        """
        Generate text using Ollama model via CLI.
        
        Args:
            prompt: Input prompt
            system: Optional system message
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
            
        Returns:
            Generated text
        """
        # Build command
        cmd = ["ollama", "run", self.model]
        
        # Construct full prompt with system message if provided
        full_prompt = prompt
        if system:
            full_prompt = f"{system}\n\n{prompt}"
            
        # Add prompt as stdin
        try:
            result = subprocess.run(
                cmd,
                input=full_prompt,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Ollama CLI error: {e.stderr}")
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Chat completion using Ollama API format.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Assistant's response
        """
        # For CLI, we'll convert messages to a single prompt
        # In production, use Ollama HTTP API for proper chat format
        prompt_parts = []
        system_msg = None
        
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "system":
                system_msg = content
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        prompt = "\n".join(prompt_parts) + "\nAssistant:"
        
        return self.generate(
            prompt=prompt,
            system=system_msg,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    def list_models(self) -> List[str]:
        """
        List available Ollama models.
        
        Returns:
            List of model names
        """
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                check=True
            )
            # Parse output to extract model names
            lines = result.stdout.strip().split("\n")[1:]  # Skip header
            models = [line.split()[0] for line in lines if line.strip()]
            return models
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to list models: {e.stderr}")
    
    def pull_model(self, model_name: str) -> bool:
        """
        Download an Ollama model.
        
        Args:
            model_name: Name of the model to download
            
        Returns:
            True if successful
        """
        try:
            subprocess.run(
                ["ollama", "pull", model_name],
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False


# Example usage
if __name__ == "__main__":
    client = OllamaClient(model="llama2")
    
    # Simple generation
    response = client.generate(
        prompt="Write a short story about a robot learning to paint.",
        system="You are a creative storytelling assistant.",
        temperature=0.8
    )
    print("Generated Story:")
    print(response)
    
    # Chat format
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"},
    ]
    response = client.chat(messages)
    print("\nChat Response:")
    print(response)
