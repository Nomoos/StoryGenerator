"""
Complete Video Generation Pipeline
Orchestrates the full flow from story idea to final video
"""

from Models.StoryIdea import StoryIdea
from Generators.GVideoPipeline import VideoPipeline
from Generators.GIncrementalImprover import IncrementalImprover
from Tools.Utils import TITLES_PATH
import os


def generate_single_video(story_title: str):
    """
    Generate video for a single story
    
    Args:
        story_title: Title of the story (folder name in TITLES_PATH)
    """
    # Load story idea
    folder_path = os.path.join(TITLES_PATH, story_title)
    idea_file = os.path.join(folder_path, "Idea.json")
    
    if not os.path.exists(idea_file):
        print(f"❌ Story idea file not found: {idea_file}")
        return
    
    story_idea = StoryIdea.from_file(idea_file)
    
    # Initialize pipeline
    pipeline = VideoPipeline(
        use_gpu=True,
        num_inference_steps=30,
        target_fps=30
    )
    
    # Generate video
    try:
        final_video = pipeline.generate_video(
            story_idea=story_idea,
            skip_existing=True,
            add_subtitles=True
        )
        
        print(f"\n✅ Success! Video created: {final_video}")
        
    except Exception as e:
        print(f"\n❌ Failed to generate video: {e}")
        import traceback
        traceback.print_exc()


def generate_all_videos():
    """Generate videos for all stories in TITLES_PATH"""
    
    if not os.path.exists(TITLES_PATH):
        print(f"❌ TITLES_PATH not found: {TITLES_PATH}")
        return
    
    # Get all story folders
    story_folders = [
        f for f in os.listdir(TITLES_PATH)
        if os.path.isdir(os.path.join(TITLES_PATH, f))
    ]
    
    if not story_folders:
        print(f"⚠️ No story folders found in {TITLES_PATH}")
        return
    
    print(f"Found {len(story_folders)} stories to process")
    
    # Initialize pipeline (reuse for all stories)
    pipeline = VideoPipeline(
        use_gpu=True,
        num_inference_steps=30,
        target_fps=30
    )
    
    # Load story ideas
    story_ideas = []
    for folder in story_folders:
        idea_file = os.path.join(TITLES_PATH, folder, "Idea.json")
        if os.path.exists(idea_file):
            try:
                story_idea = StoryIdea.from_file(idea_file)
                story_ideas.append(story_idea)
            except Exception as e:
                print(f"⚠️ Could not load {folder}: {e}")
    
    # Generate videos in batch
    results = pipeline.generate_batch(
        story_ideas=story_ideas,
        skip_existing=True,
        add_subtitles=True
    )
    
    # Summary
    successful = sum(1 for v in results.values() if v is not None)
    print(f"\n{'='*60}")
    print(f"🎬 FINAL SUMMARY")
    print(f"{'='*60}")
    print(f"Total stories: {len(story_ideas)}")
    print(f"Successful: {successful}")
    print(f"Failed: {len(story_ideas) - successful}")
    print(f"{'='*60}\n")


def improve_video(story_title: str, user_feedback: str = None):
    """
    Analyze and improve an existing video
    
    Args:
        story_title: Title of the story
        user_feedback: Optional user feedback on the video
    """
    # Load story idea
    folder_path = os.path.join(TITLES_PATH, story_title)
    idea_file = os.path.join(folder_path, "Idea.json")
    
    if not os.path.exists(idea_file):
        print(f"❌ Story idea file not found: {idea_file}")
        return
    
    story_idea = StoryIdea.from_file(idea_file)
    
    # Initialize improver
    improver = IncrementalImprover()
    
    # Analyze quality
    print(f"\n🔍 Analyzing video quality...")
    analysis = improver.analyze_video_quality(story_idea, user_feedback)
    
    print(f"\n📊 Quality Analysis:")
    print(f"  Overall Score: {analysis['overall_score']:.2%}")
    print(f"  Iteration: {analysis['iteration']}")
    
    if analysis['issues']:
        print(f"\n⚠️ Issues Found:")
        for issue in analysis['issues']:
            print(f"  • {issue}")
    
    if analysis['suggestions']:
        print(f"\n💡 Suggestions:")
        for suggestion in analysis['suggestions']:
            print(f"  • {suggestion}")
    
    # Ask if user wants to apply improvements
    print(f"\n🔧 Available improvements:")
    print("  1. regenerate_scenes - Re-segment the story into scenes")
    print("  2. improve_descriptions - Regenerate visual descriptions")
    print("  3. regenerate_keyframes - Regenerate all keyframe images")
    print("  4. adjust_pacing - Adjust scene timing and pacing")
    
    choice = input("\nApply improvements? (comma-separated numbers, or 'n' to skip): ").strip()
    
    if choice.lower() != 'n':
        improvement_map = {
            '1': 'regenerate_scenes',
            '2': 'improve_descriptions',
            '3': 'regenerate_keyframes',
            '4': 'adjust_pacing'
        }
        
        selected = [improvement_map[c.strip()] for c in choice.split(',') if c.strip() in improvement_map]
        
        if selected:
            print(f"\n🔧 Applying improvements...")
            results = improver.apply_improvements(story_idea, selected)
            
            print(f"\n✅ Improvements applied:")
            for action, result in results.items():
                print(f"  • {action}: {result}")
            
            # Regenerate video with improvements
            regenerate = input("\nRegenerate video with improvements? (y/n): ").strip().lower()
            if regenerate == 'y':
                generate_single_video(story_title)


def check_pipeline_status(story_title: str):
    """
    Check the status of video generation pipeline for a story
    
    Args:
        story_title: Title of the story
    """
    folder_path = os.path.join(TITLES_PATH, story_title)
    idea_file = os.path.join(folder_path, "Idea.json")
    
    if not os.path.exists(idea_file):
        print(f"❌ Story idea file not found: {idea_file}")
        return
    
    story_idea = StoryIdea.from_file(idea_file)
    
    pipeline = VideoPipeline()
    status = pipeline.get_pipeline_status(story_idea)
    
    print(f"\n{'='*60}")
    print(f"📊 Pipeline Status: {story_idea.story_title}")
    print(f"{'='*60}")
    print(f"Status: {status['status']}")
    print(f"Progress: {status['progress']:.1f}%")
    
    if status['completed_steps']:
        print(f"\nCompleted Steps:")
        for step in status['completed_steps']:
            print(f"  ✅ {step}")
    
    if status.get('final_video'):
        print(f"\n📁 Final Video: {status['final_video']}")
    
    if status.get('error'):
        print(f"\n❌ Error: {status['error']}")
    
    print(f"{'='*60}\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python MVideoPipeline.py <story_title>         - Generate video for a story")
        print("  python MVideoPipeline.py all                   - Generate videos for all stories")
        print("  python MVideoPipeline.py improve <story_title> - Improve existing video")
        print("  python MVideoPipeline.py status <story_title>  - Check pipeline status")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "all":
        generate_all_videos()
    elif command == "improve":
        if len(sys.argv) < 3:
            print("❌ Please specify story title")
            sys.exit(1)
        improve_video(sys.argv[2])
    elif command == "status":
        if len(sys.argv) < 3:
            print("❌ Please specify story title")
            sys.exit(1)
        check_pipeline_status(sys.argv[2])
    else:
        # Assume it's a story title
        generate_single_video(command)
