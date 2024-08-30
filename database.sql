-- Create Database User

-- Create the user
CREATE USER 'sharebuddy'@'localhost' IDENTIFIED BY 'sharebuddy';

-- Grant all privileges on the sharebuddy database to the user
GRANT ALL PRIVILEGES ON sharebuddy.* TO 'sharebuddy'@'localhost';

-- Apply the changes
FLUSH PRIVILEGES;
-- PUT THE DATABASE SQL TO CREATE DB AND TABLES HERE --
-- Create the database
CREATE DATABASE sharebuddy;

-- Use the newly created database
USE sharebuddy;

-- Create the users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the posts table (if you have a posts feature)
CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);