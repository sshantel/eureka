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

def seed_create_recipes():
    with open('data/recipes.json') as f:
        create_recipes = json.loads(f.read())

    for recipe in create_recipes:
        create_recipe_name = recipe['create_recipe_name']
        recipe_course = recipe['recipe_course']
        prep_time = recipe['prep_time']
        cook_time = recipe['cook_time']
        total_recipe_time = recipe['total_recipe_time']
        recipe_description = recipe['recipe_description']
        servings = recipe['servings']
        image = recipe['image']
        crud.create_recipe(create_recipe_name, recipe_course, prep_time, cook_time, total_recipe_time,
        recipe_description, servings, image)

seed_create_recipes()

model.db.session.commit()


