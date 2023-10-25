from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key'
sqldbname = 'db/website.db'


@app.route('/')
def index():
    return render_template('registration_db.html',
                           username_error="",
                           email_error="",
                           password_error="",
                           registration_success="")


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    username_error = ""
    email_error = ""
    password_error = ""

    # server-side validation
    if not username:
        username_error = "Username is required."
    if not password:
        password_error = "Password is required."
    if username_error or password_error:
        return render_template('registration_db.html',
                               username_error=username_error,
                               password_error=password_error,
                               registration_success="")

    # perform registration logic here (e.g, save to a database)
    newid = SaveToDB(username, email, password)
    stroutput = f'Registered: Username - {username}, Password - {password}'
    registration_success = f'Registration Successful! with id = ' + str(newid)
    print(registration_success + stroutput)
    return render_template('registration_db.html',
                           username_error="", password_error="",
                           registration_success=registration_success + stroutput)


def SaveToDB(name, email, password):
    # get max from DB
    id_max = generateID()
    if id_max > 0:
        id_max = id_max + 1
    else:
        id_max = 1
    print(id_max)

    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()

    # insert the user into the users table using paramterized query
    cur.execute("INSERT INTO user(id, name, email, password) VALUES (?, ?, ?, ?)",
                   (id_max, name, email, password))

    # commit the changes
    conn.commit()

    # close the connection
    conn.close()

    # return a success message
    return id_max

def generateID():
    max_id = 0
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()

    sqlcommand = "SELECT Max(id) from user"
    cursor.execute(sqlcommand)
    max_id = cursor.fetchone()[0]
    return max_id

if __name__ == '__main__':
    app.run()
