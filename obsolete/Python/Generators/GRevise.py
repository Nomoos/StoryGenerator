import os
import shutil
import time

import openai
from dotenv import load_dotenv

from Models.StoryIdea import StoryIdea
from Tools.Utils import SCRIPTS_PATH, sanitize_filename, IDEAS_PATH, REVISED_PATH, loadScript
from Tools.Monitor import logger, PerformanceMonitor, log_error, log_info
from Tools.Retry import retry_with_exponential_backoff, with_circuit_breaker
from Tools.Validator import OutputValidator

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please check your .env file.")

class RevisedScriptGenerator:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
    def Revise(self, storyIdea: StoryIdea):
        operation_start = time.time()
        success = False
        error_msg = None
        metrics = {}
        
        try:
            self.moveFolder(storyIdea)
            script = loadScript(storyIdea)
            metrics["original_length"] = len(script)
            
            messages = [
                {"role": "system", "content": self._build_system_prompt()},
                {"role": "user", "content": self._build_user_prompt(script)}
            ]
            
            response = self._call_openai_with_retry(messages)
            revised_script = response.choices[0].message.content.strip()
            metrics["revised_length"] = len(revised_script)
            metrics["word_count"] = len(revised_script.split())
            
            self.save_revised_script(storyIdea, revised_script)
            
            # Validate output
            revised_path = os.path.join(REVISED_PATH, sanitize_filename(storyIdea.story_title), "Revised.txt")
            is_valid, validation_metrics = OutputValidator.validate_text_file(revised_path, min_length=200)
            metrics.update(validation_metrics)
            
            if not is_valid:
                error_msg = "Revised script failed validation"
                log_error("Script Revision Validation", storyIdea.story_title, Exception(error_msg))
            else:
                success = True
                log_info(f"✅ Script revised: {metrics['word_count']} words")
                
        except Exception as e:
            error_msg = str(e)
            log_error("Script Revision", storyIdea.story_title, e)
            raise
        finally:
            duration = time.time() - operation_start
            PerformanceMonitor.log_operation(
                operation="Script_Revision",
                story_title=storyIdea.story_title,
                duration=duration,
                success=success,
                error=error_msg,
                metrics=metrics
            )
    
    @retry_with_exponential_backoff(
        max_retries=3,
        base_delay=2.0,
        max_delay=30.0,
        exceptions=(Exception,)
    )
    @with_circuit_breaker("openai")
    def _call_openai_with_retry(self, messages):
        """Call OpenAI API with retry logic and circuit breaker."""
        return openai.ChatCompletion.create(model=self.model, messages=messages)

    def _build_system_prompt(self) -> str:
        return f"""
            You are a professional viral storyteller. Your job is to rewrite and improve real-life or Reddit-style stories for short-form videos on TikTok, YouTube Shorts, and Instagram Reels. These stories must sound like someone is telling them out loud — naturally, emotionally, and conversationally. You are not writing for the page. You are writing for the ear.
        
            The target audience is people in the United States between ten and thirty years old. They care about emotional drama, awkward moments, rebellion, identity, and finding connection in a chaotic world.
        
            The final output must be a single block of clean, natural spoken narration. No formatting, no tags, no stage directions, no emojis, no labels — just what would be said aloud.
        
            Avoid all abbreviations and shorthand like “IDK,” “LOL,” “’00s,” “etc.,” or “TBH.” Always write them out fully. Say “I don’t know” instead of “IDK” and “the early two-thousands” instead of “’00s.”
        
            🟢 **Always prioritize clarity and flow in speech.** Avoid clunky phrasing, stacked consonants, or abstract terms that sound stiff or overly formal when read aloud. Don’t use phrases like “a force of unapologetic self-expression” or “platform flip-flops” unless they truly roll off the tongue. Choose vivid, concrete, human language.
        
            Use simple grammar and everyday words. Keep sentences short to medium-length. Break thoughts into natural pauses. No semicolons or stacked punctuation. Think rhythm, not rules.
        
            Start with a strong hook — a moment of emotion, confusion, or tension. Build curiosity. Let feelings unfold naturally. Show emotion through thoughts and choices, not by labeling it.
        
            End with power — a shift, a twist, a realization, or a moment that lingers. The final line should make the listener stop and think.
        
            Output only the clean, finished spoken narration. Nothing else.
            """.strip()

    def _build_user_prompt(self, script: str) -> str:
        return f"""
            Please rewrite the following story into a natural, emotionally engaging narration for short-form video. Follow all the style and formatting rules from the system prompt.
        
            Make sure it reads smoothly when spoken by realistic AI voices like ElevenLabs. Use clean, expressive phrasing with a natural rhythm. Favor short, clear sentences. Use commas or new lines to guide pacing, but avoid overusing punctuation.
        
            🟢 Polish every line for spoken clarity. Remove or rephrase anything that might sound stiff, robotic, or awkward when read aloud. Replace abstract, heavy phrases with vivid, human language. Watch out for clunky word combinations like “platform flip-flops,” “unapologetic self-expression,” or long noun strings. Everything should feel like something a real person would say confidently and smoothly.
        
            No tags, no formatting, no headings — just the final spoken narration. Return only the clean text.
        
            Story:
            {script.strip()}
            """.strip()

    def save_revised_script(self, idea: StoryIdea, script: str):
        folder_path = os.path.join(REVISED_PATH, sanitize_filename(idea.story_title))
        os.makedirs(folder_path, exist_ok=True)

        revised_file = os.path.join(folder_path, "Revised.txt")  # or 'final.txt', if you prefer

        with open(revised_file, "w", encoding="utf-8") as f:
            f.write(script.strip())

        print(f"Revised script saved to: {revised_file}")



    def moveFolder(self, storyIdea):
        script_path = os.path.join(SCRIPTS_PATH, sanitize_filename(storyIdea.story_title))
        revised_path = os.path.join(REVISED_PATH, sanitize_filename(storyIdea.story_title))

        if not os.path.exists(script_path):
            print(f"Source folder does not exist: {script_path}")
            return

        if os.path.exists(revised_path):
            print(f"Destination folder already exists. Removing: {revised_path}")
            shutil.rmtree(revised_path)

        try:
            shutil.move(script_path, revised_path)
            print(f"Moved story folder from '{script_path}' to '{revised_path}'")
        except Exception as e:
            print(f"Error moving folder: {e}")

    def loadScript(storyIdea):
        folder_path = os.path.join(REVISED_PATH, sanitize_filename(storyIdea.story_title))
        script_file = os.path.join(folder_path, "Script.txt")  # Adjust filename as needed

        if not os.path.exists(script_file):
            raise FileNotFoundError(f"Script file not found: {script_file}")

        with open(script_file, "r", encoding="utf-8") as f:
            return f.read().strip()
