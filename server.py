"""Server for recipe website."""

from flask import (Flask, render_template, request, flash, session, redirect) 

from model import connect_to_db

from jinja2 import StrictUndefined

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

@app.route('/search-results', methods=['GET']) 
def get_ingredient_and_time():
    input_ingredient = request.args.get('ingredient')
    print(input_ingredient)
    input_time = request.args.get('time') 
    print(input_time)

    url = 'https://api.spoonacular.com/recipes/search'

    payload = {'query': input_ingredient,
                'readyInMinutes': input_time,
                'number': 10,
                'apiKey': API_KEY}

    response = requests.get(url, params=payload)

    data = response.json()

    recipe_results = data['results']

    #for time in recipe_results
    #dictionary
    for result in recipe_results:
        recipe_title = result['title']
        print(recipe_title)
        recipe_id = result['id']
        print(recipe_id)
        ready_in_minutes = result['readyInMinutes']
        print(ready_in_minutes)
        print(f' Recipe: {recipe_title}. Total cooking time = {ready_in_minutes}')

    return render_template('search-results.html',
                            pformat=pformat,
                            data=data,
                            recipe_title=recipe_title,
                            recipe_id=recipe_id,
                            recipe_results=recipe_results)

@app.route('/recipes/<recipe_id>')
def recipe_id(recipe_id):
    """Show details on a particular recipe."""
    recipe = crud.get_recipe_by_id(recipe_id)

    return render_template('recipes_details.html', recipe=recipe)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)