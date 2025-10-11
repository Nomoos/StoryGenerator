# Video Production: Variant Selection

**Group:** group_4  
**Priority:** P1 (High)  
**Status:** ✅ Complete  
**Estimated Effort:** 3-4 hours  
**Completed:** 2025-10-10  

## Description

Implement video variant selection system that analyzes generated videos and selects the best variant based on quality metrics, visual coherence, and motion smoothness.

## Acceptance Criteria

- [x] Video quality scoring algorithm implemented
- [x] Variant comparison and selection logic
- [x] Quality metrics calculation (sharpness, stability, coherence)
- [x] Metadata tracking for each variant
- [x] Selected variant output with justification
- [x] Unit tests for selection logic

## Implementation

**Location:** `src/Python/Tools/VideoVariantSelector.py`  
**Script:** `scripts/select_video_variant.py`  
**Tests:** `tests/test_video_variant_selector.py`  
**Examples:** `examples/demo_video_variant_selector.py`

The VideoVariantSelector has been successfully implemented with:
- Motion smoothness scoring (35% weight)
- Temporal consistency checking (35% weight)
- Artifact detection (30% weight)
- Overall quality score (0-100 scale)
- Automated best-variant selection
- Manual override capability
- Batch processing support

**Related:** See `issues/resolved/video-production/GROUP_8_VIDEO_VARIANT_SELECTION_SUMMARY.md` for complete implementation details.

## Dependencies

- Requires: 10-video-02-interpolation (video interpolation must be complete)
- Requires: Python OpenCV for video analysis
- Install: `pip install opencv-python>=4.8.0 scikit-image>=0.21.0`

## Implementation Notes

Create `core/PrismQ/Pipeline/video_selection.py`:

```python
import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple

class VideoVariantSelector:
    def __init__(self, quality_threshold: float = 0.7):
        self.quality_threshold = quality_threshold
    
    def analyze_video(self, video_path: Path) -> Dict[str, float]:
        """Analyze video quality metrics"""
        cap = cv2.VideoCapture(str(video_path))
        
        sharpness_scores = []
        stability_scores = []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Calculate sharpness (Laplacian variance)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
            sharpness_scores.append(sharpness)
        
        cap.release()
        
        return {
            "sharpness": np.mean(sharpness_scores),
            "stability": np.mean(stability_scores),
            "quality_score": self._calculate_quality_score(sharpness_scores)
        }
    
    def select_best_variant(self, variants: List[Path]) -> Tuple[Path, Dict]:
        """Select best video variant from list"""
        scored_variants = []
        
        for variant in variants:
            metrics = self.analyze_video(variant)
            scored_variants.append((variant, metrics))
        
        # Sort by quality score
        scored_variants.sort(key=lambda x: x[1]["quality_score"], reverse=True)
        
        best_variant, best_metrics = scored_variants[0]
        return best_variant, best_metrics
```

## Output Files

**Directory:** `data/videos/selected/{gender}/{age_bucket}/`
**Files:**
- `selected_video.mp4` - Best variant
- `selection_metadata.json` - Quality metrics and justification

## Links

- Related: [HYBRID_ROADMAP.md](../../../docs/roadmaps/HYBRID_ROADMAP.md)
- Related: [PHASE_ORGANIZATION.md](../../atomic/PHASE_ORGANIZATION.md)
