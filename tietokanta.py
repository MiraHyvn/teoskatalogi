import sqlite3
from flask import g

# Tietokannassa on oltava taulu, joka on luotu esim näin:
# CREATE TABLE kayttajat (id INTEGER PRIMARY KEY, tunnus TEXT UNIQUE, salasana_hash TEXT);

def luo_yhteys():
    yhteys = sqlite3.connect("tietokanta.db")
    yhteys.row_factory = sqlite3.Row
    return yhteys

def suorita(sql, parametrit=[]):
    yhteys = luo_yhteys()
    tulos = yhteys.execute(sql, parametrit)
    yhteys.commit()
    yhteys.close()

def kysely(sql, parametrit=[]):
    yhteys = luo_yhteys()
    tulos = yhteys.execute(sql, parametrit).fetchall()
    yhteys.close()
    return tulos

