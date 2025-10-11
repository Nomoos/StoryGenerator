# StoryGenerator

Generate and refine video scripts from ideas and titles.

## Purpose

Creates initial scripts, iteratively improves them, and ensures style consistency across content.

## Modules

- **script_development.py**: Script generation and iteration
  - `ScriptGenerator`: Generate scripts from ideas
  - `ScriptScorer`: Evaluate script quality
  - `ScriptIterator`: Iteratively improve scripts
  - `GPTScriptEnhancer`: Enhance with GPT-4

- **style_consistency.py**: Style checking and consistency
  - `StyleChecker`: Ensure consistent style across scripts

## Usage

```python
from PrismQ.StoryGenerator.script_development import ScriptGenerator

generator = ScriptGenerator(llm_provider)
script = generator.generate_script(idea, target_duration=45.0)
```
