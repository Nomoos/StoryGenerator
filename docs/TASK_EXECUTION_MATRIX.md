# P1 Task Execution Matrix

**Purpose:** Comprehensive dependency and execution order for all 41 P1-High priority tasks

## Task Overview

**Total P1 Tasks:** 41 implementation tasks  
**Groups:** 10 pipeline groups  
**Estimated Effort:** 120-200 hours  
**Parallelization:** High (many independent tasks)

## Dependency Graph

```
Legend:
  → Sequential dependency (must complete before next)
  ⇉ Parallel execution possible
  ◆ Critical path
  ○ Optional/configurable

Content Pipeline (P0 - prerequisite)
  ↓
◆ Idea Generation (7 tasks)
  ├─→ 03-ideas-01-reddit-adaptation (4-5h)
  ├─→ 03-ideas-02-llm-generation (3-4h)
  │   ⇓
  ├─→ 03-ideas-03-clustering (3-4h)
  │   ⇓
  ├─→ 03-ideas-04-title-generation (3-4h)
  │   ⇓
  ├─→ 04-scoring-01-title-scorer (4-5h)
  │   ⇓
  ├─→ 04-scoring-02-voice-recommendation (2-3h)
  │   ⇓
  └─→ 04-scoring-03-top-selection (1-2h)
      ⇓
◆ Script Development (5 tasks)
  ├─→ 05-script-01-raw-generation (4-5h)
  │   ⇓
  ├─→ 05-script-02-script-scorer (3-4h)
  │   ⇓
  ├─→ 05-script-03-iteration (4-5h)
  │   ⇓
  ├─→ 05-script-04-gpt-improvement (3-4h)
  │   ⇓
  └─→ 05-script-05-title-improvement (2-3h)
      ⇓
      ⇓ (branches to parallel tracks)
      ├─────────────────┬─────────────────┐
      ⇓                 ⇓                 ⇓
◆ Scene Planning    Audio Production  [wait]
  (3 tasks)         (2 tasks)
  ├─→ 06-scenes-01  ├─→ 07-audio-01 (4-5h)
  │   (3-4h)        │   ⇓
  │   ⇓             └─→ 07-audio-02 (2-3h)
  ├─→ 06-scenes-02      ⇓
  │   (3-4h)            ⇓
  │   ⇓             Subtitle Creation
  └─→ 06-scenes-03  (2 tasks)
      (2-3h)        ├─→ 08-subtitles-01 (4-5h)
      ⇓             │   (needs audio + scenes)
      ⇓             │   ⇓
      ⇓             └─→ 08-subtitles-02 (2-3h)
      ⇓                 ⇓
◆ Image Generation      ⇓
  (4 tasks)             ⇓
  ├─→ 09-images-01 (3-4h)
  │   ⇓
  ├─→ 09-images-02 (5-6h)
  │   ⇓
  ├─→ 09-images-03 (5-6h)
  │   ⇓
  └─→ 09-images-04 (2-3h)
      ⇓
◆ Video Production
  (3 tasks)
  ├─→ 10-video-01 (6-8h)
  ├─→ 10-video-02 (6-8h) [parallel]
  │   ⇓
  └─→ 10-video-03 (1-2h)
      ⇓
◆ Post-Production
  (6 tasks)
  ├─→ 11-post-01 (2-3h)
  │   ⇓
  ├─→ 11-post-02 (3-4h) [needs subtitles]
  │   ├─→ 11-post-03 (4-5h) [optional BGM]
  │   └─→ 11-post-04 (2-3h)
  │       ⇓
  ├─→ 11-post-05 (2-3h)
  │   ⇓
  └─→ 11-post-06 (3-4h)
      ⇓
◆ Quality Control
  (3 tasks)
  ├─→ 12-qc-01 (2-3h)
  ├─→ 12-qc-02 (1-2h) [parallel]
  │   ⇓
  └─→ 12-qc-03 (2-3h)
      ⇓
◆ Export & Delivery
  (3 tasks)
  ├─→ 13-export-01 (2-3h)
  │   ⇓
  ├─→ 13-export-02 (1-2h)
  └─→ 13-export-03 (1-2h)
```

## Execution Strategies

### Strategy 1: Sequential (Single Developer)

**Timeline:** 8-12 days  
**Approach:** Complete one task at a time, following dependencies

```
Week 1:
  Day 1-2: Idea Generation (7 tasks, 23-30h)
  Day 3-4: Script Development (5 tasks, 16-21h)
  Day 5:   Scene Planning (3 tasks, 8-11h)

Week 2:
  Day 6:   Audio + Subtitles (4 tasks, 12-16h)
  Day 7-8: Image Generation (4 tasks, 15-19h)
  Day 9:   Video Production (3 tasks, 13-18h)
  Day 10:  Post-Production (6 tasks, 16-22h)
  Day 11:  QC + Export (6 tasks, 8-13h)
```

### Strategy 2: Parallel (3-4 Developers)

**Timeline:** 3-5 days  
**Approach:** Parallelize independent tasks within groups

```
Team A (2 devs): Critical path (ideas → scripts → scenes → images → video)
Team B (1 dev):  Audio pipeline (after scripts)
Team C (1 dev):  Subtitles pipeline (after audio + scenes)

Day 1:
  Team A: Idea Generation (7 tasks)
  Team B: Wait for scripts
  Team C: Wait for audio

Day 2:
  Team A: Script Development (5 tasks)
  Team B: Wait for scripts
  Team C: Wait for audio

Day 3:
  Team A: Scene Planning (3 tasks) + Image Gen start
  Team B: Audio Production (2 tasks)
  Team C: Wait for audio

Day 4:
  Team A: Image Generation (4 tasks)
  Team B: Subtitle Creation (2 tasks)
  Team C: Post-Production prep

Day 5:
  Team A: Video Production (3 tasks)
  Team B: Post-Production (6 tasks, assist)
  Team C: Post-Production (6 tasks, assist)

Day 6:
  All: QC + Export (6 tasks)
```

### Strategy 3: Aggressive Parallel (10+ Developers)

**Timeline:** 2-3 days  
**Approach:** Maximum parallelization, multiple pipelines

```
5 parallel story pipelines × 2 devs each = 10 developers

Day 1: All pipelines start (ideas + scripts)
Day 2: All pipelines continue (scenes + audio + images)
Day 3: All pipelines finish (video + post + qc + export)
```

## Critical Path Analysis

### Longest Sequential Chain (Critical Path)

```
03-ideas-01 → 03-ideas-02 → 03-ideas-03 → 03-ideas-04 → 
04-scoring-01 → 04-scoring-02 → 04-scoring-03 →
05-script-01 → 05-script-02 → 05-script-03 → 05-script-04 → 05-script-05 →
06-scenes-01 → 06-scenes-02 →
09-images-01 → 09-images-02 → 09-images-03 → 09-images-04 →
10-video-01/02 → 10-video-03 →
11-post-01 → 11-post-02 → 11-post-04 → 11-post-05 → 11-post-06 →
12-qc-01/02 → 12-qc-03 →
13-export-01 → 13-export-02/03

Total Critical Path: ~110-150 hours (sequential)
```

### Parallel Opportunities

1. **Idea Generation**: 
   - `03-ideas-01` (Reddit) ⇉ `03-ideas-02` (LLM) [parallel]
   
2. **Scene Planning + Audio**:
   - After script completion, both can start simultaneously
   
3. **Image Generation**:
   - Multiple scenes can be generated in parallel
   - `09-images-02` and `09-images-03` can run concurrently
   
4. **Video Production**:
   - `10-video-01` (LTX) ⇉ `10-video-02` (Interpolation) [parallel]
   - Multiple scene videos can be processed simultaneously
   
5. **Post-Production**:
   - `11-post-03` (BGM) is optional/parallel
   
6. **Quality Control**:
   - `12-qc-01` (preview) ⇉ `12-qc-02` (sync) [parallel]

## Resource Requirements

### Computational Resources

| Stage | CPU | Memory | GPU | Disk | Duration |
|-------|-----|--------|-----|------|----------|
| Idea Generation | Medium | 2GB | No | 100MB | 4-6h |
| Script Development | Medium | 2GB | No | 50MB | 3-5h |
| Scene Planning | Low | 1GB | No | 20MB | 2-3h |
| Audio Production | High | 4GB | No | 500MB | 3-5h |
| Subtitle Creation | Medium | 2GB | Optional | 10MB | 2-3h |
| Image Generation | High | 8GB | Yes (12GB VRAM) | 2GB | 8-12h |
| Video Production | Very High | 16GB | Yes (16GB VRAM) | 10GB | 10-15h |
| Post-Production | High | 8GB | Optional | 5GB | 5-8h |
| Quality Control | Low | 1GB | No | 100MB | 1-2h |
| Export | Medium | 2GB | No | 2GB | 1-2h |

### API Requirements

| Service | Used By | Rate Limits | Cost |
|---------|---------|-------------|------|
| OpenAI GPT-4 | Ideas, Scripts, Scenes | 10K TPM | $0.03/1K tokens |
| OpenAI GPT-4o-mini | Enhancement | 30K TPM | $0.15/1M tokens |
| ElevenLabs TTS | Audio | 100K chars/month | $1/10K chars |
| Local Ollama | Ideas, Scripts | Unlimited | Free |
| Local Whisper | Subtitles | Unlimited | Free |
| Local SDXL | Images | Unlimited | Free |
| Local LTX | Video | Unlimited | Free |

## Checkpoint Strategy

### Checkpoint Frequency

```
After each major task:
  ✓ 03-ideas-04 (after title generation)
  ✓ 04-scoring-03 (after top selection)
  ✓ 05-script-05 (after script improvement)
  ✓ 06-scenes-02 (after shot list)
  ✓ 07-audio-02 (after normalization)
  ✓ 08-subtitles-02 (after scene mapping)
  ✓ 09-images-04 (after keyframe selection)
  ✓ 10-video-03 (after variant selection)
  ✓ 11-post-06 (after color grading)
  ✓ 12-qc-03 (after quality report)
  ✓ 13-export-03 (after metadata creation)
```

### Checkpoint Data

Each checkpoint saves:
- Completed task IDs
- Output file paths
- Timestamps
- Configuration used
- Resource metrics

## Error Handling

### Retry Strategy

```csharp
public class TaskRetryPolicy
{
    public int MaxRetries { get; set; } = 3;
    public TimeSpan InitialDelay { get; set; } = TimeSpan.FromSeconds(5);
    public double BackoffMultiplier { get; set; } = 2.0;
    
    // Exponential backoff: 5s, 10s, 20s
}
```

### Failure Recovery

1. **Transient Failures** (network, API timeout):
   - Automatic retry with exponential backoff
   - Continue from last checkpoint
   
2. **Permanent Failures** (invalid input, missing file):
   - Log error details
   - Save checkpoint
   - Require manual intervention
   
3. **Partial Failures** (some scenes succeed, others fail):
   - Complete successful tasks
   - Retry only failed tasks
   - Aggregate results

## Performance Optimization

### Caching Strategy

```
Cache Layer 1: In-Memory (5 min TTL)
  - Recent API responses
  - Generated prompts
  - Configuration data

Cache Layer 2: Disk (24 hour TTL)
  - Model outputs
  - Intermediate results
  - API response cache

Cache Layer 3: Permanent Storage
  - Final artifacts
  - Selected outputs
  - Quality reports
```

### Batch Processing

```csharp
public class BatchConfig
{
    // Process multiple titles together
    public int TitleBatchSize { get; set; } = 5;
    
    // Generate multiple images simultaneously
    public int ImageBatchSize { get; set; } = 4;
    
    // Process multiple video clips in parallel
    public int VideoClipBatchSize { get; set; } = 2;
}
```

## Monitoring Metrics

### Key Performance Indicators (KPIs)

```
Pipeline Metrics:
  - Total execution time (target: <6 hours)
  - Stage completion rates (target: 100%)
  - Error rate (target: <5%)
  - Retry count (target: <10%)
  - Checkpoint frequency (every stage)

Quality Metrics:
  - Script quality score (target: >80/100)
  - Title viral score (target: >75/100)
  - Video quality score (target: >85/100)
  - A/V sync accuracy (target: >99%)
  - User engagement prediction (target: >70%)

Resource Metrics:
  - API costs per video (target: <$5)
  - GPU utilization (target: >80%)
  - Disk usage (target: <20GB per video)
  - Memory usage (target: <16GB peak)
```

### Alerting Thresholds

```
Critical Alerts:
  - Pipeline failure (any stage)
  - API rate limit exceeded
  - Disk space <10GB
  - GPU out of memory

Warning Alerts:
  - Stage duration >2x expected
  - Retry count >5
  - Quality score <70
  - Memory usage >12GB
```

## Testing Matrix

### Unit Tests (41 tasks × 3-5 tests each = ~150 tests)

```
Per Task Tests:
  ✓ ValidInput_Success
  ✓ InvalidInput_ThrowsException
  ✓ NetworkError_RetriesAndSucceeds
  ✓ Timeout_SavesCheckpoint
  ✓ PartialFailure_CompletesSuccessfulParts
```

### Integration Tests (10 groups × 2-3 tests = ~25 tests)

```
Per Group Tests:
  ✓ CompleteGroup_AllTasksSucceed
  ✓ GroupResume_ContinuesFromCheckpoint
  ✓ GroupFailure_SavesStateCorrectly
```

### End-to-End Tests (5 scenarios)

```
E2E Scenarios:
  ✓ CompletePipeline_GeneratesVideo
  ✓ ResumeFromCheckpoint_CompletesSuccessfully
  ✓ ParallelExecution_HandlesMultipleStories
  ✓ ErrorRecovery_RetriesFailedStages
  ✓ PerformanceBenchmark_MeetsTargets
```

## Implementation Checklist

### Phase 1: Foundation (Week 1)
- [ ] Create pipeline stage interface
- [ ] Implement checkpoint manager
- [ ] Add progress tracking
- [ ] Build error handling framework
- [ ] Set up logging and monitoring

### Phase 2: Group Implementation (Weeks 2-4)
- [ ] Implement Idea Generation stages (7 tasks)
- [ ] Implement Script Development stages (5 tasks)
- [ ] Implement Scene Planning stages (3 tasks)
- [ ] Implement Audio Production stages (2 tasks)
- [ ] Implement Subtitle Creation stages (2 tasks)
- [ ] Implement Image Generation stages (4 tasks)
- [ ] Implement Video Production stages (3 tasks)
- [ ] Implement Post-Production stages (6 tasks)
- [ ] Implement Quality Control stages (3 tasks)
- [ ] Implement Export & Delivery stages (3 tasks)

### Phase 3: Integration & Testing (Week 5)
- [ ] Integration tests for all groups
- [ ] End-to-end pipeline tests
- [ ] Performance optimization
- [ ] Documentation completion

### Phase 4: Production Ready (Week 6)
- [ ] Load testing
- [ ] Error scenario testing
- [ ] Production deployment guide
- [ ] Monitoring setup

## Success Criteria

### Functional Requirements
- ✅ All 41 tasks implemented and tested
- ✅ Complete pipeline executes successfully
- ✅ Checkpoint/resume works reliably
- ✅ Error handling covers all scenarios
- ✅ Configuration system is flexible

### Non-Functional Requirements
- ✅ Pipeline completes in <6 hours (single story)
- ✅ Test coverage >80%
- ✅ Error rate <5%
- ✅ Documentation complete
- ✅ Production-ready

## Related Documentation

- [Pipeline Orchestration Guide](./PIPELINE_ORCHESTRATION.md)
- [P1 High Priority Overview](../issues/p1-high/README.md)
- [Implementation Groups](../issues/p1-high/*/README.md)
- [Checkpoint System](./CHECKPOINT_SYSTEM.md)
