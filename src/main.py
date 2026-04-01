from flask import Flask, jsonify, request
from pathlib import Path
import sqlite3
import yaml
import os

def get_db_connection():
    conn = sqlite3.connect('desks.db')
    conn.row_factory = sqlite3.Row

    return conn

def init_db():
    db = get_db_connection()
    with db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS desks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL)
            """
        )

app = Flask(__name__)
init_db()
def init_desks():
    path = Path(os.getcwd() + "/Data/desks.yaml")
    with open(path) as f:
        return yaml.full_load(f)


desks = init_desks()

@app.route('/desks', methods=["GET"])
def get_desks():
    return jsonify(desks)

@app.route('/books', methods=["POST"])
def add_desk():
    desk_data = request.get_json()
    db = get_db_connection()
    db.execute('INSERT INTO DESKS (name, location) VALUES (?, ?)', (desk_data['name'], desk_data['location']))
    db.execute
    new_desk_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
    db.close

    return jsonify({"id": new_desk_id, **desk_data}), 201

@app.route('/desks/<int:desk_id>', methods=['GET'])
def get_desk(desk_id):
    for desk in desks:
        if desk['id'] == desk_id:
            return jsonify(desk)

    return jsonify({'error':"Book not found"}), 404 

app.run(debug=True)