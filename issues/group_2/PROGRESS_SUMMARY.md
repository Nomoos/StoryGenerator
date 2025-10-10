# Group 2 — Progress & Coordination Hub

**Last Updated:** 2025-10-10  
**Status:** 📋 Ready to start - 3 tasks defined

---

## 📅 Update Checklist
- [x] `.NEXT.MD` is up to date
- [x] Unfinished tasks listed below
- [x] Blockers/risks noted
- [x] Roadmap synced

---

## Current Focus (`.NEXT.MD`)

**Group 2: Content Pipeline Enhancements**

### Overview
Group 2 focuses on enhancing the content pipeline with three key improvements:

1. **Enhanced Reddit Scraper** (4-6h) - Multi-subreddit support, incremental updates, duplicate detection
2. **Social Media Sources** (6-8h) - Instagram and TikTok content collection
3. **Content Deduplication** (4-6h) - Fuzzy matching and semantic similarity detection

**Total Estimated Effort:** 14-20 hours  
**Priority:** P1 (High)  
**Status:** 📋 Not Started

### Context
These tasks build upon completed work:
- ✅ Basic Reddit scraper (`scripts/reddit_scraper.py`) - [Completed](../resolved/p0-content-pipeline/02-content-01-reddit-scraper/)
- ✅ Alternative sources (Quora, Twitter) (`scripts/scrapers/`) - [Completed](../resolved/p0-content-pipeline/02-content-02-alt-sources/)
- ✅ Basic deduplication (`scripts/deduplicate_content.py`) - [Completed](../resolved/p0-content-pipeline/02-content-04-deduplication/)

The new tasks enhance these implementations with advanced features.

---

## Unfinished Tasks

### 1. Enhanced Reddit Scraper
**File:** [.ISSUES/content-reddit-scraper-enhanced.md](.ISSUES/content-reddit-scraper-enhanced.md)  
**Priority:** P1  
**Effort:** 4-6 hours  
**Status:** 📋 Not Started

**Description:**
Enhance the existing Reddit scraper with:
- Incremental updates (fetch only new content since last scrape)
- Persistent duplicate detection using SQLite
- Enhanced rate limiting with exponential backoff
- Configurable quality thresholds per demographic
- Dynamic subreddit addition via config

**Builds on:** `scripts/reddit_scraper.py`

**Acceptance Criteria:**
- [ ] Incremental updates - track last scrape timestamp per subreddit
- [ ] Persistent duplicate detection across scrapes (use SQLite or JSON cache)
- [ ] Enhanced rate limiting with exponential backoff and retry logic
- [ ] Configurable quality thresholds per demographic
- [ ] Support for dynamic subreddit addition via config
- [ ] Improved logging and error handling
- [ ] Unit tests with mocked Reddit API
- [ ] Documentation updated with new features

---

### 2. Social Media Sources (Instagram & TikTok)
**File:** [.ISSUES/content-social-media-sources.md](.ISSUES/content-social-media-sources.md)  
**Priority:** P1  
**Effort:** 6-8 hours  
**Status:** 📋 Not Started

**Description:**
Expand alternative content sources by adding Instagram and TikTok scrapers:
- Instagram scraper (stories from hashtags/accounts)
- TikTok scraper (video descriptions and captions)
- Integration with existing unified CLI
- Mock data implementation (production API optional)

**Builds on:** `scripts/scrapers/` (existing Quora and Twitter scrapers)

**Acceptance Criteria:**
- [ ] Instagram scraper implemented following BaseScraper interface
- [ ] TikTok scraper implemented following BaseScraper interface
- [ ] Content normalization to match existing format
- [ ] Age-appropriate content filtering applied
- [ ] Integration with existing unified CLI (`alt_sources_scraper.py`)
- [ ] Rate limiting for each platform
- [ ] Compliance with platform Terms of Service
- [ ] Mock data implementation for testing
- [ ] Unit tests following existing test patterns
- [ ] Documentation updated in scrapers README

---

### 3. Enhanced Content Deduplication
**File:** [.ISSUES/content-deduplication.md](.ISSUES/content-deduplication.md)  
**Priority:** P1  
**Effort:** 4-6 hours  
**Status:** 📋 Not Started

**Description:**
Enhance the existing deduplication system with advanced techniques:
- Advanced fuzzy matching using Levenshtein distance
- Semantic similarity detection using sentence embeddings
- Configurable similarity thresholds (fuzzy: 85%, semantic: 90%)
- Performance optimization for batch processing
- Cross-source duplicate detection

**Builds on:** `scripts/deduplicate_content.py`

**Acceptance Criteria:**
- [ ] Advanced fuzzy matching using Levenshtein distance
- [ ] Semantic similarity detection using sentence embeddings
- [ ] Configurable similarity thresholds (fuzzy: 85%, semantic: 90%)
- [ ] Performance optimization for batch processing
- [ ] Cross-source duplicate detection (Reddit + Quora + Twitter + Instagram + TikTok)
- [ ] Enhanced reporting with similarity scores and duplicate groups
- [ ] Unit tests with edge cases (near-duplicates, paraphrases)
- [ ] Documentation updated with new features
- [ ] Backward compatible with existing output format

---

## Blockers/Risks

### Current Blockers
None at this time. All tasks can start immediately.

### Potential Risks

1. **API Rate Limits**
   - **Risk:** Reddit, Instagram, TikTok APIs have strict rate limits
   - **Mitigation:** Implement exponential backoff and respect limits
   - **Impact:** Low - mock implementations allow development without APIs

2. **Platform ToS Compliance**
   - **Risk:** Instagram/TikTok may block unofficial scraping
   - **Mitigation:** Use mock data, document official API paths
   - **Impact:** Low - not blocking development

3. **Performance - Semantic Similarity**
   - **Risk:** Sentence embeddings can be slow for large datasets
   - **Mitigation:** Batch processing, GPU acceleration, optional feature
   - **Impact:** Medium - may need optimization for production

4. **Dependencies**
   - **Risk:** New libraries (sentence-transformers, instagrapi, TikTokApi)
   - **Mitigation:** All available on PyPI, well-maintained
   - **Impact:** Low - standard Python packages

### Dependencies Status
- ✅ **Reddit API (PRAW):** Already configured and working
- ✅ **Base scraper infrastructure:** Complete in `scripts/scrapers/`
- ✅ **Basic deduplication:** Complete in `scripts/deduplicate_content.py`
- 📋 **New libraries:** Need to add to requirements.txt

---

## Implementation Strategy

### Recommended Task Order

**Sequential (single developer):**
1. Enhanced Reddit Scraper (foundation)
2. Content Deduplication (applies to all sources)
3. Social Media Sources (adds new sources)

**Parallel (multiple developers):**
- All three tasks are independent and can be worked simultaneously
- Each task builds on different completed work
- No inter-dependencies between the three new tasks

### Technical Approach

All tasks follow the principle of **enhancement, not replacement**:
- Extend existing code rather than rewrite
- Maintain backward compatibility
- Add optional features that can be enabled/disabled
- Use existing patterns and interfaces

---

## Links

### Project Context
- **Main Hub:** [MainProgressHub.md](../../MainProgressHub.md)
- **Roadmap:** [HYBRID_ROADMAP.md](../../docs/roadmaps/HYBRID_ROADMAP.md)
- **Group 2 README:** [README.md](README.md)

### Related Completed Work
- [Reddit Scraper (P0)](../resolved/p0-content-pipeline/02-content-01-reddit-scraper/) - ✅ Complete
- [Alternative Sources (P0)](../resolved/p0-content-pipeline/02-content-02-alt-sources/) - ✅ Complete
- [Deduplication (P0)](../resolved/p0-content-pipeline/02-content-04-deduplication/) - ✅ Complete
- [Group 2 Idea Generation (P1)](../resolved/phase-3-implementation/group-2-idea-generation/) - ✅ Complete

### Current Task Files
- [Enhanced Reddit Scraper](.ISSUES/content-reddit-scraper-enhanced.md)
- [Social Media Sources](.ISSUES/content-social-media-sources.md)
- [Enhanced Deduplication](.ISSUES/content-deduplication.md)

### Roadmap Status
**HYBRID_ROADMAP.md - Phase 3 In Progress Groups:**
```markdown
#### Group 2: Content Pipeline Enhancements (3 tasks) - 📋 NOT STARTED
- [ ] Enhanced Reddit Scraper - Multi-subreddit, incremental updates, duplicate detection
- [ ] Social Media Sources - Instagram and TikTok content collection
- [ ] Content Deduplication System - Fuzzy matching and semantic similarity

**Location:** `issues/group_2/`  
**Effort:** 14-20 hours  
**Priority:** P1 (High)
```

---

## Next Steps for Developers

### To Start Working

1. **Review context:**
   - Read [Group 2 README](README.md)
   - Review existing implementations in `scripts/` directory
   - Check completed issues in `issues/resolved/p0-content-pipeline/`

2. **Pick a task:**
   - Choose from the 3 tasks in `.ISSUES/`
   - Update `.NEXT.MD` with your chosen task
   - Create a feature branch: `feature/group2-{task-name}`

3. **Implementation:**
   - Follow TDD principles
   - Use existing patterns and interfaces
   - Write comprehensive tests
   - Update documentation

4. **Completion:**
   - All acceptance criteria met
   - Tests passing
   - Documentation updated
   - Move task file from `.ISSUES/` to `.DONE/`
   - Update `.NEXT.MD` and HYBRID_ROADMAP.md

### Development Setup

```bash
# Clone and setup
cd /path/to/StoryGenerator

# Install dependencies (will need to add new ones)
pip install -r requirements.txt

# For new tasks, add:
pip install fuzzywuzzy python-Levenshtein sentence-transformers
pip install instagrapi TikTokApi

# Run existing tests to verify setup
python -m pytest tests/

# Test existing scrapers
python scripts/reddit_scraper.py --dry-run
python scripts/scrapers/alt_sources_scraper.py --sources all --dry-run
python scripts/deduplicate_content.py --help
```

---

## Progress Tracking

**Overall Status:** 0/3 tasks complete (0%)

| Task | Status | Progress | Estimated | Started | Completed |
|------|--------|----------|-----------|---------|-----------|
| Enhanced Reddit Scraper | 📋 Not Started | 0% | 4-6h | - | - |
| Social Media Sources | 📋 Not Started | 0% | 6-8h | - | - |
| Enhanced Deduplication | 📋 Not Started | 0% | 4-6h | - | - |

**Total Effort:** 14-20 hours remaining

---

## Questions or Issues?

- Create a discussion in the GitHub repository
- Tag maintainers in PR comments
- Reference this hub issue for coordination
- Check [MainProgressHub.md](../../MainProgressHub.md) for workflow guidance
