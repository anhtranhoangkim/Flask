from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

sqldbname = 'db/website.db'

@app.route('/user', methods=['GET'])
def get_users():
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()

    cur.execute('SELECT * FROM user')
    users = cur.fetchall()

    users_list = []
    for user in users:
        users_list.append({'id': user[0], 'name': user[1], 'email': user[2], 'password': user[3]})
    return jsonify(users_list)


@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()

    cur.execute('SELECT * FROM user WHERE id = ?', (id,))
    user = cur.fetchone()

    if user:
        user_dict = {'id': user[0], 'name': user[1], 'email': user[2], 'password': user[3]}
        return jsonify(user_dict)
    else:
        return 'User not found'


@app.route('/users', methods=['POST'])
def add_user():
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()

    user_name = request.json.get('name')
    user_email = request.json.get('email')
    user_password = request.json.get('password')

    if user_name and user_email and user_password:
        cur.execute('INSERT INTO user (name, email, password)'
                    'VALUES (?, ?, ?)', (user_name, user_email, user_password))
        conn.commit()
        user_id = cur.lastrowid
        return jsonify({'id': user_id})
    else:
        return 'Required', 400




if __name__ == '__main__':
    app.run(debug=True)
