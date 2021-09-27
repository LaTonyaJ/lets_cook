CREATE DATABASE lets_cook;

\c lets_cook;

CREATE TABLE user
(
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    user_password TEXT NOT NULL
);

CREATE TABLE favorites
(
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES user,
    meal_id INTEGER NOT NULL UNIQUE
);