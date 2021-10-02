DROP DATABASE lets_cook;

CREATE DATABASE lets_cook;

\c lets_cook;

CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE meals
(
    id SERIAL PRIMARY KEY,
    api_id TEXT NOT NULL UNIQUE
);

CREATE TABLE favorites
(
    id SERIAL PRIMARY KEY,
    users_id INTEGER NOT NULL REFERENCES users,
    meals_id INTEGER NOT NULL REFERENCES meals
);

