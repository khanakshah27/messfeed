CREATE TABLE reginfo (
    id SERIAL PRIMARY KEY,
    registration_number VARCHAR(20) NOT NULL,
    mess_name VARCHAR(255) NOT NULL,
    student_name VARCHAR(255) NOT NULL,
    mess_type VARCHAR(50) NOT NULL,
    block VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL,
    room_no VARCHAR(10) NOT NULL
);

