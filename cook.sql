DROP DATABASE lets_cook;

CREATE DATABASE lets_cook;

\c lets_cook;

CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    user_password TEXT NOT NULL
);

CREATE TABLE meals
(
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL UNIQUE,
    img TEXT,
    instructions TEXT NOT NULL
);

CREATE TABLE favorites
(
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users,
    meal_id INTEGER NOT NULL REFERENCES meals
);

