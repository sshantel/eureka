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

def 

seed_users()