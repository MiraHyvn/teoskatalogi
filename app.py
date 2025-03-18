from flask import Flask
from flask import redirect, render_template, request
from werkzeug.security import generate_password_hash
import sqlite3
import tietokanta

app = Flask(__name__)

# Tietokannassa tietokanta.db on oltava taulu, joka on luotu esim näin:
# CREATE TABLE kayttajat (id INTEGER PRIMARY KEY, tunnus TEXT UNIQUE, salasana_hash TEXT);

@app.route("/")
def index():
    kayttajaluettelo = tietokanta.kysely("SELECT tunnus FROM kayttajat")
    kayttajia = len(kayttajaluettelo)
    return render_template("index.html", n = kayttajia, tunnukset = kayttajaluettelo)

@app.route("/rekisteroidy")
def rekisteroidy():
    return render_template("rekisteroidy.html")

@app.route("/luo_kayttaja", methods=["POST"])
def luo_kayttaja():
    uusi_tunnus = request.form["tunnus"]
    uusi_salasana = request.form["salasana"]
    uusi_hash = generate_password_hash(uusi_salasana)
    try:
        sql = "INSERT INTO kayttajat (tunnus, salasana_hash) VALUES (?, ?)"
        tietokanta.suorita(sql, [uusi_tunnus, uusi_hash])
    except sqlite3.IntegrityError:
        return "virhe"
    return redirect("/")
    
