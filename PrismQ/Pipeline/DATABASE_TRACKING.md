# Database-Backed Story Tracking

The Windows pipeline includes database-backed story tracking using SQLite for improved visibility and management of pipeline execution.

## Features

- **Story Registration**: Automatically track all stories processed through the pipeline
- **Status Tracking**: Monitor the status of each step for every story (pending, running, completed, failed)
- **Execution History**: Maintain a complete history of all step executions with timestamps and execution times
- **Acceptance Tracking**: Record acceptance criteria results for each step
- **Query Interface**: Query story status, pending stories, and pipeline statistics

## Database Support

The system uses **SQLite** for simple, zero-configuration storage:

- **No configuration needed** - works out of the box
- Database stored at: `data/pipeline_stories.db`
- Perfect for single-machine and multi-user setups
- Zero external dependencies
- Lightweight and fast

## Configuration

Add to your `.env` file (optional - has sensible defaults):

```env
# Database Configuration
DB_PATH=data/pipeline_stories.db
```

## Database Schema

### Stories Table
Stores story metadata:
- `story_id` (unique identifier)
- `title` (story title)
- `source` (origin: manual, reddit, pipeline, etc.)
- `metadata` (JSON/JSONB for additional data)
- `created_at`, `updated_at` (timestamps)

### Step Status Table
Tracks current status of each step:
- `story_id` (reference to story)
- `step_name` (e.g., "01_ingest")
- `status` (pending, running, completed, failed)
- `run_id` (execution identifier)
- `error_message` (if failed)
- `acceptance_passed` (boolean)
- `acceptance_details` (acceptance check results)
- `started_at`, `completed_at` (timestamps)

### Step History Table
Complete audit trail:
- `story_id`, `step_name`, `run_id`
- `status` (final status)
- `error_message` (if applicable)
- `execution_time_ms` (duration in milliseconds)
- `timestamp` (when executed)

## Usage

### Automatic Tracking

Database tracking is **enabled by default** when you run the pipeline:

```cmd
REM Database tracking happens automatically
.\pipeline\scripts\all.bat STORY-123
```

### Disable Database Tracking

Use `--no-db` flag to disable:

```cmd
REM Use filesystem-only mode (no database)
env\Scripts\python.exe pipeline\orchestration\run_step.py ^
  --step 01_ingest --story-id STORY-123 --action run --no-db
```

### Query Story Status

Get the status of all steps for a story:

```cmd
env\Scripts\python.exe pipeline\orchestration\run_step.py ^
  --action status --story-id STORY-123
```

Output:
```json
{
  "story": {
    "story_id": "STORY-123",
    "title": "My Story",
    "source": "pipeline",
    "created_at": "2025-10-10 14:30:00"
  },
  "steps": [
    {
      "step_name": "01_ingest",
      "status": "completed",
      "acceptance_passed": true,
      "completed_at": "2025-10-10 14:30:15"
    },
    {
      "step_name": "02_preprocess",
      "status": "running",
      "started_at": "2025-10-10 14:30:20"
    }
  ]
}
```

### Query Pipeline Statistics

Get statistics across all stories and steps:

```cmd
env\Scripts\python.exe pipeline\orchestration\run_step.py --action stats
```

Output:
```json
{
  "01_ingest": {
    "completed": 45,
    "failed": 2,
    "running": 1
  },
  "02_preprocess": {
    "completed": 43,
    "running": 2
  },
  "03_generate": {
    "completed": 38,
    "failed": 5
  }
}
```

## Integration with Existing Scripts

The `.bat` scripts automatically use the database when available. No changes needed to your workflow!

### Example: Full Pipeline with Database Tracking

```cmd
C:\StoryGenerator> .\pipeline\scripts\all.bat STORY-456

[01_ingest] Database tracking enabled
[01_ingest] run_id=20241010-143022 story_id=STORY-456
[01_ingest] execution succeeded
[01_ingest] acceptance met for story_id=STORY-456

[02_preprocess] Database tracking enabled
[02_preprocess] run_id=20241010-143022 story_id=STORY-456
...
```

### Check Status After Pipeline

```cmd
C:\StoryGenerator> env\Scripts\python.exe pipeline\orchestration\run_step.py ^
  --action status --story-id STORY-456

{
  "story": {
    "story_id": "STORY-456",
    "source": "pipeline"
  },
  "steps": [
    {
      "step_name": "01_ingest",
      "status": "completed",
      "acceptance_passed": true,
      "execution_time_ms": 1234
    },
    {
      "step_name": "02_preprocess",
      "status": "completed",
      "acceptance_passed": true,
      "execution_time_ms": 2345
    },
    ...
  ]
}
```

## Benefits

### 1. **Visibility**
- See which stories are pending, running, or completed at each step
- Track acceptance criteria pass/fail rates
- Monitor execution times

### 2. **Debugging**
- Query full history of step executions
- Identify which stories failed and why
- Review error messages and execution details

### 3. **Reporting**
- Generate reports on pipeline throughput
- Analyze bottlenecks (which steps take longest)
- Track success rates per step

### 4. **Lightweight & Portable**
- SQLite database is a single file
- Easy to back up and transfer
- No external database server required

## Monitoring Queries

### Find Failed Stories

```python
from pipeline.orchestration.story_db import StoryDatabase

db = StoryDatabase()
db.initialize()

# Get all failed stories
cursor = db.connection.cursor()
cursor.execute("""
    SELECT story_id, step_name, error_message 
    FROM step_status 
    WHERE status = 'failed'
""")
for row in cursor.fetchall():
    print(dict(row))
```

### Find Stories Stuck at a Step

```python
# Stories that have been "running" for too long
cursor.execute("""
    SELECT story_id, step_name, started_at
    FROM step_status
    WHERE status = 'running' 
      AND started_at < datetime('now', '-1 hour')
""")
```

### Get Slowest Steps

```python
# Average execution time per step
cursor.execute("""
    SELECT step_name, 
           AVG(execution_time_ms) as avg_time_ms,
           COUNT(*) as executions
    FROM step_history
    WHERE status = 'completed'
    GROUP BY step_name
    ORDER BY avg_time_ms DESC
""")
```

## Migration

### From Filesystem-Only to Database

The database integration is **non-disruptive**:

1. Stories already processed via filesystem continue to work
2. Database starts tracking new executions automatically
3. Old stories can be retroactively registered if needed

### Retroactively Register Stories

```python
from pipeline.orchestration.story_db import StoryDatabase
from pathlib import Path

db = StoryDatabase()
db.initialize()

# Register existing stories from filesystem
for story_file in Path("outputs/01_ingest").glob("*.json"):
    story_id = story_file.stem
    db.register_story(story_id, source="retroactive")
    db.update_step_status(story_id, "01_ingest", "completed")
```

## Troubleshooting

### Database Connection Fails

If database connection fails, the system automatically falls back to filesystem-only mode:

```
WARNING - Database initialization failed: ... Using filesystem-only mode.
```

The pipeline continues to work normally, just without database tracking.

### Database Schema Out of Date

If you upgrade and the schema has changed, re-initialize:

```python
from pipeline.orchestration.story_db import StoryDatabase

db = StoryDatabase()
db.initialize()  # Creates or updates tables
```

## Performance Considerations

### SQLite
- Suitable for: 1000s-10000s of stories
- Single writer at a time (reads are concurrent)
- Fast for single-machine setups
- Database file can grow to several GB without performance issues
- Lightweight and portable

### Indexes

The schema includes indexes on:
- `stories.story_id`
- `step_status.story_id`, `step_status.step_name`, `step_status.status`
- `step_history.story_id`

These ensure fast queries even with large datasets.

## See Also

- [Pipeline README](../scripts/README.md) - Main pipeline documentation
- [Examples](../scripts/EXAMPLES.md) - Usage examples
- [Implementation Summary](../IMPLEMENTATION_SUMMARY.md) - Architecture details
