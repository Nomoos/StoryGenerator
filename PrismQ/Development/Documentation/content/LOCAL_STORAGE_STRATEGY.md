# Local Storage Strategy (Simplified)

## Overview

This document provides a **simplified, local-first storage strategy** that avoids cloud complexity while maintaining good performance and organization.

## TL;DR - Quick Answer

**For local development/deployment:**
- ✅ **SQLite** for text content (ideas, scripts, metadata) - single file, no server needed
- ✅ **Local file system** for media files (audio, images, video) - simple, fast, no extra services
- ❌ **No PostgreSQL server** - avoid setup complexity
- ❌ **No Redis** - unnecessary for local use
- ❌ **No cloud storage** - keep everything local

**Result**: Simple, fast, zero external dependencies.

---

## Simplified Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   C# Application                            │
│                                                              │
│  ┌────────────────────┐         ┌──────────────────────┐   │
│  │  Text/Metadata     │         │  Media Files         │   │
│  │  Storage           │         │  Storage             │   │
│  │                    │         │                      │   │
│  │  SQLite Database   │         │  File System         │   │
│  │  (storygen.db)     │         │  (/data/media/)      │   │
│  │                    │         │                      │   │
│  │  • Ideas           │         │  • Audio files       │   │
│  │  • Scripts         │         │  • Images            │   │
│  │  • Metadata        │         │  • Videos            │   │
│  │  • File paths      │         │  • Subtitles         │   │
│  └────────────────────┘         └──────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Benefits**:
- ✅ No server setup required
- ✅ Single database file (portable, easy to backup)
- ✅ No network overhead
- ✅ Simple deployment
- ✅ Easy to develop and test
- ✅ Works on any OS (Windows, Linux, macOS)

---

## 1. SQLite for Text Content

### Why SQLite for Local Storage?

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| **Setup** | ✅ Zero - single file | ❌ Server install, configuration |
| **Performance** | ✅ Fast for single user | ✅ Fast for multiple users |
| **Backup** | ✅ Copy single file | ⚠️ Database tools required |
| **Portability** | ✅ Excellent | ⚠️ Limited |
| **Complexity** | ✅ Very low | ⚠️ Medium to high |
| **Dependencies** | ✅ None | ❌ Server process |

**Verdict**: SQLite is perfect for local single-user deployment.

### SQLite Schema

```sql
-- Story Ideas Table
CREATE TABLE story_ideas (
    id TEXT PRIMARY KEY,  -- UUID as TEXT
    title TEXT NOT NULL,
    segment TEXT,
    age_group TEXT,
    narrator_gender TEXT,
    tone TEXT,
    theme TEXT,
    emotional_core TEXT,
    viral_potential TEXT,  -- JSON as TEXT
    metadata TEXT,         -- JSON as TEXT
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    status TEXT DEFAULT 'draft'
);

-- Scripts Table
CREATE TABLE scripts (
    id TEXT PRIMARY KEY,
    story_idea_id TEXT REFERENCES story_ideas(id),
    version INTEGER DEFAULT 1,
    content TEXT NOT NULL,
    word_count INTEGER,
    generation_model TEXT,
    metadata TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- Voice Generations Table
CREATE TABLE voice_generations (
    id TEXT PRIMARY KEY,
    script_id TEXT REFERENCES scripts(id),
    voice_provider TEXT,
    voice_id TEXT,
    audio_file_path TEXT,  -- Relative path to file
    duration_seconds REAL,
    file_size_bytes INTEGER,
    lufs_level REAL,
    metadata TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- Video Productions Table
CREATE TABLE video_productions (
    id TEXT PRIMARY KEY,
    story_idea_id TEXT REFERENCES story_ideas(id),
    script_id TEXT REFERENCES scripts(id),
    voice_generation_id TEXT REFERENCES voice_generations(id),
    final_video_path TEXT,    -- Relative path to file
    thumbnail_path TEXT,       -- Relative path to file
    duration_seconds REAL,
    resolution TEXT,
    file_size_bytes INTEGER,
    status TEXT,
    metadata TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    completed_at TEXT
);

-- Media Files Registry (tracks all media files)
CREATE TABLE media_files (
    id TEXT PRIMARY KEY,
    video_production_id TEXT REFERENCES video_productions(id),
    media_type TEXT,  -- audio, image, video, subtitle
    file_path TEXT,   -- Relative path from data directory
    file_name TEXT,
    file_size_bytes INTEGER,
    mime_type TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- Indexes
CREATE INDEX idx_story_ideas_segment ON story_ideas(segment);
CREATE INDEX idx_story_ideas_status ON story_ideas(status);
CREATE INDEX idx_story_ideas_created ON story_ideas(created_at);
CREATE INDEX idx_scripts_story_idea ON scripts(story_idea_id);
CREATE INDEX idx_video_status ON video_productions(status);
CREATE INDEX idx_media_files_video ON media_files(video_production_id);
```

### C# Integration with SQLite

```csharp
using Microsoft.Data.Sqlite;
using System.Data;

public class StoryIdeaRepository
{
    private readonly string _connectionString;

    public StoryIdeaRepository(string dbPath = "data/storygen.db")
    {
        _connectionString = $"Data Source={dbPath}";
        InitializeDatabase();
    }

    private void InitializeDatabase()
    {
        using var connection = new SqliteConnection(_connectionString);
        connection.Open();

        // Create tables if they don't exist
        var createTableSql = @"
            CREATE TABLE IF NOT EXISTS story_ideas (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                segment TEXT,
                -- ... other columns
                created_at TEXT DEFAULT (datetime('now'))
            );
        ";

        using var command = new SqliteCommand(createTableSql, connection);
        command.ExecuteNonQuery();
    }

    public async Task<StoryIdea> CreateAsync(StoryIdea idea)
    {
        using var connection = new SqliteConnection(_connectionString);
        await connection.OpenAsync();

        var sql = @"
            INSERT INTO story_ideas (id, title, segment, age_group, narrator_gender,
                                     tone, theme, emotional_core, viral_potential, metadata)
            VALUES (@id, @title, @segment, @ageGroup, @gender, @tone, @theme,
                    @core, @viral, @metadata)";

        using var cmd = new SqliteCommand(sql, connection);
        cmd.Parameters.AddWithValue("@id", idea.Id.ToString());
        cmd.Parameters.AddWithValue("@title", idea.Title);
        cmd.Parameters.AddWithValue("@segment", idea.Segment);
        cmd.Parameters.AddWithValue("@ageGroup", idea.AgeGroup);
        cmd.Parameters.AddWithValue("@gender", idea.NarratorGender);
        cmd.Parameters.AddWithValue("@tone", idea.Tone);
        cmd.Parameters.AddWithValue("@theme", idea.Theme);
        cmd.Parameters.AddWithValue("@core", idea.EmotionalCore);
        cmd.Parameters.AddWithValue("@viral", JsonSerializer.Serialize(idea.ViralPotential));
        cmd.Parameters.AddWithValue("@metadata", JsonSerializer.Serialize(idea.Metadata));

        await cmd.ExecuteNonQueryAsync();

        return idea;
    }

    public async Task<StoryIdea?> GetByIdAsync(Guid id)
    {
        using var connection = new SqliteConnection(_connectionString);
        await connection.OpenAsync();

        var sql = "SELECT * FROM story_ideas WHERE id = @id";
        using var cmd = new SqliteCommand(sql, connection);
        cmd.Parameters.AddWithValue("@id", id.ToString());

        using var reader = await cmd.ExecuteReaderAsync();
        if (await reader.ReadAsync())
        {
            return new StoryIdea
            {
                Id = Guid.Parse(reader.GetString(0)),
                Title = reader.GetString(1),
                Segment = reader.GetString(2),
                // ... map other fields
            };
        }

        return null;
    }
}
```

---

## 2. File System for Media Files

### Directory Structure

```
data/
├── storygen.db                    # SQLite database file
├── media/
│   ├── audio/
│   │   ├── {video_id}/
│   │   │   ├── voiceover.mp3
│   │   │   └── voiceover_normalized.mp3
│   │   └── ...
│   ├── images/
│   │   ├── {video_id}/
│   │   │   ├── keyframe_000.png
│   │   │   ├── keyframe_001.png
│   │   │   └── ...
│   │   └── ...
│   ├── videos/
│   │   ├── {video_id}/
│   │   │   ├── clip_000.mp4
│   │   │   ├── clip_001.mp4
│   │   │   └── final.mp4
│   │   └── ...
│   ├── subtitles/
│   │   ├── {video_id}/
│   │   │   └── subtitles.srt
│   │   └── ...
│   └── thumbnails/
│       ├── {video_id}.jpg
│       └── ...
└── cache/                         # Temporary files
    └── ...
```

### File Path Management

```csharp
public class MediaStorageService
{
    private readonly string _basePath;
    private readonly StoryGeneratorDbContext _dbContext;

    public MediaStorageService(string basePath = "data/media")
    {
        _basePath = Path.GetFullPath(basePath);
        Directory.CreateDirectory(_basePath);
    }

    public async Task<string> SaveAudioAsync(
        Guid videoProductionId,
        Stream audioStream,
        string fileName = "voiceover.mp3")
    {
        // Create directory structure
        var audioDir = Path.Combine(_basePath, "audio", videoProductionId.ToString());
        Directory.CreateDirectory(audioDir);

        // Save file
        var filePath = Path.Combine(audioDir, fileName);
        using var fileStream = File.Create(filePath);
        await audioStream.CopyToAsync(fileStream);

        // Store relative path in database
        var relativePath = Path.Combine("audio", videoProductionId.ToString(), fileName);
        
        // Register in database
        await _dbContext.MediaFiles.AddAsync(new MediaFile
        {
            Id = Guid.NewGuid().ToString(),
            VideoProductionId = videoProductionId.ToString(),
            MediaType = "audio",
            FilePath = relativePath,
            FileName = fileName,
            FileSizeBytes = fileStream.Length,
            MimeType = "audio/mpeg"
        });
        await _dbContext.SaveChangesAsync();

        return relativePath;
    }

    public string GetFullPath(string relativePath)
    {
        return Path.Combine(_basePath, relativePath);
    }

    public async Task<bool> FileExistsAsync(string relativePath)
    {
        var fullPath = GetFullPath(relativePath);
        return File.Exists(fullPath);
    }

    public async Task DeleteVideoProductionFilesAsync(Guid videoProductionId)
    {
        // Get all media files for this video
        var mediaFiles = await _dbContext.MediaFiles
            .Where(m => m.VideoProductionId == videoProductionId.ToString())
            .ToListAsync();

        // Delete physical files
        foreach (var media in mediaFiles)
        {
            var fullPath = GetFullPath(media.FilePath);
            if (File.Exists(fullPath))
                File.Delete(fullPath);
        }

        // Delete database records
        _dbContext.MediaFiles.RemoveRange(mediaFiles);
        await _dbContext.SaveChangesAsync();
    }
}
```

---

## 3. Configuration

### appsettings.json

```json
{
  "Storage": {
    "Type": "Local",
    "Local": {
      "DatabasePath": "data/storygen.db",
      "MediaBasePath": "data/media",
      "CachePath": "data/cache"
    }
  },
  "OpenAI": {
    "ApiKey": "${OPENAI_API_KEY}",
    "Model": "gpt-4o-mini"
  },
  "ElevenLabs": {
    "ApiKey": "${ELEVENLABS_API_KEY}",
    "VoiceId": "EXAVITQu4vr4xnSDxMaL"
  }
}
```

### Dependency Injection Setup

```csharp
// Program.cs or Startup.cs
services.AddSingleton<IStoryIdeaRepository>(sp =>
{
    var config = sp.GetRequiredService<IConfiguration>();
    var dbPath = config["Storage:Local:DatabasePath"];
    return new StoryIdeaRepository(dbPath);
});

services.AddSingleton<IMediaStorageService>(sp =>
{
    var config = sp.GetRequiredService<IConfiguration>();
    var basePath = config["Storage:Local:MediaBasePath"];
    return new MediaStorageService(basePath);
});
```

---

## 4. Backup Strategy

### Simple Backup Script

```bash
#!/bin/bash
# backup.sh - Simple backup script

BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup database
cp data/storygen.db "$BACKUP_DIR/"

# Backup media files
cp -r data/media "$BACKUP_DIR/"

echo "Backup completed: $BACKUP_DIR"
```

### Automated Backups (Optional)

```csharp
public class BackupService : BackgroundService
{
    private readonly IConfiguration _config;
    private readonly ILogger<BackupService> _logger;

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                // Backup every 24 hours
                await Task.Delay(TimeSpan.FromHours(24), stoppingToken);
                await PerformBackupAsync();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Backup failed");
            }
        }
    }

    private async Task PerformBackupAsync()
    {
        var timestamp = DateTime.Now.ToString("yyyyMMdd_HHmmss");
        var backupDir = Path.Combine("backups", timestamp);
        Directory.CreateDirectory(backupDir);

        // Backup database
        var dbPath = _config["Storage:Local:DatabasePath"];
        File.Copy(dbPath, Path.Combine(backupDir, "storygen.db"));

        // Backup media (copy only changed files)
        var mediaPath = _config["Storage:Local:MediaBasePath"];
        CopyDirectory(mediaPath, Path.Combine(backupDir, "media"));

        _logger.LogInformation("Backup completed: {BackupDir}", backupDir);
    }
}
```

---

## 5. Performance Optimization

### SQLite Optimization

```sql
-- Enable WAL mode for better concurrency
PRAGMA journal_mode = WAL;

-- Increase cache size (10MB)
PRAGMA cache_size = -10000;

-- Optimize for speed
PRAGMA synchronous = NORMAL;
PRAGMA temp_store = MEMORY;

-- Analyze tables for query optimization
ANALYZE;
```

```csharp
public void OptimizeDatabase(string dbPath)
{
    using var connection = new SqliteConnection($"Data Source={dbPath}");
    connection.Open();

    // Enable optimizations
    ExecuteCommand(connection, "PRAGMA journal_mode = WAL");
    ExecuteCommand(connection, "PRAGMA cache_size = -10000");
    ExecuteCommand(connection, "PRAGMA synchronous = NORMAL");
    ExecuteCommand(connection, "PRAGMA temp_store = MEMORY");
    ExecuteCommand(connection, "ANALYZE");
}
```

### File System Optimization

- ✅ Use SSD storage for better I/O performance
- ✅ Organize files by video ID for easy cleanup
- ✅ Use relative paths in database for portability
- ✅ Clean up temporary files regularly

---

## 6. Storage Estimates

### Per Video

| Content Type | Size | Storage Location |
|-------------|------|------------------|
| Story Idea (JSON) | 5KB | SQLite database |
| Script (text) | 3KB | SQLite database |
| Metadata | 2KB | SQLite database |
| Voice Audio (MP3) | 2MB | File system |
| Keyframes (10 images) | 10MB | File system |
| Video Clips | 20MB | File system |
| Final Video (MP4) | 50MB | File system |
| Subtitles (SRT) | 5KB | File system |
| **Total** | **~82MB** | |

### Database Size

- **1,000 videos**: ~10MB database + ~82GB media files
- **10,000 videos**: ~100MB database + ~820GB media files

**Database remains small** - most data is in file system.

---

## 7. Migration from Cloud (If Needed)

If you later decide to use cloud storage, the migration is simple:

```csharp
public interface IStorageProvider
{
    Task<string> SaveFileAsync(string relativePath, Stream content);
    Task<Stream> GetFileAsync(string relativePath);
    Task DeleteFileAsync(string relativePath);
}

// Local implementation
public class LocalStorageProvider : IStorageProvider
{
    // Current implementation
}

// Future cloud implementation (if needed)
public class S3StorageProvider : IStorageProvider
{
    // S3 implementation
}

// Just swap the implementation in DI
services.AddSingleton<IStorageProvider, LocalStorageProvider>();
// or
services.AddSingleton<IStorageProvider, S3StorageProvider>();
```

---

## Comparison: Local vs Cloud

| Aspect | Local Storage | Cloud Storage |
|--------|--------------|---------------|
| **Setup Complexity** | ✅ Very Low | ⚠️ Medium |
| **Cost** | ✅ Hardware only | 💰 Ongoing fees |
| **Performance** | ✅ Excellent (local I/O) | ⚠️ Network dependent |
| **Backup** | ⚠️ Manual required | ✅ Automatic |
| **Scalability** | ⚠️ Limited by disk | ✅ Unlimited |
| **Dependencies** | ✅ None | ❌ Network, accounts |
| **Best For** | Single machine, local | Multiple machines, distributed |

**For local deployment: Local storage wins on simplicity and performance.**

---

## Recommended Setup

### Minimal Setup

```bash
# 1. Create directory structure
mkdir -p data/media/{audio,images,videos,subtitles,thumbnails}
mkdir -p data/cache

# 2. Initialize database (done automatically by C# on first run)
# The application will create storygen.db on first launch

# 3. Configure paths in appsettings.json
# Already provided above

# 4. Run the application
dotnet run
```

### That's It!

No server setup, no cloud accounts, no complex configuration.

---

## Summary

### Recommended Local Strategy

**Database**: SQLite (`data/storygen.db`)
- ✅ Single file
- ✅ Zero configuration
- ✅ Excellent performance for single user
- ✅ Easy backup (just copy the file)

**Media Files**: Local file system (`data/media/`)
- ✅ Simple organization by type and video ID
- ✅ Fast access (no network)
- ✅ Easy cleanup (delete folders)
- ✅ Portable (copy entire data folder)

**No External Services Required**:
- ❌ No PostgreSQL server
- ❌ No Redis
- ❌ No cloud storage
- ❌ No complex setup

### Benefits

1. **Simplicity**: 5 minutes to set up
2. **Performance**: Local I/O is faster than network
3. **Cost**: Free (just disk space)
4. **Portability**: Copy `data/` folder to move everything
5. **Backup**: Simple file copy
6. **Development**: Easy to test and debug

### When to Consider Cloud

Only consider cloud storage if:
- Multiple machines need to access the same data
- You need >1TB of storage
- You want automatic backups and redundancy
- You're deploying to multiple servers

For single-machine local deployment, **stick with the simple local storage strategy**.

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-08  
**Status**: Recommended for Local Deployment
