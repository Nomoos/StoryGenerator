using System.Text;

namespace StoryGenerator.Core.LLM
{
    /// <summary>
    /// Specialized prompt templates for video generation.
    /// Based on analysis of successful YouTube shorts and viral video patterns.
    /// Optimized for emotional storytelling, engagement, and visual impact.
    /// </summary>
    public static class VideoPromptTemplates
    {
        #region Cinematic Video Prompts

        /// <summary>
        /// System prompt for cinematic video generation.
        /// Optimized for dramatic, high-quality visual storytelling.
        /// </summary>
        public const string CinematicVideoSystem = @"You are a master cinematographer and visual storytelling expert.
You create detailed visual prompts optimized for cinematic short-form videos (YouTube Shorts, TikTok, Reels).
Your descriptions incorporate:
- Professional camera techniques (shot types, angles, movements)
- Dramatic lighting and color grading
- Emotional atmosphere and mood
- Cinematic composition (rule of thirds, leading lines, depth)
- Film-quality aesthetics
You ensure all prompts are suitable for AI video generation (Stable Diffusion, SDXL, LTX-Video).";

        /// <summary>
        /// User prompt template for cinematic video scenes.
        /// Parameters: {0} = scene description, {1} = emotion, {2} = duration
        /// </summary>
        public const string CinematicVideoUser = @"Create a cinematic visual prompt for this scene:

Scene: {0}
Primary Emotion: {1}
Duration: {2} seconds

Generate a detailed prompt including:
- Shot type and camera angle (create visual hierarchy)
- Camera movement (if any) to enhance storytelling
- Lighting setup (dramatic, moody, or naturalistic)
- Color palette (warm/cool tones, saturation levels)
- Composition rules (golden ratio, symmetry, depth layers)
- Atmospheric elements (fog, particles, bokeh)
- Film-quality specifications (35mm, anamorphic, depth of field)

Format as a single comprehensive paragraph optimized for AI video generation.
Focus on creating emotional impact and visual engagement for 9:16 vertical format.";

        #endregion

        #region Documentary Style Prompts

        /// <summary>
        /// System prompt for documentary-style video generation.
        /// Optimized for realistic, authentic storytelling.
        /// </summary>
        public const string DocumentaryVideoSystem = @"You are a documentary filmmaker and visual journalist.
You create authentic, realistic visual prompts for documentary-style short videos.
Your descriptions emphasize:
- Natural, unscripted moments
- Realistic lighting and environments
- Genuine emotions and reactions
- Handheld or observational camera work
- Real-world settings and details
- Journalistic authenticity
You ensure prompts generate believable, relatable visuals for social media audiences.";

        /// <summary>
        /// User prompt template for documentary-style scenes.
        /// Parameters: {0} = scene description, {1} = setting, {2} = mood
        /// </summary>
        public const string DocumentaryVideoUser = @"Create a realistic, documentary-style visual prompt:

Scene: {0}
Setting: {1}
Mood: {2}

Generate a prompt including:
- Natural, candid framing
- Realistic lighting (available light, practical sources)
- Authentic environment details
- Genuine emotional expressions
- Camera style (handheld, static, observational)
- Real-world textures and imperfections
- Relatable visual elements for ages 10-30

Write as a single paragraph optimized for photorealistic AI generation.
Emphasize authenticity and emotional relatability for vertical video format.";

        #endregion

        #region Emotional Storytelling Prompts

        /// <summary>
        /// System prompt for emotional storytelling video generation.
        /// Based on analysis showing successful stories use emotional trigger words.
        /// </summary>
        public const string EmotionalStoryVideoSystem = @"You are an expert in emotional visual storytelling for short-form video content.
You understand the psychology of engagement and viral content.
Based on analysis of successful YouTube stories, you incorporate:
- Emotional trigger words (angry, happy, shocked, heartbroken, relieved)
- Visual metaphors for feelings
- Character expressions and body language
- Color psychology for emotional impact
- Dramatic moments and turning points
- Resolution and catharsis
Your prompts create visually compelling emotional narratives that resonate with viewers aged 10-30.";

        /// <summary>
        /// User prompt template for emotional story scenes.
        /// Parameters: {0} = story beat, {1} = primary emotion, {2} = secondary emotions (comma-separated)
        /// </summary>
        public const string EmotionalStoryVideoUser = @"Create an emotionally powerful visual prompt for this story moment:

Story Beat: {0}
Primary Emotion: {1}
Secondary Emotions: {2}

Generate a prompt that captures:
- Facial expressions conveying {1}
- Body language and posture reflecting emotional state
- Color palette supporting the mood (warm for happy/angry, cool for sad/lonely)
- Lighting that enhances emotion (dramatic shadows, soft glow, harsh contrast)
- Environmental elements that mirror feelings
- Composition emphasizing isolation or connection
- Visual cues for emotional progression

Format as a cinematic prompt optimized for emotional impact in 9:16 format.
Target audience: 10-30 years old seeking relatable, dramatic content.";

        #endregion

        #region Action and Dynamic Movement Prompts

        /// <summary>
        /// System prompt for action-oriented video scenes.
        /// </summary>
        public const string ActionVideoSystem = @"You are an action cinematography specialist.
You create dynamic, energetic visual prompts for fast-paced video content.
Your descriptions feature:
- Dynamic camera movements (tracking, whip pans, zooms)
- Motion blur and speed effects
- High energy compositions
- Dramatic angles (low, high, dutch)
- Action-oriented framing
- Kinetic visual elements
You ensure prompts generate engaging, eye-catching movement for short-form platforms.";

        /// <summary>
        /// User prompt template for action scenes.
        /// Parameters: {0} = action description, {1} = intensity level, {2} = camera movement
        /// </summary>
        public const string ActionVideoUser = @"Create a dynamic action scene prompt:

Action: {0}
Intensity: {1}
Camera Movement: {2}

Generate a prompt featuring:
- {2} camera work following the action
- Motion blur and dynamic composition
- Dramatic camera angle enhancing impact
- High energy lighting and colors
- Fast-paced visual rhythm
- Sense of speed and momentum
- Sharp focus on key action elements

Write as a single paragraph optimized for dynamic AI video generation in 9:16 format.";

        #endregion

        #region Character Close-Up Prompts

        /// <summary>
        /// System prompt for character close-up shots.
        /// Optimized for emotional impact and viewer connection.
        /// </summary>
        public const string CharacterCloseUpSystem = @"You are a portrait cinematographer specializing in emotional close-ups.
You create intimate, powerful character prompts for short-form video.
Your descriptions emphasize:
- Facial micro-expressions
- Eye contact and gaze direction
- Skin texture and realistic details
- Natural lighting on faces
- Shallow depth of field
- Emotional authenticity
- Connection with viewer
You generate prompts that create immediate emotional engagement with the audience.";

        /// <summary>
        /// User prompt template for character close-ups.
        /// Parameters: {0} = character description, {1} = emotion, {2} = lighting mood
        /// </summary>
        public const string CharacterCloseUpUser = @"Create an intimate character close-up prompt:

Character: {0}
Emotion: {1}
Lighting: {2}

Generate a detailed prompt including:
- Close-up or extreme close-up framing
- Facial expression showing {1} (eyes, mouth, brow)
- {2} lighting on face
- Shallow depth of field (f/1.4-2.8)
- Natural skin texture and details
- Eye highlights (catchlights)
- Emotional authenticity and vulnerability
- 9:16 vertical composition

Format for photorealistic portrait generation with emotional depth.
Target: Ages 10-30 seeking relatable human stories.";

        #endregion

        #region Establishing Shot Prompts

        /// <summary>
        /// System prompt for establishing shots and scene setting.
        /// </summary>
        public const string EstablishingshotSystem = @"You are a location scout and establishing shot specialist.
You create immersive environmental prompts that set the scene and mood.
Your descriptions include:
- Wide angle establishing views
- Environmental storytelling
- Atmospheric conditions
- Time of day and lighting
- Architectural and natural elements
- Spatial relationships
- Setting the emotional tone
You ensure prompts create strong context for story scenes in vertical format.";

        /// <summary>
        /// User prompt template for establishing shots.
        /// Parameters: {0} = location, {1} = time of day, {2} = atmosphere
        /// </summary>
        public const string EstablishingShotUser = @"Create an establishing shot prompt:

Location: {0}
Time: {1}
Atmosphere: {2}

Generate a prompt featuring:
- Wide or medium-wide shot of {0}
- {1} lighting conditions
- {2} atmospheric mood
- Environmental storytelling details
- Spatial context and depth
- Color palette supporting the story
- Cinematic composition for 9:16 format

Write as a detailed prompt for scene-setting AI video generation.";

        #endregion

        #region Transition and Beat Prompts

        /// <summary>
        /// System prompt for transition shots between story beats.
        /// </summary>
        public const string TransitionShotSystem = @"You are a video editor and transition specialist.
You create smooth, stylistic transition prompts for story flow.
Your descriptions incorporate:
- Visual metaphors
- Match cuts and graphic matches
- Symbolic imagery
- Smooth motion flow
- Color and light transitions
- Temporal progression
- Emotional bridges
You ensure seamless storytelling through visual transitions.";

        /// <summary>
        /// User prompt template for transition shots.
        /// Parameters: {0} = from scene emotion, {1} = to scene emotion, {2} = transition type
        /// </summary>
        public const string TransitionShotUser = @"Create a transition shot prompt:

From: {0}
To: {1}
Transition Type: {2}

Generate a prompt for:
- Visual bridge from {0} to {1}
- {2} transition style
- Metaphorical or symbolic imagery
- Smooth motion and flow
- Color transition supporting mood shift
- Brief duration (1-2 seconds)
- Cinematic quality

Format for seamless story progression in vertical video.";

        #endregion

        #region Hook Shot Prompts (First 3 Seconds)

        /// <summary>
        /// System prompt for hook shots - critical first 3 seconds.
        /// Based on research showing hooks should be compelling and concise.
        /// </summary>
        public const string HookShotSystem = @"You are a social media video expert specializing in viewer retention.
You create powerful opening shots that hook viewers in the first 3 seconds.
Based on successful viral video analysis:
- Hook length: 6-16 words of visual impact
- Immediate conflict or intrigue presentation
- Strong emotional trigger
- Clear visual action or drama
- Curiosity gap creation
- Relatable situations for ages 10-30
Your prompts generate attention-grabbing opens that maximize watch time.";

        /// <summary>
        /// User prompt template for hook shots.
        /// Parameters: {0} = hook concept, {1} = conflict/intrigue element
        /// </summary>
        public const string HookShotUser = @"Create a powerful hook shot prompt (first 3 seconds):

Hook: {0}
Conflict/Intrigue: {1}

Generate a prompt that:
- Immediately shows {1}
- Creates visual curiosity gap
- Features strong emotion or action
- Uses dramatic composition
- Includes eye-catching elements
- Sets up story question
- Optimized for 9:16 vertical scroll-stopping impact

Write for maximum attention capture in the first 3 seconds.
Target: Stop viewers mid-scroll on TikTok/Reels/Shorts.";

        #endregion

        #region Resolution Shot Prompts

        /// <summary>
        /// System prompt for resolution shots - story payoff.
        /// Research shows 100% of successful stories have clear resolution.
        /// </summary>
        public const string ResolutionShotSystem = @"You are a storytelling expert specializing in satisfying conclusions.
You create powerful resolution shots that provide payoff and closure.
Your descriptions emphasize:
- Emotional catharsis
- Visual satisfaction
- Clear outcome
- Character transformation
- Justice or lesson learned
- Memorable final image
- Sense of completion
You ensure viewers feel satisfied and emotionally fulfilled.";

        /// <summary>
        /// User prompt template for resolution shots.
        /// Parameters: {0} = resolution description, {1} = final emotion, {2} = lesson/payoff
        /// </summary>
        public const string ResolutionShotUser = @"Create a satisfying resolution shot prompt:

Resolution: {0}
Final Emotion: {1}
Payoff: {2}

Generate a prompt showing:
- Clear visual resolution of conflict
- Character expressing {1}
- {2} visually communicated
- Emotional satisfaction
- Memorable final composition
- Sense of closure and completion
- Uplifting or thought-provoking ending

Format for impactful story conclusion in 9:16 format.
Goal: Leave viewers satisfied and likely to share.";

        #endregion

        #region Helper Methods

        /// <summary>
        /// Formats a cinematic video prompt.
        /// </summary>
        public static string FormatCinematicVideoPrompt(string sceneDescription, string emotion, float duration)
        {
            return string.Format(CinematicVideoUser, sceneDescription, emotion, duration);
        }

        /// <summary>
        /// Formats a documentary-style video prompt.
        /// </summary>
        public static string FormatDocumentaryVideoPrompt(string sceneDescription, string setting, string mood)
        {
            return string.Format(DocumentaryVideoUser, sceneDescription, setting, mood);
        }

        /// <summary>
        /// Formats an emotional story video prompt.
        /// </summary>
        public static string FormatEmotionalStoryPrompt(string storyBeat, string primaryEmotion, string secondaryEmotions)
        {
            return string.Format(EmotionalStoryVideoUser, storyBeat, primaryEmotion, secondaryEmotions);
        }

        /// <summary>
        /// Formats an action video prompt.
        /// </summary>
        public static string FormatActionVideoPrompt(string actionDescription, string intensity, string cameraMovement)
        {
            return string.Format(ActionVideoUser, actionDescription, intensity, cameraMovement);
        }

        /// <summary>
        /// Formats a character close-up prompt.
        /// </summary>
        public static string FormatCharacterCloseUpPrompt(string characterDescription, string emotion, string lighting)
        {
            return string.Format(CharacterCloseUpUser, characterDescription, emotion, lighting);
        }

        /// <summary>
        /// Formats an establishing shot prompt.
        /// </summary>
        public static string FormatEstablishingShotPrompt(string location, string timeOfDay, string atmosphere)
        {
            return string.Format(EstablishingShotUser, location, timeOfDay, atmosphere);
        }

        /// <summary>
        /// Formats a transition shot prompt.
        /// </summary>
        public static string FormatTransitionShotPrompt(string fromEmotion, string toEmotion, string transitionType)
        {
            return string.Format(TransitionShotUser, fromEmotion, toEmotion, transitionType);
        }

        /// <summary>
        /// Formats a hook shot prompt.
        /// </summary>
        public static string FormatHookShotPrompt(string hookConcept, string conflictElement)
        {
            return string.Format(HookShotUser, hookConcept, conflictElement);
        }

        /// <summary>
        /// Formats a resolution shot prompt.
        /// </summary>
        public static string FormatResolutionShotPrompt(string resolutionDescription, string finalEmotion, string payoff)
        {
            return string.Format(ResolutionShotUser, resolutionDescription, finalEmotion, payoff);
        }

        #endregion

        #region Advanced System Prompts

        /// <summary>
        /// System prompt for age-appropriate content filtering (10-30 demographic).
        /// </summary>
        public const string AgeAppropriateFilterSystem = @"You are a content moderator ensuring video prompts are appropriate for audiences aged 10-30.
You filter and adjust prompts to:
- Remove explicit or mature content
- Maintain emotional authenticity while being age-appropriate
- Focus on relatable teen and young adult experiences
- Include diverse, inclusive representation
- Avoid harmful stereotypes
- Ensure psychological safety
- Support positive mental health messaging
You maintain engagement while ensuring content is suitable for the target demographic.";

        /// <summary>
        /// System prompt for vertical video optimization (9:16 format).
        /// </summary>
        public const string VerticalVideoOptimizationSystem = @"You are a vertical video format specialist for mobile-first platforms.
You optimize all prompts for 9:16 aspect ratio (1080x1920) including:
- Vertical composition principles
- Mobile viewing ergonomics
- Portrait orientation framing
- Vertical eye flow (top to bottom)
- Safe areas for UI elements (top 8%, bottom 10%)
- Subject positioning for vertical space
- Text and subtitle placement
- Thumb-stopping visual hierarchy
You ensure all prompts generate content optimized for TikTok, Reels, and Shorts.";

        /// <summary>
        /// System prompt for viral potential optimization.
        /// Based on research of successful viral video patterns.
        /// </summary>
        public const string ViralOptimizationSystem = @"You are a viral video strategist with deep knowledge of engagement patterns.
Based on analysis of successful content, you optimize prompts for:
- Immediate visual impact (first 3 seconds crucial)
- Emotional resonance (trigger words: angry, shocked, happy, heartbroken)
- Relatable conflict situations
- Clear story progression (Setup → Conflict → Escalation → Climax → Resolution)
- Satisfying payoff moments
- Shareable moments and reactions
- Curiosity gaps and plot twists
- Justice/karma moments
- Universal human experiences
You maximize the viral potential of every visual prompt.";

        #endregion
    }
}
