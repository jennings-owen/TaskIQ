# Test Suite for Agile TaskIQ

**Version**: 3.0 | **Updated**: November 5, 2025

## Overview

Comprehensive test suite with 199+ tests covering backend, frontend, integration, and database constraints. All tests align with PRD requirements and standard testing practices.

## Test Coverage

| Category | Files | Test Count |
|----------|-------|------------|
| Backend Unit Tests | 2 | 74+ |
| Backend Integration Tests | 1 | 25+ |
| Backend Database Tests | 1 | 35+ |
| Frontend Component Tests | 3 | 65+ |
| **Total** | **7** | **199+** |

## Quick Start

### Backend Tests
```bash
cd backend
pytest -v                          # Run all tests
pytest --cov=. --cov-report=html  # With coverage
pytest tests/test_tasks.py -v     # CRUD operations
pytest tests/test_ai.py -v        # AI endpoints
pytest tests/test_integration.py -v  # Full workflows
pytest tests/test_database.py -v  # Database constraints
```

### Frontend Tests
```bash
cd frontend
npm test                          # Run all tests
npm test -- --coverage            # With coverage
npm test TaskList.test.jsx        # Specific component
```

## Test Files

```
backend/tests/
├── test_tasks.py          # 38+ CRUD operation tests
├── test_ai.py             # 36+ AI endpoint tests
├── test_integration.py    # 25+ full workflow tests
├── test_database.py       # 35+ database constraint tests
├── conftest.py            # Test fixtures and setup
└── TEST_SUITE_OVERVIEW.md # Complete documentation

frontend/src/__tests__/
├── TaskList.test.jsx      # 20+ task list tests
├── TaskForm.test.jsx      # 25+ task form tests
└── Dashboard.test.jsx     # 20+ dashboard tests
```

## Complete Documentation

For comprehensive test suite documentation including:
- Detailed test descriptions
- Running instructions
- API behavior expectations
- Database schema reference
- Test patterns and examples
- Troubleshooting guide
- PRD alignment checklist

**See**: [`TEST_SUITE_OVERVIEW.md`](./TEST_SUITE_OVERVIEW.md)

---

**Test Suite Version**: 3.0  
**Status**: Ready for Integration  
**Maintained By**: Integration & Testing Team
