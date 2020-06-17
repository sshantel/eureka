"""Server for recipe website."""

from flask import (Flask, render_template, request, flash, session, redirect, url_for) 

from model import connect_to_db

from jinja2 import StrictUndefined

import os
import requests

import crud 

from pprint import pformat


app = Flask(__name__)
app.secret_key = "dev"

app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ["SPOONACULAR_KEY"]

@app.route('/')
def homepage():
    """View homepage and login."""
    error=None

    return render_template('login.html', error=error)

@app.route('/share_or_learn', methods =['GET'])
def share_or_learn(): 
    return render_template('share_or_learn.html')

@app.route('/login', methods=['POST'])
def login():

    """User login."""
    email = request.form.get('email')
    password = request.form.get('password')
    user = crud.get_user_by_email(email)

    if user == None:
        flash('Account does not exist, sorry. Please sign up with an account.', 'danger')

        print(user)
        return redirect('/')

    elif password == user.password:
        session['user'] = email
        user = crud.get_user_by_email(email) 
        flash(f'Successfully logged in with the email {email}!','success')
        return redirect(url_for('share_or_learn', user=user, email=email))
        # return redirect('/share_or_learn')

    else:
        flash('Wrong password! Please try again.','danger')
        return redirect('/')

#@app.route('/share', methods=['GET'])
    #pass

@app.route('/signup', methods=['GET'])
def signup(): 
    return render_template('signup.html')

@app.route('/register', methods=['POST'])
def register():
    """User registration form."""

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    location = request.form.get('location')

    user = crud.get_user_by_email(email)

    print(user)
    if user:
        flash('Cannot create an account with that email. Try again.', 'danger')
    else:
        crud.create_user(username, email, password, location)
        flash('Account created! Please log in.', 'success')

    return render_template('search.html')

@app.route('/search', methods= ['POST'])
def search():
    return render_template('search.html')
    

@app.route('/search_results', methods=['GET']) 
def search_results():
    """User searches for ingredient and amount of time they 
    want to spend"""

    input_ingredient = request.args.get('ingredient')
    input_time = request.args.get('time')

    url = 'https://api.spoonacular.com/recipes'


    payload1 = {'query': input_ingredient,
                'maxReadyTime': input_time,
                'number': 1,
                'apiKey': API_KEY}

    response1 = requests.get(url + '/complexSearch', params=payload1)

    data1 = response1.json()

    complex_search_results = data1['results']

    list_of_recipe_ids = []

    for complex_result in complex_search_results:
        recipe_title = complex_result['title'] 
        image = complex_result['image'] 
        recipe_id = complex_result['id'] 
        list_of_recipe_ids.append(str(recipe_id))
        print(f' Recipe: {recipe_title}.')

    payload2 = {'ids' : ','.join(list_of_recipe_ids),
                'apiKey': API_KEY}

    response2 = requests.get(url + '/informationBulk', params=payload2)

    data2= response2.json()

    information_bulk_results = data2

    for information_bulk_result in information_bulk_results:
        print(information_bulk_result)
        recipe_summary = information_bulk_result['summary']
        url = information_bulk_result['sourceUrl']
        servings = information_bulk_result['servings']
        vegetarian = information_bulk_result['vegetarian']
        complex_recipe_id = information_bulk_result['id']
        complex_recipe_name = information_bulk_result['title']
        dish_types2 = information_bulk_result['dishTypes']
        print(dish_types2)
        dish_types =', '.join(dish_types2)
        print(url)

    return render_template('search_results.html',
                            pformat=pformat,
                            servings=servings,
                            url=url,
                            dish_types=dish_types,
                            data1=data1,
                            data2=data2,
                            recipe_summary=recipe_summary,
                            recipe_title=recipe_title,
                            recipe_id=recipe_id,
                            complex_recipe_id=complex_recipe_id,
                            image=image,
                            input_ingredient=input_ingredient,
                            vegetarian=vegetarian,
                            input_time=input_time,
                            complex_result=complex_result,
                            complex_search_results=complex_search_results,
                            complex_recipe_name=complex_recipe_name)

@app.route('/logout')
def logout():
    error=None
    if "user" in session:
        user = session['user']
    session.pop("user", None)
    flash('You have been logged out!', 'info') 
    return render_template('login.html', error=error)

@app.route('/saved_recipes', methods=['POST'])
def saved_recipes():

    # STATUS = {'favorite' : 'favorited',
    #           'unfavorite' :'unfavorited'}

    link_to_recipe = request.form.get('link_to_recipe')
    print('link to recipe', link_to_recipe)
    recipe_id = request.form.get('recipe_id') 
    email = session['user'] 
    print(f' EMAIL* {email}.')
    user = crud.get_user_by_email(email) 
    print('user', user)
    user_id = user.user_id
    print('user id', user_id) 
    # recipe_name = crud.get_recipe_name_by_recipe_id
    # recipe_id = crud.get_recipe_ids_a_user_has_favorited(user_id)
    print('recipe id', recipe_id)
    # link_to_recipe = crud.get_link_by_recipe_id(recipe_id)
    crud.create_saved_recipe(recipe_id, user_id, user, link_to_recipe)
    return "This recipe has been favorited!"
        #dictionary of key value pairs of statuses
    #ADD URL

@app.route('/user_saved_recipes')
def user_saved_recipes():
    email = session['user']  
    user = crud.get_user_by_email(email) 
    user_id = user.user_id 
    recipe_id = crud.get_recipe_ids_a_user_has_favorited(user_id)
    print(recipe_id)
    saved_recipes = crud.get_all_saved_recipes(user_id)
    return render_template('saved_recipes.html', user=user, saved_recipes=saved_recipes, recipe_id=recipe_id)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)