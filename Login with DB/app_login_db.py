import sqlite3

from flask import (Flask, render_template, request, redirect, session, url_for)

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def index():
    if 'username' in session:
        username = session['username']

        return (f'Hello, {username}!'
                f'<a href="/logout">Logout</a>')
    return 'Welcome! <a href="/login">Login</a>'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if check_exists(username, password):
            session['username'] = username
        return redirect(url_for('index'))

    return render_template('login.html')


def check_exists(username, password):
    result = False

    sqldbname = 'db/website.db'
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()

    sqlcommand = "SELECT * FROM user WHERE name = '" + username + "' and password = '" + password + "'"
    cursor.execute(sqlcommand)
    data = cursor.fetchall()
    print(type(data))

    if len(data) > 0:
        result = True

    conn.close()
    return result


@app.route('/logout')
def logout():
    session.pop('username', None)
    # remove 'username' from the session
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
