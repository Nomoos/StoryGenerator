# Content Pipeline: Content Deduplication System

**Group:** group_2  
**Priority:** P1 (High)  
**Status:** 📋 Not Started  
**Estimated Effort:** 4-6 hours  

## Description

Implement content deduplication system that identifies and removes duplicate or near-duplicate content from multiple sources. Uses fuzzy matching and semantic similarity.

## Acceptance Criteria

- [ ] Exact duplicate detection (hash-based)
- [ ] Near-duplicate detection (fuzzy matching)
- [ ] Semantic similarity detection (embeddings)
- [ ] Configurable similarity thresholds
- [ ] Duplicate tracking and reporting
- [ ] Batch processing support
- [ ] Unit tests with sample duplicates

## Dependencies

- Install: `fuzzywuzzy>=0.18.0 sentence-transformers>=2.2.0`
- Can work in parallel with other Group 2 tasks

## Implementation Notes

Create `core/pipeline/deduplication.py`:

```python
import hashlib
from fuzzywuzzy import fuzz
from sentence_transformers import SentenceTransformer, util
from typing import List, Dict, Tuple
import torch

class ContentDeduplicator:
    def __init__(self, 
                 fuzzy_threshold: int = 85,
                 semantic_threshold: float = 0.90):
        self.fuzzy_threshold = fuzzy_threshold
        self.semantic_threshold = semantic_threshold
        
        # Load sentence transformer for semantic similarity
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        self.seen_hashes = set()
        self.seen_content = []
    
    def _compute_hash(self, text: str) -> str:
        """Compute content hash"""
        normalized = text.lower().strip()
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def is_exact_duplicate(self, content: str) -> bool:
        """Check for exact duplicate"""
        content_hash = self._compute_hash(content)
        
        if content_hash in self.seen_hashes:
            return True
        
        self.seen_hashes.add(content_hash)
        return False
    
    def is_fuzzy_duplicate(self, content: str) -> Tuple[bool, float]:
        """Check for fuzzy (near) duplicate"""
        
        for seen in self.seen_content:
            similarity = fuzz.ratio(content, seen['text'])
            
            if similarity >= self.fuzzy_threshold:
                return True, similarity
        
        return False, 0.0
    
    def is_semantic_duplicate(self, content: str) -> Tuple[bool, float]:
        """Check for semantic duplicate using embeddings"""
        
        if not self.seen_content:
            return False, 0.0
        
        # Compute embedding for new content
        new_embedding = self.model.encode(content, convert_to_tensor=True)
        
        # Compare with seen content embeddings
        for seen in self.seen_content:
            if 'embedding' not in seen:
                seen['embedding'] = self.model.encode(
                    seen['text'], 
                    convert_to_tensor=True
                )
            
            similarity = util.cos_sim(new_embedding, seen['embedding']).item()
            
            if similarity >= self.semantic_threshold:
                return True, similarity
        
        return False, 0.0
    
    def check_duplicate(self, content: str) -> Dict:
        """Comprehensive duplicate check"""
        
        # Check exact duplicate
        if self.is_exact_duplicate(content):
            return {
                'is_duplicate': True,
                'type': 'exact',
                'similarity': 1.0
            }
        
        # Check fuzzy duplicate
        is_fuzzy, fuzzy_score = self.is_fuzzy_duplicate(content)
        if is_fuzzy:
            return {
                'is_duplicate': True,
                'type': 'fuzzy',
                'similarity': fuzzy_score / 100.0
            }
        
        # Check semantic duplicate
        is_semantic, semantic_score = self.is_semantic_duplicate(content)
        if is_semantic:
            return {
                'is_duplicate': True,
                'type': 'semantic',
                'similarity': semantic_score
            }
        
        # Not a duplicate - add to seen content
        self.seen_content.append({
            'text': content,
            'hash': self._compute_hash(content)
        })
        
        return {
            'is_duplicate': False,
            'type': None,
            'similarity': 0.0
        }
    
    def deduplicate_batch(self, contents: List[str]) -> Tuple[List[str], List[Dict]]:
        """Deduplicate a batch of content"""
        
        unique_content = []
        duplicate_reports = []
        
        for content in contents:
            result = self.check_duplicate(content)
            
            if result['is_duplicate']:
                duplicate_reports.append({
                    'content': content[:100] + '...',
                    'result': result
                })
            else:
                unique_content.append(content)
        
        return unique_content, duplicate_reports
```

## Output Files

**Directory:** `data/deduplication/`
**Files:**
- `duplicate_report.json` - Detected duplicates
- `unique_content.json` - Deduplicated content

## Links

- Related: [HYBRID_ROADMAP.md](../../../docs/roadmaps/HYBRID_ROADMAP.md)
- Related: Content pipeline in [group-1-content-pipeline](../../resolved/phase-3-implementation/group-1-content-pipeline/)
