"""
Pipeline Orchestrator Example

Demonstrates how to chain independent pipeline stages together
using their input/output contracts.
"""

from typing import Optional
from PrismQ.Infrastructure.Core.Shared.interfaces import (
    # Stage contracts
    IdeaGenerationInput,
    IdeaGenerationOutput,
    TextGenerationInput,
    TextGenerationOutput,
    AudioGenerationInput,
    AudioGenerationOutput,
    ImageGenerationInput,
    ImageGenerationOutput,
    VideoGenerationInput,
    VideoGenerationOutput,
    # Base interfaces
    IPipelineStage,
)


class PipelineOrchestrator:
    """
    Orchestrates the execution of pipeline stages.
    
    This orchestrator chains stages together using their contracts,
    without any knowledge of the internal implementation of each stage.
    """
    
    def __init__(
        self,
        idea_stage: Optional[IPipelineStage] = None,
        text_stage: Optional[IPipelineStage] = None,
        audio_stage: Optional[IPipelineStage] = None,
        image_stage: Optional[IPipelineStage] = None,
        video_stage: Optional[IPipelineStage] = None,
    ):
        """
        Initialize the pipeline orchestrator.
        
        Args:
            idea_stage: Stage 01 - Idea Generation
            text_stage: Stage 02 - Text Generation
            audio_stage: Stage 03 - Audio Generation
            image_stage: Stage 04 - Image Generation
            video_stage: Stage 05 - Video Generation
        """
        self.idea_stage = idea_stage
        self.text_stage = text_stage
        self.audio_stage = audio_stage
        self.image_stage = image_stage
        self.video_stage = video_stage
    
    async def run_full_pipeline(
        self,
        target_gender: str,
        target_age: str,
        idea_count: int = 20,
        source_stories: Optional[list] = None,
    ) -> VideoGenerationOutput:
        """
        Run the complete pipeline from idea to video.
        
        Args:
            target_gender: Target audience gender
            target_age: Target audience age bucket
            idea_count: Number of ideas to generate
            source_stories: Optional source stories to adapt
        
        Returns:
            VideoGenerationOutput with the final video
        
        Raises:
            ValueError: If required stages are not configured
        """
        # Stage 01: Idea Generation
        if not self.idea_stage:
            raise ValueError("Idea generation stage not configured")
        
        print("Stage 01: Generating ideas...")
        idea_input = IdeaGenerationInput(
            target_gender=target_gender,
            target_age=target_age,
            idea_count=idea_count,
            source_stories=source_stories
        )
        idea_result = await self.idea_stage.execute(idea_input)
        print(f"✓ Generated {idea_result.data.total_count} ideas in "
              f"{idea_result.metadata.execution_time_ms:.0f}ms")
        
        # Select the best idea (for this example, just take the first one)
        selected_idea = idea_result.data.ideas[0]
        print(f"  Selected idea: {selected_idea.content[:80]}...")
        
        # Stage 02: Text Generation
        if not self.text_stage:
            raise ValueError("Text generation stage not configured")
        
        print("\nStage 02: Generating text content...")
        text_input = TextGenerationInput(
            idea=selected_idea,
            generate_title=True,
            generate_description=True,
            generate_tags=True,
            generate_scenes=True
        )
        text_result = await self.text_stage.execute(text_input)
        print(f"✓ Generated text content in {text_result.metadata.execution_time_ms:.0f}ms")
        print(f"  Title: {text_result.data.content.title}")
        print(f"  Script length: {len(text_result.data.content.story_script)} chars")
        
        # Stage 03: Audio Generation
        if not self.audio_stage:
            raise ValueError("Audio generation stage not configured")
        
        print("\nStage 03: Generating audio...")
        audio_input = AudioGenerationInput(
            text_content=text_result.data.content,
            voice_id="female_1",
            generate_subtitles=True,
            audio_format="mp3"
        )
        audio_result = await self.audio_stage.execute(audio_input)
        print(f"✓ Generated audio in {audio_result.metadata.execution_time_ms:.0f}ms")
        print(f"  Audio file: {audio_result.data.audio.audio_file_path}")
        print(f"  Duration: {audio_result.data.audio.duration_seconds:.1f}s")
        print(f"  Subtitles: {len(audio_result.data.audio.subtitles)} segments")
        
        # Stage 04: Image Generation
        if not self.image_stage:
            raise ValueError("Image generation stage not configured")
        
        print("\nStage 04: Generating images...")
        image_input = ImageGenerationInput(
            text_content=text_result.data.content,
            audio_content=audio_result.data.audio,
            keyframe_count=5,
            image_style="cinematic"
        )
        image_result = await self.image_stage.execute(image_input)
        print(f"✓ Generated {len(image_result.data.keyframes)} keyframes in "
              f"{image_result.metadata.execution_time_ms:.0f}ms")
        
        # Stage 05: Video Generation
        if not self.video_stage:
            raise ValueError("Video generation stage not configured")
        
        print("\nStage 05: Assembling video...")
        video_input = VideoGenerationInput(
            text_content=text_result.data.content,
            audio_content=audio_result.data.audio,
            keyframes=image_result.data.keyframes,
            video_format="mp4",
            resolution="1080x1920",
            fps=30
        )
        video_result = await self.video_stage.execute(video_input)
        print(f"✓ Generated video in {video_result.metadata.execution_time_ms:.0f}ms")
        print(f"  Video file: {video_result.data.video.video_file_path}")
        print(f"  Duration: {video_result.data.video.duration_seconds:.1f}s")
        print(f"  Size: {video_result.data.video.file_size_bytes / 1024 / 1024:.2f} MB")
        
        return video_result.data
    
    async def run_partial_pipeline(
        self,
        start_stage: str,
        end_stage: str,
        **kwargs
    ):
        """
        Run a partial pipeline between specified stages.
        
        Args:
            start_stage: Starting stage ID (e.g., '01_idea_generation')
            end_stage: Ending stage ID (e.g., '03_audio_generation')
            **kwargs: Input parameters for the starting stage
        
        Returns:
            Output from the ending stage
        """
        # This allows running only a subset of the pipeline
        # e.g., just stages 02-03 for text and audio generation
        # Implementation would depend on the specific use case
        pass


# Example: Mock stage implementations for demonstration
class MockIdeaStage(IPipelineStage):
    """Mock implementation for demonstration."""
    
    @property
    def stage_name(self) -> str:
        return "IdeaGeneration"
    
    @property
    def stage_id(self) -> str:
        return "01_idea_generation"
    
    @property
    def stage_version(self) -> str:
        return "1.0.0"
    
    async def execute(self, input_data):
        from datetime import datetime
        from PrismQ.Infrastructure.Core.Shared.interfaces import (
            IdeaItem, IdeaGenerationOutput, StageResult, StageMetadata, StageStatus
        )
        
        idea = IdeaItem(
            id="mock_001",
            content="A story about personal growth and overcoming challenges",
            source="llm_generated",
            target_gender=input_data.target_gender,
            target_age=input_data.target_age,
            created_at=datetime.now()
        )
        
        output = IdeaGenerationOutput(
            ideas=[idea],
            total_count=1,
            adapted_count=0,
            generated_count=1
        )
        
        metadata = StageMetadata(
            stage_name=self.stage_name,
            stage_id=self.stage_id,
            version=self.stage_version,
            executed_at=datetime.now(),
            execution_time_ms=100.0,
            status=StageStatus.COMPLETED
        )
        
        return StageResult(data=output, metadata=metadata)
    
    async def validate_input(self, input_data) -> bool:
        return True


class MockTextStage(IPipelineStage):
    """Mock implementation for demonstration."""
    
    @property
    def stage_name(self) -> str:
        return "TextGeneration"
    
    @property
    def stage_id(self) -> str:
        return "02_text_generation"
    
    @property
    def stage_version(self) -> str:
        return "1.0.0"
    
    async def execute(self, input_data):
        from datetime import datetime
        from PrismQ.Infrastructure.Core.Shared.interfaces import (
            TextContent, TextGenerationOutput, StageResult, StageMetadata, StageStatus
        )
        
        content = TextContent(
            story_script="Once upon a time, in a world of endless possibilities...",
            title="Journey to Success",
            description="An inspiring story about achieving your dreams",
            tags=["inspiration", "motivation", "success"],
            scenes=[
                {"timestamp": 0, "description": "Opening scene"}
            ]
        )
        
        output = TextGenerationOutput(
            content=content,
            quality_score=85.5
        )
        
        metadata = StageMetadata(
            stage_name=self.stage_name,
            stage_id=self.stage_id,
            version=self.stage_version,
            executed_at=datetime.now(),
            execution_time_ms=250.0,
            status=StageStatus.COMPLETED
        )
        
        return StageResult(data=output, metadata=metadata)
    
    async def validate_input(self, input_data) -> bool:
        return True


class MockAudioStage(IPipelineStage):
    """Mock implementation for demonstration."""
    
    @property
    def stage_name(self) -> str:
        return "AudioGeneration"
    
    @property
    def stage_id(self) -> str:
        return "03_audio_generation"
    
    @property
    def stage_version(self) -> str:
        return "1.0.0"
    
    async def execute(self, input_data):
        from datetime import datetime
        from PrismQ.Infrastructure.Core.Shared.interfaces import (
            AudioContent, SubtitleSegment, AudioGenerationOutput, 
            StageResult, StageMetadata, StageStatus
        )
        
        audio = AudioContent(
            audio_file_path="/tmp/audio_mock.mp3",
            duration_seconds=30.0,
            subtitles=[
                SubtitleSegment(0.0, 5.0, "Once upon a time,"),
                SubtitleSegment(5.0, 10.0, "in a world of endless possibilities...")
            ],
            voice_id="female_1"
        )
        
        output = AudioGenerationOutput(audio=audio)
        
        metadata = StageMetadata(
            stage_name=self.stage_name,
            stage_id=self.stage_id,
            version=self.stage_version,
            executed_at=datetime.now(),
            execution_time_ms=500.0,
            status=StageStatus.COMPLETED
        )
        
        return StageResult(data=output, metadata=metadata)
    
    async def validate_input(self, input_data) -> bool:
        return True


class MockImageStage(IPipelineStage):
    """Mock implementation for demonstration."""
    
    @property
    def stage_name(self) -> str:
        return "ImageGeneration"
    
    @property
    def stage_id(self) -> str:
        return "04_image_generation"
    
    @property
    def stage_version(self) -> str:
        return "1.0.0"
    
    async def execute(self, input_data):
        from datetime import datetime
        from PrismQ.Infrastructure.Core.Shared.interfaces import (
            KeyFrame, ImageGenerationOutput, StageResult, StageMetadata, StageStatus
        )
        
        keyframes = [
            KeyFrame("kf_001", "/tmp/kf_001.png", 0.0, "Opening scene"),
            KeyFrame("kf_002", "/tmp/kf_002.png", 10.0, "Middle scene"),
            KeyFrame("kf_003", "/tmp/kf_003.png", 20.0, "Closing scene")
        ]
        
        output = ImageGenerationOutput(keyframes=keyframes)
        
        metadata = StageMetadata(
            stage_name=self.stage_name,
            stage_id=self.stage_id,
            version=self.stage_version,
            executed_at=datetime.now(),
            execution_time_ms=1500.0,
            status=StageStatus.COMPLETED
        )
        
        return StageResult(data=output, metadata=metadata)
    
    async def validate_input(self, input_data) -> bool:
        return True


class MockVideoStage(IPipelineStage):
    """Mock implementation for demonstration."""
    
    @property
    def stage_name(self) -> str:
        return "VideoGeneration"
    
    @property
    def stage_id(self) -> str:
        return "05_video_generation"
    
    @property
    def stage_version(self) -> str:
        return "1.0.0"
    
    async def execute(self, input_data):
        from datetime import datetime
        from PrismQ.Infrastructure.Core.Shared.interfaces import (
            VideoContent, VideoGenerationOutput, StageResult, StageMetadata, StageStatus
        )
        
        video = VideoContent(
            video_file_path="/tmp/final_video.mp4",
            duration_seconds=30.0,
            resolution="1080x1920",
            fps=30,
            file_size_bytes=15728640  # 15 MB
        )
        
        output = VideoGenerationOutput(video=video)
        
        metadata = StageMetadata(
            stage_name=self.stage_name,
            stage_id=self.stage_id,
            version=self.stage_version,
            executed_at=datetime.now(),
            execution_time_ms=3000.0,
            status=StageStatus.COMPLETED
        )
        
        return StageResult(data=output, metadata=metadata)
    
    async def validate_input(self, input_data) -> bool:
        return True


# Main execution example
async def main():
    """Run the complete pipeline with mock stages."""
    
    print("=" * 60)
    print("Pipeline Orchestrator - Full Pipeline Execution")
    print("=" * 60)
    
    # Create orchestrator with mock stages
    orchestrator = PipelineOrchestrator(
        idea_stage=MockIdeaStage(),
        text_stage=MockTextStage(),
        audio_stage=MockAudioStage(),
        image_stage=MockImageStage(),
        video_stage=MockVideoStage()
    )
    
    # Run the complete pipeline
    video_output = await orchestrator.run_full_pipeline(
        target_gender="women",
        target_age="18-23",
        idea_count=5
    )
    
    print("\n" + "=" * 60)
    print("Pipeline Complete!")
    print("=" * 60)
    print(f"\nFinal video: {video_output.video.video_file_path}")
    print(f"Duration: {video_output.video.duration_seconds}s")
    print(f"Resolution: {video_output.video.resolution}")
    print(f"Size: {video_output.video.file_size_bytes / 1024 / 1024:.2f} MB")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
