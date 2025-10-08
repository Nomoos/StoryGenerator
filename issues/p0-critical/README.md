# P0 - Critical Priority Issues

**Priority Level:** P0 (Critical)  
**Status:** Active Development  
**Focus:** Immediate implementation required

## Overview

This folder contains critical priority issues that must be completed immediately. These tasks are blockers for other work and represent the highest priority items for the project.

## Current Issues

### Security Issues (URGENT)

#### security-api-keys
**Status:** 🔴 NOT STARTED ⚠️ CRITICAL  
**Effort:** 2-4 hours  
**Description:** Remove exposed API keys from source code. Multiple API keys are hardcoded directly in source files, creating a critical security vulnerability.

**Must Complete:**
- [ ] Revoke ALL exposed API keys immediately
- [ ] Implement environment variable management
- [ ] Update all code to read from environment variables

[View Issue →](security-api-keys/issue.md)

#### security-file-paths
**Status:** 🔴 NOT STARTED  
**Effort:** 3-5 hours  
**Description:** Fix hard-coded Windows-specific file paths. Current paths prevent cross-platform development and team collaboration.

**Must Complete:**
- [ ] Remove all hardcoded absolute paths
- [ ] Implement platform-independent path handling
- [ ] Support Windows, macOS, and Linux

[View Issue →](security-file-paths/issue.md)

### C# Implementation

#### csharp-phase3-complete-generators
**Status:** ✅ COMPLETE (Generators Implemented)  
**Effort:** 16-24 hours  
**Description:** Complete the remaining generators in the C# implementation to achieve full feature parity with the obsolete Python implementation.

**Completed:**
- ✅ All 6 primary text-to-audio generators implemented
- ✅ Clean build with 0 errors
- ✅ All tests passing
- ✅ Documentation updated

### Content Pipeline

#### content-pipeline/
**Status:** ✅ COMPLETE (Reddit Scraper)  
**Priority:** P0/P1 (Critical Path)  
**Description:** Core content sourcing and quality control pipeline

**Key Tasks:**
- **02-content-01-reddit-scraper** ✅ (P0 Critical Path) - Reddit story scraping COMPLETE
- **02-content-02-alt-sources** (P1) - Alternative content sources
- **02-content-03-quality-scorer** (P1) - Content quality assessment
- **02-content-04-deduplication** (P1) - Duplicate content detection
- **02-content-05-ranking** (P1) - Content ranking system
- **02-content-06-attribution** (P1) - Source attribution tracking

## Best Practices

### Test-Driven Development (TDD)
1. **Write tests first** - Define expected behavior before implementation
2. **Red-Green-Refactor** - Write failing test → Make it pass → Improve code
3. **Unit test coverage** - Target >80% coverage for critical components
4. **Integration tests** - Verify component interactions
5. **Continuous testing** - Run tests on every code change

### Development Workflow
1. Review acceptance criteria thoroughly
2. Write comprehensive unit tests
3. Implement minimal code to pass tests
4. Refactor and optimize
5. Document API and usage
6. Peer review before merging

### Code Quality Standards
- Follow SOLID principles
- Use dependency injection
- Implement proper error handling
- Add XML documentation comments
- Follow C# coding conventions
- Use async/await patterns appropriately

## Dependencies

**Completed:**
- ✅ Phase 1: Interface (All tasks complete)
- ✅ Phase 2: Prototype (All tasks complete)

**Blocks:**
- Phase 4: Pipeline Orchestration
- Video generation workflows
- Full end-to-end pipeline

## Getting Started

1. Review the issue details in each subdirectory
2. Check dependencies and prerequisites
3. Write tests for acceptance criteria
4. Implement following TDD practices
5. Document as you code
6. Submit for peer review

---

**Total P0 Issues:** 4 major tasks  
**Estimated Effort:** 25-40 hours  
**Status:** 🔴 2 URGENT SECURITY ISSUES + 2 COMPLETE  

### Issue Breakdown:
1. 🔴 **Security: API Keys** - NOT STARTED ⚠️ CRITICAL URGENCY
2. 🔴 **Security: File Paths** - NOT STARTED
3. ✅ **C# Phase 3 Generators** - COMPLETE
4. ✅ **Reddit Story Scraper** - COMPLETE

**Next Priority:** Complete security issues immediately, then move to P1-High issues

## P0 Status Summary

### Completed Issues (2/4)
1. ✅ **C# Phase 3 Generators** - All 6 text-to-audio generators implemented and verified
2. ✅ **Reddit Story Scraper** - Complete with documentation and testing

### Outstanding Security Issues (2/4) ⚠️
1. 🔴 **API Key Security** - IMMEDIATE ACTION REQUIRED
   - API keys exposed in source code
   - Must revoke and move to environment variables
   - Blocks production deployment

2. 🔴 **File Path Portability** - HIGH PRIORITY
   - Windows-specific hardcoded paths
   - Prevents cross-platform development
   - Blocks team collaboration

See [P0_COMPLETION_SUMMARY.md](./P0_COMPLETION_SUMMARY.md) for detailed completion report.
