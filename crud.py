""" CRUD operations """

from model import db, User, CreateRecipe, SavedRecipe, RecipeIngredient, Ingredient, connect_to_db

def create_user(username, email):
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

    create_recipe = CreateRecipe(api_recipe_id=api_recipe_id,
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

def create_saved_recipe(recipe_id, user_id, saved_at, recipe, user):


    create_saved_recipe = SavedRecipe(user_id = user_id,
                                    saved_at = saved_at,
                                    recipe = recipe,
                                    user = user)

    db.session.add(recipe)
    db.session.commit()

    return create_saved_recipe

def recipe_ingredient(measurements):

    measurements = RecipeIngredient(measurements = measurements)


def ingredient(ingredient_name, food_group, sweet_or_savory):

    ingredient = Ingredient(ingredient_name = ingredient_name,
                food_group = food_group,
                sweet_or_savory = sweet_or_savory)

def get_user_by_id(user_id):
    """Return a user by primary key."""
    return User.query.get(user_id)

def get_user_by_email(email):
    """Return a user by email."""
    return User.query.filter(User.email == email).first()

def get_recipes():
    """Return all recipes"""
    return CreateRecipe.query.all()

def get_recipe_by_id(recipe_id):
    """Return a user by primary key."""
    return User.query.get(recipe_id)


if __name__ == '__main__':
    from server import app
    connect_to_db(app)