# Branding & Channel Strategy

This directory contains comprehensive branding guidelines and channel strategy documentation for the Nom Stories global expansion.

---

## 📚 Documentation

### Core Strategy Documents

#### [CHANNEL_NAMING_STRATEGY.md](./CHANNEL_NAMING_STRATEGY.md)
**Complete global channel naming convention and expansion strategy**

Defines:
- Main channel naming format (Nom Stories EN)
- Scary Stories channel format (Nom Scary Stories [LANG])
- Language code standards (ISO 2-letter)
- Brand consistency guidelines
- Local SEO optimization strategy
- 6 initial launch languages (EN, ES, CZ, PL, HI, DE)

**Key Sections:**
- Naming conventions and rationale
- Channel examples for all languages
- Localization vs. global branding strategy
- SEO & discovery best practices
- Brand identity guidelines (visual, tone, voice)
- Performance tracking metrics
- Risk mitigation strategies
- Future expansion plans

---

#### [PERSONA_NOM_STORIES_EN.md](./PERSONA_NOM_STORIES_EN.md)
**Target audience definition for main US channel**

Defines:
- Primary persona: "Emma" - 15-year-old US teenage female
- Complete demographics and psychographics
- Content consumption habits across platforms
- Content preferences and avoidances
- Engagement triggers and sharing motivators
- Voice and tone guidelines
- Content calendar and theme mix

**Key Sections:**
- Detailed persona profile
- Platform preferences (TikTok, YouTube Shorts, Instagram)
- Content tone and style guide
- 5 content pillars (friendship, school, relationships, family, growth)
- Success metrics and engagement indicators
- Competitor analysis
- Script format and voiceover guidelines

---

#### [METADATA_GUIDELINES.md](./METADATA_GUIDELINES.md)
**Localized SEO and metadata best practices**

Defines:
- Where to apply global brand vs. local SEO
- Channel-level metadata (global focus)
- Video-level metadata (local focus)
- Content-level localization (full adaptation)
- Platform-specific guidelines (YouTube, TikTok, Instagram)
- Translation vs. localization best practices

**Key Sections:**
- Metadata hierarchy (channel → video → content)
- Language-specific keyword research
- SEO best practices by language (ES, CZ, DE, PL, HI)
- Localization quality checklist
- Monitoring and optimization framework

---

#### [CHANNEL_TEMPLATES.md](./CHANNEL_TEMPLATES.md)
**Ready-to-use templates for channel setup**

Provides:
- Complete channel setup templates for all 6 languages
- Channel description templates (bilingual)
- Video metadata templates (titles, descriptions, tags)
- Playlist name templates
- Community post templates
- Poll and engagement templates

**Templates Included:**
- Nom Stories (EN) - Real Life Stories
- Nom Scary Stories EN, ES, CZ, PL, HI, DE
- Video metadata for each language
- Playlist structures
- Community engagement posts

---

## 🌍 Target Markets

### Priority Tier 1 (P0-P1)
High CPM, Large markets, immediate focus

| Language | Code | Channel Name | Region Config | Status |
|----------|------|--------------|---------------|--------|
| English (US) | EN | Nom Stories (EN) | [US.json](../../config/regions/US.json) | ✅ Primary |
| English | EN | Nom Scary Stories EN | [US.json](../../config/regions/US.json) | 📋 Planned |
| Spanish | ES | Nom Scary Stories ES | [ES.json](../../config/regions/ES.json) | 📋 Planned |
| German | DE | Nom Scary Stories DE | [DE.json](../../config/regions/DE.json) | 📋 Planned |

### Priority Tier 2 (P2)
Growing markets, good engagement

| Language | Code | Channel Name | Region Config | Status |
|----------|------|--------------|---------------|--------|
| Czech | CZ | Nom Scary Stories CZ | [CZ.json](../../config/regions/CZ.json) | 📋 Planned |
| Polish | PL | Nom Scary Stories PL | [PL.json](../../config/regions/PL.json) | 📋 Planned |
| Hindi | HI | Nom Scary Stories HI | [HI.json](../../config/regions/HI.json) | 📋 Planned |

### Priority Tier 3 (Future)
Emerging markets, expansion phase

| Language | Code | Potential Channel | Status |
|----------|------|-------------------|--------|
| French | FR | Nom Scary Stories FR | 🔮 Future |
| Portuguese | PT | Nom Scary Stories PT | 🔮 Future |
| Italian | IT | Nom Scary Stories IT | 🔮 Future |
| Japanese | JP | Nom Scary Stories JP | 🔮 Future |

---

## 📊 Brand Architecture

```
Nom Stories (Brand)
│
├── Nom Stories (EN)              [Main Channel - Real Life Stories]
│   └── Target: US female teens (15 y/o)
│   └── Content: Relatable teen drama, real experiences
│   └── Platforms: YouTube Shorts, TikTok, Instagram Reels
│
└── Nom Scary Stories [LANG]      [Genre Expansion - Horror]
    │
    ├── Nom Scary Stories EN      [English Horror]
    │   └── Target: Global English speakers (13-25)
    │   └── Content: True horror, urban legends, paranormal
    │
    ├── Nom Scary Stories ES      [Spanish Horror]
    │   └── Target: Spain + Latin America (13-25)
    │   └── Content: Historias de terror, leyendas urbanas
    │
    ├── Nom Scary Stories CZ      [Czech Horror]
    │   └── Target: Czech Republic (13-25)
    │   └── Content: Strašidelné příběhy, městské legendy
    │
    ├── Nom Scary Stories PL      [Polish Horror]
    │   └── Target: Poland (13-25)
    │   └── Content: Historie grozy, miejskie legendy
    │
    ├── Nom Scary Stories HI      [Hindi Horror]
    │   └── Target: India (13-25)
    │   └── Content: डरावनी कहानियाँ, भूतिया कहानियां
    │
    └── Nom Scary Stories DE      [German Horror]
        └── Target: Germany/Austria/Switzerland (13-25)
        └── Content: Gruselgeschichten, urbane Legenden
```

---

## 🎯 Quick Start Guide

### For Channel Launch

1. **Review Strategy Documents**
   - Read [CHANNEL_NAMING_STRATEGY.md](./CHANNEL_NAMING_STRATEGY.md)
   - Review target language's region config in [config/regions/](../../config/regions/)
   - Study [METADATA_GUIDELINES.md](./METADATA_GUIDELINES.md)

2. **Use Channel Templates**
   - Copy template from [CHANNEL_TEMPLATES.md](./CHANNEL_TEMPLATES.md)
   - Customize for specific language/region
   - Follow naming convention exactly

3. **Configure Technical Setup**
   - Use region JSON file for technical config
   - Set voice provider and voice ID
   - Configure platform settings

4. **Create Initial Content**
   - Follow persona guidelines (if Main Channel)
   - Use metadata templates for first 5 videos
   - Apply localization (not just translation)

5. **Launch & Monitor**
   - Track metrics defined in strategy docs
   - Optimize based on performance
   - Report findings for future channels

---

## 🔗 Related Documentation

### Configuration Files
- [Region Configs](../../config/regions/) - Technical configuration per region
- [US.json](../../config/regions/US.json) - United States (Main Channel)
- [ES.json](../../config/regions/ES.json) - Spain (Spanish)
- [CZ.json](../../config/regions/CZ.json) - Czech Republic
- [PL.json](../../config/regions/PL.json) - Poland
- [HI.json](../../config/regions/HI.json) - India (Hindi)
- [DE.json](../../config/regions/DE.json) - Germany

### Research & Strategy
- [YouTube Content Strategy](../../research/YOUTUBE_CONTENT_STRATEGY.md) - Platform research
- [Short Video System Design](../../research/SHORT_VIDEO_SYSTEM_DESIGN.md) - System architecture
- [Viral Video Requirements](../../research/VIRAL_VIDEO_REQUIREMENTS.md) - Content optimization

### Implementation
- [Integration Guide](../guides/setup/INTEGRATION_GUIDE.md) - Technical implementation
- [Pipeline Orchestration](../../docs/PIPELINE_ORCHESTRATION.md) - Content pipeline

---

## ✅ Implementation Checklist

### Channel Strategy (Complete)
- [x] Define global naming convention
- [x] Create naming strategy document
- [x] Define primary persona (US female teen)
- [x] Create metadata guidelines
- [x] Prepare channel templates for 6 languages
- [x] Create region configs (ES, PL, HI)
- [x] Document brand identity guidelines

### Next Steps (To Do)
- [ ] Reserve YouTube handles for all channels
- [ ] Create brand kit (logos, banners, thumbnails)
- [ ] Launch Nom Stories (EN) - Main Channel
- [ ] Prepare initial content (5 videos per channel)
- [ ] Set up analytics tracking
- [ ] Launch Nom Scary Stories ES (first expansion)
- [ ] Monitor performance and optimize

---

## 📈 Success Metrics

### Channel Level
- Subscriber count and growth rate
- Total views and watch time
- Average view duration
- Engagement rate (likes, comments, shares)
- Click-through rate (CTR)

### Content Level
- Video performance (views, retention)
- Best performing content themes
- Optimal posting times validation
- Thumbnail and title A/B test results

### Brand Level
- Cross-channel recognition
- Brand search volume
- Channel interconnectivity
- Global vs. local traffic balance

---

## 🤝 Contributing

### Updating Branding Documents

1. **Minor Updates**: Fix typos, update examples
   - Edit directly, commit with clear message
   
2. **Major Changes**: Strategy shifts, new markets
   - Open issue for discussion
   - Get approval from brand strategy lead
   - Update related documents

3. **New Languages**: Adding new regions
   - Create region config in `config/regions/`
   - Add channel template
   - Update this README
   - Add to metadata guidelines

---

## 📞 Contact

For questions about branding and channel strategy:
- **GitHub Issues**: https://github.com/Nomoos/StoryGenerator/issues
- **Labels**: `branding`, `naming`, `youtube`, `seo`, `persona`

For channel-specific questions:
- **Main Channel (EN)**: Use label `nom-stories-en`
- **Scary Stories**: Use label `scary-stories` + language code

---

## 📝 Document Versions

| Document | Version | Last Updated | Next Review |
|----------|---------|--------------|-------------|
| Channel Naming Strategy | 1.0 | 2025-10-10 | 2025-11-10 |
| Persona (EN) | 1.0 | 2025-10-10 | 2025-11-10 |
| Metadata Guidelines | 1.0 | 2025-10-10 | 2025-11-10 |
| Channel Templates | 1.0 | 2025-10-10 | Monthly |

---

**Status:** ✅ Strategy Defined & Documented  
**Phase:** Pre-Launch  
**Next Milestone:** Reserve handles and launch first channel  

---

*This branding documentation ensures consistent global expansion while maintaining local market relevance. All channel launches must follow these guidelines.*
