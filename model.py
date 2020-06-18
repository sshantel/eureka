"""Models for recipes web application."""
from flask_sqlalchemy import SQLAlchemy 

from datetime import datetime

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, 
                    autoincrement=True, 
                    primary_key=True)
    username = db.Column(db.String, 
                    unique=True,
                    nullable = False)
    email = db.Column(db.String, 
                    unique=True)
    password = db.Column(db.String)
    location_of_user = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'''<User user_id={self.user_id} username={self.username} email={self.email}
        password = {self.password} location of user = {self.location_of_user} created at = {self.created_at}>'''

class Recipe(db.Model):
    __tablename__ = 'recipes'

    cy_recipe_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True, 
                        unique=True) 
    cy_recipe_name = db.Column(db.String) 
    recipe_course = db.Column(db.String)
    prep_time = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)
    total_recipe_time = db.Column(db.Integer)
    recipe_description = db.Column(db.String)
    servings = db.Column(db.Integer)
    image = db.Column(db.String)
    reviews = db.Column(db.String) 

    # users  = db.relationship('User', backref = 'recipes', secondary = 'savedrecipes')
    
    def __repr__(self):
        return f'''<recipe api id={self.cy_recipe_id} recipe_name={self.cy_recipe_name}
        recipe course={self.recipe_course} prep time ={self.prep_time}
        cook time = {self.cook_time} total recipe time = {self.total_recipe_time}
        recipe description = {self.recipe_description} servings = {self.servings}
        image = {self.image} reviews = {self.reviews} >'''

class SavedRecipe(db.Model):

    __tablename__ = 'savedrecipes'

    saved_recipe_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True)
    recipe_name = db.Column(db.String)
    link_to_recipe= db.Column(db.String)
    recipe_id = db.Column(db.Integer,
                         unique = True)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'))
    saved_at = db.Column(db.DateTime, default = datetime.utcnow)

    # recipe = db.relationship('Recipe', backref = 'savedrecipes')
    user = db.relationship('User', backref = 'savedrecipes')

    def __repr__(self):
        return f'''<saved recipe id={self.saved_recipe_id} recipe_id={self.recipe_id} recipe_name = {self.recipe_name}
        user id={self.user_id} saved at={self.saved_at} url = {self.link_to_recipe}>'''

    
def connect_to_db(flask_app, db_uri='postgresql:///recipe', echo=False):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

if __name__ == '__main__':
    from server import app
    connect_to_db(app)  






