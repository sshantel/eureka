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

@app.route('/login', methods=['POST'])
def login():

    """User login."""

    email = request.form.get('email')
    password = request.form.get('password')
    user = crud.get_user_by_email(email)

    if user == None:
        flash('Account does not exist, sorry. Please sign up with an account.')
        print(user)
        return redirect('/')

    elif password == user.password:
        session['user'] = email
        flash(f'Successfully logged in with the email {email}!')
        return render_template('share_or_learn.html')

    else:
        flash('Wrong password! Please try again.')
        return redirect('/')

    if request.method == 'POST':
        return render_template('share_or_learn.html')

@app.route('/share_or_learn', methods =['POST'])
def share_or_learn():
    return render_template('share_or_learn.html')

#@app.route('/share', methods=['GET'])
    #pass

@app.route('/create', methods=['GET'])
#register
def create(): 
    return render_template('create.html')

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
        flash('Cannot create an account with that email. Try again.')
    else:
        crud.create_user(username, email, password, location)
        flash('Account created! Please log in.')

    return render_template('homepage.html')

@app.route('/search', methods=['POST'])
def search():
    learn = request.form.get('learn')
    return render_template('homepage.html')
    
    # share = request.form.get('share')
    #return render_template share
    #would i just use request.method = post vs get to render two diff
    #templates depending on what the user chooses?


@app.route('/search_results', methods=['GET']) 
def search_results():
    """User searches for ingredient and amount of time they 
    want to spend"""

    input_ingredient = request.args.get('ingredient')
    print(input_ingredient)
    input_time = request.args.get('time')

    url = 'https://api.spoonacular.com/recipes'


    payload1 = {'query': input_ingredient,
                'maxReadyTime': input_time,
                'number': 1,
                'apiKey': API_KEY}

    response1 = requests.get(url + '/complexSearch', params=payload1)

    data1 = response1.json()
    print(data1)
    print(type(data1))

    complex_search_results = data1["results"]
    print(f'this is complex search{complex_search_results}')

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
    print(data2)
    print(type(data2))

    information_bulk_results = data2

    for information_bulk_result in information_bulk_results:
        print(information_bulk_result)
        url = information_bulk_result['sourceUrl']
        print(url)
   

    return render_template('search_results.html',
                            pformat=pformat,
                            url=url,
                            data1=data1,
                            data2=data2,
                            recipe_title=recipe_title,
                            recipe_id=recipe_id,
                            image=image,
                            input_ingredient=input_ingredient,
                            input_time=input_time,
                            complex_search_results=complex_search_results)

#Search Recipes Complex
#Get Recipe Information 

@app.route('/logout')
def logout():
    error=None
    if "user" in session:
        user = session['user']
    session.pop("user", None)
    flash('You have been logged out!', 'info') #info=category for message
    return render_template('login.html', error= error)

@app.route('/recipes/<recipe_id>')
def recipe_id(recipe_id):
    """Show details on a particular recipe."""
    pass
    # return render_template('recipe_details.html')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)