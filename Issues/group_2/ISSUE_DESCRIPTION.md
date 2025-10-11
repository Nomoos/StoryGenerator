# Group 2 — Progress & Coordination Hub (Issue Description)

This is the formatted issue description for the Group 2 Progress & Coordination Hub GitHub issue.

---

# Group 2 — Progress & Coordination Hub

This issue tracks all unfinished tasks, current priorities, and blockers for **Group 2** development in StoryGenerator. Maintainers should update this issue with:
- The current priority from `issues/group_2/.NEXT.MD`
- Unfinished tasks from `issues/group_2/.ISSUES/`
- Blockers, risks, and links to roadmaps or child issues

---

## 📅 Update Checklist
- [x] `.NEXT.MD` is up to date
- [x] Unfinished tasks listed below
- [x] Blockers/risks noted
- [x] Roadmap synced

---

## Current Focus (`.NEXT.MD`)

**Phase:** Content to Script Pipeline Enhancement
**Status:** 📋 Ready to start - 3 tasks available (14-20 hours)

### Recently Completed
✅ **Idea Generation Pipeline** - All 7 tasks complete (Reddit adaptation, LLM generation, clustering, title generation, scoring, voice recommendations, top selection)
- See: [group-2-idea-generation](issues/resolved/phase-3-implementation/group-2-idea-generation/)

### Available Work
Group 2 now focuses on **enhanced content collection**:
- 3 Content Collection tasks (14-20h)

**Next Recommended:** `content-reddit-scraper-enhanced` (4-6h) or `content-deduplication` (4-6h)

---

## Unfinished Tasks

### 📦 Content Collection & Sourcing (14-20h)

1. **Enhanced Reddit Scraper** ([content-reddit-scraper-enhanced.md](issues/group_2/.ISSUES/content-reddit-scraper-enhanced.md)) - 4-6h - P1
   - Multi-subreddit scraping with better filtering and rate limiting
   - Incremental updates (fetch only new content)
   - Content quality filtering (score, length, engagement)
   - JSON output with full metadata

2. **Content Deduplication System** ([content-deduplication.md](issues/group_2/.ISSUES/content-deduplication.md)) - 4-6h - P1
   - Exact duplicate detection (hash-based)
   - Near-duplicate detection (fuzzy matching)
   - Semantic similarity detection (embeddings)
   - Configurable similarity thresholds
   - Duplicate tracking and reporting

3. **Alternative Content Sources** ([content-social-media-sources.md](issues/group_2/.ISSUES/content-social-media-sources.md)) - 6-8h - P1
   - Instagram content scraping
   - TikTok content scraping
   - Content normalization across sources
   - Quality scoring across platforms
   - API credential management

---

## Blockers/Risks

### Current Blockers
**None** - All tasks are independent and ready to start

### Potential Risks

🟡 **Medium Risk:**
- **API Rate Limits:** Reddit, Instagram, TikTok APIs have strict rate limits
  - *Mitigation:* Implement proper rate limiting, retry logic, caching
- **API Access Requirements:** Need API credentials for each platform
  - *Mitigation:* Document setup clearly, provide mock/test data

🟢 **Low Risk:**
- **API Changes:** Social media APIs may change
  - *Mitigation:* Use maintained libraries (praw, instaloader), pin versions
- **Content Quality Variance:** Different platforms have different quality
  - *Mitigation:* Platform-specific filters, content normalization

---

## Execution Strategy

### Recommended Order
1. **Phase 1:** content-reddit-scraper-enhanced (establish primary source)
2. **Phase 2:** content-deduplication + content-social-media-sources (parallel)

### Parallelization
All tasks are independent and can be worked in parallel by different team members.

### Timeline
- **With 1 developer:** 2-2.5 weeks sequential
- **With 2-3 developers:** 1-1.5 weeks with parallel work

---

## Links

### Documentation
- **Hub:** [MainProgressHub.md](../../MainProgressHub.md) - Overall progress structure
- **Roadmap:** [docs/roadmaps/HYBRID_ROADMAP.md](../../docs/roadmaps/HYBRID_ROADMAP.md) - Project roadmap
- **Status:** [GROUP_2_STATUS.md](GROUP_2_STATUS.md) - Detailed Group 2 status

### Group 2 Resources
- **README:** [README.md](README.md)
- **Current Focus:** [.NEXT.MD](.NEXT.MD)
- **Open Issues:** [.ISSUES/](.ISSUES/)
- **Completed:** [.DONE/](.DONE/)

### Related Work
- **Completed Group 2:** [group-2-idea-generation](../../issues/resolved/phase-3-implementation/group-2-idea-generation/)
- **Group 1:** [group_1](../group_1/) - Provides infrastructure
- **Other Groups:** [group_3](../group_3/), [group_4](../group_4/)

---

**Last Updated:** 2025-10-10
**Maintainer:** @Nomoos
**Agent Instructions:** Group 2 (Content Pipeline): 3 issues (14-20h) - content collection, sourcing, deduplication
