#!/bin/bash
# Apply LearnFlow database schema to PostgreSQL

set -e  # Exit on any error

echo "🔍 Checking if PostgreSQL is ready..."

# Wait for PostgreSQL to be ready
MAX_ATTEMPTS=30
ATTEMPT=0
until kubectl get pods -n postgresql -l app.kubernetes.io/name=postgresql | grep Running > /dev/null 2>&1 || [ $ATTEMPT -ge $MAX_ATTEMPTS ]; do
    echo "⏳ Waiting for PostgreSQL pod to be running... (${ATTEMPT}/${MAX_ATTEMPTS})"
    sleep 10
    ATTEMPT=$((ATTEMPT+1))
done

if [ $ATTEMPT -ge $MAX_ATTEMPTS ]; then
    echo "❌ Timed out waiting for PostgreSQL to be ready"
    exit 1
fi

echo "✅ PostgreSQL is running, applying schema..."

# Create the schema SQL
cat > /tmp/learnflow_schema.sql << 'EOF'
-- LearnFlow Database Schema

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'student', -- 'student', 'teacher', 'admin'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Modules table (curriculum modules)
CREATE TABLE IF NOT EXISTS modules (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    module_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Lessons table (individual lessons within modules)
CREATE TABLE IF NOT EXISTS lessons (
    id SERIAL PRIMARY KEY,
    module_id INTEGER REFERENCES modules(id),
    title VARCHAR(100) NOT NULL,
    content TEXT,
    lesson_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Exercises table (coding exercises)
CREATE TABLE IF NOT EXISTS exercises (
    id SERIAL PRIMARY KEY,
    lesson_id INTEGER REFERENCES lessons(id),
    title VARCHAR(100) NOT NULL,
    description TEXT,
    starter_code TEXT,
    solution_code TEXT,
    difficulty VARCHAR(20), -- 'beginner', 'intermediate', 'advanced'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User progress table
CREATE TABLE IF NOT EXISTS user_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    lesson_id INTEGER REFERENCES lessons(id),
    exercise_id INTEGER REFERENCES exercises(id),
    status VARCHAR(20), -- 'not_started', 'in_progress', 'completed'
    score DECIMAL(5,2),
    attempts INTEGER DEFAULT 0,
    mastery_level DECIMAL(5,2), -- 0-100 percentage
    last_attempted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Code submissions table
CREATE TABLE IF NOT EXISTS submissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    exercise_id INTEGER REFERENCES exercises(id),
    code TEXT,
    result TEXT, -- JSON with execution results
    passed BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AI interactions table (for tracking AI tutoring sessions)
CREATE TABLE IF NOT EXISTS ai_interactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    agent_type VARCHAR(50), -- 'triage', 'concepts', 'debug', 'exercise', 'progress'
    query TEXT,
    response TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_user_progress_user_id ON user_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_submissions_user_id ON submissions(user_id);
CREATE INDEX IF NOT EXISTS idx_exercises_lesson_id ON exercises(lesson_id);

-- Insert default modules (Python curriculum)
INSERT INTO modules (title, description, module_order) VALUES
('Basics', 'Variables, Data Types, Input/Output, Operators, Type Conversion', 1),
('Control Flow', 'Conditionals (if/elif/else), For Loops, While Loops, Break/Continue', 2),
('Data Structures', 'Lists, Tuples, Dictionaries, Sets', 3),
('Functions', 'Defining Functions, Parameters, Return Values, Scope', 4),
('OOP', 'Classes & Objects, Attributes & Methods, Inheritance, Encapsulation', 5),
('Files', 'Reading/Writing Files, CSV Processing, JSON Handling', 6),
('Errors', 'Try/Except, Exception Types, Custom Exceptions, Debugging', 7),
('Libraries', 'Installing Packages, Working with APIs, Virtual Environments', 8)
ON CONFLICT DO NOTHING;

-- Insert a default admin user (password: admin123)
INSERT INTO users (username, email, password_hash, role) VALUES
('admin', 'admin@learnflow.test', '$2b$12$LQv3c158QRv132ztL64nfOykfv8AKD5g4/4tliWLqBjwEO8d.Hpmy', 'admin')
ON CONFLICT DO NOTHING;
EOF

# Apply the schema
kubectl exec -n postgresql svc/postgresql -- psql -U postgres -d learnflow_db -f /tmp/learnflow_schema.sql

echo "✅ LearnFlow schema applied successfully!"

# Clean up temporary file
rm /tmp/learnflow_schema.sql

echo "📋 Schema includes:"
echo "   - Users and roles management"
echo "   - Module-based curriculum"
echo "   - Lesson content management"
echo "   - Exercise definitions"
echo "   - User progress tracking"
echo "   - Code submission records"
echo "   - AI interaction logging"