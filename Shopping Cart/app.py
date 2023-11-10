import sqlite3

from flask import (Flask, render_template, request, redirect, session, url_for, flash)

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key'

sqldbname = 'db/website.db'

# Search Page
@app.route('/')
def index():
    if 'current_user' in session:
        current_username = session['current_user']['name']
    else:
        current_username = ""
    return render_template('SearchWithCSSDataDBAddToCartTable.html',
                           search_text="", username=current_username)


@app.route('/searchData', methods=['POST'])
def searchData():
    # check if 'username' key exists in the session
    if 'current_user' in session:
        current_username = session['current_user']['name']
    else:
        current_username = ""

    search_text = request.form['searchInput']
    product_table = load_data_from_db(search_text)
    print(product_table)

    return render_template('SearchWithCSSDataDBAddToCartTable.html',
                           search_text=search_text, products=product_table, username=current_username)


def load_data_from_db(search_text):

    if search_text != "":
        # Khai bao bien de tro db
        conn = sqlite3.connect(sqldbname)
        cursor = conn.cursor()
        sqlcommand = "SELECT * FROM storages WHERE model LIKE '%" + search_text + "%'"
        cursor.execute(sqlcommand)
        data = cursor.fetchall()
        conn.close()
        return data


# Add to Cart
@app.route('/cart/add', methods=['POST'])
def add_to_cart():

    # get the product id and quantity from the form
    product_id = request.form["product_id"]
    quantity = int(request.form["quantity"])

    connection = sqlite3.connect(sqldbname)
    cursor = connection.cursor()
    cursor.execute("SELECT model, price FROM storages WHERE id = ?", (product_id,))

    product = cursor.fetchone()
    connection.close()

    # create a dictionary for the product
    product_dict = {
        "id": product_id,
        "name": product[0],
        "price": product[1],
        "quantity": quantity,
        # "picture": product[5],
        # "details": product[8]
    }

    # get the cart from the session or create an empty list
    cart = session.get("cart", [])

    # check if the product is already in the cart
    found = False

    # if the cart contains this product, increase the quantity to one
    for item in cart:
        if item["id"] == product_id:
            item["quantity"] += quantity
            found = True
            break

    # if the cart does not contain this product, add the new product to
    if not found:
        cart.append(product_dict)

    # save the cart back to the session
    session["cart"] = cart

    # print out
    rows = len(cart)
    outputmessage = (f'"Product added to cart successfully!"'
                     f'<br>Current: ' + str(rows) + ' products'
                                                    f'<br>Continue Search! <a href="/">Search Page</a>'
                                                    f'<br>View Shopping Cart! <a href="/view_cart">View Cart</a>')

    return outputmessage


# View Cart
@app.route("/view_cart", methods=['GET', 'POST'])
def view_cart():
    current_cart = []
    if 'cart' in session:
        current_cart = session.get("cart", [])
    if 'current_user' in session:
        current_username = session['current_user']['name']
    else:
        current_username = ""
    return render_template("cart.html", carts=current_cart, username=current_username)


# Update Cart
@app.route('/update_cart', methods=['POST'])
def update_cart():
    # get shopping cart from session
    cart = session.get('cart', [])

    # create a new cart to store updated item
    new_cart = []

    # iterate over each item in the cart
    for product in cart:
        product_id = str(product['id'])
        # if this product has a new quantity in the form data
        if f'quantity-{product_id}' in request.form:
            quantity = int(request.form[f'quantity-{product_id}'])
            # if the quantity is 0 or this is a delete field, skip this product
            if quantity == 0 or f'delete-{product_id}' in request.form:
                continue
            # otherwise, update the quantity of the product
            product['quantity'] = quantity
        # add the product to the new cart
        new_cart.append(product)
    # save the updated cart back to the session
    session['cart'] = new_cart

    # redirect to the shopping cart page
    return redirect(url_for('view_cart'))


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['txt_username']
        password = request.form['txt_password']

        # store 'username' in the session
        obj_user = get_obj_user(username, password)
        if int(obj_user[0]) > 0:
            obj_user = {
                "id": obj_user[0],
                "name": obj_user[1],
                "email": obj_user[2]
            }
            session['current_user'] = obj_user
        return redirect(url_for('index'))
    return render_template('login.html')


def get_obj_user(username, password):
    result = [],

    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    sqlcommand = "SELECT * FROM user WHERE name = ? and password = ?"
    cursor.execute(sqlcommand, (username, password))

    obj_user = cursor.fetchone()
    if len(obj_user) > 0:
        result = obj_user
    conn.close()
    return result


@app.route('/logout')
def logout():
    session.pop('current_user', None)
    # remove 'username' from the session
    return redirect(url_for('index'))


# Proceed cart
@app.route('/proceed_cart', methods=['POST'])
def proceed_cart():
    # retrieve the user ID from the session
    if 'current_user' in session:
        user_id = session['current_user']['id']
        user_email = session['current_user']['email']
    else:
        user_id = 0

    # get the shopping cart from the session
    current_cart = []
    if 'cart' in session:
        shopping_cart = session.get("cart", [])

    # save order information to the "order" table
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()

    # define the order information (create a new form)
    user_address = "User Address"
    user_mobile = "19001000"
    purchase_date = "2023-10-10"
    ship_date = "2023-10-12"
    status = 1

    # insert the order into the "order" table
    cursor.execute('INSERT INTO "order" (user_id, user_email, user_address, user_mobile, purchase_date, ship_date, status) VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (user_id, user_email, user_address, user_mobile, purchase_date, ship_date, status))

    # get the ID of the inserted order
    order_id = cursor.lastrowid
    print(order_id)

    # commit the changes and close the connection
    conn.commit()

    # save order details
    for product in shopping_cart:
        product_id = product['id']
        price = product['price']
        quantity = product['quantity']
        cursor.execute('INSERT INTO order_details (order_id, product_id, price, quantity) VALUES (?, ?, ?, ?)',
                       (order_id, product_id, price, quantity))
    conn.commit()
    conn.close()

    # to remove the current_cart from the session
    if 'cart' in session:
        current_cart = session.pop("cart", [])
    else:
        print("No current_cart in session")

    # call to orders/order_id
    order_url = url_for('orders', order_id=order_id, _external=True)
    return f'Redirecting to order page: <a href="{order_url}">{order_url}</a>'


@app.route('/orders/', defaults={'order_id': None}, methods=['GET'])
@app.route('/orders/<int:order_id>/', methods=['GET'])
def orders(order_id):
    user_id = session.get('current_user', {}).get('id')
    if user_id:
        conn = sqlite3.connect(sqldbname)
        cursor = conn.cursor()
        if order_id is not None:
            cursor.execute('SELECT * FROM "order" WHERE id = ? AND user_id = ?', (order_id, user_id))
            order = cursor.fetchone()
            cursor.execute('SELECT * FROM order_details WHERE order_id = ?', (order_id,))
            order_details = cursor.fetchall()
            conn.close()
            return render_template('order_details.html', order=order, order_details=order_details)
        else:
            cursor.execute('SELECT * FROM "order" WHERE user_id = ?', (user_id,))
            user_orders = cursor.fetchall()
            conn.close()
            return render_template('orders.html', orders=user_orders)
    return redirect(url_for('login'))


db_file = 'db/website.db'


def get_db_connection():
    connection = sqlite3.connect(db_file)
    connection.row_factory = sqlite3.Row
    return connection


@app.route('/editStorages')
def editStorages():
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
        return redirect(url_for('editStorages'))
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
                       'picture=?, price=?, RAM=?, details=? WHERE storage_id=?',
                       (product, brand, rating, model, picture, price, RAM, details))
        connection.commit()
        connection.close()

        flash('Storages updated successfully!', 'success')
        return redirect(url_for('editStorages'))
    return render_template('Admin/Storages/edit.html', storage=storage)


@app.route('/delete/<int:storage_id>', methods=['POST'])
def delete(storage_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM storages WHERE id = ?', (storage_id,))
    connection.commit()
    connection.close()

    flash('Storages deleted successfully!', 'success')
    return redirect(url_for('editStorages'))


if __name__ == '__main__':
    app.run()
