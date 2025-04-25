import sqlite3, secrets, math, markupsafe
from flask import Flask
from flask import abort, flash, make_response, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db, config, events, users


app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    murderers = users.get_top5()
    if "user_id" in session:
        username=session["username"]
    else: username=None
    return render_template("index.html", murderers=murderers, username=username)

@app.route("/events")
def ownevents():
    #need to pageniate
    user_id = session["user_id"]
    outgoing_events = events.get_outgoing_events(user_id)
    incoming_events = events.get_incoming_events(user_id)
    return render_template("ownevents.html", incoming_events=incoming_events, outgoing_events=outgoing_events)

@app.route("/murders")
@app.route("/murders/<int:page>")
def murders(page=1):
    page_size = 10
    murder_count = events.get_murder_count()
    page_count = math.ceil(murder_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/murders")
    if page > page_count:
        return redirect("/murders/" + str(page_count))
    murders=events.get_murders(page, page_size)
    return render_template("murders.html", page=page, page_count=page_count, murders=murders)

@app.route("/search")
@app.route("/search/<int:page>")
def search(page=1):
    query = request.args.get("query")
    search_count=events.get_search_count(query)
    page_size = 10
    page_count = math.ceil(search_count / page_size)
    page_count = max(page_count, 1)
    if page < 1:
        page=1
    if page > page_count:
        page-=1
    results = events.search(query, page, page_size) if query else []
    return render_template("search.html", query=query, page=page, page_count=page_count, results=results)

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
    flash("Tapahtuma luotu! Voit halutessasi antaa lisätietoja tapahtumasta.")
    return redirect("/event/" + str(event_id) + "/edit")

@app.route("/event/<int:event_id>")
def show_event(event_id):
    event = events.get_event(event_id)
    if not event: 
        abort(404)
    if "user_id" in session:
        user_id = session["user_id"]
    else: user_id = None
    if event[4] == 0:
        require_login()
        if user_id != event[1] and user_id != event[2]:
            abort(403)
    details = events.get_details(event_id)
    return render_template("eventpage.html", event=event, user_id = user_id, details = details)

@app.route("/event/<int:event_id>/edit")
def editpage(event_id):
    require_login()
    event=events.get_event(event_id)
    details=events.get_details(event_id)
    weapontypes = events.get_weapontypes()
    if not event: 
        abort(404)
    return render_template("editevent.html", event=event, details=details, weapontypes=weapontypes)

@app.route("/event/<int:event_id>/edited", methods=["POST"])
def edited(event_id):
    require_login()
    check_csrf()
    zip = request.form["zip"]
    weapontype = request.form["weapontype"]
    killerstory = request.form["killerstory"]
    if len(killerstory) > 200:
        abort(403)
    events.edit_event(event_id, zip, weapontype, killerstory)
    return redirect("/event/"+ str(event_id))

@app.route("/event/<int:event_id>/confirm", methods=["POST"])
def confirm(event_id): 
    require_login()
    check_csrf()   
    events.confirm(event_id, request.form["confirm"])    
    return redirect("/event/"+ str(event_id))

@app.route("/event/<int:event_id>/targetstory", methods=["POST"])
def targetstory(event_id):
    require_login()
    check_csrf()
    targetstory = request.form["targetstory"]
    if len(targetstory) > 200:
        abort(403)
    events.edit_targetstory(event_id, targetstory)
    return redirect("/event/"+ str(event_id))

@app.template_filter()
def show_lines(info):
    info = str(markupsafe.escape(info))
    info = info.replace("\n", "<br />")
    return markupsafe.Markup(info)

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

@app.route("/user/<string:username>")
def show_user(username):
    user_id = users.get_user_id(username)
    user = users.get_user(user_id)
    if not user:
        abort(404)
    murders = events.get_user_murders(user[0])
    deaths = events.get_user_deaths(user[0])
    murder_count = events.get_user_murder_count(user[0])
    death_count = events.get_user_death_count(user[0])
    return render_template("user.html", user=user, murders=murders, deaths=deaths, murder_count=murder_count, death_count=death_count)

@app.route("/user/<string:username>/murders")
@app.route("/user/<string:username>/murders/<int:page>")
def show_user_murders(username, page=1):
    page_size = 10
    user_id = users.get_user_id(username)

    murder_count = events.get_user_murder_count(user_id)
    page_count = math.ceil(murder_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/user/" + username + "/murders")
    if page > page_count:
        return redirect("/user/" + username + "/murders/" + str(page_count))
    murders=events.get_user_murders(user_id, page, page_size)
    return render_template("usermurders.html", page=page, page_count=page_count, murders=murders, username=username)


@app.route("/user/<string:username>/deaths")
@app.route("/user/<string:username>/deaths/<int:page>")
def show_user_deaths(username, page=1):
    page_size = 10
    user_id = users.get_user_id(username)
    death_count = events.get_user_death_count(user_id)
    page_count = math.ceil(death_count / page_size)
    page_count = max(page_count, 1)
    if page < 1:
        return redirect("/user/" + username  +"/deaths")
    if page > page_count:
        return redirect("/user/" + username + "/deaths/" + str(page_count))
    deaths=events.get_user_deaths(user_id, page, page_size)
    return render_template("userdeaths.html", page=page, page_count=page_count, deaths=deaths, username=username)

@app.route("/add_image", methods=["GET", "POST"])
def add_image():
    require_login()
    if request.method == "GET":
        return render_template("add_image.html")
    if request.method == "POST":
        check_csrf()  
        file = request.files["image"]
        if not file.filename.endswith(".jpg"):
            flash("VIRHE: väärä tiedostomuoto")
            return redirect("/add_image")
        image=file.read()
        if len(image) > 100 * 1024:
            flash("VIRHE: liian suuri kuva")
            return redirect("/add_image")
        user_id = session["user_id"]
        username = session["username"]
        users.update_image(user_id, image)
        flash("Kuvan lisäys onnistui!")
        return redirect("/user/" + username)

@app.route("/image/<string:username>")
def show_image(username):
    user_id = users.get_user_id(username)
    image = users.get_image(user_id)
    if not image:
        abort(404)
    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/register")
def register():
    if request.method == "GET":
        return render_template("register.html", filled={})


@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    if not username or len(username) > 20:
        flash("VIRHE: Käyttäjätunnus on virheellinen!")
        filled = {"username": username}
        return render_template("register.html", filled=filled)
    password1 = request.form["password1"]
    if not password1 or len(password1) > 20:
        flash("VIRHE: Salasana on virheellinen!")
        filled = {"username": username}
        return render_template("register.html", filled=filled)
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
