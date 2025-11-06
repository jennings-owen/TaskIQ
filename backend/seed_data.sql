-- Populate 'users' table
INSERT INTO users (id, name, email, password_hash) VALUES (1, 'Alice Johnson', 'alice.j@agiletaskiq.com', 'sha256$a89e59d19d98146794a2a371f7db8a9d$0fee0043e6f5aad4bfcbb659d763ebd02e2f09a5bc253ed272851d3b428bace4');
INSERT INTO users (id, name, email, password_hash) VALUES (2, 'Bob Williams', 'bob.w@agiletaskiq.com', 'sha256$62aa657e22a07e959790416e2c5b31d7$41f56f8dff8e079a11bb11786083b0e0329f4f96a2ec09f1fdd88693e493a46a');
INSERT INTO users (id, name, email, password_hash) VALUES (3, 'Carol Davis', 'carol.d@consultingfirm.com', 'sha256$2c57f6295cfa79e61cef67e57ba60219$029f077cbfdfd722477524a61e2d3d5fa9773efa93c344e02cd952431cbc7e84');

-- Populate 'tasks' table
INSERT INTO tasks (id, user_id, title, description, deadline, estimated_duration, status) VALUES (1, 2, 'Implement user authentication endpoint', 'Create the /login and /register API endpoints using JWT for user access.', '2024-11-25T17:00:00Z', 8, 'pending');
INSERT INTO tasks (id, user_id, title, description, deadline, estimated_duration, status) VALUES (2, 2, 'Fix bug #582 - Payment processing error', 'Users are reporting a 500 error during checkout. Investigate and patch immediately.', '2024-11-10T23:59:59Z', 3, 'in_progress');
INSERT INTO tasks (id, user_id, title, description, deadline, estimated_duration, status) VALUES (3, 1, 'Draft Q4 Project Plan', 'Outline key milestones, resources, and timeline for the upcoming quarter.', '2024-12-15T18:00:00Z', 16, 'pending');
INSERT INTO tasks (id, user_id, title, description, deadline, estimated_duration, status) VALUES (4, 3, 'Prepare client presentation slides', 'Create a slide deck for the Q4 review meeting with the client, focusing on performance metrics.', '2024-11-20T12:00:00Z', 6, 'pending');
INSERT INTO tasks (id, user_id, title, description, deadline, estimated_duration, status) VALUES (5, 2, 'Deploy staging environment updates', 'Push the latest build, including the new auth features, to the staging server for QA.', '2024-11-28T10:00:00Z', 2, 'pending');
INSERT INTO tasks (id, user_id, title, description, deadline, estimated_duration, status) VALUES (6, 1, 'Review team performance metrics', 'Analyze sprint velocity and burndown charts from the last cycle and prepare a summary report.', '2024-11-01T15:00:00Z', 4, 'completed');

-- Populate 'task_dependencies' table (Task 5 depends on Task 1)
INSERT INTO task_dependencies (task_id, depends_on_task_id) VALUES (5, 1);

-- Populate 'task_priority_scores' table
INSERT INTO task_priority_scores (task_id, score ) VALUES (1, 88);
INSERT INTO task_priority_scores (task_id, score ) VALUES (2, 95);
INSERT INTO task_priority_scores (task_id, score ) VALUES (3, 75);
INSERT INTO task_priority_scores (task_id, score ) VALUES (4, 80);
INSERT INTO task_priority_scores (task_id, score ) VALUES (5, 65);
INSERT INTO task_priority_scores (task_id, score ) VALUES (6, 70);

-- Populate 'task_tshirt_scores' table
INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale ) VALUES (1, 'M', 'Standard feature implementation with some complexity.');
INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale ) VALUES (2, 'S', 'Targeted bug fix with a clear scope.');
INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale ) VALUES (3, 'L', 'Large planning task involving multiple stakeholders.');
INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale ) VALUES (4, 'S', 'Standard presentation preparation with clear requirements.');
INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale ) VALUES (5, 'XS', 'Simple deployment script execution.');
INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale ) VALUES (6, 'M', 'Analysis and reporting task with moderate complexity.');