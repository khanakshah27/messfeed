CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    feedback TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT now(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
