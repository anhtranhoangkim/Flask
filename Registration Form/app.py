from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key'


@app.route('/')
def index():
    return render_template('registration.html',
                           username_error="",
                           password_error="",
                           registration_success="")


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    username_error = ""
    password_error = ""

    # server-side validation
    if not username:
        username_error = "Username is required."
    if not password:
        password_error = "Password is required."
    if username_error or password_error:
        return render_template('registration.html',
                               username_error=username_error,
                               password_error=password_error,
                               registration_success="")

    # perform registration logic here (e.g, save to a database)
    # for this example, we'll just print the values
    registration_success = f'Registration Successful! Registration: Username - {username}, Password - {password}'
    return render_template('registration.html',
                           username_error="", password_error="",
                           registration_success=registration_success)

if __name__ == '__main__':
    app.run()
