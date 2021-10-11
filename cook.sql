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

CREATE TABLE favorites
(
    id SERIAL PRIMARY KEY,
    users_id INTEGER NOT NULL REFERENCES users,
    img TEXT,
    api_id TEXT UNIQUE,
    recipe_name TEXT
);

CREATE TABLE instructions
(
    id SERIAL PRIMARY KEY,
    favorites_id INTEGER NOT NULL REFERENCES favorites,
    steps TEXT NOT NULL 
); 

CREATE TABLE ingredients
(
    id SERIAL PRIMARY KEY,
    favorites_id INTEGER NOT NULL REFERENCES favorites,
    items TEXT[] NOT NULL 
);


