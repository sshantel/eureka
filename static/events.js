"use strict";

document.querySelector('#saved-recipes').addEventListener('click', (evt) => {
  const btn = evt.target;

  const savedRecipes = {
    'recipeId': btn.value,
    'savedRecipe': btn.name
  };
        console.log(btn.value)
        console.log(btn.name)

if (btn.textContent === 'save recipe') {
    $.post('/saved_recipes', savedRecipes, (response) => {
        console.log(response)
        btn.textContent = 'unsave recipe';
    });
  } else {
    btn.textContent = 'save recipe';
  }
});


 

