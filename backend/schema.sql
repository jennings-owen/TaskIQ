-- Table for storing user information
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing tasks assigned to users
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    deadline TEXT,
    estimated_duration INTEGER,
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'in_progress', 'completed', 'blocked')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Junction table to manage dependencies between tasks (many-to-many relationship)
CREATE TABLE task_dependencies (
    id INTEGER PRIMARY KEY,
    task_id INTEGER NOT NULL,
    depends_on_task_id INTEGER NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (depends_on_task_id) REFERENCES tasks(id) ON DELETE CASCADE,
    UNIQUE(task_id, depends_on_task_id)
);

-- Table to store priority scores for tasks
CREATE TABLE task_priority_scores (
    id INTEGER PRIMARY KEY,
    task_id INTEGER NOT NULL UNIQUE,
    score INTEGER NOT NULL CHECK(score >= 1 AND score <= 100),
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);

-- Table to store T-shirt size estimations for tasks
CREATE TABLE task_tshirt_scores (
    id INTEGER PRIMARY KEY,
    task_id INTEGER NOT NULL UNIQUE,
    tshirt_size TEXT NOT NULL CHECK(tshirt_size IN ('XS', 'S', 'M', 'L', 'XL')),
    rationale TEXT,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);