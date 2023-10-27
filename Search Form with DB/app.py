import sqlite3

from flask import Flask, request, render_template

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return render_template('SearchWithCSSDataDB.html', search_text="")


@app.route('/searchData', methods=['POST'])
def search():
    search_text = request.form['searchInput']
    html_table = load_data_from_db(search_text)
    print(html_table)
    return render_template('SearchWithCSSDataDB.html', search_text=search_text, table=html_table)


# find search_text in csv and display to html
def load_data_from_db(search_text):
    sqldbname = 'db\website.db'
    if search_text != "":
        conn = sqlite3.connect(sqldbname)
        cursor = conn.cursor()
        sqlcommand = ("SELECT * FROM storages WHERE model LIKE '%"+search_text+"%'")
        cursor.execute(sqlcommand)
        data = cursor.fetchall()
        conn.close()
        return data


if __name__ == '__main__':
    app.run(debug=True)
