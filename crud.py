""" CRUD operations """

from model import db, User, Movie, Rating, connect_to_db

def create_user(username, email, password, location_of_user, created_at):
    """ Create and return a new user """

    user =  User(username = username,
                 email = email,
                 password = password,
                 location_of_user = location_of_user,
                 created_at = created_at) 


    db.session.add(user)
    db.session.commit()

    return user 

def create_saved_recipe(recipe_id, user_id, saved_at, recipe, user):


    create_saved_recipe = SavedRecipe(user_id = user_id,
                                    saved_at = saved_at,
                                    recipe = recipe,
                                    user = user)

    db.session.add(recipe)
    db.session.commit()

    return create_saved_recipe

def create_recipe(recipe_name, recipe_course, prep_time, cook_time, total_recipe_time,
    recipe_description, servings, image, reviews):

    create_recipe = Recipe(recipe_name = recipe_name,
                            recipe_course = recipe_course,
                            prep_time = prep_time,
                            cook_time = cook_time,
                            total_recipe_time = total_recipe_time,
                            recipe_description = recipe_description,
                            servings = servings,
                            image = image,
                            reviews = reviews)

    db.session.add(create_recipe)
    db.session.commit()

    return create_recipe

def recipe_ingredient(measurements):

    measurements = RecipeIngredient(measurements = measurements)


def ingredient(ingredient_name, food_group, sweet_or_savory):

    








































if __name__ == '__main__':
    from server import app
    connect_to_db(app)