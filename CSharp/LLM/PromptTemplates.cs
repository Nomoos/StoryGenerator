using System.Text;

namespace StoryGenerator.Core.LLM
{
    /// <summary>
    /// Prompt templates for LLM content generation.
    /// Optimized for story generation, scene breakdown, and shotlist creation.
    /// </summary>
    public static class PromptTemplates
    {
        /// <summary>
        /// System prompt for script generation.
        /// </summary>
        public const string ScriptGenerationSystem = @"You are an expert storyteller and scriptwriter specializing in engaging short-form content for social media. 
Your scripts are designed to hook viewers in the first 3 seconds, maintain engagement throughout, and leave a lasting impact.
You write clear, natural dialogue optimized for text-to-speech synthesis.
Focus on emotional resonance, pacing, and viral potential.";

        /// <summary>
        /// User prompt template for script generation.
        /// Parameters: {0} = title, {1} = description, {2} = tone, {3} = target length
        /// </summary>
        public const string ScriptGenerationUser = @"Generate a {3}-word script for a short-form video with the following details:

Title: {0}
Description: {1}
Tone: {2}

Requirements:
- Hook the viewer in the first sentence
- Natural, conversational language suitable for AI voice synthesis
- Clear narrative arc with emotional resonance
- Exactly {3} words (±10 words acceptable)
- No stage directions or camera instructions
- Optimized for 60-second video format";

        /// <summary>
        /// System prompt for scene breakdown.
        /// </summary>
        public const string SceneBreakdownSystem = @"You are an expert video director and cinematographer specializing in visual storytelling.
Your task is to break down scripts into detailed scenes with visual descriptions, emotions, and cinematic elements.
You understand pacing, shot composition, and how to convey emotion through visual elements.";

        /// <summary>
        /// User prompt template for scene breakdown.
        /// Parameters: {0} = script text, {1} = total duration
        /// </summary>
        public const string SceneBreakdownUser = @"Analyze the following script and break it down into scenes for a {1}-second video:

Script:
{0}

For each scene, provide:
1. Approximate timing (start time, duration)
2. Scene description
3. Primary emotion
4. Visual elements needed
5. Suggested camera angle
6. Lighting/mood

Format your response as a numbered list of scenes.";

        /// <summary>
        /// System prompt for structured shotlist generation with JSON output.
        /// </summary>
        public const string ShotlistGenerationSystem = @"You are an expert video production planner and cinematographer.
Your task is to create detailed shotlists with precise timing, camera directions, emotions, and visual elements.
You output structured JSON that can be parsed programmatically.
You ensure proper pacing, emotional flow, and technical feasibility.";

        /// <summary>
        /// User prompt template for shotlist generation.
        /// Parameters: {0} = script text, {1} = audio duration
        /// </summary>
        public const string ShotlistGenerationUser = @"Create a detailed shotlist for the following script. Audio duration: {1} seconds.

Script:
{0}

Output a JSON object with the following structure:
{{
  ""story_title"": ""Title from script"",
  ""total_duration"": {1},
  ""overall_mood"": ""Overall emotional tone"",
  ""style"": ""Visual style (cinematic, documentary, etc.)"",
  ""shots"": [
    {{
      ""shot_number"": 1,
      ""start_time"": 0.0,
      ""end_time"": 3.5,
      ""duration"": 3.5,
      ""scene_description"": ""Brief scene description"",
      ""visual_prompt"": ""Detailed visual prompt for image generation"",
      ""primary_emotion"": ""Main emotion (joy, suspense, curiosity, etc.)"",
      ""secondary_emotions"": [""emotion1"", ""emotion2""],
      ""mood"": ""Shot mood"",
      ""camera_direction"": {{
        ""shot_type"": ""wide/medium/close-up/extreme-close-up"",
        ""angle"": ""eye-level/high-angle/low-angle/dutch"",
        ""movement"": ""static/pan-left/pan-right/zoom-in/zoom-out/dolly/tracking"",
        ""focus_point"": ""What to focus on"",
        ""depth_of_field"": ""shallow/deep"",
        ""composition"": ""rule-of-thirds/centered/symmetrical""
      }},
      ""movement_type"": ""static/dynamic"",
      ""transition"": ""cut/fade/dissolve"",
      ""audio_description"": ""What audio/narration happens"",
      ""character_focus"": [""characters or subjects""],
      ""key_elements"": [""element1"", ""element2""],
      ""lighting"": ""Lighting description"",
      ""color_palette"": ""Color scheme"",
      ""importance"": 8
    }}
  ]
}}

Ensure all timings add up to {1} seconds. Each shot should be 2-8 seconds long.
Return ONLY the JSON object, no additional text.";

        /// <summary>
        /// System prompt for video description generation.
        /// </summary>
        public const string VideoDescriptionSystem = @"You are an expert at creating detailed visual prompts for AI image and video generation.
Your descriptions are vivid, specific, and optimized for Stable Diffusion, Midjourney, and similar models.
You include technical details like camera angles, lighting, composition, and artistic style.";

        /// <summary>
        /// User prompt template for video description.
        /// Parameters: {0} = scene description, {1} = mood/emotion
        /// </summary>
        public const string VideoDescriptionUser = @"Create a detailed visual prompt for the following scene:

Scene: {0}
Mood: {1}

Include:
- Specific visual elements and composition
- Lighting and color palette
- Camera angle and framing
- Artistic style (cinematic, realistic, etc.)
- Atmosphere and emotional tone

Write a single paragraph suitable for AI image/video generation.";

        /// <summary>
        /// System prompt for camera direction refinement.
        /// </summary>
        public const string CameraDirectionSystem = @"You are a professional cinematographer with expertise in shot composition and camera direction.
You provide detailed technical specifications for camera work that enhance storytelling.";

        /// <summary>
        /// User prompt template for camera direction.
        /// Parameters: {0} = shot description, {1} = emotion
        /// </summary>
        public const string CameraDirectionUser = @"Provide detailed camera direction for this shot:

Shot: {0}
Emotion: {1}

Specify:
- Shot type (wide, medium, close-up, extreme close-up)
- Camera angle (eye-level, high angle, low angle, dutch angle)
- Camera movement (static, pan, tilt, zoom, dolly, tracking)
- Focus point and depth of field
- Composition guidelines
- Any special techniques

Format as brief bullet points.";

        /// <summary>
        /// Formats a script generation prompt.
        /// </summary>
        public static string FormatScriptPrompt(string title, string description, string tone, int targetLength)
        {
            return string.Format(ScriptGenerationUser, title, description, tone, targetLength);
        }

        /// <summary>
        /// Formats a scene breakdown prompt.
        /// </summary>
        public static string FormatSceneBreakdownPrompt(string scriptText, float totalDuration)
        {
            return string.Format(SceneBreakdownUser, scriptText, totalDuration);
        }

        /// <summary>
        /// Formats a shotlist generation prompt.
        /// </summary>
        public static string FormatShotlistPrompt(string scriptText, float audioDuration)
        {
            return string.Format(ShotlistGenerationUser, scriptText, audioDuration);
        }

        /// <summary>
        /// Formats a video description prompt.
        /// </summary>
        public static string FormatVideoDescriptionPrompt(string sceneDescription, string mood)
        {
            return string.Format(VideoDescriptionUser, sceneDescription, mood);
        }

        /// <summary>
        /// Formats a camera direction prompt.
        /// </summary>
        public static string FormatCameraDirectionPrompt(string shotDescription, string emotion)
        {
            return string.Format(CameraDirectionUser, shotDescription, emotion);
        }
    }
}
