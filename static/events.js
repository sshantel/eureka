"use strict";

document.querySelector('#saved-recipes').addEventListener('click', (evt) => {
  const btn = evt.target;

  const savedRecipes = {
    'link_to_recipe': btn.value,
    'recipe_id': btn.name, 
  };
        console.log(btn.value)
        console.log(btn.name)   

if (btn.innerHTML === 'save recipe') {
    $.post('/saved_recipes', savedRecipes, (response) => {
        console.log(response)
        btn.innerHTML = 'unsave recipe';
    });
  } else {
    btn.innerHTML = 'save recipe';
  }
});


 

 