CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(60) NOT NULL,
    avatar_url TEXT NOT NULL,
    personality_type VARCHAR(20)
);


CREATE TABLE personality_types (
    type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(20) UNIQUE NOT NULL
);


CREATE TABLE post_types (
    type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(20) UNIQUE NOT NULL
);


CREATE TABLE stories (
    story_id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    user_id INT REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE commments (
    comments_id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    post_title TEXT NOT NULL,
    post_type VARCHAR(100) REFERENCES post_types(type_name),
    user_id INT REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT NOW()
);