""" CRUD operations """

from model import connect_to_db, db, User, Recipe, SavedRecipe

def create_user(username, email, password, location_of_user, phone_number):
    """ Create and return a new user """

    user =  User(username = username,
                 email = email,
                 password=password,
                 location_of_user=location_of_user,
                 phone_number=phone_number)

    db.session.add(user)
    db.session.commit()

    return user 

def create_recipe(create_recipe_name, source_url, recipe_course, prep_time, cook_time, total_recipe_time, ingredients,
    recipe_description, servings, directions, image, user_id):

    create_recipe = Recipe(create_recipe_name=create_recipe_name,
                    source_url=source_url, 
                    recipe_course=recipe_course,
                    prep_time=prep_time,
                    cook_time=cook_time,
                    total_recipe_time=total_recipe_time,
                    ingredients=ingredients,
                    recipe_description=recipe_description,
                    servings=servings,
                    directions=directions,
                    image=image,
                    user_id=user_id)

    db.session.add(create_recipe)
    db.session.commit()

    return create_recipe

def create_saved_recipe(recipe_name, recipe_id, user_id, user, link_to_recipe):


    create_saved_recipe = SavedRecipe(recipe_name=recipe_name,
                                      recipe_id=recipe_id,
                                      user_id=user_id,
                                      user=user,
                                      link_to_recipe=link_to_recipe)

    db.session.add(create_saved_recipe)
    db.session.commit()

    return create_saved_recipe

def all_uploaded_recipes(user_id):
    """Returns all of a user's uploaded recipes"""
    uploaded_recipes = Recipe.query.filter(Recipe.user_id == user_id).all()
    return uploaded_recipes

def unsave_recipe(recipe_id):
    print(SavedRecipe.recipe_id)
    print(recipe_id)    
    print(SavedRecipe)
    recipe = SavedRecipe.query.filter(SavedRecipe.recipe_id == recipe_id).first()
    print('recipe',recipe)
    db.session.delete(recipe)
    db.session.commit()

def get_phone_number_by_user_id(user_id): 
    user = User.query.filter(User.user_id == user_id).first()
    phone_number = user.phone_number 
    return phone_number 

def get_user_by_id(user_id):
    """Return a user by primary key."""
    return User.query.get(user_id)

def get_user_by_email(email):
    """Return a user by email."""
    return User.query.filter(User.email == email).first()

def get_recipe_by_id(recipe_id):
    """Return a user by recipe id."""
    return User.query.get(recipe_id)

def get_all_saved_recipes(user_id):
    """Return a user's saved recipes""" 
    return SavedRecipe.query.filter(User.user_id == user_id).all()

def get_users_who_favorited_by_recipe_id(recipe_id):
    """Return users who have saved this recipe_id into their favorites"""
    return SavedRecipe.query.filter(SavedRecipe.recipe_id == recipe_id).all()

def get_recipe_ids_a_user_has_favorited(user_id):
    """Return recipe ids that a user has favorited"""
    return SavedRecipe.query.filter(User.user_id == user_id).all()

 


if __name__ == '__main__':
    from server import app
    connect_to_db(app)