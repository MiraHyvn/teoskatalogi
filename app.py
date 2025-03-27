from flask import Flask
from flask import redirect, render_template, request, session
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
    return render_template("rekisteroidy.html")

@app.route("/kirjaudu", methods=["POST"])
def kirjaudu():
    annettu_tunnus = request.form["tunnus"]
    annettu_salasana = request.form["salasana"]
    if katalogi.tarkista_salasana(annettu_tunnus, annettu_salasana):
        session["kayttajatunnus"] = annettu_tunnus
        return redirect("/")
    else:
        return "Virhe: Väärä tunnus tai salasana."
    
@app.route("/luo_kayttaja", methods=["POST"])
def luo_kayttaja():
    uusi_tunnus = request.form["tunnus"]
    uusi_salasana = request.form["salasana"]
    try:
        katalogi.lisaa_kayttaja(uusi_tunnus, uusi_salasana)
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
    if request.method == "GET":
        teos = katalogi.hae_teos(teos_id)
        return render_template("muokkaa_teosta.html", teos = teos)
    if request.method == "POST":
        uusi_nimi = request.form["nimi"]
        katalogi.muuta_teosta(teos_id, "nimi", uusi_nimi)
    return redirect("/")

@app.route("/haku")
def haku():
    hakusana_arg = request.args.get("hakusana")
    if hakusana_arg:
        tulokset = katalogi.haku(hakusana_arg) 
    else:
        tulokset = []
    return render_template("haku.html",hakusana=hakusana_arg,tulokset=tulokset)
