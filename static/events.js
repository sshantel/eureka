"use strict";

document.querySelector('.save-recipe').addEventListener('click', (evt) => {
  const btn = evt.target;

  const savedRecipes = {
    'link_to_recipe': $(`.${evt.target.id} .title`)[0].href,
    'recipe_name': $(`.${evt.target.id} .title`).html(),
    'recipe_id': btn.id
  };  
        console.log(evt.srcElement.parentNode)
        console.log(evt)
        console.log(evt.target) 
        console.log(evt.target.id) 

if (btn.innerHTML === 'save recipe') {
    $.post('/saved_recipes', savedRecipes, (response) => {
        console.log(response)
        btn.innerHTML = 'unsave recipe';
    });
  } else {
    btn.innerHTML = 'save recipe';
  }
});

// "use strict";

// document.querySelector('.save-recipe').addEventListener('click', (evt) => {
//   const btn = evt.target;

//   const savedRecipes = {
//     'link_to_recipe': $(`.${evt.target.id} .title`)[0].href,
//     'recipe_name': $(`.${evt.target.id} .title`).html(),
//     'recipe_id': btn.id
//   };  
//         // console.log(evt.srcElement.parentNode)
//         // console.log(evt)
//         // console.log(evt.target) 
//         // console.log(evt.target.id) 

// if (btn.innerHTML === 'save recipe') {
//     $.post('/saved_recipes', savedRecipes, (response) => {
//         console.log(response)
//         btn.innerHTML = 'unsave recipe';
//     });
//   } else {
//     btn.innerHTML = 'save recipe';
//   }
// });




 

 