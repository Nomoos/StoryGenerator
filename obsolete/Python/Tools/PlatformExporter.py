"""
Platform-specific Export - Optimize exports for YouTube, TikTok, and Instagram.
"""

import os
import json
from typing import Dict, Any, Optional, List
from Models.StoryIdea import StoryIdea
from Tools.Utils import generate_title_id, get_segment_from_gender, get_age_group_from_potencial


class PlatformExporter:
    """
    Handles platform-specific export optimizations and metadata generation.
    """
    
    def __init__(self):
        """Initialize platform exporter."""
        self.platforms = {
            "youtube": self._youtube_config(),
            "tiktok": self._tiktok_config(),
            "instagram": self._instagram_config()
        }
    
    def _youtube_config(self) -> Dict[str, Any]:
        """YouTube Shorts configuration."""
        return {
            "name": "YouTube Shorts",
            "video_specs": {
                "max_duration": 60,
                "resolution": "1080x1920",
                "aspect_ratio": "9:16",
                "format": "mp4",
                "codec": "h264"
            },
            "metadata_limits": {
                "title": 100,
                "description": 5000,
                "tags": 500  # Total characters
            },
            "hashtag_strategy": "moderate",  # 3-5 hashtags
            "best_practices": [
                "First 3 seconds are crucial",
                "Add end screen with subscribe prompt",
                "Use trending music from YouTube library",
                "Optimize for mobile viewing"
            ]
        }
    
    def _tiktok_config(self) -> Dict[str, Any]:
        """TikTok configuration."""
        return {
            "name": "TikTok",
            "video_specs": {
                "max_duration": 60,
                "resolution": "1080x1920",
                "aspect_ratio": "9:16",
                "format": "mp4",
                "codec": "h264"
            },
            "metadata_limits": {
                "caption": 2200,
                "hashtags": 30  # Max number
            },
            "hashtag_strategy": "aggressive",  # 5-10 hashtags
            "best_practices": [
                "Hook viewers in first second",
                "Use trending sounds when possible",
                "Add text overlays for context",
                "Engage with trending challenges"
            ]
        }
    
    def _instagram_config(self) -> Dict[str, Any]:
        """Instagram Reels configuration."""
        return {
            "name": "Instagram Reels",
            "video_specs": {
                "max_duration": 90,
                "resolution": "1080x1920",
                "aspect_ratio": "9:16",
                "format": "mp4",
                "codec": "h264"
            },
            "metadata_limits": {
                "caption": 2200,
                "hashtags": 30  # Max number
            },
            "hashtag_strategy": "balanced",  # 5-7 hashtags
            "best_practices": [
                "Strong visual hook immediately",
                "Use Instagram's music library",
                "Add captions for sound-off viewing",
                "Post when audience is most active"
            ]
        }
    
    def generate_platform_metadata(
        self,
        story_idea: StoryIdea,
        platform: str,
        base_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate platform-specific metadata.
        
        Args:
            story_idea: StoryIdea object
            platform: Platform name (youtube, tiktok, instagram)
            base_metadata: Base metadata to extend
            
        Returns:
            Platform-specific metadata dictionary
        """
        if platform not in self.platforms:
            raise ValueError(f"Unsupported platform: {platform}")
        
        config = self.platforms[platform]
        
        # Start with base metadata or create new
        metadata = base_metadata.copy() if base_metadata else {}
        
        # Add platform-specific fields
        metadata["platform"] = platform
        metadata["platform_config"] = config
        
        # Generate platform-optimized title
        metadata["platform_title"] = self._optimize_title(
            story_idea.story_title,
            config["metadata_limits"].get("title", 100)
        )
        
        # Generate platform-optimized description
        metadata["platform_description"] = self._generate_description(
            story_idea,
            platform,
            config["metadata_limits"].get("description", 2200)
        )
        
        # Generate platform-specific hashtags
        metadata["platform_hashtags"] = self._generate_hashtags(
            story_idea,
            platform,
            config["hashtag_strategy"]
        )
        
        # Add platform-specific tips
        metadata["publishing_tips"] = config["best_practices"]
        
        return metadata
    
    def generate_all_platforms(
        self,
        story_idea: StoryIdea,
        base_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Dict[str, Any]]:
        """
        Generate metadata for all supported platforms.
        
        Args:
            story_idea: StoryIdea object
            base_metadata: Base metadata to extend
            
        Returns:
            Dictionary with metadata for each platform
        """
        all_metadata = {}
        
        for platform in self.platforms.keys():
            all_metadata[platform] = self.generate_platform_metadata(
                story_idea,
                platform,
                base_metadata
            )
        
        return all_metadata
    
    def save_platform_metadata(
        self,
        story_idea: StoryIdea,
        output_dir: str,
        platform: Optional[str] = None
    ) -> List[str]:
        """
        Save platform-specific metadata to JSON files.
        
        Args:
            story_idea: StoryIdea object
            output_dir: Directory to save metadata files
            platform: Specific platform (None for all)
            
        Returns:
            List of saved file paths
        """
        os.makedirs(output_dir, exist_ok=True)
        title_id = generate_title_id(story_idea.story_title)
        saved_files = []
        
        if platform:
            # Save single platform
            metadata = self.generate_platform_metadata(story_idea, platform)
            output_path = os.path.join(output_dir, f"{title_id}_{platform}_metadata.json")
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            saved_files.append(output_path)
            print(f"✅ Saved {platform} metadata: {output_path}")
        
        else:
            # Save all platforms
            all_metadata = self.generate_all_platforms(story_idea)
            
            for platform_name, metadata in all_metadata.items():
                output_path = os.path.join(output_dir, f"{title_id}_{platform_name}_metadata.json")
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2, ensure_ascii=False)
                
                saved_files.append(output_path)
                print(f"✅ Saved {platform_name} metadata: {output_path}")
        
        return saved_files
    
    def _optimize_title(self, title: str, max_length: int) -> str:
        """Optimize title for platform character limits."""
        if len(title) <= max_length:
            return title
        
        # Truncate and add ellipsis
        return title[:max_length-3] + "..."
    
    def _generate_description(
        self,
        story_idea: StoryIdea,
        platform: str,
        max_length: int
    ) -> str:
        """Generate platform-optimized description."""
        description_parts = []
        
        # Add title
        description_parts.append(story_idea.story_title)
        description_parts.append("")
        
        # Add theme and tone if available
        if story_idea.theme:
            description_parts.append(f"Theme: {story_idea.theme}")
        if story_idea.tone:
            description_parts.append(f"Tone: {story_idea.tone}")
        
        if story_idea.theme or story_idea.tone:
            description_parts.append("")
        
        # Add goal/description if available
        if story_idea.goal:
            description_parts.append(story_idea.goal)
            description_parts.append("")
        
        # Platform-specific call-to-action
        if platform == "youtube":
            description_parts.append("👍 Like and Subscribe for more stories!")
        elif platform == "tiktok":
            description_parts.append("❤️ Follow for more! #fyp")
        elif platform == "instagram":
            description_parts.append("💫 Follow for daily stories!")
        
        description = "\n".join(description_parts)
        
        # Truncate if needed
        if len(description) > max_length:
            description = description[:max_length-3] + "..."
        
        return description
    
    def _generate_hashtags(
        self,
        story_idea: StoryIdea,
        platform: str,
        strategy: str
    ) -> List[str]:
        """Generate platform-specific hashtags."""
        hashtags = []
        
        # Base hashtags
        hashtags.append("#shorts" if platform == "youtube" else "#reels" if platform == "instagram" else "#fyp")
        hashtags.append("#story")
        hashtags.append("#viral")
        
        # Add theme-based hashtags
        if story_idea.theme:
            theme_tag = story_idea.theme.replace(" ", "").lower()
            hashtags.append(f"#{theme_tag}")
        
        # Add tone-based hashtag
        if story_idea.tone:
            tone_tag = story_idea.tone.replace(" ", "").lower()
            hashtags.append(f"#{tone_tag}")
        
        # Strategy-specific additions
        if strategy == "aggressive":
            # TikTok style - more hashtags
            extra_tags = ["#storytime", "#trusstory", "#trending", "#foryou", "#foryoupage"]
            hashtags.extend(extra_tags[:5])
        
        elif strategy == "balanced":
            # Instagram style - moderate hashtags
            extra_tags = ["#storytelling", "#instareels", "#explore"]
            hashtags.extend(extra_tags[:3])
        
        elif strategy == "moderate":
            # YouTube style - fewer, more targeted
            extra_tags = ["#youtubeshorts", "#shortsvideo"]
            hashtags.extend(extra_tags[:2])
        
        # Remove duplicates and limit
        hashtags = list(dict.fromkeys(hashtags))
        
        # Apply platform limits
        max_hashtags = {
            "youtube": 5,
            "tiktok": 10,
            "instagram": 7
        }
        
        return hashtags[:max_hashtags.get(platform, 5)]
    
    def get_platform_info(self, platform: str) -> Dict[str, Any]:
        """Get configuration info for a platform."""
        if platform not in self.platforms:
            raise ValueError(f"Unsupported platform: {platform}")
        
        return self.platforms[platform]
    
    def list_platforms(self) -> List[str]:
        """List all supported platforms."""
        return list(self.platforms.keys())
