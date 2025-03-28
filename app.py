import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import db, config, events, users

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    try:
        username=users.get_username(session["user_id"])
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
    kohteet = users.get_other_users(session["user_id"])
    return render_template("report.html", kohteet=kohteet )

@app.route("/new_report", methods=["POST"])
def new_report():
    target_id = request.form["kohde"]
    event_id = events.add_event(session["user_id"], target_id)
    return redirect("/event/" + str(event_id) + "/edit")

@app.route("/event/<int:event_id>")
def show_event(event_id):
    event = events.get_event(event_id)
    user_id = session["user_id"]
    weapon_name = name_weapon(event[4])
    return render_template("eventpage.html", event=event, user_id = user_id, weapon_name = weapon_name)

@app.route("/register")
def register():
    if request.method == "GET":
        return render_template("register.html", filled={})

@app.route("/event/<int:event_id>/edit")
def editpage(event_id):
    event= events.get_event(event_id)
    killer_username = users.get_username(event[1])
    target_username = users.get_username(event[2])
    return render_template("editevent.html", event=event, killer_username = killer_username, target_username = target_username)

@app.route("/event/<int:event_id>/edited", methods=["POST"])
def edited(event_id):
    zip = request.form["zip"]
    weapon_type = request.form["Asetyyppi"]
    events.edit_event(event_id, zip, weapon_type)
    return redirect("/event/"+ str(event_id))

@app.route("/event/<int:event_id>/confirm", methods=["POST"])
def confirm(event_id):    
    events.confirm(event_id, request.form["confirm"])    
    return redirect("/event/"+ str(event_id))

@app.route("/event/<int:event_id>/delete", methods=["GET","POST"])
def delete_event(event_id):
    user_id = session["user_id"]
    event = events.get_event(event_id)
    if request.method == "GET":
        return render_template("delete.html", event_id=event_id, user_id=event, event=event)
    if request.method == "POST":
        if "continue" in request.form:
            events.delete_event(event_id)
            flash("Tapahtuma poistettu.")
            return redirect("/events")
        else: return redirect("/events/"+ str(event_id))




def name_weapon(weapon_id):
#jos aikaa, tee paremmin.
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
            return redirect("/")
        else:
            flash("VIRHE: väärä tunnus tai salasana")
            filled = {"username": username}
            return render_template("login.html", filled=filled)



@app.route("/logout")
def logout():
    del session["user_id"]
    flash("Olet kirjautunut ulos.")
    return redirect("/")
