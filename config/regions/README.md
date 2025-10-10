# Short Video System Configuration

This directory contains configuration files for the Short Video Generation and Distribution System.

## Configuration Files

### Main Configuration

**`short_video_config.yaml`** - Master configuration file for the entire system

This file contains:
- Region definitions (Tier 1, Tier 2, Emerging markets)
- Content strategy settings
- Pipeline stage configurations
- Localization settings
- Automation rules
- Monetization targets
- Analytics configuration
- Technical settings (database, storage, API keys)

### Region-Specific Configuration

**`regions/{REGION_CODE}.json`** - Per-region configuration files

Each region file contains:
- Region metadata (locale, language, timezone)
- Monetization data (CPM estimates, priority tier)
- Platform settings (YouTube, TikTok, Instagram)
- Voice configuration (provider, voice IDs, alternatives)
- Localization guidelines
- Content preferences and trending topics
- Demographics data
- Compliance requirements
- SEO keywords and hashtags
- Analytics benchmarks

**Available Regions:**
- `US.json` - United States (Tier 1, highest CPM) - Main Channel: Nom Stories (EN)
- `ES.json` - Spain (Tier 2) - Nom Scary Stories ES
- `CZ.json` - Czech Republic (Tier 3) - Nom Scary Stories CZ
- `PL.json` - Poland (Tier 2) - Nom Scary Stories PL
- `HI.json` - India (Tier 3) - Nom Scary Stories HI
- `DE.json` - Germany (Tier 1) - Nom Scary Stories DE
- `JP.json` - Japan (Tier 2)
- More regions to be added (UK, CA, AU, FR, IT, etc.)

## Usage

### Loading Configuration

**Python:**
```python
import yaml
import json

# Load main config
with open('config/short_video_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Load region config
with open('config/regions/US.json', 'r') as f:
    region_config = json.load(f)

# Access settings
cpm_estimate = region_config['monetization']['cpm_estimate']
voice_id = region_config['voice']['voice_id']
```

**C#:**
```csharp
using YamlDotNet.Serialization;
using System.Text.Json;

// Load main config
var yaml = File.ReadAllText("config/short_video_config.yaml");
var deserializer = new DeserializerBuilder().Build();
var config = deserializer.Deserialize<Dictionary<string, object>>(yaml);

// Load region config
var json = File.ReadAllText("config/regions/US.json");
var regionConfig = JsonSerializer.Deserialize<RegionConfig>(json);

// Access settings
var cpmEstimate = regionConfig.Monetization.CpmEstimate;
var voiceId = regionConfig.Voice.VoiceId;
```

### Environment Variables

The following environment variables must be set:

**API Keys:**
- `OPENAI_API_KEY` - OpenAI GPT-4 API key
- `ELEVENLABS_API_KEY` - ElevenLabs TTS API key
- `DEEPL_API_KEY` - DeepL translation API key
- `YOUTUBE_API_KEY` - YouTube Data API key (optional)
- `TIKTOK_API_KEY` - TikTok API key (optional)
- `INSTAGRAM_API_KEY` - Instagram Graph API key (optional)

**Database:**
- `DB_PASSWORD` - PostgreSQL database password

**Storage (if using cloud):**
- `AWS_ACCESS_KEY` - AWS S3 access key
- `AWS_SECRET_KEY` - AWS S3 secret key
- `AZURE_STORAGE_CONNECTION` - Azure Blob Storage connection string

### Configuration Validation

Run validation to check your configuration:

```bash
# Python
python scripts/validate_config.py config/short_video_config.yaml

# Expected output:
# ✓ Main configuration valid
# ✓ All required fields present
# ✓ Region configurations valid
# ✓ API keys configured
```

## Configuration Structure

### Priority Tiers

**Tier 1 (P0):** Highest priority, highest CPM
- US, UK, CA, AU, DE
- Full localization, premium voice actors
- Daily monitoring and optimization

**Tier 2 (P1):** High priority, good CPM
- JP, FR, NO, SE, DK
- Standard localization, quality voices
- Weekly monitoring

**Tier 3 / Emerging (P2-P3):** Medium-low priority
- CZ, PL, other emerging markets
- Basic localization, automated translation
- Monthly monitoring

### Content Categories

1. **Education (35%)** - Study tips, tutorials, how-to guides
2. **Entertainment (30%)** - Did you know?, fun facts, storytime
3. **Technology (20%)** - AI tools, app reviews, tech tips
4. **Lifestyle (15%)** - Productivity, fitness, motivation

### Demographics

**Age Ranges:**
- 13-17: Gen Z teenagers (TikTok, YouTube)
- 18-24: Gen Z young adults (TikTok, Instagram, YouTube)
- 25-34: Millennials (Instagram, YouTube)
- 35-44: Older millennials (YouTube, Instagram)

**Gender:**
- Male: 48%
- Female: 50%
- Other: 2%

## Customization

### Adding a New Region

1. Create new region configuration file:
```bash
cp config/regions/US.json config/regions/UK.json
```

2. Edit the new file with region-specific settings:
- Update `region.code`, `region.name`, `region.locale`
- Adjust `monetization.cpm_estimate`
- Configure `voice` settings with appropriate accent
- Customize `localization.reference_examples`
- Update `content_preferences.trending_topics`

3. Add region to main config:
```yaml
# config/short_video_config.yaml
regions:
  tier1:
    - code: UK
      locale: en-GB
      language: English (UK)
      cpm_estimate: 11.0
      priority: 1
      # ... rest of config
```

### Modifying Pipeline Stages

Edit `pipeline.stages` in `short_video_config.yaml`:

```yaml
pipeline:
  stages:
    script_generation:
      model_local: llama3.1-8b  # Change to different model
      variations: 15              # Increase variations
      temperature: 0.9            # More creative
```

### Adjusting Monetization Targets

Edit `monetization` section:

```yaml
monetization:
  target_cpm: 12.0              # Increase target
  min_video_views: 2000         # Higher threshold
  priority_regions: [US, UK]    # Focus on fewer regions
```

## Best Practices

1. **Start Small:** Begin with 1-2 regions (US, UK)
2. **Test Configuration:** Always validate before deploying
3. **Monitor Performance:** Adjust CPM estimates based on actual data
4. **Backup Configs:** Keep versioned backups of working configurations
5. **Environment-Specific:** Use different configs for dev/staging/prod
6. **Security:** Never commit API keys - use environment variables

## Troubleshooting

### Configuration Not Loading

**Issue:** `FileNotFoundError: config/short_video_config.yaml`

**Solution:** Ensure you're running from repository root:
```bash
cd /path/to/StoryGenerator
python scripts/generate_videos.py
```

### Invalid YAML Syntax

**Issue:** `yaml.scanner.ScannerError`

**Solution:** Validate YAML syntax online or with:
```bash
python -c "import yaml; yaml.safe_load(open('config/short_video_config.yaml'))"
```

### Missing Environment Variables

**Issue:** `KeyError: 'OPENAI_API_KEY'`

**Solution:** Set required environment variables:
```bash
export OPENAI_API_KEY="sk-..."
export ELEVENLABS_API_KEY="..."
```

Or create `.env` file:
```bash
cp .env.example .env
# Edit .env with your keys
```

## Related Documentation

### Branding & Channel Strategy
- [Branding Documentation](../../docs/branding/) - Complete branding and channel strategy
- [Channel Naming Strategy](../../docs/branding/CHANNEL_NAMING_STRATEGY.md) - Global naming conventions
- [Persona Definition](../../docs/branding/PERSONA_NOM_STORIES_EN.md) - US target audience (Nom Stories EN)
- [Metadata Guidelines](../../docs/branding/METADATA_GUIDELINES.md) - Localized SEO best practices
- [Channel Templates](../../docs/branding/CHANNEL_TEMPLATES.md) - Ready-to-use channel setup templates

### System Design & Research
- [SHORT_VIDEO_SYSTEM_DESIGN.md](../research/SHORT_VIDEO_SYSTEM_DESIGN.md) - Complete system design
- [SHORT_VIDEO_SYSTEM_DESIGN_CS.md](../research/SHORT_VIDEO_SYSTEM_DESIGN_CS.md) - Czech summary
- [VIRAL_VIDEO_REQUIREMENTS.md](../research/VIRAL_VIDEO_REQUIREMENTS.md) - Video requirements spec
- [YOUTUBE_CONTENT_STRATEGY.md](../research/YOUTUBE_CONTENT_STRATEGY.md) - YouTube strategy

## Support

For questions or issues:
- GitHub Issues: https://github.com/Nomoos/StoryGenerator/issues
- Documentation: `docs/` directory
- Configuration examples: `config/` directory

---

**Last Updated:** 2025-01-09  
**Version:** 1.0.0
