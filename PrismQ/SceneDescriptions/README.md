# SceneDescriptions

Scene planning and shot breakdown for video production.

## Purpose

Breaks scripts into scenes, shots, and generates timing information for video production.

## Modules

- **scene_planning.py**: Scene and shot planning
  - `ScenePlanner`: Split scripts into scenes
  - `ShotPlanner`: Create shot lists
  - `BeatSheetGenerator`: Generate beat sheets

## Usage

```python
from PrismQ.SceneDescriptions.scene_planning import ScenePlanner

planner = ScenePlanner()
scenes = planner.split_into_scenes(script)
shots = planner.create_shot_list(scenes)
```
