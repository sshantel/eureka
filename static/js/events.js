"use strict";

{var buttons = document.querySelectorAll('.save-recipe')

buttons.forEach((button)=> {button.addEventListener('click', (evt) => {
  const btn = evt.target;
  const savedRecipes = {
    'link_to_recipe': btn.previousElementSibling.href,
    'recipe_name': $(`.${evt.target.id}, .recipe-name`).html(),
    'recipe_id': btn.id
  };  
        console.log(evt.srcElement.parentNode)
        console.log(evt)
        console.log(evt.target) 
        console.log(evt.target.id) 
        console.log(savedRecipes)

if (btn.innerHTML === 'save recipe') {
    $.post('/saved_recipes', savedRecipes, (response) => { 
        console.log(response)
        btn.innerHTML = 'unsave recipe'
})
}
else if (btn.innerHTML === 'unsave recipe') {
    $.post('/unsave_recipe', savedRecipes, (response)=> {
        console.log(response)
        btn.innerHTML = 'save recipe'
})};
});
})
}

{
const textButtons = document.querySelectorAll('.text-recipe')

textButtons.forEach((button)=> {button.addEventListener('click', (evt) => {
    const btn = evt.target;
    const recipeText = {
        'link_to_recipe': btn.parentNode.children[0].href,
        'recipe_name': $(`.${evt.target.id}, .recipe-name`).html(),
};
    console.log(evt.srcElement.parentNode)
    console.log(evt)
    console.log(evt.target) 
    console.log(evt.target.id) 
    console.log(recipeText)

if (btn.innerHTML === 'text recipe link to phone') {
    $.post('/recipe_texted', recipeText, (response) => {
        console.log(response)
})};
});
})
}


function initGeocoder() { 
    $('#location-button').on('click', (evt) => {
     navigator.geolocation.getCurrentPosition((res) => {
        console.log(res);
    const geocoder = new google.maps.Geocoder();
    const latlng = {lat: res.coords.latitude, lng: res.coords.longitude}
    geocoder.geocode({'location':latlng}, (res, status) => {
    const userLocation = res[3].formatted_address
        console.log(userLocation)
        console.log(latlng)
    const locationInput = document.querySelector('#location')
    const locationButton = document.querySelector('#location-button') 
        locationInput.value = userLocation;
        console.log(locationInput)
    })
     })
    })
}

 
 
