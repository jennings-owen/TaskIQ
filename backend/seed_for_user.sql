-- Seed data generator for creating tasks related to building a full stack web application
-- for querying books from a library's online public API
-- Parameter: user_id (INTEGER) - The ID of the user to create tasks for

-- Note: This file contains a parametized seed script that should be executed 
-- with a specific user_id parameter. Replace :user_id with the actual user ID.

-- =============================================================================
-- FULL STACK LIBRARY BOOK QUERY APPLICATION TASKS
-- =============================================================================

-- 1. PROJECT PLANNING & RESEARCH TASKS
INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status) VALUES 
(:user_id, 'Research Library APIs', 'Research and evaluate available library APIs (OpenLibrary, Google Books API, WorldCat API) for book data retrieval. Document API capabilities, rate limits, and data formats.', datetime('now', '+3 days'), 6, 'pending');

INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status) VALUES 
(:user_id, 'Design System Architecture', 'Create system architecture diagram showing frontend, backend, API integration, and data flow. Define technology stack and component interactions.', datetime('now', '+5 days'), 8, 'pending');

INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status) VALUES 
(:user_id, 'Create Project Wireframes', 'Design wireframes for the book search interface, results display, book details view, and user favorites. Include mobile responsive layouts.', datetime('now', '+7 days'), 12, 'pending');

-- 2. BACKEND DEVELOPMENT TASKS
INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status) VALUES 
(:user_id, 'Setup Backend Project Structure', 'Initialize backend project with proper folder structure, configuration files, and development environment setup. Include linting and testing frameworks.', datetime('now', '+4 days'), 4, 'pending');

INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status) VALUES 
(:user_id, 'Implement Library API Client', 'Create service classes to interact with chosen library APIs. Implement error handling, rate limiting, and response caching mechanisms.', datetime('now', '+10 days'), 16, 'pending');

INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status) VALUES 
(:user_id, 'Create Book Data Models', 'Define data models/schemas for books, authors, publishers, and search results. Include validation and serialization logic.', datetime('now', '+8 days'), 6, 'pending');

INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status) VALUES 
(:user_id, 'Build Search API Endpoints', 'Implement REST endpoints for book search by title, author, ISBN, and genre. Include pagination, filtering, and sorting capabilities.', datetime('now', '+12 days'), 10, 'pending');

INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status) VALUES 
(:user_id, 'Implement Caching Layer', 'Add Redis or in-memory caching for frequently searched books and API responses to improve performance and reduce external API calls.', datetime('now', '+14 days'), 8, 'pending');

INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status) VALUES 
(:user_id, 'Add User Favorites Feature', 'Create endpoints for users to save, retrieve, and manage their favorite books. Include database schema for user preferences.', datetime('now', '+16 days'), 12, 'pending');

-- 3. FRONTEND DEVELOPMENT TASKS
INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status) VALUES 
(:user_id, 'Setup Frontend Project', 'Initialize React/Vue/Angular project with modern tooling, routing, state management, and UI component library. Configure build and development scripts.', datetime('now', '+6 days'), 6, 'pending');

INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status) VALUES 
(:user_id, 'Create Book Search Component', 'Build responsive search interface with autocomplete, filters, and advanced search options. Include search history and suggestions.', datetime('now', '+11 days'), 10, 'pending');

INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status) VALUES 
(:user_id, 'Build Book Results Display', 'Create components to display search results in grid/list views with pagination, sorting options, and book cover images.', datetime('now', '+13 days'), 8, 'pending');

INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status) VALUES 
(:user_id, 'Implement Book Details View', 'Design and build detailed book view showing full information, reviews, related books, and availability status.', datetime('now', '+15 days'), 10, 'pending');

INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status) VALUES 
(:user_id, 'Add User Authentication UI', 'Create login, register, and profile management interfaces. Implement protected routes and authentication state management.', datetime('now', '+17 days'), 12, 'pending');

INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status) VALUES 
(:user_id, 'Build Favorites Management', 'Create user interface for managing favorite books including add/remove functionality, favorites list, and export options.', datetime('now', '+18 days'), 8, 'pending');

-- 4. INTEGRATION & TESTING TASKS
INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status) VALUES 
(:user_id, 'Write Backend Unit Tests', 'Create comprehensive unit tests for API services, data models, and business logic. Aim for 80%+ code coverage.', datetime('now', '+19 days'), 16, 'pending');

INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status) VALUES 
(:user_id, 'Write Frontend Unit Tests', 'Implement unit and integration tests for React components, utilities, and state management. Include snapshot testing.', datetime('now', '+20 days'), 12, 'pending');

INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status) VALUES 
(:user_id, 'Implement API Integration', 'Connect frontend to backend APIs with proper error handling, loading states, and offline capabilities.', datetime('now', '+21 days'), 10, 'pending');

INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status) VALUES 
(:user_id, 'Perform End-to-End Testing', 'Create and execute E2E tests covering complete user journeys from search to book details to favorites management.', datetime('now', '+23 days'), 14, 'pending');

-- 5. DEPLOYMENT & OPTIMIZATION TASKS
INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status) VALUES 
(:user_id, 'Setup Docker Containers', 'Create Docker configurations for both frontend and backend applications with proper environment management and health checks.', datetime('now', '+22 days'), 8, 'pending');

INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status) VALUES 
(:user_id, 'Configure CI/CD Pipeline', 'Setup automated testing, building, and deployment pipeline using GitHub Actions or similar. Include staging and production environments.', datetime('now', '+24 days'), 12, 'pending');

INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status) VALUES 
(:user_id, 'Optimize Application Performance', 'Implement performance optimizations including lazy loading, image optimization, bundle splitting, and API response caching.', datetime('now', '+25 days'), 10, 'pending');

INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status) VALUES 
(:user_id, 'Deploy to Production', 'Deploy the complete application to production environment with monitoring, logging, and backup strategies in place.', datetime('now', '+26 days'), 6, 'pending');

-- 6. DOCUMENTATION & MAINTENANCE
INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status) VALUES 
(:user_id, 'Write Technical Documentation', 'Create comprehensive documentation including API documentation, setup guides, architecture overview, and development workflows.', datetime('now', '+27 days'), 8, 'pending');

INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status) VALUES 
(:user_id, 'Create User Guide', 'Develop user-friendly documentation explaining how to use the application, including screenshots and common use cases.', datetime('now', '+28 days'), 6, 'pending');

-- Get the task IDs for dependency mapping (these will be the last 24 tasks inserted)
-- Note: The following dependencies assume tasks are inserted in sequence

-- =============================================================================
-- TASK DEPENDENCIES
-- =============================================================================

-- Research must come before architecture design
INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Design System Architecture' 
AND t2.title = 'Research Library APIs';

-- Wireframes depend on architecture
INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Create Project Wireframes' 
AND t2.title = 'Design System Architecture';

-- Backend setup depends on architecture
INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Setup Backend Project Structure' 
AND t2.title = 'Design System Architecture';

-- API client depends on research and backend setup
INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Implement Library API Client' 
AND t2.title = 'Research Library APIs';

INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Implement Library API Client' 
AND t2.title = 'Setup Backend Project Structure';

-- Data models depend on backend setup
INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Create Book Data Models' 
AND t2.title = 'Setup Backend Project Structure';

-- Search endpoints depend on API client and data models
INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Build Search API Endpoints' 
AND t2.title = 'Implement Library API Client';

INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Build Search API Endpoints' 
AND t2.title = 'Create Book Data Models';

-- Caching depends on API client
INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Implement Caching Layer' 
AND t2.title = 'Implement Library API Client';

-- Favorites depend on data models and backend setup
INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Add User Favorites Feature' 
AND t2.title = 'Create Book Data Models';

-- Frontend setup depends on wireframes
INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Setup Frontend Project' 
AND t2.title = 'Create Project Wireframes';

-- Search component depends on frontend setup
INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Create Book Search Component' 
AND t2.title = 'Setup Frontend Project';

-- Results display depends on search component
INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Build Book Results Display' 
AND t2.title = 'Create Book Search Component';

-- Details view depends on frontend setup
INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Implement Book Details View' 
AND t2.title = 'Setup Frontend Project';

-- Auth UI depends on frontend setup
INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Add User Authentication UI' 
AND t2.title = 'Setup Frontend Project';

-- Favorites UI depends on auth UI
INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Build Favorites Management' 
AND t2.title = 'Add User Authentication UI';

-- Backend tests depend on all backend components
INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Write Backend Unit Tests' 
AND t2.title = 'Build Search API Endpoints';

-- Frontend tests depend on all frontend components
INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Write Frontend Unit Tests' 
AND t2.title = 'Build Book Results Display';

-- API integration depends on both backend and frontend
INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Implement API Integration' 
AND t2.title = 'Build Search API Endpoints';

INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Implement API Integration' 
AND t2.title = 'Create Book Search Component';

-- E2E testing depends on integration
INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Perform End-to-End Testing' 
AND t2.title = 'Implement API Integration';

-- Docker depends on both projects being set up
INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Setup Docker Containers' 
AND t2.title = 'Setup Backend Project Structure';

INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Setup Docker Containers' 
AND t2.title = 'Setup Frontend Project';

-- CI/CD depends on tests and Docker
INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Configure CI/CD Pipeline' 
AND t2.title = 'Write Backend Unit Tests';

INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Configure CI/CD Pipeline' 
AND t2.title = 'Setup Docker Containers';

-- Performance optimization depends on integration
INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Optimize Application Performance' 
AND t2.title = 'Implement API Integration';

-- Deployment depends on CI/CD and testing
INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Deploy to Production' 
AND t2.title = 'Configure CI/CD Pipeline';

INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Deploy to Production' 
AND t2.title = 'Perform End-to-End Testing';

-- Documentation can start after basic structure is in place
INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Write Technical Documentation' 
AND t2.title = 'Design System Architecture';

-- User guide depends on application being functional
INSERT INTO task_dependencies (task_id, depends_on_task_id) 
SELECT t1.id, t2.id 
FROM tasks t1, tasks t2 
WHERE t1.user_id = :user_id AND t2.user_id = :user_id 
AND t1.title = 'Create User Guide' 
AND t2.title = 'Implement API Integration';

-- =============================================================================
-- TASK PRIORITY SCORES
-- =============================================================================

-- Planning and Research (High Priority - Foundation)
INSERT INTO task_priority_scores (task_id, score) 
SELECT id, 95 FROM tasks 
WHERE user_id = :user_id AND title = 'Research Library APIs';

INSERT INTO task_priority_scores (task_id, score) 
SELECT id, 90 FROM tasks 
WHERE user_id = :user_id AND title = 'Design System Architecture';

INSERT INTO task_priority_scores (task_id, score) 
SELECT id, 80 FROM tasks 
WHERE user_id = :user_id AND title = 'Create Project Wireframes';

-- Backend Core (High Priority)
INSERT INTO task_priority_scores (task_id, score) 
SELECT id, 85 FROM tasks 
WHERE user_id = :user_id AND title = 'Setup Backend Project Structure';

INSERT INTO task_priority_scores (task_id, score) 
SELECT id, 88 FROM tasks 
WHERE user_id = :user_id AND title = 'Implement Library API Client';

INSERT INTO task_priority_scores (task_id, score) 
SELECT id, 82 FROM tasks 
WHERE user_id = :user_id AND title = 'Create Book Data Models';

INSERT INTO task_priority_scores (task_id, score) 
SELECT id, 87 FROM tasks 
WHERE user_id = :user_id AND title = 'Build Search API Endpoints';

INSERT INTO task_priority_scores (task_id, score) 
SELECT id, 70 FROM tasks 
WHERE user_id = :user_id AND title = 'Implement Caching Layer';

INSERT INTO task_priority_scores (task_id, score) 
SELECT id, 65 FROM tasks 
WHERE user_id = :user_id AND title = 'Add User Favorites Feature';

-- Frontend Core (High Priority)
INSERT INTO task_priority_scores (task_id, score) 
SELECT id, 84 FROM tasks 
WHERE user_id = :user_id AND title = 'Setup Frontend Project';

INSERT INTO task_priority_scores (task_id, score) 
SELECT id, 89 FROM tasks 
WHERE user_id = :user_id AND title = 'Create Book Search Component';

INSERT INTO task_priority_scores (task_id, score) 
SELECT id, 86 FROM tasks 
WHERE user_id = :user_id AND title = 'Build Book Results Display';

INSERT INTO task_priority_scores (task_id, score) 
SELECT id, 78 FROM tasks 
WHERE user_id = :user_id AND title = 'Implement Book Details View';

INSERT INTO task_priority_scores (task_id, score) 
SELECT id, 72 FROM tasks 
WHERE user_id = :user_id AND title = 'Add User Authentication UI';

INSERT INTO task_priority_scores (task_id, score) 
SELECT id, 60 FROM tasks 
WHERE user_id = :user_id AND title = 'Build Favorites Management';

-- Testing (Medium-High Priority)
INSERT INTO task_priority_scores (task_id, score) 
SELECT id, 75 FROM tasks 
WHERE user_id = :user_id AND title = 'Write Backend Unit Tests';

INSERT INTO task_priority_scores (task_id, score) 
SELECT id, 73 FROM tasks 
WHERE user_id = :user_id AND title = 'Write Frontend Unit Tests';

INSERT INTO task_priority_scores (task_id, score) 
SELECT id, 83 FROM tasks 
WHERE user_id = :user_id AND title = 'Implement API Integration';

INSERT INTO task_priority_scores (task_id, score) 
SELECT id, 77 FROM tasks 
WHERE user_id = :user_id AND title = 'Perform End-to-End Testing';

-- Deployment (Medium Priority)
INSERT INTO task_priority_scores (task_id, score) 
SELECT id, 68 FROM tasks 
WHERE user_id = :user_id AND title = 'Setup Docker Containers';

INSERT INTO task_priority_scores (task_id, score) 
SELECT id, 71 FROM tasks 
WHERE user_id = :user_id AND title = 'Configure CI/CD Pipeline';

INSERT INTO task_priority_scores (task_id, score) 
SELECT id, 65 FROM tasks 
WHERE user_id = :user_id AND title = 'Optimize Application Performance';

INSERT INTO task_priority_scores (task_id, score) 
SELECT id, 79 FROM tasks 
WHERE user_id = :user_id AND title = 'Deploy to Production';

-- Documentation (Lower Priority)
INSERT INTO task_priority_scores (task_id, score) 
SELECT id, 55 FROM tasks 
WHERE user_id = :user_id AND title = 'Write Technical Documentation';

INSERT INTO task_priority_scores (task_id, score) 
SELECT id, 50 FROM tasks 
WHERE user_id = :user_id AND title = 'Create User Guide';

-- =============================================================================
-- TASK T-SHIRT SCORES
-- =============================================================================

-- Research and Planning
INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) 
SELECT id, 'M', 'Requires thorough research of multiple APIs and comparison of features, documentation quality, and limitations.' 
FROM tasks WHERE user_id = :user_id AND title = 'Research Library APIs';

INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) 
SELECT id, 'L', 'Complex architectural decisions involving frontend, backend, database, caching, and external API integration patterns.' 
FROM tasks WHERE user_id = :user_id AND title = 'Design System Architecture';

INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) 
SELECT id, 'L', 'Comprehensive UI/UX design for multiple screens with responsive layouts and user experience considerations.' 
FROM tasks WHERE user_id = :user_id AND title = 'Create Project Wireframes';

-- Backend Development
INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) 
SELECT id, 'S', 'Standard project initialization with familiar tools and frameworks.' 
FROM tasks WHERE user_id = :user_id AND title = 'Setup Backend Project Structure';

INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) 
SELECT id, 'XL', 'Complex integration with external APIs requiring error handling, rate limiting, retries, and data transformation.' 
FROM tasks WHERE user_id = :user_id AND title = 'Implement Library API Client';

INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) 
SELECT id, 'M', 'Standard data modeling with validation, serialization, and relationship mapping.' 
FROM tasks WHERE user_id = :user_id AND title = 'Create Book Data Models';

INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) 
SELECT id, 'L', 'Multiple endpoints with search functionality, pagination, filtering, and query optimization.' 
FROM tasks WHERE user_id = :user_id AND title = 'Build Search API Endpoints';

INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) 
SELECT id, 'M', 'Implementation of caching strategy with TTL management and cache invalidation logic.' 
FROM tasks WHERE user_id = :user_id AND title = 'Implement Caching Layer';

INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) 
SELECT id, 'L', 'User management system with authentication, database schema, and CRUD operations for favorites.' 
FROM tasks WHERE user_id = :user_id AND title = 'Add User Favorites Feature';

-- Frontend Development
INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) 
SELECT id, 'M', 'Modern frontend project setup with build tools, routing, and state management configuration.' 
FROM tasks WHERE user_id = :user_id AND title = 'Setup Frontend Project';

INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) 
SELECT id, 'L', 'Complex search interface with autocomplete, filters, validation, and user experience enhancements.' 
FROM tasks WHERE user_id = :user_id AND title = 'Create Book Search Component';

INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) 
SELECT id, 'M', 'Results display with multiple view modes, sorting, pagination, and responsive design.' 
FROM tasks WHERE user_id = :user_id AND title = 'Build Book Results Display';

INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) 
SELECT id, 'L', 'Detailed view with rich information display, related content, and interactive elements.' 
FROM tasks WHERE user_id = :user_id AND title = 'Implement Book Details View';

INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) 
SELECT id, 'L', 'Complete authentication flow with forms, validation, routing guards, and state management.' 
FROM tasks WHERE user_id = :user_id AND title = 'Add User Authentication UI';

INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) 
SELECT id, 'M', 'User interface for managing favorites with add/remove functionality and list management.' 
FROM tasks WHERE user_id = :user_id AND title = 'Build Favorites Management';

-- Testing and Integration
INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) 
SELECT id, 'XL', 'Comprehensive backend testing including unit tests, mocks for external APIs, and edge cases.' 
FROM tasks WHERE user_id = :user_id AND title = 'Write Backend Unit Tests';

INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) 
SELECT id, 'L', 'Frontend component testing with React Testing Library, mocking, and user interaction tests.' 
FROM tasks WHERE user_id = :user_id AND title = 'Write Frontend Unit Tests';

INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) 
SELECT id, 'L', 'Integration of frontend and backend with error handling, loading states, and data flow.' 
FROM tasks WHERE user_id = :user_id AND title = 'Implement API Integration';

INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) 
SELECT id, 'XL', 'End-to-end testing setup with test automation framework and comprehensive user journey testing.' 
FROM tasks WHERE user_id = :user_id AND title = 'Perform End-to-End Testing';

-- Deployment and Infrastructure
INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) 
SELECT id, 'M', 'Docker containerization with multi-stage builds, environment configuration, and health checks.' 
FROM tasks WHERE user_id = :user_id AND title = 'Setup Docker Containers';

INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) 
SELECT id, 'L', 'CI/CD pipeline setup with automated testing, building, and deployment across environments.' 
FROM tasks WHERE user_id = :user_id AND title = 'Configure CI/CD Pipeline';

INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) 
SELECT id, 'L', 'Performance optimization including bundle analysis, lazy loading, caching strategies, and monitoring.' 
FROM tasks WHERE user_id = :user_id AND title = 'Optimize Application Performance';

INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) 
SELECT id, 'M', 'Production deployment with environment configuration, monitoring setup, and rollback procedures.' 
FROM tasks WHERE user_id = :user_id AND title = 'Deploy to Production';

-- Documentation
INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) 
SELECT id, 'M', 'Technical documentation including API docs, architecture diagrams, and development guidelines.' 
FROM tasks WHERE user_id = :user_id AND title = 'Write Technical Documentation';

INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) 
SELECT id, 'S', 'User-facing documentation with screenshots, tutorials, and frequently asked questions.' 
FROM tasks WHERE user_id = :user_id AND title = 'Create User Guide';
