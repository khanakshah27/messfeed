CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    reg_number VARCHAR(20) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL, 
    student_name VARCHAR(255),
    role VARCHAR(20) NOT NULL DEFAULT 'student',
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS admins (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    registration_number VARCHAR(20),
    mess_name VARCHAR(255),
    student_name VARCHAR(255),
    mess_type VARCHAR(50),
    block VARCHAR(50),
    category VARCHAR(50),
    room_no VARCHAR(10),
    feedback TEXT,
    status VARCHAR(20) DEFAULT 'Pending',
    admin_comment TEXT,
    timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_feedback_user_id ON feedback(user_id);
CREATE INDEX IF NOT EXISTS idx_feedback_regno ON feedback(registration_number);
