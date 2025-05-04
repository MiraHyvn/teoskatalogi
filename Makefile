all:
	sqlite3 database.db < schema.sql
	sqlite3 database.db < init.sql
	python3 -m venv venv
	venv/bin/pip install flask
remove:
	rm -f database.db
	rm -Rf venv __pycache__