from flask import Flask, request, render_template

# create an app named 'app'
# define URL for static files
app = Flask(__name__, static_url_path='/static')


# the default root - first time entering website takes to html in render_template
# render_template takes 2nd argument from users' input
@app.route('/')
def index():
    return render_template('SearchWithCSS.html', search_text="")


@app.route('/search', methods=['POST'])
def search():
    # get data from Request
    search_text = request.form['searchInput']
    return render_template('SearchWithCSS.html', search_text=search_text)

# run app with debugging
if __name__ == '__main__':
    app.run(debug=True)
