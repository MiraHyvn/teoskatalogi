from flask import Flask
from flask import redirect, render_template, request, session, abort
import sqlite3
import tietokanta, katalogi
import config

app = Flask(__name__)
app.secret_key = config.salainen_avain

@app.route("/")
def index():
    teokset = katalogi.hae_kaikki_teokset()
    kokoelmat = {}
    for t in teokset:
        kokoelmat[t["id"]] = katalogi.hae_kokoelmat_joihin_kuuluu(t["id"])
    return render_template("index.html", teokset=teokset, kokoelmat=kokoelmat)

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
    vaadi_kirjautuminen()
    annettu_teoksen_nimi = request.form["uusi_teos_nimi"]
    kayttajatunnus = session["kayttajatunnus"]
    katalogi.lisaa_teos(annettu_teoksen_nimi, kayttajatunnus)
    return redirect("/")

@app.route("/poista_teos/<int:teos_id>", methods=["POST"])
def poista_teos(teos_id):
    vaadi_kirjautuminen()
    katalogi.poista_teos(teos_id)
    return redirect("/")

@app.route("/muokkaa_teosta/<int:teos_id>", methods=["GET", "POST"])
def muokkaa_teosta(teos_id):
    vaadi_kirjautuminen()
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

@app.route("/liita_kokoelmaan/<int:teos_id>", methods=["POST"])
def liita_kokoelmaan(teos_id):
    vaadi_kirjautuminen()
    kokoelman_nimi = request.form["kokoelma"]
    katalogi.liita_teos_kokoelmaan(teos_id, kokoelman_nimi, session["kayttajatunnus"])
    return redirect("/")

@app.route("/kokoelmat")
def kokoelmat():
    kokoelmat = katalogi.hae_kaikki_kokoelmat()
    teokset = {}
    for k in kokoelmat:
        teokset[k["id"]] = katalogi.hae_teokset_jotka_kuuluvat(k["id"])
    return render_template("kokoelmat.html", kokoelmat=kokoelmat, teokset=teokset)
    
def vaadi_kirjautuminen():
    if "kayttajatunnus" not in session:
        abort(403)
