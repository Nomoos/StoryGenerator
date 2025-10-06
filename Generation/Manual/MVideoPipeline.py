"""
Manual script to run the video generation pipeline.
"""

from Video.VideoPipeline import VideoPipeline


def run_video_pipeline():
    """
    Run the complete video generation pipeline.
    Processes all voiceovers and generates final videos with thumbnails and metadata.
    """
    # Initialize the pipeline
    pipeline = VideoPipeline(
        max_workers=2,  # Number of parallel video generation tasks
        default_resolution=(1080, 1920)  # Vertical video for social media
    )
    
    # Process all stories
    stats = pipeline.batch_process(
        parallel=False,  # Set to True for parallel processing (faster but uses more resources)
        force_regenerate=False  # Set to True to regenerate existing videos
    )
    
    # Show results
    if stats['processed'] > 0:
        success_rate = (stats['successful'] / stats['processed']) * 100
        print(f"\n{'='*60}")
        print(f"✅ Video Pipeline Complete!")
        print(f"{'='*60}")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"Total Videos: {stats['successful']}")
        print(f"{'='*60}\n")
    else:
        print("\n⚠️ No stories found to process.\n")


if __name__ == "__main__":
    run_video_pipeline()
