"""
Vision model prompts for quality assessment and consistency validation.
"""

# Quality assessment prompt for single images
QUALITY_PROMPT = """Analyze this image for quality and composition. Provide scores from 0-10 for each category:

1. Overall quality (sharpness, clarity, artifacts): [score 0-10]
2. Composition (framing, rule of thirds, balance): [score 0-10]
3. Lighting quality (exposure, shadows, highlights): [score 0-10]
4. Subject clarity (focus on main subject): [score 0-10]

Also indicate:
- Are there visible artifacts or errors? (yes/no)
- Brief reasoning for your scores (1-2 sentences)

Format your response as:
Overall: X/10
Composition: X/10
Lighting: X/10
Subject: X/10
Artifacts: yes/no
Reasoning: [your brief explanation]"""

# Consistency check prompt for image pairs
CONSISTENCY_PROMPT = """Compare these two consecutive scene images for visual consistency. Provide scores from 0-10 for each category:

1. Character appearance consistency (if characters present): [score 0-10]
2. Style consistency (artistic style, color palette): [score 0-10]
3. Lighting consistency (lighting direction, quality): [score 0-10]
4. Overall visual continuity: [score 0-10]

Also list:
- Any noticeable inconsistencies
- Brief reasoning for your scores

Format your response as:
Character: X/10
Style: X/10
Lighting: X/10
Continuity: X/10
Inconsistencies: [list any issues]
Reasoning: [your brief explanation]"""

# Caption generation prompt
CAPTION_PROMPT = """Describe this image in detail. Focus on:
- Main subjects and their actions
- Setting and environment
- Mood and atmosphere
- Visual style
- Notable details

Provide a clear, descriptive caption in 2-3 sentences."""

# Descriptive analysis prompt for storyboard validation
DESCRIPTIVE_PROMPT = """Analyze this image and provide a detailed description including:

1. **Main Subject**: What/who is the focus?
2. **Action/Pose**: What is happening?
3. **Setting**: Where does this take place?
4. **Mood**: What emotion or atmosphere does it convey?
5. **Style**: What is the visual style (realistic, cartoon, etc.)?
6. **Composition**: How is the image framed?
7. **Key Details**: Any notable elements?

Be specific and objective in your description."""

# Reference image analysis prompt
REFERENCE_ANALYSIS_PROMPT = """Analyze this reference image to extract visual parameters for image generation:

1. **Style Keywords**: List 3-5 style descriptors (e.g., "photorealistic", "cinematic", "painterly")
2. **Color Palette**: Describe the dominant colors and color scheme
3. **Lighting**: Describe the lighting setup (direction, quality, mood)
4. **Composition**: Note framing, perspective, and layout
5. **Texture/Detail**: Note the level of detail and texture quality
6. **Suggested Parameters**: List specific parameters that could be used for SDXL/Stable Diffusion

Format as a structured list."""

# Multi-image sequence validation
SEQUENCE_VALIDATION_PROMPT = """You are viewing a sequence of images that should form a cohesive visual story. Analyze the sequence for:

1. **Visual Flow**: Do the images flow naturally from one to another?
2. **Style Consistency**: Is the visual style consistent throughout?
3. **Character Consistency**: Are characters (if present) consistent across frames?
4. **Narrative Coherence**: Do the visuals support a clear narrative progression?
5. **Technical Quality**: Are all images of comparable quality?

Provide:
- Overall sequence score (0-10)
- Specific issues or breaks in continuity
- Recommendations for improvement

Format your analysis clearly."""

# Error detection prompt
ERROR_DETECTION_PROMPT = """Examine this image carefully for visual errors or artifacts:

1. **Anatomical Errors**: Incorrect body proportions, extra limbs, distorted features
2. **Logical Errors**: Physically impossible elements, perspective issues
3. **Technical Artifacts**: Blurring, noise, compression artifacts, duplicate elements
4. **Inconsistencies**: Objects or elements that don't fit the scene

List any errors found with:
- Error type
- Location in image
- Severity (minor/moderate/major)

If no significant errors, respond with "No major errors detected." """

# Composition scoring prompt
COMPOSITION_SCORING_PROMPT = """Rate this image's composition using professional photography/cinematography standards:

1. **Rule of Thirds**: Is the subject well-positioned? (0-10)
2. **Balance**: Is the image visually balanced? (0-10)
3. **Leading Lines**: Are there effective leading lines or visual flow? (0-10)
4. **Depth**: Is there good use of foreground, midground, background? (0-10)
5. **Framing**: Is the subject well-framed within the image? (0-10)

Overall Composition Score: X/10
Strengths: [list 1-2]
Improvements: [list 1-2]"""

# Scene-to-prompt alignment check
PROMPT_ALIGNMENT_PROMPT = """Given this image and its intended description/prompt:
Prompt: {prompt}

Assess how well the image matches the prompt:
1. **Subject Match**: Does it show the intended subject? (0-10)
2. **Action/Pose Match**: Are actions/poses correct? (0-10)
3. **Setting Match**: Is the setting/environment correct? (0-10)
4. **Style Match**: Does the style match expectations? (0-10)
5. **Overall Alignment**: How well does it match overall? (0-10)

List any significant mismatches or missing elements.

Format:
Subject: X/10
Action: X/10
Setting: X/10
Style: X/10
Overall: X/10
Mismatches: [list any issues]"""


# Prompt templates mapping
PROMPTS = {
    "quality": QUALITY_PROMPT,
    "consistency": CONSISTENCY_PROMPT,
    "caption": CAPTION_PROMPT,
    "descriptive": DESCRIPTIVE_PROMPT,
    "reference": REFERENCE_ANALYSIS_PROMPT,
    "sequence": SEQUENCE_VALIDATION_PROMPT,
    "error_detection": ERROR_DETECTION_PROMPT,
    "composition": COMPOSITION_SCORING_PROMPT,
    "prompt_alignment": PROMPT_ALIGNMENT_PROMPT,
}


def get_prompt(prompt_type: str, **kwargs) -> str:
    """
    Get a prompt template by type and format with optional parameters.
    
    Args:
        prompt_type: Type of prompt (quality, consistency, caption, etc.)
        **kwargs: Optional parameters to format the prompt
        
    Returns:
        Formatted prompt string
    """
    if prompt_type not in PROMPTS:
        raise ValueError(f"Unknown prompt type: {prompt_type}. Available: {list(PROMPTS.keys())}")
    
    prompt = PROMPTS[prompt_type]
    
    # Format with kwargs if provided
    if kwargs:
        try:
            prompt = prompt.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing required parameter for prompt formatting: {e}")
    
    return prompt
