# Test Suite Overview - Agile TaskIQ

**Version**: 3.0  
**Last Updated**: November 5, 2025  
**Status**: Ready for Integration

---

## Executive Summary

Comprehensive test suite prepared for integration with backend and frontend implementations. All tests are structured to align with PRD requirements and standard testing practices.

### Test Coverage

| Category | Files | Test Count | Status |
|----------|-------|------------|--------|
| Backend Unit Tests | 2 | 74+ | Ready |
| Backend Integration Tests | 1 | 25+ | Ready |
| Backend Database Tests | 1 | 35+ | Ready |
| Frontend Component Tests | 3 | 65+ | Ready |
| **Total** | **7** | **199+** | **Ready** |

### Files Modified/Created

```
backend/tests/
├── test_database.py          (NEW - 35+ tests)
├── test_integration.py       (NEW - 25+ tests)
├── test_tasks.py            (UPDATED - 38+ tests, was 26)
├── test_ai.py               (UPDATED - 36+ tests, was 30)
├── conftest.py              (UPDATED - 6 new fixtures)
└── TEST_SUITE_OVERVIEW.md   (UPDATED - this file)

frontend/src/__tests__/
├── TaskList.test.jsx        (NEW - 20+ tests)
├── TaskForm.test.jsx        (NEW - 25+ tests)
└── Dashboard.test.jsx       (NEW - 20+ tests)
```

---

## Backend Test Suite

### 1. `test_tasks.py` - Task CRUD Operations

**Purpose**: Test all task management endpoints per PRD Section 10.

**Test Classes**:
- `TestTasksCRUD` - Basic CRUD operations (18 tests)
- `TestTasksPriorityScore` - Automatic priority scoring (2 tests)
- `TestTasksPerformance` - 200ms response time validation (2 tests)
- `TestTasksEdgeCases` - Boundary conditions (4 tests)
- `TestTasksSecurity` - SQL injection, XSS, unicode (4 tests)
- `TestTasksUserRelationship` - User-task associations (4 tests)
- `TestTasksStatusTransitions` - Status workflow validation (4 tests)

**Key Features**:
- Exact status code assertions (no permissive ranges)
- Performance testing for NFR compliance
- Security vulnerability testing
- Unicode and special character handling
- All CRUD operations with error scenarios

**PRD Alignment**:
- Section 5: Functional Requirements
- Section 6: Non-Functional Requirements (200ms)
- Section 10: API Design
- Section 11: Database Schema validation

---

### 2. `test_ai.py` - AI Endpoints

**Purpose**: Test priority ranking and t-shirt size recommendation endpoints.

**Test Classes**:
- `TestAIRankEndpoint` - Priority scoring algorithm (18 tests)
- `TestAISizeEndpoint` - T-shirt size recommendations (16 tests)
- `TestAIEndpointsPerformance` - Performance validation (2 tests)

**Key Features**:
- **Algorithm Validation**: Tests verify PRD formula `Score = 100 - days*5 - duration*3`
- **Clamping Tests**: Ensures scores stay within 1-100 range
- **Edge Cases**: Negative values, zero values, extreme values
- **Consistency**: Deterministic algorithm verification
- **Version Tracking**: Algorithm version metadata

**PRD Alignment**:
- Section 5: User Stories (AI capabilities)
- Section 6: NFR (200ms response time)
- Section 10: API Design (/ai/rank, /ai/size)

**Algorithm Test Coverage**:
```python
# Formula validation
test_rank_algorithm_formula_validation()

# Boundary testing
test_rank_algorithm_clamping_lower_bound()
test_rank_algorithm_clamping_upper_bound()

# Edge cases
test_rank_past_deadline()
test_rank_negative_duration()
test_rank_zero_duration()
```

---

### 3. `test_integration.py` - Full Lifecycle Tests

**Purpose**: Test complete workflows and cross-feature integration per PRD Section 14.

**Test Classes**:
- `TestTaskLifecycle` - Complete CRUD workflows (3 tests)
- `TestTaskDependencies` - Dependency management (5 tests)
- `TestUserWorkflows` - Multi-user scenarios (2 tests)
- `TestPriorityScoreIntegration` - Score generation and updates (4 tests)
- `TestTShirtSizeIntegration` - Size estimation workflows (2 tests)
- `TestPerformanceIntegration` - End-to-end performance (2 tests)
- `TestErrorHandlingIntegration` - Rollback and error recovery (3 tests)

**Key Features**:
- Complete task lifecycle: create → update → complete → delete
- Task dependency chains and circular dependency prevention
- User isolation and cascade delete testing
- Priority score auto-generation and recalculation
- Bulk operations performance testing
- Transaction rollback validation

**PRD Alignment**:
- Section 11: All 5 database tables
- Section 14: Integration test requirements
- User authentication workflows
- Task dependencies validation

---

### 4. `test_database.py` - Database Constraints

**Purpose**: Validate database integrity per PRD Section 11 and Section 14.

**Test Classes**:
- `TestDatabaseSchema` - Table existence validation (5 tests)
- `TestForeignKeyConstraints` - Referential integrity (4 tests)
- `TestCascadeDelete` - Cascade behavior (6 tests)
- `TestUniqueConstraints` - Uniqueness enforcement (4 tests)
- `TestCheckConstraints` - Value validation (3 tests)
- `TestTimestampGeneration` - Auto-timestamp fields (5 tests)
- `TestReferentialIntegrity` - Cross-table relationships (4 tests)

**Key Features**:
- All 5 tables validated: users, tasks, task_dependencies, task_priority_scores, task_tshirt_scores
- Foreign key constraint enforcement
- CASCADE DELETE verification across all relationships
- UNIQUE constraint testing (email, task_id in scores)
- CHECK constraint validation (status, priority range, t-shirt sizes)
- Timestamp auto-generation verification

**PRD Alignment**:
- Section 11: Complete database schema
- Section 14: Database test requirements
- All table relationships validated
- All constraints tested

**Schema Coverage**:
```
users ──┐
        ├──> tasks ──┬──> task_dependencies
        │            ├──> task_priority_scores
        │            └──> task_tshirt_scores
        └──> (CASCADE DELETE tested for all)
```

---

### 5. `conftest.py` - Test Fixtures

**Purpose**: Provide reusable test data and database setup.

**Database Fixtures**:
- `test_db` - In-memory SQLite (fast, isolated, for unit tests)
- `integration_db` - File-based SQLite (realistic data, for integration tests)

**How Database Setup Works**:
1. **Unit Tests**: Use `test_db` - creates fresh in-memory database for each test
2. **Integration Tests**: Use `integration_db` - auto-generates `test.db` if missing
3. **No manual setup required** - fixtures handle everything automatically

**Data Fixtures**:
- `sample_user` - Single test user
- `sample_tasks` - 3 tasks with varying statuses
- `task_data` - Template for POST requests
- `ai_rank_data` - Sample ranking request
- `ai_size_data` - Sample size request

**Integration Fixtures**:
- `multiple_users` - 3 users for multi-user testing
- `tasks_with_dependencies` - 4 tasks with dependency chain
- `tasks_with_scores` - Tasks with priority and t-shirt scores
- `overdue_tasks` - Tasks with past deadlines
- `mixed_status_tasks` - All status values represented
- `large_task_dataset` - 50 tasks for performance testing

**Schema Consistency**:
- All fixtures use schema from `backend/schema.sql`
- All CHECK constraints enforced
- Referential integrity maintained

**Note**: test.db is automatically generated by the `integration_db` fixture on first use. No manual setup required.

---

## Frontend Test Suite

### 6. `TaskList.test.jsx` - Task List Component

**Purpose**: Test task list display and interactions per PRD Section 14.

**Test Coverage** (20+ tests):
- Task list rendering with all fields
- Empty state display
- Priority score visualization
- Status badge rendering (pending, in_progress, completed, blocked)
- Loading and error states
- Task filtering by status
- Task sorting by priority
- Delete functionality
- API integration
- Real-time refresh

**Key Features**:
- Mock fetch for API isolation
- React Testing Library best practices
- User interaction testing with userEvent
- Async state management validation
- Error boundary testing

**PRD Alignment**:
- Section 12: Component structure
- Section 14: Frontend component tests
- Priority score display requirement

---

### 7. `TaskForm.test.jsx` - Task Form Component

**Purpose**: Test task creation and editing forms.

**Test Coverage** (25+ tests):
- Form field rendering
- Input validation (required fields, formats)
- Form submission (create and update)
- API integration (POST and PUT)
- Success and error feedback
- Field clearing after submission
- Status selection dropdown
- Date picker functionality
- Duration validation (positive, zero, negative)
- Special character handling
- Edit mode vs create mode

**Key Features**:
- Comprehensive validation testing
- API error handling (422, 500, network errors)
- Form state management
- User input simulation
- Accessibility testing

**PRD Alignment**:
- Section 5: User stories (CRUD operations)
- Section 10: API integration
- Section 14: Frontend tests

---

### 8. `Dashboard.test.jsx` - Dashboard Component

**Purpose**: Test priority dashboard and analytics per PRD Section 7.

**Test Coverage** (20+ tests):
- Dashboard rendering
- Task statistics (total, by status)
- Priority distribution (high/medium/low)
- Completion rate calculation
- Overdue task warnings
- Upcoming deadline display
- Average priority score
- Blocked tasks count
- Task distribution charts
- Real-time updates (auto-refresh)
- Filter controls
- Performance metrics

**Key Features**:
- Statistical calculation validation
- Chart rendering verification
- Real-time update simulation with fake timers
- Date range filtering
- Empty state handling

**PRD Alignment**:
- Section 7: PriorityDashboard requirement
- Section 14: Frontend component tests
- Analytics and visualization

---

## Running the Tests

### Backend Tests

```bash
# Navigate to backend directory
cd backend

# Run all tests
pytest -v

# Run specific test file
pytest tests/test_tasks.py -v
pytest tests/test_ai.py -v
pytest tests/test_integration.py -v
pytest tests/test_database.py -v

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test class
pytest tests/test_tasks.py::TestTasksCRUD -v

# Run specific test
pytest tests/test_ai.py::TestAIRankEndpoint::test_rank_algorithm_formula_validation -v

# Run tests matching pattern
pytest -k "priority" -v
pytest -k "security" -v
```

### Frontend Tests

```bash
# Navigate to frontend directory
cd frontend

# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test file
npm test TaskList.test.jsx
npm test TaskForm.test.jsx
npm test Dashboard.test.jsx

# Run in watch mode
npm test -- --watch
```

---

## Test Data and Fixtures

### Sample Task Data
```json
{
  "title": "Submit project report",
  "description": "Send final report to manager",
  "deadline": "2025-11-06",
  "status": "pending",
  "estimated_duration": 4,
  "priority_score": 85
}
```

### Sample AI Rank Request
```json
{
  "tasks": [
    {
      "title": "Urgent Task",
      "deadline": "2025-11-06",
      "estimated_duration": 2
    }
  ]
}
```

### Sample AI Size Request
```json
{
  "height_cm": 175,
  "weight_kg": 70,
  "gender": "male",
  "fit_preference": "regular"
}
```

---

## Integration with Development

### For Backend Developers

**When implementing endpoints**:
1. Tests expect exact status codes (201 for POST, 200 for GET/PUT, 204 for DELETE)
2. Response format must match PRD Section 10 examples
3. All responses must complete within 200ms (NFR requirement)
4. Priority score algorithm must follow: `100 - days*5 - duration*3` (clamped 1-100)

**Database implementation**:
1. Use schema from `backend/schema.sql` or `conftest.py`
2. Ensure CASCADE DELETE is configured for all foreign keys
3. CHECK constraints must be enforced (status, score range, t-shirt sizes)
4. Timestamps must auto-generate (DEFAULT CURRENT_TIMESTAMP)

**API Endpoints Expected**:
```
GET    /tasks              - List all tasks
POST   /tasks              - Create task (returns 201)
GET    /tasks/{id}         - Get specific task
PUT    /tasks/{id}         - Update task (returns 200)
DELETE /tasks/{id}         - Delete task (returns 204)

POST   /ai/rank            - Rank tasks by priority
POST   /ai/size            - T-shirt size recommendation

GET    /users/{id}/tasks   - Get user's tasks
POST   /tasks/dependencies - Create task dependency
GET    /tasks/{id}/dependencies - Get task dependencies
```

### For Frontend Developers

**Component Requirements**:
1. Components must handle loading, error, and empty states
2. API calls should use environment variable `REACT_APP_BACK_END_URL`
3. Status values: `pending`, `in_progress`, `completed`, `blocked`
4. T-shirt sizes: `XS`, `S`, `M`, `L`, `XL`

**Expected Props**:
```javascript
// TaskList
<TaskList />

// TaskForm
<TaskForm />  // Create mode
<TaskForm task={existingTask} mode="edit" />  // Edit mode

// Dashboard
<Dashboard />
```

---

## Test Maintenance

### Adding New Tests

1. **Backend**: Add to appropriate test class in existing files
2. **Frontend**: Follow existing test structure with describe/test blocks
3. **Fixtures**: Add to `conftest.py` for reusable test data
4. **Integration**: Add to `test_integration.py` for cross-feature tests

### Test Naming Convention

```python
# Backend
def test_<action>_<scenario>_<expected_result>():
    """Test description."""

# Frontend
test('action scenario expected result', async () => {
  // Test implementation
});
```

### Coverage Goals

- Overall: > 80%
- Critical paths (CRUD, AI): > 95%
- Database constraints: 100%
- Error handling: > 90%

---

## Known Limitations

1. **API Not Implemented**: Tests will fail until endpoints are built
2. **Frontend Components Missing**: Component tests require implementation
3. **Authentication**: User auth tests are placeholders (auth not in MVP)
4. **Rate Limiting**: Not tested (not in MVP scope)

---

## Next Steps

### For Developers Implementing Features

1. Tests are ready and waiting
2. Implement endpoints matching test expectations
3. Run tests to validate implementation
4. Fix any failing tests or adjust tests if requirements changed
5. Add additional tests for new features

### Test Execution Checklist

- [ ] All backend unit tests pass
- [ ] All backend integration tests pass
- [ ] All database constraint tests pass
- [ ] All frontend component tests pass
- [ ] Performance tests meet 200ms requirement
- [ ] Coverage reports generated
- [ ] Security tests pass (SQL injection, XSS)

---

## Running Tests

### Backend Tests

```bash
# Navigate to backend directory
cd backend

# Run all tests
pytest -v

# Run specific test file
pytest tests/test_tasks.py -v       # CRUD operations
pytest tests/test_ai.py -v          # AI endpoints
pytest tests/test_integration.py -v # Full workflows
pytest tests/test_database.py -v    # Database constraints

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test class
pytest tests/test_tasks.py::TestTasksCRUD -v

# Run specific test
pytest tests/test_ai.py::TestAIRankEndpoint::test_rank_algorithm_formula_validation -v

# Run tests matching pattern
pytest -k "priority" -v
pytest -k "security" -v
```

### Frontend Tests

```bash
# Navigate to frontend directory
cd frontend

# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test file
npm test TaskList.test.jsx
npm test TaskForm.test.jsx
npm test Dashboard.test.jsx

# Run in watch mode
npm test -- --watch
```

---

## Expected API Behavior

### Status Codes
```
POST   /tasks          → 201 Created
GET    /tasks          → 200 OK
GET    /tasks/{id}     → 200 OK (or 404 Not Found)
PUT    /tasks/{id}     → 200 OK (or 404 Not Found)
DELETE /tasks/{id}     → 204 No Content (or 404 Not Found)
POST   /ai/rank        → 200 OK
POST   /ai/size        → 200 OK

Validation errors   → 422 Unprocessable Entity
Invalid ID format   → 422 Unprocessable Entity
```

### Performance Requirements
- All responses must complete within **200ms** (NFR requirement)
- Tests will fail if this is exceeded

### Priority Algorithm
```python
score = 100 - (days_until_deadline * 5) - (estimated_duration * 3)
score = max(1, min(100, score))  # Clamp between 1-100
```

---

## Valid Values

### Task Status
```python
['pending', 'in_progress', 'completed', 'blocked']
```

### T-shirt Sizes
```python
['XS', 'S', 'M', 'L', 'XL']
```

### Priority Score Range
```python
1 <= score <= 100  # Enforced by CHECK constraint
```

---

## Database Schema Quick Reference

```sql
users
├── id (PK)
├── name (NOT NULL)
├── email (UNIQUE, NOT NULL)
├── password_hash
└── created_at (AUTO)

tasks
├── id (PK)
├── user_id (FK → users.id, CASCADE DELETE)
├── title (NOT NULL)
├── description
├── deadline
├── estimated_duration
├── status (CHECK: pending|in_progress|completed|blocked)
├── created_at (AUTO)
└── updated_at (AUTO)

task_dependencies
├── id (PK)
├── task_id (FK → tasks.id, CASCADE DELETE)
├── depends_on_task_id (FK → tasks.id, CASCADE DELETE)
└── UNIQUE(task_id, depends_on_task_id)

task_priority_scores
├── id (PK)
├── task_id (FK → tasks.id, CASCADE DELETE, UNIQUE)
├── score (CHECK: 1-100)
├── algorithm_version
└── generated_at (AUTO)

task_tshirt_scores
├── id (PK)
├── task_id (FK → tasks.id, CASCADE DELETE, UNIQUE)
├── tshirt_size (CHECK: XS|S|M|L|XL)
├── rationale
├── algorithm_version
└── generated_at (AUTO)
```

---

## Common Test Patterns

### Backend Test Example
```python
def test_create_task_success(self, client, task_data):
    """Test POST /tasks creates a new task successfully."""
    response = client.post("/tasks", json=task_data)
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == task_data["title"]
```

### Frontend Test Example
```javascript
test('renders task list with tasks', async () => {
  const mockTasks = [/* ... */];
  
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => mockTasks
  });

  render(<TaskList />);

  await waitFor(() => {
    expect(screen.getByText('Task Title')).toBeInTheDocument();
  });
});
```

---

## Test Fixtures Available

### Backend (`conftest.py`)
```python
# Core fixtures
test_db              # Fresh in-memory database
client               # FastAPI test client
sample_user          # Single test user
sample_tasks         # 3 tasks with varying statuses
task_data            # Template for POST requests
ai_rank_data         # Sample ranking request
ai_size_data         # Sample size request

# Integration fixtures
multiple_users           # 3 users
tasks_with_dependencies  # Task dependency chain
tasks_with_scores        # Tasks with priority/t-shirt scores
overdue_tasks           # Tasks with past deadlines
mixed_status_tasks      # All status values
large_task_dataset      # 50 tasks for performance testing
```

---

## Key Improvements

### 1. Assertion Pattern Fixes

**Before**:
```python
assert response.status_code in [200, 201, 422]  # Too permissive
```

**After**:
```python
assert response.status_code == 201  # Exact expectation
```

### 2. Removed Conditional Test Logic

**Before**:
```python
if isinstance(sample_tasks, list) and len(sample_tasks) > 0:
    task_id = sample_tasks[0]['id']
    # test logic
```

**After**:
```python
task_id = sample_tasks[0]['id']  # Fail fast if fixture broken
# test logic
```

### 3. Added Algorithm Validation

**New Tests**:
```python
def test_rank_algorithm_formula_validation(self, client):
    """Test priority algorithm follows PRD formula: 100 - days*5 - duration*3."""
    # Validates exact formula from PRD Section 10
```

### 4. Security Testing

**New Test Class**:
```python
class TestTasksSecurity:
    def test_sql_injection_in_title(self, client, task_data):
        """Test SQL injection attempts in title field."""
    
    def test_xss_in_description(self, client, task_data):
        """Test XSS attempts in description field."""
    
    def test_unicode_characters_in_task(self, client, task_data):
        """Test tasks with unicode characters."""
```

### 5. Database Constraint Testing

**New Test Coverage**:
- All 5 tables validated
- Foreign key enforcement
- CASCADE DELETE across all relationships
- UNIQUE constraints (email, task_id in scores)
- CHECK constraints (status, priority 1-100, t-shirt sizes)
- Timestamp auto-generation

### 6. Integration Test Fixtures

**New Fixtures Enable**:
- Multi-user testing
- Task dependency chains
- Priority and t-shirt score integration
- Overdue task scenarios
- Performance testing with large datasets

---

## PRD Alignment

### Section 5: Functional Requirements
- CRUD operations tested
- Auto-generated priority scores validated
- T-shirt size recommendations tested

### Section 6: Non-Functional Requirements
- 200ms response time validated in performance tests
- Security testing (SQL injection, XSS)
- Scalability tested with large datasets

### Section 10: API Design
- All endpoints tested (GET, POST, PUT, DELETE /tasks)
- /ai/rank endpoint with algorithm validation
- /ai/size endpoint with edge cases
- Request/response formats validated

### Section 11: Database Schema
- All 5 tables tested (users, tasks, task_dependencies, task_priority_scores, task_tshirt_scores)
- Foreign key constraints validated
- CASCADE DELETE tested
- CHECK constraints enforced
- UNIQUE constraints validated

### Section 12: Project Directory
- Backend test structure matches
- Frontend test structure created

### Section 14: Testing Suite
- Backend Unit Tests - Complete
- Frontend Component Tests - Complete
- Integration Tests - Complete
- Database Tests - Complete

---

## Standard Testing Practices Applied

### 1. Test Organization
- Clear class-based organization
- Descriptive test names
- Comprehensive docstrings
- Logical grouping by feature

### 2. Test Independence
- Each test is self-contained
- No shared state between tests
- Fresh database for each test
- Proper fixture cleanup

### 3. Assertion Quality
- Exact status code expectations
- Specific error message validation
- Data structure verification
- No overly permissive assertions

### 4. Coverage
- Happy path testing
- Error scenarios
- Edge cases and boundaries
- Security vulnerabilities
- Performance requirements

### 5. Maintainability
- Reusable fixtures
- Clear test documentation
- Consistent naming conventions
- Easy to extend

---

## Troubleshooting

### Tests Skip with "FastAPI app not available"
**Problem**: Backend endpoints not implemented yet  
**Solution**: Implement endpoints in `backend/main.py` or `backend/app/`

### Frontend tests fail with "Component not found"
**Problem**: Components not created yet  
**Solution**: Create components in `frontend/src/components/`

### Database constraint errors
**Problem**: Schema doesn't match test expectations  
**Solution**: Schema is defined in `backend/schema.sql` and automatically loaded by test fixtures

### Test database missing
**Problem**: integration_db fixture can't find test.db  
**Solution**: Fixture auto-generates test.db on first run. No manual action needed.

### Performance tests fail
**Problem**: Response time > 200ms  
**Solution**: Optimize queries, add indexes, use async operations

---

## Security Testing

### SQL Injection Prevention
Tests verify ORM usage prevents SQL injection:
```python
def test_sql_injection_in_title(self, client, task_data):
    """Test SQL injection attempts in title field."""
    injection_data = task_data.copy()
    injection_data["title"] = "'; DROP TABLE tasks; --"
    response = client.post("/tasks", json=injection_data)
    assert response.status_code in [201, 422]
    # Verify tasks table still exists
    list_response = client.get("/tasks")
    assert list_response.status_code == 200
```

### XSS Prevention
```python
def test_xss_in_description(self, client, task_data):
    """Test XSS attempts in description field."""
    xss_data = task_data.copy()
    xss_data["description"] = "<script>alert('XSS')</script>"
    response = client.post("/tasks", json=xss_data)
    assert response.status_code == 201
    # Data stored as-is, escaping happens on frontend
```

### Input Validation
- Field length limits enforced
- Negative values rejected
- Invalid status values rejected
- Unicode characters supported

---

## Integration Testing Checklist

### Pre-Testing Setup
- [ ] Backend running: http://localhost:8000
- [ ] Frontend running: http://localhost:3000
- [ ] Database initialized
- [ ] Environment variables configured
- [ ] Browser dev tools open

### Health & Connectivity
- [ ] Backend `/status` returns "healthy"
- [ ] Frontend loads without errors
- [ ] API docs accessible: http://localhost:8000/docs
- [ ] No CORS errors in console

### Task Management Flow
- [ ] Create task → appears in list with priority score
- [ ] Update task → UI reflects changes
- [ ] Delete task → removed from list
- [ ] All operations < 200ms

### AI Features Validation
- [ ] Priority scores calculated correctly
- [ ] Urgent tasks score higher (90-100)
- [ ] T-shirt size endpoint returns valid sizes
- [ ] Algorithm formula verified: `100 - days*5 - duration*3`

### Error Handling
- [ ] Empty title → validation error
- [ ] Negative duration → 422 error
- [ ] Non-existent task → 404 handled gracefully
- [ ] Backend down → user-friendly error

### Performance Testing
- [ ] All requests < 200ms
- [ ] UI remains responsive
- [ ] No memory leaks
- [ ] Large dataset (50+ tasks) performs well

### Cross-Browser Testing
- [ ] Chrome: All features work
- [ ] Firefox: All features work
- [ ] Edge: All features work

### Docker Testing
- [ ] `docker-compose up` starts successfully
- [ ] Both containers running
- [ ] Services accessible
- [ ] All features work in Docker

---

## Writing New Tests

### Test Naming Convention
```python
def test_<action>_<scenario>_<expected_result>(self, client):
    """Clear description of what is being tested."""
```

### Using Fixtures
```python
def test_example(client, sample_user, sample_tasks):
    """
    client: TestClient for API requests
    sample_user: Pre-created user
    sample_tasks: List of tasks
    """
    response = client.get("/tasks")
    assert response.status_code == 200
```

### Performance Testing Pattern
```python
import time

def test_performance(client):
    start = time.time()
    response = client.get("/tasks")
    duration = time.time() - start
    
    assert response.status_code == 200
    assert duration < 0.2  # < 200ms
```

### Error Testing Pattern
```python
def test_not_found(client):
    response = client.get("/tasks/99999")
    assert response.status_code == 404

def test_validation_error(client):
    response = client.post("/tasks", json={"description": "No title"})
    assert response.status_code == 422
```

---

## Coverage Reporting

```bash
# Terminal report
pytest --cov=backend --cov-report=term

# With missing lines
pytest --cov=backend --cov-report=term-missing

# HTML report
pytest --cov=backend --cov-report=html
start htmlcov/index.html  # Windows
open htmlcov/index.html   # macOS

# XML for CI/CD
pytest --cov=backend --cov-report=xml
```

### Coverage Goals
- Overall: > 80%
- Critical paths (CRUD, AI): > 95%
- Database constraints: 100%
- Error handling: > 90%

---

## CI/CD Integration

Tests run automatically via GitHub Actions on every push:

### CI Workflow
- Run all tests
- Check code coverage
- Validate performance requirements
- Generate coverage reports

### Security Workflow
- Bandit (Python security scanner)
- Safety (dependency vulnerability check)
- CodeQL (code analysis)
- Trivy (container scanning)

---

## Quick Checklist

Before committing code, ensure:

- [ ] All tests pass in your area
- [ ] New features have corresponding tests
- [ ] Status codes match expectations
- [ ] Response times < 200ms
- [ ] Database constraints enforced
- [ ] No linter errors
- [ ] Security tests pass
- [ ] Coverage maintained or improved

---

## Contact and Support

**Test Suite Version**: 3.0  
**Last Review**: November 5, 2025  
**PRD Version**: 1.0  

For questions about test expectations or to report issues with test suite, refer to PRD.md Section 14 (Testing Suite).

