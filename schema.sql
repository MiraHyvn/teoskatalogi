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

CREATE TABLE kokoelmat (
	id INTEGER PRIMARY KEY,
	kayttaja_id INTEGER REFERENCES kayttajat,
	nimi TEXT
);

CREATE TABLE kokoelmanTeokset (
	id integer PRIMARY KEY,
	teos_id INTEGER REFERENCES teokset,
	kokoelma_id INTEGER REFERENCES kokoelmat
);
