from flask import Flask, jsonify, request, redirect, url_for, render_template, session
from pathlib import Path
from libs import Lib
import sqlite3
import yaml
import os
import datetime


app = Flask(__name__)
# Flask app initialises tables and inputs starting data from yaml files
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
    '''
    Login page,
    Gets user input through login.html page,
    Navigates user to dashboard screen if credentials are correct
    '''
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
    '''
    Dashboard page where user selects functionality they wish to use
    '''
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    return render_template("dashboard.html")

@app.route("/show_desks", methods=["GET"])
def show_desks():
    '''
    Presents all desks in a table
    '''
    db = Lib.get_db_connection()
    rows = db.execute(
        "SELECT * FROM Desks"
    ).fetchall()
    db.close()

    desks = [dict(row) for row in rows]


    return render_template("desks.html", desks=desks)

@app.route("/add_desks", methods=["POST", "GET"])
def add_desks():
    if request.method == "GET":
        return render_template("add_desks.html")

    db = Lib.get_db_connection()
    with db:
        db.execute(
            "INSERT INTO Desks (name, location, floor) VALUES ( ?, ?, ?)",
            [request.form["name"],
             request.form["location"],
             request.form["floor"],
             ]
            )
    db.close()

    return redirect(url_for("dashboard"))
    

@app.route("/del_desks", methods=["POST", "GET"])
def del_desks():
    if request.method == "GET":
        return render_template("del_desks.html")

    db = Lib.get_db_connection()
    with db:
        db.execute(
            "DELETE FROM Desks WHERE name = ? AND location = ? AND floor = ?",
            [request.form["name"],
             request.form["location"],
             request.form["floor"],
             ]
            )
    db.close()

    return redirect(url_for("dashboard"))

@app.route("/show_bookings", methods=["GET"])
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

@app.route("/del_booking")

@app.route("/add_user", methods=["POST", "GET"])
def add_user():
    if request.method == "GET":
        return render_template("add_user.html")

    values = [
        request.form["username"],
        request.form["password"],
        request.form["f_name"],
        request.form["s_name"],
        request.form["email"]
    ]

    db = Lib.get_db_connection()
    with db:
        db.execute(
            f"INSERT INTO Users (username, password, f_name, s_name, email) VALUES ( ?, ?, ?, ?, ?)",
            values
        )
    db.close()

    return redirect(url_for("dashboard"))

@app.route("/del_user", methods=["POST", "GET"])
def del_user():
    if request.method == "GET":
        return render_template("del_user.html")

    db = Lib.get_db_connection()
    with db:
        db.execute(
            "DELETE FROM Users WHERE username = ?",
            [request.form["username"]]
            )
    db.close()

    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)