import sqlite3
from flask import g

def connect():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    return connection

def execute(sql, parameters=[]):
    connection = connect()
    result = connection.execute(sql, parameters)
    connection.commit()
    g.last_insert_id = result.lastrowid
    connection.close()

def query(sql, parameters=[]):
    connection = connect()
    result = connection.execute(sql, parameters).fetchall()
    connection.close()
    return result

def get_last_insert_id():
    return g.last_insert_id
