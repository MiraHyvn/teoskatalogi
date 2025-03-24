CREATE TABLE kayttajat (
	id INTEGER PRIMARY KEY,
	tunnus TEXT UNIQUE, 
	salasana_hash TEXT
);

CREATE TABLE teokset (
	id INTEGER PRIMARY KEY,
	nimi TEXT,
    	kayttaja_id INTEGER REFERENCES kayttajat
);

