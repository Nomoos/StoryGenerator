# Group 2 — Progress & Coordination Hub

This document tracks all unfinished tasks, current priorities, and blockers for **Group 2** (Content to Script Pipeline) development in StoryGenerator.

**Last Updated:** 2025-10-10
**Group Focus:** Content Collection, Idea Generation, Script Development
**Total Effort:** 14-20 hours across 3 tasks
**Status:** 📋 Ready to start - No blockers

---

## 📅 Update Checklist
- [x] `.NEXT.MD` is up to date
- [x] Unfinished tasks listed below
- [x] Blockers/risks noted
- [x] Roadmap synced

---

## Current Focus (`.NEXT.MD`)

**Phase:** Content to Script Pipeline Enhancement
**Recent Completion:** ✅ Idea Generation Pipeline complete (7 tasks - Reddit adaptation, LLM generation, clustering, title generation, scoring)

### Available Tasks
Group 2 has **3 unfinished tasks** ready for assignment:
- Content collection and sourcing (3 tasks, 14-20h)

**Next Recommended:** Start with `content-reddit-scraper-enhanced` (4-6h) or `content-deduplication` (4-6h)

See [.NEXT.MD](.NEXT.MD) for detailed status and execution order.

---

## Unfinished Tasks

### 📦 Content Collection & Sourcing (14-20h)

#### 1. Enhanced Reddit Scraper
- **File:** [content-reddit-scraper-enhanced.md](.ISSUES/content-reddit-scraper-enhanced.md)
- **Effort:** 4-6 hours
- **Priority:** P1 (High)
- **Status:** 📋 Not Started
- **Description:** Enhance Reddit content scraping with better filtering, rate limiting, and multi-subreddit support
- **Acceptance Criteria:**
  - [ ] Multi-subreddit scraping support
  - [ ] Incremental updates (fetch only new content)
  - [ ] Duplicate detection across scrapes
  - [ ] Rate limiting compliance with Reddit API
  - [ ] Content quality filtering (score, length, engagement)
  - [ ] JSON output with full metadata
  - [ ] Unit tests with mocked Reddit API

#### 2. Content Deduplication System
- **File:** [content-deduplication.md](.ISSUES/content-deduplication.md)
- **Effort:** 4-6 hours
- **Priority:** P1 (High)
- **Status:** 📋 Not Started
- **Description:** Implement content deduplication system that identifies and removes duplicate or near-duplicate content
- **Acceptance Criteria:**
  - [ ] Exact duplicate detection (hash-based)
  - [ ] Near-duplicate detection (fuzzy matching)
  - [ ] Semantic similarity detection (embeddings)
  - [ ] Configurable similarity thresholds
  - [ ] Duplicate tracking and reporting
  - [ ] Batch processing support
  - [ ] Unit tests with sample duplicates

#### 3. Alternative Content Sources
- **File:** [content-social-media-sources.md](.ISSUES/content-social-media-sources.md)
- **Effort:** 6-8 hours
- **Priority:** P1 (High)
- **Status:** 📋 Not Started
- **Description:** Add content sourcing from Instagram, TikTok, and other social media platforms
- **Acceptance Criteria:**
  - [ ] Instagram content scraping
  - [ ] TikTok content scraping
  - [ ] Content normalization across sources
  - [ ] Quality scoring across platforms
  - [ ] API credential management
  - [ ] Rate limiting for all platforms
  - [ ] Unit tests with mocked APIs

---

## Blockers/Risks

### Current Blockers
**None** - All tasks are independent and ready to start

### Potential Risks

#### 🟡 Medium Risk
- **API Rate Limits:** Reddit, Instagram, TikTok APIs have strict rate limits
  - *Mitigation:* Implement proper rate limiting, retry logic with exponential backoff
  - *Mitigation:* Cache results, implement incremental updates

- **API Access Requirements:** Need API credentials for each platform
  - *Mitigation:* Document setup process clearly in each task
  - *Mitigation:* Provide mock/test data for development without real API access

#### 🟢 Low Risk
- **API Changes:** Social media APIs may change without notice
  - *Mitigation:* Use well-maintained libraries (praw, instaloader)
  - *Mitigation:* Add version pinning to requirements

- **Content Quality Variance:** Different platforms have different content quality
  - *Mitigation:* Implement platform-specific quality filters
  - *Mitigation:* Normalize content across sources

---

## Execution Strategy

### Recommended Order

**Phase 1: Core Content Source (Week 1)**
1. content-reddit-scraper-enhanced (4-6h) - Establish primary content source

**Phase 2: Quality & Expansion (Week 1-2)**
2. content-deduplication (4-6h) - Ensure content quality
3. content-social-media-sources (6-8h) - Add alternative sources

### Parallelization Options

All tasks are independent and can be worked in parallel:
- **3 developers:** All 3 tasks simultaneously (1 week total)
- **2 developers:** Tasks 1+2 in parallel, then task 3 (1.5 weeks)
- **1 developer:** Sequential execution (2-2.5 weeks)

### Dependencies

```
Group 1 (Infrastructure) → Group 2 (Content Collection)
     ↓
infrastructure-configuration (API credentials)
     ↓
content-reddit-scraper ←→ content-deduplication ←→ content-social-media-sources
     (all can run in parallel)
```

Only dependency is Group 1's `infrastructure-configuration` for API credential management. Otherwise all tasks are independent.

---

## Links

### Main Documentation
- **Progress Hub:** [MainProgressHub.md](../../MainProgressHub.md)
- **Roadmap:** [docs/roadmaps/HYBRID_ROADMAP.md](../../docs/roadmaps/HYBRID_ROADMAP.md)
- **Completed Work:** [group-2-idea-generation](../../issues/resolved/phase-3-implementation/group-2-idea-generation/)

### Group 2 Resources
- **README:** [README.md](README.md)
- **Current Focus:** [.NEXT.MD](.NEXT.MD)
- **Open Issues:** [.ISSUES/](.ISSUES/)
- **Completed Issues:** [.DONE/](.DONE/)

### Related Groups
- **Group 1:** [Foundation & Infrastructure](../group_1/README.md) - Provides configuration management
- **Group 3:** [Audio & Visual Assets](../group_3/README.md) - Consumes scripts from Group 2
- **Group 4:** [Video Assembly & Distribution](../group_4/README.md) - Final pipeline stage

### Priority Tracking
- **P1 High Priority Issues:** [issues/p1-high/](../p1-high/README.md)
- **Issue Index:** [issues/INDEX.md](../INDEX.md)

---

## Recent Activity

### Completed (Recent)
✅ **Idea Generation Pipeline** (7 tasks complete)
- Reddit adaptation
- LLM-based idea generation
- Idea clustering and categorization
- Title generation from ideas
- Viral potential scoring
- Voice recommendations
- Top title selection

**Total Effort Completed:** 21-29 hours
**Documentation:** [group-2-idea-generation](../../issues/resolved/phase-3-implementation/group-2-idea-generation/)

### In Progress
📋 **None** - Ready for new assignments

### Next Up
🎯 **Enhanced Reddit Scraper** or **Content Deduplication** recommended as starting point

---

## Success Metrics

### Completion Criteria
- [ ] All 3 tasks moved from `.ISSUES/` to `.DONE/`
- [ ] Reddit scraper fetching quality content from multiple subreddits
- [ ] Deduplication system removing duplicates across sources
- [ ] Alternative sources integrated (Instagram, TikTok)
- [ ] Unit tests passing for all components
- [ ] Documentation complete for each component

### Quality Gates
- Reddit scraper respects rate limits
- Deduplication catches >95% of exact duplicates
- Deduplication catches >80% of near-duplicates
- All platforms have error handling and retry logic
- API credentials managed securely through config system

---

## Pipeline Context

Group 2 operates as a **complete pipeline stage**:

**Input:** External content sources (Reddit, social media)
**Output:** Filtered, deduplicated content ready for idea generation
**Dependencies:** Infrastructure from Group 1 (configuration management)
**Consumers:** Idea generation and script development (also part of Group 2)

### Current Pipeline Status
```
✅ Content Collection → ✅ Idea Generation → ✅ Title Selection → Group 3 (Asset Production)
   (3 tasks - 14-20h)   (7 tasks COMPLETE)   (included above)
```

---

**Last Sync:** 2025-10-10
**Next Review:** When first task is started
**Maintainer:** @Nomoos
