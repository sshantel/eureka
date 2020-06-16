import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb recipe')
os.system('createdb recipe')

model.connect_to_db(server.app)
model.db.create_all()

def seed_users():
    with open('data/users.json') as f:
        user_data = json.loads(f.read())

    for user in user_data:
        username = user['username']
        email = user['email']
        password = user['password']
        location_of_user = user['location_of_user']
        crud.create_user(username, email, password, location_of_user)

    
seed_users()

model.db.session.commit()

# def seed_recipes():

#     with open('data/recipes.json') as f:
#         recipe_data = json.loads(f.read())

#     for recipe in recipe_data:
#         api_recipe_id = recipe['results']['api_recipe_id']
#         recipe_course = recipe['results']['recipe_course']
#         prep_time = recipe['results']['prep_time']
#         cook_time = recipe['results']['cook_time']
#         total_recipe_time = recipe['results']['readyInMinutes']
#         recipe_description = recipe['results']['recipe_description']
#         servings = recipe['results']['servings']
#         image = recipe['results']['image']
#         url = recipe['results']['sourceUrl']
#         reviews = recipe['results']['reviews']
#         recipe_title = recipe['results']['title']

#     crud.create_recipe(api_recipe_id, recipe_course, prep_time, cook_time, total_recipe_time,
#     recipe_description, servings, image, reviews, recipe_title)

# seed_recipes()

def seed_recipe_ingredients():

    with open('data/recipe_ingredients.json') as f:
        recipe_ingredients = json.loads(f.read())

    pass

seed_recipe_ingredients()
