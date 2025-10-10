# Step {STEP_NUMBER}: {STEP_NAME}

## Purpose

{Brief description of what this step does and why it's important in the pipeline}

## Status

**Implementation:** {✅ Complete | ⚠️ Partial | ❌ Not Started}  
**Testing:** {✅ Tested | ⚠️ Needs Testing | ❌ Not Tested}  
**Documentation:** {✅ Complete | ⚠️ Partial | ❌ Missing}

## Dependencies

**Requires:**
- Previous step(s): {list}
- API services: {list}
- Models/Libraries: {list}

**Outputs used by:**
- Next step(s): {list}

## Implementation

### Code Location

**C# Implementation:**
- Primary: `{path to main C# file}`
- Supporting: `{path to supporting files}`

**Python Implementation:**
- Primary: `{path to main Python file}`
- Supporting: `{path to supporting files}`

### Key Classes/Functions

- `{ClassName}` - {brief description}
- `{FunctionName}` - {brief description}

## Input/Output

### Input Format

**Location:** `{input directory path}`

**Format:**
```json
{
  "example": "input",
  "structure": "here"
}
```

**Requirements:**
- {requirement 1}
- {requirement 2}

### Output Format

**Location:** `{output directory path}`

**Format:**
```json
{
  "example": "output",
  "structure": "here"
}
```

**Artifacts Created:**
- `{filename}` - {description}
- `{filename}` - {description}

## Usage

### CLI Command

```bash
# Example CLI command to run this step
dotnet run --project src/CSharp/StoryGenerator.CLI -- {command} {args}
```

### Programmatic Usage

```csharp
// C# Example
var stage = new {StageName}(logger, config);
var output = await stage.ExecuteAsync(input);
```

```python
# Python Example
from {module} import {function}
result = {function}(input_data)
```

### Configuration

**Required Settings:**
```json
{
  "config": {
    "key": "value"
  }
}
```

**Optional Settings:**
- `{setting}` - {description} (default: {value})

## Testing

### Manual Test

```bash
# Step-by-step manual test procedure
1. {step 1}
2. {step 2}
3. Verify: {what to check}
```

### Automated Tests

**Test Files:**
- `{test file path}` - {description}

**Run Tests:**
```bash
# C# tests
dotnet test src/CSharp/StoryGenerator.Tests --filter "ClassName"

# Python tests
pytest tests/test_{module}.py
```

## Error Handling

**Common Errors:**

1. **{Error Type}**
   - Cause: {description}
   - Solution: {how to fix}

2. **{Error Type}**
   - Cause: {description}
   - Solution: {how to fix}

**Retry Policy:** {description of retry behavior}

**Graceful Degradation:** {description of fallback behavior}

## Performance

**Expected Runtime:** {time estimate}  
**Resource Requirements:**
- CPU: {requirements}
- Memory: {requirements}
- GPU: {requirements if applicable}
- API Calls: {count and type}

**Optimization Tips:**
- {tip 1}
- {tip 2}

## Related Documentation

- [Main Issue](./issue.md) - Detailed requirements and checklist
- [Pipeline Guide](../../src/CSharp/PIPELINE_GUIDE.md) - Overall pipeline architecture
- [Quick Start](../../issues/QUICKSTART.md) - Getting started guide
- {other relevant docs}

## Examples

### Example 1: {Scenario Name}

**Input:**
```json
{example input}
```

**Command:**
```bash
{command to run}
```

**Expected Output:**
```json
{example output}
```

### Example 2: {Scenario Name}

{another complete example}

## Troubleshooting

**Q: {Common question}**  
A: {Answer}

**Q: {Common question}**  
A: {Answer}

## Changelog

- **{Date}**: {Change description}
- **{Date}**: Initial implementation

---

**Last Updated:** {Date}  
**Maintained By:** {Team/Person}
