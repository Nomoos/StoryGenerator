import os

from Generators.GRevise import RevisedScriptGenerator
from Models.StoryIdea import StoryIdea
from Tools.Utils import SCRIPTS_PATH

def batch_revise():
    generator = RevisedScriptGenerator()

    for folder_name in os.listdir(SCRIPTS_PATH):
        folder_path = os.path.join(SCRIPTS_PATH, folder_name)

        if not os.path.isdir(folder_path):
            continue

        idea_file = os.path.join(folder_path, "idea.json")
        if not os.path.exists(idea_file):
            print(f"⚠️ Skipping '{folder_name}': missing idea.json")
            continue

        try:
            idea = StoryIdea.from_file(idea_file)
            print(f"\n--- Revising: {idea.story_title} ---")
            generator.Revise(idea)
        except Exception as e:
            print(f"❌ Failed to revise '{folder_name}': {e}")

if __name__ == "__main__":
    batch_revise()
