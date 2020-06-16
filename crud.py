""" CRUD operations """

from model import connect_to_db, db, User, Recipe, SavedRecipe

def create_user(username, email, password, location_of_user):
    """ Create and return a new user """

    user =  User(username = username,
                 email = email,
                 password=password,
                 location_of_user=location_of_user)

    db.session.add(user)
    db.session.commit()

    return user 

def create_recipe(api_recipe_id, recipe_course, prep_time, cook_time, total_recipe_time,
    recipe_description, servings, image, reviews, recipe_title):

    create_recipe = Recipe(api_recipe_id=api_recipe_id,
                    recipe_course=recipe_course,
                    prep_time=prep_time,
                    cook_time=cook_time,
                    total_recipe_time=total_recipe_time,
                    recipe_description=recipe_description,
                    servings=servings,
                    image=image,
                    reviews=reviews,
                    recipe_title=recipe_title)


    db.session.add(create_recipe)
    db.session.commit()

    return create_recipe

def create_saved_recipe(recipe_id, user_id, recipe_name, user):


    create_saved_recipe = SavedRecipe(user_id = user_id,
                                    recipe_name = recipe_name,
                                    user = user)

    db.session.add(create_saved_recipe)
    db.session.commit()

    return create_saved_recipe

def get_user_by_id(user_id):
    """Return a user by primary key."""
    return User.query.get(user_id)

def get_user_by_email(email):
    """Return a user by email."""
    return User.query.filter(User.email == email).first()

def get_recipes():
    """Return all recipes"""
    return Recipe.query.all()

def get_recipe_by_id(recipe_id):
    """Return a user by primary key."""
    return User.query.get(recipe_id)


if __name__ == '__main__':
    from server import app
    connect_to_db(app)