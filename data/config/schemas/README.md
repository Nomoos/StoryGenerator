# JSON Schemas

This directory contains JSON Schema definitions for the StoryGenerator project.

## title.json

Defines the schema for title items with the following structure:

```json
{
  "id": "uuid",
  "segment": "women|men",
  "age_bucket": "10-13|14-17|18-23",
  "title": "string",
  "topic_ids": ["..."],
  "created_utc": "ISO-8601"
}
```

### Fields

- **id** (string, uuid): Unique identifier for the title
- **segment** (enum): Target audience segment - must be "women" or "men"
- **age_bucket** (enum): Target age range - must be "10-13", "14-17", or "18-23"
- **title** (string): The title text
- **topic_ids** (array): Array of related topic identifiers
- **created_utc** (string, ISO-8601): Creation timestamp

All fields are required.

### Example

See `title.example.json` for a complete example.

### C# Implementation

Corresponding C# classes are available:
- Model: `/CSharp/Models/TitleSchema.cs`
- Interface: `/CSharp/Interfaces/ITitleSchemaReader.cs`
