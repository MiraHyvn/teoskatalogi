CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE, 
    password_hash TEXT
);

CREATE TABLE Works (
    id INTEGER PRIMARY KEY,
    title TEXT,
    	user_id INTEGER REFERENCES Users,
    	deleted INTEGER DEFAULT 0
);

CREATE TABLE Collections (
    id INTEGER PRIMARY KEY,
    title TEXT,
    user_id INTEGER REFERENCES Users
);

CREATE TABLE WorksInCollection (
    id INTEGER PRIMARY KEY,
    work_id INTEGER REFERENCES Works,
    collection_id INTEGER REFERENCES Collections
);

CREATE TABLE Classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE WorkClasses (
    id INTEGER PRIMARY KEY,
    work_id INTEGER REFERENCES Works,
    class_id INTEGER REFERENCES Classes
);

