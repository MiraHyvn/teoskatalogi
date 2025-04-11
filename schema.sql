CREATE TABLE Users (
	id INTEGER PRIMARY KEY,
	name TEXT UNIQUE, 
	password_hash TEXT
);

CREATE TABLE Works (
	id INTEGER PRIMARY KEY,
	name TEXT,
    	user_id INTEGER REFERENCES Users
);

CREATE TABLE Collections (
	id INTEGER PRIMARY KEY,
	name TEXT,
	user_id INTEGER REFERENCES Users
);

CREATE TABLE WorksInCollection (
	id integer PRIMARY KEY,
	work_id INTEGER REFERENCES Works,
	collection_id INTEGER REFERENCES Collections
);
