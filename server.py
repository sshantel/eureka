"""Server for recipe website."""

from flask import (Flask, render_template, request, flash, session, redirect) 

from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage."""
    return render_template('homepage.html')

@app.route('/recipes')
def all_recipes():
    pass

@app.route('/recipes/<recipe_id>')
def recipe_id(recipe_id):
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)