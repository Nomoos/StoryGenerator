"""
Data models for vision analysis results.
Stores quality scores, consistency metrics, and validation results.
"""

from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Any
from datetime import datetime


@dataclass
class QualityScore:
    """Quality assessment scores for a single image."""
    overall_quality: float  # 0-10
    sharpness: float  # 0-10
    clarity: float  # 0-10
    composition: float  # 0-10
    lighting: float  # 0-10
    subject_clarity: float  # 0-10
    artifacts_detected: bool
    reasoning: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def average_score(self) -> float:
        """Calculate average quality score."""
        scores = [
            self.overall_quality,
            self.sharpness,
            self.clarity,
            self.composition,
            self.lighting,
            self.subject_clarity
        ]
        return sum(scores) / len(scores)


@dataclass
class ConsistencyScore:
    """Consistency assessment between two consecutive images."""
    character_consistency: float  # 0-10
    style_consistency: float  # 0-10
    lighting_consistency: float  # 0-10
    visual_continuity: float  # 0-10
    inconsistencies: List[str] = field(default_factory=list)
    reasoning: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def average_score(self) -> float:
        """Calculate average consistency score."""
        scores = [
            self.character_consistency,
            self.style_consistency,
            self.lighting_consistency,
            self.visual_continuity
        ]
        return sum(scores) / len(scores)


@dataclass
class ImageCaption:
    """Generated caption/description for an image."""
    caption: str
    confidence: float  # 0-1
    model_used: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class VisionAnalysisResult:
    """Complete vision analysis result for a single image or image sequence."""
    image_path: str
    caption: Optional[ImageCaption] = None
    quality_score: Optional[QualityScore] = None
    consistency_score: Optional[ConsistencyScore] = None
    validation_passed: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "image_path": self.image_path,
            "caption": self.caption.to_dict() if self.caption else None,
            "quality_score": self.quality_score.to_dict() if self.quality_score else None,
            "consistency_score": self.consistency_score.to_dict() if self.consistency_score else None,
            "validation_passed": self.validation_passed,
            "errors": self.errors,
            "warnings": self.warnings,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }
        return result
    
    def add_error(self, error: str):
        """Add an error and mark validation as failed."""
        self.errors.append(error)
        self.validation_passed = False
    
    def add_warning(self, warning: str):
        """Add a warning (doesn't fail validation)."""
        self.warnings.append(warning)


@dataclass
class StoryboardValidation:
    """Validation result for an entire storyboard sequence."""
    story_name: str
    scene_count: int
    scene_analyses: List[VisionAnalysisResult] = field(default_factory=list)
    overall_quality_avg: float = 0.0
    overall_consistency_avg: float = 0.0
    validation_passed: bool = True
    recommendations: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "story_name": self.story_name,
            "scene_count": self.scene_count,
            "scene_analyses": [analysis.to_dict() for analysis in self.scene_analyses],
            "overall_quality_avg": self.overall_quality_avg,
            "overall_consistency_avg": self.overall_consistency_avg,
            "validation_passed": self.validation_passed,
            "recommendations": self.recommendations,
            "timestamp": self.timestamp
        }
    
    def add_scene_analysis(self, analysis: VisionAnalysisResult):
        """Add a scene analysis and update overall scores."""
        self.scene_analyses.append(analysis)
        if not analysis.validation_passed:
            self.validation_passed = False
        
        # Recalculate averages
        if self.scene_analyses:
            quality_scores = [
                a.quality_score.average_score() 
                for a in self.scene_analyses 
                if a.quality_score
            ]
            consistency_scores = [
                a.consistency_score.average_score()
                for a in self.scene_analyses
                if a.consistency_score
            ]
            
            if quality_scores:
                self.overall_quality_avg = sum(quality_scores) / len(quality_scores)
            if consistency_scores:
                self.overall_consistency_avg = sum(consistency_scores) / len(consistency_scores)
    
    def add_recommendation(self, recommendation: str):
        """Add a recommendation for improvement."""
        self.recommendations.append(recommendation)
