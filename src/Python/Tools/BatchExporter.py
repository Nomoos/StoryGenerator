"""
Batch Export Processing - Export multiple videos at once with progress tracking.
"""

import os
import time
from typing import List, Dict, Any, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from Models.StoryIdea import StoryIdea
from Generators.GVideoCompositor import VideoCompositor
from Tools.ExportRegistry import ExportRegistry
from Tools.Utils import generate_title_id, get_segment_from_gender, get_age_group_from_potencial


class BatchExporter:
    """
    Handles batch export of multiple videos with progress tracking and error handling.
    """
    
    def __init__(
        self,
        max_workers: int = 4,
        registry: Optional[ExportRegistry] = None
    ):
        """
        Initialize batch exporter.
        
        Args:
            max_workers: Maximum number of parallel export operations
            registry: ExportRegistry instance (creates new if None)
        """
        self.max_workers = max_workers
        self.compositor = VideoCompositor()
        self.registry = registry or ExportRegistry()
        self.results = []
    
    def export_batch(
        self,
        story_ideas: List[StoryIdea],
        source_videos: List[str],
        parallel: bool = True,
        export_thumbnails: bool = True,
        export_metadata: bool = True,
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> Dict[str, Any]:
        """
        Export multiple videos in batch.
        
        Args:
            story_ideas: List of StoryIdea objects
            source_videos: List of source video paths (must match story_ideas length)
            parallel: Whether to export in parallel
            export_thumbnails: Whether to generate thumbnails
            export_metadata: Whether to generate metadata
            progress_callback: Callback function(current, total, title) for progress updates
            
        Returns:
            Dictionary with batch export results and statistics
        """
        if len(story_ideas) != len(source_videos):
            raise ValueError("Number of story_ideas must match number of source_videos")
        
        print(f"\n{'='*60}")
        print(f"📦 BATCH EXPORT: {len(story_ideas)} videos")
        print(f"{'='*60}\n")
        
        start_time = time.time()
        self.results = []
        
        if parallel and self.max_workers > 1:
            results = self._export_parallel(
                story_ideas, source_videos,
                export_thumbnails, export_metadata,
                progress_callback
            )
        else:
            results = self._export_sequential(
                story_ideas, source_videos,
                export_thumbnails, export_metadata,
                progress_callback
            )
        
        # Calculate statistics
        duration = time.time() - start_time
        successful = sum(1 for r in results if r["success"])
        failed = len(results) - successful
        
        summary = {
            "total": len(results),
            "successful": successful,
            "failed": failed,
            "duration_seconds": round(duration, 2),
            "avg_time_per_video": round(duration / len(results), 2) if results else 0,
            "results": results
        }
        
        # Print summary
        self._print_summary(summary)
        
        return summary
    
    def _export_sequential(
        self,
        story_ideas: List[StoryIdea],
        source_videos: List[str],
        export_thumbnails: bool,
        export_metadata: bool,
        progress_callback: Optional[Callable]
    ) -> List[Dict[str, Any]]:
        """Export videos sequentially."""
        results = []
        total = len(story_ideas)
        
        for i, (story_idea, video_path) in enumerate(zip(story_ideas, source_videos), 1):
            print(f"\n📹 Processing {i}/{total}: {story_idea.story_title}")
            
            if progress_callback:
                progress_callback(i, total, story_idea.story_title)
            
            result = self._export_single(
                story_idea, video_path,
                export_thumbnails, export_metadata
            )
            results.append(result)
        
        return results
    
    def _export_parallel(
        self,
        story_ideas: List[StoryIdea],
        source_videos: List[str],
        export_thumbnails: bool,
        export_metadata: bool,
        progress_callback: Optional[Callable]
    ) -> List[Dict[str, Any]]:
        """Export videos in parallel."""
        results = []
        total = len(story_ideas)
        completed = 0
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_story = {
                executor.submit(
                    self._export_single,
                    story_idea,
                    video_path,
                    export_thumbnails,
                    export_metadata
                ): (story_idea, video_path)
                for story_idea, video_path in zip(story_ideas, source_videos)
            }
            
            # Process completed tasks
            for future in as_completed(future_to_story):
                story_idea, video_path = future_to_story[future]
                completed += 1
                
                try:
                    result = future.result()
                    results.append(result)
                    
                    if progress_callback:
                        progress_callback(completed, total, story_idea.story_title)
                    
                    print(f"\n✅ [{completed}/{total}] Completed: {story_idea.story_title}")
                    
                except Exception as e:
                    error_result = {
                        "title": story_idea.story_title,
                        "title_id": generate_title_id(story_idea.story_title),
                        "success": False,
                        "error": str(e)
                    }
                    results.append(error_result)
                    print(f"\n❌ [{completed}/{total}] Failed: {story_idea.story_title} - {e}")
        
        return results
    
    def _export_single(
        self,
        story_idea: StoryIdea,
        source_video: str,
        export_thumbnail: bool,
        export_metadata: bool
    ) -> Dict[str, Any]:
        """
        Export a single video.
        
        Returns:
            Dictionary with export result information
        """
        start_time = time.time()
        title_id = generate_title_id(story_idea.story_title)
        
        result = {
            "title": story_idea.story_title,
            "title_id": title_id,
            "success": False,
            "error": None,
            "duration": 0,
            "video_path": None,
            "thumbnail_path": None,
            "metadata_path": None
        }
        
        try:
            # Check if source video exists
            if not os.path.exists(source_video):
                raise FileNotFoundError(f"Source video not found: {source_video}")
            
            # Perform export
            video_path, thumbnail_path, metadata_path = self.compositor.export_final_video(
                story_idea=story_idea,
                source_video_path=source_video,
                export_thumbnail=export_thumbnail,
                export_metadata=export_metadata
            )
            
            # Register in registry
            segment = get_segment_from_gender(story_idea.narrator_gender)
            age_group = get_age_group_from_potencial(story_idea.potencial)
            
            self.registry.register_export(
                title_id=title_id,
                title=story_idea.story_title,
                segment=segment,
                age_group=age_group,
                video_path=video_path,
                thumbnail_path=thumbnail_path,
                metadata_path=metadata_path,
                additional_info={
                    "theme": story_idea.theme,
                    "tone": story_idea.tone,
                    "language": story_idea.language
                }
            )
            
            # Update result
            result["success"] = True
            result["video_path"] = video_path
            result["thumbnail_path"] = thumbnail_path
            result["metadata_path"] = metadata_path
            
        except Exception as e:
            result["error"] = str(e)
            print(f"  ❌ Error exporting {story_idea.story_title}: {e}")
        
        finally:
            result["duration"] = round(time.time() - start_time, 2)
        
        return result
    
    def _print_summary(self, summary: Dict[str, Any]):
        """Print batch export summary."""
        print(f"\n{'='*60}")
        print(f"📊 BATCH EXPORT SUMMARY")
        print(f"{'='*60}")
        print(f"Total Videos: {summary['total']}")
        print(f"Successful: {summary['successful']} ✅")
        print(f"Failed: {summary['failed']} ❌")
        print(f"Total Duration: {summary['duration_seconds']}s")
        print(f"Avg Time/Video: {summary['avg_time_per_video']}s")
        print(f"{'='*60}\n")
        
        # List failed exports
        if summary['failed'] > 0:
            print("❌ Failed Exports:")
            for result in summary['results']:
                if not result['success']:
                    print(f"  - {result['title']}: {result['error']}")
            print()
    
    def retry_failed(
        self,
        previous_results: Dict[str, Any],
        story_ideas: List[StoryIdea],
        source_videos: List[str]
    ) -> Dict[str, Any]:
        """
        Retry failed exports from a previous batch.
        
        Args:
            previous_results: Results from previous batch export
            story_ideas: Original list of StoryIdea objects
            source_videos: Original list of source video paths
            
        Returns:
            Dictionary with retry results
        """
        # Find failed exports
        failed_indices = [
            i for i, result in enumerate(previous_results['results'])
            if not result['success']
        ]
        
        if not failed_indices:
            print("✅ No failed exports to retry")
            return {"total": 0, "successful": 0, "failed": 0, "results": []}
        
        print(f"\n🔄 Retrying {len(failed_indices)} failed exports...")
        
        # Retry failed exports
        retry_stories = [story_ideas[i] for i in failed_indices]
        retry_videos = [source_videos[i] for i in failed_indices]
        
        return self.export_batch(
            story_ideas=retry_stories,
            source_videos=retry_videos,
            parallel=False  # Sequential for retry
        )
