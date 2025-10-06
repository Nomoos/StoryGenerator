import os

from Generators.GEnhanceScript import EnhanceScriptGenerator
from Tools.Utils import  REVISED_PATH, REVISED_NAME


def BatchEnhanceScript():
    for folder_name in os.listdir(REVISED_PATH):
        EnhanceScriptGenerator().Enhance(folder_name)

BatchEnhanceScript()