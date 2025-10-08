# Security: Remove Exposed API Keys from Source Code

**ID:** `security-api-keys`  
**Priority:** P0 (Critical)  
**Effort:** 2-4 hours  
**Status:** Not Started  
**Severity:** CRITICAL ⚠️ URGENT

## Overview

Multiple API keys are hardcoded directly in source files, creating a critical security vulnerability. Anyone with repository access can misuse these keys, and they are permanently exposed in Git history. This requires immediate action to prevent unauthorized API usage and billing.

## Current State

### Exposed Keys

- **OpenAI API Key** exposed in:
  - `Generators/GStoryIdeas.py` (line 6)
  - `Generators/GScript.py` (line 8)
  - `Generators/GRevise.py` (line 9)
  - `Generators/GEnhanceScript.py` (line 7)

- **ElevenLabs API Key** exposed in:
  - `Generators/GVoice.py` (line 16)

### Impact

- ❌ Anyone with repository access can misuse these keys
- ❌ Keys are in Git history permanently
- ❌ Potential for unauthorized API usage and billing
- ❌ Violation of security best practices

## Dependencies

**Requires:**
- None (can be done immediately)

**Blocks:**
- Production deployment
- Public repository sharing
- Team collaboration

## Acceptance Criteria

### Immediate Actions (Within 24 hours)
- [ ] Revoke ALL exposed API keys immediately
- [ ] Generate new API keys from OpenAI and ElevenLabs
- [ ] Remove keys from all source files
- [ ] Verify keys are no longer accessible in code

### Short-term Actions (Within 1 week)
- [ ] Implement environment variable management
- [ ] Install and configure `python-dotenv` package
- [ ] Create `.env` file for local development
- [ ] Add `.env` to `.gitignore`
- [ ] Update all code to read from environment variables
- [ ] Create `.env.example` file for documentation

### Documentation
- [ ] Document environment variable setup in README.md
- [ ] Add security guidelines to CONTRIBUTING.md
- [ ] Update deployment documentation

### Verification
- [ ] Confirm no API keys exist in source code
- [ ] Verify `.env` is in `.gitignore`
- [ ] Test that application works with environment variables
- [ ] Scan repository for any remaining secrets

## Task Details

### 1. Immediate Key Revocation

```bash
# Log into OpenAI Dashboard
# Navigate to API Keys
# Revoke exposed keys
# Generate new keys

# Log into ElevenLabs Dashboard
# Navigate to API Keys
# Revoke exposed keys
# Generate new keys
```

### 2. Install python-dotenv

```bash
pip install python-dotenv
```

Add to `requirements.txt`:
```
python-dotenv>=1.0.0
```

### 3. Create `.env.example` File

```bash
# .env.example
OPENAI_API_KEY=your_openai_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here
```

### 4. Update `.gitignore`

```bash
# Add to .gitignore
.env
*.env
!.env.example
```

### 5. Update Code to Use Environment Variables

**Before:**
```python
# Bad - hardcoded
openai.api_key = "sk-proj-..."
```

**After:**
```python
# Good - from environment
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")
```

### Files to Update

1. `Generators/GStoryIdeas.py`
2. `Generators/GScript.py`
3. `Generators/GRevise.py`
4. `Generators/GEnhanceScript.py`
5. `Generators/GVoice.py`

### 6. Testing

```bash
# Create a test .env file
echo "OPENAI_API_KEY=test-key" > .env
echo "ELEVENLABS_API_KEY=test-key" >> .env

# Run application
python main.py

# Verify it reads from .env
# Verify no hardcoded keys remain
```

## Output Files

- `.env.example` - Template for environment variables
- Updated `requirements.txt` - Include python-dotenv
- Updated `.gitignore` - Exclude .env files
- Updated source files - No hardcoded keys

## Related Files

- `Generators/GStoryIdeas.py`
- `Generators/GScript.py`
- `Generators/GRevise.py`
- `Generators/GEnhanceScript.py`
- `Generators/GVoice.py`
- `.gitignore`
- `requirements.txt`
- `README.md`

## Security Scanning

After implementation, run security checks:

```bash
# Install git-secrets or similar
git secrets --scan

# Or use truffleHog
pip install truffleHog
truffleHog --regex --entropy=True .
```

## Notes

- ⚠️ **CRITICAL**: This is the highest priority security issue
- 🔑 Old keys must be revoked IMMEDIATELY before any other work
- 📝 Document the proper way to set up API keys for new developers
- 🔒 Consider using a secrets manager for production (AWS Secrets Manager, Azure Key Vault, etc.)
- 📊 Audit Git history to identify if keys were used maliciously

## Next Steps

After completion:
- All other development work can proceed safely
- Repository can be shared publicly (if desired)
- Team members can collaborate without security concerns
- Production deployment becomes safe

## Related Documentation

- See `docs/RESEARCH_AND_IMPROVEMENTS.md` Section 1
- Python dotenv documentation: https://pypi.org/project/python-dotenv/
