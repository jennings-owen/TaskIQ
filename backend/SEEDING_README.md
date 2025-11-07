# Database Seeding Scripts

This directory contains scripts to seed the team_synapse database with realistic project tasks for building a full stack web application to query books from a library's online public API.

## Files

- `seed_for_user.sql` - Parameterized SQL script that creates tasks, dependencies, and scores
- `seed_user_tasks.py` - Main Python script with comprehensive options
- `quick_seed.py` - Simple script for quick seeding

## Usage

### Quick Seeding (Recommended)

```bash
# See available users
python quick_seed.py

# Seed tasks for a specific user
python quick_seed.py 1
```

### Advanced Usage

```bash
# List all users in the database
python seed_user_tasks.py --list-users 1

# Seed tasks for user ID 1
python seed_user_tasks.py 1

# Clean existing tasks and seed new ones
python seed_user_tasks.py 1 --clean

# Use custom database path
python seed_user_tasks.py 1 --db-path /path/to/custom.db
```

## What Gets Created

The seeding script creates **27 tasks** organized into these categories:

### 1. Project Planning & Research (3 tasks)
- Research Library APIs
- Design System Architecture
- Create Project Wireframes

### 2. Backend Development (6 tasks)
- Setup Backend Project Structure
- Implement Library API Client
- Create Book Data Models
- Build Search API Endpoints
- Implement Caching Layer
- Add User Favorites Feature

### 3. Frontend Development (6 tasks)
- Setup Frontend Project
- Create Book Search Component
- Build Book Results Display
- Implement Book Details View
- Add User Authentication UI
- Build Favorites Management

### 4. Integration & Testing (4 tasks)
- Write Backend Unit Tests
- Write Frontend Unit Tests
- Implement API Integration
- Perform End-to-End Testing

### 5. Deployment & Optimization (4 tasks)
- Setup Docker Containers
- Configure CI/CD Pipeline
- Optimize Application Performance
- Deploy to Production

### 6. Documentation & Maintenance (2 tasks)
- Write Technical Documentation
- Create User Guide

## Additional Data Created

- **32 task dependencies** ensuring logical task ordering
- **27 priority scores** (50-95 range) based on importance
- **27 T-shirt size estimations** (XS-XL) with detailed rationales
- **Realistic deadlines** spread across 28 days
- **Estimated durations** totaling ~240 hours of work

## Task Dependencies

The script creates realistic dependencies such as:
- Architecture design depends on API research
- Backend setup depends on architecture
- Frontend components depend on wireframes
- Testing depends on implementation
- Deployment depends on testing completion

## Priority Scoring

Tasks are prioritized based on:
- **90-95**: Critical foundation tasks (API research, architecture)
- **80-89**: Core development tasks (search functionality, API endpoints)
- **70-79**: Important features (authentication, testing)
- **60-69**: Secondary features (caching, optimization)
- **50-59**: Documentation and maintenance

## T-shirt Sizing

Realistic effort estimation:
- **XS**: Simple tasks (2-4 hours)
- **S**: Standard tasks (4-8 hours)
- **M**: Moderate complexity (8-16 hours)
- **L**: Complex tasks (16-24 hours)
- **XL**: Very complex tasks (24+ hours)

## Error Handling

The scripts include comprehensive error handling for:
- Missing database files
- Invalid user IDs
- SQL execution errors
- File permission issues

## Prerequisites

- Python 3.6+
- SQLite3 (included with Python)
- Existing database.db with user records

## Notes

- The script uses SQLite transactions for data integrity
- Foreign key constraints are enabled for proper cascading
- All timestamps use ISO format for consistency
- The script can be run multiple times (use --clean to avoid duplicates)