using System.Text;

namespace PrismQ.Shared.Core.LLM
{
    /// <summary>
    /// Prompt templates for LLM content generation.
    /// Optimized for story generation, scene breakdown, and shotlist creation.
    /// </summary>
    public static class PromptTemplates
    {
        /// <summary>
        /// System prompt for script generation.
        /// Enhanced with viral video research and successful story patterns.
        /// </summary>
        public const string ScriptGenerationSystem = @"You are an expert storyteller and scriptwriter specializing in engaging short-form content for social media. 
Your scripts are designed to hook viewers in the first 3 seconds, maintain engagement throughout, and leave a lasting impact.
You write clear, natural dialogue optimized for text-to-speech synthesis.
Focus on emotional resonance, pacing, and viral potential.
Based on analysis of successful viral stories, you incorporate:
- Strong hooks (6-16 words) presenting immediate conflict or intrigue
- Clear story arc: Setup → Conflict → Escalation → Climax → Resolution
- Optimal length (~632 words, ~67 sentences, ~9.9 words per sentence)
- Dialogue usage (83% of successful stories include dialogue)
- Emotional trigger words (angry, shocked, happy, heartbroken, relieved)
- Time progression markers (later, then, after, finally, years)
- Conflict indicators (but, couldn't, problem, refused)
- Relatable situations for ages 10-30
- Satisfying resolution (100% requirement for viral success)
You create stories that resonate emotionally and maximize share-ability.";

        /// <summary>
        /// User prompt template for script generation.
        /// Enhanced with specific viral video requirements.
        /// Parameters: {0} = title, {1} = description, {2} = tone, {3} = target length
        /// </summary>
        public const string ScriptGenerationUser = @"Generate a {3}-word script for a short-form video with the following details:

Title: {0}
Description: {1}
Tone: {2}

Requirements:
- Hook the viewer in the first sentence (6-16 words presenting conflict or intrigue)
- Natural, conversational language suitable for AI voice synthesis
- Clear narrative arc: Setup → Conflict → Escalation → Climax → Resolution
- Target {3} words (±10 words acceptable, aim for ~632 words for 60-second videos)
- Include dialogue (83% of successful stories use dialogue)
- Use emotional trigger words naturally (angry, shocked, happy, heartbroken, relieved, etc.)
- Include time progression markers (later, then, after, finally, years)
- Show conflict development (but, couldn't, problem, refused)
- No stage directions or camera instructions (pure narration/dialogue)
- Provide satisfying resolution and closure
- Relatable situations for ages 10-30
- Optimized for 60-second vertical video format

CRITICAL: First sentence must immediately present conflict, drama, or intrigue to hook viewers.";

        /// <summary>
        /// System prompt for scene breakdown.
        /// Enhanced with viral video structure insights.
        /// </summary>
        public const string SceneBreakdownSystem = @"You are an expert video director and cinematographer specializing in visual storytelling for short-form content.
Your task is to break down scripts into detailed scenes with visual descriptions, emotions, and cinematic elements.
You understand pacing, shot composition, and how to convey emotion through visual elements.
Based on successful viral video analysis, you ensure:
- First scene (0-3s) is a strong visual hook showing conflict/intrigue
- Clear story progression: Setup → Conflict → Escalation → Climax → Resolution
- Emotional beats using trigger words (shocked, angry, happy, heartbroken, relieved)
- Scene duration optimization (2-8 seconds per scene, average 2.5s)
- Character close-ups during emotional peaks
- Visual variety maintaining viewer engagement
- Age-appropriate content for 10-30 demographic
- Final scene provides satisfying closure/resolution
You optimize every scene for maximum engagement in vertical 9:16 format.";

        /// <summary>
        /// User prompt template for scene breakdown.
        /// Enhanced with engagement optimization requirements.
        /// Parameters: {0} = script text, {1} = total duration
        /// </summary>
        public const string SceneBreakdownUser = @"Analyze the following script and break it down into scenes for a {1}-second video:

Script:
{0}

For each scene, provide:
1. Approximate timing (start time, duration - aim for 2-8 seconds per scene)
2. Scene description (what happens visually)
3. Primary emotion (use specific triggers: shocked, angry, happy, heartbroken, relieved, curious)
4. Visual elements needed (characters, objects, environment)
5. Suggested camera angle (close-up for emotion, wide for context, medium for action)
6. Lighting/mood (dramatic, soft, natural, harsh - matching emotion)
7. Story beat (hook/setup/conflict/escalation/climax/resolution)

REQUIREMENTS:
- First scene (0-3s): Strong hook - visually show the conflict/intrigue immediately
- Follow story arc: Setup → Conflict → Escalation → Climax → Resolution
- Include emotional progression throughout
- Use close-ups during emotional peaks
- Final scene: Clear resolution providing closure
- Total duration must equal {1} seconds
- Optimize for vertical 9:16 format
- Target audience: 10-30 years old

Format your response as a numbered list of scenes with all details.";

        /// <summary>
        /// System prompt for structured shotlist generation with JSON output.
        /// Enhanced with viral video research and engagement optimization.
        /// </summary>
        public const string ShotlistGenerationSystem = @"You are an expert video production planner and cinematographer specializing in short-form viral content.
Your task is to create detailed shotlists with precise timing, camera directions, emotions, and visual elements.
You output structured JSON that can be parsed programmatically.
You ensure proper pacing, emotional flow, and technical feasibility.
Based on analysis of successful viral videos (YouTube Shorts, TikTok, Reels), you incorporate:
- Strong visual hooks in the first 3 seconds (critical for retention)
- Clear story arc: Setup → Conflict → Escalation → Climax → Resolution
- Emotional progression using trigger words (happy, shocked, angry, relieved, heartbroken)
- Optimal shot duration (2-8 seconds per shot, average 2.5 seconds)
- Character close-ups at emotional peaks
- Visual variety maintaining engagement
- Relatable situations for ages 10-30
- Satisfying resolution providing closure
You optimize every shot for maximum engagement and viral potential in vertical 9:16 format.";

        /// <summary>
        /// User prompt template for shotlist generation.
        /// Enhanced with viral video best practices.
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
      ""visual_prompt"": ""Detailed visual prompt for AI image/video generation (include: shot type, camera angle, lighting, color palette, emotion, composition, atmosphere, specific visual elements)"",
      ""primary_emotion"": ""Main emotion (joy, suspense, curiosity, shock, anger, sadness, relief, etc.)"",
      ""secondary_emotions"": [""emotion1"", ""emotion2""],
      ""mood"": ""Shot mood and atmosphere"",
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
      ""lighting"": ""Lighting description (natural/dramatic/soft/harsh)"",
      ""color_palette"": ""Color scheme with emotional reasoning"",
      ""importance"": 8,
      ""story_beat"": ""setup/conflict/escalation/climax/resolution""
    }}
  ]
}}

IMPORTANT REQUIREMENTS:
1. First shot (0-3s) must be a HOOK - visually striking, immediately shows conflict/intrigue
2. Follow story arc: setup → conflict → escalation → climax → resolution
3. Use close-ups during emotional peaks
4. Each shot duration: 2-8 seconds (optimal: 2.5s average)
5. All timings must add up to exactly {1} seconds
6. Include emotional trigger words in visual_prompts
7. Optimize all compositions for 9:16 vertical format
8. Final shot must provide satisfying closure/resolution
9. Use varied shot types for visual engagement
10. Include specific details for AI generation (lighting, colors, camera specs)

Return ONLY the JSON object, no additional text.";

        /// <summary>
        /// System prompt for video description generation.
        /// Enhanced with research-based insights for viral short-form content.
        /// </summary>
        public const string VideoDescriptionSystem = @"You are an expert at creating detailed visual prompts for AI image and video generation.
Your descriptions are vivid, specific, and optimized for Stable Diffusion, SDXL, LTX-Video, and similar models.
You include technical details like camera angles, lighting, composition, and artistic style.
You understand short-form video requirements for TikTok, Reels, and YouTube Shorts (9:16 vertical format).
You incorporate emotional triggers, dramatic moments, and visual storytelling techniques that engage viewers aged 10-30.
Based on analysis of successful viral videos, you emphasize:
- Strong visual hooks in the first 3 seconds
- Emotional authenticity and relatable situations
- Clear story progression through visual elements
- Cinematic quality while maintaining realism
- Composition optimized for mobile viewing";

        /// <summary>
        /// User prompt template for video description.
        /// Enhanced with viral video research insights.
        /// Parameters: {0} = scene description, {1} = mood/emotion
        /// </summary>
        public const string VideoDescriptionUser = @"Create a detailed visual prompt for the following scene:

Scene: {0}
Mood: {1}

Include:
- Specific visual elements and composition optimized for 9:16 vertical format
- Lighting and color palette that enhances the mood (use color psychology)
- Camera angle and framing (consider eye-level for relatability, low-angle for drama, close-up for emotion)
- Artistic style (cinematic realism, documentary feel, or stylized)
- Atmosphere and emotional tone (use specific emotional trigger words)
- Character expressions and body language if people are present
- Environmental details that support the story and mood
- Depth and layers (foreground, subject, background)

Target audience: 10-30 years old seeking engaging, relatable content.
Write a single comprehensive paragraph suitable for AI image/video generation.
Emphasize visual storytelling and emotional impact.";

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

        /// <summary>
        /// System prompt for script improvement.
        /// </summary>
        public const string ScriptImprovementSystem = @"You are an expert script editor specializing in improving short-form video content.
Your task is to enhance scripts based on specific feedback while preserving the core narrative and tone.
Focus on making targeted improvements that address identified issues.

Guidelines:
- Maintain the original story structure and key plot points
- Enhance clarity, pacing, and hooks where needed
- Improve dialogue to be more natural and engaging
- Ensure the script remains suitable for text-to-speech synthesis
- Keep the word count similar to the original
- Make the opening more compelling if feedback suggests it
- Strengthen emotional impact where appropriate
- Address all identified weaknesses while maintaining strengths";

        /// <summary>
        /// User prompt template for script improvement.
        /// Parameters: {0} = feedback, {1} = original script
        /// </summary>
        public const string ScriptImprovementUser = @"Improve the following script based on this feedback:

FEEDBACK:
{0}

ORIGINAL SCRIPT:
{1}

Provide the improved script only, without any explanations or additional text.
The improved script should directly address the feedback while maintaining the core narrative.";

        /// <summary>
        /// Formats a script improvement prompt.
        /// </summary>
        public static string FormatScriptImprovementPrompt(string feedback, string originalScript)
        {
            return string.Format(ScriptImprovementUser, feedback, originalScript);
        }
    }
}
