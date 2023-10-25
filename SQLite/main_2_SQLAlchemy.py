import os
from flask import Flask, render_template
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)

app.config['SQLALCHEMY_DATABASE_URI'] =\'sqlite:///' + os.path.join(basedir, 'db/website.db')
ab = SQLAlchemy(app)