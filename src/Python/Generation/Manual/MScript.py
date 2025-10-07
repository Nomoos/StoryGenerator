import os

from Generators.GScript import ScriptGenerator
from Models.StoryIdea import StoryIdea
from Tools.Utils import IDEAS_PATH


def manual_generation():
    generator = ScriptGenerator()
    # pick best idea overall
    try:
        while True:
            idea = pick_best_idea()
            generator.generate_from_storyidea(idea)

            print("🎤 Voiceover Script:\n")
            print(idea.story_title)

    except Exception as e:
        print("❌ Error generating script:", str(e))

def pick_best_idea() -> StoryIdea:
    if not os.path.exists(IDEAS_PATH):
        raise FileNotFoundError(f"❌ Folder '{IDEAS_PATH}' does not exist.")

    idea_files = [f for f in os.listdir(IDEAS_PATH) if f.endswith(".json")]
    if not idea_files:
        raise FileNotFoundError(f"❌ No story idea files found in '{IDEAS_PATH}'.")

    ideas = []
    for filename in idea_files:
        filepath = os.path.join(IDEAS_PATH, filename)
        try:
            idea = StoryIdea.from_file(filepath)
            ideas.append(idea)
        except Exception as e:
            print(f"⚠️ Skipping '{filename}' due to error: {e}")

    if not ideas:
        raise ValueError("❌ No valid story ideas loaded.")

    best = max(ideas, key=lambda idea: idea.potencial.get("overall", 0))
    print(f"🏆 Picked best idea: {best.story_title} (overall: {best.potencial.get('overall', 0)})")
    return best


if __name__ == "__main__":
    manual_generation()