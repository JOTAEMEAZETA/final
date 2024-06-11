import os
from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///inventario.db")


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
    """Show portfolio of stocks"""

    sharesOwned = db.execute(
        "SELECT symbol, SUM(shares) as shares_sum FROM transactions WHERE user_id=? GROUP BY symbol HAVING SUM(shares) > 0", session['user_id'])
    cash = db.execute("SELECT cash FROM users WHERE id=?", session['user_id'])
    cashTotal = cash[0]['cash']
    totalShares = 0

    for row in sharesOwned:
        resultado = lookup(row['symbol'])
        row['actual_price'] = resultado['price']
        row['total_value'] = row['actual_price']*row['shares_sum']
        totalShares += row['total_value']

    grandTotal = totalShares+cashTotal

    return render_template("index.html", shares=sharesOwned, cashTotal=usd(cashTotal), totalShares=usd(totalShares), grandTotal=usd(grandTotal))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # TODO: Add the user's entry into the database
        # Access form data
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 400)

        shares = request.form.get("shares")
        if not shares:
            return apology("must provide number of shares to buy", 403)
        try:
            shares = int(shares)
        except ValueError:
            return apology("must provide number", 400)
        if shares < 1:
            return apology("must provide number", 400)

        searchSymbol = lookup(symbol)
        if not searchSymbol:
            return apology("must provide a valid symbol", 400)

        cashUser = db.execute(
            "SELECT cash FROM users WHERE id = ?", session['user_id']
        )
        precioPagar = shares * searchSymbol['price']
        cashSobra = cashUser[0]['cash']-precioPagar
        if cashSobra < 0:
            return apology("you don't have enough money", 403)

        db.execute(
            "UPDATE users SET cash=? WHERE id = ?", cashSobra, session['user_id'])
        db.execute("INSERT INTO transactions(user_id, symbol, shares, price, date) VALUES (?,?,?,?,?)",
                   session['user_id'], symbol.upper(), shares, precioPagar, datetime.now())

        return redirect("/")

    else:

        # Render register page
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    historial = db.execute(
        "SELECT symbol, shares, price, date FROM transactions WHERE user_id= ?", session['user_id'])
    for row in historial:
        if row['shares'] < 0:
            row['transaction'] = 'SELL'
            row['shares'] = -row['shares']
        else:
            row['transaction'] = 'BUY'

        row['price'] = usd(row['price'])
    return render_template("history.html", historial=historial)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # TODO: Add the user's entry into the database
        # Access form data
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 400)

        searchSymbol = lookup(symbol)
        if not searchSymbol:
            return apology("must provide a valid symbol", 400)
        return render_template("quoted.html", symbol=searchSymbol['symbol'], price=usd(searchSymbol['price']))

    else:

        # Render register page
        return render_template("quote.html")


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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # TODO: Add the user's entry into the database
        # Access form data
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must select symbol", 400)

        shares = request.form.get("shares")
        if not shares:
            return apology("must provide number of shares to buy", 400)
        try:
            shares = int(shares)
        except ValueError:
            return apology("must provide number", 400)
        disponibles = db.execute(
            "SELECT SUM(shares) as shares_sum FROM transactions WHERE user_id=? AND symbol=?", session['user_id'], symbol)
        availableShares = disponibles[0]['shares_sum']
        leftShares = availableShares-shares
        if leftShares < 0:
            return apology("Not enough shares", 400)

        searchSymbol = lookup(symbol)
        if not searchSymbol:
            return apology("must provide a valid symbol", 400)

        cashUser = db.execute(
            "SELECT cash FROM users WHERE id = ?", session['user_id']
        )

        totalVenta = shares * searchSymbol['price']

        cashNuevo = cashUser[0]['cash']+totalVenta

        db.execute(
            "UPDATE users SET cash=? WHERE id = ?", cashNuevo, session['user_id'])
        db.execute("INSERT INTO transactions(user_id, symbol, shares, price, date) VALUES (?,?,?,?,?)",
                   session['user_id'], symbol.upper(), -shares, totalVenta, datetime.now())

        return redirect("/")

    else:
        symbols = db.execute(
            "SELECT symbol, SUM(shares) as shares FROM transactions WHERE user_id=? GROUP BY symbol HAVING SUM(shares)>0", session['user_id'])
        # Render register page
        return render_template("sell.html", symbols=symbols)
