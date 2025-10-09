import os

import openai
from dotenv import load_dotenv

from Tools.Utils import SCRIPTS_PATH, sanitize_filename, IDEAS_PATH, REVISED_PATH, ENHANCED_NAME, REVISED_NAME

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please check your .env file.")


class EnhanceScriptGenerator:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model

    def Enhance(self, folderName: str):
        script = self.loadScript(folderName)
        folder_path = os.path.join(REVISED_PATH, folderName)
        revised_file = os.path.join(folder_path, ENHANCED_NAME)

        if os.path.exists(revised_file):
            print(f"⚠️ Enhanced file already exists: {revised_file}")
            return  # Skip saving to avoid overwriting

        messages = [
            {"role": "system", "content": self._build_system_prompt()},
            {"role": "user", "content": self._build_user_prompt(script)}
        ]
        response = openai.ChatCompletion.create(model=self.model, messages=messages)
        script = response.choices[0].message.content.strip()
        self.save_enhanced_script(folderName, script)

    def _build_system_prompt(self) -> str:
        return f"""
            You are a voice performance director. Your task is to enhance a narration script by inserting **non-spoken ElevenLabs v3 audio tags** into the original story — **without rewriting or changing any text**.
        
            🎯 Objective:  
            Make the story sound like it’s being told by a real 12–18-year-old girl in the U.S. — emotional, relatable, and believable. Add tags only where emotion, pacing, or realism clearly improves the narration.
        
            🛑 Do NOT:
            - Reword, rewrite, or fix anything
            - Change punctuation, grammar, or spelling
            - Add comments, explanations, or formatting
            - Tag every line — use tags only where needed
        
            ✅ Use only these tags, in this order of relevance for teen voice:
        
            **💖 Emotional tone & relatability**  
            [embarrassed], [hopeful], [sad], [excited], [relieved], [confused], [disappointed], [sincere]
        
            **🧠 Internal reactions & anxiety**  
            [hesitates], [sighs], [gulps], [gasps], [crying], [starts to say something], [trailing off]
        
            **🎭 Tone & style**  
            [playfully], [sarcastic], [speaking softly], [whispers], [deadpan], [matter-of-fact]
        
            **⏱️ Rhythm & pacing**  
            [pause], [long pause], [slowly], [rushed]
        
            **⚠️ Rare or intense**  
            [angry], [shouting], [terrified], [laughs], [groans], [clears throat], [inhales], [exhales], [snorts]
        
            📏 Tagging rules:
            - Max **3 tags per paragraph**
            - Max **2 tags stacked**
            - Tags go **before** the line or phrase they affect
            - If unsure, **leave it untagged**
            - Use order: **[emotion][reaction][pacing]**
        
            📘 Example:
            > [hesitates][sad] I looked at him and said I was done.  
            > [pause][playfully] You’re kidding… right?  
            > I made breakfast and sat on the couch. (no tags — neutral)
        
            🎯 Final Output:  
            Return the full story with inline tags. Do not change anything else.
                """.strip()

    def _build_user_prompt(self, script: str) -> str:
        return f"""
            Please enhance the story below by inserting **non-spoken ElevenLabs v3 audio tags**. These tags should help guide how the story is read aloud by an AI voice — **without rewriting the story in any way**.
        
            🎯 Voice Style:  
            The narrator is a girl aged 12–18 in the U.S., telling a real-life or Reddit-style story on TikTok or YouTube Shorts. Keep it emotionally honest, conversational, and rhythmically engaging.
        
            🛑 Do NOT:
            - Change, fix, rephrase, or remove any text
            - Adjust grammar, spelling, or punctuation
            - Add explanations or formatting
            - Tag every sentence — use tags **only where needed**
        
            ✅ Insert only these tags, in square brackets, before the line they affect:
        
            **💖 Emotional tone & relatability**  
            [embarrassed], [hopeful], [sad], [excited], [relieved], [confused], [disappointed], [sincere]
        
            **🧠 Internal reactions & anxiety**  
            [hesitates], [sighs], [gulps], [gasps], [crying], [starts to say something], [trailing off]
        
            **🎭 Tone & style**  
            [playfully], [sarcastic], [speaking softly], [whispers], [deadpan], [matter-of-fact]
        
            **⏱️ Rhythm & pacing**  
            [pause], [long pause], [slowly], [rushed]
        
            **⚠️ Rare or intense**  
            [angry], [shouting], [terrified], [laughs], [groans], [clears throat], [inhales], [exhales], [snorts]
        
            📏 Rules:
            - Max 3 tags per paragraph
            - Max 2 tags stacked
            - Place each tag **before** the affected line
            - If emotion or pacing is unclear — do **not** add a tag
            - Tag order: [emotion][reaction][pacing]
        
            📘 Examples:
        
            > [pause][hopeful] Maybe… this could actually work.  
            > [embarrassed][laughs] I seriously said that — out loud.  
            > I made toast and walked to school. *(no tags added)*
        
            🎯 Return only the story with tags. Do not explain, wrap, or format the output.
        
            Story:
            {script.strip()}
                """.strip()

    def save_enhanced_script(self, folderName: str, script: str):
        folder_path = os.path.join(REVISED_PATH, folderName)
        os.makedirs(folder_path, exist_ok=True)

        revised_file = os.path.join(folder_path, ENHANCED_NAME)  # or 'final.txt', if you prefer

        with open(revised_file, "w", encoding="utf-8") as f:
            f.write(script.strip())

        print(f"Enhanced script saved to: {revised_file}")

    def loadScript(self, title):
        folder_path = os.path.join(REVISED_PATH, title)
        script_file = os.path.join(folder_path, REVISED_NAME)  # Adjust filename as needed

        if not os.path.exists(script_file):
            raise FileNotFoundError(f"Script file not found: {script_file}")

        with open(script_file, "r", encoding="utf-8") as f:
            return f.read().strip()
