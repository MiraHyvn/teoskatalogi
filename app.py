from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import tietokanta, katalogi
import config

app = Flask(__name__)
app.secret_key = config.salainen_avain

@app.route("/")
def index():
    teokset = katalogi.hae_kaikki_teokset()
    return render_template("index.html", teokset = teokset)

@app.route("/rekisteroidy")
def rekisteroidy():
    # Pitäisikö olla mahdollista kun ollaan kirjautuneena?
    return render_template("rekisteroidy.html")

@app.route("/kirjaudu", methods=["POST"])
def kirjaudu():
    # Ongelma: Jos käyttäjä syöttää tunnuksen, jota ei ole 
    #   => Internal server error (500)
    annettu_tunnus = request.form["tunnus"]
    annettu_salasana = request.form["salasana"]
    # SQL-toiminto: Tarkista salasana
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
        katalogi.lisaa_kayttaja(uusi_tunnus, uusi_hash)
    except sqlite3.IntegrityError:
        return "Virhe: Käyttäjää ei voitu luoda."
    return redirect("/")

@app.route("/kirjaudu_ulos")
def kirjaudu_ulos():
    del session["kayttajatunnus"]
    return redirect("/")
    
@app.route("/luo_teos", methods=["POST"])
def luo_teos():
    annettu_teoksen_nimi = request.form["uusi_teos_nimi"]
    kayttajatunnus = session["kayttajatunnus"]
    katalogi.lisaa_teos(annettu_teoksen_nimi, kayttajatunnus)
    return redirect("/")

@app.route("/poista_teos/<int:teos_id>", methods=["POST"])
def poista_teos(teos_id):
    katalogi.poista_teos(teos_id)
    return redirect("/")

@app.route("/muokkaa_teosta/<int:teos_id>", methods=["GET", "POST"])
def muokkaa_teosta(teos_id):
    teos = katalogi.hae_teos(teos_id)
    if request.method == "GET":
        return render_template("muokkaa_teosta.html", teos = teos)
    if request.method == "POST":
        uusi_nimi = request.form["nimi"]
        sql = "UPDATE teokset SET nimi = ? WHERE id = ?"
        tietokanta.suorita(sql, [uusi_nimi, teos_id])
    return redirect("/")
