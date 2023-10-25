from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
sqldbname = 'db/website.db'


@app.route('/')
def index():
    # connect to the SQLite database
    conn = sqlite3.connect(sqldbname)
    # create a cursor object to execute SQL queries
    cursor = conn.cursor()
    # execute an SQL query to fetch data
    cursor.execute('SELECT * FROM user')
    data = cursor.fetchall()
    # close the database connection
    conn.close()
    return render_template('index.html', table=data)


if __name__ == '__main__':
    app.run(debug=True)
