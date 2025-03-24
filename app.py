from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import tietokanta
import config

app = Flask(__name__)
app.secret_key = config.salainen_avain

# Tietokannassa tietokanta.db on oltava taulu, joka on luotu esim näin:
# CREATE TABLE kayttajat (id INTEGER PRIMARY KEY, tunnus TEXT UNIQUE, salasana_hash TEXT);

@app.route("/")
def index():
    kayttajaluettelo = tietokanta.kysely("SELECT tunnus FROM kayttajat")
    kayttajia = len(kayttajaluettelo)
    return render_template("index.html", n = kayttajia, tunnukset = kayttajaluettelo)

@app.route("/rekisteroidy")
def rekisteroidy():
    # Pitäisikö olla mahdollista kun ollaan kirjautuneena?
    return render_template("rekisteroidy.html")

@app.route("/kirjaudu", methods=["POST"])
def kirjaudu():
    # Ongelma: Jos käyttäjä syöttää tunnuksen, jota ei ole => Internal server error (500)
    annettu_tunnus = request.form["tunnus"]
    annettu_salasana = request.form["salasana"]
    sql = "SELECT salasana_hash FROM kayttajat WHERE tunnus = ?"
    oikea_hash = tietokanta.kysely(sql, [annettu_tunnus])[0][0]
    if check_password_hash(oikea_hash, annettu_salasana):
        session["kayttajatunnus"] = annettu_tunnus
        return redirect("/")
    else:
        return "Virhe: Väärä tunnus tai salasana." 
    
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

@app.route("/kirjaudu_ulos")
def kirjaudu_ulos():
    del session["kayttajatunnus"]
    return redirect("/")
    
@app.route("/luo_teos", methods=["POST"])
def luo_teos():
    annettu_teoksen_nimi = request.form["uusi_teos_nimi"]
    kayttajatunnus = session["kayttajatunnus"]
    sql = "INSERT INTO teokset (nimi, kayttaja_id) VALUES (?, ?)"
    tietokanta.suorita(sql, [annettu_teoksen_nimi, kayttajatunnus])
    return redirect("/")
