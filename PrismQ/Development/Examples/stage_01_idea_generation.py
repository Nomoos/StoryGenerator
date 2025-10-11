"""
Example Pipeline Stage Implementation: Idea Generation

This example demonstrates how to implement a pipeline stage using the
modular architecture with clear input/output contracts.
"""

from datetime import datetime
from typing import Optional
from PrismQ.Infrastructure.Core.Shared.interfaces import (
    BasePipelineStage,
    IdeaGenerationInput,
    IdeaGenerationOutput,
    IdeaItem,
    ILLMProvider,
)


class IdeaGenerationStage(BasePipelineStage[IdeaGenerationInput, IdeaGenerationOutput]):
    """
    Stage 01: Idea Generation
    
    Generates creative video ideas based on target audience demographics.
    This stage is fully independent and can be tested without other stages.
    
    Dependencies:
    - ILLMProvider: For generating and adapting ideas
    
    No cross-stage dependencies.
    """
    
    def __init__(self, llm_provider: ILLMProvider):
        """
        Initialize the Idea Generation stage.
        
        Args:
            llm_provider: LLM provider for idea generation
        """
        super().__init__(
            stage_name="IdeaGeneration",
            stage_id="01_idea_generation",
            version="1.0.0"
        )
        self.llm_provider = llm_provider
    
    async def _execute_impl(
        self, 
        input_data: IdeaGenerationInput
    ) -> IdeaGenerationOutput:
        """
        Execute idea generation logic.
        
        Args:
            input_data: Validated input containing target demographics
        
        Returns:
            IdeaGenerationOutput with generated ideas
        """
        ideas = []
        
        # Step 1: Adapt source stories if provided
        if input_data.source_stories:
            adapted_ideas = await self._adapt_stories(
                input_data.source_stories,
                input_data.target_gender,
                input_data.target_age
            )
            ideas.extend(adapted_ideas)
        
        # Step 2: Generate LLM ideas to reach desired count
        remaining = input_data.idea_count - len(ideas)
        if remaining > 0:
            generated_ideas = await self._generate_ideas(
                input_data.target_gender,
                input_data.target_age,
                remaining
            )
            ideas.extend(generated_ideas)
        
        # Step 3: Return structured output
        return IdeaGenerationOutput(
            ideas=ideas,
            total_count=len(ideas),
            adapted_count=len([i for i in ideas if i.source == 'reddit_adapted']),
            generated_count=len([i for i in ideas if i.source == 'llm_generated']),
        )
    
    async def validate_input(self, input_data: IdeaGenerationInput) -> bool:
        """
        Validate input parameters.
        
        Args:
            input_data: Input to validate
        
        Returns:
            True if valid
        
        Raises:
            ValueError: If validation fails with details
        """
        valid_genders = ['women', 'men', 'all', 'non-binary']
        valid_ages = ['18-23', '24-29', '30-39', '40-49', '50+']
        
        if input_data.target_gender not in valid_genders:
            raise ValueError(
                f"Invalid target_gender '{input_data.target_gender}'. "
                f"Must be one of: {', '.join(valid_genders)}"
            )
        
        if input_data.target_age not in valid_ages:
            raise ValueError(
                f"Invalid target_age '{input_data.target_age}'. "
                f"Must be one of: {', '.join(valid_ages)}"
            )
        
        if input_data.idea_count <= 0 or input_data.idea_count > 100:
            raise ValueError(
                f"idea_count must be between 1 and 100, got {input_data.idea_count}"
            )
        
        return True
    
    async def _adapt_stories(
        self, 
        stories: list[dict], 
        gender: str, 
        age: str
    ) -> list[IdeaItem]:
        """
        Adapt source stories into video ideas.
        
        Args:
            stories: Source stories to adapt
            gender: Target gender
            age: Target age bucket
        
        Returns:
            List of adapted IdeaItem objects
        """
        ideas = []
        
        for story in stories:
            prompt = self._build_adaptation_prompt(story, gender, age)
            
            # Generate adaptation using LLM
            content = self.llm_provider.generate_completion(
                prompt=prompt,
                temperature=0.7,
                max_tokens=300
            )
            
            ideas.append(IdeaItem(
                id=f"reddit_{story.get('id', 'unknown')}",
                content=content.strip(),
                source='reddit_adapted',
                target_gender=gender,
                target_age=age,
                created_at=datetime.now(),
                metadata={
                    'original_title': story.get('title', ''),
                    'original_url': story.get('url', ''),
                    'score': story.get('score', 0),
                    'subreddit': story.get('subreddit', '')
                }
            ))
        
        return ideas
    
    async def _generate_ideas(
        self, 
        gender: str, 
        age: str, 
        count: int
    ) -> list[IdeaItem]:
        """
        Generate new ideas using LLM.
        
        Args:
            gender: Target gender
            age: Target age bucket
            count: Number of ideas to generate
        
        Returns:
            List of generated IdeaItem objects
        """
        prompt = self._build_generation_prompt(gender, age, count)
        
        # Generate ideas using LLM
        response = self.llm_provider.generate_completion(
            prompt=prompt,
            temperature=0.8,
            max_tokens=500
        )
        
        # Parse numbered list
        ideas = []
        for i, line in enumerate(response.strip().split('\n'), 1):
            line = line.strip()
            if line:
                # Remove numbering if present (e.g., "1. " or "1) ")
                content = line.split('.', 1)[-1].strip()
                if content:
                    ideas.append(IdeaItem(
                        id=f"llm_{i:03d}",
                        content=content,
                        source='llm_generated',
                        target_gender=gender,
                        target_age=age,
                        created_at=datetime.now(),
                    ))
        
        return ideas[:count]
    
    def _build_adaptation_prompt(
        self, 
        story: dict, 
        gender: str, 
        age: str
    ) -> str:
        """Build prompt for story adaptation."""
        return f"""
Adapt this story into a compelling video idea for {gender} aged {age}:

Title: {story.get('title', '')}
Content: {story.get('selftext', story.get('content', ''))}
Source: {story.get('subreddit', 'reddit')}

Create a video idea that:
- Resonates with the target audience ({gender}, {age})
- Is engaging and shareable
- Can be produced as a short video (30-60 seconds)
- Maintains the core message but adapts the framing

Return only the video idea description, no additional commentary.
"""
    
    def _build_generation_prompt(self, gender: str, age: str, count: int) -> str:
        """Build prompt for idea generation."""
        return f"""
Generate {count} creative and engaging video ideas for {gender} aged {age}.

Each idea should:
- Be relevant and interesting to the target demographic
- Be suitable for a 30-60 second video
- Be shareable on social media
- Cover diverse topics (relationships, career, personal growth, lifestyle, etc.)

Format your response as a numbered list:
1. [First idea]
2. [Second idea]
...
"""

    def get_input_schema(self) -> dict:
        """Get JSON schema for input."""
        return {
            "type": "object",
            "properties": {
                "target_gender": {
                    "type": "string",
                    "enum": ["women", "men", "all", "non-binary"]
                },
                "target_age": {
                    "type": "string",
                    "enum": ["18-23", "24-29", "30-39", "40-49", "50+"]
                },
                "idea_count": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 100
                },
                "source_stories": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "title": {"type": "string"},
                            "content": {"type": "string"}
                        }
                    }
                }
            },
            "required": ["target_gender", "target_age"]
        }
    
    def get_output_schema(self) -> dict:
        """Get JSON schema for output."""
        return {
            "type": "object",
            "properties": {
                "ideas": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "content": {"type": "string"},
                            "source": {"type": "string"},
                            "target_gender": {"type": "string"},
                            "target_age": {"type": "string"},
                            "created_at": {"type": "string", "format": "date-time"}
                        }
                    }
                },
                "total_count": {"type": "integer"},
                "adapted_count": {"type": "integer"},
                "generated_count": {"type": "integer"}
            },
            "required": ["ideas", "total_count", "adapted_count", "generated_count"]
        }


# Example usage
async def main():
    """Example of using the Idea Generation stage."""
    from PrismQ.Infrastructure.Platform.Providers.mock_provider import MockLLMProvider
    
    # Initialize dependencies
    llm_provider = MockLLMProvider()
    
    # Create stage
    stage = IdeaGenerationStage(llm_provider=llm_provider)
    
    # Prepare input
    input_data = IdeaGenerationInput(
        target_gender='women',
        target_age='18-23',
        idea_count=5,
        source_stories=[
            {
                'id': 'story123',
                'title': 'How I overcame my fear',
                'content': 'This is my story about overcoming challenges...',
                'score': 1500,
                'subreddit': 'GetMotivated'
            }
        ]
    )
    
    # Execute stage
    result = await stage.execute(input_data)
    
    # Access output
    print(f"Generated {result.data.total_count} ideas")
    print(f"Adapted: {result.data.adapted_count}, Generated: {result.data.generated_count}")
    print(f"Execution time: {result.metadata.execution_time_ms:.2f}ms")
    
    for idea in result.data.ideas:
        print(f"\n[{idea.id}] ({idea.source})")
        print(f"  {idea.content}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
