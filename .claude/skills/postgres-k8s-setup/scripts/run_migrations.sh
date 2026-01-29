#!/bin/bash

# PostgreSQL Migration Script
# Applies schema migrations for LearnFlow application

set -e  # Exit on any error

echo "Running PostgreSQL migrations for LearnFlow..."

# Wait for PostgreSQL to be fully ready
sleep 15

# Define migration SQL
MIGRATION_SQL=$(cat << 'SQL'
-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create courses/modules table
CREATE TABLE IF NOT EXISTS modules (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    module_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create lessons table
CREATE TABLE IF NOT EXISTS lessons (
    id SERIAL PRIMARY KEY,
    module_id INTEGER REFERENCES modules(id),
    title VARCHAR(255) NOT NULL,
    content TEXT,
    lesson_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create exercises table
CREATE TABLE IF NOT EXISTS exercises (
    id SERIAL PRIMARY KEY,
    lesson_id INTEGER REFERENCES lessons(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    starter_code TEXT,
    solution_code TEXT,
    difficulty VARCHAR(20) DEFAULT 'easy',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create user progress table
CREATE TABLE IF NOT EXISTS user_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    lesson_id INTEGER REFERENCES lessons(id),
    exercise_id INTEGER REFERENCES exercises(id),
    status VARCHAR(20) DEFAULT 'not_started', -- not_started, in_progress, completed
    score DECIMAL(5,2),
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create submissions table
CREATE TABLE IF NOT EXISTS submissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    exercise_id INTEGER REFERENCES exercises(id),
    code TEXT NOT NULL,
    result TEXT,
    passed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create ai_interactions table
CREATE TABLE IF NOT EXISTS ai_interactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    interaction_type VARCHAR(50),
    query TEXT,
    response TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_user_progress_user_id ON user_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_lesson_id ON user_progress(lesson_id);
CREATE INDEX IF NOT EXISTS idx_submissions_user_id ON submissions(user_id);
CREATE INDEX IF NOT EXISTS idx_submissions_exercise_id ON submissions(exercise_id);
CREATE INDEX IF NOT EXISTS idx_ai_interactions_user_id ON ai_interactions(user_id);

-- Insert default modules for LearnFlow curriculum
INSERT INTO modules (name, description, module_order) VALUES
('Python Basics', 'Introduction to Python programming', 1),
('Control Flow', 'Conditionals and loops', 2),
('Data Structures', 'Lists, tuples, dictionaries, sets', 3),
('Functions', 'Defining and using functions', 4),
('Object-Oriented Programming', 'Classes and objects', 5),
('Files and Exceptions', 'File handling and error management', 6),
('Libraries and Modules', 'Using external libraries', 7)
ON CONFLICT DO NOTHING;

COMMIT;
SQL
)

# Execute the migration
kubectl exec -n postgresql svc/postgresql -- bash -c "
PGPASSWORD=\$(kubectl get secret postgresql -n postgresql -o jsonpath='{.data.postgres-password}' | base64 -d)
psql -U postgres -d learnflow_db -c \"BEGIN; $MIGRATION_SQL\"
"

echo "✓ PostgreSQL migrations applied successfully!"
