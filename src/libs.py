from flask import Flask, jsonify, request
from pathlib import Path
import sqlite3
import yaml
import os

class Lib():
    @classmethod
    def get_db_connection(self):
        '''
        This is a method that connects to the database and returns the connection
        '''
        conn = sqlite3.connect("bookings.db")
        conn.row_factory = sqlite3.Row

        return conn

    @classmethod
    def init_db(self):
        '''
        This is a method that initialises all tables in the database 
        '''
        db = self.get_db_connection()
        with db:
            # Create the desks table if it doesnt already exist
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS Desks(
                desk_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                location TEXT NOT NULL,
                floor TEXT NOT NULL)
                """)
            # Create the users table if it doesnt already exist
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS Users(
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                f_name TEXT NOT NULL,
                s_name TEXT NOT NULL,
                email TEXT NOT NULL)
                """
            )
            # Create the bookings table if it doesnt already exist
            db.execute(
                    """
                    CREATE TABLE IF NOT EXISTS Bookings(
                    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    desk_id INTEGER,
                    start_date TEXT,
                    end_date TEXT,
                    created DATETIME,
                    FOREIGN KEY (user_id) REFERENCES Users(user_id),
                    FOREIGN KEY (desk_id) REFERENCES Desks(desk_id))
                    """
                )
        db.close()
    @classmethod
    def init_db_values(self, db, path, table_name, columns):
        '''
        This is a method that inputs all the starting data values from a single yaml file
        '''
        existing = db.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        if existing == 0:
            with open(path) as f:
                data = yaml.safe_load(f)
            placeholders = ", ".join(["?"] * len(columns))
            col_names = ", ".join(columns)

            values = [
                tuple(entry[col] for col in columns)
                for entry in data
            ]
            db.executemany(
                f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})",
                values
            )
    
    @classmethod
    def init_all_data(self):
        '''
        This method connects to the database, and populates the users and desks tables with data from the yaml files associated
        '''
        db = self.get_db_connection()
        with db:
            self.init_db_values(
                db,
                "Data/users.yaml",
                "Users",
                ["username", "password", "f_name", "s_name", "email"]
            )

            self.init_db_values(
                db,
                "Data/desks.yaml",
                "Desks",
                ["name", "location", "floor"]
            )
        db.close()
    
    @classmethod
    def get_desk_id(self, desk_name):
        db = self.get_db_connection()
        with db:
            booking = db.execute(
                "SELECT desk_id FROM Desks WHERE name = ?",
                (desk_name,)
            ).fetchone()
        db.close()
        if booking is None:
            return None
        
        return booking["desk_id"]
