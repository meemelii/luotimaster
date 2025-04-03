import sqlite3, secrets
from flask import Flask
from flask import abort, flash, make_response, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db, config, events, users

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    try:
        username=session["username"]
        return render_template("index.html", username=username)
    except: return render_template("index.html")

@app.route("/events")
def ownevents():
    user_id = session["user_id"]
    outgoing_events = events.get_outgoing_events(user_id)
    incoming_events = events.get_incoming_events(user_id)
    return render_template("ownevents.html", incoming_events=incoming_events, outgoing_events=outgoing_events)

@app.route("/murders")
def murders():
    murders=events.get_murders()
    return render_template("murders.html", murders=murders)

@app.route("/search")
def search():
    query = request.args.get("query")
    results = events.search(query) if query else []
    return render_template("search.html", query=query, results=results)

@app.route("/report")
def report():
    require_login()
    kohteet = users.get_other_users(session["user_id"])
    return render_template("report.html", kohteet=kohteet )

@app.route("/new_report", methods=["POST"])
def new_report():
    require_login()
    check_csrf()
    target_id = request.form["kohde"]
    event_id = events.add_event(session["user_id"], target_id)
    return redirect("/event/" + str(event_id) + "/edit")

@app.route("/event/<int:event_id>")
def show_event(event_id):
    event = events.get_event(event_id)
    if not event: 
        abort(404)
    if "user_id" in session:
        user_id = session["user_id"]
    else: user_id = None
    if event[5] == 0:
        require_login()
        if user_id != event[1] and user_id != event[2]:
            abort(403)
    weapon_name = name_weapon(event[4])
    return render_template("eventpage.html", event=event, user_id = user_id, weapon_name = weapon_name)

@app.route("/register")
def register():
    if request.method == "GET":
        return render_template("register.html", filled={})

@app.route("/event/<int:event_id>/edit")
def editpage(event_id):
    require_login()
    event=events.get_event(event_id)
    if not event: 
        abort(404)
    killer_username = users.get_username(event[1])
    target_username = users.get_username(event[2])
    return render_template("editevent.html", event=event, killer_username = killer_username, target_username = target_username)

@app.route("/event/<int:event_id>/edited", methods=["POST"])
def edited(event_id):
    require_login()
    check_csrf()
    zip = request.form["zip"]
    weapon_type = request.form["Asetyyppi"]
    events.edit_event(event_id, zip, weapon_type)
    return redirect("/event/"+ str(event_id))

@app.route("/event/<int:event_id>/confirm", methods=["POST"])
def confirm(event_id): 
    require_login()
    check_csrf()   
    events.confirm(event_id, request.form["confirm"])    
    return redirect("/event/"+ str(event_id))

@app.route("/event/<int:event_id>/delete", methods=["GET","POST"])
def delete_event(event_id):
    require_login()
    user_id = session["user_id"]
    event = events.get_event(event_id)
    if request.method == "GET":
        return render_template("delete.html", event_id=event_id, user_id=user_id, event=event)
    if request.method == "POST":
        if "continue" in request.form:
            check_csrf()
            events.delete_event(event_id)
            flash("Tapahtuma poistettu.")
            return redirect("/events")
        else: return redirect("/events/"+ str(event_id))


def name_weapon(weapon_id):
#if more time, do this better
        if weapon_id==1:return "Foliopuukko / muu lähiase"
        elif weapon_id==2: return "Nerf- tai vesipistooli"
        elif weapon_id==3: return "Ruoka- tai kosketusmyrkky"
        elif weapon_id==4: return "Tappava eläin" 
        elif weapon_id==5: return "Pommi tai muu ansa"
        elif weapon_id==6: return "Muu/luokittelematon"
        else: return "Ei tiedossa" 


@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("VIRHE: salasanat eivät täsmää!")
        filled = {"username": username}
        return render_template("register.html", filled=filled)
    try:
        users.create_user(username,password1)
        flash("Tunnus luotu!")
        return redirect("/")
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        filled = {"username": username}
        return render_template("register.html", filled=filled)

    

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", filled={})

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["csrf_token"] = secrets.token_hex(16)
            session["username"] = username
            return redirect("/")
        else:
            flash("VIRHE: väärä tunnus tai salasana")
            filled = {"username": username}
            return render_template("login.html", filled=filled)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    flash("Olet kirjautunut ulos.")
    return redirect("/")
