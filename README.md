# hb-project

Eureka is a full stack web app built during my time at Hackbright Academy. Eureka allows a user to search for a recipe by ingredient(s) and how much time
(maximum) they want to spend. From there, the results will show, where a user can see the name of the recipe and the link to the recipe. The user can then
save the recipe or text the link of the recipe to their phone. Users can also upload their own recipe to the database.


<h1>Technologies</h1>

<b>Tech Stack</b>: Python, JavaScript, HTML, CSS, Flask, Jinja, jQuery, PostgreSQL, SQLAlchemy, Bootstrap, Requests Library
APIs: Spoonacular, Twilio

<b> Installation </b>

<i>You must have the following installed to run Eureka: </i>

API key for Spoonacular and Twilio
PostgreSQL
Python3 
Requests Library
Cloudinary Library

Running Eureka on your computer:

Clone or fork repository:

$ git clone https://github.com/chantelyip/hb-project

Create and activate a virtual environment inside your hb-project directory:

$ virtualenv env
$ source env/bin/activate

Install dependencies:

$ pip install -r requirements.txt

Create a secrets.sh file and add your API keys and secret keys.

Add variables to your virtual environment:
$ source secrets.sh

Create database 'recipe':
$ createdb recipe
 

 
