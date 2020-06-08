"""Server for recipe website."""

from flask import (Flask, render_template, request, flash, session, redirect) 

from model import connect_to_db

from jinja2 import StrictUndefined

import api
import os
import requests

from pprint import pformat

app = Flask(__name__)

app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ["SPOONACULAR_KEY"]

@app.route('/')
def homepage():
    """View homepage."""
    return render_template('homepage.html')

@app.route('/get-ingredient-and-time', methods=['POST']) #POST 
#(inside here, take the information
#user is providing and make the API call#)
def get_ingredient_and_time(ingredient):
    input_ingredient = request.form.get('ingredient')
    time = request.form.get('time')
    print(ingredient)
    print(time)
    # results = api.get_recipes(ingredient)
    data = request.json
    return jsonify(data)
    print(results)

    url = 'https://api.spoonacular.com/recipes/search'

    payload = {'query': ingredient,
                'number': 100,
                'apiKey': API_KEY}
                
    response = requests.get(url, params=payload)

    data = response.json()

    recipe_results = data['results']

    for result in recipe_results:
        recipe_title = result['title']
        ready_in_minutes = result['readyInMinutes']
        print(f' Recipe: {recipe_title}. Total cooking time = {ready_in_minutes}')

    return render_template('search-results.html')

    # return render_template('search-results.html')
#access api into a function and get response and return response into recipe template

@app.route('/recipes')
def all_recipes():
    pass

@app.route('/recipes/<recipe_id>')
def recipe_id(recipe_id):
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)