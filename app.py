from flask import Flask
from flask import render_template, redirect
import sqlite3
import tietokanta

app = Flask(__name__)

@app.route("/")
def index():
    kayttajaluettelo = tietokanta.kysely("SELECT tunnus FROM kayttajat")
    kayttajia = len(kayttajaluettelo)
    return render_template("index.html", n = kayttajia, tunnukset = kayttajaluettelo)

@app.route("/rekisteroidy")
def rekisteroidy():
    uusi_tunnus = "Uusi Tunnus"
    tietokanta.suorita("INSERT INTO kayttajat (tunnus) VALUES (?);", [uusi_tunnus])
    return redirect("/")
