from flask import Flask, jsonify, request, redirect, url_for, render_template, session
from pathlib import Path
from libs import Lib
import sqlite3
import yaml
import os
import datetime

app = Flask(__name__)
Lib.init_db()
Lib.init_all_data()
app.secret_key= "dev-secret"

@app.route("/")
def index():
    '''
    After initialisation the user is redirected to the login page
    '''
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    db = Lib.get_db_connection()
    user = db.execute(
        "SELECT * FROM Users WHERE username = ?",
        (username,)
    ).fetchone()
    db.close()

    if user is None or user["password"] != password:
        return render_template("login.html", error="Invalid username or password")
    
    session["user_id"] = user["user_id"]
    
    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    return render_template("dashboard.html")

@app.route("/desks", methods=["GET"])
def show_desks():
    db = Lib.get_db_connection()
    rows = db.execute(
        "SELECT * FROM Desks"
    ).fetchall()
    db.close()

    desks = [dict(row) for row in rows]


    return render_template("desks.html", desks=desks)

@app.route("/bookings")
def show_bookings():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    db = Lib.get_db_connection()
    rows = db.execute(
        "SELECT * FROM Bookings WHERE user_id = ?",
        (session["user_id"],)
    ).fetchall()
    db.close()

    bookings = [dict(row) for row in rows]


    return render_template("bookings.html", bookings=bookings)

@app.route("/make_booking", methods=["POST", "GET"])
def make_booking():
    if request.method == "GET":
        return render_template("make_booking.html")

    values = [session["user_id"],
              request.form["desk_id"],
              request.form["start_date"],
              request.form["end_date"],
              True,
              (datetime.datetime.now()).strftime("%x")
              ]

    db = Lib.get_db_connection()
    with db:
        db.execute(
            f"INSERT INTO Bookings (user_id, desk_id, start_date, end_date, active, created) VALUES ( ?, ?, ?, ?, ?, ?)",
            values
        )
    db.close()

    return redirect(url_for("show_bookings"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)