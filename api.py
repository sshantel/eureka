import requests

def get_recipes(ingredient):

    payload = {'query': ingredient,
                'apiKey': API_KEY}

    res1 = requests.get('https://api.spoonacular.com/recipes/search',
    params = payload)

    ingredient_in_dishes = res1.json()

    recipe_results = ingredient_in_dishes['results']

    for result in recipe_results:
        recipe_title = result['title']
        ready_in_minutes = result['readyInMinutes']
        print(f' Recipe: {recipe_title}. Total cooking time = {ready_in_minutes}')

    return recipe_results

# payload2 = {'ingredients': 'cucumber',
#             'number' : 100}

# res2 = requests.get('https://api.spoonacular.com/recipes/findByIngredients?apiKey=af1baf325a964d2aa9a77317bfe6a467',
#     params = payload2)

# cucumber_dishes2 = res2.json()

# cucumber_results2 = cucumber_dishes2['results']

# for result2 in cucumber_results2:
#     recipe_title = result2['title']
#     ready_in_minutes = result2['readyInMinutes']
#     print(f' Recipe: {recipe_title}. Total cooking time = {ready_in_minutes}')

# print(res2.url)
