"""Server for recipe website."""

from flask import (Flask, render_template, request, flash, session, redirect, url_for) 

from model import connect_to_db

from jinja2 import StrictUndefined

import os
import requests

import crud 

from pprint import pformat

import geocoder


app = Flask(__name__)

app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ["SPOONACULAR_KEY"]

@app.route('/')
def homepage():
    """View homepage and login."""
    error=None

    return render_template('login.html', error=error)

@app.route('/login', methods=['GET','POST'])
def login():
    """User login."""

    email = request.form.get('email')
    password = request.form.get('password')
  
    user = crud.get_user_by_email(email)

    if user == None:
        flash('account does not exist, sorry')
        print(user)
        return redirect('/')

    elif password == user.password:
        session['user'] = email
        flash(f'successfully logged in with the {email}')
        return redirect('/search-results')

    else:
        flash('wrong password!')
        return redirect('/')


@app.route('/create', methods=['GET'])
#register
def create():
    """View homepage and login."""
    return render_template('create.html')

@app.route('/register', methods=['POST'])
def search():
    """User searches for ingredient and amount of time they 
    want to spend"""
    g = geocoder.ip('me')
    print(g.latlng)

    
    username = request.form.get('username')
    print(username)

    email = request.form.get('email')
    print(email)

    password = request.form.get('password')
    print(password)

    location = request.form.get('location')
    print(location)

    user = crud.get_user_by_email(email)
    print(user)
    if user:
        flash('Cannot create an account with that email. Try again.')
    else:
        crud.create_user(username, email, password, location)
        flash('Account created! Please log in.')

    return render_template('homepage.html')

@app.route('/search-results', methods=['GET']) 
def search_results():
    input_ingredient = request.args.get('ingredient')
    print(input_ingredient)
    input_time = request.args.get('time')

    url = 'https://api.spoonacular.com/recipes'


    # payload = {'query': input_ingredient,
    #             'readyInMinutes': int_input_time,
    #             'number': 10,
    #             'apiKey': API_KEY}

    payload1 = {'query': input_ingredient,
                'maxReadyTime': input_time,
                'number': 10,
                'apiKey': API_KEY}

    response1 = requests.get(url + '/complexSearch', params=payload1)

    data1 = response1.json()

    complex_search_results = data1["results"]

    list_of_recipe_ids = []

    for complex_result in complex_search_results:
        print(complex_result)
        recipe_title = complex_result['title'] 
        print(recipe_title)
        image = complex_result['image'] 
        print(image)
        recipe_id = complex_result['id'] 
        list_of_recipe_ids.append(str(recipe_id))
        print(recipe_id) 
        print(f' Recipe: {recipe_title}.')

    payload2 = {'ids' : ','.join(list_of_recipe_ids),
                'apiKey': API_KEY}

    response2 = requests.get(url + '/informationBulk', params=payload2)

    data2= response2.json()

    # id_search_results = data2["results"]

    # for id_search_result in id_search_results:
    #     print(id_search_result)

    return render_template('search-results.html',
                            pformat=pformat,
                            data1=data1,
                            data2=data2,
                            recipe_title=recipe_title,
                            recipe_id=recipe_id,
                            image=image,
                            input_ingredient=input_ingredient,
                            input_time=input_time,
                            complex_search_results=complex_search_results)

    # data = response.json()

    # recipe_results = data['results']

    # for result in recipe_results:
    #     ready_in_minutes = result['readyInMinutes']
    #     print(ready_in_minutes) 
    #     recipe_title = result['title'] 
    #     print(recipe_title)
    #     image = result['image'] 
    #     print(image)
    #     recipe_id = result['id'] 
    #     print(recipe_id)
    #     print(type(ready_in_minutes))
    #     print(type(int_input_time)) 
    #     print(f' Recipe: {recipe_title}. Total cooking time = {ready_in_minutes}')

    # recipe = crud.get_recipe_by_id(recipe_id)

    # return render_template('search-results.html',
    #                         pformat=pformat,
    #                         data=data,
    #                         recipe_title=recipe_title,
    #                         recipe_id=recipe_id,
    #                         recipe_results=recipe_results,
    #                         result=result,
    #                         image=image,
    #                         input_ingredient=input_ingredient,
    #                         int_input_time=int_input_time)
#Search Recipes Complex
#Get Recipe Information 

@app.route('/logout')
def logout():
    if "user" in session:
        user = session['user']
        flash(f'you have been logged out, {username}')
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/recipes/<recipe_id>')
def recipe_id(recipe_id):
    """Show details on a particular recipe."""
    pass
    # return render_template('recipe_details.html')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)