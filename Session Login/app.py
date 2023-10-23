from flask import (Flask, render_template, request, redirect, session, url_for)

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def index():
    # check if 'username' key exists in the session
    if 'username' in session:
        username = session['username']

        return (f'Hello, {username}!'
                f'<a href="/logout">Logout</a>')
    return 'Welcome! <a href="/login">Login</a>'


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if session finds 'username' in the session, redirects to 'index'
    if request.method == 'POST':
        username = request.form['username']
        # store 'username' in the session
        session['username'] = username
        return redirect(url_for('index'))
    # default is 'login'
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    # remove 'username' from the session
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
