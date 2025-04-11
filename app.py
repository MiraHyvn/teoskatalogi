from flask import Flask
from flask import redirect, render_template, request, session, abort
import sqlite3
import catalogue
import config

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    teokset = catalogue.get_all_works()
    kokoelmat = {}
    for t in teokset:
        kokoelmat[t["id"]] = catalogue.get_collections_that_include(t["id"])
    return render_template("index.html", works=teokset, collections=kokoelmat)

@app.route("/rekisteroidy")
def rekisteroidy():
    return render_template("register.html")

@app.route("/kirjaudu", methods=["POST"])
def kirjaudu():
    annettu_tunnus = request.form["username_input"]
    annettu_salasana = request.form["password_input"]
    kayttaja_id = catalogue.check_password(annettu_tunnus, annettu_salasana)
    if kayttaja_id:
        session["user_id"] = kayttaja_id
        return redirect("/")
    else:
        return "Virhe: Väärä tunnus tai salasana."
    
@app.route("/luo_kayttaja", methods=["POST"])
def luo_kayttaja():
    uusi_tunnus = request.form["username_input"]
    uusi_salasana = request.form["password_input"]
    if len(uusi_tunnus) > 50 or len(uusi_tunnus) == 0 or len(uusi_salasana) > 50:
        abort(403)
    try:
        catalogue.create_user(uusi_tunnus, uusi_salasana)
    except sqlite3.IntegrityError:
        return "Virhe: Käyttäjää ei voitu luoda."
    return redirect("/")

@app.route("/kirjaudu_ulos")
def kirjaudu_ulos():
    del session["user_id"]
    return redirect("/")
    
@app.route("/luo_teos", methods=["POST"])
def luo_teos():
    vaadi_kirjautuminen()
    annettu_teoksen_nimi = request.form["new_work_name_input"]
    if len(annettu_teoksen_nimi) == 0 or len(annettu_teoksen_nimi) > 50:    
        abort(403)
    kayttaja_id = session["user_id"]
    catalogue.create_work(annettu_teoksen_nimi, kayttaja_id)
    return redirect("/")

@app.route("/poista_teos/<int:teos_id>", methods=["POST"])
def poista_teos(teos_id):
    vaadi_kirjautuminen()
    teos = catalogue.get_work(teos_id)
    if session["user_id"] == teos["user_id"]:
        catalogue.delete_work(teos_id)
    else:
        abort(403)
    return redirect("/")

@app.route("/muokkaa_teosta/<int:teos_id>", methods=["GET", "POST"])
def muokkaa_teosta(teos_id):
    vaadi_kirjautuminen()
    teos = catalogue.get_work(teos_id)
    if session["user_id"] != teos["user_id"]:
        abort(403)
    if request.method == "GET":
        return render_template("edit_work.html", work = teos)
    if request.method == "POST":
        uusi_nimi = request.form["name_input"]
        catalogue.edit_work(teos_id, "name", uusi_nimi)
    return redirect("/")

@app.route("/haku")
def haku():
    hakusana_arg = request.args.get("search_term")
    if hakusana_arg:
        tulokset = catalogue.search(hakusana_arg) 
    else:
        tulokset = []
    return render_template("search.html",search_term=hakusana_arg, results=tulokset)

@app.route("/liita_kokoelmaan/<int:teos_id>", methods=["POST"])
def liita_kokoelmaan(teos_id):
    vaadi_kirjautuminen()
    kokoelman_nimi = request.form["collection_name_input"]
    catalogue.add_work_to_collection(teos_id, kokoelman_nimi, session["user_id"])
    return redirect("/")

@app.route("/kokoelmat")
def kokoelmat():
    kokoelmat = catalogue.get_all_collections()
    teokset = {}
    for k in kokoelmat:
        teokset[k["id"]] = catalogue.get_works_included_in(k["id"])
    return render_template("collections.html", collections=kokoelmat, works=teokset)
    
def vaadi_kirjautuminen():
    if "user_id" not in session:
        abort(403)
