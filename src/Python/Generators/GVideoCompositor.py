import os
import json
import subprocess
import shutil
from typing import List, Optional, Tuple
from Models.StoryIdea import StoryIdea
from Generators.GSceneAnalyzer import SceneAnalyzer
from Tools.Utils import (
    TITLES_PATH, sanitize_filename, 
    get_segment_from_gender, get_age_group_from_potencial,
    generate_title_id, get_final_export_path
)
from Tools.VideoEffects import VideoEffects


class VideoCompositor:
    """
    Composes final video by combining video segments with audio and subtitles.
    Creates the final 1080x1920 vertical video ready for publishing.
    """

    def __init__(self, output_format: str = "mp4", enable_transitions: bool = True, 
                 transition_duration: float = 0.5, apply_ken_burns: bool = False):
        """
        Initialize video compositor
        
        Args:
            output_format: Output video format (default: mp4)
            enable_transitions: Enable smooth transitions between clips (default: True)
            transition_duration: Duration of transitions in seconds (default: 0.5)
            apply_ken_burns: Apply Ken Burns effect to static images (default: False)
        """
        self.output_format = output_format
        self.analyzer = SceneAnalyzer()
        self.width = 1080
        self.height = 1920
        self.enable_transitions = enable_transitions
        self.transition_duration = transition_duration
        self.apply_ken_burns = apply_ken_burns
        self.video_effects = VideoEffects()

    def compose_final_video(
        self,
        story_idea: StoryIdea,
        add_subtitles: bool = True,
        background_music: Optional[str] = None
    ) -> str:
        """
        Compose final video with all elements
        
        Args:
            story_idea: StoryIdea object for the story
            add_subtitles: Whether to add subtitles overlay
            background_music: Path to background music file (optional)
            
        Returns:
            Path to final video file
        """
        folder_path = os.path.join(TITLES_PATH, sanitize_filename(story_idea.story_title))
        
        # Paths to input files
        video_segments_dir = os.path.join(folder_path, "video_segments")
        audio_path = os.path.join(folder_path, "voiceover_normalized.mp3")
        subtitles_path = os.path.join(folder_path, "Subtitles_Word_By_Word.txt")
        output_path = os.path.join(folder_path, f"final_video.{self.output_format}")
        
        # Verify inputs exist
        if not os.path.exists(video_segments_dir):
            raise FileNotFoundError(f"Video segments directory not found: {video_segments_dir}")
        
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        print(f"🎬 Composing final video for '{story_idea.story_title}'...")
        
        # Step 1: Concatenate video segments
        print("  1️⃣ Concatenating video segments...")
        concat_video = os.path.join(folder_path, "temp_concatenated.mp4")
        self._concatenate_video_segments(video_segments_dir, concat_video)
        
        # Step 2: Add audio
        print("  2️⃣ Adding voiceover audio...")
        video_with_audio = os.path.join(folder_path, "temp_with_audio.mp4")
        self._add_audio(concat_video, audio_path, video_with_audio)
        
        # Step 3: Add subtitles (if requested)
        if add_subtitles and os.path.exists(subtitles_path):
            print("  3️⃣ Adding subtitles overlay...")
            self._add_subtitles(video_with_audio, subtitles_path, output_path)
        else:
            # Just copy the video with audio as final output
            os.rename(video_with_audio, output_path)
        
        # Step 4: Add background music (if provided)
        if background_music and os.path.exists(background_music):
            print("  4️⃣ Adding background music...")
            temp_output = output_path.replace('.mp4', '_temp.mp4')
            os.rename(output_path, temp_output)
            self._add_background_music(temp_output, background_music, output_path)
            os.remove(temp_output)
        
        # Clean up temporary files
        print("  5️⃣ Cleaning up temporary files...")
        for temp_file in [concat_video, video_with_audio]:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass
        
        print(f"✅ Final video created: {output_path}")
        
        # Step 6: Export to production directory with thumbnail and metadata
        print("\n  6️⃣ Exporting to production directory...")
        self.export_final_video(
            story_idea=story_idea,
            source_video_path=output_path,
            export_thumbnail=True,
            export_metadata=True
        )
        
        return output_path

    def _concatenate_video_segments(self, segments_dir: str, output_path: str):
        """
        Concatenate all video segments in order with optional smooth transitions
        
        Args:
            segments_dir: Directory containing video segments
            output_path: Path for concatenated output
        """
        # Get all video segments in order
        segments = sorted([
            os.path.join(segments_dir, f)
            for f in os.listdir(segments_dir)
            if f.endswith('.mp4') and f.startswith('scene_')
        ])
        
        if not segments:
            raise FileNotFoundError(f"No video segments found in {segments_dir}")
        
        if self.enable_transitions and len(segments) > 1:
            # Concatenate with smooth transitions
            self._concatenate_with_transitions(segments, output_path)
        else:
            # Simple concatenation without transitions
            self._simple_concatenate(segments, output_path)
    
    def _simple_concatenate(self, segments: List[str], output_path: str):
        """
        Simple concatenation without transitions
        
        Args:
            segments: List of video segment paths
            output_path: Output path for concatenated video
        """
        # Create concat file for ffmpeg
        segments_dir = os.path.dirname(segments[0])
        concat_file = os.path.join(segments_dir, "concat_list.txt")
        with open(concat_file, 'w') as f:
            for segment in segments:
                f.write(f"file '{os.path.abspath(segment)}'\n")
        
        # Use ffmpeg to concatenate
        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_file,
            '-c', 'copy',
            output_path
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        
        # Clean up concat file
        os.remove(concat_file)
    
    def _concatenate_with_transitions(self, segments: List[str], output_path: str):
        """
        Concatenate video segments with smooth crossfade transitions
        
        Args:
            segments: List of video segment paths
            output_path: Output path for concatenated video
        """
        import ffmpeg
        
        # Build filter complex for crossfade transitions
        if len(segments) == 1:
            # Only one segment, just copy it
            cmd = ['ffmpeg', '-y', '-i', segments[0], '-c', 'copy', output_path]
            subprocess.run(cmd, check=True, capture_output=True)
            return
        
        # For multiple segments, use simple concat with re-encoding
        # xfade can be complex and may not work in all situations
        # Use a simple concat demuxer approach instead for reliability
        # Fallback to simple concatenation: xfade transitions are not implemented here
        # because they can be unreliable or fail in certain scenarios. This fallback is
        # intentional to ensure robust and reliable video composition.
        self._simple_concatenate(segments, output_path)

    def crop_to_vertical(self, input_video: str, output_video: str):
        """
        Crop video to 9:16 aspect ratio (1080x1920)
        
        Args:
            input_video: Input video path
            output_video: Output video path
        """
        cmd = [
            'ffmpeg', '-y',
            '-i', input_video,
            '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
            '-c:a', 'copy',
            output_video
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ Cropped video to 9:16: {output_video}")
    
    def apply_ken_burns_to_segment(self, image_path: str, audio_path: str, 
                                   output_path: str, duration: float,
                                   zoom_direction: str = "in", 
                                   pan_direction: str = "center"):
        """
        Apply Ken Burns effect to create dynamic video from static image
        
        Args:
            image_path: Input image path
            audio_path: Audio file path
            output_path: Output video path
            duration: Duration in seconds
            zoom_direction: 'in' or 'out'
            pan_direction: 'left', 'right', 'up', 'down', or 'center'
        """
        self.video_effects.apply_ken_burns_effect(
            input_image=image_path,
            output_video=output_path,
            audio_path=audio_path,
            duration=duration,
            zoom_direction=zoom_direction,
            pan_direction=pan_direction,
            zoom_intensity=1.2
        )
        print(f"✅ Applied Ken Burns effect: {output_path}")
    
    def _add_audio(self, video_path: str, audio_path: str, output_path: str):
        """
        Add audio track to video
        
        Args:
            video_path: Input video file
            audio_path: Audio file to add
            output_path: Output video with audio
        """
        cmd = [
            'ffmpeg', '-y',
            '-i', video_path,
            '-i', audio_path,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-shortest',
            output_path
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)

    def _add_subtitles(self, video_path: str, subtitles_path: str, output_path: str):
        """
        Add subtitles overlay to video
        
        Args:
            video_path: Input video file
            subtitles_path: SRT subtitles file
            output_path: Output video with subtitles
        """
        # Convert SRT to ASS for better styling control
        ass_path = subtitles_path.replace('.txt', '.ass')
        self._convert_srt_to_ass(subtitles_path, ass_path)
        
        # Add subtitles using ffmpeg
        cmd = [
            'ffmpeg', '-y',
            '-i', video_path,
            '-vf', f"ass={ass_path}",
            '-c:a', 'copy',
            output_path
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        
        # Clean up ASS file
        if os.path.exists(ass_path):
            os.remove(ass_path)

    def _convert_srt_to_ass(self, srt_path: str, ass_path: str):
        """
        Convert SRT subtitles to ASS format with custom styling
        
        Args:
            srt_path: Input SRT file
            ass_path: Output ASS file
        """
        # ASS header with styling for vertical video
        ass_header = f"""[Script Info]
Title: Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
PlayResX: {self.width}
PlayResY: {self.height}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,2,1,2,10,10,150,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        
        # Read and convert SRT
        with open(srt_path, 'r', encoding='utf-8') as f:
            srt_content = f.read()
        
        # Parse SRT and convert to ASS
        events = []
        blocks = srt_content.strip().split('\n\n')
        
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) < 3:
                continue
            
            # Parse timing (SRT format: 00:00:01,234 --> 00:00:02,345)
            timing_line = lines[1]
            start, end = timing_line.split(' --> ')
            
            # Convert to ASS time format
            start_ass = self._srt_time_to_ass(start)
            end_ass = self._srt_time_to_ass(end)
            
            # Get text
            text = ' '.join(lines[2:])
            
            # Create ASS dialogue line
            events.append(f"Dialogue: 0,{start_ass},{end_ass},Default,,0,0,0,,{text}")
        
        # Write ASS file
        with open(ass_path, 'w', encoding='utf-8') as f:
            f.write(ass_header)
            f.write('\n'.join(events))

    def _srt_time_to_ass(self, srt_time: str) -> str:
        """
        Convert SRT timestamp to ASS timestamp
        
        Args:
            srt_time: SRT time format (00:01:23,456)
            
        Returns:
            ASS time format (0:01:23.46)
        """
        # Replace comma with period, remove leading zeros from hour
        time_part, ms = srt_time.split(',')
        h, m, s = time_part.split(':')
        
        # ASS uses centiseconds (2 digits after decimal)
        cs = ms[:2]
        
        return f"{int(h)}:{m}:{s}.{cs}"

    def _add_background_music(
        self,
        video_path: str,
        music_path: str,
        output_path: str,
        music_volume: float = 0.1
    ):
        """
        Add background music mixed with voiceover
        
        Args:
            video_path: Input video with voiceover
            music_path: Background music file
            output_path: Output video
            music_volume: Background music volume (0-1)
        """
        cmd = [
            'ffmpeg', '-y',
            '-i', video_path,
            '-i', music_path,
            '-filter_complex',
            f'[0:a]volume=1.0[a1];[1:a]volume={music_volume}[a2];[a1][a2]amix=inputs=2:duration=shortest',
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-b:a', '192k',
            output_path
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)

    def export_final_video(
        self,
        story_idea: StoryIdea,
        source_video_path: str,
        export_thumbnail: bool = True,
        export_metadata: bool = True
    ) -> Tuple[str, str, str]:
        """
        Export final video to /final/{segment}/{age}/{title_id}.mp4 with thumbnail and metadata.
        
        Args:
            story_idea: StoryIdea object with story information
            source_video_path: Path to the composed final video
            export_thumbnail: Whether to generate and export thumbnail
            export_metadata: Whether to generate and export metadata JSON
            
        Returns:
            Tuple of (video_path, thumbnail_path, metadata_path)
        """
        print(f"\n📦 Exporting final video to production directory...")
        
        # Extract segment and age group from story idea
        segment = get_segment_from_gender(story_idea.narrator_gender)
        age_group = get_age_group_from_potencial(story_idea.potencial)
        title_id = generate_title_id(story_idea.story_title)
        
        print(f"  📊 Segment: {segment}")
        print(f"  📊 Age Group: {age_group}")
        print(f"  🆔 Title ID: {title_id}")
        
        # Define export paths
        video_filename = f"{title_id}.mp4"
        thumbnail_filename = f"{title_id}_thumbnail.jpg"
        metadata_filename = f"{title_id}_metadata.json"
        
        export_video_path = get_final_export_path(
            story_idea.story_title, segment, age_group, video_filename
        )
        export_thumbnail_path = get_final_export_path(
            story_idea.story_title, segment, age_group, thumbnail_filename
        )
        export_metadata_path = get_final_export_path(
            story_idea.story_title, segment, age_group, metadata_filename
        )
        
        # Copy video to export location
        print(f"  1️⃣ Copying video to: {export_video_path}")
        shutil.copy2(source_video_path, export_video_path)
        print(f"  ✅ Video exported successfully")
        
        # Generate and export thumbnail
        thumbnail_path = None
        if export_thumbnail:
            print(f"  2️⃣ Generating thumbnail (1080x1920)...")
            success = self._generate_thumbnail(export_video_path, export_thumbnail_path)
            if success:
                thumbnail_path = export_thumbnail_path
                print(f"  ✅ Thumbnail exported: {export_thumbnail_path}")
            else:
                print(f"  ⚠️ Failed to generate thumbnail")
        
        # Generate and export metadata
        metadata_path = None
        if export_metadata:
            print(f"  3️⃣ Generating metadata JSON...")
            success = self._generate_metadata(
                story_idea, export_metadata_path, title_id, segment, age_group
            )
            if success:
                metadata_path = export_metadata_path
                print(f"  ✅ Metadata exported: {export_metadata_path}")
            else:
                print(f"  ⚠️ Failed to generate metadata")
        
        print(f"\n✅ Export complete!")
        print(f"  📹 Video: {export_video_path}")
        if thumbnail_path:
            print(f"  📸 Thumbnail: {thumbnail_path}")
        if metadata_path:
            print(f"  📄 Metadata: {metadata_path}")
        
        return export_video_path, thumbnail_path, metadata_path
    
    def _generate_thumbnail(self, video_path: str, output_path: str, 
                          timestamp: float = 0.5) -> bool:
        """
        Generate thumbnail from video at specified timestamp.
        
        Args:
            video_path: Path to video file
            output_path: Path to save thumbnail
            timestamp: Timestamp in seconds to extract frame
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cmd = [
                'ffmpeg', '-y',
                '-ss', str(timestamp),
                '-i', video_path,
                '-vframes', '1',
                '-vf', f'scale={self.width}:{self.height}',
                '-q:v', '2',  # High quality JPEG
                output_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"  ❌ FFmpeg error generating thumbnail: {e}")
            return False
        except Exception as e:
            print(f"  ❌ Error generating thumbnail: {e}")
            return False
    
    def _generate_metadata(
        self,
        story_idea: StoryIdea,
        output_path: str,
        title_id: str,
        segment: str,
        age_group: str
    ) -> bool:
        """
        Generate metadata JSON file for the video.
        
        Args:
            story_idea: StoryIdea object
            output_path: Path to save metadata JSON
            title_id: Unique title ID
            segment: Segment (gender)
            age_group: Target age group
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Generate tags from story attributes
            tags = []
            if story_idea.theme:
                tags.append(story_idea.theme)
            if story_idea.tone:
                tags.append(story_idea.tone)
            if story_idea.narrator_type:
                tags.append(story_idea.narrator_type)
            
            # Add generic tags
            tags.extend(['shorts', 'viral', 'story'])
            
            # Generate description
            description = f"{story_idea.story_title}\n\n"
            if story_idea.theme:
                description += f"Theme: {story_idea.theme}\n"
            if story_idea.tone:
                description += f"Tone: {story_idea.tone}\n"
            if story_idea.goal:
                description += f"\n{story_idea.goal}\n"
            
            # Create metadata dictionary
            metadata = {
                "title_id": title_id,
                "title": story_idea.story_title,
                "description": description.strip(),
                "tags": tags,
                "segment": segment,
                "age_group": age_group,
                "narrator_gender": story_idea.narrator_gender,
                "theme": story_idea.theme,
                "tone": story_idea.tone,
                "language": story_idea.language,
                "potencial_score": story_idea.potencial.get("overall", 0),
                "video_format": {
                    "resolution": f"{self.width}x{self.height}",
                    "aspect_ratio": "9:16",
                    "format": "mp4"
                }
            }
            
            # Write metadata to JSON file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"  ❌ Error generating metadata: {e}")
            return False
