"""Server for recipe website."""

from flask import (Flask, render_template, request, flash, session, redirect, url_for) 

from model import connect_to_db

import cloudinary 
import cloudinary.uploader
import cloudinary.api

from jinja2 import StrictUndefined

import os
import requests

import crud

from twilio.rest import Client

from pprint import pformat

app = Flask(__name__)
app.secret_key = "dev"

app.jinja_env.undefined = StrictUndefined

spoonacular_key = os.environ["spoonacular_key"] 

cloud_name = os.environ["cloud_name"]
cloudinary_api_key = os.environ["cloudinary_api_key"]
cloudinary_api_secret = os.environ["cloudinary_api_secret"]

cloudinary.config( 
  cloud_name = cloud_name, 
  api_key = cloudinary_api_key, 
  api_secret = cloudinary_api_secret  
)

twilio_api = os.environ["twilio_api"]
twilio_auth = os.environ["twilio_auth"]

account_sid = twilio_api
auth_token = twilio_auth
client = Client(account_sid, auth_token)

@app.route('/')
def homepage():
    """View homepage and login."""
    error=None
    return render_template('login.html', error=error)

@app.route('/share_or_learn')
def share_or_learn(): 
    """Asking the user whether they want to either share or learn a recipe"""
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
        return redirect(url_for('share_or_learn'))

    else:
        flash('Wrong password! Please try again.','danger')
        return redirect('/')

@app.route('/signup', methods=['GET'])
def signup(): 
    """Render user signup/registration page"""
    return render_template('signup.html')

@app.route('/register', methods=['POST'])
def register():
    """User registration form."""
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    location = request.form.get('location')
    print('location',location)
    phone_number = request.form.get('phone-number')
    print(phone_number)
    user = crud.get_user_by_email(email)
    print(user)
    if user:
        flash('you already have an account, please log in', 'danger')
        return redirect('/')
    else:
        crud.create_user(username, email, password, location, phone_number)
        flash('Account created!', 'success')

    return render_template('search.html')

@app.route('/account')
def account():
    """Render user account details (WIP)"""
    return render_template('account.html')

@app.route('/search')
def search(): 
    """User to input ingredient/time they want to spend"""
    return render_template('search.html')

@app.route('/share', methods=['POST'])
def share():
    """User to share recipe"""
    return redirect('/share')

@app.route('/share')
def show_share_page():
    """Render share recipe page"""
    return render_template('share.html')

@app.route('/search_results', methods=['GET']) 
def search_results():
    """Returning recipe results for user"""
    input_ingredient = request.args.get('ingredient')
    input_time = request.args.get('time')

    url1 = 'https://api.spoonacular.com/recipes'

    payload1 = {'query': input_ingredient,
                'maxReadyTime': input_time,
                'number': 10,
                'apiKey': spoonacular_key}

    response1 = requests.get(url1 + '/complexSearch', params=payload1)

    data1 = response1.json()

    complex_search_results = data1['results']

    list_of_recipe_ids = []

    for complex_result in complex_search_results:
        recipe_title = complex_result['title'] 
        print('recipe_title', recipe_title)
        image = complex_result['image'] 
        recipe_id = complex_result['id'] 
        list_of_recipe_ids.append(str(recipe_id))
        print(f' Recipe: {recipe_title}.')

    payload2 = {'ids' : ','.join(list_of_recipe_ids),
                'apiKey': spoonacular_key}

    response2 = requests.get(url1 + '/informationBulk', params=payload2)

    br = response2.json()

    information_bulk_results = br

    return render_template('search_results.html',
                          pformat=pformat,
                          input_ingredient=input_ingredient,
                          input_time=input_time,
                          data1=data1,
                          br=br)
    
@app.route('/logout')
def logout():
    """User logout function"""
    error=None
    if "user" in session:
        user = session['user']
    session.pop("user", None)
    flash('You have been logged out!', 'info') 
    return render_template('login.html', error=error)

@app.route('/saved_recipes', methods=['POST'])
def saved_recipes():
    """Function for user to save a recipe"""
    link_to_recipe = request.form.get('link_to_recipe')
    print(link_to_recipe)
    recipe_id = request.form.get('recipe_id') 
    print(recipe_id)
    email = session['user']  
    print(email)
    user = crud.get_user_by_email(email) 
    print(user)
    user_id = user.user_id
    recipe_name = request.form.get('recipe_name')
    crud.create_saved_recipe(recipe_name, recipe_id, user_id, user, link_to_recipe)
    return "This recipe has been saved!!"

@app.route('/unsave_recipe', methods=['POST'])
def unsave_recipe(): 
    """User to unsave a recipe"""
    recipe_id = request.form.get('recipe_id') 
    unsave_recipe = crud.unsave_recipe(recipe_id)
    return('this recipe has been unsaved!')

@app.route('/user_saved_recipes')
def user_saved_recipes():
    """User to view all of their saved recipes"""
    email = session['user']  
    user = crud.get_user_by_email(email) 
    user_id = user.user_id 
    recipe_id = crud.get_recipe_ids_a_user_has_favorited(user_id)
    saved_recipes = crud.get_all_saved_recipes(user_id)
    return render_template('saved_recipes.html', user=user, saved_recipes=saved_recipes, recipe_id=recipe_id)

@app.route('/recipe_submitted', methods=['POST'])
def recipe_submitted():
    """User to upload their own recipe"""
    create_recipe_name = request.form.get('create_recipe_name')
    source_url = request.form.get('source-url')
    recipe_course = request.form.get('recipe-course')
    prep_time = request.form.get('prep-time')
    cook_time = request.form.get('cook-time')
    total_recipe_time = request.form.get('total-cook-time')
    ingredients = request.form.get('ingredients')
    recipe_description = request.form.get('recipe-description')
    servings = request.form.get('servings')
    directions = request.form.get('directions')
    filename = request.files.get('image-upload')
    if filename:
        response = cloudinary.uploader.upload(filename)
        print(response)
        image = response['secure_url']
    print(image)
    email = session['user']
    user = crud.get_user_by_email(email) 
    user_id = user.user_id 
    creating_recipe = crud.create_recipe(create_recipe_name, source_url, recipe_course, prep_time, cook_time, total_recipe_time, ingredients, 
    recipe_description, servings, directions, image, user_id)

    return render_template('recipe_submitted.html', creating_recipe=creating_recipe, image=image)

@app.route('/recipe_texted', methods = ['POST'])
def recipe_texted():
    """Function for user to text the recipe link to their phone"""
    link_to_recipe = request.form.get('link_to_recipe')
    print(link_to_recipe)
    recipe_name = request.form.get('recipe_name')
    email = session['user'] 
    user = crud.get_user_by_email(email) 
    user_id = user.user_id
    phone_number = crud.get_phone_number_by_user_id(user_id)

    message = client.messages \
    .create(
         body=link_to_recipe,
         from_='+12054966699',
         to='+1' + phone_number  
     )

    print(message.sid)
    return('recipe has been texted')

@app.route('/uploaded_recipes')
def uploaded_recipes():
    email = session['user'] 
    user = crud.get_user_by_email(email) 
    user_id = user.user_id
    uploaded_recipes = crud.all_uploaded_recipes(user_id) 
    print(uploaded_recipes)
    return render_template('users_uploaded_recipes.html', uploaded_recipes=uploaded_recipes)

@app.route('/map')
def map():
    return render_template('map.html')

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)