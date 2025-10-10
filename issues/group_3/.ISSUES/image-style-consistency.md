# Image Generation: Style Consistency System

**Group:** group_3  
**Priority:** P1 (High)  
**Status:** 📋 Not Started  
**Estimated Effort:** 6-8 hours  

## Description

Implement style consistency system for SDXL keyframe generation to ensure visual coherence across all images in a video. Use IP-Adapter or similar for style transfer and consistency.

## Acceptance Criteria

- [ ] Style reference image selection/creation
- [ ] Style transfer to all keyframes
- [ ] Visual coherence scoring across frames
- [ ] Color palette consistency
- [ ] Character/object consistency across frames
- [ ] Style library for different video types
- [ ] Unit tests for style consistency

## Dependencies

- Install: `diffusers>=0.25.0 ip-adapter>=1.0.0`
- Requires: SDXL infrastructure from Group 3
- Requires: GPU with 12GB+ VRAM

## Implementation Notes

Create `core/pipeline/style_consistency.py`:

```python
from diffusers import StableDiffusionXLPipeline, IPAdapterPlus
from pathlib import Path
from typing import List, Dict
import torch

class StyleConsistencyManager:
    def __init__(self, model_id: str = "stabilityai/stable-diffusion-xl-base-1.0"):
        self.pipe = StableDiffusionXLPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            variant="fp16"
        )
        self.pipe.to("cuda")
        
        # Load IP-Adapter for style consistency
        self.pipe.load_ip_adapter(
            "h94/IP-Adapter", 
            subfolder="sdxl_models",
            weight_name="ip-adapter-plus_sdxl_vit-h.bin"
        )
    
    def create_style_reference(self, 
                              prompt: str, 
                              output_path: Path) -> Path:
        """Generate style reference image"""
        
        image = self.pipe(
            prompt=prompt,
            num_inference_steps=50,
            guidance_scale=7.5
        ).images[0]
        
        image.save(output_path)
        return output_path
    
    def generate_with_style(self,
                           prompts: List[str],
                           style_image: Path,
                           output_dir: Path) -> List[Path]:
        """Generate keyframes with consistent style"""
        
        # Set IP-Adapter scale for style influence
        self.pipe.set_ip_adapter_scale(0.8)
        
        generated_images = []
        
        for i, prompt in enumerate(prompts):
            output_path = output_dir / f"keyframe_{i:03d}.png"
            
            image = self.pipe(
                prompt=prompt,
                ip_adapter_image=style_image,
                num_inference_steps=50,
                guidance_scale=7.5
            ).images[0]
            
            image.save(output_path)
            generated_images.append(output_path)
        
        return generated_images
    
    def validate_consistency(self, images: List[Path]) -> Dict[str, float]:
        """Validate visual consistency across images"""
        # Calculate color histogram similarity
        # Calculate feature similarity
        # Return consistency scores
        pass
```

## Output Files

**Directory:** `data/images/styled/{gender}/{age_bucket}/`
**Files:**
- `style_reference.png` - Reference style image
- `keyframe_*.png` - Style-consistent keyframes
- `consistency_report.json` - Consistency metrics

## Links

- Related: [HYBRID_ROADMAP.md](../../../docs/roadmaps/HYBRID_ROADMAP.md)
- Related: Completed image tasks in [group-7-image-generation](../../resolved/phase-3-implementation/group-7-image-generation/)
