from flask import Flask
from flask import redirect, render_template, request, session, abort
import sqlite3, secrets
import catalogue
import config

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    works = catalogue.get_all_works()
    all_classes = catalogue.get_all_classes()
    if "user_id" in session:
        u_collections = catalogue.get_collections_by_user(session["user_id"])
    else:
        u_collections = None
    work_classes = {}
    w_collections = {}
    for w in works:
        work_classes[w["id"]] = catalogue.get_classes(w["id"]) 
        w_collections[w["id"]] = catalogue.get_collections_that_include(w["id"])
    return render_template("index.html", works=works, all_classes = all_classes, work_classes = work_classes, u_collections = u_collections, w_collections=w_collections)

@app.route("/rekisteroidy")
def register():
    return render_template("register.html")

@app.route("/kirjaudu", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username_input = request.form["username_input"]
        password_input = request.form["password_input"]
        valid_user_id = catalogue.check_password(username_input, password_input)
        if valid_user_id:
            session["user_id"] = valid_user_id
            session["user_name"] = catalogue.get_user_name(valid_user_id)
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            return "Virhe: Väärä tunnus tai salasana. <a href=\"/kirjaudu\"> Palaa takaisin </a>"
    
@app.route("/luo_kayttaja", methods=["POST"])
def create_user():
    username_input = request.form["username_input"]
    password_input = request.form["password_input"]
    if len(username_input) > 50 or len(username_input) == 0 or len(password_input) > 50:
        abort(403)
    try:
        catalogue.create_user(username_input, password_input)
    except sqlite3.IntegrityError:
        return "Virhe: Käyttäjää ei voitu luoda."
    return redirect("/")

@app.route("/kirjaudu_ulos")
def logout():
    del session["user_id"]
    del session["user_name"]
    return redirect("/")
    
@app.route("/luo_teos", methods=["POST"])
def create_work():
    require_login()
    check_csrf()
    work_title_input = request.form["work_title_input"]
    medium_input = request.form["medium_input"]
    if len(work_title_input) == 0 or len(work_title_input) > 50:    
        abort(403)
    user_id = session["user_id"]
    classes = {"tekniikka": medium_input}
    catalogue.create_work(work_title_input, classes, user_id)
    return redirect("/")

@app.route("/poista_teos/<int:work_id>", methods=["POST"])
def delete_work(work_id):
    require_login()
    check_csrf()
    work = catalogue.get_work(work_id)
    if session["user_id"] == work["user_id"]:
        catalogue.delete_work(work_id)
    else:
        abort(403)
    return redirect("/")

@app.route("/muokkaa_teosta/<int:work_id>", methods=["GET", "POST"])
def muokkaa_teosta(work_id):
    require_login()
    work = catalogue.get_work(work_id)
    if not work:
        abort(404)
    if session["user_id"] != work["user_id"]:
        abort(403)
    if request.method == "GET":
        return render_template("edit_work.html", work = work)
    if request.method == "POST":
        check_csrf()    
        updated_title = request.form["title_input"]
        catalogue.edit_work(work_id, "title", updated_title)
    return redirect("/")

@app.route("/haku")
def search():
    search_term_arg = request.args.get("search_term")
    if search_term_arg:
        results = catalogue.search(search_term_arg)
    else:
        results = []
    return render_template("search.html",search_term=search_term_arg, results=results)

@app.route("/luo_kokoelma", methods=["POST"])
def create_collection():
    require_login()
    check_csrf()
    collection_title_input = request.form["collection_title_input"]
    if len(collection_title_input) == 0 or len(collection_title_input) > 50:
        abort(403)
    user_id = session["user_id"]
    catalogue.create_collection(collection_title_input, user_id)
    return redirect("/kokoelmat")

@app.route("/liita_kokoelmaan/<int:work_id>", methods=["POST"])
def add_to_collection(work_id):
    require_login()
    check_csrf()
    # Should refer to collection by id rather than title?
    collection_title = request.form["collection_title_input"]
    collection = catalogue.get_collection(collection_title)
    if collection["user_id"] != session["user_id"]:
        abort(403)
    try:
        catalogue.add_work_to_collection(work_id, collection_title, session["user_id"])
    except sqlite3.IntegrityError:
        # Requested to add something that already exists => don't do anything
        return("Virhe: Teos on jo kokoelmassa")
    return redirect("/")

@app.route("/kokoelmat")
def collections():
    all_collections = catalogue.get_all_collections()
    works = {}
    for c in all_collections:
        works[c["id"]] = catalogue.get_works_included_in(c["id"])
    return render_template("collections.html", collections=all_collections, works=works)
    
def require_login():
    if "user_id" not in session:
        abort(403)
    
@app.route("/kayttaja/<int:user_id>")
def user(user_id):
    require_login() 
    if user_id != session["user_id"]:
        abort(403)
    w = catalogue.get_works_by_user(user_id)
    c = catalogue.get_collections_by_user(user_id)
    s = catalogue.get_user_stats(user_id, c)
    return render_template("user.html", works = w, collections = c, stats = s)

def check_csrf():
    if "csrf_token" not in session:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)
