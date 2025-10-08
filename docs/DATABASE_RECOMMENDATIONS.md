# Database Recommendations for StoryGenerator

## Overview

This document provides comprehensive database recommendations for storing ideas, text content, and media assets in the StoryGenerator pipeline.

> **🏠 For Local/Simplified Deployment**: See [LOCAL_STORAGE_STRATEGY.md](./LOCAL_STORAGE_STRATEGY.md) for a simpler approach using SQLite + local file system (zero external dependencies, 5-minute setup).

> **☁️ This Document**: Covers enterprise/cloud deployment with PostgreSQL + Object Storage (for distributed systems, multiple servers).

## Database Strategy by Content Type

### 1. Text Content Storage (Ideas, Scripts, Metadata)

#### Recommended: PostgreSQL with JSON Support

**Why PostgreSQL?**
- ✅ Excellent JSON/JSONB support for flexible schema
- ✅ Full ACID compliance for data integrity
- ✅ Rich text search capabilities (tsvector, tsquery)
- ✅ Mature .NET integration (Npgsql, Entity Framework Core)
- ✅ Free and open source
- ✅ Excellent performance for structured + semi-structured data
- ✅ Supports full-text search and indexing

**Schema Design:**

```sql
-- Story Ideas Table
CREATE TABLE story_ideas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    segment VARCHAR(50),  -- teens, young_adults, adults
    age_group VARCHAR(50),  -- 10-15, 16-20, 21-30
    narrator_gender VARCHAR(20),
    tone TEXT,
    theme TEXT,
    emotional_core TEXT,
    viral_potential JSONB,  -- Store complex scoring data
    metadata JSONB,  -- Flexible metadata storage
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(50) DEFAULT 'draft'
);

-- Scripts Table
CREATE TABLE scripts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    story_idea_id UUID REFERENCES story_ideas(id),
    version INTEGER DEFAULT 1,  -- v1, v2, v3, etc.
    content TEXT NOT NULL,
    word_count INTEGER,
    generation_model VARCHAR(100),  -- gpt-4o-mini, qwen2.5-14b
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Voice Generation Records
CREATE TABLE voice_generations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    script_id UUID REFERENCES scripts(id),
    voice_provider VARCHAR(50),  -- elevenlabs, resemble
    voice_id VARCHAR(100),
    audio_file_path TEXT,
    duration_seconds DECIMAL(10,2),
    file_size_bytes BIGINT,
    lufs_level DECIMAL(5,2),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Video Productions Table
CREATE TABLE video_productions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    story_idea_id UUID REFERENCES story_ideas(id),
    script_id UUID REFERENCES scripts(id),
    voice_generation_id UUID REFERENCES voice_generations(id),
    final_video_path TEXT,
    thumbnail_path TEXT,
    duration_seconds DECIMAL(10,2),
    resolution VARCHAR(20),  -- 1080x1920
    file_size_bytes BIGINT,
    status VARCHAR(50),  -- rendering, completed, failed
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- Performance Metrics
CREATE TABLE pipeline_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    video_production_id UUID REFERENCES video_productions(id),
    stage_name VARCHAR(100),
    duration_ms INTEGER,
    success BOOLEAN,
    error_message TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_story_ideas_segment ON story_ideas(segment);
CREATE INDEX idx_story_ideas_status ON story_ideas(status);
CREATE INDEX idx_story_ideas_created ON story_ideas(created_at DESC);
CREATE INDEX idx_scripts_story_idea ON scripts(story_idea_id);
CREATE INDEX idx_video_status ON video_productions(status);

-- Full-text search indexes
CREATE INDEX idx_story_ideas_title_fts ON story_ideas USING gin(to_tsvector('english', title));
CREATE INDEX idx_scripts_content_fts ON scripts USING gin(to_tsvector('english', content));
```

**C# Integration:**

```csharp
using Npgsql;
using System.Data;

public class StoryIdeaRepository : IStoryIdeaRepository
{
    private readonly string _connectionString;

    public async Task<StoryIdea> CreateAsync(StoryIdea idea)
    {
        using var connection = new NpgsqlConnection(_connectionString);
        await connection.OpenAsync();

        var sql = @"
            INSERT INTO story_ideas (title, segment, age_group, narrator_gender, 
                                     tone, theme, emotional_core, viral_potential, metadata)
            VALUES (@title, @segment, @ageGroup, @gender, @tone, @theme, 
                    @core, @viral::jsonb, @metadata::jsonb)
            RETURNING id, created_at";

        using var cmd = new NpgsqlCommand(sql, connection);
        cmd.Parameters.AddWithValue("title", idea.Title);
        cmd.Parameters.AddWithValue("segment", idea.Segment);
        cmd.Parameters.AddWithValue("ageGroup", idea.AgeGroup);
        cmd.Parameters.AddWithValue("gender", idea.NarratorGender);
        cmd.Parameters.AddWithValue("tone", idea.Tone);
        cmd.Parameters.AddWithValue("theme", idea.Theme);
        cmd.Parameters.AddWithValue("core", idea.EmotionalCore);
        cmd.Parameters.AddWithValue("viral", JsonSerializer.Serialize(idea.ViralPotential));
        cmd.Parameters.AddWithValue("metadata", JsonSerializer.Serialize(idea.Metadata));

        using var reader = await cmd.ExecuteReaderAsync();
        if (await reader.ReadAsync())
        {
            idea.Id = reader.GetGuid(0);
            idea.CreatedAt = reader.GetDateTime(1);
        }

        return idea;
    }
}
```

**Alternative: Entity Framework Core**

```csharp
public class StoryGeneratorDbContext : DbContext
{
    public DbSet<StoryIdea> StoryIdeas { get; set; }
    public DbSet<Script> Scripts { get; set; }
    public DbSet<VoiceGeneration> VoiceGenerations { get; set; }
    public DbSet<VideoProduction> VideoProductions { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<StoryIdea>(entity =>
        {
            entity.ToTable("story_ideas");
            entity.HasKey(e => e.Id);
            entity.Property(e => e.ViralPotential)
                .HasColumnType("jsonb");
            entity.HasIndex(e => e.Segment);
            entity.HasIndex(e => e.CreatedAt);
        });
    }
}
```

### 2. Media File Storage (Audio, Images, Video)

#### Recommended: Object Storage + Database References

**Option A: Cloud Object Storage (Recommended for Production)**

- **AWS S3** / **Azure Blob Storage** / **Google Cloud Storage**
- Store file metadata in PostgreSQL, actual files in object storage
- Benefits:
  - Scalable (unlimited storage)
  - Cost-effective ($0.023/GB/month for AWS S3 Standard)
  - Built-in CDN integration
  - Automatic redundancy and backups
  - Direct browser upload/download

**Option B: Local File System + Database**

For development or on-premises deployment:

```csharp
public class MediaStorageService : IMediaStorageService
{
    private readonly string _basePath = "/data/media";
    private readonly IMediaRepository _repository;

    public async Task<string> StoreAudioAsync(
        Guid videoProductionId,
        Stream audioStream,
        string fileName)
    {
        // Store file
        var relativePath = $"audio/{videoProductionId}/{fileName}";
        var fullPath = Path.Combine(_basePath, relativePath);
        Directory.CreateDirectory(Path.GetDirectoryName(fullPath));

        using var fileStream = File.Create(fullPath);
        await audioStream.CopyToAsync(fileStream);

        // Store metadata in database
        await _repository.CreateMediaRecordAsync(new MediaRecord
        {
            VideoProductionId = videoProductionId,
            MediaType = "audio",
            FilePath = relativePath,
            FileSize = fileStream.Length,
            CreatedAt = DateTime.UtcNow
        });

        return relativePath;
    }
}
```

**Hybrid Approach (Recommended):**

```sql
CREATE TABLE media_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    video_production_id UUID REFERENCES video_productions(id),
    media_type VARCHAR(50),  -- audio, image, video, subtitle
    storage_type VARCHAR(50),  -- local, s3, azure_blob
    file_path TEXT,  -- relative path or object key
    file_name VARCHAR(500),
    file_size_bytes BIGINT,
    mime_type VARCHAR(100),
    storage_metadata JSONB,  -- bucket, region, etc.
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### Option C: PostgreSQL Binary Storage (Not Recommended for Large Files)

PostgreSQL can store binary data via BYTEA or Large Objects (LOB), but this is **NOT recommended** for video files because:
- ❌ Poor performance for large files (>10MB)
- ❌ Database bloat
- ❌ Backup/restore complexity
- ❌ No streaming support
- ✅ OK for small files (<1MB) like thumbnails

**Only use for small assets:**

```sql
CREATE TABLE thumbnails (
    id UUID PRIMARY KEY,
    video_production_id UUID REFERENCES video_productions(id),
    image_data BYTEA,  -- Store small images (<1MB)
    mime_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 3. Caching Layer

#### Recommended: Redis

For caching API responses, viral scores, and frequently accessed data:

```csharp
public class CachedIdeaService : IIdeaService
{
    private readonly IDatabase _redis;
    private readonly IStoryIdeaRepository _repository;

    public async Task<StoryIdea> GetByIdAsync(Guid id)
    {
        // Try cache first
        var cached = await _redis.StringGetAsync($"idea:{id}");
        if (cached.HasValue)
            return JsonSerializer.Deserialize<StoryIdea>(cached);

        // Fallback to database
        var idea = await _repository.GetByIdAsync(id);
        
        // Cache for 1 hour
        await _redis.StringSetAsync(
            $"idea:{id}",
            JsonSerializer.Serialize(idea),
            TimeSpan.FromHours(1)
        );

        return idea;
    }
}
```

## Comparison Table

| Database | Text Content | Media Files | Caching | Best For |
|----------|--------------|-------------|---------|----------|
| **PostgreSQL** | ✅ Excellent | ⚠️ Small files only | ❌ No | Primary data store |
| **MySQL** | ✅ Good | ⚠️ Limited | ❌ No | Alternative to PostgreSQL |
| **MongoDB** | ✅ Good | ⚠️ GridFS for files | ✅ Yes | Document flexibility |
| **Redis** | ⚠️ Not primary | ❌ No | ✅ Excellent | Caching, sessions |
| **S3/Blob** | ❌ No | ✅ Excellent | ❌ No | Media file storage |
| **SQLite** | ✅ Good | ❌ No | ❌ No | Development only |

## Recommended Stack

### Development Environment
```yaml
databases:
  primary: PostgreSQL 16
  cache: Redis 7
  media: Local filesystem
```

### Production Environment
```yaml
databases:
  primary: PostgreSQL 16 (RDS/Azure Database/Cloud SQL)
  cache: Redis 7 (ElastiCache/Azure Cache/Memorystore)
  media: S3/Azure Blob Storage/Google Cloud Storage
```

## Storage Estimates

For **1,000 videos**:

| Content Type | Size per Item | Total Storage |
|-------------|---------------|---------------|
| Story Ideas (JSON) | ~5KB | 5MB |
| Scripts (text) | ~3KB | 3MB |
| Voice Audio (MP3) | ~2MB | 2GB |
| Keyframe Images | ~10MB (10 frames) | 10GB |
| Final Videos (MP4) | ~50MB | 50GB |
| Subtitles (SRT) | ~5KB | 5MB |
| **Total** | | **~62GB** |

**PostgreSQL**: ~50MB for metadata  
**Object Storage**: ~62GB for media files

## Configuration Example

```json
{
  "ConnectionStrings": {
    "StoryGeneratorDb": "Host=localhost;Database=storygenerator;Username=app;Password=***"
  },
  "Redis": {
    "ConnectionString": "localhost:6379",
    "InstanceName": "storygenerator:"
  },
  "Storage": {
    "Type": "S3",  // or "Local", "AzureBlob"
    "S3": {
      "BucketName": "storygenerator-media",
      "Region": "us-east-1",
      "AccessKeyId": "***",
      "SecretAccessKey": "***"
    },
    "Local": {
      "BasePath": "/data/media"
    }
  }
}
```

## Summary

**Recommended Architecture:**
- ✅ **PostgreSQL** for all text content, metadata, and relationships
- ✅ **S3/Azure Blob** for all media files (audio, images, video)
- ✅ **Redis** for caching API responses and frequently accessed data
- ✅ **File system paths** stored as strings in PostgreSQL
- ✅ Use UUIDs for primary keys (better for distributed systems)

**Benefits:**
- Clear separation of concerns
- Scalable to millions of videos
- Cost-effective storage
- Fast query performance
- Easy backup and recovery

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-08  
**Status**: Production Recommendation
