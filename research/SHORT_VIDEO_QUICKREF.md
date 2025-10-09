# Short Video System - Quick Reference Guide

**Version:** 1.0  
**Last Updated:** 2025-01-09

## Overview

Quick reference for the Short Video Generation and Distribution System. For complete details, see [SHORT_VIDEO_SYSTEM_DESIGN.md](./SHORT_VIDEO_SYSTEM_DESIGN.md).

---

## 📋 Quick Facts

| Metric | Target |
|--------|--------|
| **Production Capacity** | 50-100 videos/day (Phase 3) |
| **Cost per Video** | $0.22-0.95 (base) + $0.15-0.40 (localization) |
| **Target CPM** | $8-15 (Tier 1 regions) |
| **Pipeline Duration** | 15-30 minutes per video |
| **Supported Platforms** | YouTube Shorts, TikTok, Instagram Reels |
| **Supported Languages** | 10+ (expandable) |

---

## 🌍 Region Priorities

### Tier 1 (Highest CPM) - Priority: P0
- **US** ($12.5 CPM) - English (US)
- **UK** ($11.0 CPM) - English (UK)
- **CA** ($10.5 CPM) - English (Canada)
- **AU** ($10.0 CPM) - English (Australia)
- **DE** ($10.5 CPM) - German

### Tier 2 (High CPM) - Priority: P1
- **JP** ($9.0 CPM) - Japanese
- **FR** ($8.5 CPM) - French
- **NO** ($9.5 CPM) - Norwegian

### Tier 3 / Emerging - Priority: P2-P3
- **CZ** ($4.5 CPM) - Czech
- **PL** ($5.0 CPM) - Polish
- Others (expandable)

---

## 🎬 Pipeline Stages

### Stage 1: Trend Analysis (5-10 min)
- **Model:** Mistral 7B / Llama 3.1 8B (local)
- **Input:** Google Trends, YouTube, TikTok, Reddit
- **Output:** 20-50 prioritized video concepts
- **Cost:** Minimal (local inference)

### Stage 2: Script Generation (2-5 min)
- **Model:** Llama 3.1 8B → GPT-4o (hybrid)
- **Input:** Video concept with hook
- **Output:** 30-60 second script (60-100 words)
- **Cost:** $0.02-0.05 per script

### Stage 3: Voiceover Generation (1-3 min)
- **Provider:** ElevenLabs (primary), Azure TTS (fallback)
- **Input:** Script + locale
- **Output:** High-quality audio (48kHz, -16 LUFS)
- **Cost:** $0.10-0.30 per voiceover

### Stage 4: Visual Generation (5-15 min)
- **Tools:** SDXL, Stable Diffusion, Stock APIs
- **Input:** Script + visual prompts
- **Output:** 3-8 keyframe images (9:16, 1080x1920)
- **Cost:** $0.05-0.50 (varies by method)

### Stage 5: Subtitle Generation (1-2 min)
- **Tool:** WhisperX
- **Input:** Voiceover audio
- **Output:** Word-level subtitles with timing
- **Cost:** $0.05-0.10

### Stage 6: Video Assembly (2-5 min)
- **Tool:** FFmpeg
- **Input:** Audio + visuals + subtitles
- **Output:** Final MP4 (9:16, 30fps, H.264)
- **Cost:** $0.05-0.10 (compute)

### Stage 7: Post-Production (1-2 min)
- Thumbnail generation
- Metadata optimization (title, description, hashtags)
- Platform-specific formatting
- **Cost:** Minimal

---

## 💰 Cost Structure

### Per Video (Base)
- Script: $0.02-0.05
- Voiceover: $0.10-0.30
- Visuals: $0.05-0.50
- Processing: $0.05-0.10
- **Total:** $0.22-0.95

### Per Localization
- Translation: $0.05-0.10
- Additional voiceover: $0.10-0.30
- **Total:** $0.15-0.40

### Monthly Fixed
- AI APIs: $200-500
- Storage/hosting: $50-100
- Tools: $100-200
- **Total:** $350-800

### Break-Even Analysis
- Cost per video: ~$1.30 (base + localization)
- Revenue at 10k views (US): $10-15
- **Break-even:** ~1,000 views per video

---

## 📊 Success Metrics

### Technical
- ✅ Pipeline uptime: >99%
- ✅ Video generation time: <10 min
- ✅ Error rate: <5%
- ✅ Quality score: >80/100

### Content
- 🎯 Watch time: >80%
- 🎯 Engagement rate: >5%
- 🎯 Viral rate: >1% (10k+ views)
- 🎯 CPM: >$8 (Tier 1)

### Business
- 💰 Monthly revenue: $5k+ (Month 6)
- 💰 Subscriber growth: >10%/month
- 💰 ROI: >200% (Year 1)

---

## 🗂️ Configuration Files

### Main Config
```
config/short_video_config.yaml
```
Contains:
- Region definitions
- Pipeline settings
- Automation rules
- Monetization targets

### Region Configs
```
config/regions/{REGION_CODE}.json
```
Available:
- US.json (United States)
- DE.json (Germany)
- JP.json (Japan)
- CZ.json (Czech Republic)

---

## 🚀 Quick Start

### 1. Installation
```bash
# Clone repository
git clone https://github.com/Nomoos/StoryGenerator.git
cd StoryGenerator

# Install dependencies
pip install -r requirements.txt

# Copy configuration
cp config/short_video_config.example.yaml config/short_video_config.yaml
```

### 2. Configuration
```bash
# Set environment variables
export OPENAI_API_KEY="sk-..."
export ELEVENLABS_API_KEY="..."

# Edit configuration
nano config/short_video_config.yaml
```

### 3. Generate First Video
```python
from pipeline import ShortVideoPipeline

pipeline = ShortVideoPipeline()
result = pipeline.generate_video(
    topic="AI productivity tips",
    locale="en-US",
    platform="youtube"
)
```

---

## 📈 Implementation Phases

### Phase 1: MVP (Weeks 1-4)
- ✅ Single region (US)
- ✅ English only
- ✅ 10-20 test videos
- ✅ Basic analytics

### Phase 2: Localization (Weeks 5-8)
- 🔄 5 regions (US, UK, CA, AU, DE)
- 🔄 Automated localization
- 🔄 Cost optimization
- 🔄 50+ videos generated

### Phase 3: Scaling (Weeks 9-12)
- 🔄 50-100 videos/day
- 🔄 Content gap analysis
- 🔄 Batch automation
- 🔄 Analytics dashboard

### Phase 4: Monetization (Months 4-6)
- ⏳ Monetization approval
- ⏳ 10+ regions
- ⏳ $5k+/month revenue
- ⏳ Brand partnerships

---

## 🎨 Platform Specifications

### YouTube Shorts
- **Aspect Ratio:** 9:16
- **Resolution:** 1080x1920 or 720x1280
- **Duration:** 15-60 seconds (optimal: 30-45s)
- **Format:** MP4 (H.264)
- **Frame Rate:** 30 fps
- **Hashtags:** 3 max recommended
- **Watch Time:** Critical for algorithm

### TikTok
- **Aspect Ratio:** 9:16
- **Resolution:** 1080x1920
- **Duration:** 15-60 seconds
- **Format:** MP4
- **Frame Rate:** 30 fps
- **Hashtags:** Up to 30
- **Trending Audio:** Important for discovery

### Instagram Reels
- **Aspect Ratio:** 9:16
- **Resolution:** 1080x1920
- **Duration:** 15-90 seconds (optimal: 30-60s)
- **Format:** MP4
- **Frame Rate:** 30 fps
- **Hashtags:** Up to 30
- **Visual Quality:** High importance

---

## 🔧 Common Commands

### Generate Videos
```bash
# Single video
python scripts/generate_video.py --topic "AI tips" --locale en-US

# Batch generation
python scripts/batch_generate.py --count 10 --locale en-US

# With localization
python scripts/generate_video.py --topic "AI tips" \
  --locales en-US,de-DE,ja-JP
```

### Trend Analysis
```bash
# Fetch latest trends
python scripts/fetch_trends.py --sources google,youtube,tiktok

# Analyze content gaps
python scripts/analyze_gaps.py --region US --min-score 70
```

### Analytics
```bash
# Generate report
python scripts/analytics_report.py --start 2025-01-01 --end 2025-01-31

# Export data
python scripts/export_analytics.py --format csv
```

---

## 🆘 Troubleshooting

### Video Generation Fails
1. Check API keys are set
2. Verify configuration file is valid
3. Check disk space
4. Review error logs

### Low CPM
1. Focus on Tier 1 regions
2. Improve watch time (hook, pacing)
3. Optimize titles and thumbnails
4. A/B test different formats

### Poor Engagement
1. Strengthen hook (first 3 seconds)
2. Add dynamic subtitles
3. Use trending topics
4. Test different video lengths

---

## 📚 Documentation

### Design Documents
- [SHORT_VIDEO_SYSTEM_DESIGN.md](./SHORT_VIDEO_SYSTEM_DESIGN.md) - Complete system design
- [SHORT_VIDEO_SYSTEM_DESIGN_CS.md](./SHORT_VIDEO_SYSTEM_DESIGN_CS.md) - Czech summary

### Configuration
- [config/regions/README.md](../config/regions/README.md) - Region config guide
- [config/short_video_config.yaml](../config/short_video_config.yaml) - Master config

### Related Research
- [VIRAL_VIDEO_REQUIREMENTS.md](./VIRAL_VIDEO_REQUIREMENTS.md) - Video requirements
- [YOUTUBE_CONTENT_STRATEGY.md](./YOUTUBE_CONTENT_STRATEGY.md) - YouTube strategy
- [ai-model-comparison-for-game-design.md](./gpt-research/ai-model-comparison-for-game-design.md) - AI pipeline

---

## 💡 Pro Tips

### Content Strategy
- ✅ Focus on Tier 1 regions (80/20 rule)
- ✅ Localize top performers (>10k views)
- ✅ Test hooks extensively (first 3 seconds)
- ✅ Use trending topics (24-48h window)
- ✅ Batch production for efficiency

### Optimization
- 🎯 Watch time > views (algorithm priority)
- 🎯 CTR > 5% (good performance)
- 🎯 Engagement > 5% (viral potential)
- 🎯 Subtitle usage critical (mobile viewing)
- 🎯 Platform-specific optimization

### Monetization
- 💰 Reach thresholds quickly (focus, consistency)
- 💰 Diversify platforms (reduce risk)
- 💰 Build affiliate partnerships early
- 💰 Track CPM by region (optimize allocation)
- 💰 Reinvest revenue into scaling

---

## 🔗 Quick Links

- **Repository:** https://github.com/Nomoos/StoryGenerator
- **Issues:** https://github.com/Nomoos/StoryGenerator/issues
- **Discussions:** https://github.com/Nomoos/StoryGenerator/discussions
- **Documentation:** `docs/` directory

---

## 📞 Support

**Technical Issues:**
- GitHub Issues with `short-video` label

**Questions:**
- GitHub Discussions

**Business Inquiries:**
- partnerships@example.com (placeholder)

---

**Status:** ✅ Complete  
**Maintained By:** StoryGenerator Team  
**License:** See repository LICENSE file
