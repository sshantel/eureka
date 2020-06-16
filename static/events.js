"use strict";

document.querySelector('#favorite-recipe').addEventListener('click', (evt) => {
  const btn = evt.target;

  const favoriteRecipes = {
    'recipeId': btn.value,
    'favoriteName': btn.name
  };
        console.log(btn.value)
        console.log(btn.name)

if (btn.textContent === 'favorite recipe') {
    $.post('/favorite', favoriteRecipes, (response) => {
        console.log(response)
        btn.textContent = 'unfavorite recipe';
    });
  } else {
    btn.textContent = 'favorite recipe';
  }
});


 

