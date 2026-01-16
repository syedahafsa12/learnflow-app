-- LearnFlow Database Schema
-- AI-Powered Python Tutoring Platform

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('student', 'teacher', 'admin')),
    full_name VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Students table (extends users)
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    current_module INTEGER DEFAULT 1,
    total_mastery_score DECIMAL(5, 2) DEFAULT 0.00,
    learning_streak_days INTEGER DEFAULT 0,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Teachers table (extends users)
CREATE TABLE IF NOT EXISTS teachers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    department VARCHAR(100),
    specialization VARCHAR(100)
);

-- Modules (Python curriculum)
CREATE TABLE IF NOT EXISTS modules (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    order_index INTEGER NOT NULL,
    topics TEXT[] NOT NULL
);

-- Student progress tracking
CREATE TABLE IF NOT EXISTS student_progress (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    module_id INTEGER NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    mastery_score DECIMAL(5, 2) DEFAULT 0.00,
    exercises_completed INTEGER DEFAULT 0,
    exercises_total INTEGER DEFAULT 0,
    quiz_score DECIMAL(5, 2) DEFAULT 0.00,
    code_quality_avg DECIMAL(5, 2) DEFAULT 0.00,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, module_id)
);

-- Conversations (chat history)
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    agent_name VARCHAR(50) NOT NULL,
    query TEXT NOT NULL,
    response TEXT NOT NULL,
    routed_to VARCHAR(50),
    confidence DECIMAL(3, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Code submissions
CREATE TABLE IF NOT EXISTS code_submissions (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    module_id INTEGER REFERENCES modules(id) ON DELETE SET NULL,
    code TEXT NOT NULL,
    language VARCHAR(20) DEFAULT 'python',
    output TEXT,
    error_message TEXT,
    execution_time_ms INTEGER,
    quality_score DECIMAL(5, 2),
    feedback TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Exercises
CREATE TABLE IF NOT EXISTS exercises (
    id SERIAL PRIMARY KEY,
    module_id INTEGER NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    difficulty VARCHAR(20) CHECK (difficulty IN ('easy', 'medium', 'hard')),
    starter_code TEXT,
    test_cases JSONB,
    solution TEXT,
    created_by INTEGER REFERENCES teachers(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Exercise attempts
CREATE TABLE IF NOT EXISTS exercise_attempts (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    exercise_id INTEGER NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    code TEXT NOT NULL,
    passed BOOLEAN DEFAULT FALSE,
    test_results JSONB,
    attempts_count INTEGER DEFAULT 1,
    time_spent_seconds INTEGER,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Quizzes
CREATE TABLE IF NOT EXISTS quizzes (
    id SERIAL PRIMARY KEY,
    module_id INTEGER NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    questions JSONB NOT NULL,
    passing_score DECIMAL(5, 2) DEFAULT 70.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Quiz attempts
CREATE TABLE IF NOT EXISTS quiz_attempts (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    quiz_id INTEGER NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
    answers JSONB NOT NULL,
    score DECIMAL(5, 2) NOT NULL,
    passed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Struggle alerts
CREATE TABLE IF NOT EXISTS struggle_alerts (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    module_id INTEGER REFERENCES modules(id) ON DELETE SET NULL,
    trigger_type VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    severity VARCHAR(20) CHECK (severity IN ('low', 'medium', 'high')),
    resolved BOOLEAN DEFAULT FALSE,
    resolved_by INTEGER REFERENCES teachers(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

-- Insert default Python curriculum modules
INSERT INTO modules (name, description, order_index, topics) VALUES
('Basics', 'Python fundamentals', 1, ARRAY['Variables', 'Data Types', 'Input/Output', 'Operators', 'Type Conversion']),
('Control Flow', 'Control structures', 2, ARRAY['Conditionals', 'For Loops', 'While Loops', 'Break', 'Continue']),
('Data Structures', 'Built-in data structures', 3, ARRAY['Lists', 'Tuples', 'Dictionaries', 'Sets']),
('Functions', 'Function definition and usage', 4, ARRAY['Defining Functions', 'Parameters', 'Return Values', 'Scope']),
('OOP', 'Object-oriented programming', 5, ARRAY['Classes', 'Objects', 'Attributes', 'Methods', 'Inheritance', 'Encapsulation']),
('Files', 'File handling', 6, ARRAY['Reading Files', 'Writing Files', 'CSV', 'JSON']),
('Errors', 'Error handling', 7, ARRAY['Try/Except', 'Exception Types', 'Custom Exceptions', 'Debugging']),
('Libraries', 'Working with packages', 8, ARRAY['Package Management', 'APIs', 'Virtual Environments'])
ON CONFLICT DO NOTHING;

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_students_user_id ON students(user_id);
CREATE INDEX IF NOT EXISTS idx_conversations_student_id ON conversations(student_id);
CREATE INDEX IF NOT EXISTS idx_conversations_created_at ON conversations(created_at);
CREATE INDEX IF NOT EXISTS idx_code_submissions_student_id ON code_submissions(student_id);
CREATE INDEX IF NOT EXISTS idx_code_submissions_module_id ON code_submissions(module_id);
CREATE INDEX IF NOT EXISTS idx_student_progress_student_id ON student_progress(student_id);
CREATE INDEX IF NOT EXISTS idx_exercise_attempts_student_id ON exercise_attempts(student_id);
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_student_id ON quiz_attempts(student_id);
CREATE INDEX IF NOT EXISTS idx_struggle_alerts_student_id ON struggle_alerts(student_id);
CREATE INDEX IF NOT EXISTS idx_struggle_alerts_resolved ON struggle_alerts(resolved);
