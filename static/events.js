"use strict";

document.querySelector('#favorite-recipe').addEventListener('click', (evt) => {
  const btn = evt.target;

  const favoriteRecipes = {
    'favoriteName': btn.name,
    'recipeId': btn.value
  };
        console.log(btn.value)
        console.log(btn.name)

if (btn.textContent === 'favorite recipe') {
    $.post('/favorite', favoriteRecipes, (favorite, recipe_id) => {
        btn.textContent = 'unfavorite recipe';
    });
  } else {
    btn.textContent = 'favorite recipe';
  }
});

