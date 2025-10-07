# Issue Tracking System

This document describes the structured issue tracking system for the AI Video Pipeline project.

## 📋 Overview

The AI Video Pipeline is broken down into 10 major stages, each with its own GitHub issue template. This approach ensures:

- **Clear scope** for each component
- **Trackable progress** with checklists
- **Dependencies** are documented
- **Success criteria** are defined
- **Effort estimation** for planning

## 🗂️ Issue Templates

All issue templates are located in `.github/ISSUE_TEMPLATE/` and can be used when creating new issues on GitHub.

### Available Templates

| Stage | Template File | Component | Priority | Effort |
|-------|---------------|-----------|----------|--------|
| 1 | `01-environment-setup.yml` | Environment & Model Setup | High | 1-2 weeks |
| 2 | `02-asr-enhancement.yml` | ASR Enhancement | Medium | 1 week |
| 3 | `03-shotlist-generation.yml` | Shotlist Generation | High | 2 weeks |
| 4 | `04-vision-guidance.yml` | Vision Guidance (Optional) | Low | 2 weeks |
| 5 | `05-sdxl-keyframes.yml` | SDXL Keyframe Generation | High | 2 weeks |
| 6 | `06-video-synthesis.yml` | Video Synthesis | High | 3 weeks |
| 7 | `07-post-production.yml` | Post-Production | Medium | 1 week |
| 8 | `08-pipeline-integration.yml` | Pipeline Integration | High | 2 weeks |
| 9 | `09-csharp-implementation.yml` | C# Implementation | Low | 4+ weeks |
| 10 | `10-documentation.yml` | Documentation | Medium | 2 weeks |

## 🏷️ Labels

Each issue template includes predefined labels:

### Stage Labels
- `stage-1` through `stage-10` - Identifies which stage

### Priority Labels
- `priority: high` - Critical path items
- `priority: medium` - Important but not blocking
- `priority: low` - Nice to have, research phase

### Component Labels
- `setup` - Environment and infrastructure
- `asr` - Speech recognition
- `llm` - Large language models
- `vision` - Vision models
- `image-generation` - Image synthesis
- `video-generation` - Video synthesis
- `post-production` - Final processing
- `integration` - Pipeline orchestration
- `csharp` - C# implementation
- `documentation` - Docs and examples

### Type Labels
- `feature` - New functionality
- `enhancement` - Improvements to existing
- `research` - Investigation and planning

## 🔄 Issue Workflow

### 1. Creating Issues

To create a new issue from a template:

1. Go to the [Issues tab](https://github.com/Nomoos/StoryGenerator/issues)
2. Click "New Issue"
3. Select the appropriate stage template
4. Fill in any additional context
5. Submit the issue

### 2. Linking Issues

- Child issues should reference the parent issue
- Use "Part of #X" or "Closes #X" in issue descriptions
- Dependencies should be clearly stated

### 3. Progress Tracking

Each issue contains:
- **Subtasks**: Detailed checklist of work items
- **Testing**: Validation steps
- **Success Criteria**: Definition of done
- **Files**: What needs to be created/modified

Mark checkboxes as you complete work:
```markdown
- [x] Completed task
- [ ] Pending task
```

### 4. Closing Issues

Close an issue when:
- All subtasks are complete
- Testing passes
- Success criteria are met
- Code is merged to main branch

## 📊 Implementation Status

### Current Status (as of template creation)

| Stage | Status | Progress |
|-------|--------|----------|
| Stage 1: Environment Setup | 🔄 Partial | 40% |
| Stage 2: ASR Enhancement | ✅ Implemented | 80% |
| Stage 3: Shotlist Generation | 📋 Planned | 0% |
| Stage 4: Vision Guidance | 📋 Planned | 0% |
| Stage 5: SDXL Keyframes | 📋 Planned | 0% |
| Stage 6: Video Synthesis | 📋 Planned | 0% |
| Stage 7: Post-Production | 🔄 Partial | 30% |
| Stage 8: Pipeline Integration | 📋 Planned | 0% |
| Stage 9: C# Implementation | 📋 Research | 10% |
| Stage 10: Documentation | 🔄 In Progress | 50% |

**Legend**: 
- ✅ Completed
- 🔄 In Progress
- 📋 Planned
- ⚠️ Blocked

## 🎯 Getting Started

### For Contributors

1. **Choose a Stage**: Pick an issue that matches your skills and interests
2. **Read Documentation**: Review [PIPELINE.md](../PIPELINE.md) and [docs/CHILD_ISSUES.md](../docs/CHILD_ISSUES.md)
3. **Set Up Environment**: Follow [docs/INSTALLATION.md](../docs/INSTALLATION.md)
4. **Create a Branch**: Use naming convention `feature/stage-X-description`
5. **Work on Subtasks**: Complete items from the issue checklist
6. **Submit PR**: Reference the issue number in your pull request

### For Project Managers

1. **Create Child Issues**: Use templates to create issues for each stage
2. **Set Milestones**: Group related stages into milestones
3. **Track Progress**: Use GitHub Projects for Kanban view
4. **Update Status**: Keep the status table in this file up to date

## 🔗 Related Documentation

- **[PIPELINE.md](../PIPELINE.md)** - Detailed technical breakdown
- **[docs/CHILD_ISSUES.md](../docs/CHILD_ISSUES.md)** - Full issue templates with extensive details
- **[README.md](../README.md)** - Project overview
- **[docs/INSTALLATION.md](../docs/INSTALLATION.md)** - Setup instructions

## 📝 Template Structure

Each issue template follows this structure:

```yaml
---
name: "Stage X: Component Name"
about: Brief description
title: "[Pipeline] Issue Title"
labels: ["label1", "label2", "stage-X"]
assignees: []
---

## 📋 Component Information
- Component name
- Stage number
- Priority
- Estimated effort

## 🎯 Overview
High-level description

## 📊 Current State
What exists now

## ✅ Requirements
Must/Should/Nice to have

## 📝 Subtasks
Detailed work items

## 🧪 Testing
How to validate

## 📁 Files to Create/Modify
What files are affected

## ✨ Success Criteria
Definition of done

## 🔗 Dependencies
Related issues

## 📚 References
External links
```

## 🤝 Contributing

To improve the issue tracking system:

1. Discuss in [Discussions](https://github.com/Nomoos/StoryGenerator/discussions)
2. Submit a PR to update templates
3. Keep templates in sync with [docs/CHILD_ISSUES.md](../docs/CHILD_ISSUES.md)

## 📧 Questions?

If you have questions about the issue tracking system:
- Check [docs/FAQ.md](../docs/FAQ.md)
- Search existing issues
- Start a [Discussion](https://github.com/Nomoos/StoryGenerator/discussions)
- Contact maintainers

---

**Last Updated**: 2024-01-XX  
**Maintained By**: StoryGenerator Team
