import sqlite3
from flask import g

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

