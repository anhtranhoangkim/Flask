from flask import Flask, render_template, request, url_for
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Kim Anh'

# if not exists, then create
db_file = 'db/website.db'

def get_db_connection():
    connection = sqlite3.connect(db_file)
    connection.row_factory = sqlite3.Row
    return connection

@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM storages')
    storages = cursor.fetchall()
    connection.close()
    return render_template('Admin/Storages/index.html', storages=storages)