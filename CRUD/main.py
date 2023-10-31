from flask import Flask, render_template, request, url_for, flash, redirect
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


@app.route('/editStorages')
def index():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM storages')
    storages = cursor.fetchall()
    connection.close()
    return render_template('Admin/Storages/index.html', storages=storages)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        product = request.form['product']
        brand = request.form['brand']
        rating = request.form['rating']
        model = request.form['model']
        picture = request.form['picture']
        price = request.form['price']
        RAM = request.form['RAM']
        details = request.form['details']

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO storages (product, brand, rating, model, picture, price, RAM, details) '
                       'VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (product, brand, rating, model, picture, price, RAM, details))
        connection.commit()
        connection.close()

        flash('Storages added successfully', 'success')
        return redirect(url_for('index'))
    return render_template('Admin/Storages/add.html')


@app.route('/edit/<int:storage_id>', methods=['GET', 'POST'])
def edit(storage_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM storages WHERE id = ?', (storage_id,))
    storage = cursor.fetchone()
    connection.close()

    if request.method == 'POST':
        product = request.form['product']
        brand = request.form['brand']
        rating = request.form['rating']
        model = request.form['model']
        picture = request.form['picture']
        price = request.form['price']
        RAM = request.form['RAM']
        details = request.form['details']

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('UPDATE storages SET product=?, brand=?, rating=?, model=?, '
                       'picture=?, price=?, RAM=?, details=?, storage_id=?',
                       (product, brand, rating, model, picture, price, RAM, details))
        connection.commit()
        connection.close()

        flash('Storages updated successfully!', 'success')
        return redirect(url_for('index'))


@app.route('/delete/<int:storage_id>', methods=['POST'])
def delete(storage_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM storages WHERE id = ?', (storage_id,))
    connection.commit()
    connection.close()

    flash('Storages deleted successfully!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()







