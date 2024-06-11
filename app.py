import os
from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, url_for, send_from_directory, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from helpers import apology, login_required, lookup, usd

# Configure application
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = { 'pdf', 'jpg', 'jpeg'}
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///inventario.db")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show Areas"""

    areas = db.execute("SELECT * FROM areas")

    return render_template("areas.html", areas=areas)

@app.route("/new_area", methods=["GET", "POST"])
@login_required
def new_areas():
     if request.method == "POST":
        # TODO: Add the user's entry into the database
        # Access form data
        nombre = request.form.get("nombre")
        if not nombre:
            return apology("must provide nombre", 400)

        tag = request.form.get("tag")
        if not tag:
            return apology("must provide tag", 400)
        
        ubicacion = request.form.get("ubicacion")
        # if not ubicacion:
        #     return apology("must provide ubicacion", 400)
        
        descripcion = request.form.get("descripcion")
        # if not descripcion:
        #     return apology("must provide descripcion", 400)
        
        db.execute("INSERT INTO areas(nombre, tag, ubicacion, descripcion) VALUES (?,?,?,?)",
                   nombre, tag, ubicacion, descripcion)

        return redirect("/")
     else:
        return render_template("new_area.html")

@app.route("/areas", methods=["GET", "POST"])
@login_required
def areas():
    """Buy shares of stock"""
    if request.method == "POST":
        # TODO: Add the user's entry into the database
        # Access form data

        return redirect("/")

    else:

        id_area = request.args.get("id")
        if not id_area:
            return apology("must provide id", 400)
        equipos = db.execute(
        "SELECT * FROM equipos WHERE area_id= ?", id_area)

        # Render register page
        return render_template("equipos.html", equipos=equipos, id_area=id_area)


@app.route("/editar_area",methods=["GET", "POST"])
@login_required
def editar_area():
    if request.method == "POST":
        # TODO: Add the user's entry into the database
        # Access form data
        id_area = request.form.get("id")
        if not id_area:
            return apology("must provide id", 400)

        nombre = request.form.get("nombre")
        if not nombre:
            return apology("must provide nombre", 400)

        tag = request.form.get("tag")
        if not tag:
            return apology("must provide tag", 400)
        
        ubicacion = request.form.get("ubicacion")
      
        
        descripcion = request.form.get("descripcion")
       
        
        db.execute("UPDATE areas SET nombre=?, tag=?, ubicacion=?, descripcion=? WHERE id=?",
                   nombre, tag, ubicacion, descripcion, id_area)

        return redirect("/")
    
    else:

        id_area = request.args.get("id")
        if not id_area:
                return apology("must provide id", 400)
        area = db.execute(
            "SELECT * FROM areas WHERE id= ?", id_area)
        return render_template("edit_area.html", area=area[0])


@app.route("/borrar_area")
@login_required
def borrar_area():
        
        id_area = request.args.get("id")
        if not id_area:
                return apology("must provide id", 400)
        db.execute(
            "DELETE FROM areas WHERE id= ?", id_area)
        return redirect("/")


@app.route("/new_equipo", methods=["GET", "POST"])
@login_required
def new_equipo():
     if request.method == "POST":
        # TODO: Add the user's entry into the database
        # Access form data
        area_id = request.form.get("area_id")
        if not area_id:
            return apology("must provide area_id", 400)

        nombre = request.form.get("nombre")
        if not nombre:
            return apology("must provide nombre", 400)

        tag = request.form.get("tag")
        if not tag:
            return apology("must provide tag", 400)
        
        tipo_equipo = request.form.get("tipo_equipo")
        if not tipo_equipo:
            return apology("must provide tipo de equipo", 400)
        
        marca = request.form.get("marca")
        if not marca:
            return apology("must provide marca", 400)
        
        modelo = request.form.get("modelo")
        if not modelo:
            return apology("must provide modelo", 400)
        
        
        descripcion = request.form.get("descripcion")
        # if not descripcion:
        #     return apology("must provide descripcion", 400)

        mantenimiento1 = request.form.get("mantenimiento1")

        mantenimiento2 = request.form.get("mantenimiento2")

        mantenimiento = request.form.get("mantenimiento2")

        proveedor = request.form.get("proveedor")

        if 'archivo_jpg' not in request.files:
            return apology("must provide jpg", 400)
        archivo_jpg = request.files["archivo_jpg"]
        if archivo_jpg and allowed_file(archivo_jpg.filename):
            filename1 = secure_filename(archivo_jpg.filename)      
        
        if 'archivo_pdf' not in request.files:
            return apology("must provide pdf", 400)
        archivo_pdf = request.files["archivo_pdf"]
        if archivo_pdf and allowed_file(archivo_pdf.filename):
            filename2 = secure_filename(archivo_pdf.filename)

        archivo_jpg.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))     
        archivo_pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
        
        db.execute("INSERT INTO equipos(area_id, nombre, tag, tipo_equipo, marca, modelo, descripcion, archivo_jpg, archivo_pdf, fecha_mantenimiento_1, fecha_mantenimiento_2, mantenimiento, proveedor) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                   area_id,nombre, tag, tipo_equipo, marca, modelo, descripcion, filename1, filename2, mantenimiento1, mantenimiento2, mantenimiento, proveedor)

        return redirect("/areas?id="+area_id)
     else:
        id_area = request.args.get("id")
        if not id_area:
                return apology("must provide id", 400)
        return render_template("new_equipo.html",area_id=id_area)

@app.route("/equipos", methods=["GET", "POST"])
@login_required
def equipos():
    """Buy shares of stock"""
    if request.method == "POST":
        # TODO: Add the user's entry into the database
        # Access form data

        return redirect("/")

    else:

        id_equipo = request.args.get("id")
        if not id_equipo:
            return apology("must provide id", 400)
        componentes = db.execute(
        "SELECT * FROM componentes WHERE equipo_id= ?", id_equipo)

        # Render register page
        return render_template("componentes.html", componentes=componentes, id_equipo=id_equipo)


@app.route("/editar_equipo",methods=["GET", "POST"])
@login_required
def editar_equipo():
    if request.method == "POST":
        # TODO: Add the user's entry into the database
        # Access form data
        equipo_id = request.form.get("id")
        if not equipo_id:
            return apology("must provide id", 400)

        area_id = request.form.get("area_id")
        if not area_id:
            return apology("must provide area_id", 400)

        nombre = request.form.get("nombre")
        if not nombre:
            return apology("must provide nombre", 400)

        tag = request.form.get("tag")
        if not tag:
            return apology("must provide tag", 400)
        
        tipo_equipo = request.form.get("tipo_equipo")
        if not tipo_equipo:
            return apology("must provide tipo de equipo", 400)
        
        marca = request.form.get("marca")
        if not marca:
            return apology("must provide marca", 400)
        
        modelo = request.form.get("modelo")
        if not modelo:
            return apology("must provide modelo", 400)
        
        mantenimiento1 = request.form.get("mantenimiento1")

        mantenimiento2 = request.form.get("mantenimiento2")

        mantenimiento = request.form.get("mantenimiento")

        proveedor = request.form.get("proveedor")
        
        
        descripcion = request.form.get("descripcion")
        # if not descripcion:
        #     return apology("must provide descripcion", 400)

        filename1 = request.form.get("archivo_jpg")

        filename2 = request.form.get("archivo_pdf")

        if 'archivo_jpg' in request.files:
            archivo_jpg = request.files["archivo_jpg"]
            if archivo_jpg and allowed_file(archivo_jpg.filename):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
                filename1 = secure_filename(archivo_jpg.filename)
                archivo_jpg.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))      
        
        if 'archivo_pdf' in request.files:   
            archivo_pdf = request.files["archivo_pdf"]
            if archivo_pdf and allowed_file(archivo_pdf.filename):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
                filename2 = secure_filename(archivo_pdf.filename)
                archivo_pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))

        
        db.execute("UPDATE equipos SET area_id=?, nombre=?, tag=?, tipo_equipo=?, marca=?, modelo=?, descripcion=?, archivo_jpg=?, archivo_pdf=?, fecha_mantenimiento_1=?, fecha_mantenimiento_2=?, mantenimiento=?, proveedor=? WHERE id=?",
                    area_id, nombre, tag, tipo_equipo, marca, modelo, descripcion, filename1, filename2,mantenimiento1, mantenimiento2, mantenimiento, proveedor, equipo_id)

        return redirect("/areas?id="+area_id)
    
    else:

        id_equipo = request.args.get("id")
        if not id_equipo:
                return apology("must provide id", 400)
        equipo = db.execute(
            "SELECT * FROM equipos WHERE id= ?", id_equipo)
        return render_template("edit_equipo.html", equipo=equipo[0])


@app.route("/borrar_equipo")
@login_required
def borrar_equipo():
        
        id_equipo = request.args.get("id")
        if not id_equipo:
                return apology("must provide id", 400)
        db.execute(
            "DELETE FROM equipos WHERE id= ?", id_equipo)
        return redirect("/")


@app.route("/new_componente", methods=["GET", "POST"])
@login_required
def new_componente():
     if request.method == "POST":
        # TODO: Add the user's entry into the database
        # Access form data
        equipo_id = request.form.get("equipo_id")
        if not equipo_id:
            return apology("must provide equipo_id", 400)

        nombre = request.form.get("nombre")
        if not nombre:
            return apology("must provide nombre", 400)

        tag = request.form.get("tag")
        if not tag:
            return apology("must provide tag", 400)
        
        tipo_componente = request.form.get("tipo_componente")
        if not tipo_componente:
            return apology("must provide tipo de componente", 400)
        
        marca = request.form.get("marca")
        if not marca:
            return apology("must provide marca", 400)
        
        modelo = request.form.get("modelo")
        if not modelo:
            return apology("must provide modelo", 400)
        
        
        descripcion = request.form.get("descripcion")
        # if not descripcion:
        #     return apology("must provide descripcion", 400)

        mantenimiento1 = request.form.get("mantenimiento1")

        mantenimiento2 = request.form.get("mantenimiento2")

        mantenimiento = request.form.get("mantenimiento")

        proveedor = request.form.get("proveedor")

        if 'archivo_jpg' not in request.files:
            return apology("must provide jpg", 400)
        archivo_jpg = request.files["archivo_jpg"]
        if archivo_jpg and allowed_file(archivo_jpg.filename):
            filename1 = secure_filename(archivo_jpg.filename)      
        
        if 'archivo_pdf' not in request.files:
            return apology("must provide pdf", 400)
        archivo_pdf = request.files["archivo_pdf"]
        if archivo_pdf and allowed_file(archivo_pdf.filename):
            filename2 = secure_filename(archivo_pdf.filename)

        archivo_jpg.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))     
        archivo_pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
        
        db.execute("INSERT INTO componentes(equipo_id, nombre, tag, tipo_componente, marca, modelo, descripcion, archivo_jpg, archivo_pdf, fecha_mantenimiento_1, fecha_mantenimiento_2, mantenimiento, proveedor) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                   equipo_id,nombre, tag, tipo_componente, marca, modelo, descripcion, filename1, filename2, mantenimiento1, mantenimiento2, mantenimiento, proveedor)

        return redirect("/equipos?id="+equipo_id)
     else:
        id_equipo = request.args.get("id")
        if not id_equipo:
                return apology("must provide id", 400)
        return render_template("new_componente.html",equipo_id=id_equipo)


@app.route("/editar_componente",methods=["GET", "POST"])
@login_required
def editar_componente():
    if request.method == "POST":
        # TODO: Add the user's entry into the database
        # Access form data
        componente_id = request.form.get("id")
        if not componente_id:
            return apology("must provide id", 400)

        equipo_id = request.form.get("equipo_id")
        if not equipo_id:
            return apology("must provide equipo_id", 400)

        nombre = request.form.get("nombre")
        if not nombre:
            return apology("must provide nombre", 400)

        tag = request.form.get("tag")
        if not tag:
            return apology("must provide tag", 400)
        
        tipo_componente = request.form.get("tipo_componente")
        if not tipo_componente:
            return apology("must provide tipo de componente", 400)
        
        marca = request.form.get("marca")
        if not marca:
            return apology("must provide marca", 400)
        
        modelo = request.form.get("modelo")
        if not modelo:
            return apology("must provide modelo", 400)
        
        
        descripcion = request.form.get("descripcion")
        # if not descripcion:
        #     return apology("must provide descripcion", 400)

        mantenimiento1 = request.form.get("mantenimiento1")

        mantenimiento2 = request.form.get("mantenimiento2")

        mantenimiento = request.form.get("mantenimiento")

        proveedor = request.form.get("proveedor")

        filename1 = request.form.get("archivo_jpg")

        filename2 = request.form.get("archivo_pdf")

        if 'archivo_jpg' in request.files:
            archivo_jpg = request.files["archivo_jpg"]
            if archivo_jpg and allowed_file(archivo_jpg.filename):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
                filename1 = secure_filename(archivo_jpg.filename)
                archivo_jpg.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))      
        
        if 'archivo_pdf' in request.files:   
            archivo_pdf = request.files["archivo_pdf"]
            if archivo_pdf and allowed_file(archivo_pdf.filename):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
                filename2 = secure_filename(archivo_pdf.filename)
                archivo_pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
       
        
        db.execute("UPDATE componentes SET equipo_id=?, nombre=?, tag=?, tipo_componente=?, marca=?, modelo=?, descripcion=?, archivo_jpg=?, archivo_pdf=?, fecha_mantenimiento_1=?, fecha_mantenimiento_2=?, mantenimiento=?, proveedor=? WHERE id=?",
                    equipo_id, nombre, tag, tipo_componente, marca, modelo, descripcion, filename1, filename2, mantenimiento1, mantenimiento2, mantenimiento, proveedor, componente_id)

        return redirect("/equipos?id="+equipo_id)
    
    else:

        id_componente = request.args.get("id")
        if not id_componente:
                return apology("must provide id", 400)
        componente = db.execute(
            "SELECT * FROM componentes WHERE id= ?", id_componente)
        return render_template("edit_componente.html", componente=componente[0])


@app.route("/borrar_componente")
@login_required
def borrar_componente():
        
        id_componente = request.args.get("id")
        if not id_componente:
                return apology("must provide id", 400)
        db.execute(
            "DELETE FROM componentes WHERE id= ?", id_componente)
        return redirect("/")

@app.route("/componentes_all")
@login_required
def componentes_all():
        componentes = db.execute(
        "SELECT * FROM componentes")
        # Render register page
        return render_template("componentes_all.html", componentes=componentes)

@app.route("/equipos_all")
@login_required
def equipos_all():
        equipos = db.execute(
        "SELECT * FROM equipos")
        # Render register page
        return render_template("equipos_all.html", equipos=equipos)


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")




@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # TODO: Add the user's entry into the database

        # Access form data
        username = request.form.get("username")
        if not username:
            return apology("must provide username", 400)

        usernameCheck = db.execute("SELECT username FROM users WHERE username=?", username)
        if len(usernameCheck) == 1:
            return apology("that username already exists", 400)

        password = request.form.get("password")
        if not password:
            return apology("must provide password", 400)

        confirmation = request.form.get("confirmation")
        if not confirmation:
            return apology("must provide confirmation", 400)

        if password != confirmation:
            return apology("confirmation and password must be the same", 400)

        passwordHash = generate_password_hash(password, method='pbkdf2', salt_length=16)

        # Insert data into database
        db.execute(
            "INSERT INTO users (username, hash) VALUES(?, ?)", username, passwordHash)

        return redirect("/login")

    else:

        # Render register page
        return render_template("register.html")
